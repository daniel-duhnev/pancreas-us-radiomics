# Project context (thesis)

## Research direction
- Goal: perform a study similar in spirit to prior work (e.g., “Clara’s paper”), but using automated image analysis rather than manual measurements.
- Constraint: dataset is small (~134 images), so deep learning is optional and not the default recommendation.

## Hypothesis
The texture (and possibly intensity) patterns inside the transplanted pancreas on ultrasound contain information correlated with prognosis / clinical rejection.

## What we measure
- Focus on texture radiomics (and optionally intensity/first-order statistics).
- Avoid relying on shape/size features as primary signals because ultrasound pancreas boundaries can be unreliable.

## Dataset realities & assumptions
- We have 134 unique ultrasound images stored as DICOMs.
- Each image corresponds to a folder ID like `49_01`.
- There may be multiple images per underlying patient, tied to “motivo” timepoints (1 week, 1 month, 1 year, suspicion, follow-up). Current plan: treat each image as a separate sample for radiomics/statistics unless/until proven otherwise.

## Critical verification task
Confirm that the clinical spreadsheet (`bd_estudiUPF.csv` / `bd_estudiUPF.xlsx`) correctly matches the image dataset:
- Every study ID should have a row in the spreadsheet (no orphan images).
- Every spreadsheet row should map to an image (no ghost entries).
If uncertainty remains, contact the data provider / hospital clinic.

## Expected outcomes
- It is acceptable if the analysis fails to find strong predictive signals.
- A negative result is still a valid thesis outcome if the methodology is solid and limitations are clearly described.

## Timeline hints (from supervisor notes)
- Short term: understand dataset structure + confirm spreadsheet mapping.
- Next: finish preprocessing (done now) and move quickly into radiomics.
- After Easter / March–April: start writing introduction + methods while experiments run.

