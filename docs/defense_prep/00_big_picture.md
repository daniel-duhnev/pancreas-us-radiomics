# M0 · The Big Picture

Goal of this module: be able to say what your thesis did, why, and what you found — in 60
seconds, in 5 minutes, and in one sentence. If you can only prepare one thing, prepare this.

---

## The one-sentence version

> "I tested whether automated texture analysis (radiomics) of ordinary grayscale ultrasound can
> detect pancreas transplant rejection. It cannot — but I proved that finding is real, not a bug,
> by showing the same pipeline *does* recover the known clinical-biomarker signal (ARFI/DCE-US)."

## The 60-second pitch (memorise the beats, not the words)

1. **Problem.** Pancreas transplant patients can reject the graft. The gold-standard test is
   biopsy — invasive, risky, and prone to sampling error. We want a non-invasive alternative.
2. **Opportunity.** Ultrasound is already done routinely. A recent study (Bassaganyas et al. 2025)
   showed two *specialised* ultrasound modes — ARFI elastography and DCE-US — can flag rejection.
   But those need special acquisition and manual measurement.
3. **My question.** Can I skip the specialised modes and instead extract *radiomics* texture
   features from the plain grayscale B-mode image that's captured anyway — and predict rejection
   automatically?
4. **What I did.** Built a preprocessing + PyRadiomics pipeline, extracted 93 texture features
   from 137 studies (55 patients), tested each statistically, and trained four ML classifiers —
   all on an *independent* one-study-per-patient dataset to respect the repeated-measures structure.
5. **What I found.** Nothing discriminates rejection. No feature survives multiple-testing
   correction; best classifier AUC is 0.636 with a confidence interval that includes chance (0.5).
   I confirmed this with alternative texture families and tissue normalisation — all null.
6. **Why it's trustworthy (the punchline).** The *same* pipeline reproduced the published ARFI
   result to three decimal places (ARFI p < 0.001 in the late period). So the pipeline works; the
   texture signal genuinely isn't there in B-mode.
7. **Takeaway.** Rejection changes tissue *stiffness* and *perfusion* — which ARFI and DCE-US
   measure directly — but not the acoustic-boundary *texture* that B-mode encodes. Future work:
   deep learning, multi-parametric models, larger multi-centre cohorts.

---

## The five objectives (know these verbatim-ish)

Your introduction states five objectives. Committees love asking "did you meet your objectives?"

1. **Extract** radiomics features from pancreas transplant ultrasound (build the pipeline).
2. **Test** whether individual features discriminate rejection (univariate statistics).
3. **Build** ML classifiers and evaluate predictive performance (multivariate).
4. **Reproduce** the clinical-biomarker analysis of Bassaganyas et al. (positive control).
5. **Compare** automated radiomics vs manual clinical biomarkers.

**Your answer to "did you meet them?":** Yes to all five. 1–3 gave a robust negative result,
4 validated the pipeline, and 5 showed clinical biomarkers work where radiomics doesn't. The
negative outcome of objectives 2–3 is a *finding*, not a failure — objective 4 is what makes that
claim credible.

---

## Why a negative result is a real contribution

You *will* be asked some version of "isn't this just a failed experiment?" Your answer:

- **It narrows the search space.** The field now knows hand-crafted texture features on B-mode
  are unlikely to work for pancreas rejection — so resources should go elsewhere (deep learning,
  multi-parametric). That is useful scientific information.
- **It's a rigorously *established* negative, not an *inconclusive* one.** The positive control
  proves the method could have detected a signal if one existed. Most "failed" projects can't
  distinguish "no signal" from "broken pipeline." Yours can.
- **It has a mechanistic explanation** (see M5): B-mode texture encodes macroscopic acoustic
  boundaries; rejection is microscopic. The negative result is *predicted* by the physics, which
  makes it believable rather than mysterious.
- **Publication bias makes negatives scarce and valuable.** Well-controlled negative results
  prevent others from wasting effort repeating the same dead end.

---

## The shape of the evidence (why it's robust)

Every one of these independent analyses points the same way — that convergence is your strength:

| Analysis | Result |
|----------|--------|
| Univariate tests, independent dataset (n=55) | No feature survives FDR |
| ML classifiers (4 models), independent dataset | AUC ≈ chance (best 0.636, CI includes 0.5) |
| Time-stratified (early ≤90d / late >90d) | No consistent signal |
| Paired within-patient (14 patients) | No feature survives FDR |
| Alternative textures (LBP, Gabor, Laws', 153 features) | All null |
| Surrounding-tissue normalisation | Null / slightly worse |
| **Clinical biomarkers (positive control)** | **ARFI p < 0.001 late period — signal recovered** |

The last row is the load-bearing one. Say it every time you describe the negative result.

---

## Quick self-check

- Can you give the 60-second pitch without notes?
- Can you list the five objectives and say you met all five?
- Can you answer "isn't this a failed experiment?" in three sentences?
- Can you name the positive control and why it matters?

If yes to all four, you own the big picture. Move to M1.
