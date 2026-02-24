# Pancreas Ultrasound Radiomics

Project to extract radiomic features from pancreas ultrasound images.

Goals
- Build reproducible preprocessing that removes hand-drawn white contours.
- Extract radiomic features from masked pancreas regions.
- Run validation and ML experiments.

Pipeline
- Phase 1 - Preprocessing: clean files, build binary masks from clinician contours, convert images to grayscale.
- Phase 2 - Feature extraction: use PyRadiomics to compute intensity and texture features.
- Phase 3 - Validation: basic statistical checks and simple classifiers (e.g., Random Forest).

Tech
- Python 3.9
- OpenCV (`opencv-python`), `pydicom` for DICOM handling
- `pyradiomics`, `SimpleITK` for feature extraction
- `numpy`, `pandas`, `matplotlib` for analysis

Quick setup
```bash
# clone
git clone https://github.com/daniel-duhnev/pancreas-us-radiomics.git
cd pancreas-us-radiomics

# create and activate the conda env using environment.yml
conda env create -f environment.yml
conda activate thesis_env
```

Notes
- Analysis notebooks are under the analysis/ folders.
- The data is not made public so it has been exluded from this repo.
- The preprocessing step aims to remove bright clinician contours. See analysis/07_check_and_reduce_mask.ipynb and analysis/08_mask_erosion_loss_analysis.ipynb for the erosion and validation workflow.
