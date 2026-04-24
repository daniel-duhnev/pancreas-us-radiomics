# Plan: Integrate 3 New Images from Carlos

## Context

Carlos sent DICOM images for 3 of the 4 missing studies (34_02, 40_02, 41_03) on 2026-04-23. Study 47_01 has no images and should be excluded (confirmed by Carlos: "no tiene imágenes colgadas, nunca las pudimos recuperar").

Downloaded files are in `~/Downloads/Páncreas restantes (22-04-2026)/`. Structure matches existing DICOMs: `study_id/date/dicom_uid`.

After integration, dataset goes from 134 to 137 studies. Study 47_01 remains in the clinical spreadsheet (138 rows) but has no image — mark as excluded.

---

## Steps

### Step 1: Copy DICOMs into data folder

Copy the 3 folders into `data/PANCREAS_2/PANCREAS_2/`:

```
cp -r ~/Downloads/Páncreas\ restantes\ \(22-04-2026\)/34_02 data/PANCREAS_2/PANCREAS_2/
cp -r ~/Downloads/Páncreas\ restantes\ \(22-04-2026\)/40_02 data/PANCREAS_2/PANCREAS_2/
cp -r ~/Downloads/Páncreas\ restantes\ \(22-04-2026\)/41_03 data/PANCREAS_2/PANCREAS_2/
```

**Checks:**
- Verify each folder has structure: `study_id/date/dicom_file`
- Verify these 3 folders did NOT already exist (they shouldn't)
- Verify total DICOM folder count goes from 134 to 137

### Step 2: Run preprocessing (NB 06b) on only the 3 new studies

- Do NOT re-run the full notebook on all 134 existing studies
- Either run only the 3 new ones manually, or add a skip-if-exists check
- Output goes to `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED/`

**Checks:**
- Visually inspect the 3 output images + masks
- Look for: closed contour, reasonable mask shape, no black/empty segmentation
- If contour is not closed (like edge cases 03_01 and 43_01), handle manually per `docs/PREPROCESSING_PIPELINE.md`

### Step 3: Run erosion (NB 09) on the 3 new studies

- Process only the 3 new studies
- Output goes to `data/PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1/`

**Checks:**
- 3 new mask files appear in `masks/`
- 3 new segmented files appear in `segmented/`
- Append 3 rows to `manifest_eroded_CONTOUR_SUBTRACTED_k3_i1.csv`
- Verify eroded masks have non-zero pixel count

### Step 4: Run radiomics extraction (NB 12) on the 3 new studies

- Append 3 rows to `reports/12_radiomics_features_k3_i1.csv`
- Should go from 134 to 137 rows

**Checks:**
- No NaN values in the 3 new rows
- Feature count still 93
- Study IDs match (34_02, 40_02, 41_03)

### Step 5: Re-run merge (NB 13)

- Joins radiomics CSV with clinical spreadsheet
- `reports/13_merged_radiomics_clinical.csv` goes from 134 to 137 rows

**Checks:**
- The 3 new study IDs merge correctly (have matching rows in `bd_estudiUPF.csv`)
- 47_01 remains unmatched (no image) — confirm it's not in the output
- Verify rejection labels are correct for the 3 new studies

### Step 6: Mark 47_01 as excluded

- Add a note in NB 13 or in this doc that 47_01 is permanently excluded
- Reason: images were never recovered (Carlos confirmed 2026-04-23)
- Final dataset: 137 studies from 56 patients (was 138 in spreadsheet, minus 47_01)

### Step 7: Re-run stats and ML (NB 14a, NB 15)

- Update results with 137 instead of 134 studies
- Results will likely be essentially identical (3 extra data points)

**Checks:**
- Compare p-values before/after — should be very similar
- If any big changes, investigate the 3 new studies specifically

### Step 8: Update experiment notebooks (16-19)

- They read from `reports/13_merged_radiomics_clinical.csv`
- They will automatically pick up the 137 rows next time they run
- No code changes needed

---

## Risk areas

- Preprocessing edge cases: the 3 new images might have unclosed contours or dimension mismatches, like 03_01 and 43_01 did historically
- Duplicate data: before copying, verify the studies don't already exist in any folder
- Manifest consistency: after appending rows, verify the manifest row count matches the mask file count

## Effort estimate

~2 hours if pipeline runs cleanly. Add 1-2 hours if edge cases arise.

## When to do this

After completing Category 1 (ML improvements). The new experiment notebooks (16-19) work fine on the existing 134-row CSV. Integrate the 3 images in a clean session before thesis writing begins.
