# Analysis reports guide (what to keep)

The folder `analysis/reports/` is gitignored (not pushed to GitHub). Treat these CSVs as **local artifacts**: either copy them when migrating, or regenerate them from notebooks.

Below is a file-by-file recommendation.

## dataset_audit_simple.csv (135 lines)
**What it is:** basic dataset inventory (DICOM filename, image size, channels, modality, full path).

**Why it’s useful:** easy to cite in the thesis (e.g., all images are US, RGB, 768×1024, N=134 unique studies).

**Status:** safe and small.

**Recommendation:** KEEP. You can regenerate via `analysis/03_dataset_audit.ipynb`.

## mask_erosion_loss_report_PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED.csv (529 lines)
**What it is:** per-study pixel loss from erosion for multiple kernels (includes K=3, which is what you chose).

**Why it’s useful:** justifies the final erosion choice (K=3 gives a modest ROI shrink while cleaning boundary artifacts).

**Status:** relevant to the current pipeline.

**Recommendation:** KEEP (gold nugget). Regenerate via `analysis/08_mask_erosion_loss_analysis.ipynb` if needed.

## mask_erosion_boundary_white_report_PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED.csv (671 lines)
**What it is:** per-study measurement of “white pixels near the mask boundary” across kernels.

**Why it’s useful:** evidence that your preprocessing removes annotation artifacts (and that K=3 can drive boundary-whites toward ~0).

**Caveat:** if these were generated *before* the final fix for edge cases (`03_01`, `43_01`), results for those two may be outdated.

**Recommendation:** KEEP, but consider REGENERATING once (after edge-case fixes) if you plan to include figures/tables in the thesis.

## mask_erosion_loss_flags_kernel10.csv (16 lines)
**What it is:** list of studies where K=10 erosion causes excessive ROI loss (likely >30%).

**Why it’s useful:** supports the narrative “K=10 is too aggressive for many images; we moved to K=3”.

**Recommendation:** KEEP if you want the story/justification. Otherwise ARCHIVE.

## mask_erosion_loss_flags_kernel3_PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED.csv (1 line)
**What it is:** empty file with only a header (meaning: no studies crossed the flag threshold).

**Why it’s useful:** minimal; better expressed as a sentence/metric in the notebook output.

**Recommendation:** DELETE or IGNORE. If you need it for the thesis, regenerate and/or replace with a small summary table (e.g., “0/134 flagged at threshold X%”).

## mask_erosion_loss_report.csv (403 lines)
**What it is:** older erosion loss results for the earlier dataset (kernels 5/9/10 shown in the snippet).

**Why it’s useful:** only if you want to document the evolution of the pipeline (pre contour-subtraction baseline).

**Recommendation:** ARCHIVE (not needed for final analysis). Safe to delete if you don’t plan to discuss earlier approaches.

## mask_erosion_boundary_white_report.csv (537 lines)
**What it is:** older “white boundary” metrics for the earlier dataset.

**Recommendation:** ARCHIVE (not needed for final analysis). Same logic as `mask_erosion_loss_report.csv`.

## contour_refinement_sweep_v1.csv (82 lines)
**What it is:** a parameter sweep summary (columns like `white_threshold`, `boundary_band_dilate`, `exclude_dilate`, `post_erosion_kernel`, etc.).

**Why it’s useful:** only if you want to show you tried multiple contour-cleaning strategies and chose a trade-off between ROI loss vs boundary whiteness.

**Caveat:** this file is not currently referenced by notebooks in `analysis/`, so it may be hard to reproduce exactly.

**Recommendation:** ARCHIVE unless you can point to the notebook/script that generated it.

## contour_refinement_summary_v1.csv (2 lines)
**What it is:** one-line summary of the sweep (mean/median lost %, mean/median boundary-white %, etc.).

**Recommendation:** ARCHIVE together with the sweep. Not required for final work.

## Practical suggestion (simple)
If you want to keep everything but reduce confusion:
- Make a local folder like `analysis/reports_archive/` and move the “ARCHIVE” files there.
- Keep only the “KEEP” files under `analysis/reports/`.

When migrating machines, copy:
- `analysis/reports/` (only if you want these artifacts)
- always copy `data/` (required)
