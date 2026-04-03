# New machine user checklist (manual)

This is the shortest reliable path to continue work on this project on any machine.

## 1) Get the code
- Install Git.
- Clone the repo:
  - `git clone <repo-url>`
  - `cd master-thesis`

## 2) Transfer the data (required)
The entire `data/` folder is gitignored, so it will NOT come from GitHub.

Minimum to continue radiomics:
- `data/PANCREAS_2/` (raw DICOM dataset)
- `data/bd_estudiUPF.csv` (clinical labels)

Recommended (saves time, avoids recomputing):
- `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/` (final masks + segmented previews)

How to do it (one simple approach):
- Zip the folder(s) you want to transfer.
- Upload to Google Drive.
- On the new machine: download + unzip into the repo root so the path is exactly `master-thesis/data/...`.

Quick check:
- After unzip, you should have `master-thesis/data/PANCREAS_2/PANCREAS_2/<study_id>/...`.

## 3) Install Python tooling
### Recommended (least pain): Miniconda/Conda
Conda is not “the only way”, but it is the most reproducible here because this repo has an `environment.yml`.

- Install Miniconda (or Anaconda).
- Create the environment:
  - `conda env create -f environment.yml`
  - `conda activate thesis_env`
- Make the Jupyter kernel available:
  - `python -m ipykernel install --user --name thesis_env --display-name "thesis_env"`

### Alternative (works, but more manual): regular Python + venv
This can work on Windows/Linux/macOS **if** you install Python 3.9 and manually install the same packages.

- Install Python 3.9.
- Create venv and activate it.
- Install packages (you’ll need at least):
  - `opencv-python`, `pydicom`, `numpy`, `pandas`, `matplotlib`, `SimpleITK`, `pyradiomics`, `ipykernel`

Note: because this repo does not currently include a `requirements.txt`, conda is the smoother path.

## 4) Install editor tools (recommended)
- Install VS Code.
- Install VS Code extensions:
  - Python
  - Jupyter

## 5) Verify everything works (2-minute test)
Open any notebook in `analysis/` and select kernel:
- `thesis_env (Python 3.9.x)`

Run this in a notebook cell:
- `import cv2, pydicom, numpy as np, pandas as pd, SimpleITK as sitk; import radiomics`

## 6) Resume work (what to run next)
- Single-image radiomics test:
  - `analysis/11_extract_radiomics_for_one_test_image.ipynb`
- Then build the “all images → one CSV” radiomics extraction notebook (see `docs/RADIOMICS_PLAN.md`).

## Common mistakes to avoid
- Forgetting to transfer `data/`.
- Running notebooks on the wrong Python (system Python) and getting missing `cv2` / `pyradiomics`.
- Changing folder names under `data/` (the notebooks expect current paths).
