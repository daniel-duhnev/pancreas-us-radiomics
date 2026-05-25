# Development Guide

## Project goal

Extract radiomics texture features from pancreas transplant ultrasound images and test whether they can predict graft rejection. The main finding is negative - radiomics does not predict rejection, but clinical biomarkers (ARFI elastography) do.

## Environment

- Conda environment: `thesis_env` (Python 3.9.25)
- Do NOT create additional environments
- Run notebooks in VS Code or Jupyter with kernel set to `thesis_env`

To create the environment from scratch:

```bash
conda env create -f environment.yml
conda activate thesis_env
python -m ipykernel install --user --name thesis_env --display-name "thesis_env"
```

Quick sanity check (run in a notebook cell):

```python
import cv2, pydicom, numpy as np, pandas as pd, SimpleITK as sitk
import radiomics
```

## Data paths

Data is gitignored and does not come from git clone. You must transfer it manually.

| Path | Contents |
|------|----------|
| `data/PANCREAS_2/PANCREAS_2/<study_id>/<date>/` | Raw DICOM files |
| `data/bd_estudiUPF.csv` | Clinical spreadsheet (138 rows, 56 patients) |
| `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/` | Final preprocessed images and masks |
| `analysis/reports/` | All computed CSV results (also gitignored) |

Key facts:
- Study 47_01 has clinical data but no images - it is excluded from all analyses
- This leaves 137 usable studies from 55 patients
- The `rejection` column in merged CSVs is the ground truth label (binary: 0/1)
- The `motivo` column encodes visit reason (time post-transplant), NOT rejection status

## How to run notebooks

1. Open any notebook in `analysis/`
2. Select kernel: `thesis_env (Python 3.9.25)`
3. Run cells top to bottom

Notebooks are numbered in dependency order. Later notebooks depend on outputs from earlier ones.

## Notebook overview

| Range | Purpose | Status |
|-------|---------|--------|
| 01-09 | Preprocessing (DICOM to masks) | Complete |
| 10-11 | Edge cases and QA | Complete |
| 12 | Radiomics feature extraction | Complete |
| 13 | Merge radiomics with clinical labels | Complete |
| 14a/14b | Univariate statistics | Complete |
| 15, 17, 17b | Machine learning classification | Complete |
| 18 | Build independent dataset (1 per patient) | Complete |
| 19 | Statistics on independent dataset | Complete |
| 20 | ML on independent dataset | Complete |
| 21 | Paired within-patient analysis | Complete |
| 22 | Alternative texture features (LBP, Gabor, Laws') | Complete |
| 23 | Surrounding tissue analysis | Complete |
| *_normalised | Parallel versions with image normalisation | Complete |

All notebooks are complete. No further coding is needed.

## Coding conventions

- Plain, straightforward style - explicit loops over dense comprehensions
- Descriptive variable names (no single-letter names except trivial indices)
- Short comments only where the "why" is not obvious
- Cells under 40 lines
- No fancy abstractions or heavy refactoring
- Print minimal, helpful status messages

## Thesis compilation

The thesis lives in `thesis/`. To compile:

```bash
cd thesis
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"
latexmk -pdf MasterThesis.tex
```

## Key conventions

- "Study ID" is the folder name under `data/PANCREAS_2/PANCREAS_2/` (e.g., `01_01`)
- Each study ID is treated as one data point
- Patient IDs are the first two digits of the study ID (e.g., patient 01 has studies 01_01, 01_02)
- The independent dataset uses 1 study per patient (55 total)
- The paired analysis uses 14 patients who have both rejection and non-rejection studies
