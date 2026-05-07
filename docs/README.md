# Handoff docs

This folder contains concise docs meant to let you (or another coding agent) resume work quickly, especially when moving to a new machine.

Start here:
- [AGENT_HANDOFF.md](AGENT_HANDOFF.md) — rules-of-engagement for working in this repo (env, paths, how to run notebooks)
- [NEW_MACHINE_USER_CHECKLIST.md](NEW_MACHINE_USER_CHECKLIST.md) — short manual checklist for you to resume work on any machine
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — what the thesis is trying to answer + assumptions from supervisor meetings
- [PREPROCESSING_PIPELINE.md](PREPROCESSING_PIPELINE.md) — what the current segmentation/preprocessing pipeline does and where outputs live
- [REPORTS_GUIDE.md](REPORTS_GUIDE.md) — what the CSV reports are and which ones to keep
- [RADIOMICS_PLAN.md](RADIOMICS_PLAN.md) — how to go from images+masks → texture features → merge with clinical labels → stats/ML
- [MIGRATION_CHECKLIST.md](MIGRATION_CHECKLIST.md) — how to continue on a new machine, including what must be copied (gitignored data)

Current plans:
- [PLAN_THESIS_ROADMAP.md](PLAN_THESIS_ROADMAP.md) — master plan for remaining work (NB 18-23, thesis writing, timeline through June 2026)
- [PLAN_INTEGRATE_NEW_IMAGES.md](PLAN_INTEGRATE_NEW_IMAGES.md) — steps to add 3 new DICOMs (34_02, 40_02, 41_03)
- [PLAN_NON_INDEPENDENT_DATA_AND_PAIRED_ANALYSIS.md](PLAN_NON_INDEPENDENT_DATA_AND_PAIRED_ANALYSIS.md) — approaches for handling repeated measures
- [THESIS_WRITING_PLAN.md](THESIS_WRITING_PLAN.md) — chapter-by-chapter writing plan with page budgets

Legacy (superseded but kept for reference):
- [legacy/PLAN_ML_STRUCTURED_EXPERIMENTS.md](legacy/PLAN_ML_STRUCTURED_EXPERIMENTS.md) — original sequential ML approach (superseded by joint optimization in NB 17b)
- [legacy/PLAN_EXPERIMENTS_SURROUNDING_TISSUE_AND_ALT_FEATURES.md](legacy/PLAN_EXPERIMENTS_SURROUNDING_TISSUE_AND_ALT_FEATURES.md) — detailed implementation code for LBP, Gabor, Laws', surrounding tissue (referenced from roadmap)
