"""Generate the preprocessing pipeline figure for the thesis (Figure 2.1).

Creates a 2x2 panel showing:
  (a) Original ultrasound with clinician contour
  (b) Extracted binary mask (contour subtracted)
  (c) Eroded binary mask (K=3, iter=1)
  (d) Final segmented tissue ROI

Uses study 10_01 as the example.
Output: thesis/Figures/preprocessing_pipeline.pdf
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA = PROJECT_ROOT / "data"

img_original = mpimg.imread(
    DATA / "PANCREAS_PREPROCESSED" / "10_01_image.png"
)
img_mask = mpimg.imread(
    DATA / "PANCREAS_PREPROCESSED" / "10_01_mask.png"
)
img_mask_eroded = mpimg.imread(
    DATA / "PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1"
    / "masks" / "10_01_mask_eroded_k3_i1.png"
)
img_segmented = mpimg.imread(
    DATA / "PANCREAS_PREPROCESSED_CONTOUR_SUBTRACTED_ERODED_K3_I1"
    / "segmented" / "10_01_segmented_k3_i1.png"
)

# Crop all images to the region around the ROI for visual clarity.
# Find bounding box from the mask (largest non-zero region).
if img_mask.ndim == 3:
    mask_gray = img_mask[:, :, 0]
else:
    mask_gray = img_mask

rows = np.any(mask_gray > 0.1, axis=1)
cols = np.any(mask_gray > 0.1, axis=0)
rmin, rmax = np.where(rows)[0][[0, -1]]
cmin, cmax = np.where(cols)[0][[0, -1]]

# Add generous padding around the ROI.
pad = 80
h, w = img_mask.shape[:2]
rmin = max(0, rmin - pad)
rmax = min(h, rmax + pad)
cmin = max(0, cmin - pad)
cmax = min(w, cmax + pad)

images = [img_original, img_mask, img_mask_eroded, img_segmented]
titles = [
    "(a) Original ultrasound\nwith clinician contour",
    "(b) Extracted binary mask",
    "(c) Eroded mask (K=3, iter=1)",
    "(d) Segmented tissue ROI",
]

fig, axes = plt.subplots(2, 2, figsize=(8, 7))

for ax, img, title in zip(axes.flat, images, titles):
    cropped = img[rmin:rmax, cmin:cmax]
    if cropped.ndim == 3 and cropped.shape[2] >= 3:
        ax.imshow(cropped[:, :, :3])
    else:
        ax.imshow(cropped, cmap="gray")
    ax.set_title(title, fontsize=10)
    ax.axis("off")

plt.tight_layout(pad=1.5)

out_path = PROJECT_ROOT / "thesis" / "Figures" / "preprocessing_pipeline.pdf"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved: {out_path}")

out_path_png = out_path.with_suffix(".png")
fig.savefig(out_path_png, dpi=300, bbox_inches="tight")
print(f"Saved: {out_path_png}")
plt.close()
