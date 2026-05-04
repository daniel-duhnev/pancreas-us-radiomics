# Plan: ML Pipeline Improvements (Category 1)

## Context

Notebook 15 ran LogReg and Random Forest on the 93 radiomics features (after correlation removal to 31) with stratified 5-fold CV. Results: AUC ~0.5 (chance level). But we only reported test metrics, and we used simple correlation-based feature reduction instead of proper feature selection.

This notebook addresses both gaps. It reads from existing CSVs — no dependency on the 3 new images.

## Notebook: `analysis/16_ml_improvements.ipynb`

---

## Step 1.1: Add Training Metrics

**Goal:** Report train AND test AUC side-by-side to distinguish "no signal" from "overfitting".

**What to do:**
- Load `reports/13_merged_radiomics_clinical.csv` (134 rows, 93 features)
- Load `reports/14a_stats_radiomics_features.csv` (for the correlation-reduced feature list)
- Copy the classification setup from NB 15: same scaler, same models, same CV
- Add `return_train_score=True` to the `cross_validate()` call
- Extract and print `train_auc` alongside `test_auc`

**Key code change:**
```python
cv_results = cross_validate(
    model, X_scaled, y,
    cv=cv,
    scoring=scoring,
    return_train_score=True
)

auc_train = cv_results["train_auc"].mean()
auc_test = cv_results["test_auc"].mean()
```

**Interpretation:**
- Train ~0.5, Test ~0.5 = no signal (expected for our data)
- Train high, Test ~0.5 = overfitting
- Train high, Test high = genuine signal

**Run on:** full dataset (n=134) and late subset (>90 days post-transplant)

**Output:** Print a table comparing NB 15 results vs NB 16 results.

---

## Step 1.2: Recursive Feature Elimination (RFE)

**Goal:** Use RFECV to find the optimal feature subset. This is more principled than the correlation-based reduction in NB 15.

**What to do:**
- Start from the 31 features after correlation removal
- Use RFECV with LogReg as estimator (coefficients drive elimination)
- Use nested CV to avoid data leakage: RFE runs inside outer fold

**Nested CV approach (no leakage):**
```python
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results_per_fold = []

for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X, y)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Scale on training fold only
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # RFE on training fold only
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    rfecv = RFECV(
        estimator=LogisticRegression(C=1.0, penalty="l2",
                                      class_weight="balanced",
                                      max_iter=1000, random_state=42),
        step=1,
        cv=inner_cv,
        scoring="roc_auc",
        min_features_to_select=1,
    )
    rfecv.fit(X_train_scaled, y_train)

    # Evaluate on held-out test fold
    X_train_sel = rfecv.transform(X_train_scaled)
    X_test_sel = rfecv.transform(X_test_scaled)

    # Train final model on selected features, score on test
    model = LogisticRegression(C=1.0, penalty="l2",
                                class_weight="balanced",
                                max_iter=1000, random_state=42)
    model.fit(X_train_sel, y_train)
    y_prob = model.predict_proba(X_test_sel)[:, 1]
    fold_auc = roc_auc_score(y_test, y_prob)

    results_per_fold.append({
        "fold": fold_idx,
        "n_features_selected": rfecv.n_features_,
        "test_auc": fold_auc,
        "selected_features": [f for f, s in zip(feature_names, rfecv.support_) if s],
    })

    print(f"Fold {fold_idx}: selected {rfecv.n_features_} features, AUC={fold_auc:.3f}")
```

**Also run:** same RFE with Random Forest as estimator (feature importances drive elimination).

**Run on:** full dataset and late subset.

**Output files:**
- `reports/16_ml_improved_results.csv` — train/test metrics comparison
- `reports/16_rfe_feature_ranking.csv` — which features selected per fold, frequency across folds
- `reports/16_rfe_cv_scores.csv` — RFECV curve (N features vs CV score)

---

## Step 1.3: Summary Comparison

Print a final table:

| Experiment | Model | Features | Train AUC | Test AUC |
|-----------|-------|----------|-----------|----------|
| NB 15 baseline | LogReg | 31 (corr removed) | ? | 0.429 |
| NB 15 baseline | RF | 31 (corr removed) | ? | 0.515 |
| NB 16 + train metrics | LogReg | 31 | X.XXX | X.XXX |
| NB 16 + train metrics | RF | 31 | X.XXX | X.XXX |
| NB 16 + RFE | LogReg | N (RFE) | X.XXX | X.XXX |
| NB 16 + RFE | RF | N (RFE) | X.XXX | X.XXX |

---

## Coding standards (per AGENT_HANDOFF.md)

- Plain loops, descriptive variable names
- Cells under 40 lines
- Minimal status prints (no verbose logging)
- Comments only for non-obvious logic (e.g., why nested CV matters)
- No list comprehensions in complex spots
- No fancy abstractions or helper modules

## Input files

- `reports/13_merged_radiomics_clinical.csv` (134 rows x 100 columns)
- `reports/14a_stats_radiomics_features.csv` (p-values, for reference)
- NB 15 code as reference for model setup

## Expected outcome

RFE will likely confirm that no subset of radiomics features achieves meaningful AUC. Train AUC will likely also be ~0.5, confirming there is genuinely no signal (not overfitting). This strengthens the negative result by ruling out "we just used the wrong features" or "the model overfit."

## Effort estimate

~2 hours total. Step 1.1 is ~30 min. Step 1.2 is ~1-1.5 hours (nested CV needs care).
