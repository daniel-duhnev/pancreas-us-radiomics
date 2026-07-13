# M5 · Narrative & Interpretation

Goal: tie every result into one coherent story that a committee finds *convincing*. The facts are in
M4; this module is about **meaning**. If M4 is the "what," this is the "so what." A defense is won or
lost here.

---

## 1. The central claim, stated cleanly

> Radiomics texture features from grayscale B-mode ultrasound do **not** discriminate pancreas
> transplant rejection. This is a **robust, mechanistically-explained negative result**, validated
> by a positive control on the same data.

Three words to keep saying: **robust** (holds across every analysis), **mechanistic** (the physics
predicts it), **controlled** (the positive control proves the statistical analysis is sound and
powered).

---

## 2. The physical explanation — the heart of your defense

This is the single most important idea to internalise. If you can explain *why*, physically, the
result almost had to come out negative, the committee stops seeing "failure" and starts seeing
"insight."

**How B-mode makes an image:** echoes come from **boundaries where acoustic impedance changes**
(acoustic impedance = tissue density × speed of sound). So B-mode texture encodes **macroscopic
structural interfaces between tissue types** — at a spatial resolution of only ~**0.5–2 mm**.

**What rejection actually is, physically:** **microscopic** changes — inflammatory cell infiltration
of the acinar parenchyma, interstitial oedema, venulitis, and (later) fibrosis. These happen at the
**cellular/interstitial scale**, well below B-mode's resolution, and they don't necessarily create
new **acoustic-impedance boundaries** that a texture feature could pick up.

**Therefore:** B-mode texture is looking at the wrong physical property, at the wrong scale.
The negative result isn't a surprise — it's what the image-formation physics predicts.

**By contrast, why ARFI and DCE-US succeed:**
- **ARFI measures stiffness** (shear-wave velocity). Inflammation and fibrosis *directly* increase
  parenchymal stiffness → a directly measurable change.
- **DCE-US measures perfusion** (microbubble dynamics). Rejection-related vascular damage *directly*
  reduces blood flow → a measurable change.

Both access physical properties **proximal to the pathophysiology** of rejection. B-mode texture is
**distal** to it. That's the whole story in one line:

> "Rejection changes tissue stiffness and perfusion, not the acoustic-boundary texture that grayscale
> ultrasound encodes — so the modalities that measure stiffness and perfusion work, and texture
> doesn't."

**Supporting context:** radiomics *has* worked on ultrasound for liver fibrosis, thyroid nodules,
breast lesions — but those involve **larger, focal structural changes** (nodules, architectural
distortion, advanced fibrosis). Early diffuse rejection has no focal lesion with texture contrast, so
texture-based methods are fundamentally limited here.

---

## 3. The positive control — why anyone should believe your negative

A negative result is only worth anything if you can rule out "your analysis was just broken or too
weak." You can — but be **precise about scope**, because a sharp examiner will test it:

- Your radiomics features and the clinical ARFI/DCE-US measurements come from the **same patients**,
  with the **same rejection labels and grouping**, and go through the **same statistical analysis**.
- That analysis found *nothing* in the radiomics features but **reproduced Bassaganyas et al. to 3
  decimal places** in the clinical measurements (ARFI late p < 0.001, r = 0.72; 10/12 features match
  exactly).
- Since the analysis and the labelled cohort are identical for both feature sets, the difference must
  lie in the **features**, not the analysis. The statistics demonstrably **can** detect a real signal
  in this cohort at this sample size → the radiomics null isn't a broken or underpowered analysis.

**This is your answer to "how do you know it's not just underpowered / a stats bug?"** — power and
correctness of the *statistical analysis* are demonstrated, not assumed.

**What the positive control does NOT cover (say this before they do).** The clinical measurements are
tabular numbers that **never pass through your segmentation or PyRadiomics extraction**. So the
control validates the statistical + data-handling stage, **not** the image-processing pipeline. The
imaging stage is defended *separately*: three independent feature descriptors (PyRadiomics, LBP,
Gabor, Laws') are all null — a single extraction bug wouldn't fool all three — plus error-free
extraction, sensible feature distributions, and visual mask QC. Honest residual limitation: those
texture methods share the same segmentation masks, so there is **no dedicated positive control for
the imaging stage itself**. Concede that cleanly; it reads as rigour, not weakness. (Full defense in
M6.)

---

## 4. The between-patient vs within-patient insight (your original contribution)

This is the most intellectually interesting finding — and it goes *beyond* Bassaganyas. Make sure you
can tell it.

**The observation:** ARFI is strongly significant in the unpaired late-period analysis (**p < 0.001**),
but in the **paired** within-patient analysis (14 patients who had both outcomes) it **collapses to
p = 0.86**. And on the independent one-per-patient dataset it's also non-significant (p = 0.69).

**What this means:** the ARFI signal is a **between-patient** effect, not a **within-patient** one.
Interpretation: patients who eventually reject may simply have **inherently stiffer grafts** (donor
factors, surgical factors, pre-existing subclinical fibrosis) — a *stable baseline* difference — rather
than ARFI detecting the acute rejection episode itself. When each patient is their own control, the
difference disappears.

**The nuance to state (don't overclaim):**
- This reframes ARFI as potentially a **risk-stratification** tool (who is at higher risk) more than a
  **diagnostic** test for an active episode.
- **Alternative explanation:** the paired test has only 14 pairs (12 with ARFI) → it may simply be
  **underpowered** to detect a real within-patient change. You cannot resolve this with 14 pairs.
- Bassaganyas used unpaired comparisons throughout and did **not** examine this. So it's a genuine,
  **hypothesis-generating** observation from your work — worth investigating in larger longitudinal
  cohorts. Present it with appropriate humility and it becomes a strength.

**Why it strengthens your thesis:** it shows you didn't just run a pipeline — you interrogated the
*structure* of the signal and found something the original authors missed. That's the mark of a
thoughtful analysis.

---

## 5. Why the negative result is valuable (rehearse this)

- **Scientific value:** it **narrows the search space** — the field now knows hand-crafted texture on
  B-mode is a dead end for pancreas rejection, so effort should go to deep learning / multi-parametric
  models. Negative results prevent wasted duplication.
- **Clinical value:** it confirms specialised modes (ARFI, DCE-US) **remain necessary** — automated
  analysis of routine grayscale can't replace them yet.
- **Methodological value:** the positive control + robustness across six analyses is a template for how
  to establish a *credible* negative result (most can't distinguish "no signal" from "bad method").

---

## 6. How the pieces fit (one mental map)

```
Clinical need: non-invasive rejection detection (biopsy is bad)
        │
        ├── Specialised US (ARFI stiffness, DCE-US perfusion) → WORKS  ← Bassaganyas + your replication
        │
        └── Cheap automated alternative: radiomics texture on B-mode → your question
                    │
                    ├── univariate (independent n=55) → 0 survive FDR
                    ├── ML (4 models) → AUC ≈ chance (0.636, CI incl. 0.5)
                    ├── time-stratified → no consistent signal
                    ├── paired within-patient → 0 survive FDR
                    ├── alt. features (LBP/Gabor/Laws') → null   ← rules out "wrong features"
                    └── surrounding normalisation → null          ← rules out "acquisition noise"
                              │
                              ▼
        WHY: B-mode texture = macroscopic acoustic boundaries; rejection = microscopic
             → wrong property, wrong scale. ARFI/DCE-US measure the right properties.
                              │
                              ▼
        Bonus insight: ARFI is a between-patient (baseline stiffness) effect, not within-patient
                       (paired p=0.86) → risk marker more than acute-episode diagnostic.
```

---

## 7. The three sentences to end your talk on

1. "Automated texture analysis of grayscale ultrasound does not capture the tissue changes of pancreas
   transplant rejection — and I showed this robustly, with a positive control confirming my analysis is
   sound and powered to detect a real signal when one exists."
2. "The reason is physical: B-mode texture encodes macroscopic acoustic boundaries, while rejection is
   a microscopic change in stiffness and perfusion that ARFI and DCE-US measure directly."
3. "So clinical biomarkers remain necessary, and future non-invasive work should target those physical
   properties — via deep learning, multi-parametric imaging, and larger multi-centre cohorts."

---

## Quick self-check

- Explain, physically, why B-mode texture can't see rejection but ARFI/DCE-US can — in under a minute.
- Explain the role of the positive control in one sentence.
- Tell the between-/within-patient ARFI story, including the underpowered caveat.
- Give three reasons the negative result is valuable.
- Close your talk with the three summary sentences from memory.
