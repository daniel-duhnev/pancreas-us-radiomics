# Pancreas US Radiomics - Thesis Project

## Environment
- Conda env: `thesis_env` (Python 3.9.25). Do NOT create other envs.
- Python path: `/home/daniduhnev/miniconda3/envs/thesis_env/bin/python`
- Run notebooks in Jupyter/VS Code with kernel set to `thesis_env`.

## Key data paths
- Raw DICOMs: `data/PANCREAS_2/PANCREAS_2/<study_id>/<date>/`
- Canonical processed data: `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/`
- Clinical spreadsheet: `data/bd_estudiUPF.csv` (138 rows, 56 patients; study 47_01 has no images and is excluded - 137 usable studies from 55 patients)
- Merged radiomics + clinical: `analysis/reports/13_merged_radiomics_clinical_normalised.csv` (137 rows)
- Data is gitignored. It does not come from git clone.

## Project status
- ALL experiment notebooks complete (NB 01-23 plus normalised variants). No further coding needed.
- Thesis writing complete (all chapters done, compiles cleanly)
- Remaining: personal sections (dedication, acknowledgements), final proofread, send to Gemma

## Current phase (May 2026)
- Thesis is content-complete and in polishing phase
- See `docs/PLAN_THESIS_FINAL_STEPS.md` for remaining tasks
- Submit to Gemma for review: June 8
- Final submission: mid June 2026
- Thesis defence: mid July 2026

## Coding standards
- See `docs/DEVELOPMENT_GUIDE.md` for full rules
- Short version: plain style, explicit loops, descriptive names,
  cells under 40 lines, no clever one-liners, no emojis

## People
- Student: Daniel Duhnev (daniel.duhnev01@estudiant.upf.edu)
- Supervisor: Gemma Piella (UPF)
- Clinical team: Carlos Perez, Clara Bassaganyas, Joana Ferrer,
  M. Angeles Garcia, Helena Font (Hospital Clinic Barcelona)
