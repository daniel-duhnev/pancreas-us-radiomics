# Pancreas Ultrasound Radiomics

Master thesis project investigating whether radiomics texture features from grayscale ultrasound can predict pancreas transplant rejection.

## Key Finding

Radiomics features do NOT discriminate rejection from non-rejection (0/93 features significant, all ML classifiers AUC ~0.5). However, clinical ARFI elastography biomarkers DO predict rejection in the late post-transplant period (p < 0.001), consistent with Bassaganyas et al. 2025. The negative radiomics result combined with the positive clinical replication is itself the thesis contribution.

## Project Structure

```
analysis/          Jupyter notebooks (01-21 complete, 22-23 planned)
data/              Raw DICOMs + clinical spreadsheet (gitignored)
docs/              Documentation and plans (start with docs/README.md)
scripts/           Utility scripts for figure generation
thesis/            LaTeX thesis (compiles with TeX Live 2026)
```

## Dataset

- 55 patients, 137 ultrasound studies (98 no-rejection, 39 rejection)
- Hospital Clinic de Barcelona, Oct 2016 - Feb 2020
- Siemens Acuson S3000: grayscale US, ARFI elastography, DCE-US

## Pipeline

1. **Preprocessing** (NB 01-10): DICOM → grayscale, contour detection and removal, mask erosion
2. **Feature extraction** (NB 11-12): PyRadiomics → 93 texture/intensity features per study
3. **Statistical analysis** (NB 14a-14b): Mann-Whitney U, FDR correction, clinical feature replication
4. **Machine learning** (NB 15-20): Joint optimization (StandardScaler → SelectKBest → model), LOOCV/10-fold CV
5. **Paired analysis** (NB 21): Within-patient comparison for 14 patients with both outcomes

## Quick Setup

```bash
git clone https://github.com/daniel-duhnev/pancreas-us-radiomics.git
cd pancreas-us-radiomics
conda env create -f environment.yml
conda activate thesis_env
```

Data is not included in the repository. See `docs/NEW_MACHINE_USER_CHECKLIST.md` for setup instructions.

## Documentation

See `docs/README.md` for the full documentation index. Key entry points:
- `docs/AGENT_HANDOFF.md` - rules for working in this repo
- `docs/PLAN_THESIS_ROADMAP.md` - master plan for remaining work
- `docs/THESIS_HANDOFF.md` - instructions for thesis-writing agents

## Tech

- Python 3.9 (conda env `thesis_env`)
- OpenCV, pydicom, SimpleITK, PyRadiomics
- scikit-learn, pandas, matplotlib
- LaTeX (TeX Live 2026) for thesis
