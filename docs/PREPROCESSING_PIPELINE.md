# Preprocessing pipeline (current state)

## Objective
Turn clinician-drawn white contour boxes into clean ROI masks that do not include the contour line itself, so that radiomics measures tissue texture rather than annotation artifacts.

## Raw input
- DICOMs under `data/PANCREAS_2/PANCREAS_2/<study_id>/<date>/*.dcm`
- Images are RGB ultrasound with white annotation/contour drawn by clinicians.

## Core steps (conceptual)
1. Load DICOM → RGB image.
2. Detect “white” pixels using a channel threshold (e.g., > 200 on R/G/B).
3. Remove UI noise by keeping the largest connected component.
4. Morphological closing to bridge small gaps in the contour.
5. Find contour + fill it to produce a solid mask.
6. Subtract the contour outline from the filled mask (this removes the bright annotation border).
7. Convert to grayscale.
8. Optionally erode the mask slightly (K=3, iter=1) to reduce boundary artifacts.
9. Save:
   - `*_mask*.png` (binary mask)
   - `*_image.png` or `*_segmented*.png` (preview) for QA.

## Notebooks and outputs
- Batch contour subtraction:
  - `analysis/06b_segment_all_images_contour_subtracted.ipynb`
  - Output: `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED/` (grayscale images + masks)

- Erosion + final dataset generation:
  - `analysis/09_erode_mask_and_generate_new_dataset.ipynb`
  - Input: `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED/`
  - Output: `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/`
    - `masks/`
    - `segmented/`
    - `manifest_eroded_CONTOUR_SUBTRACTED_k3_i1.csv`

## Edge cases handled
Two studies had issues (historically): `03_01` and `43_01`.
- Symptom A: mask/image dimension mismatch (e.g. 768x1024 vs 1024x768)
  - Minimal fix used: transpose or nearest-neighbor resize to align shapes.
- Symptom B: clinician contour not fully closed → filled ROI collapses → segmented image looks pitch black.
  - Fix notebook: `analysis/10_handle_edge_cases.ipynb`
  - Uses a much larger morphological closing “brush” kernel to force closure.
  - Outputs: `data/PANCREAS_EDGE_CASES_FIXED/`
  - Corrected mask+segmented files were copied back into the main eroded dataset folder (data-only change, not tracked by git).

## What matters for radiomics
- Masks should be binary and correctly aligned to the image.
- Removing the contour line is critical; otherwise radiomics features will measure annotation texture.

