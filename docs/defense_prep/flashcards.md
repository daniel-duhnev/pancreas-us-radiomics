# Flashcards

Q → A recall cards, grouped by module and tagged **[E]** easy / **[M]** medium / **[H]** hard.
Cover the answer, say it out loud, then check. Re-drill anything you miss.

---

## M0 · Big picture

- **[E]** Q: In one sentence, what did your thesis test?
  A: Whether radiomics texture features from grayscale B-mode ultrasound can predict pancreas
  transplant rejection.
- **[E]** Q: What was the headline result?
  A: They cannot — no feature survives FDR, best ML AUC 0.636 with CI including chance.
- **[M]** Q: What is the "positive control" and what exactly does it validate?
  A: The *same statistical analysis* (same patients, same labels) recovers the clinical ARFI/DCE-US
  signal to 3 decimals but finds nothing in radiomics → the analysis is sound and powered, so the
  radiomics null is real. Scope: it validates the stats/data handling, NOT the image pipeline.
- **[M]** Q: List the five objectives.
  A: (1) Extract radiomics features; (2) test individual features; (3) build ML classifiers;
  (4) reproduce Bassaganyas' clinical analysis; (5) compare radiomics vs clinical biomarkers.
- **[H]** Q: Why is a negative result a real contribution here?
  A: It's a *controlled, mechanistically-explained* negative (not inconclusive); it narrows the search
  space; it confirms specialised modes remain necessary; negatives are scarce due to publication bias.

## M1 · Clinical background

- **[E]** Q: What does a pancreas transplant restore?
  A: Endogenous, glucose-responsive insulin production → long-term normoglycaemia in type-1 diabetes.
- **[E]** Q: What is the reference standard for diagnosing rejection?
  A: Percutaneous biopsy, graded by the Banff schema.
- **[M]** Q: Give three limitations of biopsy.
  A: Invasive/risky (bleeding, pancreatitis, fistula); deep graft not always accessible; sampling
  error (focal rejection missed).
- **[E]** Q: What does ARFI elastography measure, physically?
  A: Tissue stiffness, via shear-wave velocity (m/s) — stiffer tissue = faster wave.
- **[E]** Q: What does DCE-US measure?
  A: Microvascular perfusion, via microbubble contrast wash-in/wash-out time–intensity curves.
- **[M]** Q: What physically creates a B-mode image?
  A: Echoes from boundaries where acoustic impedance (density × speed of sound) changes — i.e.
  macroscopic tissue interfaces.
- **[M]** Q: Name the three rejection types.
  A: Acute T-cell-mediated, antibody-mediated, chronic (fibrosis).
- **[H]** Q: Why the 90-day cutoff?
  A: The first 90 days are noisy (surgical healing, post-op oedema); after 90 days rejection-related
  stiffness/perfusion changes become detectable. Same cutoff as Bassaganyas.
- **[M]** Q: What did Bassaganyas et al. 2025 find?
  A: In the late period, rejection had higher ARFI stiffness (1.46 vs 0.97 m/s, p<0.001) and lower
  DCE-US perfusion; combined OR ~23. Same cohort/scanner as your thesis.

## M2 · Radiomics & pipeline

- **[E]** Q: What does radiomics do?
  A: Extracts many quantitative texture/intensity/heterogeneity features from an image for analysis.
- **[M]** Q: Walk the preprocessing pipeline.
  A: Load RGB → detect white contour (all channels >200) → largest connected component → morphological
  close (10×10) → fill → subtract contour → grayscale → erode (3×3, 1 iter).
- **[M]** Q: Why remove the white contour before extraction?
  A: The bright annotation line would create artificial high-intensity texture and corrupt features.
- **[H]** Q: What special handling did studies 03_01 and 43_01 need, and why?
  A: Their contours had large gaps → normal 10×10 closing failed → empty masks; fixed with a 35×35
  closing kernel to force the gaps closed.
- **[E]** Q: Name the six feature classes.
  A: First-order, GLCM, GLRLM, GLSZM, GLDM, NGTDM.
- **[M]** Q: What does GLCM capture vs first-order?
  A: GLCM = co-occurrence of grey-level *pairs* at an offset (spatial texture); first-order = intensity
  histogram stats with *no* spatial info.
- **[M]** Q: Why per-image z-score normalisation?
  A: Ultrasound has no fixed intensity scale (unlike CT Hounsfield units); gain/depth/pressure change
  brightness, so z-scoring makes scans comparable.
- **[M]** Q: Why disable shape features?
  A: ROI geometry reflects imaging plane/probe angle, not graft biology — it would add acquisition noise.
- **[H]** Q: What do the alternative feature families rule out?
  A: "Wrong features" — LBP, Gabor, and Laws' are three distinct texture methods, all null.
- **[H]** Q: What does surrounding-tissue normalisation rule out?
  A: Acquisition variability as the confound — local normalisation didn't reveal a signal (slightly
  worse), so the null isn't an acquisition artifact.

## M3 · ML & statistics

- **[E]** Q: How many studies/patients in the full vs independent dataset?
  A: Full 137 studies/55 patients; independent 55 studies/55 patients (one per patient).
- **[M]** Q: What is the independence problem?
  A: Repeated studies per patient are correlated; violates the independence assumption → inflated
  p-values (stats) and patient leakage across folds (ML).
- **[M]** Q: How is the independent dataset built?
  A: One study per patient; for the 14 dual-outcome patients, the first rejection study; otherwise the
  first available study.
- **[M]** Q: Shapiro → which tests?
  A: Both groups normal → Welch's t-test; otherwise Mann-Whitney U.
- **[M]** Q: Why Welch's rather than Student's t-test?
  A: Welch doesn't assume equal variances (separate variance estimates, adjusted df) — safer with
  unequal groups.
- **[E]** Q: What does FDR / Benjamini-Hochberg control?
  A: The false discovery rate — the expected proportion of false positives among features called
  significant.
- **[M]** Q: Walk the ML pipeline.
  A: Correlation filter (|r|>0.9) → StandardScaler → SelectKBest(F-stat, k tuned) → classifier;
  scaler+selection refit inside each CV fold.
- **[E]** Q: The four classifiers?
  A: Logistic Regression, Random Forest, SVM, Gaussian Naive Bayes.
- **[M]** Q: What does an AUC of 0.5 mean? And a CI including 0.5?
  A: 0.5 = chance (no better than random ranking); a CI including 0.5 = performance indistinguishable
  from chance.
- **[H]** Q: LOOCV vs stratified k-fold — trade-off?
  A: LOOCV nearly unbiased but high variance; stratified k-fold balances bias/variance and preserves
  class ratio. Used 10-fold (independent) / 5-fold (full).

## M4 · Results

- **[E]** Q: Best radiomics AUC and CI?
  A: 0.636, 95% CI [0.48, 0.78] (Logistic Regression) — includes chance.
- **[E]** Q: How many radiomics features survive FDR?
  A: Zero (24 nominal, all adjusted p ≥ 0.16).
- **[M]** Q: What happened with the SVM and why is it informative?
  A: Collapsed to AUC 0.408, predicting nearly everything as rejection (spec 0.029) — the sign of no
  separable signal in a small imbalanced set.
- **[M]** Q: ARFI late-period result?
  A: p < 0.001, effect size r = 0.72 (mediana); 8/17 clinical features significant in the late period.
- **[H]** Q: Why are clinical features null on the independent dataset?
  A: Only 7 of 21 rejection studies fall in the late window; pooling early+late dilutes the ARFI
  effect. Doesn't contradict the positive late result.
- **[H]** Q: Paired clinical ARFI result and meaning?
  A: p = 0.86 — non-significant within-patient; ARFI reflects stable between-patient baseline
  stiffness, not a transient within-patient rejection change.

## M5 · Narrative

- **[H]** Q: Why, physically, does B-mode texture miss rejection but ARFI/DCE-US catch it?
  A: B-mode texture encodes macroscopic acoustic-impedance boundaries (~0.5–2 mm); rejection is
  microscopic (inflammation, oedema, fibrosis). ARFI/DCE-US measure stiffness/perfusion — properties
  rejection changes directly.
- **[M]** Q: Give the one-line summary of the physical explanation.
  A: "Rejection changes stiffness and perfusion, not the acoustic-boundary texture B-mode encodes."
- **[M]** Q: Why does radiomics work for liver/thyroid/breast but not here?
  A: Those involve larger, focal structural changes; early diffuse rejection has no focal
  texture-contrast lesion.

## M6 · Defence

- **[H]** Q: State your master framing in one breath.
  A: Every debatable choice biases performance *upward*; results are still at chance, so the negative
  conclusion is conservative — and the positive control shows the shared statistical analysis detects
  a real signal when one exists.
- **[M]** Q: "Isn't it underpowered?" — best answer?
  A: The same statistical analysis recovered ARFI at p<0.001 from the clinical measurements in the
  same patients; and six independent analyses all agree — not a power artifact.
- **[H]** Q: Does the positive control validate your image pipeline?
  A: No — the clinical values are tabular and never touch segmentation/PyRadiomics; they share only
  the downstream stats. It validates the analysis, not the imaging. The imaging is defended by the 3
  alternative descriptors + QC (residual: no dedicated segmentation control).
- **[M]** Q: Is your CV truly nested?
  A: No — k and hyperparameters were tuned on all data (disclosed in Limitation 5). That bias is
  upward, so a nested version would push AUCs toward 0.5.
- **[M]** Q: Is the independent dataset external validation?
  A: No — a one-study-per-patient subsample of the same cohort, for independence, not external
  validation.
- **[H]** Q: Can you reproduce the extraction exactly? (provenance)
  A: Features were extracted when all 137 studies were present; a later migration lost the raw images
  for 3 studies (34_02/40_02/41_03), so a clean re-run yields 134. It's a data-transfer gap, not an
  analysis error, and doesn't change the null conclusion.

## M7 · Logistics

- **[E]** Q: Date, time, room?
  A: 16 July 2026, 09:00, room 55.309.
- **[E]** Q: The committee?
  A: Gemma Piella (supervisor), Miguel Ángel González Ballester, Sotiris Papadiamantis.
- **[M]** Q: Session structure?
  A: 20–25 min talk → 15–20 min questions per committee member → you leave → they deliberate → grade
  announced.
- **[M]** Q: Which version gets graded?
  A: The copy sent to the committee ~1 week before the defense (later repo edits don't affect the grade).
