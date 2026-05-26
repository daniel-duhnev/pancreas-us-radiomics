# Plan: Address Gemma's 17 Feedback Points on Thesis Draft

## Context

Gemma reviewed the thesis draft (the older version before image normalisation) and provided 17 feedback points. Some require text changes, some require structural reorganisation of the Results chapter, and some can be defended or are already addressed in the updated version she hasn't seen yet.

---

## Point-by-Point Analysis and Actions

### Point 1: "Clinical imaging analysis" wording
**Gemma's point:** We say "replicates the clinical imaging analysis" but we didn't extract features from images - we took pre-recorded measurements and ran stats.
**Verdict:** She's correct. We took tabular ARFI/DCE-US values from the clinical spreadsheet and ran Mann-Whitney tests on them. Bassaganyas et al. performed the actual imaging measurements. We reproduced their statistical analysis on the same data.
**Action:** Change wording in introduction (line 17) and objective 4 (line 68) from "replicates the clinical imaging analysis" to "reproduces the statistical analysis of the clinical imaging biomarkers reported by". Similar change needed in abstract and discussion.
**Files:** `introduction.tex` (lines 17, 68), `abstract.tex`, `discussion.tex`

---

### Point 2: Abbreviation definitions
**Gemma's point:** Define abbreviations once (first use) and then use them consistently. Don't redefine. Don't define TIC if barely used.
**Findings:**
- ARFI defined in introduction (line 11) AND methods (line 8) - remove second definition
- DCE-US defined in introduction (line 11) AND methods (line 8) - remove second definition
- TIC defined in introduction (line 33) - used only 2 more times. Consider spelling out or just dropping the abbreviation.
- Other abbreviations to check: IBSI, GLCM, GLRLM, GLSZM, GLDM, NGTDM, FDR, LOOCV, AUC, LBP, ROC
**Action:** Remove re-definitions in methods.tex line 8. Replace with just "ARFI" and "DCE-US" (already defined). Check TIC usage - if only used a few times, remove abbreviation.
**Files:** `methods.tex` (line 8), `introduction.tex` (check TIC)

---

### Point 3: Radiomics workflow - mention image preprocessing
**Gemma's point:** The radiomics workflow description on "page 5" (introduction line 39) doesn't mention image preprocessing.
**Current text:** "The radiomics workflow typically involves image acquisition, region-of-interest segmentation, feature extraction, feature selection, and statistical or machine learning analysis."
**Verdict:** She's right. Image preprocessing (normalisation, noise reduction, etc.) is a standard step between segmentation and feature extraction that should be mentioned.
**Action:** Add "image preprocessing" to the workflow list: "...region-of-interest segmentation, image preprocessing, feature extraction..."
**Files:** `introduction.tex` (line 39)

---

### Point 4: Missing references for radiomics in other domains
**Gemma's point:** First paragraph of "page 6" (introduction line 43) mentions radiomics applied to liver fibrosis, thyroid, breast - no references given.
**Current text:** "Nevertheless, several studies have applied radiomics to ultrasound for liver fibrosis staging, thyroid nodule classification, and breast lesion characterisation, with variable success depending on the degree of acquisition standardisation."
**Verdict:** She's right. This is an unbacked claim. Needs citations.
**Action:** DONE. Added three verified references:
1. Wang et al. (2019) *Gut* 68(4):729-741. DOI: 10.1136/gutjnl-2018-316204. Liver fibrosis, shear wave elastography radiomics, multicentre.
2. Park et al. (2021) *European Radiology* 31(4):2405-2413. DOI: 10.1007/s00330-020-07365-9. Thyroid nodules, US radiomics + TIRADS.
3. Romeo et al. (2021) *European Radiology* 31(12):9511-9519. DOI: 10.1007/s00330-021-08009-2. Breast lesions, multicenter US radiomics.

BibTeX keys: `wang2019liver`, `park2021thyroid`, `romeo2021breast`
**Files:** `introduction.tex` (line 43), `bibliography.bib` -- COMPLETED

---

### Point 5: Objective 2 should mention ML too
**Gemma's point:** Objective 2 says "Conduct statistical hypothesis testing" but this should also cover ML, not just stats.
**Current text (line 64):** "Test whether radiomics features discriminate rejection from no rejection. Conduct statistical hypothesis testing on each extracted feature to determine whether any individual texture or intensity measure differs significantly between the two outcome groups."
**Verdict:** She has a point. The bold title says "discriminate" (which is broader) but the description only mentions statistical testing. ML classification (objective 3) is separate, but the discrimination question is answered by BOTH. The description could acknowledge this.
**Action:** Modify to: "Conduct statistical hypothesis testing and machine learning classification to determine whether individual or combined texture features differ significantly between the two outcome groups."
**OR** leave objective 2 as stats-only and note that objective 3 extends this with multivariate ML. Either is defensible - but simplest fix is to rephrase the bold title: "Test whether individual radiomics features discriminate rejection from no rejection" to make it explicitly about individual features (stats), with objective 3 covering combinations (ML).
**Files:** `introduction.tex` (line 64)

---

### Point 6: Objective 4 - same as point 1
**Gemma's point:** Same issue as point 1 - "Replicate the clinical imaging analysis" is misleading.
**Current text (line 68):** "Replicate the clinical imaging analysis of Bassaganyas et al. Apply the same statistical methodology to the clinical imaging features..."
**Verdict:** Correct. We should say "Reproduce the statistical analysis of the clinical biomarkers reported by Bassaganyas et al."
**Action:** Reword objective 4 title and description.
**Files:** `introduction.tex` (line 68)

---

### Point 7: DICOM and RGB - do we really have DICOMs? Are they RGB?
**Gemma's point:** "you talk about DICOM but you did not have DICOMs but png... Do you really have RGB?"
**Findings from code:**
- Notebook 03 audit: ALL 134 files (now 137) are DICOM format (pydicom reads them successfully, Modality=US)
- SamplesPerPixel = 3 for ALL images (confirmed RGB)
- The preprocessing pipeline loads DICOMs with pydicom, detects RGB channels, uses all 3 channels for white pixel detection, then converts to grayscale
**Verdict:** We DO have DICOMs and they ARE RGB. The Bassaganyas paper also confirms: "The videos were stored and later exported in DICOM format." Gemma may be confused about what format the images are in, or she may be thinking of a different dataset. We can politely clarify.
**Action:** Keep current wording (it's correct). In email response, explain that we verified: all files are .dcm DICOM files with SamplesPerPixel=3 (RGB), loaded with pydicom. The white contour detection uses RGB channels.
**Pushback (polite):** This is correct as written. The data files are DICOM (.dcm) and contain RGB ultrasound frames.

---

### Point 8: Explain normalisation before feature extraction
**Gemma's point:** Before feature extraction, explain about normalisation of images.
**Current state:** In the UPDATED thesis (which Gemma hasn't read), methods.tex line 115 now describes the PyRadiomics normalisation (z-score, scale=100, 3sigma clipping) immediately before feature computation in Section 2.3.
**Verdict:** Already addressed in current version. Gemma was reading the OLD draft.
**Action:** No change needed. Mention in email that this is now included.

---

### Point 9: Reason for disabling shape features
**Gemma's point:** The reason for not using shape is "in each image, the region of visible pancreas is different" - not because "ROI shapes are determined by the clinician's annotation."
**Current text (methods.tex line 115):** "Shape-based features were disabled, as ultrasound ROI shapes are determined by the clinician's annotation rather than by the underlying tissue morphology."
**Verdict:** Gemma's point is subtly different and more fundamental. The issue is:
1. The ultrasound imaging plane varies between examinations (different portions of the graft are visible)
2. The clinician then draws around whatever is visible
So shape reflects the imaging window AND the annotation, not graft morphology.
Our current wording focuses on the annotation aspect, but misses the deeper point: the visible region itself changes between exams.
**Action:** Reword to: "Shape-based features were disabled because the shape of the visible pancreas region varies between examinations depending on the ultrasound imaging plane and probe positioning, rather than reflecting the morphology of the graft itself."
**Files:** `methods.tex` (line 115)

---

### Point 10: MAJOR - Cannot do statistical tests on all 137 non-independent images
**Gemma's point:** The tests assume independence. You should NOT include the statistical test on all 137 images. Only apply tests to independent images (one per patient, ~55-56 studies).
**Verdict:** She's correct methodologically. Standard Mann-Whitney and t-tests assume independent observations. With multiple studies per patient, the effective sample size is inflated and p-values may be unreliable. The independent dataset (55 studies, 1 per patient) is the methodologically correct analysis.
**Implications for thesis:**
- The full-dataset univariate analysis (Section 3.2 "Full Dataset") should NOT be presented as primary
- The independent dataset analysis should become the PRIMARY statistical result
- The full-dataset result could be mentioned briefly as exploratory/supplementary, with explicit caveat about violated independence
- The stratified analysis (motivo-based, also on 137 studies) has the same problem
**Action:** Restructure Results Section 3.2:
- Make the independent dataset (currently §3.2.3) the PRIMARY subsection
- Demote or remove the full-dataset analysis (currently §3.2.1)
- Demote or remove the stratified analysis (currently §3.2.2) - or redo it on the independent dataset
- Update discussion, abstract, and conclusions accordingly
**This is the biggest structural change.**
**Files:** `results.tex` (Section 3.2), `discussion.tex`, `abstract.tex`, `methods.tex` (may need to reframe)

---

### Point 11: Which test for homogeneity of variances?
**Gemma's point:** You test normality and then use Welch's t-test when normal. Which test did you use to check homogeneity of variances?
**Findings from code:** We use `scipy.stats.ttest_ind(equal_var=False)` which IS Welch's t-test. Welch's t-test does NOT assume equal variances - that's the whole point of using Welch's over Student's t-test. We don't need to test for homogeneity of variances because Welch's test handles unequal variances by definition.
**Verdict:** We don't test for homogeneity because we always use Welch's (which doesn't assume it). But the thesis doesn't explain this clearly enough. Gemma may not have noticed the "(unequal variances)" qualifier.
**Action:** Make this explicit in the text. Change to something like: "If both groups passed the normality test (p > 0.05), Welch's t-test was used. Welch's t-test was chosen over Student's t-test because it does not assume homogeneity of variances, making a separate variance equality test unnecessary."
**Files:** `methods.tex` (line 149)

---

### Point 12: "ensures" is too strong
**Gemma's point:** "This adaptive approach ensures that parametric assumptions are not violated" - "ensure" is too strong.
**Current text (methods.tex line 149):** "This adaptive approach ensures that parametric assumptions are not violated while preserving statistical power when appropriate."
**Verdict:** She's right. The Shapiro-Wilk test is itself imperfect (it can fail to reject normality in small samples, or reject it for trivial deviations in large samples). The word "ensures" overstates what the procedure does.
**Action:** Replace with: "This adaptive approach aims to select an appropriate test for each feature based on its distributional characteristics."
**Files:** `methods.tex` (line 149)

---

### Point 13: "corrected significance threshold" is wrong terminology
**Gemma's point:** You correct the p-values, not the threshold. The threshold (alpha=0.05) itself is not corrected.
**Current text (methods.tex line 153):** "A corrected significance threshold of alpha=0.05 was used throughout."
**Verdict:** She's technically correct. We apply BH correction to the p-values, then compare the adjusted p-values to 0.05. The threshold is the same 0.05 - what changes are the p-values.
**Action:** Replace with: "Statistical significance was defined as FDR-adjusted p-values below 0.05."
**Files:** `methods.tex` (line 153)

---

### Point 14: Stratification by motivo - what exactly is being compared?
**Gemma's point:** Is stratification done for all patients or only those with rejection? When comparing two time points, you should use paired measures.
**Clarification:** We are NOT comparing early vs late within the same patient. We are:
1. Splitting the dataset into early (motivo 1-2) and late (motivo 3-5) subsets
2. Within each subset, comparing rejection vs no-rejection groups
So the comparison is still between-group (rej vs no-rej), just restricted to a time-based subset. We are not doing a paired comparison across time points.
**Verdict:** The confusion may stem from unclear writing. The text could be clearer about what's being compared (groups) vs what's being stratified (time period). However, given point 10 (independence violation), the stratified analysis on 137 studies may need to be removed or heavily caveated anyway.
**Action:** If we keep any stratified analysis, rewrite to make crystal clear: "The dataset was partitioned by post-transplant period, and the rejection vs no-rejection comparison was repeated within each time stratum." Consider doing this on the independent dataset instead.
**Files:** `methods.tex` (lines 155-160), `results.tex`

---

### Point 15: Same independence problem for clinical features (17 features on 138 studies)
**Gemma's point:** Same as point 10 but for the clinical feature analysis.
**Verdict:** Same issue. The clinical analysis on 138 studies violates independence.
**However:** This analysis is a REPLICATION of Bassaganyas et al., who used ALL studies (not per-patient). To replicate their methodology, we must use the same approach they did. The purpose is validation of our pipeline, not discovery.
**Action:** Keep the clinical replication as-is (matching Bassaganyas methodology), but add explicit caveat: "This analysis uses all available studies to replicate the methodology of Bassaganyas et al., who did not restrict to one study per patient. The resulting p-values should be interpreted with caution due to the non-independence of repeated measures within patients." Could additionally run clinical stats on independent dataset as a supplementary check.
**Pushback (partial):** The clinical analysis serves as a replication of published work using their exact methodology. Restricting to independent observations would make the comparison invalid.
**Files:** `results.tex` (section 3.3), possibly `methods.tex`

---

### Point 16: Why both motivo-based AND days-based stratification?
**Gemma's point:** "I do not fully understand why you do both."
**Explanation:** Bassaganyas et al. used a >90 days post-transplant cutoff. Our motivo variable is a categorical visit-type indicator, not a precise time measurement. To replicate their exact methodology, we use the days-based cutoff. The motivo-based grouping was done as an alternative to see if results are consistent. The days-based late subset matches Bassaganyas sample sizes exactly (52 ARFI, 50 DCE-US).
**Action:** Make the rationale clearer in the text: explain that the days-based stratification is used for replication purposes (matching Bassaganyas), and briefly note the motivo-based result as a consistency check. Consider removing the motivo-based result entirely if it adds confusion without adding value.
**Files:** `methods.tex` (lines 164-165), `results.tex` (line 172)

---

### Point 17: ANOVA F-statistic assumptions + patient-level splits
**Gemma's point (part A):** SelectKBest with ANOVA F-statistic - does it require ANOVA assumptions?
**Findings:** Yes, technically the F-statistic assumes normality, equal variances, and independence. However:
- In sklearn, f_classif is used for RANKING features (not hypothesis testing)
- The relative ranking is robust to assumption violations
- The actual p-values may be unreliable, but we only use the F-score to rank features, not to make significance claims
- The StandardScaler before SelectKBest ensures features are on comparable scales
**Action:** Add brief justification: "The ANOVA F-statistic was used as a univariate discriminative measure for feature ranking. While the F-test formally assumes normality and equal variances, these assumptions primarily affect p-value accuracy; the relative ranking of features by discriminative power is robust to moderate violations, and the F-statistic serves here as a selection heuristic rather than a hypothesis test."
Could also mention mutual_info_classif as an alternative that was considered.

**Gemma's point (part B):** "If you include all 137 images, the split in training and testing should be done at patient level, not at image level."
**Findings:** In NB 17b (full dataset, 137 studies), LOOCV leaves out one STUDY, not one PATIENT. A patient's other studies can be in training while one is in test. This is a form of data leakage.
In NB 20 (independent dataset, 55 studies), this is NOT an issue because each patient has exactly one study. 10-fold CV on the independent dataset is correct.
**Verdict:** This reinforces point 10. The full-dataset ML has a methodological flaw (no patient-level grouping). The independent-dataset ML is correct.
**Action:** Two options:
A) Simply drop full-dataset ML from main text (it's methodologically flawed)
B) Add explicit caveat about the patient-level leakage and present it as exploratory
The independent dataset ML is the correct primary ML result.
**Files:** `methods.tex` (evaluation strategy section), `results.tex` (section 3.4)

---

## Summary: What Needs to Change

### COMPLETED (text edits done, thesis compiles):
- Point 1 + 6: "clinical imaging analysis" -> "statistical analysis of clinical biomarkers" (intro, discussion) DONE
- Point 2: Removed ARFI/DCE-US re-definitions in methods; removed TIC abbreviation DONE
- Point 3: Added "image preprocessing" to radiomics workflow list DONE
- Point 4: Added 3 verified references (Wang 2019, Park 2021, Romeo 2021) DONE
- Point 5: Objective 2 title now says "individual radiomics features" DONE
- Point 8: Image normalisation already described in methods (no change needed) DONE
- Point 9: Shape features reworded to reference imaging plane variability DONE
- Point 11: Added Welch's t-test explanation (no variance test needed) DONE
- Point 12: "ensures" softened to "aims to select" DONE
- Point 13: FDR wording corrected ("FDR-adjusted p-values below 0.05") DONE
- Point 15 (partial): Added caveat to clinical replication explaining non-independence DONE
- Point 17A: Added F-statistic justification (ranking heuristic, not hypothesis test) DONE

### No change needed (defended in email):
- Point 7: DICOMs are confirmed RGB (evidence from notebook audit)
- Abstract: Already uses "clinical biomarker analysis" (not "clinical imaging analysis")

### REMAINING - requires Wednesday meeting discussion:
- Point 10: Move full-dataset stats/ML to appendix (or delete?)
- Point 14: Whether to redo stratification on independent dataset (small subgroups ~25-30)
- Point 15 (remainder): Whether to additionally run clinical stats on 55 independent patients (new analysis)
- Point 16: Keep both stratifications, keep only days-based, or remove motivo-based?
- Point 17B: Full-dataset ML to appendix (tied to point 10 decision)

---

## Execution Plan

### Phase 1: Literature search (Point 4) -- COMPLETED
Found and added Wang 2019 (liver), Park 2021 (thyroid), Romeo 2021 (breast). All verified via PubMed Central.

### Phase 2: Minor text edits (Points 1, 2, 3, 5, 6, 9, 11, 12, 13, 15 caveat, 17A) -- COMPLETED
All isolated wording changes done. Thesis compiles cleanly (75 pages, 0 errors).

### Phase 3: Major restructuring (Points 10, 14, 15 remainder, 16, 17B) -- BLOCKED on meeting

Waiting for Wednesday meeting with Gemma to confirm approach.

---

#### Current results.tex structure (for reference):

```
Section 3.1: Feature Extraction Summary
Section 3.2: Radiomics Statistical Analysis
  3.2.1: Full Dataset (137 studies) ← NON-INDEPENDENT, move to appendix
  3.2.2: Stratified Analysis (motivo-based, 137 studies) ← NON-INDEPENDENT, discuss
  3.2.3: Independent Dataset (55 patients) ← CORRECT, becomes primary
Section 3.3: Clinical Feature Replication
  3.3.1: Full Dataset (138 studies) ← replicates Bassaganyas, keep with caveat
  3.3.2: Late Post-Transplant Period ← days-based stratification, keep
  3.3.3: Replication of Bassaganyas et al. ← comparison table, keep
Section 3.4: Machine Learning Classification
  3.4.1: Full Dataset (LOOCV, 137 studies) ← NON-INDEPENDENT, move to appendix
  3.4.2: Independent Dataset (10-fold CV, 55 patients) ← CORRECT, becomes primary
Section 3.5: Paired Analysis (14 patients) ← keep as-is
Section 3.6: Alternative Texture Features ← keep as-is
Section 3.7: Surrounding Tissue Analysis ← keep as-is
```

Current appendix.tex has:
- Appendix A: Complete 93-feature table (independent dataset)
- Appendix B: PyRadiomics Configuration

---

#### Point 10 + 17B: Move full-dataset analysis to appendix

**Decision needed from Gemma:** Appendix (with caveat) or delete entirely?

**If appendix (most likely):**

Step 1: Create new appendix chapter in appendix.tex:
```latex
\chapter{Full-Dataset Exploratory Analysis}
\label{app:full_dataset}
The following results use all 137 studies (multiple observations per patient). 
Because the statistical tests and cross-validation assume independent observations, 
these results should be interpreted with caution. They are included for completeness 
as an exploratory supplement to the primary independent-dataset analysis.
```

Step 2: Move these blocks from results.tex to the new appendix:
- Section 3.2.1 text + Table 3.1 (top 10 radiomics features, full dataset)
- Section 3.4.1 text + Table 3.4 (ML results, full dataset) + Figure 3.3 (ROC curves)

Step 3: In results.tex main text, replace removed sections with brief references:
- Under Section 3.2, add one sentence: "An exploratory analysis on the full dataset of 137 studies is reported in Appendix~\ref{app:full_dataset}; those results have the same negative interpretation but use non-independent observations."
- Under Section 3.4, add one sentence: "Full-dataset ML results using LOOCV are reported in Appendix~\ref{app:full_dataset}."

Step 4: Renumber subsections:
- 3.2 becomes: first subsection is "Independent Dataset" (currently 3.2.3), no longer 3.2.1
- 3.4 becomes: first subsection is "Independent Dataset" (currently 3.4.2)
- OR: remove subsection headers entirely since there's only one analysis in each

Step 5: Update cross-references:
- discussion.tex references "full dataset" analysis: update to say "appendix" or reframe
- abstract.tex: check if it mentions "137 studies" analysis specifically (it mentions 137 in context of the overall dataset, not the specific analysis - likely fine)

**If delete:**
Same as above but skip creating the appendix chapter. Simply remove the sections.

---

#### Point 14 + 16: Stratification

**Decision needed from Gemma:** One of three options:

**Option A - Remove radiomics stratification entirely:**
- Delete Section 3.2.2 (Stratified Analysis) from results.tex (lines 49-51, about 3 lines of text)
- Remove the motivo-based paragraph from clinical section (line 172 of results.tex)
- Keep days-based clinical stratification (it replicates Bassaganyas)
- Simplest option. Radiomics result on 55 independent patients is sufficient.

**Option B - Move to appendix alongside full-dataset results:**
- Move Section 3.2.2 into the new "Full-Dataset Exploratory Analysis" appendix
- Same issue: done on 137 non-independent studies

**Option C - Redo on independent dataset:**
- Filter independent dataset (55 patients) by days post-transplant
- Early: patients whose selected study was <= 90 days (estimated ~25)
- Late: patients whose selected study was > 90 days (estimated ~30)
- Run Mann-Whitney on each subset, compare rejection vs no-rejection
- Problem: very small subgroups (~10-15 rejection cases per stratum)
- Requires: load 18_independent_dataset_normalised.csv, merge with dias_pTXP from bd_estudiUPF.csv, split, run stats
- Could be a new notebook or a few cells added to existing NB 19

**For clinical stratification (point 16):**
- The days-based clinical stratification (Section 3.3.2) STAYS regardless - it replicates Bassaganyas
- The motivo-based comparison paragraph (results.tex line 172) can be kept as a one-line note or removed
- It adds confusion without adding much value. Recommend removing or shortening to one sentence.

---

#### Point 15: Clinical stats on independent patients (new analysis)

**Decision needed from Gemma:** Run this supplementary analysis?

**If yes:**

Step 1: Create notebook `24_clinical_stats_independent.ipynb` (or add cells to NB 19)

Step 2: Implementation:
```python
# Load independent dataset study IDs
independent = pd.read_csv("analysis/reports/18_independent_dataset_normalised.csv")
study_ids = independent["study_id"].tolist()  # 55 IDs

# Load clinical spreadsheet
clinical = pd.read_csv("data/bd_estudiUPF.csv")

# Filter to 55 independent studies
clinical_indep = clinical[clinical["study_id"].isin(study_ids)]

# Run Mann-Whitney on each of 17 clinical features
# Group by RECHAZO CLINICO (0 vs 1)
# Report p-values, effect sizes, medians
```

Step 3: Expected output:
- Table with 17 rows (4 ARFI + 13 DCE-US), columns: feature, n_NR, n_R, p-value, effect size, median NR, median R
- Sample sizes will be smaller than full dataset (not all 55 will have ARFI/DCE-US data)
- Estimated: ~40 with ARFI, ~45 with DCE-US (based on 88% and 92% availability rates)

Step 4: Interpretation hypothesis:
- ARFI might still be significant (it's a between-patient signal that persists even with independent observations)
- Or it might lose significance due to smaller sample size
- Either way it's informative: if significant = confirms between-patient discrimination; if not = sample size issue

Step 5: Add to results.tex:
- New subsection under Section 3.3: "Independent Patient Analysis" 
- Or add a paragraph after the replication table
- Brief: "When restricted to 55 independent observations, ARFI mediana [remained significant / did not reach significance] (p = X)."

Step 6: Add to methods.tex:
- One sentence noting that clinical features were additionally tested on the independent patient subset

---

#### Files to modify in Phase 3 (after meeting confirms approach):

| File | What changes |
|------|-------------|
| `results.tex` | Remove/move 3.2.1, 3.2.2, 3.4.1; renumber subsections; add brief cross-references |
| `appendix.tex` | New chapter "Full-Dataset Exploratory Analysis" with moved content |
| `methods.tex` | Add sentence explaining independent dataset is primary; possibly note clinical independent analysis |
| `discussion.tex` | Update references to "full dataset" to say "appendix" or remove; reframe if needed |
| `abstract.tex` | Likely no change (already mentions independent dataset) |
| `bibliography.bib` | No change |
| New notebook (if point 15) | `24_clinical_stats_independent.ipynb` or added cells in NB 19 |

---

#### Execution order after meeting:

1. Point 10+17B first (biggest structural change, move sections to appendix)
2. Point 14+16 next (remove or move stratification, depends on decision)
3. Point 15 last (new analysis if requested, then add results)
4. Compile and verify after each step
5. Final read-through of results.tex for flow and numbering

### Phase 4: Email response -- COMPLETED
Email drafted and reviewed. Sent (or ready to send) before Wednesday meeting.

---

## Files to Modify

| File | Changes |
|------|---------|
| `introduction.tex` | Points 1, 2, 3, 4, 5, 6 |
| `methods.tex` | Points 2, 9, 11, 12, 13, 14, 16, 17 |
| `results.tex` | Points 10, 14, 15, 16, 17 (MAJOR restructure) |
| `discussion.tex` | Point 1 (wording), point 10 (update framing) |
| `abstract.tex` | Point 1 (wording), point 10 (update framing) |
| `bibliography.bib` | Point 4 (new references) |

---

## Decisions Made

1. **Point 10 (full-dataset analysis):** Move to appendix with explicit caveat about non-independence. Present as "exploratory, for completeness" - not as primary results.

2. **Point 14/16 (stratification):** Discuss with Gemma. Clara's paper does stratify on full dataset (precedent). Potentially add independent-dataset stratification as supplementary. Keep for now with caveat.

3. **Point 15 (clinical replication):** Keep replication as-is (matching Bassaganyas) AND also add independent-patient clinical analysis. Note: clinical features are NOT in the independent dataset CSV - need to extract from `bd_estudiUPF.csv` filtered to the 55 patients. Requires a small new analysis.

4. **Point 17 (full-dataset ML):** Move to appendix alongside full-dataset stats. Independent-dataset ML (NB 20) is primary.

## Implementation Notes

- Running clinical stats on independent dataset requires: load `bd_estudiUPF.csv`, filter to 55 study IDs from independent dataset, run Mann-Whitney on ARFI + DCE-US features.
- The stratification question (early/late on independent dataset) results in small subgroups (~20-30 per stratum). Discuss with Gemma whether this is worthwhile.
- All text changes to the thesis require recompilation and checking for LaTeX errors.
