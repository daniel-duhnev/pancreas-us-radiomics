# Image Normalisation: What Was Done and Results Comparison

## Motivation

Supervisor feedback (May 2026): "I am seeing that in the pre-processing you do not normalise the images nor standardise the features. It is essential to do that in image processing and machine learning."

Investigation revealed two distinct steps:
1. **Feature standardisation** (z-score of extracted features before ML): already done correctly via `StandardScaler` inside sklearn `Pipeline`, fitted per-fold with no data leakage.
2. **Image normalisation** (z-score of pixel intensities before feature extraction): NOT done in the original pipeline.

Image normalisation was then added as best practice, producing a parallel set of results for comparison.

## What Was Done

### PyRadiomics normalisation settings

Added to the feature extractor in NB 12 (normalised version):

```python
settings = {
    "force2D": True,
    "force2Ddimension": 0,
    "normalize": True,
    "normalizeScale": 100,
    "removeOutliers": 3,
}
```

This applies per-ROI z-score normalisation: `normalised_pixel = (pixel - mean_ROI) / std_ROI * 100`, with outliers beyond 3 standard deviations clipped before computing statistics. The scale factor of 100 preserves numerical precision for texture features.

### Notebooks created

Eight new notebooks with `_normalised` suffix, each a copy of the original with paths updated:

| Notebook | Purpose | Output |
|----------|---------|--------|
| `12_extract_radiomics_all_images_normalised.ipynb` | Feature extraction with normalisation | `12_radiomics_features_normalised.csv` |
| `13_merge_clinical_and_radiomics_normalised.ipynb` | Merge with clinical labels | `13_merged_radiomics_clinical_normalised.csv` |
| `14a_stats_radiomics_features_normalised.ipynb` | Univariate stats (137 studies) | `14a_stats_radiomics_features_normalised.csv` |
| `17b_ml_joint_optimization_normalised.ipynb` | Joint feature+hyperparameter search | `17b_joint_optimization_results_normalised.csv` |
| `18_build_independent_dataset_normalised.ipynb` | 1-per-patient dataset | `18_independent_dataset_normalised.csv` |
| `19_stats_independent_dataset_normalised.ipynb` | Univariate stats (55 studies) | `19_stats_independent_dataset_normalised.csv` |
| `20_ml_independent_dataset_normalised.ipynb` | ML on independent dataset | `20_ml_independent_dataset_results_normalised.csv` |
| `21_paired_analysis_normalised.ipynb` | Within-patient paired tests | `21_paired_analysis_radiomics_normalised.csv` |

All output CSVs and figures are in `analysis/reports/` with `_normalised` suffix. Original notebooks and results are untouched.

## Results Comparison

### Univariate statistics (full dataset, N=137)

| Metric | Original | Normalised |
|--------|----------|------------|
| Features with uncorrected p < 0.05 | 0 | 4 |
| Features surviving FDR correction | 0 | 0 |

The 4 uncorrected-significant features in the normalised analysis are all first-order intensity features (Minimum, 10Percentile, Median, Mean) with small effect sizes (rank-biserial r ~ 0.22-0.25). None survive multiple testing correction.

### Univariate statistics (independent dataset, N=55)

| Metric | Original | Normalised |
|--------|----------|------------|
| Features with uncorrected p < 0.05 | 4 | 24 |
| Features surviving FDR correction | 0 | 0 |

The normalised analysis finds more uncorrected trends (24 vs 4), predominantly first-order intensity features. However, none survive FDR correction in either case, and this is expected given the small sample size and large feature space.

### Paired analysis (14 patients with both outcomes)

| Metric | Original | Normalised |
|--------|----------|------------|
| Features with uncorrected p < 0.05 | 59 | 47 |
| Features surviving FDR correction | 0 | 0 |

### ML classification (full dataset, N=137, LOOCV)

| Model | Original AUC | Normalised AUC |
|-------|-------------|----------------|
| LogReg | 0.501 | 0.535 |
| RF | 0.399 | 0.564 |
| SVM | 0.531 | 0.417 |
| NaiveBayes | 0.537 | 0.533 |

Best original: NaiveBayes 0.537. Best normalised: RF 0.564. Both near chance.

### ML classification (independent dataset, N=55, 10-fold CV)

| Model | Original AUC | Normalised AUC |
|-------|-------------|----------------|
| LogReg | 0.569 | 0.636 |
| RF | 0.506 | 0.588 |
| SVM | 0.283 | 0.408 |
| NaiveBayes | 0.508 | 0.618 |

Best original: LogReg 0.569. Best normalised: LogReg 0.636. Modest improvement but all 95% CIs include 0.5 given N=55.

### Feature count after correlation removal (|r| > 0.9)

| Dataset | Original | Normalised |
|---------|----------|------------|
| Features retained | 32 | 27 |

Normalisation changes inter-feature correlations slightly, resulting in fewer features after the correlation filter.

## Conclusions

1. **Scientific conclusion unchanged.** No features survive FDR correction in any analysis. All ML models produce AUC values consistent with chance classification. B-mode ultrasound radiomics texture features do not carry detectable signal for pancreas transplant rejection.

2. **Normalisation produces marginally different numbers but identical interpretation.** The normalised pipeline shows slightly more uncorrected trends in the independent dataset (24 vs 4 features at p < 0.05), and slightly higher ML AUC values (0.636 vs 0.569 best), but these are within noise for N=55 and none survive multiple testing correction.

3. **Best practice satisfied.** The normalised results are reported as primary in the thesis, with the original results available for comparison. This addresses the supervisor's feedback while demonstrating that the scientific conclusion is robust to this methodological choice.

## Technical notes

- Feature standardisation (StandardScaler inside Pipeline inside CV) was already correct and unchanged.
- Mann-Whitney U is rank-based, so feature standardisation would not change statistical test p-values.
- The `normalizeScale=100` combined with default `binWidth=25` gives approximately 8-12 effective bins for texture features, which is standard for radiomics.
- Original notebooks (without `_normalised` suffix) are preserved intact for reproducibility.
