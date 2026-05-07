# Plan: Implementing Supervisor's Recommended Experiments

## Context

After the meeting with supervisor Gemma Piella (2026-04-08), she recommended 4 categories of additional experiments to strengthen the thesis before writing. The current analysis (notebooks 12-15) showed that radiomics features from grayscale ultrasound do NOT predict pancreas transplant rejection (0/93 significant, ML AUC ~0.5), while clinical biomarkers (ARFI) DO predict it. Gemma's recommendations aim to (1) ensure the ML pipeline is rigorous, (2) add a proper paired analysis exploiting the repeated-measures structure, (3) use surrounding tissue for normalization and contrast analysis, and (4) try alternative texture features beyond standard PyRadiomics.

All 4 categories are planned in detail below so Daniel can decide which to prioritize.

---

## Category 1: ML Pipeline Improvements

**Goal:** Make the existing ML analysis (notebook 15) more rigorous by adding training metrics and proper feature selection via RFE.

**Why it matters:** Currently we only report test metrics. Without training metrics, we can't distinguish "the model learned nothing" from "the model overfit." RFE may find a smaller, more predictive feature subset than simple correlation removal.

### Notebook: `16_ml_improvements.ipynb` (new)

#### Step 1.1: Add Training Metrics

**What:** Re-run the existing `cross_validate` calls with `return_train_score=True` to report both train and test AUC/sensitivity/specificity side-by-side.

**Implementation:**
- Copy the `evaluate_classifiers` function from NB 15
- Add `return_train_score=True` to `cross_validate()` call
- Extract `cv_results["train_auc"]`, `cv_results["train_sensitivity"]`, `cv_results["train_specificity"]`
- Report both train and test metrics in the results table
- **Interpretation guide:**
  - Train AUC high + Test AUC low = overfitting
  - Train AUC low + Test AUC low = no signal (expected for our data)
  - Train AUC high + Test AUC high = genuine signal

**Key code change in `evaluate_classifiers`:**
```python
cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring,
                            return_train_score=True)

# existing test metrics
auc_test = cv_results["test_auc"].mean()
# NEW training metrics
auc_train = cv_results["train_auc"].mean()
```

**Files:**
- Reads: `reports/13_merged_radiomics_clinical.csv`, `reports/14a_stats_radiomics_features.csv`
- Writes: `reports/16_ml_improved_results.csv`

**Effort:** Small (~1 hour). Straightforward extension of existing code.

#### Step 1.2: Recursive Feature Elimination (RFE)

**What:** After correlation removal (93 -> 31 features), apply RFE to find the optimal subset. Use `RFECV` (RFE with cross-validation) to automatically select the best number of features.

**Implementation:**
```python
from sklearn.feature_selection import RFECV

# Use LogReg as the estimator for RFE (coefficients drive elimination)
estimator = LogisticRegression(C=1.0, penalty="l2", class_weight="balanced",
                                max_iter=1000, random_state=42)

# RFE with 5-fold stratified CV
rfecv = RFECV(
    estimator=estimator,
    step=1,              # remove 1 feature per iteration
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring="roc_auc",
    min_features_to_select=1,
)

# Fit on scaled data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
rfecv.fit(X_scaled, y)

print(f"Optimal number of features: {rfecv.n_features_}")
print(f"Selected features: {[f for f, s in zip(feature_names, rfecv.support_) if s]}")
```

- Run RFE on both full dataset and late subset
- After RFE selects features, re-run LogReg + RF with train+test metrics
- Report: feature ranking, optimal N, AUC before/after RFE
- **Important:** RFE must happen INSIDE the CV loop to avoid data leakage. Use a nested CV approach or document the limitation if using the simpler approach.

**Nested CV (proper, no leakage):**
```python
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for train_idx, test_idx in outer_cv.split(X, y):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # RFE on training fold only
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    rfecv = RFECV(estimator=estimator, cv=inner_cv, scoring="roc_auc")
    rfecv.fit(X_train_scaled, y_train)
    
    # Evaluate on test fold using selected features
    X_train_sel = rfecv.transform(X_train_scaled)
    X_test_sel = rfecv.transform(X_test_scaled)
    # ... train and evaluate
```

**Files:**
- Reads: same as Step 1.1
- Writes: `reports/16_rfe_results.csv`, `reports/16_rfe_feature_ranking.csv`

**Effort:** Medium (~2-3 hours). Nested CV adds complexity.

**Expected outcome:** RFE will likely confirm that no subset of radiomics features achieves meaningful AUC. This strengthens the negative result by showing it's not just a feature selection problem.

---

## Category 2: Paired Analysis (Wilcoxon Signed-Rank Test)

**Goal:** Exploit the 14 patients who have both rejection and non-rejection studies to run a paired statistical test. Each patient is their own control, eliminating between-patient variability.

**Why it matters:** The current Mann-Whitney analysis treats all studies as independent, which inflates effective sample size. A paired analysis on 14 patients with both outcomes is the most internally valid test possible with this data. Gemma specifically wants the "max time difference" variant.

### Notebook: `17_paired_analysis.ipynb` (new)

#### Step 2.1: Identify and Select Paired Studies

**What:** For each of the 14 patients with both outcomes, select 1 rejection study and 1 non-rejection study with the maximum time difference (days post-transplant). This maximizes the chance of detecting a difference because the organ states are most distinct.

**Implementation:**
```python
# Load data
df = pd.read_csv("reports/13_merged_radiomics_clinical.csv")

# Column 'Dias pTXP' has days post-transplant (pre-computed in source spreadsheet)
# Find patients with both outcomes
both_outcomes = df.groupby("patient_id")["rejection"].nunique()
patients_both = both_outcomes[both_outcomes == 2].index.tolist()
print(f"Patients with both outcomes: {len(patients_both)}")  # expect 14

# For each patient: pick the rejection + non-rejection study pair
# with maximum |days_rej - days_no_rej|
pairs = []
for pid in patients_both:
    patient_data = df[df["patient_id"] == pid]
    rej_studies = patient_data[patient_data["rejection"] == 1]
    no_rej_studies = patient_data[patient_data["rejection"] == 0]
    
    best_diff = -1
    best_pair = None
    for _, r in rej_studies.iterrows():
        for _, nr in no_rej_studies.iterrows():
            diff = abs(r["Dias pTXP"] - nr["Dias pTXP"])
            if diff > best_diff:
                best_diff = diff
                best_pair = (r["study_id"], nr["study_id"], diff)
    
    pairs.append({
        "patient_id": pid,
        "rej_study": best_pair[0],
        "no_rej_study": best_pair[1],
        "days_difference": best_pair[2],
    })

pairs_df = pd.DataFrame(pairs)
print(pairs_df)
```

**Data check needed:** Verify that `Dias pTXP` column is present in merged CSV. If not, it needs to be brought in from `bd_estudiUPF.csv` via the merge step. The column exists in the source spreadsheet.

#### Step 2.2: Compute Within-Patient Differences

**What:** For each radiomics feature, compute (rejection value - non-rejection value) for each of the 14 pairs.

```python
# Build paired difference dataframe
diffs = {}
for _, pair in pairs_df.iterrows():
    rej_row = df[df["study_id"] == pair["rej_study"]]
    no_rej_row = df[df["study_id"] == pair["no_rej_study"]]
    
    for feat in feature_cols:
        if feat not in diffs:
            diffs[feat] = []
        diff_val = rej_row[feat].values[0] - no_rej_row[feat].values[0]
        diffs[feat].append(diff_val)

diff_df = pd.DataFrame(diffs, index=pairs_df["patient_id"])
```

#### Step 2.3: Wilcoxon Signed-Rank Test

**What:** For each feature, test whether the median within-patient difference is significantly different from zero.

```python
from scipy.stats import wilcoxon

results = []
for feat in feature_cols:
    d = diff_df[feat].dropna().values
    
    # Wilcoxon requires at least 10 observations and non-zero differences
    non_zero = d[d != 0]
    if len(non_zero) >= 6:  # minimum practical for n=14
        stat, p_value = wilcoxon(non_zero, alternative="two-sided")
        results.append({
            "feature": feat,
            "n_pairs": len(non_zero),
            "median_diff": float(np.median(d)),
            "mean_diff": float(np.mean(d)),
            "p_value": p_value,
        })

results_df = pd.DataFrame(results).sort_values("p_value")
```

#### Step 2.4: Also Run on Clinical Features

**What:** Apply the same paired analysis to ARFI and DCE-US clinical features. Since ARFI was significant in the unpaired analysis (p<0.001 in late subset), checking whether it remains significant in the paired analysis is a strong validation.

#### Step 2.5: Visualization

- Paired difference plots (dot plot with lines connecting each patient's rej vs no-rej values)
- Histogram of within-patient differences for top features

**Files:**
- Reads: `reports/13_merged_radiomics_clinical.csv`, `../data/bd_estudiUPF.csv` (for `Dias pTXP` if not in merged)
- Writes: `reports/17_paired_analysis_radiomics.csv`, `reports/17_paired_analysis_clinical.csv`, `reports/17_paired_study_selection.csv`

**Effort:** Medium (~3-4 hours). The study selection logic and verification need care.

**Expected outcome:** With only 14 pairs, radiomics features will almost certainly remain non-significant (Wilcoxon with n=14 can only detect very large effects). ARFI might remain significant, which would be a strong finding. Even null radiomics results add thesis value: "even with between-patient variability removed, radiomics texture features show no signal."

**Data dependency check:** Need to verify `Dias pTXP` is in `reports/13_merged_radiomics_clinical.csv`. If not, Step 2.1 needs to join it from the source spreadsheet.

---

## Category 3: Surrounding Region Analysis & Normalization

**Goal:** Use the tissue surrounding the pancreas in the US image as (a) a reference for normalizing intensity across images, and (b) a source of contrast features that may discriminate rejection.

**Why it matters:** Ultrasound image intensity depends heavily on machine settings (gain, depth, frequency), patient body habitus, and probe positioning. Two images of the same pancreas can look very different in absolute intensity. By extracting the region around the pancreas and using it as a per-image reference, we can:
1. **Normalize** pancreas features relative to surrounding tissue, creating a more homogeneous dataset across images
2. **Compare** pancreas vs surrounding tissue -- maybe rejected pancreases look different relative to their surroundings (e.g., different contrast, different texture relationship) even if their absolute texture is indistinguishable
3. **Test** surrounding tissue alone -- maybe rejection causes visible changes in surrounding tissue too (inflammation, edema, fat infiltration)

This is conceptually about *where we look* and *how we normalize*, not about what features we compute.

### Notebook: `18_surrounding_region_analysis.ipynb` (new)

#### Step 3.1: Extract Surrounding Region Mask

**What:** Dilate the pancreas mask to create a ring of tissue around the organ.

**Implementation:**
```python
import cv2

def create_surrounding_mask(mask, dilation_pixels=10):
    """Create a ring mask around the organ by dilating and subtracting."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (dilation_pixels * 2 + 1, dilation_pixels * 2 + 1))
    dilated = cv2.dilate(mask.astype(np.uint8), kernel, iterations=1)
    
    # Ring = dilated minus original
    ring = dilated - mask.astype(np.uint8)
    
    return ring
```

**Dilation sizes to try:** 5, 10, 15 pixels (test sensitivity to ring width)

**Visualization:** For each dilation size, show example images with pancreas mask (red) and surrounding ring (blue) overlaid, so we can visually verify the ring looks reasonable and doesn't extend outside the ultrasound field.

**Edge case:** Some pancreas masks may be near the edge of the ultrasound cone/image. The ring could extend into black (non-image) areas. Need to detect and exclude these pixels (e.g., exclude pixels where image intensity = 0).

#### Step 3.2: Normalize Pancreas by Surrounding Tissue

**What:** For each image, compute mean and std of the surrounding tissue, then z-score normalize the entire image. Re-extract the same 93 PyRadiomics features from the normalized pancreas region.

**Rationale:** If machine settings make image A globally brighter than image B, this normalization removes that difference. Features computed on the normalized image capture *how the pancreas differs from its local surroundings* rather than absolute intensity.

```python
def normalize_by_surrounding(image, organ_mask, surrounding_mask):
    """Normalize image intensities using surrounding tissue as reference."""
    surround_vals = image[surrounding_mask > 0]
    surround_mean = np.mean(surround_vals)
    surround_std = np.std(surround_vals)
    
    if surround_std > 0:
        normalized = (image - surround_mean) / surround_std
    else:
        normalized = image - surround_mean
    
    return normalized

# Then re-run PyRadiomics on (normalized_image, organ_mask)
# This gives 93 "normalized" radiomics features per image
```

**Analysis:** Run the same statistical pipeline as NB 14a (Mann-Whitney, FDR) on the normalized features. Compare p-values before vs after normalization.

#### Step 3.3: Pancreas-vs-Surrounding Contrast Features

**What:** For each image, compute features that describe the *relationship* between pancreas and surrounding tissue. The hypothesis: rejected pancreases may have different contrast with their surroundings compared to non-rejected.

```python
def compute_contrast_features(image, organ_mask, surrounding_mask):
    """Compute features describing pancreas vs surrounding tissue contrast."""
    pancreas_vals = image[organ_mask > 0]
    surround_vals = image[surrounding_mask > 0]
    
    features = {}
    
    # Intensity contrast
    features["contrast_mean_diff"] = np.mean(pancreas_vals) - np.mean(surround_vals)
    features["contrast_mean_ratio"] = np.mean(pancreas_vals) / (np.mean(surround_vals) + 1e-8)
    features["contrast_median_diff"] = np.median(pancreas_vals) - np.median(surround_vals)
    features["contrast_median_ratio"] = np.median(pancreas_vals) / (np.median(surround_vals) + 1e-8)
    
    # Variability contrast
    features["contrast_std_diff"] = np.std(pancreas_vals) - np.std(surround_vals)
    features["contrast_std_ratio"] = np.std(pancreas_vals) / (np.std(surround_vals) + 1e-8)
    
    # Distribution overlap (how different are the two distributions)
    # Kolmogorov-Smirnov statistic: 0 = identical, 1 = completely different
    from scipy.stats import ks_2samp
    ks_stat, _ = ks_2samp(pancreas_vals, surround_vals)
    features["contrast_ks_statistic"] = ks_stat
    
    # Percentile-based contrast
    for pct in [10, 25, 75, 90]:
        features[f"contrast_p{pct}_diff"] = (
            np.percentile(pancreas_vals, pct) - np.percentile(surround_vals, pct)
        )
    
    return features
```

**Feature count:** ~11 contrast features per image (per dilation size)

#### Step 3.4: Features from Surrounding Region Alone

**What:** Extract the same 93 PyRadiomics features from the surrounding ring instead of the pancreas. Test whether surrounding tissue texture itself differs between rejection groups.

```python
# Re-use existing PyRadiomics pipeline but pass surrounding_mask instead of organ_mask
# extractor.execute(sitk_image, sitk_surrounding_mask)
```

**Rationale:** If rejection causes inflammation that extends beyond the pancreas, surrounding tissue features might show signal even when pancreas features don't.

### Pipeline for NB 18

1. Load each image + mask (same loading as NB 12)
2. For each image and each dilation size (5, 10, 15 px):
   a. Create surrounding region mask
   b. Verify mask quality (no out-of-bounds, sufficient pixels)
   c. Normalize image by surrounding tissue stats
   d. Extract PyRadiomics from normalized pancreas
   e. Compute contrast features (pancreas vs surrounding)
   f. Extract PyRadiomics from surrounding region alone
3. Merge all features with clinical labels
4. Run Mann-Whitney + FDR for each feature set separately
5. Compare: which approach (if any) shows more signal than raw PyRadiomics?

**Files:**
- Reads: processed images from `data/processed/`, masks, `reports/13_merged_radiomics_clinical.csv` (for labels)
- Writes: `reports/18_normalized_radiomics.csv`, `reports/18_contrast_features.csv`, `reports/18_surrounding_radiomics.csv`, `reports/18_surrounding_stats.csv`

**Effort:** Medium-Large (~4-6 hours). The mask dilation and normalization are straightforward; running PyRadiomics 3 extra times (normalized, surrounding x3 dilation sizes) takes compute time.

**Expected outcome:** The normalization experiment is the most promising -- if inter-image intensity variation was masking a real signal, normalization could reveal it. The contrast features are novel and quick to compute. Surrounding-tissue-alone is a long shot but easy once the mask exists.

---

## Category 4: Alternative Texture Features (LBP, Gabor, Laws')

**Goal:** Extract texture features not available in PyRadiomics and test them against rejection status using the same statistical pipeline.

**Why it matters:** PyRadiomics computes histogram statistics (firstorder), gray-level co-occurrence matrices (GLCM), run-length matrices (GLRLM), size-zone matrices (GLSZM), dependence matrices (GLDM), and neighborhood tone-difference matrices (NGTDM). These are all well-established radiomics features, but they don't cover all texture analysis methods. LBP, Gabor, and Laws' capture fundamentally different texture properties:
- **LBP:** local micro-patterns (edges, spots, flat regions) -- encodes the relationship between each pixel and its circular neighborhood
- **Gabor:** frequency and orientation content -- responds to periodic patterns at specific scales and directions
- **Laws':** texture energy at different scales -- uses predefined kernels to detect level, edge, spot, ripple, and wave patterns

None of these are in PyRadiomics. If rejection changes ultrasound texture in ways that GLCM/GLRLM/etc. don't capture, these methods might find it.

### Pre-requisite: Install scikit-image

```bash
conda activate thesis_env
pip install scikit-image
```

Currently NOT installed. Needed for LBP and Gabor.

### Notebook: `19_alternative_texture_features.ipynb` (new)

#### Step 4.1: Local Binary Patterns (LBP)

**What:** LBP encodes local texture by comparing each pixel to its circular neighbors. For each pixel, it creates a binary code based on whether neighbors are brighter or darker. The histogram of these codes describes the texture.

**Implementation:**
```python
from skimage.feature import local_binary_pattern

def extract_lbp_features(image, mask, radius=1, n_points=8):
    """Extract LBP histogram features from masked region."""
    lbp = local_binary_pattern(image, n_points, radius, method="uniform")
    
    # Apply mask: only count LBP values inside the ROI
    lbp_masked = lbp[mask > 0]
    
    # Histogram of LBP patterns (uniform LBP has n_points + 2 bins)
    n_bins = n_points + 2
    hist, _ = np.histogram(lbp_masked, bins=n_bins, range=(0, n_bins), density=True)
    
    # Create feature dict
    features = {}
    for i, val in enumerate(hist):
        features[f"lbp_r{radius}_p{n_points}_bin{i}"] = val
    
    return features
```

**Configurations to test:**
- (R=1, P=8): captures fine texture (10 features)
- (R=2, P=16): captures medium texture (18 features)
- (R=3, P=24): captures coarse texture (26 features)

**Feature count:** 10 + 18 + 26 = 54 LBP features per image

#### Step 4.2: Gabor Filters

**What:** Gabor filters respond to texture at specific frequencies and orientations. Each filter is a sinusoidal wave modulated by a Gaussian envelope. The response magnitude describes how much of that frequency/orientation is present.

**Implementation:**
```python
from skimage.filters import gabor

def extract_gabor_features(image, mask, frequencies=[0.1, 0.25, 0.4],
                           thetas=[0, np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3, 5*np.pi/6]):
    """Extract Gabor filter response statistics from masked region."""
    features = {}
    
    for freq in frequencies:
        for theta in thetas:
            # Apply Gabor filter
            filt_real, filt_imag = gabor(image, frequency=freq, theta=theta)
            
            # Magnitude response
            magnitude = np.sqrt(filt_real**2 + filt_imag**2)
            
            # Stats from masked region only
            vals = magnitude[mask > 0]
            
            label = f"gabor_f{freq:.2f}_t{theta:.2f}"
            features[f"{label}_mean"] = float(np.mean(vals))
            features[f"{label}_std"] = float(np.std(vals))
            features[f"{label}_energy"] = float(np.sum(vals**2))
    
    return features
```

**Feature count:** 3 frequencies x 6 orientations x 3 stats = 54 Gabor features per image

#### Step 4.3: Laws' Texture Energy Measures

**What:** Laws' method convolves the image with small 1D kernels (combined into 2D via outer product), then computes local energy. Five kernels capture different properties: Level (smoothing), Edge, Spot, Ripple, Wave.

**Implementation (custom -- no standard library for this):**
```python
from scipy.signal import convolve2d

# Laws' 1D kernels (length 5)
LAWS_KERNELS = {
    "L5": np.array([1, 4, 6, 4, 1]),      # Level (averaging)
    "E5": np.array([-1, -2, 0, 2, 1]),     # Edge
    "S5": np.array([-1, 0, 2, 0, -1]),     # Spot
    "R5": np.array([1, -4, 6, -4, 1]),     # Ripple
    "W5": np.array([-1, 2, 0, -2, 1]),     # Wave
}

def extract_laws_features(image, mask):
    """Extract Laws' texture energy features from masked region."""
    kernel_names = list(LAWS_KERNELS.keys())
    features = {}
    
    for i, name_row in enumerate(kernel_names):
        for j, name_col in enumerate(kernel_names):
            if j < i:  # skip symmetric duplicates
                continue
            
            # 2D kernel = outer product of two 1D kernels
            kernel_2d = np.outer(LAWS_KERNELS[name_row], LAWS_KERNELS[name_col])
            
            # Convolve image
            response = convolve2d(image.astype(float), kernel_2d, mode="same")
            
            # Energy = mean of absolute response in masked region
            vals = np.abs(response[mask > 0])
            
            label = f"laws_{name_row}{name_col}"
            features[f"{label}_mean"] = float(np.mean(vals))
            features[f"{label}_std"] = float(np.std(vals))
            features[f"{label}_energy"] = float(np.sum(vals**2) / len(vals))
    
    return features
```

**Feature count:** 15 unique kernel pairs (upper triangle of 5x5) x 3 stats = 45 Laws' features per image

### Pipeline for NB 19

1. Load each image + mask (same loading as NB 12)
2. For each image:
   a. Extract LBP features (3 radius configs)
   b. Extract Gabor features (3 freq x 6 orientation)
   c. Extract Laws' features (15 kernel pairs)
3. Total: ~153 alternative features per image (54 LBP + 54 Gabor + 45 Laws')
4. Merge with clinical labels
5. Run Mann-Whitney + FDR correction (same approach as NB 14a)
6. Report: how many significant? Compare to 0/93 from PyRadiomics
7. If any significant, run ML classification with these features

**Files:**
- Reads: processed images from `data/processed/` (grayscale numpy + masks), `reports/13_merged_radiomics_clinical.csv` (for labels)
- Writes: `reports/19_alternative_features.csv`, `reports/19_alternative_stats.csv`

**Effort:** Medium (~3-4 hours). The feature extraction functions are straightforward. Main work is loading images, extracting, and running stats.

**Expected outcome:** Likely still null -- if the underlying ultrasound texture truly doesn't differ between groups, no feature extraction method will find signal. But this rules out the possibility that we just used the wrong features, which is a valid concern. Even a null result here strengthens the thesis: "we tried 93 PyRadiomics features AND 153 alternative texture features -- none discriminate rejection."

---

## Implementation Order Recommendation

| Priority | Category | Notebook | Effort | Thesis Value |
|----------|----------|----------|--------|-------------|
| 1 | Cat 1: ML improvements | `16_ml_improvements.ipynb` | Small (1-2h) | High: shows rigor, required by supervisor |
| 2 | Cat 2: Paired analysis | `17_paired_analysis.ipynb` | Medium (3-4h) | High: novel analysis, strongest internal validity |
| 3 | Cat 4: Alt. texture features | `19_alternative_texture_features.ipynb` | Medium (3-4h) | Medium: rules out "wrong features" concern |
| 4 | Cat 3: Surrounding region | `18_surrounding_region_analysis.ipynb` | Medium-Large (4-6h) | Medium-High: novel normalization idea, most creative |

**Recommendation:** Do Categories 1 and 2 first -- quick wins with highest thesis value. Then Category 4 (alternative features) since it's simpler and directly tests whether different features find signal. Category 3 (surrounding region) last since it's the most involved, but it's also the most novel and creative idea -- the normalization approach could genuinely reveal hidden signal if inter-image intensity variation was a confound.

---

## Critical Files

| File | Role |
|------|------|
| `analysis/15_feature_selection_and_ml.ipynb` | Base code to extend for NB 16 |
| `analysis/14a_stats_radiomics_features.ipynb` | Statistical analysis pattern to follow |
| `reports/13_merged_radiomics_clinical.csv` | Input data (134 rows, has `patient_id`, 93 radiomics features) |
| `reports/14a_stats_radiomics_features.csv` | P-values for feature selection |
| `../data/bd_estudiUPF.csv` | Source spreadsheet (has `Dias pTXP` column for paired analysis) |
| `docs/PLAN_REPEATED_MEASURES.md` | Approach 7 has paired analysis code template |
| `analysis/12_extract_radiomics_all_images.ipynb` | Image loading pattern for NB 18/19 |
| `docs/PREPROCESSING_PIPELINE.md` | How images are preprocessed (needed for NB 18/19) |

---

## Coding Standards

Per `AGENT_HANDOFF.md`: write code a plain junior engineer would understand. No list comprehensions, no lambda functions, explicit loops, descriptive variable names, comments explaining non-obvious logic. Follow the style of existing notebooks 12-15.

---

## Verification

For each notebook:
1. Run all cells top to bottom, verify no errors
2. Check output CSV files are saved correctly to `reports/`
3. Cross-check sample sizes match expectations (134 total, 14 paired patients, etc.)
4. Verify no data leakage in ML pipeline (scaling/selection inside CV folds)
5. Compare new results against existing results to confirm consistency where expected
