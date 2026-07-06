# Practice Quizzes

Questions only — answers with explanations are in `quiz_answers.md`. Write or say your answer, then
check. Each quiz mixes **recall**, **reasoning**, and **defend-the-choice** questions. Don't peek.

---

## Quiz 1 — Big picture & clinical (M0–M1)

1. Give the 60-second pitch of your thesis (aim for 6 beats).
2. Why is biopsy inadequate as a routine screening tool? Give three reasons.
3. What does ARFI physically measure, and how does rejection change it?
4. What does DCE-US physically measure, and how does rejection change it?
5. Explain what a B-mode image is made of, physically (what produces the echoes?).
6. Why is the 90-day cutoff used, and what happens to the ARFI signal before vs after it?
7. (Defend) A committee member says "this is just a failed experiment." Respond in 3 sentences.

## Quiz 2 — Radiomics & pipeline (M2)

1. List the preprocessing steps in order, with the two kernel sizes.
2. Why must the white contour be removed before feature extraction?
3. Name the six PyRadiomics feature classes and their counts (they sum to 93).
4. In one line each, what do GLCM, GLRLM, and NGTDM capture?
5. (Defend) Why did you disable shape features?
6. (Defend) Why per-image z-score normalisation rather than raw intensities?
7. What do the three alternative feature families rule out, and why is that convincing?
8. (Reasoning) You didn't resample to physical pixel spacing. Why does this *not* invalidate the
   negative result?

## Quiz 3 — ML & statistics (M3)

1. State the dataset numbers: total studies, patients, class split, dual-outcome patients.
2. Explain the independence problem in both its statistical and ML forms.
3. How is the independent dataset constructed, and why is it the primary analysis?
4. Describe the Shapiro → Welch/Mann-Whitney decision rule.
5. What does FDR control, and why is it needed when testing 93 features?
6. Walk the ML pipeline stages and say which are refit inside each CV fold.
7. Why is class_weight="balanced" used?
8. (Reasoning) What does it mean that all four AUC confidence intervals include 0.5?
9. (Defend) A reviewer says your correlation pre-filter leaks label information. Concede and defend.

## Quiz 4 — Results (M4)

1. How many radiomics features were nominally significant on the independent dataset, and how many
   survived FDR?
2. State the best ML model, its AUC, and its confidence interval.
3. What happened with the SVM, and why is that consistent with the conclusion?
4. State the late-period ARFI result (p and effect size) and why it's called the positive control.
5. (Reasoning) The clinical features are non-significant on the independent dataset. Reconcile this
   with the significant late-period result.
6. State the paired clinical ARFI p-value and explain what it implies about the nature of the signal.
7. How close was your replication of Bassaganyas, and what was the one discrepancy?

## Quiz 5 — Narrative & interpretation (M5)

1. Give the physical explanation for the negative result in under a minute.
2. Why do ARFI and DCE-US succeed where B-mode texture fails? (physics)
3. Explain the between-patient vs within-patient ARFI insight, including the caveat.
4. Give three distinct reasons a negative result is valuable here.
5. Why does radiomics work on ultrasound for liver/thyroid/breast but not pancreas rejection?

## Quiz 6 — Defence under pressure (M6)

1. Deliver your master framing (the "every bias is upward" line) verbatim-ish.
2. "Your CV isn't truly nested." Respond.
3. "Same patient appeared in train and test." Respond.
4. "Can you reproduce your feature extraction exactly?" Respond honestly.
5. "You didn't FDR-correct the clinical tests." Respond.
6. "Why should we believe rejection has no texture signature at all?" Respond.
7. "If you had six more months, what's the single most valuable thing you'd do?" Respond.

## Quiz 7 — Rapid-fire recall (mixed)

1. Best radiomics AUC + CI?
2. ARFI late-period p-value and effect size?
3. Paired ARFI p-value?
4. How many studies / patients (full and independent)?
5. Class split (no-rejection : rejection)?
6. Number of radiomics features and their six classes?
7. Bin width used?
8. How much does pixel spacing vary across the cohort?
9. Committee members and defense date?
10. Which dataset version gets graded?
