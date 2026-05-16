# Next Steps: NB 22 and NB 23 (Final Experiment Notebooks)

## Context

All core analysis is complete (NB 01-21). The overall finding is negative: B-mode ultrasound radiomics features do not predict pancreas transplant rejection. NB 22 and 23 are the final experiments. Their purpose is to **rule out alternative explanations** for the negative result:

- NB 22 asks: "Did we use the wrong texture features?" If LBP, Gabor, and Laws' also show no signal, the answer is no - no texture method works on this data.
- NB 23 asks: "Did inter-image intensity variation mask a real signal?" If normalizing by surrounding tissue still shows nothing, the answer is no.

**Both notebooks are expected to produce negative results.** That is a valid and useful finding for the thesis. It strengthens the conclusion that the limitation is fundamental (grayscale US lacks the tissue property information needed) rather than methodological.

After NB 22-23, no further experiment notebooks are planned.

---

## Environment Prerequisites

**scikit-image is NOT installed** in `thesis_env`. It is needed for LBP in NB 22.

Install before starting NB 22:
```bash
conda activate thesis_env
pip install scikit-image
```

Verify:
```python
from skimage.feature import local_binary_pattern
print("OK")
```

All other packages needed are already available:
- `scipy` (1.13.1) - for `convolve2d` (Laws') and `stats` (Wilcoxon, Mann-Whitney)
- `cv2` (4.13.0) - for Gabor kernels (`cv2.getGaborKernel`, `cv2.filter2D`), mask dilation
- `numpy`, `pandas`, `matplotlib` - standard
- `radiomics` (PyRadiomics) - needed in NB 23 for re-extraction on normalized images
- `SimpleITK` - needed in NB 23 for PyRadiomics input format

---

## How Images and Masks Are Loaded

All 137 studies follow the same pattern (established in NB 12):

```python
import cv2, pydicom, os, numpy as np

raw_folder = os.path.join("..", "data", "PANCREAS_2", "PANCREAS_2")
mask_folder = os.path.join("..", "data", "PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1", "masks")

def load_grayscale_and_mask(study_id):
    """Load DICOM as grayscale numpy array + binary mask."""
    # Find DICOM
    patient_folder = os.path.join(raw_folder, study_id)
    subfolders = [f for f in os.listdir(patient_folder) if not f.startswith(".")]
    date_folder = os.path.join(patient_folder, subfolders[0])
    files = [f for f in os.listdir(date_folder) if not f.startswith(".")]
    dicom_path = os.path.join(date_folder, files[0])

    # Read DICOM -> grayscale
    ds = pydicom.dcmread(dicom_path)
    pixels = ds.pixel_array
    if len(pixels.shape) == 3:
        gray = cv2.cvtColor(pixels, cv2.COLOR_RGB2GRAY)
    else:
        gray = pixels

    # Load mask (0/255 uint8 PNG -> binary 0/1)
    mask_path = os.path.join(mask_folder, f"{study_id}_mask_eroded_k3_i1.png")
    mask_raw = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    mask_binary = (mask_raw > 0).astype(np.uint8)

    # Handle shape mismatch (rare: studies 03_01, 43_01)
    if gray.shape != mask_binary.shape:
        mask_binary = cv2.resize(mask_binary, (gray.shape[1], gray.shape[0]),
                                 interpolation=cv2.INTER_NEAREST)

    return gray, mask_binary
```

**Key facts:**
- Images: 768x1024, uint8, 0-255
- Masks: 768x1024, binary (0 or 1 after conversion)
- 137 studies total (137 mask files in the masks folder)
- Study IDs come from `reports/13_merged_radiomics_clinical.csv` column `study_id`

---

## NB 22: Alternative Texture Features

### Goal

Extract 3 families of texture features not in PyRadiomics, test them against rejection status. Total: ~153 new features per image.

### Feature Families

**1. LBP (Local Binary Patterns)** - requires `scikit-image`

Encodes local micro-patterns by comparing each pixel to its circular neighborhood.

Configurations:
- (R=1, P=8): fine texture → 10 histogram bins
- (R=2, P=16): medium texture → 18 histogram bins
- (R=3, P=24): coarse texture → 26 histogram bins

Total: 54 LBP features per image.

Method: compute LBP on full image, then extract histogram only from pixels inside the mask.

**2. Gabor Filters** - uses `cv2.getGaborKernel` + `cv2.filter2D`

Responds to texture at specific frequencies and orientations.

Configurations:
- Frequencies (lambda): 3 values (e.g., 5, 10, 20 pixels wavelength)
- Orientations (theta): 6 values (0, 30, 60, 90, 120, 150 degrees)
- Stats per response: mean, std, energy (from masked region)

Total: 3 × 6 × 3 = 54 Gabor features per image.

Method: apply each Gabor filter to full image, compute magnitude response, extract stats from masked region only.

**3. Laws' Texture Energy Measures** - uses `scipy.signal.convolve2d`

Detects texture energy using predefined 1D kernels combined into 2D filters.

Five 1D kernels (L5, E5, S5, R5, W5). Compute all unique 2D combinations (upper triangle of 5×5 = 15 pairs). Stats per response: mean, std, energy.

Total: 15 × 3 = 45 Laws' features per image.

Method: convolve full image with each 2D kernel, extract stats from masked region.

### Analysis Pipeline

1. **Extract features** from all 137 studies → save as `reports/22_alternative_features.csv` (137 rows × ~154 cols including study_id)
2. **Stats on full dataset (137 studies):**
   - Normality check (Shapiro-Wilk) → choose t-test or Mann-Whitney per feature
   - Uncorrected p-values + effect sizes
   - Benjamini-Hochberg FDR correction across all ~153 features
   - Same approach as NB 14a
3. **Stats on independent dataset (55 studies):**
   - Filter to 55 studies using `reports/18_independent_dataset.csv`
   - Same statistical tests
   - Same approach as NB 19
4. **ML on independent dataset (55 studies):**
   - Correlation removal (|r| > 0.9, guided by p-values from step 3)
   - Pipeline: StandardScaler → SelectKBest(f_classif) → model
   - 4 models: LogReg, RF, SVM, NaiveBayes (same as NB 20)
   - 10-fold stratified CV (primary), LOOCV (comparison)
   - Same approach as NB 20
5. **Comparison:** side-by-side table of PyRadiomics (93 features) vs alternative (153 features) results

### Output Files

- `reports/22_alternative_features.csv` - raw features (137 × ~154)
- `reports/22_stats_full_dataset.csv` - stats on 137 studies
- `reports/22_stats_independent_dataset.csv` - stats on 55 studies
- `reports/22_ml_results.csv` - ML classification results
- `reports/22_roc_curves.png` - ROC curves if any model exceeds AUC 0.55

### What NOT to do

- Do NOT run paired analysis on these features (NB 21 is self-contained, n=14 is too small for 153 features)
- Do NOT apply FDR correction to clinical features (that convention is from Clara's paper)
- Do NOT combine alternative features with PyRadiomics features in ML (test them separately to answer "do different features find signal?")

---

## NB 23: Surrounding Tissue Analysis

### Goal

Use tissue surrounding the pancreas to (a) normalize intensity variation across images, and (b) compute contrast features. Re-extract PyRadiomics on normalized images. Test everything against rejection.

### Approach

**Step 1: Create surrounding tissue mask**

Dilate the pancreas mask by N pixels, subtract the original → ring of surrounding tissue.

```python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*N+1, 2*N+1))
dilated = cv2.dilate(mask_binary, kernel, iterations=1)
surrounding = dilated - mask_binary
```

Use dilation of 10 pixels as primary (also try 5 and 15 for sensitivity check).

**Edge case:** The ring might extend into black regions (outside the ultrasound cone). Exclude pixels where the original image intensity = 0:
```python
surrounding[gray == 0] = 0
```

**Step 2: Z-score normalize pancreas by surrounding tissue**

```python
surround_vals = gray[surrounding > 0]
surround_mean = np.mean(surround_vals)
surround_std = np.std(surround_vals)
normalized = (gray.astype(float) - surround_mean) / surround_std
```

**Step 3: Re-extract PyRadiomics on normalized image**

Convert the normalized (float) image back to int16 range, then run through the same PyRadiomics extractor as NB 12. This gives 93 "normalized radiomics" features per image.

Important: the normalized image has negative values and is float. Scale to int16 range before passing to PyRadiomics:
```python
# Scale to int16 range for PyRadiomics
norm_scaled = np.clip(normalized * 1000, -32768, 32767).astype(np.int16)
sitk_image = sitk.GetImageFromArray(norm_scaled)
```

**Step 4: Compute contrast features (pancreas vs surrounding)**

~11 features per image describing the relationship between pancreas and surrounding tissue:
- Mean/median difference and ratio
- Std difference and ratio
- KS statistic (distribution dissimilarity)
- Percentile-based contrasts (10th, 25th, 75th, 90th)

### Analysis Pipeline

1. **For each of 137 studies:** create surrounding mask, normalize, extract normalized radiomics (93 features), compute contrast features (~11 features)
2. **Save:** `reports/23_normalized_radiomics.csv` (137 × 94), `reports/23_contrast_features.csv` (137 × ~12)
3. **Stats on full dataset (137 studies)** - same pipeline as NB 14a for both feature sets
4. **Stats on independent dataset (55 studies)** - same as NB 19
5. **ML on independent dataset (55 studies)** - same as NB 20, run separately on:
   - Normalized radiomics features (93, after correlation removal)
   - Contrast features (~11, possibly combined with normalized radiomics)
6. **Comparison table:** original radiomics vs normalized radiomics vs contrast features

### Output Files

- `reports/23_normalized_radiomics.csv` - normalized PyRadiomics features
- `reports/23_contrast_features.csv` - pancreas-vs-surrounding features
- `reports/23_stats_normalized.csv` - stats on normalized features
- `reports/23_stats_contrast.csv` - stats on contrast features
- `reports/23_ml_results.csv` - ML results
- `reports/23_surrounding_mask_examples.png` - QA visualization (3-4 example images with mask + ring overlay)

### What NOT to do

- Do NOT extract radiomics from the surrounding ring alone (low priority, adds complexity for unlikely payoff)
- Do NOT test multiple dilation sizes in ML (pick 10px as primary; show 5/15 sensitivity only in stats)
- Do NOT run paired analysis on these features

---

## Shared Conventions (both notebooks)

### Coding style
- Junior-engineer style: explicit loops, descriptive variable names, cells under 40 lines
- Print progress every 10 studies during extraction loops
- No emojis, no AI-ish formatting

### Statistical pipeline (same as NB 14a/19)
- Shapiro-Wilk normality check per feature per group
- Both normal → Welch's t-test; otherwise → Mann-Whitney U
- Effect size: Cohen's d (t-test) or rank-biserial correlation (Mann-Whitney)
- FDR correction: Benjamini-Hochberg across ALL features in the notebook

### ML pipeline (same as NB 20)
- Correlation removal: |r| > 0.9, drop the feature with the higher p-value
- Pipeline: StandardScaler → SelectKBest(f_classif) → model
- k values: [5, 10, 15, 20, max_remaining]
- Models: LogReg (C=[0.01, 0.1, 1, 10]), RF (max_depth=[3,5,7], min_samples_leaf=[3,5,10]), SVM (C=[0.1,1,10], kernel=[linear, rbf]), NaiveBayes (var_smoothing=[1e-9, 1e-7, 1e-5])
- All with class_weight="balanced" where applicable, random_state=42
- Inner CV: 5-fold stratified; Outer CV: 10-fold stratified (primary)
- LOOCV as comparison
- Bootstrap 95% CI on 10-fold AUC (1000 resamples)

### Data sources
- Full dataset labels: `reports/13_merged_radiomics_clinical.csv` (column `rejection`, column `study_id`)
- Independent dataset: `reports/18_independent_dataset.csv` (55 rows, same columns)
- Study IDs for extraction: use the 137 study_ids from `13_merged_radiomics_clinical.csv`

### Interpretation cell
Each notebook ends with a markdown cell interpreting the results. Frame around the thesis question: "does this alternative approach reveal signal that standard PyRadiomics missed?"

---

## After NB 22-23: What Remains

Once these notebooks are complete, the experimental work for the thesis is done. Remaining tasks are all thesis-writing:

1. **Results sections 3.5-3.7** - write up paired analysis (NB 21) and extended analysis (NB 22-23) results in LaTeX
2. **Related Work** - 4 subsections currently TODO stubs in `thesis/introduction.tex`
3. **Discussion and Conclusions** - interpret overall findings, limitations, future work
4. **Abstract** - finalize after all sections are written
5. **Final figures** - any additional thesis-quality plots needed from NB 22-23 results

Timeline: NB 22-23 should be done by May 30. Thesis to Gemma by June 8.

---

## Key Numbers for Reference

| Dataset | Studies | Patients | Rejection | No rejection |
|---------|---------|----------|-----------|--------------|
| Full | 137 | 56 | 39 (28%) | 98 (72%) |
| Independent | 55 | 55 | 21 (38%) | 34 (62%) |
| Paired | 14 pairs | 14 | 14 | 14 |

| Analysis | Best finding | After FDR |
|----------|-------------|-----------|
| Radiomics stats (137) | firstorder_Minimum p=0.053 | All >0.84 |
| Radiomics stats (55) | ngtdm_Busyness p=0.024 | All >0.38 |
| Paired radiomics (14) | ngtdm_Coarseness p=0.011 | All >0.28 |
| ML full dataset | NaiveBayes AUC 0.537 | - |
| ML independent | LogReg AUC 0.569 [0.40, 0.72] | - |
| Clinical (late >90d) | ARFI media p<0.001 | - |

---

## File Dependencies

```
NB 22 reads:
  data/PANCREAS_2/PANCREAS_2/          (raw DICOMs for grayscale images)
  data/.../masks/                       (binary masks)
  reports/13_merged_radiomics_clinical.csv  (study_ids + labels)
  reports/18_independent_dataset.csv       (independent subset)

NB 23 reads:
  (same as NB 22, plus)
  NB 12's PyRadiomics extractor config  (force2D, 6 feature classes)

Both write to:
  reports/22_*.csv, reports/23_*.csv
```
