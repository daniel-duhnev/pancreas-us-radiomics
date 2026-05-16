# Thesis Proofread Findings

Full review conducted May 16, 2026. All numbers verified against source CSVs.

---

## Critical Issues (factual/accuracy)

### 1. introduction.tex line 35 - "23.2-fold probability of rejection"
The phrase "23.2-fold probability of rejection" is unclear. Probabilities cannot exceed 1, so a "23.2-fold probability" is meaningless as stated. This likely refers to an odds ratio or likelihood ratio from the Bassaganyas paper. Should be rephrased to "23.2-fold odds ratio" or "combined score yielded an odds ratio of 23.2 for rejection" -- but only after verifying against the actual paper what the 23.2 represents (OR? relative risk? likelihood ratio?).

### 2. introduction.tex line 35 - "first prospective study"
The introduction calls the Bassaganyas study "prospective." The methods chapter describes our dataset as "retrospective" (methods.tex line 6). Both use the same cohort. If the dataset is retrospective, the Bassaganyas study cannot be prospective on the same data. Verify whether Bassaganyas describe their study as prospective or retrospective, and make the two chapters consistent.

### 3. methods.tex line 115 - "fixed bin width of 25 grey levels (the PyRadiomics default)"
Verified: the default IS 25 (confirmed from PyRadiomics source code). However, the NB 12 code does NOT explicitly set binWidth -- it relies on the default. The statement is factually correct but might benefit from explicitly stating "default value, not explicitly configured" for full transparency. **Minor -- no change strictly required.**

---

## Moderate Issues (clarity, consistency, structure)

### 4. methods.tex line 48 - dataset summary table says "Number of patients: 56"
The table says 56 patients but the text (line 48) says the cohort was reduced to 55 patients after excluding 47_01. The table should clarify: 56 originally enrolled, 55 with usable data. Currently the table mixes pre- and post-exclusion numbers (56 patients but 137 studies). Either change to 55 and add a footnote, or add a row "Patients with usable imaging: 55".

### 5. results.tex line 70 - Full clinical dataset "138 studies (98 NR, 40 R)"
This is the clinical set including 47_01. But the radiomics sections use 137 studies (98 NR, 39 R). The text explains this but the jump from 39 R to 40 R between adjacent sections could confuse a reader. Consider adding "(including 47_01)" parenthetically when the 138/40 numbers appear.

### 6. methods.tex line 162 - FDR not applied to clinical features
The text says "FDR correction was not applied to the clinical features" and gives the reason (replicating Bassaganyas). This is methodologically sound but should ideally be mentioned again briefly in the results (Section 3.3) since a reader might jump there directly. Currently the results just present uncorrected p-values without reminding why.

### 7. results.tex line 187 - "optimistic bias from the nested hyperparameter tuning"
The 5-fold AUCs are described as having "optimistic bias from the nested hyperparameter tuning." This is slightly misleading -- nested CV is designed to reduce bias, not introduce it. The bias comes from the inner CV overfitting to the training folds. Rephrase to something like "marginally higher, likely reflecting optimistic inner-fold selection rather than true signal."

### 8. introduction.tex line 23 - "Rejection remains the leading cause of graft failure beyond the first 90 days"
Cited to white2009. This is a strong claim. If white2009 doesn't say exactly this (it may say "one of the leading causes" or give a different time frame), it should be softened. Worth double-checking the paper.

### 9. results.tex line 245 - "maximised the temporal separation between the two studies (measured by study-number gap)"
The term "temporal separation" is slightly misleading when it's actually measured by study-number gap, not actual days. The gap between visit 01 and visit 03 could be 2 weeks or 2 years depending on scheduling. Rephrase to "maximised the study-number gap between the two observations" and drop "temporal."

---

## Minor Issues (style, formatting, wording)

### 10. Inconsistent use of em-dashes vs dashes
The thesis uses `---` (em-dashes) in some places (results.tex lines 25, 104, etc.) and regular dashes elsewhere. The user mentioned another agent was removing em-dashes. Need to decide: all em-dashes or all single dashes. Currently mixed.

### 11. methods.tex line 39 - "Area" feature has "---" as full name
In Table tab:clinical_features, the "Area" DCE-US feature has "---" as its full name. This should either be given a proper description or noted as "total enhancement area" or similar.

### 12. results.tex lines 40-44 - Missing median values in table
Table tab:radiomics_top10 shows "---" for the median NR/R values of features ranked 6-10. This is inconsistent with showing values for features 1-5. Either show all or explain why some are omitted.

### 13. methods.tex line 98 - Special handling paragraph
The paragraph about studies 03_01 and 43_01 is very implementation-specific. Consider whether this level of detail belongs in the thesis or should be shortened to a single sentence ("Two studies required larger closing kernels to handle contour gaps").

### 14. introduction.tex - Related Work subsection lengths
- Section 1.2.1 (Pancreas Transplant Rejection): 2 paragraphs
- Section 1.2.2 (Ultrasound Imaging): 4 paragraphs (longest)
- Section 1.2.3 (Radiomics): 3 paragraphs
- Section 1.2.4 (ML): 3 paragraphs

Section 1.2.2 is disproportionately long relative to the others. Consider whether the detailed ARFI/DCE-US exposition could be tightened since the methods chapter covers this too.

### 15. results.tex line 6 - Feature class order inconsistency
The feature extraction results list classes as "first-order (18), GLCM (24), GLDM (14), GLRLM (16), GLSZM (16), NGTDM (5)" but Table tab:feature_classes in methods.tex lists them as "First Order, GLCM, GLRLM, GLSZM, GLDM, NGTDM". GLDM and GLRLM are swapped between the two. Should use the same order everywhere (the table order is more standard).

### 16. Abstract is still placeholder
The abstract.tex still contains the template placeholder text ("The abstract should have at least 200 but not more than 600 words...") with irrelevant keywords ("Imaging techniques; Cloud computing; Alzheimer"). This needs to be written last but flagging it so it's not forgotten.

### 17. results.tex - No section numbers in cross-references
The text writes "Section~\ref{sec:statistical_analysis}" which renders as "Section 2.4" -- this is correct. But in some places it says "(see Section~\ref{...})" and in others just "Section~\ref{...}". Should be consistent -- either always parenthetical or never.

### 18. introduction.tex line 17 - Thesis scope statement
"This thesis investigates whether radiomics texture features extracted from conventional grayscale ultrasound images can discriminate between pancreas transplant rejection and non-rejection."
This is accurate but could mention upfront that the answer is negative, so the reader isn't misled into expecting a positive result. Academic convention varies -- some prefer revealing the answer in the introduction (especially for negative results), others save it. Consider adding a sentence like "As will be shown, the results are negative, making this a methodological contribution rather than a clinical tool."

### 19. Spelling: "grey" vs "gray"
methods.tex uses "grey" (British: "grey levels", "grey-level co-occurrence") but the PyRadiomics feature names use "Gray" (American: GrayLevelVariance). This is unavoidable for the feature names but the running text should be consistently British. Verify no accidental "gray" appears in running text.

### 20. results.tex line 294 - Paired clinical interpretation
"patients who eventually experience rejection may have inherently stiffer grafts"
This is a strong causal interpretation. The paired analysis shows no within-patient change, but the alternative explanation could also be temporal: the non-rejection study might be from a period when the graft was healthy. The interpretation should be slightly more hedged: "may reflect stable between-patient differences in baseline tissue stiffness."

---

## Things That Are Correct (verified, no change needed)

- All table numbers match source CSVs (verified: 14a, 14b, 17b, 20, 21 stats)
- 137 studies / 55 patients / 98 NR / 39 R -- all correct
- 300 correlated feature pairs -- verified
- 93 -> 32 after correlation filter -- verified
- PyRadiomics binWidth=25 default -- verified from source code
- int16 cast -- verified from NB 12 code
- ARFI mediana p=0.028, median 1.255 vs 1.47 -- verified
- Motivo counts: early 67 (57/10), late 70 (41/29) -- verified
- Paired: 14 pairs, 9 features p<0.05, all FDR=0.28 -- verified
- Paired clinical: ARFI mediana p=0.86, media p=0.91 -- verified
- Independent ML: LogReg AUC 0.569, CI [0.40, 0.72] -- verified
- Bootstrap CIs match 20_bootstrap_ci.csv -- verified

---

## Suggested Additions (for future sections)

### For Results sections 3.6-3.7:
- Consider including the `23_surrounding_mask_examples.png` figure (shows methodology visually)
- Consider ROC plot from NB 22 (`22_roc_curves.png`) -- though potentially repetitive

### For Discussion:
- The paired ARFI interpretation (issue #20) should be expanded in Discussion
- The "wrong features ruled out" argument (NB 22) is strong and should feature prominently
- The intensity normalization negative result (NB 23) addresses a specific reviewer objection
- Power analysis / sample size discussion would strengthen Limitations section

---

## Priority Order for Fixes

1. **Issue #1** (23.2-fold) -- factual clarity, could mislead readers
2. **Issue #2** (prospective vs retrospective) -- factual contradiction
3. **Issue #4** (56 vs 55 patients in table) -- confusing
4. **Issue #15** (feature class order) -- inconsistency across sections
5. **Issue #9** (temporal vs study-number gap) -- misleading wording
6. Everything else is low priority / stylistic
