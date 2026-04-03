# Migration checklist (new machine)

## What `git clone` gives you
- Notebooks under `analysis/`
- Environment spec in `environment.yml`
- Code + docs

## What `git clone` does NOT give you (gitignored)
Per `.gitignore`, these are excluded:
- `data/` (all images, masks, derived datasets)
- `analysis/reports/` (generated CSVs/reports)
- `.vscode/` (editor config)
- DICOMs (`*.dcm`) and NIfTI (`*.nii*`) anywhere

## Recommended transfer strategy
### Option A (fastest to resume)
Copy the entire `data/` directory to the new machine.
- Pros: no recomputation, everything works immediately.
- Cons: bigger transfer.

### Option B (minimal transfer + recompute)
Transfer only:
- `data/PANCREAS_2/` (raw dataset)
- `data/bd_estudiUPF.csv` (labels)
Then rerun notebooks:
- `analysis/06b_segment_all_images_contour_subtracted.ipynb`
- `analysis/09_erode_mask_and_generate_new_dataset.ipynb`
- `analysis/10_handle_edge_cases.ipynb` (only if needed)

## Environment setup (must match)
1. Install conda (Miniconda recommended).
2. `conda env create -f environment.yml`
3. `conda activate thesis_env`
4. Make kernel visible to Jupyter/VS Code:
   - `python -m ipykernel install --user --name thesis_env --display-name "thesis_env"`
5. In VS Code notebooks, select kernel: `thesis_env (Python 3.9.25)`.

## Quick validation on the new machine
Run in a notebook cell:
- `import cv2, pydicom, numpy as np, SimpleITK as sitk; import radiomics`

Check paths exist:
- `data/PANCREAS_2/PANCREAS_2/`
- `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/` (if you copied derived data)

## Common pitfalls
- Using system Python or a different env → missing `cv2` / `pyradiomics`.
- Missing `data/` → notebooks appear “broken” but it’s just absent inputs.
- Notebook outputs differ slightly across machines; focus on reproducibility of the pipeline and documented parameters.

