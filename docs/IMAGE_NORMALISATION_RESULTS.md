# Image Normalisation - What Was Done and Results

## Background

Supervisor feedback (May 2026): image normalisation and feature standardisation are essential in image processing and machine learning.

After investigation:
1. **Feature standardisation** (z-score of extracted features before ML) - already done correctly via `StandardScaler` inside sklearn `Pipeline`, fitted per-fold with no data leakage.
2. **Image normalisation** (z-score of pixel intensities before feature extraction) - was NOT done in the original pipeline.

Image normalisation was added, producing a parallel set of results. The normalised results are reported as primary in the thesis.

## PyRadiomics normalisation settings

```python
settings = {
    "force2D": True,
    "force2Ddimension": 0,
    "normalize": True,
    "normalizeScale": 100,
    "removeOutliers": 3,
}
```

This applies per-ROI z-score normalisation: each pixel is transformed as `(pixel - mean) / std * 100`, with outliers beyond 3 standard deviations clipped first. The scale factor of 100 preserves numerical precision for texture features.

This is a per-image operation - no cross-image information is used, so there is no data leakage when train/test splits happen later.

## Notebooks created

Eight notebooks with `_normalised` suffix, each a copy of the original with updated paths:

| Notebook | Purpose | Output CSV |
|----------|---------|------------|
| `12_extract_radiomics_all_images_normalised` | Feature extraction with normalisation | `12_radiomics_features_normalised.csv` |
| `13_merge_clinical_and_radiomics_normalised` | Merge with clinical labels | `13_merged_radiomics_clinical_normalised.csv` |
| `14a_stats_radiomics_features_normalised` | Univariate stats (137 studies) | `14a_stats_radiomics_features_normalised.csv` |
| `17b_ml_joint_optimization_normalised` | ML on full dataset (LOOCV) | `17b_joint_optimization_results_normalised.csv` |
| `18_build_independent_dataset_normalised` | 1-per-patient dataset | `18_independent_dataset_normalised.csv` |
| `19_stats_independent_dataset_normalised` | Univariate stats (55 studies) | `19_stats_independent_dataset_normalised.csv` |
| `20_ml_independent_dataset_normalised` | ML on independent dataset (10-fold CV) | `20_ml_independent_dataset_results_normalised.csv` |
| `21_paired_analysis_normalised` | Within-patient paired tests | `21_paired_analysis_radiomics_normalised.csv` |

Original notebooks and results are untouched.

## Results comparison

### Univariate statistics - full dataset (N=137)

| Metric | Original | Normalised |
|--------|----------|------------|
| Features with uncorrected p < 0.05 | 0 | 4 |
| Features surviving FDR correction | 0 | 0 |

### Univariate statistics - independent dataset (N=55)

| Metric | Original | Normalised |
|--------|----------|------------|
| Features with uncorrected p < 0.05 | 4 | 24 |
| Features surviving FDR correction | 0 | 0 |

### Paired analysis (14 patients with both outcomes)

| Metric | Original | Normalised |
|--------|----------|------------|
| Features with uncorrected p < 0.05 | 59 | 47 |
| Features surviving FDR correction | 0 | 0 |

### ML classification - full dataset (N=137, LOOCV)

| Model | Original AUC | Normalised AUC |
|-------|-------------|----------------|
| LogReg | 0.501 | 0.535 |
| RF | 0.399 | 0.564 |
| SVM | 0.531 | 0.417 |
| NaiveBayes | 0.537 | 0.533 |

### ML classification - independent dataset (N=55, 10-fold CV)

| Model | Original AUC | Normalised AUC |
|-------|-------------|----------------|
| LogReg | 0.569 | 0.636 |
| RF | 0.506 | 0.588 |
| SVM | 0.283 | 0.408 |
| NaiveBayes | 0.508 | 0.618 |

Best normalised: LogReg 0.636, 95% CI [0.48, 0.78] - still includes 0.5.

### Feature count after correlation removal (|r| > 0.9)

| Dataset | Original | Normalised |
|---------|----------|------------|
| Features retained | 32 | 27 |

## Conclusions

1. **Scientific conclusion unchanged.** No features survive FDR correction in any analysis. All ML models produce AUC values consistent with chance. Radiomics texture features do not carry detectable signal for rejection.

2. **Normalisation produces marginally different numbers but identical interpretation.** More uncorrected trends appear (24 vs 4 on the independent dataset), and ML AUCs are slightly higher (0.636 vs 0.569 best), but these are within noise for N=55.

3. **Best practice satisfied.** The normalised results are reported as primary in the thesis, addressing the supervisor's feedback while showing that the conclusion is robust to this methodological choice.

## Technical notes

- Mann-Whitney U is rank-based, so feature standardisation alone would not change p-values
- `normalizeScale=100` with default `binWidth=25` gives approximately 8-12 effective bins for texture features
- Original notebooks are preserved intact for reproducibility
