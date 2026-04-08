# Radiomics plan (texture-focused)

## Goal
Compute texture (and optionally first-order intensity) features for each study’s ROI using PyRadiomics, then test correlation with clinical rejection labels.

## Current starting point
- A working single-image extraction notebook exists:
  - `analysis/11_extract_radiomics_for_one_test_image.ipynb`
  - It loads one DICOM + its mask from `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/masks/` and prints GLCM + firstorder features.

## Next deliverable: “all images → one CSV”
Create a new notebook (suggested name): `analysis/12_extract_radiomics_all_images.ipynb`.
Steps:
1. Load `manifest_eroded_CONTOUR_SUBTRACTED_k3_i1.csv` from the eroded dataset output.
2. For each study ID, locate:
   - the corresponding DICOM image (preferred: original DICOM → grayscale)
   - the corresponding mask PNG
3. Convert to SimpleITK objects.
4. Run PyRadiomics extractor with a controlled, explicit feature set:
   - Start lean: `glcm` + `firstorder`.
   - Optionally add `glrlm`, `glszm`, `gldm`, `ngtdm` later.
5. Save results to `analysis/reports/radiomics_features_k3_i1.csv` (note: `analysis/reports/` is gitignored).

## Merge with clinical labels
1. Load `data/bd_estudiUPF.csv`.
2. Identify the column that contains the study ID (or build it if the ID is split across columns).
3. Identify outcome columns (e.g., “rechazo clinico” / rejection yes/no, and possibly “motivo”).
4. Merge using a strict join key (study ID).
5. Create a clean modeling table with:
   - `study_id`
   - label(s)
   - radiomics features

## Analysis strategy (simple first)
- Univariate statistics:
  - For each feature, compare rejection vs no rejection.
  - If assumptions for t-test are not met, use Mann–Whitney U.
- Multiple testing awareness:
  - Start without correction to see if any signal exists.
  - If you find many “significant” features, apply correction (e.g., Benjamini–Hochberg FDR) and report both.
- Feature reduction / selection (to avoid overfitting):
  - Drop highly correlated features.
  - Use a simple model (e.g., logistic regression with regularization, or random forest) to rank feature importance.
- ML validation (keep realistic for small N):
  - Use stratified cross-validation.
  - Report AUC / sensitivity / specificity.

## Important open questions
- Confirm that spreadsheet rows correspond to images (study IDs match).
- Decide whether to treat repeated measures (same patient multiple timepoints) differently. Default: treat each image as a sample.

