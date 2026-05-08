"""Generate patient flow diagram for the thesis (Dataset section).

Shows: initial cohort → exclusions → final analysis dataset.
Output: thesis/Figures/patient_flow.pdf
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

fig, ax = plt.subplots(figsize=(7, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis("off")

box_style = dict(
    boxstyle="round,pad=0.5",
    facecolor="white",
    edgecolor="black",
    linewidth=1.2,
)
excl_style = dict(
    boxstyle="round,pad=0.4",
    facecolor="#f0f0f0",
    edgecolor="gray",
    linewidth=1.0,
)

# Box 1: Initial cohort
ax.text(
    5, 11, "56 patients, 138 imaging studies\n"
    "Hospital Clínic de Barcelona\n"
    "Oct 2016 – Jan 2020",
    ha="center", va="center", fontsize=10,
    bbox=box_style,
)

# Arrow 1
ax.annotate(
    "", xy=(5, 9.6), xytext=(5, 10.2),
    arrowprops=dict(arrowstyle="->" , lw=1.2),
)

# Exclusion box (right)
ax.text(
    8.2, 9.9, "Excluded (n = 1):\n"
    "Study 47_01\n"
    "(no images available)",
    ha="center", va="center", fontsize=8.5,
    bbox=excl_style,
)
ax.annotate(
    "", xy=(7.0, 9.9), xytext=(5.8, 9.9),
    arrowprops=dict(arrowstyle="->", lw=1.0, color="gray"),
)

# Box 2: Radiomics extraction
ax.text(
    5, 8.8, "55 patients, 137 studies\n"
    "Radiomics features extracted\n"
    "(93 features per study)",
    ha="center", va="center", fontsize=10,
    bbox=box_style,
)

# Arrow 2
ax.annotate(
    "", xy=(5, 7.4), xytext=(5, 8.0),
    arrowprops=dict(arrowstyle="->", lw=1.2),
)

# Box 3: Merged dataset
ax.text(
    5, 6.6, "137 studies in merged\n"
    "radiomics–clinical dataset",
    ha="center", va="center", fontsize=10,
    bbox=box_style,
)

# Arrow 3 (splits)
ax.annotate(
    "", xy=(3.0, 5.0), xytext=(5, 5.9),
    arrowprops=dict(arrowstyle="->", lw=1.2),
)
ax.annotate(
    "", xy=(7.0, 5.0), xytext=(5, 5.9),
    arrowprops=dict(arrowstyle="->", lw=1.2),
)

# Box 4a: No rejection
ax.text(
    3.0, 4.3, "No rejection\n"
    "n = 98 studies\n"
    "(71%)",
    ha="center", va="center", fontsize=10,
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="#e8f4e8",
        edgecolor="black",
        linewidth=1.2,
    ),
)

# Box 4b: Rejection
ax.text(
    7.0, 4.3, "Rejection\n"
    "n = 39 studies\n"
    "(29%)",
    ha="center", va="center", fontsize=10,
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="#fce8e8",
        edgecolor="black",
        linewidth=1.2,
    ),
)

# Note at bottom
ax.text(
    5, 2.8,
    "14 patients contributed studies to both groups\n"
    "Studies per patient: 1–7 (mean 2.5)",
    ha="center", va="center", fontsize=9,
    fontstyle="italic", color="#444444",
)

plt.tight_layout()

out_path = PROJECT_ROOT / "thesis" / "Figures" / "patient_flow.pdf"
fig.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved: {out_path}")

out_path_png = out_path.with_suffix(".png")
fig.savefig(out_path_png, dpi=300, bbox_inches="tight")
print(f"Saved: {out_path_png}")
plt.close()
