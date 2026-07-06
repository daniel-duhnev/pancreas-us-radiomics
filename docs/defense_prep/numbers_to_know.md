# Numbers To Know Cold

One page. If you can recite this from memory, you're safe on facts. Every number is from your thesis
/ committed reports.

## Dataset
- **56 patients → 55** (after excluding 47_01, whose images were never recovered).
- **138 studies → 137** (radiomics); **138** used for clinical replication (47_01 had clinical data).
- Outcome split (137): **98 no-rejection : 39 rejection** ≈ **72:28**.
- **2.5** studies/patient on average (range **1–6**).
- **14** patients have **both** outcomes (drives the repeated-measures problem).
- **Independent dataset: 55 studies** (one per patient), **34 NR : 21 R**.
- Collection **Oct 2016 – Feb 2020**, **Siemens Acuson S3000 Helx** scanner, Hospital Clínic Barcelona.

## Features
- **93 radiomics features** = First-order 18 · GLCM 24 · GLRLM 16 · GLSZM 16 · GLDM 14 · NGTDM 5.
- Shape features **disabled**. **force2D**. Per-image **z-score** normalise (×100, 3σ clip).
  Bin width **25** (default). **No resampling** (pixel spacing varies **~2.7× , ≈0.11–0.29 mm**).
- **316** feature pairs with |r| > 0.9. Correlation filter → **~27** features (thesis; code shows 31).
- **17 clinical features** = **4 ARFI** (stiffness) + **13 DCE-US** (perfusion).
- Alternative textures: **153** = LBP 54 + Gabor 54 + Laws' 45.

## Radiomics results (independent, n=55) — the negative core
- **24 of 93** features nominal p < 0.05; **0 survive FDR** (all adjusted p **≥ 0.16**).
- Top hit: `firstorder_90Percentile` **p = 0.004** (r = −0.46). 19/24 lower in rejection.
- **ML best AUC = 0.636, 95% CI [0.48, 0.78]** (Logistic Regression, k=10). CI includes 0.5.
  - RF 0.588 [0.43, 0.75]; **SVM 0.408** (collapsed, spec 0.029); NB 0.618 [0.45, 0.78].
- Full-dataset ML (exploratory, appendix, leaky): best AUC **0.564**.

## Clinical replication (positive control) — the credibility core
- Full dataset (n=138): only **ARFI mediana p = 0.028**, **ARFI media p = 0.029** significant.
- **Late period (>90 d, n=58): 8 of 17 significant.**
  - **ARFI media p < 0.001 (r = 0.74)**, **ARFI mediana p < 0.001 (r = 0.72)**, ARFI DE p<0.001,
    ARFI RIQ p=0.004; plus DCE-US WiAUC 0.008, WoAUC 0.019, WiWoAUC 0.020, WiPi 0.044.
  - Median shear-wave velocity **0.97 (NR) vs ~1.44–1.46 (R)** m/s.
- **Replication vs Bassaganyas: 10 of 12 features match to 3 decimals.** Only RT differs (0.142 vs
  0.276, both non-significant).
- Clinical features on **independent** set (n=55): **none significant** (ARFI mediana p = 0.69) —
  because only **7 of 21** rejection studies fall in the late window; pooling dilutes the effect.

## Paired analysis (14 patients, both outcomes)
- Radiomics: 8/93 nominal, lowest `ngtdm_Coarseness` p=0.017; **all FDR = 0.49** (none survive).
- **Clinical: none significant. ARFI mediana p = 0.86**, media 0.91 — the between-vs-within insight.

## Robustness checks (all null)
- Alternative textures (153): full set 5 nominal (< the 7.7 expected by chance); independent 7
  nominal (mostly Laws'); **none survive FDR**. Best family AUC: Laws' 0.651 [0.50, 0.80].
- Surrounding-tissue normalisation: none significant (closest p=0.057); ML AUC 0.525. Contrast
  features (11): none significant; ML AUC 0.549.

## The four you can never miss
1. **0.636, CI [0.48, 0.78]** — best radiomics AUC, includes chance.
2. **24 nominal → 0 after FDR** — the radiomics null.
3. **ARFI late p < 0.001, r = 0.72** — the positive control.
4. **Paired ARFI p = 0.86** — between-patient, not within-patient.

## Logistics
- **16 July 2026, 09:00, room 55.309.** Committee: Piella (supervisor), González Ballester,
  Papadiamantis. **20–25 min talk + 15–20 min Q per member.** Report to committee ~1 week prior.
