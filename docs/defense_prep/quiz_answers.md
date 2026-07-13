# Quiz Answer Key

Answers with brief explanations. If your answer captured the key idea, count it right even if worded
differently — the goal is understanding, not memorised phrasing. Numbers, however, must be exact.

---

## Quiz 1 — Big picture & clinical

1. **Pitch (6 beats):** problem (rejection, biopsy is bad) → opportunity (US already done; ARFI/DCE-US
   work but need specialists) → question (can radiomics on plain B-mode predict rejection?) → method
   (93 features, 137 studies, independent dataset, stats + 4 ML models) → result (null; best AUC 0.636,
   CI includes chance) → punchline (same statistical analysis recovered ARFI from the clinical
   measurements to 3 decimals → the analysis is sound/powered, so the null is real).
2. **Biopsy limits:** invasive/risky (bleeding, pancreatitis, fistula); deep graft not always
   accessible; sampling error (focal rejection missed). (Bonus: low real-world uptake.)
3. **ARFI:** tissue stiffness via shear-wave velocity; rejection (inflammation/fibrosis) increases
   stiffness → higher velocity.
4. **DCE-US:** microvascular perfusion via microbubble time–intensity curves; rejection damages
   vessels → reduced/altered perfusion.
5. **B-mode:** echoes from boundaries where acoustic impedance (density × speed of sound) changes →
   encodes macroscopic tissue interfaces, ~0.5–2 mm resolution.
6. **90-day cutoff:** first 90 days are noisy (surgical healing, post-op oedema); after 90 days the
   graft settles and stiffness/perfusion changes emerge → ARFI significant only in the late period.
7. **"Failed experiment" rebuttal:** It's a *controlled* negative — the positive control (the same
   statistical analysis recovers ARFI at p<0.001, matching the published values to 3 decimals) proves
   the analysis is sound and powered, so "no signal" is a real finding, not a broken/underpowered
   analysis. It's robust across six analyses, and the physics explains it. That narrows the field's
   search space. (The control validates the stats, not the image pipeline.)

## Quiz 2 — Radiomics & pipeline

1. Load RGB → white-pixel detection (all channels >200) → largest connected component → morphological
   **close (10×10)** → fill → subtract contour → grayscale → **erode (3×3, 1 iteration)**.
2. The bright contour line would inject artificial high-intensity texture and corrupt every
   texture/intensity feature.
3. First-order **18**, GLCM **24**, GLRLM **16**, GLSZM **16**, GLDM **14**, NGTDM **5** = **93**.
4. GLCM = grey-level pair co-occurrences at an offset (local texture); GLRLM = runs of consecutive
   same-intensity pixels (coarseness/direction); NGTDM = how each grey level differs from its
   neighbourhood average (coarseness/contrast/busyness).
5. **Shape disabled:** ROI geometry reflects imaging plane/probe angle, not graft biology → would add
   acquisition noise.
6. **Per-image z-score:** US has no calibrated intensity scale; gain/depth/pressure vary brightness, so
   z-scoring per image makes scans comparable.
7. **Alternative families rule out "wrong features":** LBP, Gabor, Laws' are three methodologically
   distinct texture methods; all null → the failure isn't specific to PyRadiomics.
8. **Pixel spacing:** variable spacing adds *noise* to texture and varies with imaging depth, not
   rejection — it can only weaken a real signal, never create a spurious one. So the null stands and is
   conservative.

## Quiz 3 — ML & statistics

1. **137** studies, **55** patients; **98 NR : 39 R** (~72:28); **14** dual-outcome patients.
   (Independent: 55 studies, 34 NR : 21 R.)
2. **Statistical:** repeated studies per patient are correlated → inflate effective sample size →
   over-small p-values. **ML:** the same patient in train and test → patient-level leakage → inflated
   apparent performance.
3. **Independent dataset:** one study per patient (first rejection study for dual-outcome patients,
   else first study). Primary because it satisfies the independence assumption — no patient spans
   train/test; full 137-set is exploratory only.
4. **Shapiro-Wilk** on each group: both normal (p>0.05) → **Welch's t-test**; otherwise
   **Mann-Whitney U**.
5. **FDR** controls the expected proportion of false positives among "significant" features; needed
   because testing 93 features at p<0.05 yields ~5% false hits by chance. Result: 24 nominal, 0 survive.
6. **Pipeline:** correlation filter (|r|>0.9, done once) → **StandardScaler** (refit per fold) →
   **SelectKBest F-stat, k tuned** (refit per fold) → classifier (refit per fold). Scaler + selection
   are inside the fold; the correlation filter is outside (a disclosed minor leakage).
7. **class_weight="balanced":** counteracts the 72:28 imbalance by penalising minority-class (rejection)
   errors more, so models don't just predict the majority.
8. **All CIs include 0.5:** performance is statistically indistinguishable from random guessing — no
   reliable multivariate signal.
9. **Correlation pre-filter leakage:** Concede — the tie-break used full-data univariate p-values, so
   label info enters before the split. Defend — it only chooses which of two near-duplicate features to
   keep (tiny impact) and biases *upward*, so the null result is conservative; a label-free tie-break
   would remove it.

## Quiz 4 — Results

1. **24** nominal (p<0.05); **0** survive FDR (all adjusted p ≥ 0.16).
2. **Logistic Regression, AUC 0.636, 95% CI [0.48, 0.78]** (k=10).
3. **SVM collapsed** (AUC 0.408, sensitivity 1.0, specificity 0.029) — predicted almost everything as
   rejection, the signature of no separable signal in a small imbalanced set.
4. **ARFI late period: p < 0.001, r = 0.72** (mediana). Positive control because the *same statistical
   analysis* (same patients/labels) detected the published clinical signal, proving the analysis can
   find a real effect when one exists — it validates the stats, not the image pipeline.
5. **Reconcile:** the independent set pools all time periods and prefers first (often early) rejection
   studies; only **7 of 21** rejection studies are late, so the late-concentrated ARFI effect is
   diluted. Consistent with the paired result.
6. **Paired ARFI p = 0.86:** within-patient, the ARFI difference vanishes → the signal is a stable
   *between-patient* baseline-stiffness effect, not a transient within-patient rejection change.
   (Caveat: only 14 pairs → could be underpowered.)
7. **Replication:** 10 of 12 features match Bassaganyas to 3 decimal places; only **RT** differs
   (0.142 vs 0.276), both non-significant — likely a curve-fitting/database-update difference.

## Quiz 5 — Narrative

1. **Physical explanation:** B-mode texture encodes macroscopic acoustic-impedance boundaries at
   ~0.5–2 mm; rejection is microscopic (inflammation, oedema, fibrosis) → not captured by texture.
2. **ARFI/DCE-US succeed:** they measure stiffness and perfusion — properties rejection changes
   directly — which are *proximal* to the pathophysiology, unlike distal texture.
3. **Between vs within:** unpaired ARFI p<0.001 but paired p=0.86 → the effect is between-patient
   (baseline stiffness / risk marker), not a within-patient acute change. Caveat: 14 pairs may be
   underpowered; hypothesis-generating, not definitive.
4. **Value:** narrows the search space (texture on B-mode is a dead end here); confirms specialised
   modes remain necessary; provides a template for a *credible* negative (positive control + robustness).
5. **Liver/thyroid/breast:** those involve larger, focal structural changes with texture contrast;
   early diffuse rejection has no focal lesion → texture methods fundamentally limited.

## Quiz 6 — Defence

1. **Master framing:** "Every debatable choice in my pipeline biases performance upward; it's still at
   chance, so the negative conclusion is conservative — and the positive control shows the shared
   statistical analysis can detect a real signal when one exists."
2. **Not nested:** Concede k/hyperparameters tuned on all data (disclosed); bias is upward; nested CV
   would push AUCs toward 0.5 and reinforce the conclusion.
3. **Patient in train+test:** only in the *full* set, which is exploratory/appendix; the independent
   one-per-patient set is leakage-free and is primary; leaky full-set AUC (0.564) is even lower.
4. **Reproduce extraction:** honest — features extracted when all 137 present; migration lost raw
   images for 3 studies (34_02/40_02/41_03) so a clean re-run gives 134; a data-transfer gap, not an
   analysis error; conclusion unchanged.
5. **No FDR on clinical:** deliberate — to replicate Bassaganyas' per-feature uncorrected analysis
   like-for-like; stated in Methods; the radiomics hypothesis tests all use FDR.
6. **No texture signature:** not "physically impossible" — "not detectable in B-mode texture at
   clinical resolution here." The physics (macroscopic boundaries vs microscopic pathology) explains it.
7. **Six months:** commit to one — e.g. a multi-parametric model fusing B-mode with ARFI/DCE-US (since
   the signal lives in stiffness/perfusion), or deep learning on raw images, or external validation.

## Quiz 7 — Rapid-fire

1. 0.636, CI [0.48, 0.78].
2. p < 0.001, r = 0.72.
3. p = 0.86.
4. Full: 137 studies / 55 patients. Independent: 55 / 55.
5. 98 : 39 (~72:28).
6. 93 features — First-order, GLCM, GLRLM, GLSZM, GLDM, NGTDM.
7. 25 (PyRadiomics default).
8. ~2.7× (≈0.11–0.29 mm).
9. Piella, González Ballester, Papadiamantis; 16 July 2026.
10. The copy sent to the committee ~1 week before the defense.
