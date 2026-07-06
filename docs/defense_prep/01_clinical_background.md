# M1 · Clinical Background (from first principles)

Goal: explain the clinical problem well enough that a clinician on the committee (or Gemma) trusts
you understand *why* this matters, not just the ML. Most of this is standard background — the
thesis-specific facts are flagged with **[THESIS]**.

---

## 1. Why pancreas transplantation exists

- **Type 1 diabetes (T1D):** the immune system destroys the insulin-producing β-cells in the
  pancreas. Without insulin, blood glucose is uncontrolled → long-term damage to eyes, kidneys,
  nerves, blood vessels.
- A **pancreas transplant** replaces that endocrine function with a donor pancreas, restoring
  natural, glucose-responsive insulin production. **[THESIS]** It is the only established treatment
  that can restore long-term *normoglycaemia* (normal blood sugar) and free the patient from
  injected insulin. Often done together with a kidney transplant (many T1D patients also have
  kidney failure).
- The catch: the recipient's immune system sees the donor organ as foreign and attacks it →
  **graft rejection**.

## 2. What "rejection" actually is

Rejection = the recipient's immune system damaging the transplanted organ. Three types (know all
three — a clinician may ask):

1. **Acute T-cell-mediated rejection:** T-lymphocytes infiltrate the graft (the classic acute
   attack). Most treatable if caught early.
2. **Antibody-mediated rejection:** the recipient makes antibodies against the donor tissue;
   damages the graft's small blood vessels.
3. **Chronic rejection:** slow, progressive **fibrosis** (scarring) and loss of function over
   months/years.

**[THESIS]** Rejection remains the leading cause of graft failure beyond the first 90 days and
affects ~20% of grafts within the first year. Patients are kept on **immunosuppressant** drugs to
suppress this; catching rejection early lets clinicians adjust immunosuppression before damage is
irreversible.

**Why detection is hard:** rejection can be **subclinical** (no symptoms), and routine blood
markers (serum amylase, lipase, glucose) are **non-specific** — they rise for many reasons, not
just rejection. So you can't reliably diagnose rejection from a blood test.

### The histology (what rejection looks like under a microscope) — matters for M5

Rejection shows up as: inflammation of the acinar parenchyma (the enzyme-producing tissue),
**oedema** (fluid swelling), **venulitis** (inflammation of small veins), and progressive
**fibrosis**. **Key point for later:** these are *microscopic, cellular-level* changes. Hold that
thought — it's the whole explanation for your negative result (M5).

## 3. The reference standard: biopsy (and why it's a problem)

- **Percutaneous biopsy** = pushing a needle through the skin to take a tissue sample, then
  grading it histologically under the **Banff schema** (the standardised grading system for
  transplant rejection). This is the **gold standard** — it gives direct histological proof.
- **[THESIS]** But biopsy has serious drawbacks:
  - **Invasive / risky:** bleeding, pancreatitis, fistula formation.
  - **Access:** the pancreas graft sits deep in the abdomen, not always reachable.
  - **Sampling error:** rejection can be focal; if the needle misses the affected region, you get
    a false negative.
  - **[THESIS]** In practice, a multi-centre survey found biopsy is actually performed in only a
    minority of suspected rejection episodes, because of these barriers.
- **Consequence:** there is a real clinical need for a **non-invasive** test to decide who actually
  needs a biopsy. That is the gap your thesis addresses.

## 4. Ultrasound: the three tools

Ultrasound works by sending sound pulses into tissue and listening to the echoes. Different
*modes* extract different physical information. Understand what each **physically measures** —
this is the crux of your whole argument.

### (a) B-mode (conventional grayscale ultrasound) — what radiomics uses

- **What it is:** the standard grayscale image. Brightness at each pixel = strength of the echo
  returned from that location.
- **What creates the echo (crucial):** echoes come from **boundaries where acoustic impedance
  changes**. *Acoustic impedance* = tissue density × speed of sound in that tissue. Where two
  tissues with different impedance meet, sound reflects back. So B-mode texture encodes
  **macroscopic structural interfaces between tissue types**.
- **[THESIS]** Spatial resolution is roughly **0.5–2 mm** axially. So B-mode literally cannot
  "see" cellular-scale changes.
- **Role in your thesis:** this is the image you extract radiomics texture from. Routinely captured,
  no special protocol — that's *why* it would be attractive if it worked.

### (b) ARFI elastography — measures STIFFNESS

- **ARFI = Acoustic Radiation Force Impulse.** A strong focused ultrasound "push" pulse displaces
  the tissue slightly; the scanner then measures how fast the resulting **shear wave** travels
  sideways through the tissue.
- **Physics:** stiffer tissue → faster shear wave. Reported as **shear-wave velocity in m/s**.
- **Why it's relevant:** inflammation and fibrosis make the graft **stiffer** → higher velocity.
  So ARFI measures a property (stiffness) that rejection directly changes.
- **[THESIS]** Four ARFI numbers were recorded per study: median, mean, standard deviation (DE),
  and interquartile range (RIQ) of the shear-wave velocity measurements. ARFI available for
  121/138 studies (some failed a quality filter: IQR/median ratio > 0.3 were excluded at source).

### (c) DCE-US — measures PERFUSION (blood flow)

- **DCE-US = Dynamic Contrast-Enhanced Ultrasound.** Inject a **microbubble contrast agent** into
  a vein; the bubbles reflect ultrasound strongly. Watch them wash into and out of the graft over
  time → a **time–intensity curve** for each region.
- **Physics:** the shape of that curve reflects **microvascular perfusion** (how well blood flows
  through the graft). Rejection damages small vessels → reduced/altered perfusion.
- **[THESIS]** Thirteen parameters were derived from the curves, describing wash-in (contrast
  arrival/peak: e.g. PE peak enhancement, WiAUC wash-in area, RT rise time, TTP time-to-peak),
  wash-out (clearance: WoAUC, WoR, FT), and overall perfusion (WiPi, WiWoAUC, mTTI, QOF, Area).
  DCE-US available for 127/138 studies.

**The 17 clinical features = 4 ARFI + 13 DCE-US.** You don't need every abbreviation memorised,
but know the *categories* and that ARFI = stiffness, DCE-US = perfusion.

## 5. The prior work you build on: Bassaganyas et al. 2025

- **[THESIS]** Same hospital (Hospital Clínic Barcelona), **same patient cohort**, same scanner
  (Siemens Acuson S3000 Helx), same imaging protocol as your thesis.
- They ran the **first prospective study combining ARFI + DCE-US in pancreas transplant.** Finding:
  after the initial 90-day post-op period, rejection was associated with **higher stiffness**
  (ARFI median 1.46 vs 0.97 m/s, p < 0.001) and **lower perfusion** (several DCE-US params p < 0.05).
  Their combined score reached an odds ratio of ~23 for rejection.
- **Why this matters to you:** their positive result is exactly what your pipeline *reproduces* as
  a positive control. You are not competing with them — you're testing whether a *cheaper, automated*
  approach (radiomics on B-mode) can match their specialised, manual approach. It can't, and your
  replication of their numbers proves your machinery is sound.

## 6. The 90-day cutoff (know why it exists)

- The **first 90 days** post-transplant are noisy: surgical healing, post-op oedema, and
  peri-operative changes swamp any rejection signal.
- After 90 days ("**late period**") the graft has settled, so rejection-related changes (stiffness,
  perfusion) become detectable.
- **[THESIS]** Both your analysis and Bassaganyas use the same **90-day cutoff** for the late
  period. This is why ARFI is significant *only* in the late subset, not on the full dataset. Keep
  this straight — it comes up in your results.

---

## Common clinical questions you should be ready for

- *"Why not just biopsy everyone?"* → Invasive, risky, deep graft, sampling error, low real-world
  uptake. The point is a non-invasive triage tool.
- *"What does ARFI actually measure, physically?"* → Shear-wave velocity = tissue stiffness.
- *"What does DCE-US measure?"* → Microvascular perfusion via microbubble wash-in/wash-out curves.
- *"Why grayscale B-mode for radiomics and not ARFI images?"* → B-mode is captured routinely with
  no special protocol; if texture worked, it'd be a free, automatic biomarker. Testing that is the
  whole point.
- *"What's the difference between the rejection types?"* → T-cell-mediated (acute), antibody-mediated,
  chronic (fibrosis). Your outcome variable is binary clinical rejection, not typed (a limitation).

---

## Quick self-check

- Explain acoustic impedance and what B-mode texture encodes.
- Say what ARFI and DCE-US each measure and why rejection would change them.
- Give three reasons biopsy is inadequate.
- Explain the 90-day cutoff.
- State what Bassaganyas et al. found and how it relates to your work.
