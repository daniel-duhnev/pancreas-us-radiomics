# M2 · Radiomics & the Imaging Pipeline (from first principles)

Goal: explain what radiomics is, walk through your preprocessing pipeline step by step, and
justify **every** feature-extraction setting. This is the module a technical committee member
(e.g. Miguel Ángel González Ballester, whose field is medical image analysis) is most likely to
probe. **[THESIS]** marks facts specific to your work.

---

## 1. What radiomics is (first principles)

- **Idea:** convert a medical image into a large table of **quantitative numbers** ("features")
  describing texture, intensity, and spatial heterogeneity — patterns often too subtle for the eye.
- **Premise:** disease alters tissue microstructure, which *might* show up as changes in these
  texture numbers even when a radiologist can't see a difference.
- **Standard workflow:** acquire image → segment a region of interest (ROI) → preprocess →
  extract features → select features → statistical/ML analysis. Your thesis follows exactly this.
- **Standardisation:** the **IBSI** (Image Biomarker Standardisation Initiative) defined and
  standardised radiomics features so results are comparable across studies. **[THESIS]** You used
  **PyRadiomics** (thesis states v3.0.1), an IBSI-compliant open-source library. Say "IBSI-compliant"
  — it signals you used standard, defensible definitions rather than home-made features.
- **Origin:** radiomics came from oncology on **CT and MRI** (where intensity is calibrated —
  Hounsfield units in CT). Applying it to **ultrasound** is harder (see §5) and is part of what
  makes your negative result plausible.

## 2. The problem the preprocessing solves

**[THESIS]** The raw DICOM images have a **white contour** drawn by the clinician around the
pancreas graft (the ROI annotation). If you fed that straight into radiomics, the bright contour
line would create artificial high-intensity texture and corrupt every feature. So the pipeline's
job: **keep the tissue inside the contour, throw away the contour line itself.**

## 3. The preprocessing pipeline, step by step

Know this cold — you may be asked to "walk me through your preprocessing." **[THESIS]** all steps:

1. **Load DICOM as RGB; detect white pixels.** A pixel is "contour" if its value exceeds **200 on
   all three colour channels** (R, G, B all > 200) — i.e. bright white.
2. **Keep the largest connected component.** Images contain other white marks (scale bars, UI
   elements). Taking only the largest connected blob of white pixels isolates the clinician's
   contour.
3. **Morphological closing** with a **10×10** square structuring element. Closing = dilate then
   erode; it **bridges small gaps** in the drawn line so the contour becomes a continuous closed
   loop.
4. **Fill and subtract.** Fill the closed loop → a solid mask of the whole annotated region. Then
   **subtract the original contour pixels** so the final mask is the tissue *interior only*, without
   the bright border.
5. **Grayscale conversion.** Convert the RGB image to grayscale for feature extraction.
6. **Mask erosion** with a **3×3** kernel, **1 iteration** (this is the "K3 I1" in the data folder
   name). Shrinks the mask slightly to remove any residual boundary/partial-contour artifacts at
   the tissue–background edge.

**Output per study:** a binary mask + a segmented grayscale image (original × mask). These feed
radiomics extraction.

### The two edge cases (be honest about this one)

**[THESIS]** Two studies (**03_01** and **43_01**) had contours with **large gaps** that the normal
10×10 closing couldn't bridge → the fill collapsed → empty masks. Fix: a much larger **35×35**
closing kernel to force the gaps closed. The pipeline also auto-detects/corrects mask–image
dimension mismatches (transpose or nearest-neighbour resize).

> **Audit note (know this):** in the code, these two edge cases were integrated partly by a manual
> out-of-band file step rather than fully in code, and the manifest still listed them with 0 pixels.
> It doesn't change any result (both studies are included and processed), but if pushed on
> reproducibility, acknowledge it's a documented rough edge, not a silent error. See M6.

## 4. Feature extraction settings — and the reason for each

**[THESIS]** You must be able to justify each of these:

| Setting | Value | Why |
|---------|-------|-----|
| `force2D` | True | Each study is a single 2D ultrasound slice, not a 3D volume. |
| Normalisation | per-image **z-score**, scaled ×100, outliers beyond **3σ clipped** | Ultrasound has **no fixed intensity scale** (unlike CT's Hounsfield units). Gain/depth/probe pressure change absolute brightness between scans. Z-scoring per image puts them on a comparable scale. ×100 keeps numbers in a sensible range for binning. |
| Bin width | **25** grey levels (PyRadiomics default) | Discretises intensities into bins before computing texture matrices. Fixed-bin-width is a standard IBSI choice. |
| Shape features | **disabled** | The visible pancreas region depends on the imaging plane and probe angle, so ROI *geometry* reflects imaging conditions, not graft biology. Including shape would inject acquisition noise. |
| Data type | cast to **16-bit signed integer** | Required format for PyRadiomics discretisation after scaling. |
| Resampling | **none** | (See limitation below.) Features computed in pixel units. |

**Result: 93 features per study, extracted from all 137 studies with no failures.**

### Two settings that are genuine limitations (own them, don't hide them)

- **No image resampling / pixel spacing discarded.** **[THESIS]** Because no resampling was applied,
  texture was computed in **pixel units**, and the physical **pixel spacing varied ~2.7×** across the
  cohort (~**0.11–0.29 mm**) with depth/zoom. **Your defense line (from the thesis itself):** this
  variation adds *noise* to texture measurements — it makes a real signal *harder* to find, it cannot
  *manufacture* a spurious one. So it makes the negative result more conservative, not less valid.
- **Single configuration.** Default bin width 25, no wavelet or Laplacian-of-Gaussian (LoG) filters.
  Alternative configs *might* capture other spatial frequencies. **[THESIS]** You partially addressed
  this with the alternative feature families (§6), which were also null.

## 5. Why ultrasound radiomics is hard (context that helps your case)

**[THESIS]** cites these — they explain why a null result is unsurprising:

- Ultrasound is **operator-dependent** (probe pressure, gain, angle).
- It has **no standardised intensity scale** (unlike CT Hounsfield units).
- It contains **speckle noise** intrinsic to coherent imaging.
- Literature: Duron et al. — preprocessing choices strongly affect US feature repeatability;
  Soleymani et al. — only **27.6%** of US radiomics features were reproducible across scan
  settings/vendors. Radiomics *has* worked on US for liver fibrosis, thyroid nodules, breast lesions
  — but those involve **larger structural changes** than diffuse early rejection.

## 6. The six PyRadiomics feature classes (know what each captures)

**[THESIS]** 93 features across six classes. Learn the intuition, not the individual feature names.

| Class | Count | What it captures (intuition) |
|-------|------:|------------------------------|
| **First Order** | 18 | Intensity **histogram** statistics — mean, variance, skewness, entropy. Ignores spatial arrangement; just "how bright/spread out are the pixels." |
| **GLCM** (Grey-Level Co-occurrence Matrix) | 24 | How often pairs of grey levels occur at a given offset/direction — captures **local texture patterns** (contrast, correlation, homogeneity). |
| **GLRLM** (Run-Length Matrix) | 16 | Lengths of **runs** of consecutive same-intensity pixels — captures coarseness/directionality. |
| **GLSZM** (Size-Zone Matrix) | 16 | Sizes of connected **zones** of uniform intensity, direction-independent. |
| **GLDM** (Dependence Matrix) | 14 | Dependence of a pixel on its **neighbours** (how many neighbours are "similar"). |
| **NGTDM** (Neighbouring Grey-Tone Difference Matrix) | 5 | How much each grey level differs from its neighbourhood **average** (coarseness, contrast, busyness). |

Memory hook: **First-order = histogram (no space). GLCM = pixel pairs. GLRLM = runs. GLSZM = zones.
GLDM = neighbour dependence. NGTDM = neighbourhood difference.** The five texture classes all encode
*spatial* relationships in different ways; first-order does not.

**[THESIS]** These 93 are highly redundant: **316 feature pairs** had |correlation| > 0.9 (worst
within GLRLM/GLSZM). This is why an ML correlation filter was applied later (M3).

## 7. Alternative texture families (the robustness check)

**[THESIS]** To rule out "maybe PyRadiomics is just the wrong feature set," three more families were
extracted from the *same* images — **153 features total**:

- **Local Binary Patterns (LBP):** encode local texture by thresholding each pixel's neighbours
  against it → a binary code → histogram. Three scales (R=1/P=8, R=2/P=16, R=3/P=24), "uniform"
  variant. **54 features.**
- **Gabor filters:** orientation- and frequency-selective bandpass filters. Bank of 3 wavelengths ×
  6 orientations = 18 filters; 3 summary stats (mean, std, energy) each. **54 features.**
- **Laws' texture energy:** convolve with small separable kernels (Level, Edge, Spot, Ripple, Wave)
  → 15 2D filters × 3 stats. **45 features.**

**Point to make:** three *methodologically distinct* families, each capturing texture differently,
**all failed**. That rules out "wrong features" as the explanation for the null result.

## 8. Surrounding-tissue normalisation (the other robustness check)

**[THESIS]** To test "maybe acquisition variability (gain/depth/pressure) masks a real signal":
build a **ring mask** around the pancreas (dilate mask by 10 px, subtract original, exclude
zero-intensity cone-exterior pixels), then z-score the image using the *surrounding tissue's* mean
and std (the surroundings see the same acquisition settings). Re-extract the 93 features on the
normalised image, plus **11 contrast features** (differences/ratios of intensity stats between
pancreas and surroundings, plus a Kolmogorov–Smirnov distribution comparison).

**Result:** still null (actually slightly *worse*). **Interpretation:** if acquisition noise were
hiding a signal, local normalisation should have revealed it. It didn't → the absence of texture
signal is genuine, not an acquisition artifact.

---

## Common questions you should be ready for

- *"Walk me through your preprocessing."* → The 6 steps in §3, then the two edge cases.
- *"Why did you disable shape features?"* → ROI geometry reflects imaging plane/probe angle, not
  biology; including it adds noise.
- *"Why per-image normalisation?"* → US has no calibrated intensity scale; z-scoring makes scans
  comparable.
- *"Why didn't you resample to physical spacing?"* → It's a limitation; but variable spacing adds
  noise that weakens signal, it can't create a false one, so the null result stands (and is
  conservative).
- *"What does GLCM/GLRLM/etc. measure?"* → Use the table in §6.
- *"How do you know it's not just the wrong features?"* → Three alternative families (LBP, Gabor,
  Laws') all null.

---

## Quick self-check

- Walk the 6 preprocessing steps from memory, with the kernel sizes.
- Justify force2D, per-image normalisation, disabled shape, no resampling.
- Name the 6 feature classes and one-line what each captures.
- Explain the two robustness checks (alternative families; surrounding normalisation) and what each
  rules out.
