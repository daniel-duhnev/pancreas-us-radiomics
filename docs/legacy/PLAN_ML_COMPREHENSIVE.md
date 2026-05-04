# Plan: Complete Remaining ML Work Before Next Experiments

## Context

Meeting with Gemma (Mon 27 Apr) produced 5 recommendations for strengthening the ML pipeline. Daniel also has pending tasks: integrate 3 new images from Carlos, handle non-independent data (multiple studies per patient), and paired analysis. All of this needs to be done before moving to Categories 2-4 (NB 17-19). Thesis experiments deadline: early May 2026.

Current state: 134 studies, 55 patients, 93 radiomics features. All test AUCs ~0.5 so far. No significant features after FDR correction. Existing notebooks: NB 16 (complex, done), NB 16_simpler (created, not run), NB 16_1 (learning, not run).

Gemma's 5 recommendations:
1. Review radiomics + ultrasound papers (4 links)
2. Try Boruta algorithm for feature selection
3. Leave-one-out cross-validation (LOOCV)
4. ROC curves + threshold selection via Youden's index
5. More models (SVM, Naive Bayes) + hyperparameter optimization

## Order of Operations

### Phase 0: Integrate 3 New Images (134 → 137 studies)

Follow existing `docs/PLAN_INTEGRATE_NEW_IMAGES.md`. Steps: copy DICOMs → NB 06b preprocess → NB 09 erosion → NB 12 radiomics → NB 13 merge. Mark 47_01 excluded.

Do this first so everything downstream uses the full 137-study dataset.

**Effort:** ~2h if clean, +1-2h for edge cases (34_02 has non-standard DICOM name, 41_03 has 2 series).

### Phase 1: Build Independent Dataset (1 image per patient)

**Why:** 55 patients contribute 137 studies. Some patients appear in both train and test, leaking patient-specific patterns. Gemma and Daniel both flagged this.

**Approach:** Create a filtered version of the merged CSV with 1 row per patient (~55 rows):
- Patient has only one state (all rejection or all non-rejection) → take earliest study by date
- Patient has both states (14 patients) → take the rejection study (earliest if multiple)

**Decision needed:** How to pick when patient has both states. "Take rejection" keeps class balance closer to ~25% rejection. Alternative: take earliest by date regardless. Daniel mentioned "take rejection, always first by date" — follow that unless corrected.

**Implementation:** Small utility cell at the top of the ML notebook. Reads `13_merged_radiomics_clinical.csv` + dates from `bd_estudiUPF.csv`, outputs a filtered dataframe. Not a separate notebook — just a data prep step.

### Phase 2: Comprehensive ML Notebook — `analysis/16_ml_comprehensive.ipynb`

One notebook incorporating all of Gemma's recommendations, built incrementally. Runs on both the full dataset (137 studies, GroupKFold by patient) and the independent dataset (~55 studies, LOOCV).

Structure (start simple, add complexity):

**Section A: Data Prep**
- Load merged CSV, remove correlated features (93 → ~31)
- Build independent dataset (Phase 1 logic)
- Print: sample counts, class balance for both datasets

**Section B: Baseline Models — Simple Train/Test Split**
- One 70/30 stratified split on the independent dataset
- Four models: LogisticRegression, RandomForest (constrained), SVM (RBF kernel), GaussianNB
- For each: train, predict, print train AUC + test AUC
- This is the simplest possible evaluation — establishes the floor

**Section C: ROC Curves + Youden's Index**
- For each model from Section B: plot ROC curve on the test set
- Compute Youden's J = sensitivity + specificity - 1 at each threshold
- Mark the optimal threshold on each ROC curve
- Print: optimal threshold, sensitivity, specificity at that threshold
- Use `sklearn.metrics.roc_curve` + manual Youden computation

**Section D: LOOCV Evaluation**
- Run all 4 models with leave-one-out CV on the independent dataset (~55 samples)
- For the full dataset (137 studies), use `GroupKFold(n_splits=5)` grouped by patient_id instead
- Report: mean AUC, sensitivity, specificity for each model on each dataset
- Compare LOOCV results to the single-split results from Section B

**Section E: Boruta Feature Selection**
- Install `boruta` package if needed (`pip install boruta`)
- Run Boruta on the independent dataset using RF as the base estimator
- Boruta creates shadow features (shuffled copies), trains RF, compares real vs shadow importances over many iterations, keeps features that consistently beat shadows
- Print: confirmed features, tentative features, rejected features
- If Boruta selects a subset: re-run Section D models on that subset

**Section F: Hyperparameter Optimization**
- Only for models that showed any hint of signal (test AUC > 0.55 consistently)
- If nothing shows signal, run grid search on LogReg + SVM anyway to be thorough
- Use `GridSearchCV` with LOOCV (independent) or GroupKFold (full)
- LogReg: C = [0.01, 0.1, 1, 10], penalty = [l1, l2]
- SVM: C = [0.1, 1, 10], kernel = [linear, rbf], gamma = [scale, auto]
- RF: max_depth = [3, 5, 7, None], min_samples_leaf = [3, 5, 10]
- NB: var_smoothing = [1e-9, 1e-7, 1e-5]
- Print best params and best CV score for each

**Section G: Summary Table + Interpretation**
- One table with all results: model, dataset, feature set, AUC, sensitivity, specificity
- Interpretation: does anything work? Does Boruta find signal? Does LOOCV change the story?

### Phase 3: Paired Analysis (NB 17)

Already planned in `docs/PLAN_NEW_EXPERIMENTS.md` Category 2. The 14 patients with both rejection and non-rejection studies.

Do this after Phase 2 because it's a separate statistical question (within-patient differences) rather than classification.

### Phase 4: Paper Review (Not Code)

Gemma's rec #1: review 4 papers on radiomics + ultrasound. Daniel reads these himself. Not part of the coding plan, but note: insights from papers may inform feature engineering choices in NB 18-19.

## Key Design Decisions

1. **One notebook for all ML** (16_ml_comprehensive.ipynb): Keeps everything in one place. Each section builds on the previous. Better than scattering across 5 notebooks.

2. **Two datasets throughout**: Full (137, GroupKFold) and independent (~55, LOOCV). Run every analysis on both. This addresses the non-independence concern directly.

3. **Start with train/test split, end with LOOCV**: Simplest first, most rigorous last. If results are similar, the simpler approach was fine all along.

4. **Boruta before hyperparameters**: Feature selection first, then optimize on the selected features. No point tuning hyperparameters on noise features.

5. **Constrained RF everywhere**: `max_depth=5, min_samples_leaf=5` for RF in all sections to avoid the train AUC = 1.0 problem. Show the unconstrained version once in Section B to demonstrate why.

6. **Keep existing NB 16 and 16_simpler**: They're already done/created. The new comprehensive notebook replaces the need to re-run them but they serve as exploration history.

## Files

- **Creates:** `analysis/16_ml_comprehensive.ipynb`
- **Reads:** `reports/13_merged_radiomics_clinical.csv`, `reports/14a_stats_radiomics_features.csv`, `data/bd_estudiUPF.csv` (for dates in Phase 1)
- **Writes:** `reports/16_comprehensive_ml_results.csv`
- **Modifies (Phase 0):** Various data pipeline files per integration plan

## Dependencies

- `boruta` package — needs `pip install boruta` in thesis_env
- All other packages (sklearn, scipy, matplotlib, pandas, numpy) already installed

## Verification

1. Phase 0: 137 rows in merged CSV, no NaNs in new rows
2. Phase 1: ~55 rows in independent dataset, 1 per patient, verify class balance
3. Phase 2 Section B: Constrained RF train AUC < 1.0
4. Phase 2 Section C: ROC curves render, Youden threshold marked
5. Phase 2 Section D: LOOCV runs without error on ~55 samples (55 folds)
6. Phase 2 Section E: Boruta completes, prints feature decisions
7. Phase 2 Section F: GridSearchCV completes, best params printed
8. All: run top to bottom, no errors, results saved to CSV

## Effort Estimate

- Phase 0: ~2-3h (mostly waiting for pipeline steps)
- Phase 1: ~30min (data prep logic)
- Phase 2: ~4-5h (new notebook, most substantial piece)
- Phase 3: ~3-4h (separate notebook, already planned)
- Total: ~10-12h of coding work
