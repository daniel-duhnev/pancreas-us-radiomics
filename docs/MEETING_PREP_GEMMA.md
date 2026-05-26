# Meeting Prep - Gemma (Wednesday 1:30pm)

## Meeting agenda

### 1. Image normalisation update (5 min)

Show her that it's done. Key points:
- PyRadiomics built-in normalisation: per-image z-score, scale=100, 3 sigma outlier clipping
- Re-ran ALL experiments (8 normalised notebooks)
- Results unchanged: 0 features survive FDR, ML at chance (best AUC 0.636, CI includes 0.5)
- Normalised results are now primary in the thesis

If she wants to see the code:
- NB `12_extract_radiomics_all_images_normalised.ipynb`, cell 3 (settings dict)
- NB `14a_stats_radiomics_features_normalised.ipynb`, cell 8 (test results)

### 2. Feature standardisation clarification (2 min)

Show her the pipeline code:
- NB `17b_ml_joint_optimization_normalised.ipynb`, cell 5 (pipeline definition)
- The StandardScaler is INSIDE the Pipeline, fitted per-fold
- Location in thesis: Methods Section 2.5.2, line 181

### 3. DICOM/RGB clarification (2 min)

If she asks again:
- NB `03_dataset_audit.ipynb`, cell 4 output: "Channels: 3 (RGB) for all 134 images"
- NB `06b_segment_all_images_contour_subtracted.ipynb`, cell with `pydicom.dcmread()`
- Bassaganyas paper page 3: "The videos were stored and later exported in DICOM format"
- The ultrasound exports B-mode frames as RGB DICOM (standard for Siemens systems)

### 4. Independence / full-dataset issue - DISCUSSION (10-15 min)

This is the biggest topic. Our proposal:
- Move full-dataset stats + ML to appendix (with caveat about non-independence)
- Independent dataset (55 studies, 1 per patient) becomes primary
- Ask her: is appendix acceptable, or should it be removed entirely?

Questions to ask Gemma:
- Is she OK with the full-dataset results in an appendix as "exploratory"?
- For the clinical replication: we need to match Bassaganyas methodology (they used all studies). Can we keep this as pipeline validation with a caveat? Or does she want us to also run clinical stats on independent patients?
- Stratification (early/late): should we redo this on the independent dataset? The subgroups would be small (~20-30). Worth doing or skip?

Key code if she asks:
- NB `18_build_independent_dataset_normalised.ipynb` - how we select 1 study per patient
- NB `19_stats_independent_dataset_normalised.ipynb` - stats on independent data
- NB `20_ml_independent_dataset_normalised.ipynb` - ML on independent data (10-fold CV, 1 patient per fold since 1 study per patient)

### 5. ANOVA F-statistic in SelectKBest (5 min)

Our defence:
- Used as a RANKING function, not for hypothesis testing
- Only the relative F-scores matter (which features have most between-group variance)
- P-values from f_classif are not used for any significance claims
- StandardScaler runs before SelectKBest so scale is normalised
- Alternative: mutual_info_classif (nonparametric) - could mention we considered it

Code: NB `17b_ml_joint_optimization_normalised.ipynb`, cell 5:
```python
Pipeline([
    ("scaler", StandardScaler()),
    ("select", SelectKBest(f_classif)),
    ("model", model)
])
```

### 6. Motivo stratification (5 min)

Explain clearly:
- We split the dataset by TIME PERIOD (early vs late)
- Within each stratum, compare rejection vs no-rejection
- We are NOT comparing the same patient at two time points
- The days-based cutoff (>90 days) matches Bassaganyas exactly
- The motivo-based grouping was a secondary check (same direction, slightly different n)

Ask Gemma: keep both stratifications, keep only days-based, or remove entirely?

### 7. Quick fixes already made (2 min)

Mention briefly:
- "Clinical imaging analysis" changed to "statistical analysis of clinical biomarkers"
- Abbreviations: removed double definitions
- Shape features: reworded justification
- "Ensures" softened
- FDR wording fixed
- Welch's t-test: added explanation that it handles unequal variances by design
- Added "image preprocessing" to radiomics workflow
- Will add references for US radiomics in liver/thyroid/breast (in progress)

### 8. Wavelet/LoG filters (2 min)

Acknowledge:
- We did NOT implement wavelet/LoG image filtering (time constraint)
- Listed as limitation and future work in discussion
- What we DID test: alternative feature families (LBP, Gabor, Laws') - also negative
- These are different from what she suggested but complement the story

---

## Key files to have open during meeting

| What | File/notebook | Cell |
|------|---------------|------|
| PyRadiomics normalisation settings | `12_extract...normalised.ipynb` | Cell 3 |
| ML pipeline with StandardScaler | `17b_ml_joint...normalised.ipynb` | Cell 5 |
| LOOCV implementation | `17b_ml_joint...normalised.ipynb` | Cell 3 + 7 |
| Independent dataset construction | `18_build...normalised.ipynb` | Cell 3-4 |
| Stats on independent dataset | `19_stats...normalised.ipynb` | Cell 6 + 8 |
| ML on independent dataset (10-fold) | `20_ml...normalised.ipynb` | Cell 7 |
| Dataset audit (DICOM/RGB proof) | `03_dataset_audit.ipynb` | Cell 4 output |
| Thesis PDF | `thesis/MasterThesis.pdf` | Sections 2.3, 2.5, 3.2 |

---

## Potential difficult questions and answers

**"Why didn't you do patient-level splits on the full dataset?"**
- You're right, we should have used GroupKFold with patient IDs. We didn't initially but the independent dataset (1 per patient) eliminates this issue entirely. The full-dataset ML is now in the appendix as exploratory.

**"How many features survive after you do everything correctly (independent dataset, FDR)?"**
- Zero. 24 reach uncorrected p<0.05 but all have FDR-adjusted p >= 0.16.

**"Is the ML result meaningful at AUC 0.636?"**
- No. The 95% CI is [0.48, 0.78] which includes 0.5 (chance). With N=55, we cannot distinguish this from random.

**"Why not try wavelet/LoG?"**
- Time constraint. The thesis deadline is mid-June. We tested 3 alternative feature families (153 features total) which were also negative. Wavelet/LoG is noted as future work.

**"The paired analysis shows ARFI loses significance - what does that mean?"**
- It suggests ARFI may measure between-patient differences (inherent stiffness) rather than within-patient rejection-induced changes. Only 14 pairs though - underpowered. Hypothesis-generating, not definitive. Discuss whether this belongs in main text or should be flagged more prominently.
