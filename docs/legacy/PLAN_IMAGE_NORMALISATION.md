# Plan: Replicate All Results with Image Normalisation

## Context

**Supervisor feedback:** Image normalisation and feature standardisation are a must.

**Our response after investigation:**
- Feature standardisation (StandardScaler): ALREADY DONE in all ML pipelines, correctly inside Pipeline inside CV (no leakage)
- Image normalisation: NOT DONE — raw pixels (0-255) go into PyRadiomics in NB 12

**Goal:** Re-extract radiomics features with PyRadiomics `normalize=True` and replicate all downstream analyses. Keep original notebooks unchanged — create parallel versions with `_normalised` suffix.

---

## Data Leakage: NOT a concern

PyRadiomics normalisation is **per-image**: each image z-scored using its OWN mean and std. No cross-image information is used. When train/test splits happen later (in ML), each image was already independently normalised — no leakage possible.

StandardScaler in ML: inside Pipeline inside CV. Fitted on training fold only. No leakage.

---

## Data Flow: Original vs Normalised

```
ORIGINAL:                                    NORMALISED (new):
12_extract... → 12_radiomics_features.csv    12_extract..._normalised → 12_radiomics_features_normalised.csv
      ↓                                              ↓
13_merge... → 13_merged.csv                  13_merge..._normalised → 13_merged_normalised.csv
      ↓                                              ↓
14a_stats... (full dataset)                  14a_stats..._normalised (full dataset)
      ↓                                              ↓
17b_ml... (full dataset ML)                  17b_ml..._normalised (full dataset ML)
      ↓                                              ↓
18_build_independent → 18_independent.csv    18_build..._normalised → 18_independent_normalised.csv
      ↓           ↓                                  ↓           ↓
19_stats_indep   20_ml_indep                 19_stats..._normalised  20_ml..._normalised
      ↓                                              ↓
21_paired_analysis                           21_paired..._normalised
```

---

## Notebooks to Create (8 total)

Each is a copy of the original with minimal changes: different input/output file paths and (for NB 12) the PyRadiomics settings.

### 1. `12_extract_radiomics_all_images_normalised.ipynb`

**Change from original NB 12:**
```python
# ORIGINAL:
settings = {"force2D": True, "force2Ddimension": 0}

# NEW:
settings = {
    "force2D": True,
    "force2Ddimension": 0,
    "normalize": True,
    "normalizeScale": 100,
    "removeOutliers": 3,
}
```
**Output:** `reports/12_radiomics_features_normalised.csv`

### 2. `13_merge_clinical_and_radiomics_normalised.ipynb`

**Change from original NB 13:**
- Load `reports/12_radiomics_features_normalised.csv` instead of `12_radiomics_features_k3_i1.csv`
- Save to `reports/13_merged_radiomics_clinical_normalised.csv`

### 3. `14a_stats_radiomics_features_normalised.ipynb`

**Change from original NB 14a:**
- Load `reports/12_radiomics_features_normalised.csv`
- Save to `reports/14a_stats_radiomics_features_normalised.csv` (+ PNGs with _normalised suffix)

### 4. `17b_ml_joint_optimization_normalised.ipynb`

**Change from original NB 17b:**
- Load `reports/13_merged_radiomics_clinical_normalised.csv`
- Load `reports/14a_stats_radiomics_features_normalised.csv`
- Save to `reports/17b_joint_optimization_results_normalised.csv` (+ PNG)

### 5. `18_build_independent_dataset_normalised.ipynb`

**Change from original NB 18:**
- Load `reports/13_merged_radiomics_clinical_normalised.csv`
- Save to `reports/18_independent_dataset_normalised.csv`
- Same selection logic (1 study per patient, prefer first rejection study)

### 6. `19_stats_independent_dataset_normalised.ipynb`

**Change from original NB 19:**
- Load `reports/18_independent_dataset_normalised.csv`
- Load `reports/14a_stats_radiomics_features_normalised.csv` (for comparison)
- Save to `reports/19_stats_independent_dataset_normalised.csv` (+ PNGs)

### 7. `20_ml_independent_dataset_normalised.ipynb`

**Change from original NB 20:**
- Load `reports/18_independent_dataset_normalised.csv`
- Load `reports/19_stats_independent_dataset_normalised.csv`
- Load `reports/17b_joint_optimization_results_normalised.csv` (for comparison)
- Same ML pipeline (StandardScaler still inside Pipeline — still needed even with image normalisation because different features have different scales)
- Save to `reports/20_ml_independent_dataset_results_normalised.csv` (+ PNGs)

### 8. `21_paired_analysis_normalised.ipynb`

**Change from original NB 21:**
- Load `reports/13_merged_radiomics_clinical_normalised.csv`
- Load `reports/14a_stats_radiomics_features_normalised.csv` (for comparison)
- Load `reports/19_stats_independent_dataset_normalised.csv` (for comparison)
- Save to `reports/21_paired_analysis_radiomics_normalised.csv` (+ PNGs)

---

## What Changes in Each Notebook (Summary)

| Notebook | Lines that change | Nature of change |
|----------|-------------------|------------------|
| 12 | PyRadiomics settings (1 cell), output path (2 lines) | Core change: add normalize settings |
| 13 | Input path (1 line), output path (1 line) | Path only |
| 14a | Input path (1-2 lines), output paths (3-4 lines) | Path only |
| 17b | Input paths (2 lines), output paths (2 lines) | Path only |
| 18 | Input path (1 line), output path (1 line) | Path only |
| 19 | Input paths (2 lines), output paths (4 lines) | Path only |
| 20 | Input paths (3 lines), output paths (4 lines) | Path only |
| 21 | Input paths (3 lines), output paths (5 lines) | Path only |

---

## Execution Order

Must be sequential (each depends on the previous):
1. NB 12 (extraction ~2-3 min)
2. NB 13 (merge, instant)
3. NB 14a (stats, seconds)
4. NB 18 (build independent, instant)
5. NB 17b (ML full dataset, ~30 sec)
6. NB 19 (stats independent, seconds)
7. NB 20 (ML independent, ~30 sec)
8. NB 21 (paired analysis, seconds)

---

## Key Question: Do We Also Need a "Standardised Feature Dataset"?

The supervisor mentioned both "image normalisation" and "feature standardization". We clarified that feature standardisation IS done via StandardScaler in ML. But should we ALSO produce a CSV with pre-standardised features?

**Answer: NO.**
- For ML: StandardScaler inside Pipeline is the correct approach (fitted on training data per fold)
- For stats: standardising features doesn't change Mann-Whitney results (rank-based) or t-test results (invariant to linear transforms)
- Producing a pre-standardised CSV would actually be WRONG because it would fit StandardScaler on ALL data (including test), introducing leakage

The only thing we need is the image normalisation step (which produces different features entirely).

---

## Expected Impact on Results

**Most likely:** Results remain negative (no FDR-significant features, ML at chance).

Reasoning:
- Image normalisation changes absolute values but preserves relative patterns
- GLCM/GLRLM/GLSZM/GLDM features are based on co-occurrence patterns — partially robust to intensity shifts
- The discretisation will change (different number of bins), which DOES change texture features
- But if no signal exists in the tissue, normalisation cannot create one

**If results change:** Would indicate acquisition variability was masking a real signal. Would require updating thesis Results + Discussion.

---

## Files Summary

**New notebooks (8):**
- `analysis/12_extract_radiomics_all_images_normalised.ipynb`
- `analysis/13_merge_clinical_and_radiomics_normalised.ipynb`
- `analysis/14a_stats_radiomics_features_normalised.ipynb`
- `analysis/17b_ml_joint_optimization_normalised.ipynb`
- `analysis/18_build_independent_dataset_normalised.ipynb`
- `analysis/19_stats_independent_dataset_normalised.ipynb`
- `analysis/20_ml_independent_dataset_normalised.ipynb`
- `analysis/21_paired_analysis_normalised.ipynb`

**New output CSVs (8):**
- `analysis/reports/12_radiomics_features_normalised.csv`
- `analysis/reports/13_merged_radiomics_clinical_normalised.csv`
- `analysis/reports/14a_stats_radiomics_features_normalised.csv`
- `analysis/reports/17b_joint_optimization_results_normalised.csv`
- `analysis/reports/18_independent_dataset_normalised.csv`
- `analysis/reports/19_stats_independent_dataset_normalised.csv`
- `analysis/reports/20_ml_independent_dataset_results_normalised.csv`
- `analysis/reports/21_paired_analysis_radiomics_normalised.csv`

---

## Verification

After running all notebooks:
1. NB 12 normalised: 93 features x 137 studies (same shape as original)
2. Feature values differ from original (confirm with correlation check)
3. Stats results: report how many uncorrected/FDR significant
4. ML results: report AUCs with CIs
5. Compare all results side-by-side with originals
