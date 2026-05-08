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
- NB 17: sequential ML experiments — complete (AUC ~0.5, no signal)
- NB 17b: joint optimization ML — complete (best AUC 0.537, confirms no signal)
- NB 18: independent dataset built (55 studies, 1 per patient)
- NB 19: stats on independent dataset — complete
- NB 20: ML on independent dataset — complete
- 3 new images (34_02, 40_02, 41_03) integrated (137 studies total)
- Study 47_01 excluded (no images, confirmed by hospital)
- Thesis Methods chapter: written and audited (see thesis/methods.tex)
- Next notebooks to create: NB 21-23 (see docs/PLAN_THESIS_ROADMAP.md)

## Current phase (May 2026)
- Paired analysis (14 patients with both outcomes) — NB 21
- Extended analysis (alt texture features, surrounding tissue) — NB 22, 23
- Thesis writing in LaTeX (Methods done, Results/Discussion/Introduction next)

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
- Independent dataset + core results: May 6-16
- Extended analysis: May 19-30
- Thesis writing: ongoing from May 12
- Submit to Gemma for review: June 8
- Final submission: mid June 2026
- Thesis defence: mid July 2026
