# New Machine Setup

Step-by-step checklist to get this project running on a fresh machine.

## 1. Clone the repository

```bash
git clone <repo-url>
cd pancreas-us-radiomics
```

## 2. Transfer the data

The `data/` folder is gitignored. You need to copy it manually (e.g., from an external drive or cloud storage).

Minimum required:
- `data/PANCREAS_2/` - raw DICOM dataset
- `data/bd_estudiUPF.csv` - clinical labels spreadsheet

Recommended (saves recomputing):
- `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/` - preprocessed masks and images
- `analysis/reports/` - all computed CSV results

After transfer, verify the path structure:
```
pancreas-us-radiomics/data/PANCREAS_2/PANCREAS_2/<study_id>/<date>/...dcm
```

## 3. Set up Python environment

Install Miniconda (or Anaconda), then:

```bash
conda env create -f environment.yml
conda activate thesis_env
python -m ipykernel install --user --name thesis_env --display-name "thesis_env"
```

Alternative (manual install with pip):
- Requires Python 3.9
- Key packages: `opencv-python`, `pydicom`, `numpy`, `pandas`, `matplotlib`, `SimpleITK`, `pyradiomics`, `scikit-learn`, `scipy`, `ipykernel`

## 4. Verify the installation

Open any notebook in `analysis/`, select kernel `thesis_env`, and run:

```python
import cv2, pydicom, numpy as np, pandas as pd, SimpleITK as sitk
import radiomics
```

If this runs without errors, you are ready to go.

## 5. Install LaTeX (for thesis compilation)

Install TeX Live 2026 (or later). Then:

```bash
cd thesis
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"
latexmk -pdf MasterThesis.tex
```

On Linux, adjust the TeX Live path accordingly.

## 6. What to run

All analysis notebooks (01-23 plus normalised variants) are complete. To reproduce results from scratch:

1. Run notebooks 06b and 09 (preprocessing) - requires raw DICOMs
2. Run notebook 12 (radiomics extraction)
3. Run notebook 13 (merge with clinical data)
4. Run notebooks 14a, 14b (statistics)
5. Run notebooks 17b, 18, 19, 20, 21 (ML and independent dataset)
6. Run notebooks 22, 23 (extended analysis)

Or simply copy `analysis/reports/` from the previous machine and skip rerunning.

## Common problems

- **Missing `cv2` or `pyradiomics`**: You are running on the wrong Python. Check that your kernel is `thesis_env`.
- **File not found errors in notebooks**: The `data/` folder was not transferred, or the path structure is wrong.
- **LaTeX errors**: Make sure TeX Live is installed and the PATH export is active in your shell.
