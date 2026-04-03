# Agent handoff (read first)

## Non-negotiables
- Use the existing conda environment `thesis_env` (Python 3.9.25).
- Do NOT create additional environments (no new conda envs, no `.venv`, no system Python installs).
- Run notebooks via VS Code / Jupyter with kernel set to `thesis_env`.

## Repo goals (1 sentence)
Extract texture-focused radiomics features from pancreas ultrasound ROIs (defined by clinician white contours), then test whether these features correlate with clinical rejection and/or improve prognosis prediction.

## What’s “done” vs “next”
Done (preprocessing):
- Batch pipeline to turn DICOMs into grayscale images + clean masks (contour subtraction) and generate an eroded dataset (K=3, iter=1) with `masks/` and `segmented/` previews.
- Special handling for two outlier images where the clinician contour wasn’t closed.

Next (radiomics):
- Extract texture features (GLCM etc.) from the ROI for all images.
- Merge features with `bd_estudiUPF.csv` labels and run statistical tests / basic ML.

## Key conventions
- “Study ID” is the folder name under `data/PANCREAS_2/PANCREAS_2/` (e.g., `01_01`).
- We treat each study ID (image) as one data point, even if clinically it might represent the same patient at multiple timepoints (“motivos”).

## Where data lives (important)
- Data is gitignored (see `.gitignore`), so agents must NOT expect it to come from `git clone`.
- Canonical raw data input: `data/PANCREAS_2/PANCREAS_2/<study_id>/<date>/...dcm`
- Canonical current processed dataset for radiomics:
  - `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/`
    - `masks/` (binary masks)
    - `segmented/` (visual QA images)
    - `manifest_eroded_CONTOUR_SUBTRACTED_k3_i1.csv`

## How to run things (simple)
- Open the relevant notebook in `analysis/`.
- Select kernel: `thesis_env (Python 3.9.25)`.
- Run cells top-to-bottom.

## What to avoid
- Don’t “nbconvert” run notebooks using a different Python.
- Don’t refactor notebooks heavily or add fancy abstractions.
- Don’t delete or rename dataset folders without confirming what notebooks reference.

## Quick sanity commands (optional)
Run inside a notebook cell (kernel = `thesis_env`):
- `import cv2, pydicom, numpy as np, SimpleITK as sitk; import radiomics`

