# Plan: Thesis Roadmap — Independent Dataset, Paired Analysis, Extended Experiments, Writing

## Context

Gemma's feedback (May 6 meeting): the thesis is 30 credits and needs ~40-50 pages. Current work is too small — need independent dataset results, paired analysis, extended analysis, and to start writing immediately. Deadline: mid June 2026 submission (~6 weeks from May 6).

**What's done:**
- Notebooks 01-15: preprocessing, radiomics extraction, stats, baseline ML (all complete)
- NB 17 (sequential ML experiments): AUC ~0.5, no signal (complete)
- NB 17b (joint optimization ML): AUC ~0.53 best, confirms no signal (complete)
- 3 new DICOMs received from Carlos (34_02, 40_02, 41_03) at `data/Páncreas restantes (22-04-2026)/`

**What's needed:**
1. Integrate 3 new images (134 → 137 studies)
2. Build independent dataset (1 per patient, ~55-56 studies)
3. Repeat stats + ML on independent dataset
4. Paired analysis (14 patients with both outcomes)
5. Extended analysis (surrounding tissue, alternative features) for 30-credit depth
6. Start writing thesis NOW

---

## Phase 1: Data Preparation (May 6-9)

### Step 1.1: Integrate 3 new images
Follow `docs/PLAN_INTEGRATE_NEW_IMAGES.md`:
1. Copy 34_02, 40_02, 41_03 from `data/Páncreas restantes (22-04-2026)/` to `data/PANCREAS_2/PANCREAS_2/`
2. Run NB 06b (segmentation) on 3 new studies only
3. Run NB 09 (erosion) on 3 new studies
4. Run NB 12 (radiomics extraction) on 3 new studies
5. Re-run NB 13 (merge): 134 → 137 rows

**Effort:** ~2 hours if pipeline runs cleanly.

### Step 1.2: Build independent dataset — `analysis/18_build_independent_dataset.ipynb`
Selection rule (from Gemma's meetings):
- 1 study per patient
- If patient has only one outcome: pick the first study by date (study_id order)
- If patient has both rejection and no-rejection: pick the first rejection study

**Expected result:** ~55-56 studies (21 rejection, 34-35 no-rejection, ~38% rejection rate)

Save to `reports/18_independent_dataset.csv` — same columns as 13_merged but filtered.

**Effort:** ~1 hour. Simple filtering logic.

---

## Phase 2: Core Results on Independent Dataset (May 9-16)

### Step 2.1: Statistical tests — `analysis/19_stats_independent_dataset.ipynb`
Repeat the NB 14a analysis on the independent dataset:
- Mann-Whitney U test on all 93 features (or 31 post-correlation)
- Benjamini-Hochberg FDR correction
- Compare to the 137-study results
- Correlation heatmap

Pattern: reuse NB 14a structure, swap data source to `18_independent_dataset.csv`.

**Effort:** ~2 hours.

### Step 2.2: ML joint optimization — `analysis/20_ml_independent_dataset.ipynb`
Repeat the NB 17b approach on the independent dataset:
- Pipeline: StandardScaler → SelectKBest → model
- 4 models: LogReg, RF, SVM, NB
- Joint grid search over features (k) + hyperparameters
- **Use 10-fold stratified CV** (Gemma's suggestion for small dataset)
- Also run LOOCV as a comparison point
- ROC curves, Youden threshold, summary table

Pattern: reuse NB 17b structure, swap data source, change CV to 10-fold.

**Effort:** ~2-3 hours.

### Step 2.3: Paired analysis — `analysis/21_paired_analysis.ipynb`
14 patients have both rejection and no-rejection studies.
- For each patient: select one rejection study and one no-rejection study
- Compute within-patient feature differences (rejection - no-rejection)
- Wilcoxon signed-rank test on each feature's differences
- Also test ARFI and clinical features if available in paired data
- Report: which features (if any) show significant within-patient changes

Gemma said this should be straightforward — just a few lines of code after extracting the data.

**Effort:** ~2-3 hours.

---

## Phase 3: Start Thesis Writing (May 12-ongoing, parallel with Phase 2)

Gemma explicitly said: start writing NOW, don't wait until experiments are done.

Sections to draft first (can write before all results are in):
1. **Introduction** — pancreas transplant rejection, ultrasound monitoring, radiomics motivation
2. **Background/Related Work** — literature review of 4 papers Gemma sent + radiomics in US
3. **Methods** — dataset description, preprocessing pipeline, feature extraction, statistical tests, ML approach
4. **Dataset** — 137 studies, 56 patients, clinical variables, class distribution

Sections to write after results:
5. **Results** — stats tables, ML tables, ROC curves, paired analysis
6. **Discussion** — interpret negative result, comparison to literature, limitations
7. **Conclusion**

**Thesis format:** LaTeX. Need to set up template (UPF thesis template or standard).

**Effort:** Ongoing. Aim for 5-10 pages per week. Start with Methods (most mechanical, can write now).

---

## Phase 4: Extended Analysis (May 19-30)

These add depth and pages for the 30-credit requirement. Detailed implementation specs are in `docs/legacy/PLAN_EXPERIMENTS_SURROUNDING_TISSUE_AND_ALT_FEATURES.md` (code snippets for all extraction functions).

### Step 4.1: Alternative texture features — `analysis/22_alternative_texture_features.ipynb`
Extract non-PyRadiomics features:
- LBP (Local Binary Patterns): 3 radius configs (R=1,2,3) → ~54 features
- Gabor filters: 3 freq × 6 orientations × 3 stats → ~54 features
- Laws' kernels: 15 pairs × 3 stats → ~45 features
Total: ~153 new features per image

Run stats + ML on these. If they also show no signal, it rules out "wrong features" as a concern.

**Effort:** 3-4 hours. **Priority:** High — adds a full new experiment chapter.

### Step 4.2: Surrounding tissue normalization — `analysis/23_surrounding_tissue_analysis.ipynb`
- Create surrounding tissue mask (dilate pancreas mask by 5/10/15 pixels)
- Z-score normalize image by surrounding tissue stats
- Re-extract radiomics on normalized images
- Compute contrast features (pancreas vs surrounding): ~11 features per dilation

**Effort:** 4-6 hours. **Priority:** Medium — novel approach, adds depth.

### Step 4.3: Repeat extended analyses on independent dataset
If Steps 4.1/4.2 produce interesting features, repeat the ML pipeline on the independent dataset.

---

## Phase 5: Complete Thesis (June 1-15)

- Write Results and Discussion sections
- Create final publication-quality figures
- Compile all summary tables
- Proofread and format
- Submit to Gemma for review (aim: June 8)
- Final revisions and submission (June 15)

---

## Notebook numbering summary

| NB | Name | Status |
|---|---|---|
| 01-13 | Preprocessing through merge | Complete |
| 14a/14b | Stats (137 studies) | Complete |
| 15 | Baseline ML | Complete |
| 17 | Sequential ML experiments (137 studies) | Complete |
| 17b | Joint optimization ML (137 studies) | Complete |
| 18 | Build independent dataset | Complete |
| 19 | Stats on independent dataset | Complete |
| 20 | ML on independent dataset (10-fold CV) | Complete |
| **21** | **Paired analysis (14 patients)** | **To create** |
| **22** | **Alternative texture features** | **To create** |
| **23** | **Surrounding tissue analysis** | **To create** |

---

## Weekly timeline

| Week | Dates | Focus | Deliverables |
|---|---|---|---|
| 1 | May 6-12 | Data prep + independent dataset | NB 18, integrate new images, start NB 19-20 |
| 2 | May 12-19 | Core independent results + start writing | NB 19, 20, 21 complete. Thesis: Intro + Methods drafted |
| 3 | May 19-26 | Extended analysis + writing | NB 22, 23. Thesis: Background + Dataset sections |
| 4 | May 26-Jun 1 | Results writing + polish experiments | Thesis: Results section with all tables/figures |
| 5 | Jun 1-8 | Discussion + review | Thesis: Discussion + Conclusion. Send to Gemma |
| 6 | Jun 8-15 | Final revisions + submit | Incorporate Gemma's feedback. Submit |

---

## Key data numbers

- Full dataset: 137 studies (after new images), ~56 patients
- Independent dataset: ~55-56 studies (21 rej, 34-35 no-rej)
- Paired subset: 14 patients with both outcomes
- Features: 93 original → 32 after correlation removal
- Current best AUC (full dataset, joint opt): 0.537 (SVM/NaiveBayes tied)

## Files referenced

- `docs/PLAN_INTEGRATE_NEW_IMAGES.md` — integration steps for 3 new images
- `docs/PLAN_NON_INDEPENDENT_DATA_AND_PAIRED_ANALYSIS.md` — 7 approaches for non-independence
- `docs/legacy/PLAN_EXPERIMENTS_SURROUNDING_TISSUE_AND_ALT_FEATURES.md` — detailed code for Categories 3-4 (LBP, Gabor, Laws', surrounding tissue)
- `reports/13_merged_radiomics_clinical.csv` — current 137-study dataset
- `data/Páncreas restantes (22-04-2026)/` — 3 new DICOMs from Carlos
