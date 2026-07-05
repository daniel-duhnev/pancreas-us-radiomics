# Code Audit — Findings & Way Forward

**Date:** 2026-07-05
**Auditor:** independent read-only review (Claude Code)
**Scope:** `analysis/` notebooks (data pipeline + statistics + machine learning) and
reproducibility/environment. Thesis prose/wording was explicitly out of scope.
**Method:** every finding below was **verified against the actual code and data** with small
read-only Python/bash scripts (no files modified, no notebooks re-executed). Verification
commands are given inline so a future agent can re-confirm in minutes.

---

## 0. How to read this document

- Findings are triaged: **Critical** (submission-blocking / reproducibility break) →
  **Should-fix** (methodology an examiner will challenge) → **Minor** (hygiene).
- Each finding has: *What · Where (notebook + cell) · Evidence (verified) · Why it matters ·
  Way forward*.
- A **Refuted candidates** section at the end lists things that were checked and found to be
  non-issues, so nobody re-investigates them.
- Nothing here has been fixed. This is a findings report only.

### Project context (for a fresh agent)
- Goal: predict pancreas-transplant **rejection** (binary `RECHAZO CLÍNICO`) from radiomics
  texture features of grayscale B-mode ultrasound. Clinical ARFI/DCE-US replication of
  Bassaganyas et al. 2025 is the **positive control**.
- The headline scientific result is **negative and intended**: no radiomics feature survives
  FDR; all classifiers sit at chance (AUC ≈ 0.5). So the audit's job is to make sure that
  negative conclusion rests on sound, reproducible code — not to rescue a positive result.
- Datasets: "full" = **137 studies / 55 patients** (`reports/13_merged_radiomics_clinical.csv`);
  "independent" = **55 studies / 55 patients** (`reports/18_independent_dataset.csv`), a
  one-study-per-patient **subsample** of the 137 (NOT external data).
- Two parallel result families exist everywhere: original and `_normalised` (pyradiomics image
  normalisation). The **normalised** family is reported as primary in the thesis.
- Env: conda `thesis_env`, Python 3.9.25, interpreter
  `/home/daniduhnev/miniconda3/envs/thesis_env/bin/python`.

### Verified environment snapshot (live `thesis_env`, 2026-07-05)
```
numpy 1.26.4 · pandas 2.2.3 · scikit-learn 1.6.1 · scipy 1.13.1
pyradiomics 3.1.0 · SimpleITK 2.5.3 · opencv 4.10.0 · pydicom 2.4.4
```

---

## Severity summary

| ID  | Severity | One-line | Primary location |
|-----|----------|----------|------------------|
| C1  | **Critical** | Physical pixel spacing discarded → texture features confounded by scanner depth/zoom | `12_extract_radiomics_all_images*.ipynb` cell 4–5 |
| C2  | **Critical** | Analysis uses 137 studies; only 134 reproducible (3 raw studies lost, not in backup) | `reports/12_*`, `13_*`, manifest |
| C6  | **Should-fix (high)** | "Nested CV" is not nested — `k` + hyperparameters chosen on all data before the reported CV | `20_*`, `17b_*`, `22`, `23` |
| S3  | Should-fix | `normalize=True` normalises the whole (black-dominated) image, not the ROI; comment wrong | `12_..._normalised.ipynb` cell 5 |
| S4  | Should-fix | `binWidth` never set → pyradiomics default 25 on uncalibrated US intensities | `12_*` cell 5 |
| S5  | Should-fix | Edge-case masks integrated by a manual file copy; manifest says 0 px; guard warns but doesn't skip | `10_*`, `12_*` cell 2, manifest |
| S7  | Should-fix | No patient-grouped CV → 137-set CV leaks patients across folds | `15`, `17`, `17b` |
| S8  | Should-fix | Correlation pre-filter breaks ties with full-data p-values (supervised, outside CV) | `15,17,17b,20,22,23` cell 2 |
| S9  | Should-fix | Sens/spec reported at a Youden threshold tuned on the same CV predictions | `17,17b,20` (`compute_youden`) |
| S10 | Should-fix | "Independent dataset" is an outcome-driven subsample of the 137, not external validation | `18_*` cell 6 |
| S11 | Should-fix | No FDR on the clinical tests in `14b` (all) and `21` (clinical block) | `14b`, `21` cell 10 |
| S12 | Should-fix | `environment.yml` broken (numpy 2.0.2 incompatible; scikit-learn & scipy missing) | `environment.yml` |
| M1–M6 | Minor | data-snooping in exploratory NB17, warning suppression, stale NB19 narrative, absolute paths, etc. | various |

---

## CRITICAL

### C1 — Physical pixel spacing is discarded before radiomics extraction

**Where:** `analysis/12_extract_radiomics_all_images.ipynb` and
`analysis/12_extract_radiomics_all_images_normalised.ipynb`, `load_image_and_mask` (cell 4) and
extractor config (cell 5).

**What:** The image is built with `sitk.GetImageFromArray(gray)` (cell 4) — this assigns the
SimpleITK default spacing **(1, 1, 1)**. The extractor settings are
`{"force2D": True, "force2Ddimension": 0}` (cell 5) with **no `resampledPixelSpacing`** and the
code never calls `SetSpacing(...)`. So all texture features are computed in *pixel* units.

**Evidence (verified):** `PixelSpacing` is present in **all 134** DICOMs, isotropic, and varies
**0.1101 → 0.2948 mm** — 14 distinct values, **2.68× spread** — driven by US depth/zoom.
```bash
# re-verify:
/home/daniduhnev/miniconda3/envs/thesis_env/bin/python - <<'PY'
import os, pydicom
from collections import Counter
RAW="data/PANCREAS_2/PANCREAS_2"
vals=[]
for s in sorted(os.listdir(RAW)):
    d=os.path.join(RAW,s)
    if not os.path.isdir(d): continue
    for dp,_,fs in os.walk(d):
        for f in sorted(fs):
            if f.endswith('.png') or 'Zone.Identifier' in f: continue
            try:
                ds=pydicom.dcmread(os.path.join(dp,f),stop_before_pixels=True)
                vals.append(round(float(ds.PixelSpacing[0]),4)); raise StopIteration
            except StopIteration: break
            except Exception: continue
        else: continue
        break
print(len(vals),'studies; distinct=',len(set(vals)),'min',min(vals),'max',max(vals),'ratio',max(vals)/min(vals))
PY
```

**Why it matters:** A GLCM (and GLRLM/GLSZM/GLDM/NGTDM) 1-pixel offset corresponds to a
*different physical distance* in every patient. Texture features therefore encode the scanner
depth/zoom setting as much as the tissue. This is the classic IBSI ultrasound pitfall and one of
the first things a radiomics examiner checks. It weakens both the negative result (features are
noisy/confounded) and any claim of standards compliance.

**Way forward:**
1. Preferred: resample to a common isotropic spacing before extraction, e.g. set on the SITK
   image `img.SetSpacing((s, s))` from the real `PixelSpacing`, then extractor
   `settings["resampledPixelSpacing"] = [s0, s0, 1]` (pick a target ~median 0.155 mm),
   `interpolator=sitkBSpline` for image, nearest-neighbour for mask. Re-run NB12 (both variants)
   → NB13 → all downstream. Given results are null, this only pushes AUCs further toward 0.5 and
   *strengthens* the conclusion.
2. Minimum: if not re-running, state explicitly in Methods/Limitations that features are in pixel
   units and pixel spacing varies 2.7× across the cohort, and that this confounds texture scale.

---

### C2 — Analysis rests on 137 studies but only 134 are reproducible

**Where:** `analysis/reports/12_radiomics_features_k3_i1.csv`,
`12_radiomics_features_normalised.csv`, both `13_merged_radiomics_clinical*.csv`; the eroded-mask
manifest `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/manifest_eroded_CONTOUR_SUBTRACTED_k3_i1.csv`.

**What:** The committed feature and merged CSVs contain **137** studies. The raw data folder, the
manifest, and the mask folder each contain **134**. The 3 extra study IDs —
**`34_02`, `40_02`, `41_03`** — exist nowhere on disk: not under `data/PANCREAS_2/`, not in the
`data.zip` backup (which *does* contain the other 134 raw DICOMs, 406 path entries). They are
mid-sequence studies of patients whose siblings survive (`34_01/34_03`, `40_01/40_03`,
`41_01/41_02`), so this is almost certainly accidental loss (probably the Mac→WSL migration),
not an intentional exclusion.

Because `12_*` cell 6 iterates `manifest["study_id"]` (now 134 rows), **re-running the extraction
today produces 134 rows, not 137.** NB13 then merges to 134, NB18 subsamples from 134, etc. The
entire stats/ML chain was built on 137.

**Evidence (verified):**
```bash
/home/daniduhnev/miniconda3/envs/thesis_env/bin/python - <<'PY'
import os,csv
raw=set(d for d in os.listdir('data/PANCREAS_2/PANCREAS_2') if os.path.isdir('data/PANCREAS_2/PANCREAS_2/'+d))
ids=set(r['study_id'].strip() for r in csv.DictReader(open('analysis/reports/13_merged_radiomics_clinical.csv')))
print('raw',len(raw),'merged',len(ids),'in CSV not raw:',sorted(ids-raw))
PY
# -> raw 134 merged 137 in CSV not raw: ['34_02','40_02','41_03']
unzip -l data.zip | grep -cE "34_02|40_02|41_03"   # -> 0 (not in backup)
```

**Why it matters:** The reported numbers were computed when the data existed, so they aren't
necessarily *wrong* — but they are **unreproducible and unverifiable** (you can't re-check the
masks/segmentation for those 3, and a re-run yields a different n). The silent 137-vs-134
discrepancy (manifest 134, analysis 137) is exactly what a careful reviewer notices.

**Way forward (decide before doing any re-runs):**
1. Try to **recover** `34_02/40_02/41_03` raw DICOMs from an external/original source (hospital
   export, older backup drive). If recovered, drop them into `data/PANCREAS_2/PANCREAS_2/`, and
   regenerate mask (NB09) + manifest so everything is 137 and reproducible.
2. If unrecoverable, **drop them**, re-run NB12→NB13→NB18→all stats/ML to **n=134** (127? recount
   class balance), and update every count/table/figure in the thesis. Add a one-line provenance
   note.
Do **not** submit with the unexplained 137/134 mismatch.

---

## SHOULD-FIX (methodology an examiner can challenge)

### C6 — "Nested cross-validation" is not nested (optimistic bias)

**Where:** `analysis/20_ml_independent_dataset.ipynb` cells 7 & 9 (primary, n=55);
`17b_ml_joint_optimization.ipynb` optimisation cell (n=137); same pattern in
`22_alternative_texture_features.ipynb` and `23_surrounding_tissue_analysis.ipynb`; and both
`_normalised` twins.

**What (verified code):**
```python
gs = GridSearchCV(spec["pipe"], spec["grid"], cv=cv_inner, scoring="roc_auc").fit(X, y)  # ALL data
best_pipe = gs.best_estimator_
y_proba = cross_val_predict(clone(best_pipe), X, y, cv=cv_outer, method="predict_proba")[:,1]
```
`select__k` **and** the model hyperparameters (`C`, `max_depth`, `min_samples_leaf`, kernel,
`var_smoothing`) are chosen by `GridSearchCV.fit(X, y)` on the **entire dataset**, then the
"outer" 10-fold/LOOCV re-uses those fixed choices. Only the `StandardScaler` stats and the
*identity* of the selected features are refit per fold (because `SelectKBest` sits inside the
pipeline). The **k value and hyperparameters are contaminated by the test folds.** The notebook
comments call the LOOCV/10-fold result "unbiased" — it is not.

**Why it matters:** The reported AUCs (independent LogReg 0.569 non-norm / 0.636 norm; full-set
LOOCV values in `17b`) are optimistically biased. The bias is small here (grids are small, results
already null) but the *claim* of unbiased/nested CV is inaccurate — a defensible-methodology issue.

**Way forward:** make it truly nested by passing the whole search as the estimator:
```python
inner = StratifiedKFold(5, shuffle=True, random_state=42)
outer = StratifiedKFold(10, shuffle=True, random_state=42)
search = GridSearchCV(spec["pipe"], spec["grid"], cv=inner, scoring="roc_auc")
y_proba = cross_val_predict(search, X, y, cv=outer, method="predict_proba")[:,1]
```
Re-running will nudge AUCs toward 0.5, *supporting* the conclusion. At minimum, drop the words
"unbiased"/"nested" from code comments and thesis text.

---

### S3 — Whole-image z-score normalisation dominated by the black background

**Where:** `analysis/12_extract_radiomics_all_images_normalised.ipynb` cell 5.

**What (verified code + comment):**
```python
settings = {"force2D": True, "force2Ddimension": 0,
            "normalize": True, "normalizeScale": 100, "removeOutliers": 3}
# comment in the cell: "normalize=True applies per-ROI z-score normalisation"
```
pyradiomics `normalize=True` normalises using the mean/σ of the **entire image** (all voxels),
**not** the ROI — the code comment is factually wrong. The frames are ~768×1024 with a large
off-sector **black background** whose area ratio varies per image, so the per-image mean/σ (and
the `removeOutliers=3` σ-clip) are background-driven and inconsistent across patients — the
opposite of the gain-invariance normalisation is meant to provide.

**Why it matters:** The "normalised" family is the thesis's *primary* result, so the normalisation
being background-driven undermines its interpretation.

**Way forward:** fix the comment; if intensity normalisation is wanted, normalise **within the
ROI** or crop to the US sector first. NB23 already prototypes a surrounding-tissue normalisation —
reference/reuse that. State which variant is primary and why.

---

### S4 — `binWidth` never set (pyradiomics default 25 on arbitrary US intensities)

**Where:** `analysis/12_*` cell 5 (both variants).

**What:** Neither extractor sets `binWidth` or `binCount`, so pyradiomics uses the default
`binWidth=25`. On raw 8-bit grayscale (0–255) that is ~10 gray levels; on the normalised images
(`normalizeScale=100`, ±3σ) it is a *different, uncontrolled* bin count — so the two variants are
not discretised comparably. IBSI practice for uncalibrated modalities (ultrasound) is to fix and
report a **bin count**.

**Way forward:** set an explicit `settings["binCount"] = 32` (or 64), justify in Methods, re-run;
or, if not re-running, document the default and the raw-vs-normalised discretisation difference in
Limitations.

---

### S5 — Edge-case masks integrated out-of-band; manifest inconsistent; guard doesn't skip

**Where:** `analysis/10_handle_edge_cases.ipynb`; `12_*` cell 2 (zero-pixel guard) and cell 6
(loop); manifest.

**What (verified):** NB10 fixes masks for `03_01` and `43_01` (their drawn contours had gaps →
empty masks in the batch) and writes them to `data/PANCREAS_EDGE_CASES_FIXED/masks/`. But `12_*`
reads masks from the *eroded* folder under a different filename
(`{id}_mask_eroded_k3_i1.png`). On disk, the fixed masks were **manually copied + renamed** into
the eroded folder — confirmed by leftover Windows artifacts
`03_01_k3_i1_mask.png:Zone.Identifier` and `43_01_k3_i1_mask.png:Zone.Identifier` in
`.../ERODED_K3_I1/masks/`. Meanwhile the manifest **still records `03_01`/`43_01` as
`orig_pixels=0, eroded_pixels=0`**, and `12_*` cell 2's zero-pixel check only **prints a WARNING**
— it does not skip. Extraction proceeds and succeeds *only because* a non-empty file happens to
exist at the expected path.
```bash
ls "data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/masks/" | grep Zone.Identifier
# 03_01_k3_i1_mask.png:Zone.Identifier , 43_01_k3_i1_mask.png:Zone.Identifier
```

**Why it matters:** Not reproducible. Re-running NB09→NB12 alone (without the manual copy) yields
empty ROIs for `03_01`/`43_01` → pyradiomics errors or silently garbage features. The manifest is
internally inconsistent.

**Way forward:** make the integration a **code step** — have NB10 write the fixed eroded masks
directly into `.../ERODED_K3_I1/masks/` with the correct name **and** update the manifest's
`orig_pixels/eroded_pixels/lost_pct` rows for `03_01`/`43_01`. Change the guard in `12_*` cell 2/6
to a hard `continue`/skip on zero-pixel masks. Delete the `:Zone.Identifier` files.

---

### S7 — No patient-grouped cross-validation (137-set leaks patients across folds)

**Where:** `15_feature_selection_and_ml.ipynb`, `17_ml_sequential_experiments.ipynb`,
`17b_ml_joint_optimization.ipynb` (all operate on the 137-study set).

**What (verified):** `grep` across every notebook finds **no** `GroupKFold`,
`LeaveOneGroupOut`, `StratifiedGroupKFold`, or `groups=`. The 137-set notebooks use
`StratifiedKFold`/`LeaveOneOut` on **studies**. 55 patients contribute a mean of **2.5** studies
(up to 6), and 14 patients have both outcomes — so a patient's studies land in train and test
folds simultaneously. `patient_id` is already carried into `13_merged_*`, so the fix is available.
(The 55-study notebooks — `19,20,22,23,24,25` — are patient-clean only because they are one study
per patient.)

**Why it matters:** Any positive result on the 137-set would be inflated. Results here are null,
so no false positive was created, but the leakage undermines the validity of the 137-set AUCs.

**Way forward:** use `StratifiedGroupKFold(n_splits=..., ...).split(X, y, groups=patient_id)` on
the 137-set (and pass `groups` through `cross_val_predict`/`GridSearchCV`). Or, since the docs
already demote the 137-set analyses to the appendix, make the demotion reason explicit ("not
patient-grouped → optimistic"). LOOCV on the 137-set is *worse* than it looks: it leaves out one
study while the same patient stays in training.

---

### S8 — Supervised feature pre-filter outside the CV

**Where:** correlation-removal block, `15` cell 4; `17` cell 2; `17b` cell 2; `20` cell 2; `22`
cell ~20; `23` cell ~28.

**What (verified code):** for each |Pearson| > 0.9 pair, drop the feature with the **higher
univariate p-value**, where p-values come from `14a`/`19` computed on the **full labelled
dataset**:
```python
p_values = dict(zip(stats_df["feature"], stats_df["p_value"]))   # full-data p-values
...
if p_values.get(fi,1.0) <= p_values.get(fj,1.0): to_drop.add(fj)
else: to_drop.add(fi)
```
Label information enters feature reduction before the CV split.

**Why it matters:** Small impact (it only chooses which of two near-duplicate features to keep),
but inconsistent with the leakage-free framing and layered on top of C6.

**Way forward:** break ties with a **label-free** rule (keep the feature with lower mean absolute
correlation to the rest, or simply the first), or move the entire correlation filter inside the CV
fold. If left as-is, note it as a minor limitation.

---

### S9 — Operating-point sensitivity/specificity tuned on the evaluation data

**Where:** `compute_youden` in `17`, `17b`, `20` (and normalised twins).

**What (verified code):**
```python
J = tpr - fpr; best = np.argmax(J)     # threshold from the SAME pooled CV/LOO probabilities
return {"sensitivity": tpr[best], "specificity": 1-fpr[best], ...}
```
The threshold that maximises Youden's J is chosen on the pooled out-of-fold probabilities, then
sensitivity/specificity are reported at that same threshold.

**Why it matters:** AUC is unaffected, but the reported sens/spec are optimistic (in-sample
operating point).

**Way forward:** select the threshold inside each training fold, or clearly label reported
sens/spec as "at the AUC-optimal (Youden) operating point, in-sample."

---

### S10 — "Independent dataset" (55) is an outcome-driven subsample, not external validation

**Where:** `18_build_independent_dataset.ipynb` cell 6 (selection) and cell 8 (asserts).

**What (verified code):**
```python
for pid, group in df.groupby("patient_id"):
    group_sorted = group.sort_values("study_id")
    if len(group["rejection"].unique()) == 1:
        pick = group_sorted.iloc[0]                         # single outcome: first study
    else:
        pick = group_sorted[group_sorted["rejection"]==1].iloc[0]   # both: first REJECTION study
```
So the 55-set is (i) a **subset of the 137 training pool**, not held-out data, and (ii)
**outcome-conditioned** — it forces the rejection study for all 14 dual-outcome patients (asserted
in cell 8: "all 14 dual-outcome patients have rejection study selected"), enriching rejection and
preferentially picking early studies. "First by `study_id`" also assumes study_id order = temporal
order.

**Why it matters:** The words "independent" and "validate" risk being read as external validation.
It is a repeated-measures-free subsample. The selection is non-random and label-dependent, which
biases class balance and timepoint mix. Also note **NB21 (paired) selects a different study per
patient** (max-separated pair), so "the rejection study" is not consistent across analyses.

**Way forward:** keep the analysis (it correctly satisfies the independence assumption for
stats/CV) but rename/reframe: "one-study-per-patient subsample," never "external validation."
Acknowledge the outcome-conditioned, non-random selection as a limitation and note the
inconsistency with NB21's pairing.

---

### S11 — Missing multiple-comparison correction on the clinical tests

**Where:** `14b_stats_clinical_features.ipynb` (all clinical features);
`21_paired_analysis.ipynb` cell 10 (clinical block).

**What (verified):** `multipletests` is **imported but never called** in `14b`
(0 call sites) — 17 ARFI/DCE-US features reported at raw p<0.05. In `21`, BH-FDR is applied to the
**radiomics** block (cell 7) but **not** to the **clinical** block (cell 10 computes Wilcoxon
p-values only). Every sibling notebook (`14a`, `19`, `24`, `25`, and 21-radiomics) applies FDR.
```bash
# call-site count (import vs actual call):
grep -oE "multipletests\(" analysis/14b_stats_clinical_features.ipynb | wc -l   # -> 0
grep -oE "multipletests\(" analysis/21_paired_analysis.ipynb | wc -l            # -> 1 (radiomics only)
```

**Why it matters:** Inconsistent statistics an examiner will spot. The `14b` omission *may* be a
deliberate replication of Bassaganyas (who reported uncorrected p) — but that must be stated. The
`21`-clinical omission looks like an oversight.

**Way forward:** add BH-FDR to `21`'s clinical block for consistency. For `14b`, either add FDR or
add a sentence next to the table stating the omission is intentional to mirror Bassaganyas et al.

---

### S12 — `environment.yml` cannot recreate the working environment

**Where:** `environment.yml` (repo root).

**What (verified):** the file pins `numpy==2.0.2`, `pandas==2.3.3`, `pyradiomics==3.1.0`,
`simpleitk==2.5.3`, and **omits scikit-learn and scipy entirely** — yet the ML/stats notebooks
depend on both. The live working env is numpy **1.26.4** / pandas 2.2.3 / scikit-learn 1.6.1 /
scipy 1.13.1. numpy 2.0.2 is ABI-incompatible with this pyradiomics/SimpleITK stack.

**Why it matters:** Anyone (examiner, future you) building from this file gets a broken env; the
two libraries the ML relies on aren't even declared. Ties directly into C2 (reproducibility).

**Way forward:** regenerate from the live env and verify a clean install runs NB12 + NB20:
```bash
conda env export -n thesis_env --no-builds > environment.yml   # then hand-trim the prefix line
```

---

## MINOR (hygiene — fix if time permits)

- **M1 — Data snooping in exploratory NB17.** `17_ml_sequential_experiments.ipynb` Exp2 fits
  Boruta on `X_scaled` (whole data, cell 8) and computes permutation-importance ranking on the
  whole data (cell 9), then selects the feature-subset **size** by `best_n = argmax(LOOCV AUC)` —
  optimising directly on the evaluation metric. NB17's own header calls the approach flawed and it
  is superseded by NB17b. Keep it clearly labelled exploratory/appendix.
- **M2 — Global `warnings.filterwarnings("ignore")`** in the ML notebooks (`17,17b,20,22,23`) can
  hide real warnings (convergence, undefined metrics). Scope it or review warnings once.
- **M3 — Stale saved narrative.** NB19's committed markdown says "4 features" while the CSV/thesis
  use 24 (normalised primary). Re-run or edit so the saved notebook matches reported numbers.
- **M4 — Absolute machine paths** baked into the manifest (`source_image` =
  `/home/daniduhnev/.../...png`) — non-portable; regenerate with relative paths.
- **M5 — `find_dicom_path` uses unsorted `os.listdir()[0]`** for the date subfolder and file —
  nondeterministic *if* a study ever holds >1 file. Verified all 134 studies have exactly 1 image
  file, so harmless today; sort for safety.
- **M6 — `11_extract_radiomics_for_one_test_image.ipynb`** uses a bare default extractor (no
  force2D/normalize, only glcm+firstorder), so it does not validate the batch config — fine as a
  smoke test, just don't cite its numbers.

---

## Checked and REFUTED (confirmed NON-issues — do not re-investigate)

- **YBR vs RGB colour space:** all 134 DICOMs are `PhotometricInterpretation = RGB`, so
  `cv2.cvtColor(..., COLOR_RGB2GRAY)` in `12_*` cell 4 is correct (no luminance distortion).
  Verified by reading the tag on every study.
- **CSV BOM breaking the merge:** `data/bd_estudiUPF.csv` *does* start with a UTF-8 BOM
  (`\xef\xbb\xbf`), but current pandas strips it — `pd.read_csv(...).columns[0] == 'id estudio'`
  and `df['id estudio']` works. No bug on this env (would matter only under a different reader).
- **`SelectKBest` k grid exceeding feature count:** the `k` grids exactly match the reduced feature
  counts — independent set reduces 93 → **31** (grid max = 31), full set reduces 93 → **32** (grid
  max = 32). No silent clamp; the grids were deliberately sized.
- **Cross-patient leakage inside feature extraction / image normalisation:** extraction and (image)
  normalisation are strictly per-image, so there is no leakage in that stage. All ML leakage lives
  in the split notebooks (C6/S7/S8).

---

## Suggested execution order for a follow-up agent

Given a few weeks to submission and a **null** headline result, prioritise reproducibility and
defensibility over chasing performance:

1. **C2 first** — decide recover-vs-drop the 3 studies; it changes `n` and every downstream number.
2. **S12** — regenerate `environment.yml`; verify a clean env runs NB12 + NB20 (unblocks all re-runs).
3. **C1 + S4 + S3** — one coordinated re-extraction pass on NB12 (both variants): add
   `resampledPixelSpacing`, set `binCount`, fix the normalisation scope/comment. Then re-run
   NB13 → stats → ML. Expect AUCs to move *toward* 0.5 (supports the thesis).
4. **C6 + S8 + S9** — mechanical CV/leakage fixes in `17b,20,22,23` (and normalised twins):
   proper nested CV, label-free correlation tie-break, in-fold thresholding.
5. **S7** — add `StratifiedGroupKFold(groups=patient_id)` to the 137-set notebooks, or document why
   they are appendix-only.
6. **S11 + S5** — add FDR to `21` clinical (and decide on `14b`); make the edge-case mask
   integration a code step and fix the manifest.
7. **Minors** as time allows.

After any re-run, re-verify the counts with the Stage-0 snippets above and update the thesis
tables/figures. Scripts used for this audit were read-only and left in the session scratchpad;
they are reproduced inline here so nothing external is needed.
