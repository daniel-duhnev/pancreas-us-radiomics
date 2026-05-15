# Plan: Structured ML Experiments - One Variable at a Time

## Context

The ML work has become messy - 4 exploratory notebooks (16a, 16b, 16c, 16_1), a kitchen-sink comprehensive notebook, and no clear structure. Daniel wants to reset and take a scientific approach: define a baseline, change one thing at a time, keep the winner, move on. Each experiment answers one question. The final result is a single defensible ML pipeline.

All results so far show AUC ~0.5. Boruta rejected all 31 features. The goal isn't to find a miracle - it's to be thorough and structured so the negative result is bulletproof for the thesis.

## Step 0: Clean up

- Move `16a_ml_improvements.ipynb`, `16b_*`, `16c_*`, `16_1_*` into `analysis/archive/`
- Move `docs/PLAN_ML_COMPREHENSIVE.md` into `docs/legacy/`
- Start fresh with a new notebook

## Notebook: `analysis/17_ml_experiments.ipynb`

Using 17 because the 16 series was exploratory. This is the "real" structured ML notebook.

## Fixed methodology (not an experiment - this is the measuring stick)

- **Evaluation:** LOOCV on the full dataset (134 samples). Most robust for small n, Gemma recommended it.
- **Scaling:** StandardScaler fit inside each fold (no leakage).
- **Metric:** AUC computed from collected LOO predicted probabilities. Also report sensitivity + specificity at Youden threshold.
- **Random state:** 42 everywhere for reproducibility.

## Experiment sequence

### Experiment 1: Which algorithm works best?

**Change:** algorithm
**Hold constant:** all 31 features (after correlation removal), default hyperparameters, LOOCV

Try:
- LogisticRegression (C=1.0, l2, balanced)
- RandomForest (n=100, max_depth=5, min_samples_leaf=5, balanced)
- SVM (rbf, balanced)
- GaussianNB

**Output:** Table with LOOCV AUC for each. Pick the best (or top 2 if close). ROC curves for all 4.

**Carry forward:** winning algorithm (or top 2)

### Experiment 2: Does feature selection help?

**Change:** feature set
**Hold constant:** winning algorithm from Exp 1, LOOCV

Try:
- All 31 features (baseline)
- Boruta selection (may select 0 - that's a result)
- RFE: iteratively drop least important feature, record AUC at each step, find the best subset size

**Output:** Table with AUC for each feature set. If Boruta selects 0 features, that confirms no signal. RFE curve shows whether fewer features helps.

**Carry forward:** best feature set (likely "all 31" if no signal)

### Experiment 3: Do better hyperparameters help?

**Change:** hyperparameters
**Hold constant:** winning algorithm + feature set, 5-fold stratified CV (not LOOCV - grid search with LOOCV produces NaN with roc_auc scoring)

Try: small grid search for the winning algorithm. Example grids:
- LogReg: C=[0.01, 0.1, 1, 10], penalty=[l1, l2]
- RF: max_depth=[3, 5, 7], min_samples_leaf=[3, 5, 10]
- SVM: C=[0.1, 1, 10], kernel=[linear, rbf]
- NB: var_smoothing=[1e-9, 1e-7, 1e-5]

**Output:** Best params, best CV AUC. Then re-evaluate best params with LOOCV to confirm.

**Carry forward:** best hyperparameters

### Experiment 4: Final pipeline + ROC + threshold

**Change:** nothing - this is the final evaluation
**Hold constant:** best algorithm + features + hyperparameters from Exp 1-3

- Run LOOCV with the final pipeline
- Plot ROC curve, mark Youden threshold
- Report: AUC, sensitivity, specificity at Youden threshold
- Save ROC curve to `reports/17_roc_final.png`
- Compare to the default threshold (0.5) - show that Youden doesn't help when AUC ~0.5

### Experiment 5: Does the late subset change anything?

**Change:** dataset
**Hold constant:** final pipeline from Exp 4

- Repeat Exp 4 on late subset (68 samples, motivo 3/4/5)
- Save ROC curve to `reports/17_roc_late.png`
- If AUC is meaningfully higher: late-stage studies might carry more signal
- If same: confirms no signal regardless of time post-transplant

## Notebook cell structure

Each experiment is a block of 3-4 cells:
1. Markdown: what we're testing, what's fixed, what changes
2. Code: run the experiment, print results
3. Code: plot (if applicable)
4. Markdown: conclusion - what won, what we carry forward

Estimated ~20-25 cells total. Each cell under 40 lines per AGENT_HANDOFF.md.

## Summary cell at the end

One table showing the full experiment chain:
| Exp | Question | Winner | AUC |
Followed by 2-3 sentences: "We tested 4 algorithms, 3 feature selection methods, hyperparameter grids, and 2 datasets. The best pipeline achieved AUC = X. [Interpretation]."

## Files

- **Archive:** move 16a, 16b, 16c, 16_1 to `analysis/archive/`
- **Archive:** move `docs/PLAN_ML_COMPREHENSIVE.md` to `docs/legacy/`
- **Creates:** `analysis/17_ml_experiments.ipynb`
- **Reads:** `reports/13_merged_radiomics_clinical.csv`, `reports/14a_stats_radiomics_features.csv`
- **Writes:** `reports/17_ml_experiment_results.csv`, `reports/17_roc_final.png`, `reports/17_roc_late.png`

## Why this is better

1. **One question per experiment.** No more "run everything and hope something sticks."
2. **Each experiment's conclusion is the next experiment's input.** Clear dependency chain.
3. **Reproducible.** Fixed seeds, saved results, documented decisions.
4. **Defensible for thesis.** "We systematically evaluated algorithms, feature selection, and hyperparameters. At each stage, the best result was carried forward."
5. **Handles the negative result well.** If every experiment returns AUC ~0.5, the chain of experiments shows you were thorough - not that you were lazy.

## Verification

- Run all cells top to bottom
- Check that each experiment's "winner" is used in the next experiment
- ROC PNGs saved and look correct
- Summary CSV has one row per experiment with the key result
- No warnings or errors (fix the LOOCV + GridSearchCV NaN issue by using 5-fold for grid search)
