# Plan: Radiomics Feature Extraction, Clinical Merge, and Statistical Analysis

## Context

The preprocessing phase is complete: 134 ultrasound images have clean grayscale versions and eroded binary masks. A single-image radiomics test (notebook 11) works. The next phase is to extract features for all images, merge with clinical data, and run statistical tests to answer the thesis hypothesis: *does pancreas texture on ultrasound correlate with transplant rejection?*

The supervisor's guidance is clear: start with statistical tests (t-test / Mann-Whitney per feature), see if anything is significant before worrying about alpha correction, then move to feature selection and ML.

### Relationship to Clara's paper (Bassaganyas et al. 2025, European Radiology)

Clara's paper uses **the same dataset** (138 studies, 56 patients, 98 normal / 40 rejection). She analyzed ARFI elastography and DCE-US perfusion parameters -- these are **manual measurements already in the clinical spreadsheet** (`bd_estudiUPF.csv` columns: ARFI_mediana, PE, WiAUC, RT, etc.).

Our thesis extends this by asking: can **automated texture analysis from the images themselves** (radiomics) add diagnostic value? This is complementary, not a replication.

Key methodological takeaways from Clara's paper:
- **Statistical test**: Mann-Whitney U (they did not use t-tests -- continuous data, small groups)
- **Significance level**: alpha = 0.05, two-sided
- **No alpha correction applied** (but they only tested ~12 parameters; we will have ~100, so correction matters more for us)
- **Logistic regression** for odds ratios and AUC, with cut-offs via Youden's criterion
- **Time stratification matters**: parameters behaved very differently in first 90 days vs after 90 days post-transplant. The `motivo` column encodes this (1=1 week, 2=1 month, 3=1 year, 4=suspicion, 5=follow-up). Motivo 1 and 2 are within 90 days; motivo 3+ is beyond.
- **Clara's key result**: ARFI cut-off 1.27 m/s achieved AUC 0.80 for rejection prediction (after 90 days). Combined elastography + DCE-US gave 23.2x odds of rejection.

**Implication for our plan**: we should run statistical tests both on the full dataset AND stratified by time period (<=90 days vs >90 days), since texture features may also behave differently across timepoints.

---

## Pre-flight: Machine Migration Sanity (~30 min)

Before doing new work, verify the existing pipeline still runs on this Mac.

### Step 0a: Clean up Windows WSL artifacts
- Delete 2 `Zone.Identifier` junk files in `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/masks/`

### Step 0b: Fix manifest for edge cases
- The manifest shows `orig_pixels=0, eroded_pixels=0` for studies `03_01` and `43_01`, but the actual mask files have real pixels (34,018 and 20,911 respectively). The masks were fixed by notebook 10 and copied back, but the manifest was never updated.
- Update the manifest CSV to reflect the actual pixel counts for these two studies.

### Step 0c: Run notebook 01 (setup test)
- Open `analysis/01_setup_test.ipynb`, select kernel `thesis_env (Python 3.9)`, run all cells.
- Confirms environment works on this Mac.

### Step 0d: Run notebook 11 (single-image radiomics test)
- Open `analysis/11_extract_radiomics_for_one_test_image.ipynb`, run all cells.
- Confirms the full radiomics pipeline (DICOM load, mask load, SimpleITK conversion, PyRadiomics extraction) works on Apple Silicon.

**No need to rerun preprocessing notebooks (06b, 09, 10)** -- the data outputs are already transferred and verified (134 masks, 134 study folders, 1:1 match).

---

## Phase 1: Batch Radiomics Extraction -- Notebook 12 (new)

**File:** `analysis/12_extract_radiomics_all_images.ipynb`

### What it does
Loop over all 134 studies, extract radiomics features, output a single CSV.

### Cells (step by step)

1. **Imports** -- same as notebook 11: `os, cv2, pydicom, numpy, pandas, SimpleITK, radiomics.featureextractor`

2. **Load manifest** -- read `manifest_eroded_CONTOUR_SUBTRACTED_k3_i1.csv`, print row count and verify no zero-pixel masks remain.

3. **Helper: locate DICOM for a study ID** -- given a study_id, walk `data/PANCREAS_2/PANCREAS_2/{study_id}/{date_folder}/` and return the first `.dcm` file path. Print warning if not found.

4. **Helper: load and prepare image+mask pair** -- for a study_id: load DICOM -> grayscale, load mask PNG -> binary (0/1), check shape alignment, convert both to SimpleITK. Return the pair.

5. **Configure PyRadiomics extractor** -- enable feature classes: `firstorder`, `glcm`, `glrlm`, `glszm`, `gldm`, `ngtdm`. This gives a comprehensive feature set (~100 features). Disable shape features (per supervisor guidance: texture and intensity only, not shape).

6. **Extraction loop** -- iterate over manifest rows. For each study: load pair, run extractor, collect features into a list of dicts. Print progress every 10 studies. Catch and log errors per study without stopping the loop.

7. **Build DataFrame and save** -- convert list of dicts to DataFrame. Save to `analysis/reports/radiomics_features_k3_i1.csv`. Print shape and first 5 rows.

### Output
- `analysis/reports/radiomics_features_k3_i1.csv`: 134 rows x ~100+ feature columns + study_id

---

## Phase 2: Merge with Clinical Data -- Notebook 13 (new)

**File:** `analysis/13_merge_clinical_and_radiomics.ipynb`

### What it does
Merge radiomics features with clinical labels from `bd_estudiUPF.csv`.

### Cells

1. **Load radiomics CSV** from `analysis/reports/radiomics_features_k3_i1.csv`

2. **Load clinical CSV** from `data/bd_estudiUPF.csv`. Clean the `id estudio` column (strip whitespace). Key columns:
   - `id estudio` (join key)
   - `RECHAZO CLINICO` (primary binary label: 0/1)
   - `motivo` (timepoint: 1=1wk, 2=1mo, 3=1yr, 4=suspicion, 5=follow-up)
   - `id paciente` (patient ID, for repeated measures awareness)
   - `Rechazo confirmado por biopsia` and `RECHAZO biopsia` (severity, for secondary analysis)

3. **Inner join** on study_id. Expect ~134 matched rows (4 clinical-only orphans dropped: 34_02, 40_02, 41_03, 47_01).

4. **Print class distribution** by RECHAZO CLINICO and by motivo. Also print cross-tab of rejection by motivo.

5. **Save merged table** to `analysis/reports/merged_radiomics_clinical.csv`.

---

## Phase 3: Statistical Analysis -- Notebook 14 (new)

**File:** `analysis/14_statistical_analysis.ipynb`

Following supervisor guidance: *"start with statistical tests, see if anything is significant before worrying about alpha correction"*

### Cells

1. **Load merged CSV**

2. **Split into groups**: rejection (RECHAZO CLINICO=1) vs no rejection (=0). Print group sizes.

3. **Normality check per feature**: for each radiomics feature, run Shapiro-Wilk test on each group. Record which features pass normality assumption (p > 0.05 in both groups). Note: Clara's paper used Mann-Whitney throughout -- radiomics features are often non-normal, so expect most to fail normality.

4. **Univariate testing -- full dataset (uncorrected)**:
   - If both groups pass normality: independent t-test
   - Otherwise: Mann-Whitney U test (consistent with Clara's approach)
   - For each feature: compute test statistic, p-value, effect size (rank-biserial correlation for Mann-Whitney, Cohen's d for t-test)
   - Sort by p-value ascending
   - Print table of all features with p < 0.05 (if any)

5. **Univariate testing -- stratified by time period**:
   - Subset 1: motivo <= 2 (within 90 days: 1 week + 1 month)
   - Subset 2: motivo >= 3 (beyond 90 days: 1 year, suspicion, follow-up)
   - Repeat Mann-Whitney for each subset
   - Compare: are different features significant in early vs late timepoints?
   - This mirrors Clara's finding that parameters behave differently before/after 90 days.

6. **Interpret uncorrected results**:
   - If zero significant features: report this finding. No need for alpha correction. This is a valid thesis result ("texture radiomics do not discriminate rejection in this cohort").
   - If significant features exist: proceed to step 7.

7. **Alpha correction (if needed)**:
   - Apply Benjamini-Hochberg FDR correction (standard for radiomics studies)
   - Report which features survive correction
   - Context: running ~100 tests at alpha=0.05 expects ~5 false positives by chance

8. **Correlation heatmap**: compute pairwise Pearson correlation between all radiomics features. Identify clusters of highly correlated features (r > 0.9). This informs feature selection for ML.

9. **Summary table**: save results to `analysis/reports/univariate_stats_results.csv`

### Additional packages needed
- `scipy.stats` (already available via pyradiomics dependencies)
- `statsmodels` for FDR correction -- need to `pip install statsmodels`

---

## Phase 4: Feature Selection and ML -- Notebook 15 (new)

**File:** `analysis/15_feature_selection_and_ml.ipynb`

This is the ML phase. Only proceed here after Phase 3 results are reviewed with supervisor.

### Cells

1. **Load merged data**

2. **Feature selection** (two approaches, as supervisor suggested):
   - **Correlation filter**: drop one feature from each pair with r > 0.9 (keep the one with lower p-value from Phase 3)
   - **Univariate filter**: keep only features with uncorrected p < some threshold (based on Phase 3 results)

3. **Train classifiers** with stratified k-fold cross-validation (k=5 or leave-one-out given small N=134):
   - Logistic Regression (with L1/L2 regularization) -- consistent with Clara's use of logistic regression
   - Random Forest
   - SVM (if time permits)
   - Report per-fold: AUC, sensitivity, specificity
   - Use class weighting to handle imbalance (29% rejection vs 71% normal)

4. **Feature importance**: from Random Forest, extract feature importances. From Logistic Regression, extract coefficients. Compare with univariate results.

5. **Optional: combined model**: if texture features show promise, consider a model that combines radiomics features with Clara's ARFI/DCE-US parameters (columns already in spreadsheet). This could show whether texture adds value on top of elastography/perfusion.

6. **Results summary**: save model performance and feature importance to `analysis/reports/ml_results.csv`

### Additional packages needed
- `scikit-learn` -- need to `pip install scikit-learn`

---

## Data Integrity Notes

- **134 images, 134 masks**: perfect 1:1 match, verified
- **138 clinical records**: 4 orphans without images (34_02, 40_02, 41_03, 47_01) -- dropped on merge
- **Edge cases 03_01, 43_01**: masks are valid (34,018 and 20,911 nonzero pixels), manifest needs updating
- **Class balance**: ~40 rejection (29%) vs ~98 no rejection (71%) -- imbalanced. ML models should use stratified splits and consider class weighting.
- **Same dataset as Clara's paper**: this is by design -- our work extends her manual-measurement approach with automated image analysis.

---

## Files to create/modify

| Action | File | Purpose |
|--------|------|---------|
| Clean | `data/.../masks/*Zone.Identifier` (2 files) | Remove WSL junk |
| Update | `data/.../manifest_...csv` (2 rows) | Fix 03_01, 43_01 pixel counts |
| Create | `analysis/12_extract_radiomics_all_images.ipynb` | Batch feature extraction |
| Create | `analysis/13_merge_clinical_and_radiomics.ipynb` | Merge features + labels |
| Create | `analysis/14_statistical_analysis.ipynb` | Univariate stats + alpha correction |
| Create | `analysis/15_feature_selection_and_ml.ipynb` | Feature selection + classifiers |
| Install | `statsmodels`, `scikit-learn` via pip | Additional dependencies |

---

## Verification

After each notebook:
- Notebook 12: check CSV has 134 rows and ~100 feature columns, no NaN study IDs
- Notebook 13: check merged table has ~134 rows, rejection column is 0/1 with no NaNs
- Notebook 14: check statistical results table is populated, p-values are between 0 and 1
- Notebook 15: check cross-validation AUC values are reasonable (0.5 = random, >0.7 = promising)

---

## Execution order

1. **Pre-flight (0a-0d)** -- do first, quick sanity checks on new machine
2. **Notebook 12** -- batch extraction (main new work)
3. **Notebook 13** -- merge with clinical data (quick, depends on 12)
4. **Notebook 14** -- statistical analysis (core thesis results, discuss with supervisor)
5. **Notebook 15** -- ML (depends on 14 results to guide feature selection)
