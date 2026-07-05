# Thesis Review — Findings Report

**Reviewed:** `thesis/*.tex` (abstract, introduction, methods, results, discussion, appendix)
**Date:** 2026-07-05
**Method:** Section-by-section scientific-writing review. Every quantitative claim
was cross-checked against the underlying analysis outputs in `analysis/reports/`
(the thesis uses the **`_normalised`** CSV variants as its canonical source — this
was confirmed by exact matches throughout). Priorities: technical/scientific
errors, AI-sounding / awkward writing, structure & clarity.

**Nothing in `thesis/` has been changed.** This report only flags and explains.
After you review, we decide together what to fix.

---

## Executive summary

The thesis is in strong shape. The numbers are **remarkably accurate** — the vast
majority of p-values, effect sizes, AUCs, confidence intervals, and sample counts
match the analysis outputs to three decimal places. The methodology (independent
dataset as primary, positive-control replication, multiple robustness analyses) is
sound and the negative result is honestly and rigorously argued. Several apparent
discrepancies I chased turned out to be non-issues (see "Resolved / non-issues").

That said, there are **two findings worth fixing before Gemma sees it**, plus a
handful of smaller consistency and writing items.

### Severity counts
| Severity | Count |
|---|---|
| Critical (breaks a conclusion) | 0 |
| Major (factual error / misleading comparison) | 2 |
| Moderate (consistency / methodology nuance) | 4 |
| Minor (writing, cosmetics) | 7 |
| Claims to verify against cited sources | 1 group |

### Must-fix (Major)
1. **Abstract calls the 39 rejection studies "biopsy-confirmed" — they are not.**
   Only **27 of the 39** rejection studies are biopsy-confirmed (verified from
   `biopsy_confirmed_rejection` in the merged data); the analysis outcome is the
   *clinical* rejection label (`RECHAZO CLÍNICO`), exactly as Methods §2.1 states.
2. **§3.7.1 compares full-dataset (n=137) surrounding-tissue results against
   independent-dataset (n=55) standard results.** The "24 uncorrected hits" and
   "AUC 0.636" it is compared against are from the independent dataset, while the
   surrounding-tissue analysis is on the full dataset. Not like-for-like.

---

## Chapter 1 — Abstract

| # | Loc | Severity | Category | Finding | Suggested fix |
|---|---|---|---|---|---|
| A1 | abstract.tex:8 | **Major** | Technical/accuracy | "137 ultrasound studies from 55 patients (**39 with biopsy-confirmed rejection**)". Verified: only **27/39** rejection studies are biopsy-confirmed; 12 are clinical-only. The analysis label is clinical rejection (`RECHAZO CLÍNICO`), which Methods §2.1 correctly describes as "clinical assessment and, where available, biopsy confirmation." Intro §1.1 itself notes biopsy is *not* routine. So "biopsy-confirmed" is an overclaim that contradicts the rest of the thesis. | Change to "39 rejection studies" (or "39 studies with clinically diagnosed rejection"). If you want to mention biopsy, say "27 of which were biopsy-confirmed." |
| A2 | abstract.tex:8 | Moderate | Consistency | "**39** with … rejection" is grammatically attached to the **patient** count (55 patients), but 39 is the number of rejection **studies**. Patient-level, only **21** patients ever had a rejection study. | Reword so the reader can't read 39 as a patient count, e.g. "137 studies (39 rejection) from 55 patients." |
| A3 | abstract.tex:12 | Minor | AI-writing | Closing tricolon "deep learning approaches, multi-parametric imaging models, and larger multi-centre cohorts" is a mild AI-cadence tell but acceptable in an abstract. | Optional: leave as-is. |

All other abstract numbers verified correct: best AUC **0.636 [0.48, 0.78]** ✓;
ARFI late-period **p<0.001, r=0.72** ✓; "matching … to three decimal places" ✓.

---

## Chapter 1 — Introduction

| # | Loc | Severity | Category | Finding | Suggested fix |
|---|---|---|---|---|---|
| I1 | introduction.tex:23 | Verify | Technical | "affecting approximately **20%** of grafts within the first year" [niederhaus2013, white2009] — plausible but I cannot verify without the sources. | Confirm the figure and that both citations support it. |
| I2 | introduction.tex:23 | Verify | Technical | "Rejection remains the **leading cause** of graft failure beyond the first 90 days." Strong claim. | Confirm against citation. |
| I3 | introduction.tex:35 | Verify | Technical | "combined score achieved an **odds ratio of 23.2**"; §1.2.2 ARFI "1.46 vs 0.97 m/s" — the ARFI figures match your own late-period result, good; the OR 23.2 is from Bassaganyas. | Confirm OR 23.2 against the paper. |
| I4 | introduction.tex:43 | Verify | Technical | "only **27.6%** of radiomics features were reproducible" [soleymani2022]; "IBSI … standardised **169** features" [zwanenburg2020]. | Confirm both figures against sources. |
| I5 | introduction.tex:15 & 39 | Minor | AI-writing | "The **key premise** is that…" (§1.1) and "The **fundamental premise** is that…" (§1.2.3) are near-identical constructions close together. | Vary one of them. |
| I6 | introduction.tex:47–55 (§1.2.4) | Moderate | Structure / AI-writing | The "Machine Learning for Medical Image Classification" subsection reads as generic textbook background ("Several challenges are characteristic… First… Second… Third…") with little tie to *this* study until the last sentence. It is the most AI/filler-sounding passage in the thesis. | Tighten to the points you actually use (small-n/high-dim, class imbalance, CV choice) and cut the generic scaffolding, or explicitly connect each challenge to a design choice you made. |

---

## Chapter 2 — Methods

| # | Loc | Severity | Category | Finding | Suggested fix |
|---|---|---|---|---|---|
| M1 | methods.tex:48, Table 2.2 (:65) | Moderate | Numeric | Class ratio stated as "**71:29**". 98:39 = 71.5 : 28.5, which rounds to **72:28** (or state 71.5:28.5). "71:29" rounds one side and not the other. | Use "72:28" or "71.5:28.5" consistently in §2.1 and Table 2.2. |
| M2 | methods.tex:39, Table 2.1 | Minor | Completeness | The DCE-US feature "**Area**" has an em-dash "—" for its full name while every other feature is named. | Give it a name (e.g. "Area under time-intensity curve") or a footnote. |
| M3 | methods.tex:171 / §2.5.1 | Moderate | Technical / methodology | The correlation pre-filter (93→27) drops the higher-*p* member of each correlated pair using p-values computed on the **whole dataset**, and is applied **once, outside** the cross-validation loop (only StandardScaler + SelectKBest are re-fit inside folds, per §2.5.2). This is a mild information-leakage path. **It does not threaten your conclusions** — leakage can only *inflate* performance, and performance is already at chance — but a careful examiner may raise it. | Either (a) add one sentence acknowledging the pre-filter is outside CV and note it can only bias *upward*, so the null result is conservative; or (b) if quick, move the filter inside the fold as a sensitivity check. Option (a) is sufficient. |

Methods is otherwise excellent — specific, correct, and well-motivated. Verified:
independent-dataset construction, 45 t-test / 48 M-W split (§3.2), 93→27 reduction
(both full and independent datasets genuinely reduce to 27), 10-fold (independent)
vs 5-fold (full), and every configuration value against Appendix C.

---

## Chapter 3 — Results

| # | Loc | Severity | Category | Finding | Suggested fix |
|---|---|---|---|---|---|
| R1 | results.tex:316–318 (§3.7.1) | **Major** | Technical / consistency | The surrounding-tissue **normalised radiomics** analysis is run on the **full dataset (n=137)** (0 uncorrected hits; ML AUC 0.525), but the text compares it to "the standard per-image normalised analysis (which yielded **24 uncorrected hits on the independent dataset**)" and "below the standard analysis result (**AUC = 0.636**)". Both comparators are **independent-dataset (n=55)** figures. This is not a like-for-like comparison. The correct full-dataset baseline is Appendix A: **4** uncorrected hits and best AUC **0.564**. The conclusion ("normalisation didn't help") still holds under the correct comparison — only the cited numbers are mismatched. | Compare to the full-dataset standard results (App. A: 4 hits, AUC 0.564), **or** re-run the surrounding-tissue analysis on the independent dataset, **or** add an explicit caveat that the surrounding analysis is full-dataset-only and the standard figures quoted are independent-dataset. |
| R2 | results.tex:23 (§3.2) | Minor | Consistency | Body gives `firstorder_90Percentile` "rank-biserial **r = −0.47**", but the value is −0.465 and Appendix B Table lists **−0.46**. | Use −0.46 in both places (matches the data). |
| R3 | results.tex (§3.3.3) | Low | Judgement | The RT replication discrepancy (ours 0.142 vs Bassaganyas 0.276) explanation is speculative ("most likely … values were updated … RT most sensitive to curve-fitting"). It is honestly flagged as a hypothesis and both are non-significant, so it does not affect conclusions. | Fine as written; optionally soften "The most likely explanation" to "A possible explanation." |

Everything else in Results was cross-checked and matches the analysis outputs:
- §3.2 independent radiomics (top features, 24 nominal, min FDR 0.16) ✓
- §3.2.1 stratified early (`RMS` p=0.044) / late (`Maximum` p=0.038) ✓
- §3.3.1 clinical full (Table 3.3, all 17 rows) ✓
- §3.3.2 clinical late (Table 3.4, 8 sig, ARFI p<0.001) ✓
- §3.3.3 replication (Table 3.5, days-split vs Bassaganyas; motivo WiPi=0.066) ✓
- §3.3.4 clinical independent (Table 3.6, all 17 rows, min p RT=0.060) ✓
- §3.4 ML independent (Table 3.5: AUCs, CIs, sens/spec, SVM collapse) ✓
- §3.5 paired radiomics (8 features, `ngtdm_Coarseness` top) & clinical (ARFI 0.86/0.91) ✓; pair gaps median 2 (range 1–5) ✓
- §3.6 alternative features (full: 5 hits; independent: 7 hits, Laws 5/7; per-family & ML AUCs) ✓
- §3.7.2 contrast features (`contrast_p25_diff` p=0.10; NB AUC 0.549) ✓

---

## Chapter 4 — Discussion & Conclusions

| # | Loc | Severity | Category | Finding | Suggested fix |
|---|---|---|---|---|---|
| D1 | discussion.tex:20 (§4.1.2) & results.tex:116 (§3.3.3) | Minor | AI-writing / repetition | The construction "**serves two purposes / an important dual purpose. First… Second…**" appears in *both* the Results replication section and the Discussion. Near-verbatim reuse is a noticeable AI-style tell. | Reword one instance. |
| D2 | discussion.tex:10 (§4.1.1) | Verify | Technical | "spatial resolution of clinical B-mode imaging, which is typically **0.5–2 mm axially**." Plausible for abdominal US but worth a citation. | Add a citation or soften to "on the order of a millimetre." |
| D3 | discussion.tex:38 (§4.1.4) & §4.4 | Minor | AI-writing | A few generic/grandiose phrases ("narrows the search space", "valuable for directing research resources toward more promising directions"). | Optional trims; content is fine. |

Structure/logic verified as sound: the five Conclusions map cleanly to the five
Objectives; the central between-patient-vs-within-patient ARFI argument is
well-reasoned and appropriately hedged with the underpowered-alternative
interpretation; "8 of 17 clinical features" and "r=0.72" match the data.

- **Limitations §4.2 item 1** repeats the "137 studies from 55 patients (**39 with
  rejection**)" phrasing — same studies-vs-patients ambiguity as A2 (here at least
  it says "with rejection", not "biopsy-confirmed"). Consider harmonising wording
  with the abstract fix.

---

## Appendices & typesetting (Chapter 5 of review)

| # | Loc | Severity | Category | Finding | Suggested fix |
|---|---|---|---|---|---|
| P1 | build (`MasterThesis.log`) | Minor | Typesetting | **26 overfull hboxes**; worst is **109 pt** (App. A motivo feature list) and 60 pt (§3.2). Cause: long monospaced feature names (`firstorder_90Percentile`, `glszm_SizeZoneNonUniformity`) that don't line-break, running into the margin. | Allow breaks in `\texttt{}` (e.g. the `seqsplit` package, or insert `\allowbreak` after underscores, or `\sloppy` in those paragraphs). |
| P2 | build | Nit | Typesetting | Repeated pdfTeX "destination with the same identifier (name{page.})" warnings — from `\pagenumbering{gobble}` in the preface. Cosmetic, does not affect output. | Ignore, or set distinct page numbering for front matter. |

Cross-references and citations: **no undefined references or citations** — clean.
App. A (ML full, 5-fold 0.52–0.60), App. B (full 93-feature table top rows), and
App. C (bin-width→~24 bins arithmetic) all verified against the data.

---

## Global AI-writing / phrasing pass

Overall the prose is **specific and grounded** — it does not read as strongly
AI-generated. The recurring tics to watch, aggregated:

1. **Verbatim repetition of stock phrases.** "gain, depth, and probe pressure"
   appears ~3× (methods §2.3, App. C, limitations §4.2) — vary or cross-reference.
   "serves two/dual purpose(s), First… Second…" appears twice (D1). "rules out X as
   the explanation" is used three times (within-patient correlation / acquisition
   variability / wrong features) — rhetorically effective but noticeably patterned.
2. **Tricolon lists** ("inflammation, oedema, and fibrosis"; "texture, intensity,
   and spatial heterogeneity") are frequent. A couple are fine; several in a row
   read as AI cadence.
3. **Generic scaffolding** in §1.2.4 (see I6) — the clearest filler passage.
4. **"premise" twice** in similar framing (I5).

None of these are errors; they are polish items for the "sounds a bit AI" concern.

---

## Resolved / non-issues (checked, no action needed)

These looked like discrepancies but the thesis is **correct**:
- **SVM `k=27`** (Table 3.5) vs raw data `best_k=31`: the notebook's `k_values`
  includes 31 but only 27 features exist, so `SelectKBest` caps k at 27. Thesis's 27
  is the correct effective value.
- **NaiveBayes `k=27`** (App. A) vs raw `best_k=32`: same capping (full set = 27).
- **"93→27" reduction**: confirmed by notebook output for *both* full and
  independent datasets.
- **Non-normalised CSVs** (e.g. `19_stats_independent_dataset.csv`) do **not** match
  the thesis — but the **`_normalised`** variants match exactly. The thesis is
  consistently built on the normalised pipeline (as intended).
- **Table 3.8 Laws' `p<0.05 = 5`**: correct pooled count (matches the §3.6.1 text
  "5 of 7"). Note: the source file `22_per_family_results.csv` reports **8** for
  Laws — that CSV value is an internal analysis-output artifact; the thesis number
  is the right one. (Flagged only so it doesn't surprise you if someone opens that
  CSV.)

---

## Numbers reconciliation appendix (thesis vs source CSV)

| Thesis location | Claim | Source (`analysis/reports/…`) | Status |
|---|---|---|---|
| Abstract / §3.4 | best AUC 0.636 [0.48,0.78] | `20_bootstrap_ci_normalised.csv` (0.636, 0.477, 0.775) | ✔ |
| §3.2 | `firstorder_90Percentile` p=0.004, r (−0.47 body / −0.46 app) | `19_stats_independent_dataset_normalised.csv` (0.00414, −0.465) | ✔ (see R2) |
| §3.2 | 24 nominal sig; 45 t / 48 M-W; min FDR 0.16 | same | ✔ |
| §3.2.1 | early `RMS` 0.044; late `Maximum` 0.038 | `25_..._early/late.csv` | ✔ |
| §3.3.1 | clinical full, ARFI mediana 0.028 / media 0.029 | `14b_stats_clinical_features.csv` | ✔ (all 17) |
| §3.3.2 | late 8 sig; ARFI media 0.97/1.44, r=0.74 | 14b notebook late subset (n=58: 36/22) | ✔ |
| §3.3.3 | replication days-split (0.008/0.019/0.020/0.044…); motivo WiPi 0.066 | 14b comparison | ✔ |
| §3.3.4 | clinical independent, min p RT=0.060 | `24_clinical_stats_independent.csv` | ✔ (all 17) |
| §3.4 | ML independent AUC/CI/sens/spec; SVM 0.408 | `20_ml_independent_dataset_results_normalised.csv` | ✔ |
| §3.5.1 | 14 pairs, gap median 2 (1–5) | `21_selected_pairs_normalised.csv` | ✔ |
| §3.5.2 | 8 paired radiomics <0.05, `ngtdm_Coarseness` top, FDR 0.49 | `21_paired_analysis_radiomics_normalised.csv` | ✔ |
| §3.5.3 | paired clinical: ARFI 0.86/0.91/0.73/0.85; WoR 0.16 | `21_paired_analysis_clinical_normalised.csv` | ✔ |
| §3.6 | full 5 hits / indep 7 hits (Laws 5/7); per-family & ML AUCs | `22_*` | ✔ (per-family Laws count caveat above) |
| §3.7.1 | normalised radiomics 0 hits (full); ML 0.525 | `23_stats_normalized.csv`, `23_ml_results.csv` | ✔ (but comparator mismatch — R1) |
| §3.7.2 | contrast `p25_diff` 0.10; NB 0.549 | `23_stats_contrast.csv`, `23_ml_results.csv` | ✔ |
| App. A | full radiomics 4 hits; 22 t/71 M-W; min FDR 0.80 | `14a_stats_radiomics_features_normalised.csv` | ✔ |
| App. A | ML full LOOCV (LR .535 / RF .564 / SVM .417 / NB .533) | `17b_joint_optimization_results_normalised.csv` | ✔ |
| Data | 39 rejection **studies**, 21 rejection **patients**, 27/39 biopsy-confirmed | `13_merged_..._normalised.csv` | drives A1/A2 |

---

## Suggested next step

The two Major items (A1 biopsy-confirmed wording; R1 dataset-mismatch comparison)
are the only substantive fixes. Both are small text edits (A1) or a small
numbers/caveat change (R1). Everything else is polish. Tell me which findings you
want to act on and I'll draft the exact `.tex` edits for your approval before
applying anything.
