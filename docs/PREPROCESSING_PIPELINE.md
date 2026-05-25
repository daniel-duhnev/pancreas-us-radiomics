# Preprocessing Pipeline

## Goal

Turn clinician-drawn white contour boxes in ultrasound images into clean binary masks that exclude the annotation line itself. This ensures radiomics features measure tissue texture, not annotation artifacts.

## Input

- DICOMs at `data/PANCREAS_2/PANCREAS_2/<study_id>/<date>/*.dcm`
- Images are RGB ultrasound frames with a white contour drawn by clinicians around the pancreas graft

## Pipeline steps

1. Load DICOM and extract the RGB image
2. Detect white pixels using a channel threshold (R, G, B all > 200)
3. Remove UI noise by keeping only the largest connected white component
4. Morphological closing to bridge small gaps in the contour line
5. Find the contour boundary and fill it to produce a solid mask
6. Subtract the contour outline from the filled mask (removes the bright annotation border)
7. Convert image to grayscale
8. Erode the mask by 3 pixels (kernel=3, iterations=1) to further reduce boundary artifacts
9. Save outputs:
   - Binary mask (PNG)
   - Segmented preview image (for visual QA)

## Notebooks

| Notebook | What it does | Output folder |
|----------|--------------|---------------|
| `06b_segment_all_images_contour_subtracted.ipynb` | Contour detection and mask creation | `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED/` |
| `09_erode_mask_and_generate_new_dataset.ipynb` | Erosion and final dataset assembly | `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/` |
| `10_handle_edge_cases.ipynb` | Fixes for 2 problematic studies | `data/PANCREAS_EDGE_CASES_FIXED/` |

## Final output structure

```
data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/
    masks/          - binary mask PNGs (one per study)
    segmented/      - visual preview PNGs (one per study)
    manifest_eroded_CONTOUR_SUBTRACTED_k3_i1.csv  - index of all processed studies
```

## Edge cases

Two studies had issues:
- **03_01**: Dimension mismatch between mask and image. Fixed with transpose/resize.
- **43_01**: Clinician contour not fully closed, causing the fill operation to fail. Fixed by using a much larger morphological closing kernel to force closure.

Both fixes are in notebook 10. The corrected files were copied back into the main eroded dataset folder.

## Important notes

- Masks must be binary and correctly aligned to the image
- Removing the contour line is critical - otherwise texture features will pick up the annotation rather than tissue
- The erosion step (K=3, iter=1) provides a safety margin against residual boundary pixels
- 137 studies are successfully processed (study 47_01 excluded - no images available)
