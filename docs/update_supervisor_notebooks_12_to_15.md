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

*Notebooks 13, 14a, 14b, 15 — to be added as we review each one.*
