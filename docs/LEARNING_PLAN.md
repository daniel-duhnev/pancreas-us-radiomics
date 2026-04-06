# Learning Plan: Radiomics, Statistics, and ML

A structured plan for understanding the core concepts behind this thesis project.
Each module covers key concepts with explanations, then produces a hands-on
Jupyter notebook with worked examples.

---

## Module 1: Radiomics and PyRadiomics -- What Are These Numbers?

**Goal:** Understand what a "feature" is, why textures matter in medical imaging,
and what PyRadiomics actually computes from a single ultrasound image.

### 1.1 What is a radiomics feature?

- An image is a grid of pixel intensity values (0-255 for grayscale).
- A "feature" is a single number that summarizes some property of that pixel grid
  within a region of interest (the mask).
- Example: the mean pixel value, the standard deviation, or how "rough" the
  texture looks.
- Analogy: if someone shows you two photos of sand -- one fine, one coarse --
  you can tell the difference. Radiomics tries to quantify that difference as
  numbers.

### 1.2 First-order features (intensity-based, no spatial info)

- These only care about the **histogram** of pixel values, not where pixels are
  located.
- Examples: Mean, Median, Variance, Skewness, Kurtosis, 10th Percentile, Entropy.
- **Hands-on:** take one image, plot its histogram inside the mask, compute
  mean/std/entropy by hand, then compare with PyRadiomics output.

### 1.3 Texture features (second-order, spatial relationships)

These care about how **neighbouring pixels** relate to each other:

- **GLCM (Gray-Level Co-occurrence Matrix):** "How often does pixel value X
  appear next to pixel value Y?" Captures patterns like contrast, homogeneity,
  correlation.
- **GLRLM (Gray-Level Run-Length Matrix):** "How often do we see a run of N
  consecutive pixels with the same value?" Captures coarseness vs fine grain.
- **GLSZM (Gray-Level Size Zone Matrix):** "How big are connected regions of
  similar intensity?" Like GLRLM but in 2D zones.
- **GLDM (Gray-Level Dependence Matrix):** "How many neighbouring pixels have
  a similar value?" Captures local uniformity.
- **NGTDM (Neighbouring Gray-Tone Difference Matrix):** "How different is each
  pixel from its neighbours?" Captures busyness, complexity.
- **Hands-on:** build a tiny 5x5 pixel grid, compute a GLCM by hand, then show
  how PyRadiomics gets the same answer.

### 1.4 Why texture matters in medical imaging

- Tissue pathology (inflammation, fibrosis, rejection) changes the microscopic
  structure.
- This changes the ultrasound echo pattern, which changes pixel textures.
- Radiomics hypothesis: these texture changes are too subtle for the eye but
  detectable by math.

### 1.5 What PyRadiomics does under the hood

- Takes a SimpleITK image + binary mask.
- Quantizes gray levels (binning).
- Builds the matrices (GLCM, GLRLM, etc.) from the masked region.
- Computes summary statistics from each matrix.
- Returns ~93 numbers per image.

### Notebook: `12_1_understanding_radiomics_features.ipynb`

- Load one real image from our dataset (e.g., study 01_01) with its mask.
- Show the image, overlay the mask, show the cropped region.
- Plot the intensity histogram inside the mask.
- Compute 3 first-order features by hand (mean, std, entropy) and verify against
  PyRadiomics.
- Build a tiny GLCM example (4x4 synthetic image) step by step.
- Extract all features for this one image, group them by class, and explain the
  top 5 from each class in plain language.
- Show what happens when you change the image (add noise, blur it) -- how do
  features change?

---

## Module 2: Statistical Testing -- What Do p-values Actually Mean?

**Goal:** Understand what a t-test/Mann-Whitney does, what a p-value is, what
alpha means, why testing many features inflates false positives, and why
statistical tests don't have a "test set."

### 2.1 The core question

- We have two groups (rejection vs no-rejection) and a measurement (one feature).
- Question: "Is the difference between these groups real, or could it be random
  chance?"
- A statistical test answers: "How likely would we see this difference if there
  were actually no difference?" That probability is the **p-value**.

### 2.2 t-test vs Mann-Whitney

- **t-test:** assumes data is normally distributed (bell curve), compares means.
- **Mann-Whitney U:** no distribution assumption, compares ranks (which group
  tends to have higher values?).
- When to use which: Shapiro-Wilk normality test decides. Most of our features
  fail normality, so we use Mann-Whitney.
- **Hands-on:** take one feature, plot both group distributions, run both tests,
  see if they agree.

### 2.3 What is a p-value, really?

- p = 0.03 means: "If rejection had zero effect on this feature, there's a 3%
  chance we'd see a difference this large by luck."
- p < 0.05 is a convention (not magic). Alpha = 0.05 means we accept a 5% false
  positive rate.
- A p-value is **NOT** the probability that the result is wrong. It's the
  probability of the data given no effect.
- **Hands-on:** simulate fake data (two groups drawn from the same distribution),
  run Mann-Whitney 1000 times, show that ~5% of tests give p < 0.05 even when
  there's no real difference.

### 2.4 The multiple comparisons problem

- We test 93 features at alpha = 0.05. Even if none are truly different, we
  expect ~4-5 false positives by chance (93 x 0.05 = 4.65).
- This is why finding "2 significant features out of 93" could easily be noise.
- **Bonferroni correction:** divide alpha by number of tests (very strict).
- **Benjamini-Hochberg FDR:** controls the proportion of false discoveries
  (less strict).
- **Hands-on:** simulate 93 features with NO real difference, run 93 Mann-Whitney
  tests, count how many give p < 0.05. Repeat 100 times. Show the distribution
  of false positives.

### 2.5 Why statistical tests have no "test set"

- In ML: you train on some data, test on held-out data. The test set proves the
  model generalises.
- In a statistical test: you use ALL the data at once. There's no train/test
  split.
- The p-value itself is the safeguard against overfitting -- but only if you
  don't test too many things (hence alpha correction).
- If you look at your data, find the best feature, then test only that one, the
  p-value is misleading (this is "data dredging" or "p-hacking").
- Connection to our project: we test 93 features, find 0 significant. This is
  actually a clean result -- no cherry-picking.

### 2.6 Effect size -- the forgotten half

- A p-value tells you IF there's a difference, not HOW BIG.
- **Cohen's d** (for t-test): difference in means divided by pooled standard
  deviation. d=0.2 small, d=0.5 medium, d=0.8 large.
- **Rank-biserial correlation** (for Mann-Whitney): ranges from -1 to +1, how
  well the groups separate.
- Our features have small effect sizes (|r| < 0.2), meaning even if something
  were significant, the groups barely separate.

### Notebook: `14_1_understanding_statistical_tests.ipynb`

- Take one real feature from our data, plot the two group distributions side
  by side.
- Run t-test and Mann-Whitney, show p-values and effect sizes.
- Simulate the null hypothesis: generate 95 + 39 random numbers from the SAME
  distribution, run the test, repeat 10,000 times, plot the p-value distribution
  (should be uniform).
- Simulate a TRUE effect: generate groups with a known difference (Cohen's d =
  0.5), run the test, show how p-value and effect size behave.
- The multiple comparisons demo: run 93 tests on pure noise, count false
  positives, apply BH correction, show how it protects you.
- Interactive example: vary the effect size and sample size, see how p-values
  change (statistical power).

---

## Module 3: Machine Learning Classification Basics

**Goal:** Understand the ML approach as an alternative to statistical tests,
why we need train/test splits, what AUC means, and why small datasets make
ML hard.

### 3.1 From statistical test to classifier

- Statistical test asks: "Is this feature different between groups?"
- Classifier asks: "Given all features together, can I predict which group a new
  sample belongs to?"
- Key difference: ML can combine multiple weak features into a stronger
  prediction.

### 3.2 Why we need train/test splits

- If you train and evaluate on the same data, you measure memorisation, not
  generalisation.
- **Overfitting:** a complex model can perfectly fit training data but fail on
  new data.
- **Cross-validation:** split data into K folds, train on K-1, test on 1, rotate.
  Average the results.
- Our setup: stratified 5-fold CV (keeps the 29% rejection ratio in each fold).

### 3.3 Key metrics

- **Accuracy:** misleading with imbalanced classes (always predicting "no
  rejection" gives 71% accuracy).
- **Sensitivity (recall):** of all rejection cases, how many did we catch?
- **Specificity:** of all no-rejection cases, how many did we correctly identify?
- **AUC (Area Under ROC Curve):** overall discrimination ability. 0.5 = random,
  1.0 = perfect.
- Why AUC is preferred for imbalanced datasets.

### 3.4 The models we used

- **Logistic Regression:** draws a line (hyperplane) between classes. Simple,
  interpretable. L2 regularisation prevents overfitting.
- **Random Forest:** builds many decision trees on random subsets, votes on the
  answer. Handles non-linear patterns.
- **Class weighting:** tells the model that rejection cases are more important
  (because they're rarer).

### 3.5 Feature selection and curse of dimensionality

- 93 features, 134 samples: more features than useful for this sample size.
- Correlated features: 305 pairs with |r| > 0.9 means many features carry the
  same information.
- Removing correlated features reduces redundancy and helps models generalise.
- Rule of thumb: you want at least 10-20 samples per feature for reliable ML.

### 3.6 Interpreting our results

- AUC 0.43-0.56: at or below chance level.
- This is consistent with the statistical analysis (no features individually
  discriminate).
- Does not mean ML is useless -- means these particular features on this dataset
  don't carry enough signal.

### Notebook: `15_1_understanding_ml_classification.ipynb`

- Build a tiny synthetic example: 2 features, 2 classes, visible on a scatter
  plot.
- Train logistic regression, draw the decision boundary, compute AUC.
- Show overfitting: add 50 random noise features, train without regularisation,
  show train AUC vs test AUC diverging.
- Show cross-validation: implement a manual 5-fold loop on our actual data with
  just 3 features.
- Plot an ROC curve and explain what it means.
- Compare with our actual notebook 15 results.

---

## Execution Order

| Step | What | Output |
|------|------|--------|
| 1 | Review Module 1 plan | Confirm / adjust |
| 2 | Build `12_1_understanding_radiomics_features.ipynb` | Interactive notebook |
| 3 | Review Module 2 plan | Confirm / adjust |
| 4 | Build `14_1_understanding_statistical_tests.ipynb` | Interactive notebook |
| 5 | Review Module 3 plan | Confirm / adjust |
| 6 | Build `15_1_understanding_ml_classification.ipynb` | Interactive notebook |
| 7 | Audit actual analysis notebooks (12, 14a, 14b, 15) | Check for mistakes |
