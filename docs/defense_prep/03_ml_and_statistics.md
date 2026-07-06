# M3 · ML & Statistics Methodology (from first principles)

Goal: explain your dataset structure, your statistical tests, and your ML pipeline — and defend the
design choices. This and M6 are where a methods-focused committee will spend most of their time.
**[THESIS]** marks thesis-specific facts.

---

## 1. The dataset (know these numbers cold)

**[THESIS]**
- **56 patients, 138 studies** originally. A "study" = one ultrasound examination session, ID
  format `XX_YY` (XX = patient, YY = visit).
- **One study excluded: 47_01** — the hospital confirmed its images were **never recovered** and
  can't be provided. It was a rejection case. → leaves **55 patients, 137 studies**.
- Outcome split: **98 no-rejection : 39 rejection** ≈ **72:28** class ratio (imbalanced).
- **2.5 studies per patient on average** (range 1–6).
- **14 patients have studies in *both* outcome classes** (rejection at one visit, no-rejection at
  another). This is the crux of the "repeated measures" problem.
- Outcome label = the binary clinical variable **RECHAZO CLÍNICO** (clinical rejection, 0/1),
  assigned by the clinical team from clinical assessment + biopsy where available.

**Numbers hook:** 56→55 patients, 138→137 studies (47_01 dropped), 98/39 split, 14 dual-outcome.

## 2. The independence problem (this is central — understand it deeply)

Standard statistical tests (t-test, Mann-Whitney) and standard cross-validation **assume every
observation is independent**. Your data violates this: the same patient contributes multiple
studies, and those studies are correlated (same anatomy, same scanner settings, same baseline
tissue). Two concrete harms:

- **In statistics:** repeated measures **inflate the effective sample size** → artificially small
  p-values → false positives.
- **In ML:** if the same patient appears in both training and test folds, the model can "recognise"
  the patient rather than learn rejection → **patient-level leakage** → inflated apparent
  performance.

### Your solution: the "independent dataset"

**[THESIS]** Build a subset with **exactly one study per patient**, so every observation is
independent:
- **n = 55** studies (one per patient), **34 no-rejection : 21 rejection**.
- **Construction rule:** for the 14 patients with both outcomes, pick their **first rejection**
  study (so the rejection group stays as populated as possible); for everyone else, the first
  available study.
- **This is the PRIMARY dataset** for all statistics and ML. The full 137-study dataset is reported
  **only as an exploratory supplement** (in the appendix) because it violates independence.

**Say this clearly in the defense:** "My primary analysis is the independent one-study-per-patient
dataset, which satisfies the independence assumption. The full dataset is exploratory only."

> **Nuance to be ready for (M6):** the selection rule is outcome-conditioned (it prefers rejection
> studies), and the "independent 55" is a *subsample of the same 137 patients*, not a truly external
> validation cohort. It's a repeated-measures control, not external validation. Know the distinction.

## 3. Univariate statistical testing (per feature)

**[THESIS]** For each of the 93 features, a two-step adaptive procedure:

1. **Normality check — Shapiro-Wilk test** on each group. Tests whether the data plausibly come
   from a normal distribution.
2. **Choose the test:**
   - If **both groups pass** normality (p > 0.05) → **Welch's t-test**.
   - Otherwise → **Mann-Whitney U test** (non-parametric, compares ranks/medians).
   - **[THESIS]** On the independent dataset: 45 features got Welch, 48 got Mann-Whitney.

**Why Welch's t-test (not Student's)?** Welch does **not assume equal variances** between groups —
it uses separate variance estimates and adjusts the degrees of freedom. This removes the need for a
separate variance-equality test and is safer when group sizes/variances differ (they do here:
34 vs 21).

**Effect sizes** (report magnitude, not just significance):
- Welch → **Cohen's d** (difference in means in standard-deviation units).
- Mann-Whitney → **rank-biserial correlation** (non-parametric effect size).

### Multiple testing and the FDR correction (understand this well)

**The problem:** testing 93 features at p < 0.05 each means ~5% will look "significant" by chance
alone (≈4–5 features) even if nothing is real. This is the **multiple comparisons problem**.

**The fix:** **Benjamini-Hochberg (BH) procedure**, which controls the **False Discovery Rate (FDR)**
— the expected *proportion of false positives among the features you call significant*. You rank
p-values and apply a graded threshold. A feature is "significant" only if its **FDR-adjusted p (q-value)
< 0.05**.

- FDR is **less conservative than Bonferroni** (which controls the chance of *any* false positive) —
  appropriate for screening many features.
- **[THESIS] Key result:** 24 features reached *nominal* p < 0.05 on the independent dataset, but
  **none survived FDR** (all adjusted p ≥ 0.16). That's the statistical heart of the negative result.

## 4. The machine learning pipeline

Univariate tests ask "does any *single* feature discriminate?" ML asks "does any *combination* do
better?" **[THESIS]** pipeline:

### Step 0 — correlation pre-filter
For each feature pair with **|Pearson r| > 0.9**, drop the one with the **higher (less significant)
p-value** from the univariate analysis. **[THESIS]** This reduced 93 → **27 features** (as reported
in the thesis).

> **Known discrepancy (be aware):** the committed code's reduced set on the normalised independent
> data was actually **31** features (the SVM used k=31 = "all features"), while the thesis text says
> 27. Both indicate heavy reduction and the conclusion is unchanged. If asked the exact count, say
> "the |r|>0.9 filter cuts the ~93 features down to about 30 — roughly a third — after removing the
> redundant pairs." Don't state a false precise number you can't back up. (See M6.)

### Step 1–3 — the scikit-learn Pipeline (jointly optimised)
Everything below is wrapped in **one `Pipeline`** and re-fitted **inside each CV fold** to prevent
leakage:
1. **StandardScaler** — z-score each feature, fitted on the **training fold only**.
2. **SelectKBest(f_classif)** — rank features by the **ANOVA F-statistic** (ratio of between-group to
   within-group variance) and keep the top **k**. Here **k is a hyperparameter**, tuned by the grid
   search. (F-stat used as a *ranking* measure, robust to moderate non-normality — not as a formal
   test.)
3. **Classifier** — one of four (below).

### The four classifiers (know why each was chosen)
**[THESIS]** chosen to span model families/assumptions:

| Model | Type | Key hyperparameters searched | Notes |
|-------|------|------------------------------|-------|
| **Logistic Regression** | linear, L2-regularised | C ∈ {0.01, 0.1, 1, 10} | interpretable; class_weight="balanced" |
| **Random Forest** | tree ensemble, non-linear | max_depth ∈ {3,5,7}, min_samples_leaf ∈ {3,5,10} | handles interactions; balanced |
| **SVM** | max-margin, kernel | kernel ∈ {linear, rbf}, C ∈ {0.1,1,10} | strong in high-D; balanced |
| **Gaussian Naive Bayes** | probabilistic | var_smoothing ∈ {1e-9,1e-7,1e-5} | assumes feature independence |

**class_weight="balanced"** counteracts the 72:28 imbalance by penalising minority-class (rejection)
errors more.

### Evaluation strategy
- **GridSearchCV with 5-fold stratified CV** picks hyperparameters, optimising **AUC**.
- Two generalisation estimates:
  - **LOOCV (leave-one-out):** hold out one study at a time. Nearly unbiased but **high variance**.
  - **Stratified k-fold:** keeps class ratio in each fold. **10 folds** for the independent dataset
    (primary), 5 folds for the larger full dataset.
- **[THESIS]** The **independent dataset gives the primary, leakage-free evaluation** — one study
  per patient means no patient spans train and test. Full-dataset LOOCV has patient-level leakage →
  exploratory only.

### Metrics
- **AUC (area under the ROC curve)** — primary. Threshold-independent, good for imbalance.
  AUC 0.5 = chance; 1.0 = perfect.
- **Sensitivity & specificity** at the **Youden's index** operating point (the threshold maximising
  sensitivity + specificity − 1).
- **Bootstrap 95% CI** — resample 1000 times to get a confidence interval on the AUC. **If the CI
  includes 0.5, performance is indistinguishable from chance.** This is your key interpretive tool.

## 5. The other analyses (know what each adds)

- **Time-stratified analysis.** Split by days post-transplant: **early ≤90 days** vs **late >90
  days**, matching Bassaganyas' cutoff. Tests whether a signal is concentrated in one period.
  **[THESIS]** independent-dataset late group is only **n=13** — underpowered, treated as a
  robustness check.
- **Paired within-patient analysis.** For the **14 patients with both outcomes**, form one
  rejection + one no-rejection pair each (maximise the visit gap so they're distinct episodes),
  compute the within-patient difference, and apply the **Wilcoxon signed-rank test** (the paired,
  non-parametric test). This is the cleanest control for between-patient confounding — each patient
  is their own control.
- **Clinical replication.** Apply the *same* stats machinery to the 17 clinical features to
  reproduce Bassaganyas (positive control). **[THESIS]** FDR was deliberately **not** applied here,
  because the goal was to *replicate their per-feature analysis*, not to make an independent claim —
  an intentional methodological choice, not an oversight. (See M6.)

## 6. Concepts a committee may ask you to define

Be ready to define each in one or two sentences:

- **AUC / ROC curve:** ROC plots true-positive rate vs false-positive rate across thresholds; AUC is
  the area under it = probability the model ranks a random positive above a random negative.
- **Sensitivity vs specificity:** sensitivity = of the true rejections, the fraction caught;
  specificity = of the true non-rejections, the fraction correctly cleared.
- **Cross-validation:** repeatedly train on part of the data and test on the held-out part, to
  estimate performance on unseen data.
- **Data leakage:** when information from the test set influences training (e.g. scaling on all data,
  or the same patient in train and test) → over-optimistic results.
- **Overfitting:** model learns noise specific to the training data; worsened by many features vs few
  samples (your 93 features / 55–137 samples is exactly this high-dimensional regime).
- **Class imbalance:** unequal group sizes bias models toward the majority; handled here with
  class_weight="balanced".
- **FDR / multiple comparisons:** correcting p-values because testing many features inflates false
  positives.
- **Effect size:** magnitude of a difference (Cohen's d, rank-biserial), independent of sample size —
  complements the p-value.
- **Bootstrap CI:** resample the data with replacement many times to estimate the uncertainty of a
  statistic.

---

## Quick self-check

- State the dataset numbers (55/137, 98/39, 14 dual-outcome) without looking.
- Explain the independence problem and how the independent dataset fixes it.
- Explain the Shapiro → Welch/Mann-Whitney decision and why Welch.
- Explain FDR and why 24 nominal hits but 0 after correction is the expected null pattern.
- Walk the ML pipeline (correlation filter → scaler → SelectKBest → classifier) and say what's
  re-fitted per fold and why.
- Explain what an AUC confidence interval spanning 0.5 means.
