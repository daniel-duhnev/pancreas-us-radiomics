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

**What SelectKBest does:** Before training, pick the top `k` most discriminative features. It ranks all 27 features by how well each one separates the two classes, then keeps only the best `k`.

**What the F-statistic is:** For each feature: `F = (between-group variance) / (within-group variance)`. High F = the rejection and non-rejection groups are well separated on that feature. It's a one-way ANOVA on each feature individually.

**ANOVA formally assumes:** normality, equal variances, independence.

**Our defence:**
- Used as a RANKING function, not for hypothesis testing
- Only the relative F-scores matter (which features have most between-group variance)
- P-values from f_classif are not used for any significance claims — we never say "feature X is significant based on SelectKBest"
- The ranking is robust: if feature A separates groups better than feature B, that holds even if the data isn't perfectly normal
- StandardScaler runs before SelectKBest so scale is normalised
- Alternative: mutual_info_classif (nonparametric) — could mention we considered it

Code: NB `17b_ml_joint_optimization_normalised.ipynb`, cell 5:
```python
Pipeline([
    ("scaler", StandardScaler()),
    ("select", SelectKBest(f_classif)),
    ("model", model)
])
```

If she pushes: "Would you prefer mutual_info_classif? We can swap it — one line of code. But the ML result is at chance regardless, so feature selection method doesn't change the conclusion."

### 5b. Patient-level splits / data leakage (5 min)

**Gemma's point:** "If you include all 137 images, the split in training and testing should be done at patient level, not at image level."

**She's right.** This is the ML-side of the independence problem (point 10 is the stats-side).

**What happened in NB 17b (full dataset):**
- LOOCV leaves out one STUDY, not one PATIENT
- 42 of 55 patients have 2-6 studies each
- When testing on study A1, studies A2, A3, A4 from the same patient are in the training set
- The model can "recognise" Patient A from training, not learn what rejection looks like
- This is data leakage (same patient in both train and test)

**Patient distribution:**
- 13 patients: 1 study (no leakage possible)
- 14 patients: 2 studies
- 20 patients: 3 studies
- 5 patients: 4 studies
- 2 patients: 5 studies, 1 patient: 6 studies

**Correct approach would be:** `GroupKFold(groups=patient_id)` — ensures all of a patient's studies go to the same fold.

**What we actually did (NB 20 — independent dataset):**
- 55 studies, exactly 1 per patient
- LOOCV here = leave one patient out (no leakage by construction)
- 10-fold CV also clean — no patient can appear in both train and test
- This is the methodologically correct ML evaluation

**Key point for Gemma:** The flaw only affects NB 17b (full-dataset ML), which we're moving to appendix anyway. The primary result (NB 20) is clean. And interestingly, the full-dataset AUC is LOWER (0.53) than independent (0.64) — so the leakage didn't even help. Both are at chance level.

**Proposal:** Move full-dataset ML to appendix with caveat. Independent dataset ML is primary.

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
