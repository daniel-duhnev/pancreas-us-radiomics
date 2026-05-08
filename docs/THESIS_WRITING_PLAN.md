# Thesis Writing Plan

## Context

Analysis notebooks 12-17b are complete. Notebooks 18-23 are planned (independent dataset, paired analysis, extended analysis — see `PLAN_THESIS_ROADMAP.md`). The thesis is for the EMAI program (Erasmus Mundus Master in AI) at UPF, supervised by Gemma Piella. Gemma said (May 6 meeting): start writing NOW, don't wait for all results. Thesis is 30 credits, needs ~40-50 pages.

**Decisions made:**
- Format: LaTeX (using EMAI 2026 template)
- Writing approach: Claude writes full draft sections for review
- Deadline: mid June 2026 submission (moved up from July)

The thesis tells a clear story: we tested whether radiomics texture features from grayscale ultrasound predict pancreas transplant rejection (they don't), and we replicated clinical biomarker results from Bassaganyas et al. 2025 (ARFI/perfusion features do predict rejection). The negative radiomics result combined with the positive clinical replication is itself the contribution.

---

## Step 1: Set Up LaTeX Project

Unzip `thesis-documents-and-templates/Template_TFM_Latex_EMAI_2026.zip` into a new `thesis/` directory.

- Update `MasterThesis.tex` with: title, author, supervisor (Gemma Piella), submit date (July 2026), partner university (UPF)
- Add packages: `booktabs`, `subcaption`, `multirow`, `siunitx`
- Create `Figures/` directory, copy existing assets (correlation heatmap, example US images)
- Start `bibliography.bib` with core references (Bassaganyas 2025, PyRadiomics, IBSI standard)
- Compile to verify: `pdflatex` -> `bibtex` -> `pdflatex` x2

---

## Step 2: Write Methods Chapter (First -- Most Stable)

The entire methods chapter is ready to write. The pipeline is complete and won't change.

### Section 3.1: Dataset (~2 pages)
- Study population: 56 patients, Hospital Clinic Barcelona, Oct 2016 - Feb 2020
- 138 initial studies, 137 with radiomics. Class split: 98 normal, 39 rejection
- Imaging protocol: Siemens Acuson S3000, grayscale US + ARFI + DCE-US
- Outcome definition: biopsy or clinical criteria
- Data structure: repeated measures (55 patients -> 137 studies, mean 2.5 per patient)
- **Table 1**: Dataset summary (demographics, class balance)
- **Figure 1**: Example images (raw DICOM, preprocessed, mask, segmented ROI)

### Section 3.2: Image Preprocessing (~2 pages)
- Contour detection and removal (white pixel threshold, morphological operations)
- Mask erosion (kernel 3, 1 iteration) to remove boundary artifacts
- Edge case handling (studies 03_01 and 43_01)
- **Figure 2**: Pipeline flowchart diagram (new to create)

### Section 3.3: Radiomics Feature Extraction (~1.5 pages)
- PyRadiomics config: force2D, binWidth=25, int16 cast
- 6 feature classes enabled, shape disabled
- Single `.execute()` call per image
- **Table 2**: Feature classes (name, count, what each captures)

### Section 3.4: Statistical Analysis (~1.5 pages)
- Normality check (Shapiro-Wilk) -> Welch's t-test or Mann-Whitney U
- Effect sizes: Cohen's d / rank-biserial correlation
- FDR correction (Benjamini-Hochberg) for radiomics
- Stratification: motivo-based AND days-based (>90 days)

### Section 3.5: ML Classification (~2-3 pages)
- Correlation removal (|r|>0.9, p-value-guided selection): 93 → 32 features
- Joint optimization: Pipeline (StandardScaler → SelectKBest → model) with GridSearchCV
- 4 models: LogReg, RF, SVM, NaiveBayes (all with class_weight="balanced" where applicable)
- Full dataset (137 studies): LOOCV evaluation
- Independent dataset (~55 studies): 10-fold stratified CV (Gemma's recommendation)
- Metrics: AUC, sensitivity, specificity via Youden's index

---

## Step 3: Write Introduction (~8-10 pages)

### Section 2.1: Problem Statement (~2-3 pages)
- Pancreas transplant rejection rates, diagnostic challenge
- Biopsy limitations (invasive, complications)
- Ultrasound as first-line imaging, ARFI/DCE-US emerging
- The gap: can automated texture analysis (radiomics) complement or replace manual measurements?

### Section 2.2: State of the Art (~4-5 pages)
- 2.2.1: Pancreas transplant rejection monitoring (clinical context)
- 2.2.2: Ultrasound imaging of pancreas grafts (grayscale US, ARFI, DCE-US)
- 2.2.3: Radiomics in medical imaging (definition, feature classes, PyRadiomics, applications)
- 2.2.4: ML for medical image classification (small datasets, CV, class imbalance)

**Note:** This section requires the most literature reading. Reference Bassaganyas 2025 citations heavily.

### Section 2.3: Objectives (~0.5 page)
5 specific objectives:
1. Extract radiomics features from pancreas transplant US images
2. Test whether radiomics features discriminate rejection vs no-rejection
3. Build ML classifiers and evaluate predictive performance
4. Replicate clinical imaging analysis of Bassaganyas et al. 2025
5. Compare automated radiomics vs manual clinical biomarkers

### Section 2.4: Report Structure (~0.5 page)

---

## Step 4: Write Results (~6-8 pages)

### Section 4.1: Feature Extraction (0.5 page)
- 93 features from 137 studies, no failures, 300 correlated pairs
- **Figure 4**: Correlation heatmap (exists: `reports/14a_correlation_heatmap_radiomics.png`)

### Section 4.2: Radiomics Statistical Analysis (~1.5 pages)
- Full dataset: 0/93 significant. Closest: firstorder_Minimum p=0.055
- Early/late subsets: still 0 significant
- **Table 3**: Top 10 features by p-value
- **Figure 5**: Box plot of firstorder_Minimum by group (to generate)

### Section 4.3: Clinical Feature Replication (~2-3 pages)
- Full dataset: 2 significant (ARFI mediana/media)
- Late >90 days: 8 significant. ARFI p<0.0001
- Replication matches Clara to 3 decimal places (14/15 features)
- **Table 4**: Clinical results full dataset
- **Table 5**: Clinical results late period
- **Table 6**: Replication comparison (our p-values vs Clara's)
- **Figure 6**: ARFI box plots by rejection status (to generate)

### Section 4.4: ML Classification (~2-3 pages)
- **Table 7**: Joint optimization results — full dataset (137 studies, LOOCV)
- **Table 8**: Joint optimization results — independent dataset (~55 studies, 10-fold CV)
- All AUC ~0.5, models are guessing on both datasets
- ROC curves for all models
- **Table 9**: Paired analysis results (14 patients, Wilcoxon signed-rank)

### Section 4.5: Extended Analysis (~2 pages)
- Alternative texture features (LBP, Gabor, Laws'): stats + ML results
- Surrounding tissue normalization: stats + ML results
- If no signal: rules out "wrong features" and "wrong normalization" concerns

---

## Step 5: Write Discussion & Conclusion (~5-7 pages)

### Section 5.1: Discussion (~3-4 pages)
- 5.1.1: Radiomics negative result -- why (grayscale US lacks stiffness/perfusion info, small sample, single config)
- 5.1.2: Clinical biomarkers work -- ARFI captures rejection-induced fibrosis and stiffness
- 5.1.3: Replication validates methodology -- p-values match to 3 decimals
- 5.1.4: Implications -- targeted biomarkers outperform generic texture analysis

### Section 5.2: Limitations (~1.5 pages)
1. Repeated measures / non-independence (55 patients -> 137 studies)
2. Small sample size (137 studies, 39 rejection)
3. No FDR correction in clinical analysis (14b)
4. Single PyRadiomics configuration
5. ML used only radiomics, not combined with clinical features
6. Motivo as unreliable time proxy (13 misclassified studies)
7. Single-center, single-scanner

### Section 5.3: Future Steps (~0.5-1 page)
1. Repeated measures sensitivity analysis (mixed-effects models, one-per-patient)
2. Combined radiomics + clinical ML model
3. Alternative PyRadiomics settings (binWidth, wavelet filters)
4. Deep learning on raw images
5. Larger multicenter studies

### Section 5.4: Conclusions (~0.5 page)
Radiomics doesn't predict rejection. Clinical biomarkers (ARFI) do. This narrows the search space for future non-invasive monitoring approaches.

---

## Step 6: Abstract, Appendix, Final Polish

- **Abstract** (200-600 words): draft now, finalize last
- **Keywords**: Pancreas transplantation; Graft rejection; Radiomics; Ultrasound; Machine learning
- **Appendix A**: Complete 93-feature table with p-values
- **Appendix B**: Full clinical results across all subsets
- **Appendix C**: PyRadiomics configuration

---

## Figures to Generate

New figures needed (from notebook data):
1. Preprocessing pipeline flowchart/diagram
2. Mask erosion before/after comparison
3. Box plot: firstorder_Minimum by rejection status
4. Box plots: ARFI values by rejection status (late period)
5. Box plots: DCE-US perfusion by rejection status
6. Replication scatter plot (our p-values vs Clara's)
7. ROC curves for ML classifiers (regenerate NB 15)
8. Patient flow diagram (study inclusion/exclusion)

---

## Timeline (updated May 2026)

| Period | Focus | Deliverable |
|--------|-------|-------------|
| **May 6-12** | Data prep + independent dataset | NB 18, integrate new images |
| **May 12-19** | Core independent results + start writing | NB 19, 20, 21. Thesis: Intro + Methods |
| **May 19-26** | Extended analysis + writing | NB 22, 23. Thesis: Background + Dataset |
| **May 26-Jun 1** | Results writing | Thesis: Results with all tables/figures |
| **Jun 1-8** | Discussion + review | Thesis: Discussion + Conclusion. Send to Gemma |
| **Jun 8-15** | Final revisions + submit | Final thesis |

Key dates:
- Thesis submission: mid June 2026
- Thesis defence: mid July 2026
- Graduation: August 31, 2026

---

## Page Budget (target: ~40 pages)

| Section | Pages |
|---------|-------|
| Abstract + front matter | 3 |
| Introduction | 8-10 |
| Methods | 8-12 |
| Results | 6-8 |
| Discussion + Conclusion | 5-7 |
| Bibliography | 2-3 |
| **Total body** | **~35-40** |
| Appendices (may not count) | 3-5 |

---

## Writing Tips

- **The negative result IS the thesis.** Don't apologize for it. Frame it: radiomics doesn't work, clinical biomarkers do, this is informative.
- **The replication is a strength.** Matching Bassaganyas to 3 decimals proves the pipeline is correct and the negative result isn't a bug.
- **Aim for 40 pages.** The template warns longer is not better.
- **Figures carry 15% of the grade.** Make them publication-quality with proper labels and informative captions.
- **Tables: use booktabs style.** No vertical lines. `\toprule`, `\midrule`, `\bottomrule`.
- **Each paragraph = one point.** Claim, evidence, implication.
- **Don't pad.** If under 30 pages, expand State of the Art or add figures, not redundant text.
- **Appendix is overflow.** Long tables (all 93 features) go there, not in the main text.

---

## Key Source Files

| File | What it provides |
|------|------------------|
| `docs/PLAN_THESIS_ROADMAP.md` | Master plan for all remaining work |
| `docs/PROJECT_CONTEXT.md` | Dataset description, research context |
| `docs/PREPROCESSING_PIPELINE.md` | Image preprocessing details |
| `docs/PLAN_NON_INDEPENDENT_DATA_AND_PAIRED_ANALYSIS.md` | Repeated measures approaches |
| `reports/13_merged_radiomics_clinical.csv` | Current 137-study merged dataset |
| `reports/14a_stats_radiomics_features.csv` | All radiomics p-values and effect sizes |
| `reports/14b_stats_clinical_features.csv` | All clinical p-values and effect sizes |
| `reports/17b_joint_optimization_results.csv` | Joint optimization ML results |
| `reports/14b_comparison_our_results_vs_bassaganyas2025.pdf` | Replication comparison report |
| Clara's paper (in repo root) | Reference methodology and results to replicate |
