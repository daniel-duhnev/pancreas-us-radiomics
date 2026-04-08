# Supervisor Update: Notebooks 12-15

Preparation notes for supervisor meetings. Covers key concepts, methodology, implementation details, and results for each analysis notebook.

---

## Notebook 12: Radiomics Feature Extraction

### What we did

Extracted 93 numerical features from 134 pancreas transplant ultrasound images using PyRadiomics. Each image has an associated segmentation mask defining the region of interest (the pancreas).

### How PyRadiomics works

It is **not** an iterative process. The core pattern is:

```python
from radiomics import featureextractor

extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
extractor.disableAllFeatures()
extractor.enableFeatureClassByName("firstorder")  # repeat for each class
# ...
features = extractor.execute(sitk_image, sitk_mask)  # single call, returns all features
```

- `RadiomicsFeatureExtractor` is the main class
- `.execute(image, mask)` is a **single function call** that takes one image + one mask and returns a dictionary of all enabled features
- We loop over our 134 studies externally, calling `.execute()` once per image
- Output dictionary keys look like `original_firstorder_Mean`, `original_glcm_Contrast`, etc.
- Keys starting with `diagnostics_` are metadata and are filtered out

### Why 93 features

We explicitly enabled 6 feature classes and disabled shape features (per supervisor guidance — shape describes the mask geometry, not image content):

| Feature class | Count | What it captures |
|---------------|-------|------------------|
| **First-order** | 18 | Pixel intensity statistics (mean, variance, skewness, entropy, percentiles). No spatial info. |
| **GLCM** | 24 | How often pairs of pixel values appear next to each other (co-occurrence). Core texture descriptor. |
| **GLRLM** | 16 | Length of consecutive runs of the same intensity. Long runs = smooth, short runs = heterogeneous. |
| **GLSZM** | 16 | Size of connected zones of the same intensity. Similar to GLRLM but in 2D, not just one direction. |
| **GLDM** | 14 | How much each pixel differs from its neighbours. |
| **NGTDM** | 5 | How different a pixel's neighbourhood average is from the overall image average. |

**Important distinction:** GLCM, GLRLM, etc. are intermediate *matrices*, not features. The features are statistics computed *from* those matrices (e.g. "GLCM Correlation" summarises the entire co-occurrence matrix into one number).

### Critical settings

- **`force2D=True`**: Our images are 2D ultrasound slices. Without this, texture matrices (GLCM, GLRLM) fail because they expect a 3D volume.
- **`binWidth=25`** (PyRadiomics default): Pixel intensities are discretised into bins before computing texture matrices. Reduces noise sensitivity but trades off some detail.
- **`int16` cast**: PyRadiomics requires integer pixel values. We cast from the original format to int16 before extraction.

### Preprocessing per image

1. Load DICOM with `pydicom`
2. Convert RGB to grayscale if needed (`cv2.cvtColor`)
3. Load mask PNG, binarise (255 -> 1)
4. Resize mask if dimensions mismatch with image
5. Cast image to `int16`
6. Convert both to SimpleITK objects (`sitk.GetImageFromArray`)

### Results

- **Input**: 134 studies from the manifest (all had valid non-zero masks)
- **Output**: CSV with shape (134, 94) — 134 rows x 93 features + 1 study_id column
- **No failures**: All 134 extractions succeeded, no NaN values
- **Output file**: `reports/12_radiomics_features_k3_i1.csv`

### Key points for discussion

- The `k3_i1` in the filename refers to kernel size 3 and iteration 1 from the mask erosion step (notebook 09)
- All features are computed within the masked region only — pixels outside the mask are ignored
- Feature values are not normalised at this stage; normalisation happens later in the ML pipeline (notebook 15)

---

## Notebook 13: Merge Clinical and Radiomics Data

### What it does

A data preparation step — no analysis. Joins the radiomics features (from NB 12) with clinical metadata into a single CSV so downstream notebooks can load one file.

- **Input 1**: `reports/12_radiomics_features_k3_i1.csv` (134 studies, 93 features)
- **Input 2**: `../data/bd_estudiUPF.csv` (138 clinical records)
- **Operation**: Inner join on `study_id`
- **Output**: `reports/13_merged_radiomics_clinical.csv` (134 rows x 100 columns)

The 100 columns are: study_id, patient_id, 93 radiomics features, motivo, rejection, biopsy_confirmed_rejection, biopsy_performed, biopsy_rejection_type.

### Who uses it

Only **notebook 15** (ML classification) loads the merged file. Notebooks 14a and 14b do their own data loading independently — 14a loads radiomics + clinical separately and joins them itself, 14b loads only the clinical CSV since it doesn't need radiomics features.

### Why a separate notebook

Keeps the pipeline modular: extraction (12) -> preparation (13) -> analysis (14-15). NB 15 doesn't have to worry about how the join works, it just loads the ready-made file. The merge itself is trivial (one inner join), but separating it avoids mixing data wrangling with modelling logic.

---

## Notebook 14a: Statistical Analysis of Radiomics Features

This is the core analysis for the radiomics side. Tests whether any of the 93 extracted features differ between rejection and no-rejection groups.

### Strategy

1. Check normality (Shapiro-Wilk) on both groups for each feature
2. If both groups are normal: Welch's t-test (`equal_var=False`). If not: Mann-Whitney U
3. Compute effect size (Cohen's d for t-test, rank-biserial correlation for Mann-Whitney)
4. Apply Benjamini-Hochberg FDR correction across all 93 tests
5. Repeat analysis on early (motivo 1-2) and late (motivo 3-5) subsets
6. Compute feature correlation matrix for use in notebook 15

### Key decisions

- **Welch's t-test over standard t-test**: our groups are unbalanced (95 vs 39). Welch's doesn't assume equal variance, making it safer. We verified this change has negligible impact on results (p-values shift by ~0.01, no conclusions change).
- **Two-sided tests throughout**: we don't assume direction of difference (rejection could increase or decrease a feature).
- **Mann-Whitney for 78/93 features**: only 15 pass normality in both groups. Most radiomics features have skewed distributions.
- **FDR over Bonferroni**: Benjamini-Hochberg controls the false discovery rate (proportion of false positives among significant results) rather than the family-wise error rate. Less conservative, more appropriate for exploratory analysis with 93 tests.

### Results

**Full dataset (134 studies: 95 no-rejection, 39 rejection):**
- Features with uncorrected p < 0.05: **0 out of 93**
- Features surviving FDR correction: **0**
- Closest: `firstorder_Minimum` at p = 0.055 (rank-biserial r = -0.21, small effect)

**Early subset (motivo 1-2, 66 studies: 56 vs 10):**
- 0 features significant. Closest: `glcm_ClusterProminence` at p = 0.126

**Late subset (motivo 3-5, 68 studies: 39 vs 29):**
- 0 features significant. Closest: `firstorder_Minimum` at p = 0.052

**Correlation analysis:**
- 305 feature pairs have |r| > 0.9 (high redundancy among the 93 features)
- This motivates the correlation-based feature reduction in notebook 15

### Interpretation

No radiomics feature distinguishes rejection from no-rejection at conventional significance thresholds. This is a **negative result** but not necessarily a failure — it means ultrasound texture features as extracted by PyRadiomics do not carry detectable signal for rejection in our dataset. Possible explanations:
- Sample size too small (134 studies, only 39 rejection) for subtle effects
- Ultrasound image quality/variability masks the signal
- Rejection may not manifest in texture patterns detectable at this resolution
- Repeated measures inflate apparent sample size (55 patients, not 134 independent observations)

### Known limitations

- **Repeated measures**: 55 patients contribute 134 studies. Independence assumption is violated. Documented in the notebook with a pointer to `docs/PLAN_REPEATED_MEASURES.md`.
- **No stratified FDR**: FDR is applied to the full dataset analysis but not to the stratified subsets (early/late are exploratory).

---

## Notebook 14b: Statistical Analysis of Clinical Features

Tests 17 clinical/imaging features (ARFI elastography, DCE-US perfusion parameters, QOF, Area) against rejection. This is where we replicate Clara's paper (Bassaganyas et al. 2025).

### Features tested (17 total)

| Category | Features |
|----------|----------|
| **ARFI elastography (4)** | ARFI mediana, ARFI media, ARFI DE, ARFI RIQ |
| **DCE-US perfusion (11)** | PE, WiAUC, RT, mTTI, TTP, WiR, WiPi, WoAUC, WiWoAUC, FT, WoR |
| **Other (2)** | QOF, Area |

### Strategy

Same as 14a but simpler:
1. Mann-Whitney U for all features (matching Clara's methodology, no normality check needed)
2. Rank-biserial correlation as effect size
3. Stratified by motivo (early 1-2, late 3-5) AND by actual days post-transplant (>90 days)
4. **Note**: no FDR correction is applied (matches Clara's paper, but worth acknowledging)

### Key decision: motivo vs actual days

The motivo column (1-5) is a category label, not actual time. We discovered that **13 studies are misclassified** when using motivo as a proxy for time:
- Motivo 4 (suspected rejection) ranges from 11 to 8,429 days (23 years!)
- Motivo 5 (follow-up) ranges from 36 to 3,535 days
- Some motivo 4/5 studies happened within 90 days, some motivo 1/2 happened later

Using the `Dias pTXP` column (actual days post-transplant, pre-computed in the source spreadsheet) with a >90 day cutoff gives a different late subset (58 vs 71 studies) and **matches Clara's published results exactly**.

We keep both analyses: motivo-based (our own) and days-based (Clara's replication).

### Results

**Full dataset (138 studies: 98 no-rejection, 40 rejection):**
- 2 features significant: ARFI mediana (p=0.028), ARFI media (p=0.030)

**Early motivo 1-2 (67 studies: 57 vs 10):**
- 0 features significant

**Late motivo 3-5 (71 studies: 41 vs 30):**
- 7 significant: all 4 ARFI + WiAUC, WoAUC, WiWoAUC

**Late >90 days / Clara's split (58 studies: 36 vs 22):**
- 8 significant: all 4 ARFI + WiAUC, WoAUC, WiWoAUC, WiPi
- P-values match Clara's paper to 3 decimal places (14 of 15 features match; only RT diverges slightly: 0.142 vs 0.276)

### Key observations

- **ARFI features are the strongest signal**: ARFI mediana and ARFI media reach p < 0.0001 in the late group with large effect sizes (r > 0.7). These are elastography measurements of tissue stiffness — rejection makes the pancreas stiffer.
- **Perfusion features are weaker but present**: WiAUC, WoAUC (blood flow patterns) are significant in the late group. Rejection disrupts blood supply.
- **Time matters**: no signal in the early period. Rejection effects on tissue properties take time to manifest, or early studies are dominated by post-surgical changes.
- **Our replication of Clara's paper is successful**: nearly identical p-values confirm our data handling and statistical implementation are correct.

### Known limitations

- **No FDR correction applied**: with 17 features tested across 4+ subsets, some borderline results (e.g. WiPi at p=0.044) might not survive correction. The strong ARFI results (p < 0.0001) would survive any correction.
- **Repeated measures**: same issue as 14a. 56 patients contribute 138 studies.
- **Missing data**: ARFI features have 17 missing studies (121/138 available), DCE-US has 11 missing (127/138). Handled via `dropna()`.

---

## Notebook 15: Feature Selection and ML Classification

Attempts to classify rejection vs no-rejection using radiomics features. Given that notebook 14a found zero significant features, this is an important but expected-to-fail experiment.

### Important: what features are used (and not used)

The ML classifier uses **only radiomics features** (texture and intensity features extracted by PyRadiomics in NB 12). It does **not** include any of the clinical features from 14b — no ARFI, no perfusion parameters, no QOF, no Area. The merged CSV that NB 15 loads (`13_merged_radiomics_clinical.csv`) contains 93 radiomics feature columns plus metadata (study_id, patient_id, motivo, rejection label), but none of the clinical imaging measurements.

This means the ML has never seen the features that actually show statistical signal (ARFI, DCE-US). A combined model using both radiomics + clinical features would be a separate experiment we haven't done yet (see Proposed Next Steps).

### Strategy

1. Remove highly correlated features (|r| > 0.9) to reduce redundancy
2. Train two classifiers with stratified 5-fold cross-validation
3. Report AUC, sensitivity, specificity
4. Try both full dataset and late-only subset
5. Extract Random Forest feature importances

### Step 1: Correlation-based feature reduction

93 features for 134 samples is a recipe for overfitting. Plus, 305 feature pairs have |r| > 0.9 (massive redundancy).

**Key decision — p-value-guided removal:** when two features correlate above the threshold, we keep the one with the lower p-value from notebook 14a's statistical analysis. This ensures features with the most signal (even marginal) survive. The original version dropped by column order, which accidentally removed `firstorder_Minimum` (our best feature, p=0.055) in favour of `10Percentile` (p=0.128).

**Result:** 93 -> 31 radiomics features retained. All 31 are texture/intensity features (e.g. `firstorder_Minimum`, `glcm_Correlation`, `ngtdm_Coarseness`). No clinical features.

### Step 2: Classifiers

Two models, both inside a `sklearn.Pipeline` with `StandardScaler`:

- **Logistic Regression** (L2 penalty, C=1.0): linear baseline, interpretable
- **Random Forest** (100 trees): non-linear, captures feature interactions

Both use `class_weight="balanced"` to handle class imbalance (95 vs 39). Without this, models tend to predict the majority class ("no rejection") for everything.

**Why only two algorithms?** They cover both linear (LogReg) and non-linear (RF) approaches. When both produce AUC ~0.5, the problem is the features (no signal), not the model choice. Adding more algorithms (SVM, XGBoost, etc.) would confirm the same null result — you can't build a good classifier from features that don't discriminate. If we had found AUC = 0.7+, we would try more algorithms to optimise. For a negative result, two is sufficient to demonstrate the case.

### Step 3: Evaluation — no data leakage

**Stratified 5-fold CV**: splits data into 5 folds preserving the class ratio, trains on 4 folds, tests on 1, rotates 5 times.

The `StandardScaler` is **inside** the Pipeline, meaning it is fitted only on each training fold, never on the test fold. This prevents data leakage — if scaling were applied to the whole dataset before CV, the test fold would be contaminated by training data statistics. Verified correct.

### Results

| Dataset | Model | AUC | Sensitivity | Specificity |
|---------|-------|-----|-------------|-------------|
| Full (n=134) | Logistic Regression | 0.429 | 0.407 | 0.442 |
| Full (n=134) | Random Forest | 0.515 | 0.100 | 0.958 |
| Late motivo 3-5 (n=68) | Logistic Regression | 0.515 | 0.580 | 0.543 |
| Late motivo 3-5 (n=68) | Random Forest | 0.497 | 0.373 | 0.775 |

**All AUCs are around 0.5 — the models are guessing.** Logistic Regression on the full dataset scores 0.429, which is *below* chance. Random Forest's 95.8% specificity is misleading — it learned to say "no rejection" almost always, catching only 1 in 10 rejection cases.

### Step 4: Feature importances

Random Forest ranks `RunLengthNonUniformity`, `ngtdm_Contrast`, `ngtdm_Coarseness` as most important. But with AUC at 0.5, these importances are noise — the model isn't learning anything real.

### Why ML fails here

1. **No univariate signal**: 14a found 0 significant features. ML can sometimes find multivariate patterns that univariate tests miss, but not here.
2. **Small effective sample size**: 134 studies from 55 patients with 31 features after reduction. Still a difficult ratio for learning.
3. **Class imbalance**: 95 vs 39 limits what models can learn about the minority class, even with balanced weighting.
4. **Repeated measures**: studies from the same patient are correlated, further reducing effective sample size below the nominal 134.

### Key takeaway for the thesis

**This is a valid negative result.** Radiomics features from grayscale ultrasound, as extracted with PyRadiomics, do not predict pancreas transplant rejection in our cohort. This contrasts with the clinical features in 14b (ARFI elastography, DCE-US perfusion) which do show strong signal — suggesting that targeted clinical imaging biomarkers outperform automated texture analysis for this task.

The negative result is still publishable and informative: it sets a baseline and narrows the search space for future work (e.g. different imaging modalities, larger cohorts, deep learning on raw images instead of handcrafted features).

---
---

## Overall Summary

We built a complete pipeline from raw ultrasound images to ML classification:

**NB 12** extracted 93 radiomics features from 134 studies using PyRadiomics. **NB 13** merged these with clinical metadata. **NB 14a** tested all 93 radiomics features for association with rejection — none reached significance (closest: `firstorder_Minimum` at p=0.055). **NB 14b** tested 17 clinical features — ARFI elastography strongly distinguishes rejection in the late post-transplant period (p < 0.0001), and we replicated Clara's published results to 3 decimal places. **NB 15** attempted ML classification with radiomics features — AUC ~0.5 across all models, confirming the lack of signal.

**Bottom line:** Radiomics texture features from grayscale ultrasound do not predict rejection. Clinical imaging biomarkers (ARFI, DCE-US perfusion) do, particularly beyond 90 days post-transplant.

---

## Limitations

1. **Repeated measures / non-independence**: 55 patients contribute 134 studies (mean 2.4 per patient). All tests assume independence between studies, which is violated. 14 patients have both rejection and no-rejection studies. This matches Clara's approach but should be acknowledged and investigated further.

2. **Small sample size**: 134 studies (39 rejection) limits statistical power for subtle effects and makes ML prone to overfitting. The effective sample size is even smaller when accounting for repeated measures.

3. **No FDR correction in 14b**: the clinical feature analysis tests 17 features across multiple subsets without multiple comparison correction. Strong results (ARFI) survive any correction, but borderline ones (WiPi, WiWoAUC) may not.

4. **Single extraction configuration**: PyRadiomics was run with one set of parameters (binWidth=25, force2D, int16). Different bin widths or preprocessing could yield different features.

5. **Motivo as time proxy**: unreliable — 13 studies are misclassified. We addressed this by adding actual days-based stratification, but the motivo-based analysis should be interpreted cautiously.

---

## Proposed Next Steps

1. **Repeated measures sensitivity analysis**: implement the approaches in `docs/PLAN_REPEATED_MEASURES.md` — particularly one-study-per-patient (first/last/random) and mixed-effects models. This would either confirm or weaken the current findings. High priority as it affects all conclusions.

2. **Apply FDR correction to 14b**: straightforward addition. Would clarify which clinical features are robust to multiple testing.

3. **Combine radiomics + clinical features in ML**: NB 15 currently uses only radiomics. Since clinical features (ARFI) show signal, a combined model might perform better. Worth testing whether radiomics adds anything on top of clinical features.

4. **Explore alternative PyRadiomics settings**: different bin widths (e.g. 10, 50), wavelet/LoG filtered features, or different image preprocessing. The current null result is specific to one configuration.

5. **Deep learning on raw images**: instead of handcrafted radiomics features, train a CNN directly on the ultrasound images. Requires more data or transfer learning, but avoids the feature engineering bottleneck.

---

## Discussion Points for Supervisor

- **Is the negative radiomics result sufficient for the thesis, or do we need to try more configurations?** We could vary binWidth, add wavelet filters, or try different feature subsets. But this risks p-hacking if not pre-registered.

- **How to handle the repeated measures limitation?** Our tests assume each study is independent, but 55 patients contribute 134 studies — so they aren't. We've documented 7 possible approaches (e.g. pick one study per patient, use mixed-effects models). Which are essential vs nice-to-have for the thesis?

- **Should we try a combined radiomics + clinical ML model?** NB 15 currently uses only radiomics features (no ARFI, no perfusion). Since clinical features show strong signal in 14b, feeding both feature sets into a classifier would test whether radiomics adds anything on top of clinical biomarkers. If it doesn't, that's an additional finding. If it does, it changes the narrative.

- **Scope of the thesis going forward**: is the current pipeline (extraction -> stats -> ML) the final scope, or are there additional analyses expected (e.g. survival analysis, longitudinal modelling, deep learning)?

- **Publication angle**: the replication of Clara's results plus the negative radiomics finding could frame a paper around "clinical biomarkers outperform automated texture analysis for pancreas transplant rejection detection." Is this the direction we want?
