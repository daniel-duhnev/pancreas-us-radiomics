# Plan: Independent-Dataset Restructure + WSL Migration Recovery

**Updated:** 2026-07-03
**Status:** Stage 0 DONE, Stage 1 DONE, Stage 2 + 3 PENDING
**Owner:** Daniel (with agent assistance)

This is the active plan for the final thesis stretch. It supersedes the "Phase 3" section
of [PLAN_GEMMA_FEEDBACK_RESPONSE.md](PLAN_GEMMA_FEEDBACK_RESPONSE.md), which was blocked on a
supervisor meeting. The blocking questions are now resolved (see Decisions below).

## Context

Two threads are being closed out:

1. **Machine migration (Mac to Lenovo/WSL2, months later).** The environment works and the
   thesis compiles, but the gitignored `analysis/reports/` lost all computed result CSVs, three
   Python packages were missing, and `CLAUDE.md` had the old Mac Python path. Recovered in
   Stage 0. See [wsl-migration notes below](#migration-notes).

2. **Supervisor-mandated restructure (Gemma).** Standard statistical tests and cross-validation
   assume independent observations. Because many patients contribute several studies, analyses
   on all 137 studies violate independence (and the full-dataset ML has patient-level leakage:
   LOOCV leaves out one study, not one patient). This is the same flaw as the Bassaganyas et al.
   tabular paper, which reused same-patient timepoints as if independent. The fix: make the
   independent 55-patient dataset (one study per patient) the primary basis for the main body,
   and keep the full 137-study analysis as a concise appendix.

## Decisions (locked in)

- **Main body = independent 55; appendix = full 137.** Every core analysis in the main body
  rests on the independent dataset; the full-dataset radiomics stats, radiomics stratification,
  and radiomics ML move to a new appendix chapter, written concisely (assumes reader already
  has context from the main body).
- **Restore, do not recompute.** The Mac-computed report CSVs exactly match the numbers already
  written in the thesis. They were restored via copy. Existing pipeline notebooks (12-23) are
  NOT re-run, to avoid any risk of breaking things in the final stretch. Only genuinely new
  analyses are computed.
- **Clinical replication stays in the main body** (full 138 studies, framed as a Bassaganyas
  replication and pipeline validation - it carries the positive late-period ARFI result), AND a
  new independent-55 clinical analysis is added alongside it.
- **Radiomics time-stratification is redone on the independent 55** (days-based, 90-day cutoff)
  for the main body; the motivo-based full-137 stratification moves to the appendix.
- **New analyses live in new standalone notebooks** (NB 24, NB 25); no existing notebook is
  edited.

---

## Stage 0 - Restore data + fix environment (DONE, 2026-07-03)

- Restored `analysis/reports/` from the verified backup at
  `/mnt/c/Users/Daniel/Downloads/master-thesis 2 (1)/master-thesis/pancreas-us-radiomics/analysis/reports/`
  (46 CSVs + 34 PNGs). `reports/` is gitignored, so this produced no tracked changes. The 4
  original repo files were preserved (no collisions).
- Installed missing packages into `thesis_env`: `statsmodels`, `scikit-image`, `boruta` (plus
  `nbformat`, `nbclient` for executing the new notebooks). Core scientific libraries
  (numpy 1.26.4, pandas 2.2.3, scikit-learn 1.6.1, scipy 1.13.1, pyradiomics 3.1.0) were NOT
  changed. Added the first three to `environment.yml`.
- Fixed the `CLAUDE.md` Python path to `/home/daniduhnev/miniconda3/envs/thesis_env/bin/python`.
- **Restore-consistency verified:** recomputing the independent radiomics stats on this machine
  reproduces the thesis numbers exactly (top feature `firstorder_90Percentile` p=0.004, 24
  features p<0.05, min FDR 0.156; LogReg 10-fold AUC 0.636; ARFI mediana p=0.028).

---

## Stage 1 - Two new independent-dataset analyses (DONE, 2026-07-03)

Both are new standalone notebooks that read restored CSVs plus `data/bd_estudiUPF.csv` and
write new report CSVs. They mirror existing, verified code (NB 14b and NB 19). They do not
touch any existing notebook.

### NB 24 - Clinical features on the independent dataset
`analysis/24_clinical_stats_independent.ipynb`
- Filters the clinical spreadsheet to the 55 independent study ids, runs Mann-Whitney per
  feature (rank-biserial effect size), and adds a Benjamini-Hochberg FDR column for
  completeness (uncorrected p is the headline, matching the full-dataset clinical table).
- Output: `reports/24_clinical_stats_independent.csv` (17 rows) and
  `reports/24_boxplots_clinical_independent.png`.
- **Result: no clinical feature is significant, not even uncorrected.** ARFI mediana p=0.69,
  ARFI media p=0.77, contrasting with the full dataset (ARFI mediana p=0.028) and the late
  period (ARFI p<0.001). This is consistent with the thesis: the ARFI signal is specific to the
  late post-transplant period, and the independent selection favours first-rejection studies
  (often early), so pooling across time dilutes the effect. Mirrors the paired analysis (NB 21).

### NB 25 - Time-stratified radiomics on the independent dataset
`analysis/25_radiomics_stratified_independent.ipynb`
- Attaches `Días pTXP`, splits the 55 into early (<= 90 days, n=42) and late (> 90 days, n=13),
  and runs the NB 14a per-feature procedure (Shapiro-Wilk, Welch or Mann-Whitney, FDR) in each.
- Output: `reports/25_radiomics_stratified_independent_early.csv` and `..._late.csv` (93 rows each).
- **Result: no feature survives FDR in either subgroup** (early: 1 uncorrected hit; late: 1
  uncorrected hit). The late subgroup is small (6 no-rejection vs 7 rejection) and underpowered;
  reported as a robustness check. Consistent with the null radiomics finding.

---

## Stage 2 - Thesis restructure (PENDING) - DETAILED EDIT PLAN

Depends on Stage 1 outputs. Do the edits in the order below (methods first, then results,
then appendix, then discussion/abstract, then compile). Floats use `\label`/`\ref` and are
globally numbered, so moving them auto-renumbers; do not hand-edit any numbers.

Verified numbers to use (from the executed notebooks and the restored CSVs):
- Independent radiomics stats (primary, already in text): 55 studies (34 NR, 21 R); 45 Welch,
  48 Mann-Whitney; 24 features p<0.05; top `firstorder_90Percentile` p=0.004 (r=-0.47); none
  survive FDR (all q>=0.16).
- Independent stratified (NB 25): early <=90d n=42 (28 NR, 14 R) -> 1 uncorrected hit
  (`firstorder_RootMeanSquared` p=0.044), 0 FDR; late >90d n=13 (6 NR, 7 R) -> 1 uncorrected hit
  (`firstorder_Maximum` p=0.038), 0 FDR.
- Independent clinical (NB 24): 55 studies (34 NR, 21 R); ARFI available 47/55, DCE-US 54/55;
  0 features significant (uncorrected or FDR); ARFI mediana p=0.69, ARFI media p=0.77; smallest
  p is RT=0.060. Timing reason: only 7 of the 21 independent rejection studies are late (>90d),
  and the ARFI signal is late-specific.

### Step 2.1 - methods.tex (additive/reframing, low risk; do first)

1. **Add "Independent Dataset Construction" (new subsection in Section~\ref{sec:statistical_analysis},
   before the stratification paragraph).** This currently does NOT exist and must, because the
   independent dataset is now primary. Describe: to satisfy the independence assumption, one
   study per patient was selected; for the 14 patients with both outcomes the first rejection
   study was chosen, otherwise the first study; yielding 55 studies (34 NR, 21 R). Reference the
   repeated-measures note in Section~\ref{sec:dataset}. (Source: NB 18.)
2. **Reframe the stratification paragraph (methods lines ~155-160).** State that the primary
   radiomics stats and the time-stratified radiomics analysis are performed on the independent
   dataset, with the time split based on actual days post-transplant (<=90 vs >90 days, matching
   Bassaganyas and the clinical late-period analysis). Move the motivo-based full-dataset
   stratification description into an appendix-facing sentence (it is exploratory).
3. **Clinical paragraph (methods line ~162):** add one sentence that the 17 clinical features
   were additionally tested on the independent 55-study subset (one per patient) as an
   independence check, complementing the full-dataset replication.
4. **ML Evaluation Strategy (methods lines ~197-206):** add that the independent dataset (one
   study per patient) is the primary, leakage-free evaluation; note the full-dataset LOOCV
   leaves out one study rather than one patient, so a patient's other studies can appear in
   training - a patient-level leakage that makes the full-dataset ML exploratory (reported in the
   appendix). Clarify the outer CV: 10-fold on the independent dataset, 5-fold on the full
   dataset (matching the results text). Keep the metric descriptions.
5. **Scanner model (methods line 8 and Table `tab:dataset_summary`):** replace the generic
   "Siemens ultrasound system" with "Siemens Acuson S3000 Helx, with convex (1-4.5 MHz) and
   linear (4-9 MHz) multifrequency probes", cited to Bassaganyas et al. Verified: the DICOM tag
   `ManufacturerModelName` is `syngo.via.VB80E` (the Siemens export/post-processing software, not
   the scanner), while the Bassaganyas paper - the same patient cohort - states the acquisition
   scanner explicitly.

Note on step ordering: do the methods edits WITHOUT forward-referencing `app:full_dataset`
(that label is created in Step 2.3). Methods establishes the full dataset as "exploratory"; the
explicit `\ref{app:full_dataset}` cross-references live in results.tex (Step 2.2). This keeps
methods independently compilable after Step 2.1.

### Step 2.2 - results.tex (the main restructure)

Section 3.2 (Radiomics Statistical Analysis):
- **Remove** the "Full Dataset" subsection (text + `tab:radiomics_top10`) and the motivo
  "Stratified Analysis" subsection -> move to appendix (Step 2.3).
- **Promote** the "Independent Dataset" content to primary: drop the follow-up framing opener
  ("To address the potential confound of repeated measures, the same analysis was performed...")
  and make it the primary analysis. Keep the 24-feature result and `fig:boxplots_radiomics`
  (already N=55).
- **Add** subsection "Time-Stratified Analysis" (NB 25 numbers above) with a small summary
  table and the small-late-subgroup caveat.
- **Add** one pointer sentence: exploratory full-dataset stats are in Appendix~\ref{app:full_dataset}.

Section 3.3 (Clinical Feature Replication): keep Full Dataset / Late Period / Replication
subsections unchanged (legitimate Bassaganyas replication).
- **Add** subsection "Independent Patient Analysis" (NB 24): a 17-row table like
  `tab:clinical_full` with an added FDR column, plus 2-3 sentences: no feature significant, ARFI
  mediana p=0.69, and the timing explanation (only 7 of 21 independent rejection studies are
  late). Cross-link to the paired analysis (Section~\ref{sec:paired_results}).

Section 3.4 (Machine Learning Classification):
- **Remove** the "Full Dataset" subsection (text + `tab:ml_full` + `fig:roc_full`) -> appendix.
- **Promote** the "Independent Dataset" ML content to primary; reword the opener.
- **Add** pointer to the appendix. Update the closing paragraph ("across both datasets") to
  "on the independent dataset ... (the full-dataset exploratory analysis in
  Appendix~\ref{app:full_dataset} agrees)".

Cross-references to fix inside results.tex:
- Paired analysis paragraph ("In the full-dataset analysis, `firstorder_Minimum` ranked
  highest") -> add `(Appendix~\ref{app:full_dataset})`.
- Sections 3.6 (Alternative) and 3.7 (Surrounding) stay as-is (supplementary robustness checks;
  Gemma did not flag them; they already report the independent dataset).

### Step 2.3 - appendix.tex (new chapter)

Add `\chapter{Full-Dataset Exploratory Analysis}\label{app:full_dataset}` (place it as the first
appendix chapter). Intro caveat: 137 studies, multiple per patient; standard tests and CV assume
independence; the full-dataset LOOCV leaves out a study not a patient (patient-level leakage);
included for completeness; same negative conclusion as the primary independent analysis. Then
paste the moved blocks: full-dataset radiomics stats text + `tab:radiomics_top10`; motivo
stratified paragraph; full-dataset ML text + `tab:ml_full` + `fig:roc_full`. Keep existing
appendix chapters (independent 93-feature longtable `app:full_features`, and `app:pyradiomics_config`).

### Step 2.4 - discussion.tex and abstract.tex (reframing)

- discussion "Negative Radiomics Result" (line ~8): reorder the list so the independent dataset
  is primary and the full-dataset is exploratory/appendix; keep the robustness narrative.
- discussion "Paired Analysis" subsection: add a sentence that the independent-dataset clinical
  analysis (NB 24) also found ARFI non-significant, corroborating the between-patient / late-
  period interpretation.
- discussion Limitations "Repeated measures" (line ~54): note the full-dataset analyses are now
  reported as exploratory in the appendix; the primary analyses use the independent dataset.
- discussion Conclusions objectives 2 and 3: reword "two independent datasets" / "full dataset"
  phrasing so the independent dataset reads as primary (the full dataset is not "independent").
- abstract: reword "the analysis was extended with an independent dataset" so the independent
  dataset reads as the primary analysis and the full dataset as supplementary. Keep scientific
  claims. (Adding the independent-clinical null to the abstract is optional - decide during edit.)
- introduction objectives: quick consistency check that objective wording does not present the
  full dataset as primary.

### Step 2.5 - compile and verify

- `cd thesis && latexmk -pdf -interaction=nonstopmode -halt-on-error MasterThesis.tex`
- Check: 0 errors; grep log for `LaTeX Warning: Reference` and `Citation undefined` (expect
  none); no `??` in the PDF; the main body has no full-dataset radiomics/ML subsection; the new
  appendix chapter exists; List of Tables / List of Figures reordered cleanly.
- Read the rendered Results and Appendix chapters end to end for flow and correct numbers.

### Resolved content decisions (2026-07-04)

- **Abstract framing:** reframe so the independent dataset is the primary basis for the thesis's
  scientific claims (radiomics and ML null on independent data). The clinical positive result
  stays in the main body but is presented explicitly as a POSITIVE CONTROL / pipeline validation
  (reproducing Bassaganyas using their non-independent methodology), NOT as an independent
  discovery claim. Keep the timing nuance: ARFI discriminates only in the late period, and the
  pooled-independent clinical result is null partly because only 7 of 21 independent rejection
  studies are late. Rationale: non-independent data is unpublishable when used to ASSERT an
  effect (a discovery claim); it is legitimate as a positive control that validates the pipeline.
  So the discovery claims (radiomics, ML) are independent-only; the clinical replication is a
  labelled validation.
- **Motivo-based clinical paragraph (Section 3.3):** leave as-is. Trimming saves ~3 lines and
  risks inconsistency; the existing text already explains the days-vs-motivo distinction.
- **Scanner model:** RESOLVED. Siemens Acuson S3000 Helx (convex 1-4.5 MHz, linear 4-9 MHz),
  per Bassaganyas et al. (same cohort). DICOM only records the syngo.via export software.

## Stage 3 - Finish and polish (PENDING, mostly Daniel)

- Write `dedication.tex` and `acknowledgements.tex` (template placeholders).
- Full proofread, verify PDF rendering, final compile, send to Gemma.

---

## New-analysis results summary

| Analysis | Dataset | Uncorrected p<0.05 | Survives FDR | Note |
|----------|---------|--------------------|--------------|------|
| Clinical (NB 24) | Independent 55 (pooled) | 0 / 17 | 0 | ARFI mediana p=0.69 (vs 0.028 full, <0.001 late) |
| Radiomics early (NB 25) | Independent, <= 90 days (n=42) | 1 / 93 | 0 | top firstorder_RootMeanSquared p=0.044 |
| Radiomics late (NB 25) | Independent, > 90 days (n=13) | 1 / 93 | 0 | small subgroup; top firstorder_Maximum p=0.038 |

<a name="migration-notes"></a>
## Migration notes and known issues

- **`environment.yml` is stale beyond the Stage 0 additions.** It lists numpy 2.0.2 / pandas
  2.3.3 (actual env: 1.26.4 / 2.2.3) and OMITS scikit-learn and scipy, so recreating the env
  from it elsewhere would produce a broken env. The live `thesis_env` works and is what runs
  notebooks; notebooks never read `environment.yml`. Regenerate from the live env
  (`conda env export`) if reproducibility on a fresh machine is needed. Not a blocker.
- **NB 19 saved markdown is stale.** Its interpretation cell reports the original (non-normalised)
  count of 4 uncorrected features and old top features; the saved CSV and the thesis use the
  normalised run (24 features, top `firstorder_90Percentile`). The code is correct and
  reproduces the thesis numbers; only the narrative cell was never refreshed. Cosmetic.
- **Mac paths in notebooks are in saved outputs only** (historical logs), not in code. Harmless.

## Related docs

- [REPORTS_GUIDE.md](REPORTS_GUIDE.md) - report CSV inventory (includes NB 24 and 25 outputs)
- [PLAN_GEMMA_FEEDBACK_RESPONSE.md](PLAN_GEMMA_FEEDBACK_RESPONSE.md) - the 17-point feedback plan
- [PLAN_THESIS_FINAL_STEPS.md](PLAN_THESIS_FINAL_STEPS.md) - polishing checklist
- [MACHINE_MIGRATION_GUIDE.md](MACHINE_MIGRATION_GUIDE.md) - migration procedure
