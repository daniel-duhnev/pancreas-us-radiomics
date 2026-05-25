# Agent handoff (read first)

## Non-negotiables
- Use the existing conda environment `thesis_env` (Python 3.9.25).
- Do NOT create additional environments (no new conda envs, no `.venv`, no system Python installs).
- Run notebooks via VS Code / Jupyter with kernel set to `thesis_env`.

## Repo goals (1 sentence)
Extract texture-focused radiomics features from pancreas ultrasound ROIs (defined by clinician white contours), then test whether these features correlate with clinical rejection and/or improve prognosis prediction.

## What’s “done” vs “next”
Done:
- Preprocessing pipeline: DICOMs → grayscale images + clean masks (contour subtraction, erosion K=3 iter=1)
- Radiomics extraction: 93 PyRadiomics features from 137 studies
- Stats (NB 14a/14b): 0/93 radiomics features significant; ARFI significant in late period
- ML (NB 15, 17, 17b): all models AUC ~0.5, no predictive signal from radiomics

Next (May 2026 - see docs/PLAN_THESIS_ROADMAP.md):
- ~~Integrate 3 new images~~ (done, 137 studies)
- ~~Build independent dataset (1 per patient, 55 studies) - NB 18~~ (done)
- ~~Stats + ML on independent dataset (10-fold CV) - NB 19, 20~~ (done)
- ~~Paired analysis (14 patients) - NB 21~~ (done)
- Extended analysis (LBP, Gabor, Laws’, surrounding tissue) - NB 22, 23
- Thesis writing in LaTeX (Results 3.5-3.7, Discussion, Related Work remaining)

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

## Coding + writing style (required)
- Write code in a plain, straightforward style (like a very strong junior engineer).
- Prefer clarity over cleverness:
  - Use explicit multi-line `for` loops (not dense comprehensions) when it improves readability.
  - Use descriptive variable names (avoid single-letter names except trivial indices).
  - Avoid “shortcut” one-liners that hide logic.
- Keep comments short and literal (explain *why* when needed; don’t narrate every line).
- No emojis.
- No “AI-ish” formatting or decoration (avoid big ASCII separators like `----` or fancy banner blocks).
- Keep notebooks readable top-to-bottom:
  - Step-by-step cells.
  - Print helpful, minimal status messages.
  - Avoid heavy refactors unless requested.

Quick rubric (use this before editing notebooks):
- Cell size: any code cell > ~40 lines is a smell for “not junior-readable”.
- Idioms: count comprehensions, ternaries, heavy chaining; each one is fine occasionally, but lots of them shifts the notebook away from the house style.
- Repetition: if you see the same “find date folder → find dicom → read → mask” block repeated, readability decays fast (future readers must mentally diff variants).
- Tone: comments should explain why and invariants; avoid dramatic wording (it ages poorly and confuses reviewers).
- Audience: decide per notebook whether it’s an “exploration scratchpad” vs a “pipeline artifact”; apply strict style mainly to pipeline artifacts.

## What to avoid
- Don’t “nbconvert” run notebooks using a different Python.
- Don’t refactor notebooks heavily or add fancy abstractions.
- Don’t delete or rename dataset folders without confirming what notebooks reference.

## Current next steps (May 2026)

All preprocessing and radiomics extraction (NB 01-21) is complete. Next steps:

**Code (notebooks):**
- NB 22: Alternative texture features (LBP, Gabor, Laws') - not yet created
- NB 23: Surrounding tissue analysis - not yet created
- See `docs/PLAN_THESIS_ROADMAP.md` for context and `docs/legacy/PLAN_EXPERIMENTS_SURROUNDING_TISSUE_AND_ALT_FEATURES.md` for code snippets

**Thesis writing (LaTeX):**
- Results §3.5 (paired analysis) - data ready at `analysis/reports/21_*`
- Related Work (4 subsections) - needs literature research
- Discussion + Conclusions - write after all results sections
- See `docs/THESIS_HANDOFF.md` for comprehensive writing agent instructions

## Quick sanity commands (optional)
Run inside a notebook cell (kernel = `thesis_env`):
- `import cv2, pydicom, numpy as np, SimpleITK as sitk; import radiomics`

