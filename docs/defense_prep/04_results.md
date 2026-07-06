# M4 · Results You Must Know Cold

Goal: recall every headline number and, more importantly, say **what it means**. Numbers here are
taken directly from your thesis results chapter and the committed report CSVs. The condensed version
is in `numbers_to_know.md` — this file explains each in context.

Read each result as: **number → what it means → why it supports the conclusion.**

---

## 1. Feature extraction

- **93 features** extracted from **all 137 studies**, **zero failures**. (18 first-order, 24 GLCM,
  16 GLRLM, 16 GLSZM, 14 GLDM, 5 NGTDM.)
- **316 feature pairs** had |correlation| > 0.9 → heavy redundancy → motivates the correlation
  filter before ML.

## 2. Radiomics univariate — the independent dataset (PRIMARY, n=55: 34 NR / 21 R)

- Test split: **45 features → Welch's t-test, 48 → Mann-Whitney** (from Shapiro-Wilk).
- **24 of 93 features reached nominal p < 0.05** (26%), mostly first-order (7 of the 24).
  - Top hits: `firstorder_90Percentile` (**p = 0.004**, r = −0.46), `firstorder_RootMeanSquared`
    (p = 0.005, r = −0.46), `firstorder_Mean` (p = 0.005, r = −0.45).
  - In **19 of 24**, rejection had *lower* values (weak trend toward lower intensity in rejection).
- **None survived FDR correction — all adjusted p ≥ 0.16.** ← **the statistical core of the thesis.**
- **Meaning:** even with each patient contributing exactly one independent observation, no feature
  significantly discriminates rejection after correcting for multiple testing. 24/93 nominal hits is
  only modestly above the ~5% expected by chance given the feature correlation structure.

## 3. Time-stratified radiomics (independent dataset) — robustness check

- Early (≤90 d, **n=42**: 28 NR/14 R): one nominal hit (`firstorder_RootMeanSquared`, p = 0.044).
- Late (>90 d, **n=13**: 6 NR/7 R): one nominal hit (`firstorder_Maximum`, p = 0.038).
- **Neither survives FDR** (min adjusted p = 0.61 early, 0.34 late); the two hits are *different*
  features → chance, not a consistent time-dependent signal. Late group (n=13) is underpowered.

## 4. Radiomics ML — the independent dataset (PRIMARY, n=55)

Correlation filter reduced 93 → **27 features** (thesis figure; committed code shows 31 — see M6).
Primary metric: **10-fold stratified CV AUC**; LOOCV as secondary; bootstrap 95% CI (1000 resamples).

| Model | k | AUC (10-fold) | 95% CI | AUC (LOOCV) | Sens | Spec |
|-------|--:|--------------:|--------|------------:|-----:|-----:|
| **Logistic Regression** | 10 | **0.636** | **[0.48, 0.78]** | 0.609 | 0.714 | 0.559 |
| Random Forest | 10 | 0.588 | [0.43, 0.75] | 0.618 | 0.238 | 0.971 |
| SVM | 27 | 0.408 | [0.25, 0.58] | — | 1.000 | 0.029 |
| Naive Bayes | 15 | 0.618 | [0.45, 0.78] | 0.592 | 0.571 | 0.765 |

- **Best model = Logistic Regression, AUC 0.636, but CI [0.48, 0.78] includes 0.5** → not
  distinguishable from chance.
- **SVM collapsed** (AUC 0.408, sensitivity 1.0, specificity 0.029): it predicted almost everything
  as rejection — a classic sign of an unstable model on a small, imbalanced set. Mention this as
  evidence there's no stable signal for it to latch onto.
- **All four CIs span 0.5.** The weak univariate trend (§2) does **not** translate into useful
  multivariate prediction.
- Full-dataset ML (exploratory, appendix, LOOCV with patient leakage): best AUC **0.564** — also at
  chance, and *lower* than the leakage-free 0.636, which is reassuring rather than worrying.

## 5. Clinical replication — the POSITIVE CONTROL (this is your credibility)

### Full dataset (n=138: 98 NR / 40 R), Mann-Whitney throughout
- Only **2 significant**: `ARFI mediana` (p = 0.028, r = 0.26; median 1.255 NR vs 1.470 R) and
  `ARFI media` (p = 0.029). Rejection = **stiffer** graft. No DCE-US significant on the full set —
  consistent with Bassaganyas (perfusion differences emerge only late).

### Late period (>90 d, n=58: 36 NR / 22 R) — the signal appears
- **8 of 17 features significant:**
  - All four ARFI: `ARFI media` **p < 0.001 (r = 0.74)**, `ARFI mediana` **p < 0.001 (r = 0.72)**,
    `ARFI DE` p < 0.001 (r = 0.57), `ARFI RIQ` p = 0.004 (r = 0.49). Median velocity **0.97 (NR) vs
    ~1.44–1.46 (R)** → clearly stiffer in rejection.
  - Four DCE-US perfusion params: WiAUC (0.008), WoAUC (0.019), WiWoAUC (0.020), WiPi (0.044) — all
    showing **lower perfusion** in rejection.
- Early period (≤90 d, n=80): **no significant features** — post-op noise masks the signal, exactly
  as clinically expected.

### The replication itself (Table: ours vs Bassaganyas)
- For the 12 features they reported, **our late-period p-values match theirs to 3 decimal places for
  10 of 12.** ARFI mediana "< 0.001" in both.
- **Only discrepancy: RT (rise time)** — ours 0.142 vs their 0.276, **both non-significant**, so it
  changes nothing. Likely explanation: RT is computed from the initial slope of the time-intensity
  curve and is the DCE-US parameter most sensitive to curve-fitting; the database values were likely
  updated between their export and yours. Integral/peak measures (more fit-robust) match exactly.
- **Why this matters (say it):** the replication (a) validates the whole pipeline — data loading,
  grouping, testing — and (b) proves the negative radiomics result is *not* a broken-pipeline
  artifact. Same machinery detects the clinical signal when it exists.

### Clinical features on the independent dataset (n=55; ARFI 47, DCE 54)
- **No clinical feature significant, even uncorrected.** ARFI mediana p = 0.69, ARFI media p = 0.77.
  Smallest p across all 17 = 0.060 (RT).
- **This does NOT contradict the positive result.** The independent set pools all time periods and,
  for dual-outcome patients, prefers the *first* rejection study (often early). Only **7 of the 21**
  rejection studies fall in the late (>90 d) window where ARFI discriminates. Pooling early + late
  dilutes the ARFI effect. Consistent with the paired analysis (§7).

## 6. Paired within-patient analysis (14 patients with both outcomes)

- **Radiomics:** 8 of 93 nominal hits (Wilcoxon signed-rank), lowest `ngtdm_Coarseness` p = 0.017;
  **all FDR-adjusted p = 0.49** → none survive. And the nominal hits are *different* features than in
  the unpaired analyses → instability confirms "no reproducible signal."
- **Clinical (the striking one):** **no feature significant.** ARFI features that were p < 0.001 in
  the unpaired late analysis are now: ARFI mediana **p = 0.86**, ARFI media 0.91, ARFI DE 0.73, ARFI
  RIQ 0.85. Best clinical feature WoR p = 0.16.
- **Interpretation (important, see M5):** when each patient is their own control, the ARFI difference
  **vanishes** (p < 0.001 → p = 0.86). This suggests ARFI reflects **stable between-patient
  differences** in baseline stiffness, not a transient within-patient change caused by an acute
  rejection episode. Caveat: only 14 pairs (12 with ARFI) → could also be underpowered. Present it as
  hypothesis-generating.

## 7. Alternative texture families (153 features) — robustness

- **Full dataset (137):** 5/153 nominal (3 LBP, 2 Gabor), min q = 0.60. Under the null you'd *expect*
  ~7.7 hits (153 × 0.05); observing 5 is **below chance expectation**.
- **Independent (55):** 7/153 nominal, mostly Laws' (5 of 7), strongest `laws_L5W5_mean` p = 0.021;
  min q = 0.54. None survive FDR.
- **Per-family ML (independent):** LBP best AUC 0.527, Gabor 0.490, Laws' 0.651 [0.50, 0.80],
  combined 0.550 [0.40, 0.71] (k=5). Every CI includes 0.5.
- **Point:** three distinct feature philosophies, all null → not a "wrong features" problem.

## 8. Surrounding-tissue normalisation — robustness

- **Normalised radiomics (93, full dataset):** none significant; closest
  `gldm_SmallDependenceLowGrayLevelEmphasis` p = 0.057; all q > 0.78. Best ML (LogReg, k=20) AUC 0.525.
  *Slightly worse* than un-normalised → normalisation removed rather than revealed signal.
- **Contrast features (11):** none significant; strongest `contrast_p25_diff` p = 0.10, q = 0.40.
  Best ML (Naive Bayes, k=6) AUC 0.549.
- **Point:** if acquisition variability were masking a signal, local normalisation should have helped.
  It didn't → the null is genuine, not an acquisition artifact.

---

## The four numbers you can never get wrong

1. **Best radiomics AUC = 0.636, 95% CI [0.48, 0.78]** (includes chance). Logistic Regression.
2. **Radiomics: 24 nominal hits, 0 survive FDR** (all adjusted p ≥ 0.16).
3. **ARFI late period: p < 0.001, effect size r = 0.72** (mediana) — the positive control.
4. **Paired ARFI: p = 0.86** — the between- vs within-patient insight.

If you blank on everything else, hold onto these four.

---

## Quick self-check

- Recite the ML table (at least LogReg 0.636 [0.48,0.78] and the SVM collapse).
- Explain why 24 nominal but 0 after FDR is the *expected* null pattern.
- State the ARFI late-period result and why it's the positive control.
- Explain why clinical features are null on the independent set without contradicting the positive
  result.
- Explain the paired ARFI p = 0.86 result and what it implies.
