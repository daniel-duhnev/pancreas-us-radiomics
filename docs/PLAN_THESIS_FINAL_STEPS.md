# Thesis Final Steps Plan

**Created:** 2026-05-24  
**Status:** Content-complete; polishing phase  
**Target:** Send to Gemma for review by June 8

---

## Current State

The thesis compiles cleanly at ~10,500 words across 4 chapters + appendix. All experiment notebooks (01-23 + 8 normalised variants) are complete. All results use normalised image data. All figures are regenerated.

---

## Remaining Issues (by priority)

### A. Factual Errors — Must Fix (5 min total)

These are numbers that still reference the old un-normalised analysis.

| # | File | Line | Current (wrong) | Correct | Reason |
|---|------|------|-----------------|---------|--------|
| 1 | `abstract.tex` | 10 | "best: 0.569, 95% CI [0.40, 0.72]" | "best: 0.636, 95% CI [0.48, 0.78]" | Old independent ML result |
| 2 | `discussion.tex` | 102 | "best: 0.569, 95% CI [0.40, 0.72]" | "best: 0.636, 95% CI [0.48, 0.78]" | Same |
| 3 | `methods.tex` | 174 | "93 to 32 features" | "93 to 27 features" | Old correlation filter count |
| 4 | `discussion.tex` | 58 | "no individual radiomics feature shows even uncorrected significance on the independent dataset" | "no individual radiomics feature achieves significance after FDR correction on the independent dataset" | 24 features now reach uncorrected p<0.05 |

### B. Inconsistency — Should Fix (2 min)

| # | Issue | Details |
|---|-------|---------|
| 5 | Scanner model name | Methods (lines 8, 69): "Siemens Acuson S3000". Discussion (line 52): "Siemens ACUSON S2000". The THESIS_WRITING_PLAN.md says S3000. DICOM headers only show the PACS software (syngo.via), not the scanner. **Action:** Verify with clinical team which is correct (likely S3000 based on methods + docs). Fix the one that's wrong. |

### C. Personal Sections — Only Daniel Can Write

| # | File | Current state |
|---|------|---------------|
| 6 | `dedication.tex` | Template placeholder: "I would like to dedicate this work to..." |
| 7 | `acknowledgements.tex` | Template placeholder with bullet points for supervisor/co-supervisor/family |

These are required for submission but only the author can write them.

### D. Final Polish — Before Sending to Gemma

| # | Task | Effort |
|---|------|--------|
| 8 | Full human read-through for flow, grammar, typos | 30-60 min |
| 9 | Verify PDF rendering (table placement, figure floats, page breaks) | 10 min |
| 10 | Check bibliography completeness (all \cite keys resolve, no unused entries) | Already verified — 0 warnings |

---

## What Does NOT Need Doing

- No more experiments or notebooks needed
- No new sections to write (all chapters are complete)
- No figure regeneration needed (all done with normalised data)
- No new bibliography entries needed (0 citation warnings)
- Surrounding tissue analysis (NB 23) and alternative features (NB 22) were done on UN-normalised data, but this is fine: those analyses test different hypotheses (alternative feature families, spatial normalisation) and image normalisation doesn't apply to them the same way

---

## Execution Order

1. Fix items A1-A4 (factual errors) — can be done right now by Claude
2. Resolve item B5 (scanner name) — requires Daniel to confirm with clinical team OR check Bassaganyas et al. paper
3. Write items C6-C7 (dedication, acknowledgements) — Daniel only
4. Do item D8 (proofread) — human read-through recommended
5. Compile final PDF and submit to Gemma

---

## Distance from Done

| Milestone | Status |
|-----------|--------|
| All experiments | DONE |
| All results with normalised data | DONE |
| Methods chapter | DONE |
| Results chapter | DONE (all 7 sections) |
| Discussion + Conclusions | DONE |
| Introduction + Related Work | DONE |
| Abstract | DONE (1 number to fix) |
| Appendix | DONE |
| Figures | DONE (all regenerated) |
| LaTeX compilation | DONE (no errors) |
| **Remaining effort** | **~1 hour total** (fixes + personal sections + proofread) |
