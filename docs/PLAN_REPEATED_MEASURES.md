# Plan: Addressing Repeated Measures in Pancreas Radiomics Analysis

## Background

Our dataset contains **134 ultrasound studies from 55 patients** (mean 2.4 studies per patient). Of these, **14 patients have both rejection and no-rejection studies**. All current statistical analyses (Mann-Whitney U tests, t-tests) treat studies as independent observations. However, studies from the same patient are correlated due to shared genetics, surgical technique, and baseline organ characteristics. This violates the independence assumption underlying these tests.

Clara's paper (Bassaganyas et al. 2025) uses the same independent-observations approach, so our replication is methodologically consistent with the original work. Nonetheless, this is a known limitation that warrants further investigation.

### Evidence of Instability

A sensitivity analysis revealed concerning instability in our results:

- **First study per patient** (55 obs: 14 rejection, 41 no-rejection): some features flip to significant -- `firstorder_Minimum` (p=0.026), `firstorder_10Percentile` (p=0.024), `ngtdm_Busyness` (p=0.033).
- **Last study per patient** (55 obs: same split): those same features become clearly non-significant (p > 0.7).

This instability confirms that the choice of which study to include per patient materially affects the results, and that the repeated measures structure is influencing our findings.

---

## Proposed Approaches

The following seven approaches are ordered roughly from simplest to most sophisticated. Each can be implemented independently. The goal is to understand how robust our radiomic feature findings are once we properly account for within-patient correlation.

---

### 1. One-Study-Per-Patient: First Visit

**What it does:** Subset the data to include only the earliest study (by date) for each patient. Run all statistical tests on this reduced dataset of 55 observations.

**Implementation:**

```python
# Using pandas
df_first = df.sort_values('study_date').groupby('patient_id').first().reset_index()
# Then run Mann-Whitney U on df_first for each feature
from scipy.stats import mannwhitneyu
stat, pval = mannwhitneyu(
    df_first.loc[df_first['rejection'] == 1, feature],
    df_first.loc[df_first['rejection'] == 0, feature],
    alternative='two-sided'
)
```

**Packages:** `pandas`, `scipy.stats.mannwhitneyu`

**Pros:**
- Simple and easy to interpret.
- Captures the baseline state of the organ before subsequent changes.
- Eliminates within-patient correlation entirely.

**Cons:**
- Reduces sample size from 134 to 55, substantially reducing statistical power.
- Early visits (motivo 1) may reflect high post-surgical dispersion, adding noise unrelated to rejection status.
- Biased toward early timepoints, which may not represent the typical state of the organ.

**Expected impact:** Results will differ from the full-dataset analysis. Some currently significant features may lose significance due to reduced power; others may gain significance if the full-dataset results were driven by repeated observations from a few patients.

---

### 2. One-Study-Per-Patient: Last Visit

**What it does:** Subset the data to include only the most recent study for each patient. Run all statistical tests on this reduced dataset of 55 observations.

**Implementation:**

```python
df_last = df.sort_values('study_date').groupby('patient_id').last().reset_index()
# Same Mann-Whitney approach as above
```

**Packages:** `pandas`, `scipy.stats.mannwhitneyu`

**Pros:**
- Simple and easy to interpret.
- Captures the most recent (and potentially most clinically relevant) state.
- Eliminates within-patient correlation entirely.

**Cons:**
- Reduces sample size from 134 to 55.
- Biased toward late timepoints; may reflect chronic changes rather than acute rejection.
- For patients with both outcomes, the "last" study may not be representative.

**Expected impact:** As observed in our sensitivity analysis, results differ substantially from the first-visit approach. Features that are significant with first-visit selection (e.g., `firstorder_Minimum`, `firstorder_10Percentile`, `ngtdm_Busyness`) are non-significant here (p > 0.7), highlighting the instability problem.

---

### 3. One-Study-Per-Patient: Random Selection (Repeated 1000 Times)

**What it does:** For each of 1000 iterations, randomly select one study per patient, then run all statistical tests. Report the distribution of p-values across iterations for each feature.

**Implementation:**

```python
import numpy as np
from scipy.stats import mannwhitneyu

n_iterations = 1000
p_values = {feature: [] for feature in feature_list}

for i in range(n_iterations):
    # Randomly pick one study per patient
    df_random = df.groupby('patient_id').apply(
        lambda x: x.sample(n=1, random_state=i)
    ).reset_index(drop=True)

    for feature in feature_list:
        rej = df_random.loc[df_random['rejection'] == 1, feature].dropna()
        no_rej = df_random.loc[df_random['rejection'] == 0, feature].dropna()
        if len(rej) > 0 and len(no_rej) > 0:
            _, pval = mannwhitneyu(rej, no_rej, alternative='two-sided')
            p_values[feature].append(pval)

# Summarize: median p-value, proportion of iterations where p < 0.05
for feature in feature_list:
    pvals = np.array(p_values[feature])
    print(f"{feature}: median p = {np.median(pvals):.4f}, "
          f"significant in {np.mean(pvals < 0.05)*100:.1f}% of iterations")
```

**Packages:** `pandas`, `numpy`, `scipy.stats.mannwhitneyu`

**Pros:**
- Avoids the arbitrary bias of choosing first or last visit.
- Quantifies how sensitive each feature's significance is to study selection.
- Features that are significant in >90% of iterations are robust; features significant in <50% are unreliable.

**Cons:**
- Still uses only 55 observations per iteration (reduced power).
- Does not formally model within-patient correlation.
- Computationally more involved (though 1000 iterations is fast for this dataset size).

**Expected impact:** This approach will reveal which features are consistently significant regardless of study selection (robust findings) versus which features are significant only with certain selections (unstable findings). This is the most informative of the one-study-per-patient approaches.

---

### 4. Mixed-Effects Models

**What it does:** Fit a linear mixed model for each radiomic feature with rejection status as the fixed effect and patient as a random intercept. This properly accounts for within-patient correlation while using all 134 observations.

**Implementation:**

```python
import statsmodels.formula.api as smf

# For each feature:
model = smf.mixedlm(
    f"{feature} ~ rejection",
    data=df,
    groups=df["patient_id"]
)
result = model.fit()

# Extract the fixed effect of rejection
print(result.summary())
p_value_rejection = result.pvalues['rejection']
coefficient = result.params['rejection']
```

Alternative in R (if needed):

```r
library(lme4)
library(lmerTest)

model <- lmer(feature ~ rejection + (1 | patient_id), data = df)
summary(model)
```

**Packages:**
- Python: `statsmodels` (`MixedLM`)
- R alternative: `lme4`, `lmerTest`

**Pros:**
- Gold standard for repeated/clustered measures.
- Uses all 134 observations, maximizing statistical power.
- Properly accounts for within-patient correlation via the random intercept.
- Provides estimates of both between-patient and within-patient variance.

**Cons:**
- More complex to implement and interpret than simple tests.
- Assumes the feature values follow a roughly normal distribution (may need transformation for some radiomics features).
- Convergence issues possible with small cluster sizes.
- The 14 patients with both outcomes drive much of the information about the rejection effect.

**Expected impact:** This is the most principled approach and should be considered the primary analysis if we move beyond the replication framework. Results may differ from the naive Mann-Whitney in either direction. Features whose significance was driven by within-patient correlation will likely lose significance; features masked by between-patient variability may gain significance.

---

### 5. GEE (Generalized Estimating Equations)

**What it does:** Fit a marginal model using GEE with an exchangeable correlation structure, treating patient as the clustering variable. This estimates population-average effects of rejection on each feature.

**Implementation:**

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# For each feature:
model = smf.gee(
    f"{feature} ~ rejection",
    groups="patient_id",
    data=df,
    cov_struct=sm.cov_struct.Exchangeable(),
    family=sm.families.Gaussian()
)
result = model.fit()

print(result.summary())
p_value_rejection = result.pvalues['rejection']
```

**Packages:** `statsmodels` (`GEE`, `cov_struct`)

**Pros:**
- Uses all 134 observations.
- Robust to misspecification of the correlation structure (sandwich/robust standard errors).
- Provides population-average effects, which are often more interpretable for clinical questions.
- Does not require normality assumptions as strictly as mixed models.

**Cons:**
- Requires choosing a correlation structure (exchangeable is reasonable here but still an assumption).
- Less efficient than mixed models if the correlation structure is correctly specified.
- Small number of clusters (55 patients) can lead to underestimation of standard errors; consider using a small-sample correction (e.g., `cov_type='bias_reduced'`).
- Does not provide patient-specific estimates.

**Expected impact:** Results should be broadly consistent with mixed-effects models but with potentially wider confidence intervals. The population-average interpretation aligns well with the clinical question ("on average, do rejection studies differ from no-rejection studies?").

---

### 6. Bootstrap with Cluster Resampling

**What it does:** Perform bootstrap resampling at the patient level (not the study level). Each bootstrap iteration draws 55 patients with replacement and includes ALL studies for each selected patient. Run the Mann-Whitney test on each bootstrap sample and compute bootstrap confidence intervals for test statistics and p-values.

**Implementation:**

```python
import numpy as np
from scipy.stats import mannwhitneyu

n_bootstrap = 1000
patient_ids = df['patient_id'].unique()
bootstrap_stats = {feature: [] for feature in feature_list}

for i in range(n_bootstrap):
    # Resample patients (with replacement)
    rng = np.random.default_rng(seed=i)
    sampled_patients = rng.choice(patient_ids, size=len(patient_ids), replace=True)

    # Build bootstrap sample: all studies from sampled patients
    # Use a counter to handle duplicate patient selections
    bootstrap_dfs = []
    for pid in sampled_patients:
        bootstrap_dfs.append(df[df['patient_id'] == pid])
    df_boot = pd.concat(bootstrap_dfs, ignore_index=True)

    for feature in feature_list:
        rej = df_boot.loc[df_boot['rejection'] == 1, feature].dropna()
        no_rej = df_boot.loc[df_boot['rejection'] == 0, feature].dropna()
        if len(rej) > 1 and len(no_rej) > 1:
            stat, pval = mannwhitneyu(rej, no_rej, alternative='two-sided')
            bootstrap_stats[feature].append(stat)

# Compute 95% confidence interval for the test statistic
for feature in feature_list:
    stats = np.array(bootstrap_stats[feature])
    ci_lower, ci_upper = np.percentile(stats, [2.5, 97.5])
    print(f"{feature}: bootstrap 95% CI = [{ci_lower:.2f}, {ci_upper:.2f}]")
```

**Packages:** `pandas`, `numpy`, `scipy.stats.mannwhitneyu`

**Pros:**
- Non-parametric: makes no distributional assumptions.
- Respects the clustering structure by resampling at the patient level.
- Uses all available data within each bootstrap sample.
- Provides confidence intervals that account for within-patient correlation.

**Cons:**
- Computationally more intensive than parametric methods (though manageable for this dataset).
- Does not provide a single "corrected" p-value in the traditional sense; instead provides distributional information.
- Theoretical properties of cluster bootstrap with unequal cluster sizes are less well-established.
- Interpretation requires more care than standard hypothesis tests.

**Expected impact:** Bootstrap confidence intervals will generally be wider than those from naive Mann-Whitney, reflecting the true uncertainty when accounting for clustering. Features with narrow CIs that exclude zero are robust findings; features with wide CIs are unreliable.

---

### 7. Paired Analysis for Patients with Both Outcomes

**What it does:** For the 14 patients who have both rejection and no-rejection studies, compute the within-patient difference in each feature (rejection value minus no-rejection value). If a patient has multiple studies per outcome, average them first. Then run a one-sample Wilcoxon signed-rank test on these differences.

**Implementation:**

```python
from scipy.stats import wilcoxon

# Identify patients with both outcomes
both = df.groupby('patient_id')['rejection'].nunique()
patients_both = both[both == 2].index

# Compute mean feature value per patient per outcome
df_both = df[df['patient_id'].isin(patients_both)]
patient_means = df_both.groupby(['patient_id', 'rejection'])[feature_list].mean()

# Compute within-patient differences
rej_means = patient_means.xs(1, level='rejection')
no_rej_means = patient_means.xs(0, level='rejection')
diffs = rej_means - no_rej_means  # DataFrame with 14 rows

# One-sample Wilcoxon signed-rank test (H0: median difference = 0)
for feature in feature_list:
    d = diffs[feature].dropna()
    if len(d) >= 10:  # minimum for meaningful test
        stat, pval = wilcoxon(d, alternative='two-sided')
        print(f"{feature}: median diff = {d.median():.4f}, p = {pval:.4f}")
```

**Packages:** `pandas`, `scipy.stats.wilcoxon`

**Pros:**
- Completely eliminates between-patient variability -- each patient serves as their own control.
- Very clean interpretation: does a patient's feature value change when they have rejection vs. not?
- The most internally valid comparison possible with this data.

**Cons:**
- Only 14 patients, giving very low statistical power.
- Wilcoxon signed-rank test with n=14 can only detect large effects.
- Averaging multiple studies per outcome within a patient discards temporal information.
- Results from 14 patients may not generalize to the full cohort.

**Expected impact:** Due to the small sample size (n=14), most features will likely be non-significant even if real effects exist. However, any feature that IS significant in this analysis has very strong evidence, since between-patient confounding is eliminated. This is best used as a complementary analysis rather than a primary one.

---

## Recommended Investigation Order

1. **Start with Approach 3** (random selection, 1000 iterations) -- this quickly reveals which features are robust vs. unstable, requiring minimal additional infrastructure.
2. **Then implement Approach 4** (mixed-effects models) -- this is the most principled analysis and should become the primary method for any new findings we wish to report beyond replication.
3. **Run Approach 7** (paired analysis) as a complementary check -- despite low power, any significant findings here are very compelling.
4. **Consider Approach 6** (cluster bootstrap) if there are concerns about the normality assumptions of mixed models for specific features.
5. **Approaches 1, 2, and 5** are lower priority but straightforward to implement for completeness.

---

## Notes

- This plan is for **future investigation only**. No implementation is required at this time.
- The current analysis (treating studies as independent) is consistent with Bassaganyas et al. 2025 and is appropriate for the replication phase of this thesis.
- Any of the above approaches can be implemented independently; they do not depend on each other.
- Results from multiple approaches should be compared: features that are significant across several approaches are the most trustworthy.
