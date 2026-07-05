# Plan: Evaluate Gemma's Wavelet / LoG Suggestion

**Updated:** 2026-07-04
**Status:** RESEARCH DONE, decision PENDING (Daniel to decide whether to implement)
**Owner:** Daniel (with agent assistance)

This is a decision-support document, not an active work order. It exists so that if
Daniel later decides to act on Gemma's wavelet/Laplacian-of-Gaussian suggestion, the
research, feasibility, and exact implementation steps are already worked out. No thesis
or code changes have been made for this.

## Context

The thesis is content-complete, restructured around the independent 55-patient dataset,
and compiles cleanly (81 pp). The only open scientific question is Gemma's suggestion:

> "In a different study of radiomics, we found that the radiomics features that
> discriminate were not those extracted directly from the image but those from
> wavelet-filtered images and Laplacian of Gaussian filtered images at different
> sigmas. Maybe you can try that as well."

**What she means, technically:** PyRadiomics can apply *image-type filters* before
feature extraction. Instead of extracting the 93 features from the raw image only
(`imageType: Original`), you also enable `Wavelet` (PyWavelets) and `LoG` (Laplacian of
Gaussian at several sigma values, via SimpleITK). Each filtered image yields the full
feature set again, so the feature count multiplies. Enabled by one or two lines in the
extraction config.

**Why she suggests it:** several influential radiomics papers (e.g. Aerts et al.
lung/H&N; a 2023 HCC CT study) report wavelet-derived features among the *most*
discriminative — sometimes more than original-image features.

**The catch (decisive for us):** the best-designed benchmark on exactly this question,
Demircioglu 2022 (*Eur Radiol Exp* 6:40), tested 8 preprocessing filters (incl. wavelet
+ LoG) across 7 datasets with 5 selectors x 5 classifiers and found they do **not**
reliably improve predictive performance — the filtered features are highly correlated
with the originals while inflating dimensionality by up to 10x. At our n = 55 with FDR
correction, added dimensionality is a liability, not an asset.

## Key technical findings (PyRadiomics docs + literature)

1. **LoG is effectively blocked on our data.** PyRadiomics' LoG is a *3D* filter.
   Official docs: *"the image size must be at least 4 voxels in each dimension; if this
   constraint is not met, no LoG derived images can be generated."* Our images are
   single 2D ultrasound slices stored as depth-1 volumes, so LoG would be skipped
   entirely. Making it work would require true 3D volumes, which do not exist for this
   cohort. **=> LoG is off the table.**

2. **Wavelet on a single slice is uncertain.** PyRadiomics wavelet uses a 3D stationary
   wavelet transform (`_swt3`). On a depth-1 image it may (a) work in-plane and yield 4
   decompositions (LL/LH/HL/HH), or (b) error / need reshaping. Needs a ~30-min
   spike-test on ONE image before any commitment.

3. **The spirit of Gemma's idea is ALREADY in the thesis.** Section
   `sec:alternative_results` extracts Gabor filter responses and Laws' texture energy —
   both are *filtered-image* features in the same family as wavelet subbands. They were
   also null. Strong defense point: "I tested filter-based features (Gabor, Laws');
   wavelet is the one filter family I did not add, and the literature predicts it would
   not change the conclusion."

4. **Feature explosion math (if wavelet works in 2D):** ~4 decompositions x 93 = ~372
   wavelet features, added to the 93 originals => ~465 features on 55 patients. FDR over
   ~465 correlated features on n = 55 is near-certain to yield zero survivors,
   consistent with every other analysis in the thesis.

## Options

### Option A — Do NOT implement; strengthen the write-up (RECOMMENDED)
Lowest risk, highest value-per-hour, and fully defensible.

- Keep the existing brief mention in `discussion.tex` (the "Single PyRadiomics
  configuration" limitation already names wavelet/LoG).
- Add 2-3 sentences that: (a) acknowledge Gemma's point and cite Aerts et al. for
  wavelet features being discriminative in some domains; (b) note the thesis already
  probes filter-based features via Gabor and Laws' (Section `sec:alternative_results`),
  both null; (c) cite Demircioglu 2022 that added wavelet/LoG features do not reliably
  improve performance and mainly inflate dimensionality — a liability at n = 55;
  (d) state the technical constraint that PyRadiomics LoG needs >= 4 voxels/dimension,
  incompatible with single-slice 2D data.
- Add one BibTeX entry (Demircioglu 2022; optionally Aerts 2014).
- **Effort: ~1-2 hours, pure writing. Zero code/data risk. Recompile + proofread.**

### Option B — Implement WAVELET only (fallback, if Daniel wants the numbers)
LoG stays excluded (technically blocked). Expected null result. Follow the SAME
conservative pattern used for NB24/NB25: **add new standalone notebooks; do NOT modify
or re-run any existing verified notebook or overwrite any restored CSV.**

- **B0. Spike-test (~30 min):** scratch notebook, one image, add
  `extractor.enableImageTypeByName('Wavelet')` to the existing NB12 settings, run
  `extractor.execute(...)`, confirm `wavelet-*` columns come back on a depth-1 array
  without error. **If it errors -> stop, fall back to Option A.**
- **B1.** New extraction notebook `26_extract_radiomics_wavelet_normalised.ipynb`
  (clone `12_extract_radiomics_all_images_normalised.ipynb` + the one wavelet line);
  extract all 137 studies -> `reports/26_radiomics_wavelet_normalised.csv`.
  **Sanity-gate:** its `original_*` columns must match `12_..._normalised.csv` exactly.
- **B2.** New build notebook: left-join `wavelet-*` columns onto
  `reports/18_independent_dataset_normalised.csv` by `study_id` ->
  `reports/26_independent_wavelet_normalised.csv`.
- **B3.** New stats notebook (clone NB19), widen the one selection line to
  `startswith(("original_", "wavelet-"))`; Shapiro -> Welch/Mann-Whitney -> BH-FDR loop
  is unchanged. Output `reports/26_stats_wavelet_independent.csv`.
- **B4.** New ML notebook (clone NB20): same widened line; ALSO raise the hardcoded
  `k_values = [5, 10, 15, 20, 31]` for the larger feature set. Correlation filter +
  `SelectKBest` + bootstrap CI already loop off `feature_cols`. Output
  `reports/26_ml_wavelet_independent.csv`.
- **B5.** Write-up: short new results subsection (independent-primary), one Methods
  sentence, fold outcome into the Discussion limitation; full-dataset version to the
  appendix if a full-137 variant is also run.
- **Effort: code is small (single-line prefix edits + bumped `k`); real costs are the
  wavelet-2D spike, re-extraction runtime, and write-up/verification near the defence.
  ~1 focused day if the spike passes. Expected outcome: another null.**

### Option C — Wavelet + LoG fully
Not feasible: LoG requires >= 4 voxels/dimension; single-slice data cannot satisfy this
without 3D volumes that do not exist. **Excluded.**

## Codebase plumbing (verified via code exploration)

- **Extraction config is inline in the NB12 pair** (no params `.yaml`):
  `analysis/12_extract_radiomics_all_images_normalised.ipynb` uses
  `settings = {force2D:True, force2Ddimension:0, normalize:True, normalizeScale:100,
  removeOutliers:3}`, then `disableAllFeatures()` + six `enableFeatureClassByName(...)`
  (firstorder/glcm/glrlm/glszm/gldm/ngtdm; shape disabled). Only `Original` imageType
  today. Adding wavelet = one line: `enableImageTypeByName('Wavelet')`. PyRadiomics
  3.1.0; single 2D slices via `sitk.GetImageFromArray` (depth=1) handled by force2D.
- **Data chain:** NB12 (extract) -> NB13 (merge clinical) -> NB18 (independent 55) ->
  NB19/NB14a/NB25 (stats) + NB20 (ML). Downstream notebooks only `read_csv`.
- **The change surface is one line, repeated:** every stats/ML notebook selects features
  with `feature_cols = [c for c in df.columns if c.startswith("original_")]`. Widen to
  `startswith(("original_", "wavelet-"))` to admit new columns; everything downstream
  (Shapiro/Welch/Mann-Whitney, BH-FDR, >0.9 correlation filter, `SelectKBest`, bootstrap
  CI) is already driven off `feature_cols`. Only extra edit: NB20's `k_values` list.
- Label column everywhere is `rejection` (0/1); `patient_id` gives 55-patient
  uniqueness; `motivo` (NB14a) / `Dias pTXP` (NB25) drive early/late stratification.

## Recommendation

**Take Option A.** It answers Gemma completely, costs ~1-2 hours, adds no risk two weeks
before the defence, and is backed by the strongest evidence available (Demircioglu 2022)
plus the thesis's own Gabor/Laws null results. Option B is a valid "maximum thoroughness"
path only if there are ~1-2 spare days and the wavelet numbers are wanted in hand; its
most likely outcome is a null that restates the existing conclusion. Option C is not
possible on this data.

## Verification (whichever option is taken)
- Option A: `latexmk` exits 0; new citation resolves (no `?`); discussion reads cleanly.
- Option B: spike-test returns `wavelet-*` columns; each new notebook runs top-to-bottom
  on `thesis_env`; output CSV shapes as expected; `latexmk` clean; main body shows the
  independent-dataset wavelet result, appendix the full-dataset version.

## References found during research
- Demircioglu A. (2022) *The effect of preprocessing filters on predictive performance
  in radiomics.* Eur Radiol Exp 6:40. (Filters do not reliably improve performance.)
- Aerts HJWL et al. (2014) *Decoding tumour phenotype by noninvasive imaging...* Nat
  Commun 5:4006. (Wavelet features among the most predictive in lung/H&N CT.)
- PyRadiomics docs: LoG is 3D, needs >= 4 voxels/dimension; wavelet via PyWavelets.
