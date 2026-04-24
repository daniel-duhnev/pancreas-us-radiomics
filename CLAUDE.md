# Pancreas US Radiomics — Thesis Project

## Environment
- Conda env: `thesis_env` (Python 3.9.25). Do NOT create other envs.
- Python path: `/opt/homebrew/Caskroom/miniconda/base/envs/thesis_env/bin/python`
- Run notebooks in Jupyter/VS Code with kernel set to `thesis_env`.

## Key data paths
- Raw DICOMs: `data/PANCREAS_2/PANCREAS_2/<study_id>/<date>/`
- Canonical processed data: `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/`
- Clinical spreadsheet: `data/bd_estudiUPF.csv` (138 rows, 56 patients)
- Merged radiomics + clinical: `reports/13_merged_radiomics_clinical.csv`
- Data is gitignored. It does not come from git clone.

## Project status
- Notebooks 01-15: complete (preprocessing, radiomics extraction, stats, ML)
- Notebook 16: ML improvements (Category 1) — next to implement
- Notebooks 17-19: planned experiments (see docs/PLAN_NEW_EXPERIMENTS.md)
- 3 new images (34_02, 40_02, 41_03) to integrate (see docs/PLAN_INTEGRATE_NEW_IMAGES.md)
- Study 47_01 excluded (no images, confirmed by hospital)

## Coding standards
- See `docs/AGENT_HANDOFF.md` for full rules
- Short version: plain junior-engineer style, explicit loops, descriptive names,
  cells under 40 lines, no clever one-liners, no emojis

## People
- Student: Daniel Duhnev (daniel.duhnev01@estudiant.upf.edu)
- Supervisor: Gemma Piella (UPF)
- Clinical team: Carlos Perez, Clara Bassaganyas, Joana Ferrer,
  M. Angeles Garcia, Helena Font (Hospital Clinic Barcelona)

## Thesis timeline
- Experiments complete: early May 2026
- Thesis submission: mid June 2026
- Thesis defence: mid July 2026
