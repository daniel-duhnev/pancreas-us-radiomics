# M6 · Defending Weaknesses & Tough Questions

Goal: never be cornered. Every question below is one a sharp committee could ask. Each has a
**model answer** and, where useful, an **"if pushed further"** follow-up. Practice saying these out
loud until they're natural.

**Your master framing — deploy it constantly:**

> "Almost every debatable choice in my pipeline could only make performance look *better* than it
> truly is. Since the result is still at chance even so, those choices make my negative conclusion
> **conservative**, not fragile. And the positive control shows the shared statistical analysis can
> detect a real signal when one exists."

Most of these weaknesses are **already disclosed in your Limitations section** — so you're not
admitting anything new, you're demonstrating you understand your own work. A few (marked ⚠ *not in
the thesis*) are things to handle honestly if they come up.

---

## A. "Is this just an underpowered / failed study?"

**Q: With only 55–137 samples and 93 features, isn't your negative result just low power?**
- Model answer: "Two things rule that out. First, the **positive control**: the *same statistical
  analysis*, on the same patients with the same labels, recovered the published ARFI result at
  p < 0.001 to three decimal places from the clinical measurements. If the analysis were simply too
  weak to detect *any* effect in this cohort, it couldn't have detected that one. Second, the null
  result is **consistent across six independent analyses** — univariate, multivariate ML,
  time-stratified, paired, three alternative feature families, and tissue normalisation. A power
  problem wouldn't produce that uniform convergence. Any undetected radiomics effect would have to be
  very small."
- If pushed: "A formal power analysis isn't meaningful for a multivariate radiomics pipeline where
  the true effect size is unknown — but the positive control is a stronger, empirical demonstration
  that the statistical analysis has enough power to find a real signal in this cohort."

**Q: Your positive control is on tabular clinical data — how does that validate your image-processing
pipeline at all?** ⚠ *(the sharpest version of the question — likely from a computer-vision examiner)*
- Model answer: "It's an important distinction, and I want to be precise. The clinical ARFI and
  DCE-US values are measurements that never pass through my segmentation or PyRadiomics extraction —
  they enter the *same downstream statistical analysis* as the radiomics features, from the same
  patients with the same rejection labels. So the replication validates my **statistical analysis and
  data handling**, and proves that analysis is powered to detect a real effect — it rules out 'the
  statistics are broken or underpowered.' It does **not** validate the image-processing stage, and I
  don't claim it does."
- If pushed ("then how do you know your segmentation/extraction isn't the problem?"): "The image
  pipeline is defended separately. Three *independent* feature descriptors — PyRadiomics, plus LBP,
  Gabor, and Laws' texture energy — are all null; a single extraction bug wouldn't fool three
  different methods. Extraction completed error-free on all studies with sensible, well-behaved
  feature distributions and the expected within-class correlation structure, and I visually checked
  the masks. The honest residual limitation is that all the texture methods share the *same
  segmentation*, so there's no dedicated positive control for the segmentation stage itself — a
  test–retest or a synthetic-phantom check would be the way to add one. But a segmentation subtle
  enough to wipe out a real signal while leaving error-free, sensible features is unlikely, and it
  would have to do so consistently across four descriptors."

**Q: You have more features than samples — isn't that hopeless / overfitting?**
- "That high-dimensional regime is exactly why I did *not* rely on raw multivariate fitting. I
  reduced 93 correlated features to ~30 with a correlation filter, used SelectKBest inside the
  pipeline, regularised every model, and used class-balanced weights. And I judged success by AUC
  confidence intervals, not point estimates — all of which include chance. Overfitting would inflate
  *apparent* performance; I still saw none."

---

## B. Radiomics & extraction choices

**Q: You discarded the physical pixel spacing — isn't your texture confounded by scanner
depth/zoom?** *(This is disclosed in Limitation 4.)*
- Model answer: "Yes — I did not resample, so texture was computed in pixel units, and physical
  spacing varies about 2.7-fold across the cohort, roughly 0.11 to 0.29 mm. That's a real
  limitation, and I state it. But crucially, variable spacing adds **noise** to the texture
  measurements — it makes a genuine signal *harder* to detect. It cannot manufacture a spurious
  association between texture and rejection, because the spacing varies with imaging depth, not with
  rejection status. So if anything it makes my negative result more conservative. Correcting it
  would only push the AUCs further toward 0.5."
- If pushed ("shouldn't you have resampled?"): "In principle yes, and that's the standard IBSI
  recommendation; I'd add `resampledPixelSpacing` in a revision. Given the result is already null,
  I expect it to strengthen, not change, the conclusion."

**Q: Why bin width 25? Isn't that arbitrary for uncalibrated ultrasound intensities?**
- "25 is the PyRadiomics default and I report it. Fixed-bin-width discretisation is a standard IBSI
  choice. I agree that for an uncalibrated modality a fixed **bin count** is arguably cleaner, and
  a sensitivity analysis over bin settings would be a reasonable extension. But the three
  *alternative* feature families I tested — LBP, Gabor, Laws' — don't use PyRadiomics binning at all
  and were also null, so the discretisation choice isn't driving the result."

**Q: Your normalisation — is it normalising the ROI or the whole image?**  ⚠ *(nuance not spelled
out in the thesis)*
- "PyRadiomics `normalize=True` performs a **per-image** z-score using the whole image's mean and
  standard deviation, which is what my Methods describes. I also recognised that whole-image
  statistics can be influenced by the large off-sector background, which is exactly why I ran the
  **surrounding-tissue normalisation** experiment — a *local* normalisation using the ring of tissue
  around the graft. That also produced null results, so the normalisation scope isn't hiding a
  signal either."
- Honesty note: an internal code comment mislabelled this as per-ROI; the *thesis text is correct*
  (per-image). If asked precisely, describe the per-image behaviour and pivot to the surrounding-
  tissue experiment as the local-normalisation check.

**Q: Why disable shape features?**
- "ROI geometry here reflects the imaging plane and probe angle, not the graft's true morphology —
  the same graft looks different depending on how it's insonated. Shape features would encode
  acquisition conditions rather than biology, so including them would add noise. Texture and
  intensity are the biologically meaningful signals for this question."

**Q: How do you know it's not just the wrong feature set (PyRadiomics)?**
- "I tested three methodologically distinct alternative families — Local Binary Patterns, Gabor
  filters, and Laws' texture energy, 153 features total. Each captures texture differently, and all
  three were null after correction. Three independent feature philosophies failing together rules
  out 'wrong features' as the explanation."

---

## C. ML methodology (the most likely grilling area)

**Q: You call it nested CV, but did you tune hyperparameters on the whole dataset?** *(Disclosed in
Limitation 5.)*
- Model answer: "I'm glad you asked, because I'm explicit about this in my limitations. The number
  of selected features k and the model hyperparameters were chosen by grid search over the full
  dataset, and only the scaler and selected-feature identities were refit per fold — so it's not
  fully nested. That introduces an **optimistic** bias. But that bias can only make performance look
  *better*. Since the AUCs are still at chance, a properly nested CV would push them *toward* 0.5 and
  reinforce my conclusion. The grids are small, so the effect is minor. If I were revising, I'd pass
  the whole GridSearch as the estimator to `cross_val_predict` to make it truly nested."
- Key line: "Every leakage in my pipeline biases *upward*, and I still found nothing."

**Q: The correlation pre-filter used p-values from the full labelled data — isn't that leakage?**
*(Disclosed in Limitation 5.)*
- "Yes, the tie-break between two features correlated above 0.9 used full-data univariate p-values,
  so a small amount of label information enters feature reduction before the split. It only decides
  *which of two near-duplicate features* to keep, so the impact is tiny — and again it can only
  inflate performance. A label-free tie-break (e.g. keep the feature with lower mean correlation to
  the rest) would remove it entirely."

**Q: Your reported sensitivity and specificity — what threshold?** *(Disclosed in Limitation 5.)*
- "They're reported at the Youden-optimal operating point computed on the pooled out-of-fold
  predictions — an in-sample operating point, so those sens/spec values are optimistic. The AUC,
  which is threshold-independent, is unaffected and is my primary metric. I'd choose the threshold
  inside each training fold in a revision."

**Q: SVM got AUC 0.408 with specificity 0.029 — did your model break?**
- "That's actually informative. The SVM collapsed to predicting almost everything as rejection —
  sensitivity 1.0, specificity near 0 — which is what an SVM does on a small, imbalanced dataset
  when there's **no separating signal** to find. Its failure is consistent with the overall
  conclusion: there's no stable structure for it to latch onto. Logistic Regression and Naive Bayes
  were more stable but still at chance."

**Q: The full (137-study) dataset — didn't the same patient appear in train and test?** *(Disclosed
in Limitation 3.)*
- "Yes, and that's precisely why the 137-study analyses are **exploratory only**, in the appendix.
  With repeated measures, LOOCV leaves out one study while the same patient stays in training —
  patient-level leakage. My **primary** analyses use the independent one-study-per-patient dataset,
  where no patient can span train and test, so it's leakage-free by construction. Tellingly, the
  leaky full-set result (AUC 0.564) is actually *lower* than the clean independent result (0.636),
  which is reassuring."
- If pushed ("why not GroupKFold on the 137 set?"): "That would be the right fix to make the
  full-set analysis valid — group by patient_id, which I already carry in the data. I instead
  solved the independence problem upstream by building the independent dataset as the primary
  analysis, and demoted the full set to exploratory."

---

## D. Statistics

**Q: You didn't FDR-correct the clinical features — inconsistent with the radiomics?** *(Disclosed
and justified in Methods.)*
- "That was deliberate. The clinical analysis exists to **replicate** Bassaganyas et al., who
  reported per-feature uncorrected p-values. To compare like-for-like, I used the same uncorrected
  testing, and I state this in Methods — the clinical p-values are a methodological validation, not
  an independent claim. My *own* radiomics hypothesis tests all use Benjamini-Hochberg FDR."
- ⚠ Honesty note: the *paired* clinical block did not get FDR where the radiomics block did. If
  asked specifically about the paired analysis, acknowledge that adding FDR there for consistency
  would be a reasonable fix — but note the clinical paired features weren't significant even
  uncorrected (best p = 0.16), so it changes nothing.

**Q: Why Shapiro-then-Welch/Mann-Whitney instead of one test?**
- "For each feature I first checked normality with Shapiro-Wilk; if both groups looked normal I used
  Welch's t-test, otherwise the non-parametric Mann-Whitney U. This adapts the test to each
  feature's distribution. I used Welch rather than Student's because it doesn't assume equal
  variances, which is safer with unequal group sizes."

**Q: 24 of 93 features were nominally significant — that sounds like a lot.**
- "It's 26%, which is above the naive 5%, but the 93 features are highly correlated — 316 pairs
  exceed 0.9 correlation — so they're not 93 independent tests. After Benjamini-Hochberg correction,
  **none** survive, all adjusted p at or above 0.16. And the nominally-significant features are
  **different** across my independent, full, and paired analyses, which is the signature of chance
  findings rather than a real, reproducible effect."

---

## E. Dataset & provenance

**Q: Your 'independent dataset' — is that external validation?**
- "No, and I'm careful with the terminology. It's a **one-study-per-patient subsample** of the same
  cohort, built so that observations are independent — which is what statistical tests and
  cross-validation require. It is not external, held-out data. Its purpose is to remove the
  repeated-measures confound, not to validate on a new population. True external validation on
  another centre's data is future work."
- If pushed on selection: "For the 14 patients with both outcomes I selected their first rejection
  study, to keep the rejection group populated. That's an outcome-conditioned choice, which I'd flag
  as a limitation — it slightly enriches rejection and favours earlier studies. But the conclusion
  is null regardless."

**Q: How were the 14 dual-outcome patients handled consistently across analyses?** ⚠
- "In the independent dataset I pick the first rejection study; in the paired analysis I instead
  pick a maximally-separated rejection/no-rejection pair for the same patient. They serve different
  purposes — independence vs within-patient contrast — so they legitimately select different studies.
  Both point to the same null conclusion."

**Q: Can you reproduce your feature extraction exactly?** ⚠ *(The provenance gap — handle honestly
if it arises; unlikely unless they run the code.)*
- Honest answer if directly asked: "The features were extracted from all 137 studies at analysis
  time. During a later machine migration, the raw images for three studies (34_02, 40_02, 41_03)
  were not carried over, so re-running extraction today would regenerate 134 of the 137. The
  computed features and all downstream results are from when the data was complete; the gap is a
  data-transfer issue, not an analysis error. Recovering those three from the original hospital
  export, or re-running cleanly to n=134, would resolve it — and given everything is null, it
  wouldn't change the conclusion."
- Do **not** volunteer this unprompted. It's a reproducibility housekeeping issue, not a result
  issue. If it comes up, be straight about it and move on.

**Q: Why exclude study 47_01?**
- "Its images were never recovered from the imaging system and the hospital confirmed they can't be
  provided. It was a rejection case, so excluding it slightly *reduces* the rejection group — it
  doesn't help my result. It's kept in the clinical replication, though, because that study had
  valid ARFI/DCE-US measurements even without images."

**Q: Small discrepancy — the thesis says 93→27 features but is it exactly 27?** ⚠
- "The correlation filter removes the redundant half of every pair above 0.9, cutting the ~93
  features down to roughly 30. If the precise count is queried, I'd verify it against the code — the
  exact number depends on the dataset variant. The substantive point is that heavy redundancy
  reduction still left no discriminative signal."
- Honesty note: thesis text says 27; the committed normalised-independent code reduced to 31 (SVM
  used k=31). Minor and immaterial, but don't defend "27" as exact if challenged — describe it as
  "about a third of the features remain."

---

## F. Interpretation

**Q: Why should we believe rejection has *no* texture signature at all?**
- "I don't claim it's physically impossible — I claim it's **not detectable** in grayscale B-mode
  texture at clinical resolution, in this cohort, with these methods. The mechanism explains why:
  B-mode texture encodes macroscopic acoustic-impedance boundaries at roughly 0.5–2 mm resolution,
  while rejection is a microscopic change — cellular infiltration, oedema, fibrosis. ARFI and DCE-US
  work because they measure stiffness and perfusion, which rejection changes directly. Different
  physics, different result."

**Q: Your paired ARFI result contradicts Bassaganyas — did they get it wrong?**
- "Not at all — I *reproduced* their unpaired result exactly. What I add is that when you compare
  rejection and non-rejection studies *within the same patient*, the ARFI difference vanishes
  (p = 0.86). That suggests their signal reflects stable **between-patient** differences in baseline
  stiffness rather than a within-patient change from an acute episode. It refines the interpretation
  — ARFI may be more of a risk marker than an acute-episode diagnostic. I present it cautiously
  because I only have 14 pairs, so it could also be underpowered."

**Q: So is radiomics on ultrasound useless?**
- "No — it works where there are larger, focal structural changes: liver fibrosis staging, thyroid
  nodules, breast lesions. My result is specific to *diffuse, early pancreas transplant rejection*,
  which lacks a focal texture-contrast lesion. It narrows where texture-based radiomics is worth
  applying."

---

## G. "So what?" and future work

**Q: What's the practical impact of a negative result?**
- "It saves the field effort by ruling out a tempting cheap approach — hand-crafted texture on
  routine B-mode — and it confirms that specialised modes (ARFI, DCE-US) remain necessary. It also
  points future work in a concrete direction: deep learning on raw images, multi-parametric models
  that fuse B-mode with stiffness and perfusion, expanded PyRadiomics configurations (wavelet/LoG,
  resampling, bin-count sweeps), larger multi-centre cohorts, and longitudinal mixed-effects models."

**Q: If you had more time, what's the single most important thing you'd do?**
- Pick one and commit: "A multi-parametric model fusing B-mode with the ARFI and DCE-US measurements
  — because my results show the discriminative information lives in stiffness and perfusion, so
  anchoring a model on those and testing whether B-mode adds anything is the highest-value next
  step." (Alternatively: deep learning on raw images, or external multi-centre validation.)

---

## The landmine questions — over-prepare these

1. "Isn't it just underpowered?" → positive control (same stats, clinical signal recovered) +
   six-way convergence.
2. "Does the positive control validate your *image* pipeline?" → No — it validates the statistical
   analysis only; the imaging stage is defended by the 3 alternative descriptors + QC (residual: no
   dedicated segmentation control — concede it).
3. "Your CV isn't nested / you tuned on all data." → disclosed; bias is upward; still null →
   conservative.
4. "Same patient in train and test?" → full set is exploratory/appendix; independent set is
   leakage-free primary.
5. "Can you reproduce the extraction exactly?" → be honest about the 3 lost studies; not a result
   issue; conclusion unchanged.
6. "Why no texture signal at all?" → the physics: macroscopic boundaries vs microscopic pathology.

---

## Quick self-check

- Deliver the master framing ("every choice biases upward, still null → conservative") in one breath.
- Answer the "underpowered?" question using the positive control.
- Concede the non-nested CV *and* turn it into a strength.
- Handle the provenance question honestly without derailing.
- Explain the paired ARFI result without implying Bassaganyas was wrong.
