# Thesis Defense — Speaking Script

**Non-invasive Detection of Pancreas Graft Rejection: Comparing Automated Texture Analysis with Clinical Ultrasound Biomarkers**

Daniel Duhnev · EMAI 2024–2026 · Supervisor: Gemma Piella (UPF)
Defense: Thursday 16 July 2026, 09:00, room 55.309
Committee: Gemma Piella · Miguel Ángel González · Sotiris Papadiamantis

---

## How to use this document

- This is a **read-aloud script**. The text in the **"SAY"** blocks is what you actually speak — written the way you talk, so you can read it almost verbatim and still sound natural.
- Each slide has a **time budget**. The whole talk lands at **~20–22 minutes** at a calm, slow pace (~120 words/minute). That is right inside the 20–25 minute window, with slack.
- **"ON SCREEN"** reminds you what the committee is looking at.
- **"EXPLAIN THE FIGURE"** is a detailed, accurate walk-through of every plot and diagram — both so you can narrate it well *and* so you understand it completely. Read these carefully while rehearsing; you do not read them aloud word-for-word, you use them to talk about the figure confidently.
- **"IF ASKED"** gives you the precise numbers and the safe answer for the most likely probes.
- Anything in *[square brackets and italics]* is a stage direction to yourself, not spoken.

**Golden rules for the day:** breathe between slides. It is fine to pause. You are presenting a *clean, honest negative result with a working positive control* — that is a strong scientific story, not a weak one. Own it.

---

## Timing map

| # | Slide | Budget | Running |
|---|-------|--------|---------|
| 1 | Title | 0:30 | 0:30 |
| 2 | Outline | 0:30 | 1:00 |
| 3 | Clinical background | 1:15 | 2:15 |
| 4 | The opportunity | 1:15 | 3:30 |
| 5 | Research question & objectives | 1:00 | 4:30 |
| 6 | Dataset | 1:30 | 6:00 |
| 7 | Preprocessing | 1:20 | 7:20 |
| 8 | Radiomics feature extraction | 1:15 | 8:35 |
| 9 | Statistical methodology | 1:15 | 9:50 |
| 10 | Machine-learning methodology | 1:25 | 11:15 |
| 11 | Result 1 — statistics | 1:40 | 12:55 |
| 12 | Result 2 — classifiers | 1:35 | 14:30 |
| 13 | Result 3 — ARFI positive control | 1:50 | 16:20 |
| 14 | Why ARFI works but radiomics doesn't | 1:45 | 18:05 |
| 15 | Robustness | 1:20 | 19:25 |
| 16 | Discussion | 1:15 | 20:40 |
| 17 | Limitations | 1:05 | 21:45 |
| 18 | Conclusions | 1:05 | 22:50 |
| 19 | Future work & thank you | 0:45 | 23:35 |

**If you are running long:** the easiest slides to compress are **9 and 10** (methods) — you can cut the sub-details and keep the headline. Do *not* rush slides 11–14; those are the ones the committee cares about.

---

## Slide 1 — Title · *0:30*

**ON SCREEN:** Title, your name, EMAI 2024–2026, supervisor Gemma Piella, defense date.

**SAY:**
> Good morning, and thank you all for being here. My name is Daniel Duhnev, and this is my master's thesis for the EMAI programme, supervised by Gemma Piella. The title is *"Non-invasive Detection of Pancreas Graft Rejection — Comparing Automated Texture Analysis with Clinical Ultrasound Biomarkers."* Over the next twenty minutes or so, I will show how I tested whether we can detect pancreas transplant rejection automatically, from ordinary ultrasound images, and how that compares against the specialised ultrasound biomarkers the clinicians already use.

*[Breathe. Advance.]*

---

## Slide 2 — Outline · *0:30*

**ON SCREEN:** Four-part agenda — Motivation · Data & Methods · Results · Conclusions.

**SAY:**
> Here is the plan. First, the motivation — what pancreas rejection is, and why we badly need a non-invasive test. Second, the data and the analysis pipeline. Third, the results, which are the heart of the talk and include an important positive control. And finally, what it all means, the limitations, and where this could go next. I will keep the methods tight so we have time on the results.

---

## Slide 3 — Clinical Background · *1:15*

**ON SCREEN:** Pancreas transplant treats type 1 diabetes; rejection threatens the graft; biopsy is the reference standard but invasive.

**SAY:**
> Let me start with the clinical problem. Pancreas transplantation is the one established treatment that can restore normal blood-sugar control in patients with type 1 diabetes — a working graft frees the patient from insulin injections. But the immune system can attack the transplanted organ. That is rejection, and it remains one of the leading causes of graft loss, affecting roughly one in five grafts in the first year.
>
> The problem is detecting it. The reference standard today is a percutaneous needle biopsy of the graft. Biopsy is invasive — it carries real risks of bleeding and pancreatitis. The pancreas sits deep in the abdomen, so it is not always easy to reach; the needle samples only a tiny piece of tissue, so focal rejection can be missed entirely; and results take time. Because of all this, biopsy is *not* done routinely — in practice it is reserved for cases of strong clinical suspicion. So there is a clear, unmet need: a reliable, non-invasive way to monitor the graft and flag which patients actually need that biopsy. That need is the motivation for this whole thesis.

**IF ASKED — "how is rejection diagnosed in your data if not always by biopsy?"**
> The label in my dataset is the clinical rejection variable assigned by the transplant team, based on the full clinical picture and, where available, biopsy confirmation. Of the 39 rejection studies, 27 were biopsy-confirmed; the rest are clinical diagnoses — precisely because biopsy is not routine. I treat that label noise as a limitation, which I come back to at the end.

---

## Slide 4 — The Opportunity: Non-invasive Ultrasound · *1:15*

**ON SCREEN:** Ultrasound is cheap/fast/bedside; specialised US biomarkers (ARFI, DCE-US) already work; but they need special protocols; → the radiomics gap.

**SAY:**
> So where could a non-invasive test come from? Ultrasound is the natural place to look — it is cheap, fast, done at the bedside, and uses no radiation. And we already know ultrasound *can* see rejection. Recent work by Bassaganyas and colleagues at Hospital Clínic — using this very same patient cohort — showed that two specialised ultrasound techniques discriminate rejection in the late period after transplant. The first is ARFI elastography, which measures how *stiff* the tissue is. The second is dynamic contrast-enhanced ultrasound, which measures *perfusion*, the blood flow through the graft.
>
> The catch is that both of these need special acquisition protocols, extra equipment or a contrast injection, and careful manual measurement by a trained radiologist. That limits how widely they can be used, and it introduces operator-dependent variability.
>
> So here is my research gap. Every routine scan already captures ordinary grayscale — so-called B-mode — images. Could we apply *radiomics* — fully automated texture analysis — to those plain images, and get the same diagnostic information for free? That is the question this thesis sets out to answer.

---

## Slide 5 — Research Question & Objectives · *1:00*

**ON SCREEN:** Central question + five objectives.

**SAY:**
> That gives the central question of the thesis: *can radiomics texture features from grayscale ultrasound predict pancreas rejection?* I broke it into five concrete objectives. One — build a pipeline to extract standardised texture features from the graft region. Two — test each feature individually, with statistics, to see if any single one discriminates rejection. Three — go multivariate, and build machine-learning classifiers. Four — and this one is crucial — reproduce the known clinical-biomarker result on the same patients, as a *positive control* to prove my pipeline actually works. And five — directly compare the automated radiomics against the manual clinical biomarkers. Please keep these five in mind, because my conclusions map straight back onto them.

---

## Slide 6 — Dataset · *1:30*

**ON SCREEN:** 137 studies / 55 patients; 39 rejection (27 biopsy-confirmed) / 98 no-rejection; repeated measures → independent dataset of 55.

**SAY:**
> The data comes from Hospital Clínic de Barcelona, collected between 2016 and 2020 on a single Siemens ultrasound system. After excluding one study whose images were never recovered, I have 137 grayscale ultrasound studies from 55 transplant patients. Of those, 39 studies had clinically diagnosed rejection — 27 of them biopsy-confirmed — and 98 had no rejection. So the classes are imbalanced, roughly 72 to 28.
>
> Now, one subtlety that shaped the entire analysis. This is a repeated-measures dataset: many patients were scanned several times over the years — on average two to three studies each — and 14 patients appear in *both* outcome groups at different visits. If I simply pooled all 137 studies as if they were independent, I would be double-counting patients, and that artificially inflates statistical significance and leaks information across cross-validation folds.
>
> So my *primary* analysis takes just **one study per patient** — giving a clean, independent dataset of 55 studies: 34 no-rejection and 21 rejection. The full 137 is kept only as an exploratory supplement in the appendix. If you take one methodological point from this talk, let it be this: statistical independence is why the number 55 matters.

**IF ASKED — "why one per patient and not a mixed-effects model?"**
> A mixed-effects or GEE model is a completely valid alternative and I mention it in the thesis. I chose the one-study-per-patient design because it is the most transparent way to guarantee independence, it mirrors exactly how Bassaganyas structured the clinical comparison, and it avoids modelling assumptions on a modest sample. I then cross-check with a paired within-patient analysis, which is the most conservative use of the repeated measures.

**IF ASKED — "how did you pick which study per patient?"**
> For patients who had both outcomes, I selected their first rejection study, so the rejection group is populated wherever possible; for everyone else, the first available study. That is a fixed, pre-specified rule, not tuned to the result.

---

## Slide 7 — Preprocessing: Isolating the Graft · *1:20*

**ON SCREEN:** `preprocessing_pipeline.png` — four panels (a→d).

**EXPLAIN THE FIGURE** *(this is the diagram on the right — walk through the four panels left to right):*
- **Panel (a) — Original.** A grayscale B-mode ultrasound of the graft with a bright **white contour** that the clinician drew by hand around the pancreas. That contour tells us where the graft is, but the bright line itself would poison any texture measurement, so it has to go.
- **Panel (b) — Binary mask.** I detect the white contour pixels (any pixel bright on all three colour channels, above a threshold of 200), keep only the largest connected white component so I don't grab scale bars or other markings, close small gaps in the line with a morphological operation, fill the enclosed region, and then *subtract the contour line itself*. The result is a solid white mask of the graft interior only — no bright border.
- **Panel (c) — Eroded mask.** I shrink that mask inward slightly, with a 3-by-3 kernel, one iteration. This pulls the region of interest away from the bright tissue edge, so I measure genuine internal texture rather than boundary effects.
- **Panel (d) — Final ROI.** The original image multiplied by that eroded mask — a clean, graft-only region. *This* is what goes into feature extraction.

**SAY:**
> Before I can measure any texture, I have to isolate the graft tissue itself, and cleanly. The figure shows the pipeline on one example study. We start on the left with the original image, where the clinician has drawn a white contour around the graft. I detect that contour, fill the region it encloses, and then subtract the bright line, giving the solid mask in the second panel. I then erode the mask inward slightly — third panel — so I'm not measuring the bright boundary. And the fourth panel is the final result: a clean, graft-only region of interest. Every one of the 137 studies went through this automatically; a couple of tricky cases with broken contours needed a larger gap-closing step, but nothing was extracted by hand.

---

## Slide 8 — Radiomics Feature Extraction · *1:15*

**ON SCREEN:** `correlation_heatmap.png` — 93×93 correlation matrix.

**EXPLAIN THE FIGURE:**
- This is a **93-by-93 correlation matrix** of all the extracted features, computed across the full dataset. Each cell is the Pearson correlation between two features: **red is strong positive correlation, blue is negative**, pale is uncorrelated.
- The eye-catching thing is the **bright red blocks along the diagonal**. Those blocks are *families* of features that all measure closely related things — especially the run-length (GLRLM) and size-zone (GLSZM) texture families. In total, **316 pairs of features correlate above 0.9**.
- The message: the 93 features are highly **redundant** — many are near-duplicates of each other. That matters for the machine learning, because feeding 93 collinear features into a classifier on a small sample invites overfitting. So this heatmap is exactly why I add a correlation filter before modelling.

**SAY:**
> With the graft isolated, I extract the texture features using PyRadiomics — a standard, IBSI-compliant library, so the extraction is reproducible and comparable with other studies. From each graft I compute **93 features** in six families: first-order intensity statistics, and five texture families — GLCM, GLRLM, GLSZM, GLDM and NGTDM — which capture things like coarseness, homogeneity, and contrast. Because ultrasound brightness depends on machine settings like gain and depth, I normalise each image with a per-image z-score first, so I'm comparing texture and not scanner settings.
>
> The heatmap on the right is the correlation structure of those 93 features. All those red blocks mean the features are heavily redundant — 316 pairs correlate above 0.9. That redundancy is why, before machine learning, I filter the set down. In short: each image becomes a 93-number fingerprint of its texture, but there is a lot less independent information there than 93 suggests.

**IF ASKED — "why 2D and no shape features?"**
> Each study is a single ultrasound frame, not a volume, so I extract in 2D. I deliberately disabled shape features, because the visible extent of the pancreas depends on the imaging plane and probe angle — so ROI geometry reflects how the scan was taken, not the graft's real morphology. Including it would have added acquisition noise dressed up as signal.

---

## Slide 9 — Statistical Methodology · *1:15*

**ON SCREEN:** Per-feature test → Shapiro-Wilk → Welch's t / Mann-Whitney U → Benjamini-Hochberg FDR → effect sizes.

**SAY:**
> The first analysis is univariate: for each of the 93 features, does it differ between the rejection and no-rejection groups? For each feature I first run a Shapiro-Wilk test to check whether the distribution is roughly normal. If it is, I use Welch's t-test — Welch's, specifically, because it doesn't assume the two groups have equal variance. If it isn't normal, I use the Mann-Whitney U test. On the independent dataset that split the features roughly in half — 45 got the t-test, 48 got Mann-Whitney.
>
> Now, I'm running 93 tests at once, so by pure chance some will look significant. To control that, I apply Benjamini-Hochberg false-discovery-rate correction across all 93. And I always report effect sizes alongside p-values — Cohen's d or the rank-biserial correlation — because with a modest sample, a p-value on its own can mislead. This is deliberately textbook, defensible methodology. And it is the *same* pipeline I later point at the clinical biomarkers, which is what makes the positive control a fair test.

---

## Slide 10 — Machine-Learning Methodology · *1:25*

**ON SCREEN:** Correlation filter 93→27; Pipeline (Scaler → SelectKBest → classifier); 4 models; joint GridSearchCV; stratified k-fold + LOOCV; bootstrap CIs.

**SAY:**
> A single feature might miss a signal that only shows up when features are combined — so next I built classifiers. First I remove the redundancy we saw in the heatmap: whenever two features correlate above 0.9, I drop the less informative one. That takes 93 down to 27.
>
> Then everything sits inside one scikit-learn pipeline: standardise the features, then SelectKBest picks the top *k* by an ANOVA F-score, then the classifier. The crucial detail is that this **whole pipeline is re-fitted inside every cross-validation fold** — the scaling and the feature selection only ever see the training data — so there is no information leakage into the test fold. I tried four classifiers spanning a range of assumptions: logistic regression, random forest, SVM, and naive Bayes. And I jointly tuned both the number of features *k* and each model's hyperparameters by grid search.
>
> For evaluation I used stratified 10-fold cross-validation as the primary metric, with leave-one-out as a secondary check, and I put bootstrap 95% confidence intervals on every AUC — because with a small sample, the honest question is not "what's the AUC" but "can we distinguish it from 0.5."

**IF ASKED — "how did you prevent leakage?"**
> Feature selection and scaling are inside the CV loop, re-fit on each training fold only. And because the primary evaluation is on the independent dataset — one study per patient — no patient can ever appear in both a training and a test fold. That is the leakage-free design; the full-dataset numbers, where LOOCV can leave other studies from the same patient in training, I report only as exploratory.

---

## Slide 11 — Result 1: No Radiomics Feature Discriminates Rejection · *1:40*

**ON SCREEN:** `boxplots_radiomics_top5.png` (bottom, full width) — top 5 features by lowest p-value, no-rejection (blue) vs rejection (orange).

**EXPLAIN THE FIGURE:**
- These are **five box-and-whisker plots**, side by side. Each panel is one radiomics feature — and specifically the **five features with the *lowest* p-values** on the independent dataset. In other words, these are the *best-case* features, the ones most likely to show something.
- In each panel there are **two boxes: blue is no-rejection (n = 34), orange is rejection (n = 21)**. The box spans the middle 50% of values, the line inside is the median, the whiskers show the spread.
- The thing to point at is that **the blue and orange boxes sit right on top of each other** — heavily overlapping, medians almost level. Even for the strongest features, you could not draw a line that separates rejection from no-rejection.
- The strongest single feature was a first-order intensity percentile at an uncorrected p of 0.004 — but with a small effect size, and it does not survive correction.

**SAY:**
> Here is the first main result, and it is a clean null. After false-discovery-rate correction, **zero of the 93 radiomics features** significantly discriminate rejection. Now, 24 features did dip below an uncorrected p of 0.05 — but that is almost exactly what you would expect from noise across 93 correlated tests, and *none* of them survive correction; the smallest corrected value is around 0.16.
>
> The boxplots make this concrete. These are the five *best* features — the lowest p-values I have. Blue is no-rejection, orange is rejection. And you can see the boxes overlap almost completely; the medians are practically level. Even my strongest features cannot separate the groups. There was a weak hint that rejection cases have slightly *lower* image intensity, but it is small and it washes out under correction. And this is not a quirk of the smaller dataset — the same null holds on the full 137. So at the level of individual features, grayscale texture shows no signal for rejection.

---

## Slide 12 — Result 2: Classifiers Perform at Chance · *1:35*

**ON SCREEN:** `roc_independent_dataset.png` — ROC curves hugging the diagonal.

**EXPLAIN THE FIGURE:**
- This is a **ROC curve** — receiver operating characteristic. The x-axis is the false-positive rate, the y-axis is the true-positive rate. A **perfect classifier** hugs the top-left corner; a classifier that is **guessing randomly** lies along the diagonal dashed line from bottom-left to top-right, which corresponds to an area under the curve, an AUC, of 0.5.
- The point to make: **my curves hug that diagonal.** They wobble a little above and below it, but they never pull away into the top-left. The best area under the curve is 0.636 — and, critically, its 95% confidence interval runs from 0.48 to 0.78, which *crosses 0.5*.
- So visually and numerically, the classifiers are indistinguishable from a coin flip.

**SAY:**
> Machine learning tells exactly the same story. The best classifier was logistic regression, with a cross-validated AUC of 0.636. But look at the confidence interval: 0.48 to 0.78. It crosses 0.5 — which means we cannot statistically distinguish it from random guessing. The other models were similar or worse: random forest at 0.59, naive Bayes at 0.62, and the SVM actually collapsed below chance at 0.41 — it just predicted almost everything as rejection, which is a classic small-sample instability, not a signal.
>
> On the ROC plot, that is what you are seeing: the curves hug the diagonal, the line of pure chance. So combining features multivariately does *not* rescue a signal that was not there feature-by-feature. Now, at this point a very fair worry is: maybe my whole pipeline is simply broken, and it would find nothing no matter what. The next slide answers exactly that.

---

## Slide 13 — Result 3: Positive Control — The Pipeline Works · *1:50*

**ON SCREEN:** `14c_boxplots_arfi_late_period.png` — two ARFI boxplots (median & mean shear-wave velocity) for the late period (>90 days), no-rejection vs rejection, panel titles reading **p < 0.001, r = 0.72 / 0.74**.

**EXPLAIN THE FIGURE:**
- Two boxplots for the **clinical biomarker** ARFI — not radiomics — restricted to the **late post-transplant period, beyond 90 days** (the chronic phase where rejection-related fibrosis has set in). Left panel is **median** shear-wave velocity, right is **mean** — both in metres per second, a direct measure of **tissue stiffness**.
- In each: **blue is no-rejection (n = 33), orange is rejection (n = 19).** The **rejection box sits clearly higher** — the two boxes barely overlap.
- The medians tell the story: stiffness rises from about **0.97 m/s in no-rejection to about 1.46 m/s in rejection**, at **p < 0.001 and a large effect size, r = 0.72** (0.74 for the mean). This is the number that replicates Bassaganyas et al. to three decimal places.
- Contrast this with the *radiomics* boxplots two slides ago, where blue and orange sat on top of each other. Same patients, same pipeline — here there is a real, visible separation; there, none.

**SAY:**
> This is the slide that makes the whole thesis credible. I took the *exact same* statistical pipeline and pointed it at the clinical biomarkers recorded for these same patients. And it works. ARFI elastography — the stiffness measure — clearly separates the groups in the late post-transplant period: you can see the rejection boxes sitting well above the no-rejection boxes. The median stiffness rises from about 0.97 to about 1.46 metres per second, at **p below 0.001** with a large effect size of 0.72. In fact my numbers match the published Bassaganyas result to three decimal places.
>
> Now compare this picture with the radiomics boxplots two slides ago, where the boxes overlapped completely. Same patients, same pipeline — a real signal here, nothing there. And that is the whole logic: my pipeline *can* detect rejection when a real signal is present in the data. So the radiomics null is a genuine finding about grayscale texture — not a bug, and not an underpowered mistake. This positive control is what separates a strong negative result from a weak one.

> *Note: the earlier full-cohort ARFI boxplot (`14b`) still exists — it shows the whole cohort where ARFI is only p≈0.03. The strong late-period separation is what you present here; the full-vs-late breakdown lives on the "ARFI Time-Stratification" backup slide.*

**IF ASKED — "so is ARFI significant or not? your slide 13 says yes and later you say the effect vanishes."**
> Both are true and they are not in conflict — it is a *between-patient* effect, not a *within-patient* one. That is exactly the next slide.

---

## Slide 14 — Why ARFI Works but Radiomics Doesn't · *1:45*

**ON SCREEN:** `21_boxplots_paired_differences_normalised.png` — within-patient difference boxplots (radiomics panels + two ARFI panels), centred on a red zero line.

**EXPLAIN THE FIGURE:**
- This figure asks a different question: for the **14 patients who have both a rejection scan and a non-rejection scan**, what is the *within-patient change*? Each patient acts as their own control.
- Each panel is a boxplot of the **differences** (rejection value minus the same patient's no-rejection value). The **red dashed line is zero — meaning no within-patient change.** The first few panels are radiomics features (blue); the last two are the ARFI biomarkers (gold).
- The thing to point out: **every box straddles that red zero line.** The distributions of differences are centred on zero. In particular, the ARFI panels — which were so strong *between* patients — sit right on zero here. The paired ARFI test gives **p = 0.86**: essentially no within-patient shift.

**SAY:**
> This is my favourite slide, because it is a genuine insight rather than just another null. If ARFI detects rejection so strongly, why can't texture pick up anything — and what is ARFI really measuring? So I looked at the 14 patients who had *both* a rejection scan and a non-rejection scan, and I compared each patient against themselves. That is the most conservative test you can do: every patient is their own control.
>
> The figure shows the within-patient differences. The red line is zero — no change. And every box straddles it. Look at the ARFI panels on the right in particular: between patients ARFI was highly significant, but *within* a patient the difference is essentially nothing — p equals 0.86.
>
> That reframes the entire result. The strong ARFI signal is a **between-patient** effect: patients who go on to reject tend to have *baseline* stiffer grafts in the late period, a chronic property — rather than the stiffness jumping up transiently at the moment of rejection. So grayscale texture is being asked to catch a transient, cross-sectional change that may simply not exist in a form the pixels can capture. I present this as hypothesis-generating — it is a small paired sample of 14 — but it is a coherent, mechanistic explanation, and it ties the whole story together.

---

## Slide 15 — Robustness: The Null Holds Every Way I Tested It · *1:20*

**ON SCREEN:** `23_surrounding_mask_examples.png` — graft (red) and surrounding ring (blue) overlays on three studies.

**EXPLAIN THE FIGURE:**
- Three example ultrasound images, each with two coloured overlays: the **red region is the pancreas graft**, and the **blue ring is the tissue immediately surrounding it** — made by dilating the graft mask outward by 10 pixels and subtracting the graft itself, excluding anything outside the ultrasound cone.
- The idea being illustrated: use that surrounding ring as a **local brightness reference**. If differences in gain or depth between scans were hiding a real texture signal, then normalising the graft against its own neighbouring tissue — which was scanned under identical settings — should *reveal* it. It didn't. Performance stayed at chance. So acquisition variability is ruled out as the culprit.

**SAY:**
> I did not want this null to rest on any single modelling choice, so I attacked it from four directions. First, the paired within-patient radiomics analysis — no signal. Second, I went beyond PyRadiomics entirely and added three completely different texture families — Local Binary Patterns, Gabor filters, and Laws' texture energy — 153 features in total — and still no signal survived correction. Third, the surrounding-tissue normalisation shown here: I used the ring of tissue around the graft as a local reference, in case scanner settings were washing out a real difference — and performance stayed at chance, if anything slightly worse. And fourth, the full 137-study dataset as an exploratory check — same null.
>
> When a result is that stable — across preprocessing, across feature type, across dataset, across statistical design — you can be confident it is real, and not an artefact of one arbitrary decision. That robustness is a big part of why I stand behind the conclusion.

**IF ASKED — "did any alternative feature family do better?"**
> Laws' texture energy had the highest single-family AUC at 0.651 — but its confidence interval, 0.50 to 0.80, still includes chance, and nothing survived FDR correction. Across all three families, the significant-feature counts were at or below what you'd expect by chance. So no, nothing meaningfully beat the coin flip.

---

## Slide 16 — Discussion: What the Negative Result Means · *1:15*

**ON SCREEN:** Grayscale texture doesn't encode rejection; the signal lives in stiffness & perfusion; well-controlled negative result; clinically useful.

**SAY:**
> So what does this mean? The interpretation is that the information distinguishing rejection lives in the *physical tissue properties* that specialised ultrasound measures — stiffness through ARFI, and perfusion through contrast ultrasound — and those properties are simply *not* encoded in the brightness-texture patterns of a standard B-mode image. Radiomics can only work with what is actually in the pixels, and for this problem, that signal is not there.
>
> I want to frame this as a strength, not a disappointment. This is a *well-controlled* negative result: the pipeline is validated by the ARFI positive control, and the null survives every robustness check I threw at it. A negative result with a working control is far more informative than a noisy, over-fit positive one — and far more honest. And it is clinically useful: it tells the field not to chase a cheap grayscale-radiomics shortcut, and to keep investing in the biomarkers that genuinely work.

---

## Slide 17 — Limitations · *1:05*

**ON SCREEN:** Modest sample / single centre; 2D single-frame; clinical label; class imbalance; retrospective, hand-drawn ROIs.

**SAY:**
> I want to be upfront about the limitations, because they are real. The sample is modest and from a single centre, so I cannot claim this generalises everywhere. The images are 2D single frames, so I am not capturing volumetric or temporal texture that a full 3D scan or a cine loop might contain. My outcome label is *clinical* rejection, and only 27 of the 39 rejection cases were biopsy-confirmed, so there is some label noise. The classes are imbalanced, and it is retrospective with hand-drawn regions, which adds variability.
>
> But here is my key defence. *None* of these fully explains the null — because the positive control worked on the very same data, with the very same limitations. The same modest, imbalanced, single-centre, hand-drawn dataset was perfectly able to reveal the ARFI signal. So the limitations qualify how far the finding generalises, but they do not undermine the core conclusion.

---

## Slide 18 — Conclusions · *1:05*

**ON SCREEN:** Radiomics doesn't detect rejection; classifiers at chance; pipeline validated; ARFI is baseline stiffness; biomarkers remain necessary.

**SAY:**
> To conclude, mapping back to my five objectives. I built the extraction pipeline and the statistical and machine-learning analyses — objectives one to three. The answer to the central question is **no**: automated grayscale radiomics does not detect pancreas rejection — no feature survived correction, and every classifier performed at chance. Objective four, the control, succeeded and validated everything — I reproduced the ARFI result at p below 0.001 and effect size 0.72. And objective five, the comparison, produced the real insight: that the ARFI signal is a between-patient baseline-stiffness effect, not a transient change.
>
> So the bottom line for the clinic is this: the specialised biomarkers that measure stiffness and perfusion remain necessary for non-invasive rejection monitoring. A texture shortcut on ordinary images will not replace them.

---

## Slide 19 — Future Work & Thank You · *0:45*

**ON SCREEN:** Deep learning; multi-parametric fusion; larger multi-centre prospective cohorts; volumetric/temporal US; Thank you.

**SAY:**
> Briefly, where could this go? Deep learning on the raw images might find representations that hand-crafted texture misses, though it would need more data. Fusing B-mode with ARFI and perfusion into a multi-parametric model is probably the most promising clinical direction. Larger, multi-centre, prospective cohorts with biopsy-confirmed labels would settle generalisability. And moving to 3D or cine-loop ultrasound would add the temporal texture I could not access here.
>
> That is the end of my talk. Thank you for your attention — and thank you to Gemma for supervising this work, and to the clinical team at Hospital Clínic. I am very happy to take your questions.

*[Breathe. Smile. Wait for the first question. It is completely fine to pause and think before answering, and fine to say "that's a good question, let me reason through it." If you don't know something, say what you'd need to check.]*

---

# Q&A Preparation — likely questions, answers, and which backup slide

*Jump to a backup slide only if it genuinely helps; otherwise just answer.*

**Q: Why is your sample only 55 when you have 137 studies? Isn't that throwing away data?**
→ Independence. Pooling 137 double-counts the 14 patients in both groups and leaks across CV folds. One-per-patient guarantees clean inference; the full 137 is in the appendix and reaches the *same* null, so nothing is lost in the conclusion. **Backup B4 (full vs independent).**

**Q: Could the negative result just be low power / small sample?**
→ Three reasons it isn't just power: (1) the *same-sized* data revealed ARFI at p<0.001 — power was sufficient for a real effect; (2) the null replicates on the full 137; (3) effect sizes are tiny and distributions overlap, not "borderline." **Backup B1 (stats detail).**

**Q: Maybe PyRadiomics is the wrong feature set?**
→ Tested exactly that: three independent texture families (LBP, Gabor, Laws' — 153 features) all null; best family (Laws') AUC 0.651 with CI crossing chance. Ruling out "wrong features." **Backup B3 / robustness slide.**

**Q: Could acquisition settings (gain/depth) be hiding the signal?**
→ Surrounding-tissue normalisation tested this — normalise the graft against its own neighbouring tissue, same acquisition. Stayed at chance, slightly worse. Rules out acquisition confound. **Slide 15.**

**Q: How do you know your pipeline isn't just broken?**
→ The positive control. Same pipeline reproduces Bassaganyas' ARFI/DCE-US result to 3 decimal places. **Slide 13 / Backup B2.**

**Q: Your slide says ARFI p<0.001 but also that ARFI "disappears" — which is it?**
→ Between-patient vs within-patient. Cross-sectionally (between patients, late period) ARFI is strongly significant. Paired within-patient it's p=0.86. Interpretation: rejecting patients have chronically stiffer grafts (baseline), not a transient jump. **Slide 14.**

**Q: Isn't ARFI significant only in the late period? Your full-cohort number is p≈0.03.**
→ Correct, and that's the honest framing. Full cohort: ARFI median p=0.028. Early period (≤90d): nothing significant. Late (>90 days, chronic-phase fibrosis): p<0.001, r=0.72, 0.97→1.46 m/s, plus 4 DCE-US parameters — matching the published cutoff and result. The effect is time-dependent. **Backup B2b (time-stratification).**

**Q: Why did SVM go below chance (0.41)?**
→ Small-sample instability with class imbalance — it collapsed to predicting nearly all-rejection (sensitivity 1.0, specificity 0.03). Not a real inverse signal; a degenerate solution. Balanced class weights were on; the CI [0.25, 0.58] includes chance. **Backup B3.**

**Q: Did you address multiple testing / leakage properly?**
→ Benjamini-Hochberg FDR across all features; feature selection and scaling re-fit inside every CV fold; primary evaluation on one-per-patient data so no patient spans train/test. **Slides 9–10.**

**Q: Clinical label is not all biopsy-confirmed — doesn't that undermine it?**
→ 27/39 biopsy-confirmed; rest clinical, because biopsy isn't routine. It's a limitation (label noise), but the same label was sufficient for ARFI to work — so noise didn't prevent detecting a *real* signal. **Slide 17.**

**Q: Why disable shape features?**
→ ROI extent reflects imaging plane/probe angle, not true graft morphology — shape would encode acquisition, not biology. **Slide 8 / IF ASKED note.**

**Q: What would make radiomics work here — is it hopeless?**
→ Not necessarily hopeless: deep features, multi-parametric fusion, 3D/temporal data, and larger cohorts are all untested here. But grayscale hand-crafted texture, as tested thoroughly, does not carry the signal. **Slide 19.**

---

# Backup slides — what each one is for

These live **after** the "Thank you" slide and are **not presented**. They are a reference reservoir: if a question needs a number or a figure, you jump straight to the relevant one, then jump back. Announce it naturally — *"I actually have a backup slide on that…"*

- **B1 — Statistical Detail:** full independent-dataset stats setup; per-feature p-value comparison (full vs independent); the fact that nothing reaches q<0.05. *For deep statistics questions.*
- **B2 — Clinical Biomarker Replication:** the Bassaganyas replication, ARFI p<0.001 / r=0.72 late period, DCE-US parameters, 3-decimal match. *For "is the pipeline valid / is ARFI really significant" questions.*
- **B2b — ARFI Time-Stratification (new):** full cohort (p≈0.03) → early period (null) → late period (8 features significant, ARFI p<0.001, 0.97→1.46 m/s). *For "isn't ARFI only significant in the late period?" — the single most likely deep question.*
- **B3 — ML Configuration & Results:** correlation filter, SelectKBest, the four AUCs (LogReg 0.636, RF 0.588, NB 0.618, SVM 0.408), 1000-resample bootstrap CIs, sens/spec and why SVM collapsed. *For ML questions.*
- **B4 — Full Dataset (137) Exploratory:** why 137 violates independence, and that it reaches the same null anyway. *For "why not use all the data" questions.*

---

# Final-day checklist

- [ ] Slides open correctly on the room machine (bring a PDF export as backup, plus the .pptx on a USB).
- [x] Slide-13 ARFI figure resolved — now the late-period boxplot (p<0.001, r=0.72), matching the spoken headline.
- [ ] Rehearse aloud twice with a timer; note where you naturally run long.
- [ ] Water on the table; a printed copy of this script.
- [ ] Know your first sentence (slide 1) and your last sentence (slide 19) cold.
- [ ] Pauses are your friend. You are the expert on this work in the room.
