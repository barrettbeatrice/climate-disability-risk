"""
build_fig5_regression_forest.py
================================
Forest plot of the spatial-error regression coefficients.

This is the visual answer to Part 1 Question 2: "What structural factors
differentiate high-risk from low-risk counties?"

The previous visual suite (fig1 bivariate choropleth, fig2 top-10 bars,
fig3 scatter quadrants, fig4 LISA cluster map) all answered Question 1
(WHERE convergent risk is located). Question 2 was reported as a text
table only. This figure extends the suite to fig5.

Estimates are drawn from notebooks/part1_statistical_analysis.py:
spatial-error (Kelejian-Prucha GM) regression of the dual-percentile
vulnerability index on ACS 5-year (2022) covariates plus state fixed
effects, n=3,098, OLS R^2=0.581, spatial pseudo-R^2=0.548, lambda=+0.604.

Reading the plot:
- Coefficients to the LEFT of zero (negative beta) indicate the variable
  is associated with LOWER convergent vulnerability holding everything
  else fixed.
- Coefficients to the RIGHT of zero (positive beta) indicate the variable
  is associated with HIGHER convergent vulnerability.
- Whiskers are +/- 1.96 * SE (approximate 95% CI for asymptotic
  z-tests with the GM library's reported standard errors).
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

PROJECT_ROOT = Path("/sessions/charming-dreamy-thompson/mnt/climate-disability-risk")
VIZ_DIR = PROJECT_ROOT / "visualizations"

# Estimates from docs/part1_statistical_findings.md table
# (spatial-error specification, standardized covariate effects).
COEFS = [
    # (label,                 beta,    se,    p,         note)
    ("log Median Income",   -33.001, 3.406, 0.000,     "Dominant negative driver"),
    ("log Medicare Pop",     +7.244, 0.437, 0.000,     "Scale of denominator"),
    ("Pct Uninsured",        +0.220, 0.059, 0.000174,  "Positive significant"),
    ("Pct 65+",              -0.075, 0.049, 0.130,     "Not significant"),
    ("Pct Below Poverty",    +0.050, 0.064, 0.433,     "Not significant"),
]

# Color rule: dark navy if p<0.01, magenta if 0.01<=p<0.05,
# medium grey if p>=0.05. Mirrors the Stevens.pinkblue family used
# elsewhere in the suite so this fig reads as the same family.
def color_for(p):
    if p < 0.01:
        return "#3b4994"    # deep navy — strong signal
    if p < 0.05:
        return "#be64ac"    # magenta — borderline
    return "#9b9b9b"        # grey — null

def main():
    labels = [c[0] for c in COEFS]
    betas = np.array([c[1] for c in COEFS])
    ses   = np.array([c[2] for c in COEFS])
    pvals = np.array([c[3] for c in COEFS])
    notes = [c[4] for c in COEFS]

    # Sort by |beta| descending for visual readability
    order = np.argsort(-np.abs(betas))
    labels = [labels[i] for i in order]
    betas = betas[order]
    ses   = ses[order]
    pvals = pvals[order]
    notes = [notes[i] for i in order]

    y = np.arange(len(labels))[::-1]   # plot top-down
    colors = [color_for(p) for p in pvals]

    fig = plt.figure(figsize=(13, 7), facecolor="white")
    ax = fig.add_axes([0.32, 0.16, 0.62, 0.74])

    ax.axvline(0, color="#666", lw=0.9, zorder=1)
    ax.errorbar(
        betas, y, xerr=1.96 * ses,
        fmt="o", markersize=11,
        ecolor="#444", elinewidth=1.4, capsize=5, capthick=1.4,
        markerfacecolor="white", markeredgewidth=2.2,
        zorder=3,
    )
    # Recolor the markers per significance tier
    for i, (b, c) in enumerate(zip(betas, colors)):
        ax.plot(b, y[i], "o", markersize=11, mfc=c, mec=c, zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=12)
    ax.set_xlabel(r"Standardized coefficient $\beta$ on dual-percentile vulnerability index",
                  fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=10)

    # Annotate each row with beta (SE) and p-value
    xmax = max(np.abs(betas) + 1.96 * ses) * 1.05
    ax.set_xlim(-xmax, xmax)
    for i, (b, s, p, n) in enumerate(zip(betas, ses, pvals, notes)):
        sign = "+" if b >= 0 else "-"
        # right-aligned annotation outside the plot area
        ptxt = "p<0.001" if p < 0.001 else f"p={p:.3f}"
        ax.annotate(
            f"{sign}{abs(b):.2f}  ({s:.2f})  {ptxt}",
            xy=(xmax * 1.02, y[i]),
            xycoords=("data", "data"),
            ha="left", va="center",
            fontsize=9.5, color="#333", clip_on=False,
        )

    # Title block
    fig.text(0.04, 0.93,
             "Spatial-error regression — what structural factors differentiate\n"
             "high-risk from low-risk counties?",
             fontsize=18, fontweight="bold", va="top")
    fig.text(0.04, 0.83,
             "Outcome: dual-percentile vulnerability index (0–100). Predictors: ACS 5-year (2022) "
             "structural covariates plus state fixed effects.\n"
             "Spatial error correction (Kelejian-Prucha GM): λ = +0.604, OLS R² = 0.581, "
             "spatial pseudo-R² = 0.548, n = 3,098.",
             fontsize=10.5, color="#444", va="top")

    # Legend (significance tier)
    handles = [
        Patch(color="#3b4994", label="p < 0.01"),
        Patch(color="#be64ac", label="0.01 ≤ p < 0.05"),
        Patch(color="#9b9b9b", label="p ≥ 0.05 (not significant)"),
    ]
    leg = ax.legend(
        handles=handles, loc="lower right",
        bbox_to_anchor=(1.02, -0.16),
        fontsize=9, frameon=True, framealpha=0.96,
        title="Significance tier", title_fontsize=10, ncol=3,
    )
    leg.get_frame().set_edgecolor("#cccccc")

    # Right-side header above annotations
    fig.text(0.945, 0.83, "β  (SE)        p-value",
             ha="right", va="top", fontsize=9.5, color="#666",
             fontweight="bold")

    # Footer
    fig.text(0.5, 0.04,
             "Standardized covariate effects from spatial-error model. "
             "Negative β → covariate is associated with LOWER convergent vulnerability. "
             "Whiskers ± 1.96 × SE.",
             ha="center", fontsize=9, color="#777")
    fig.text(0.5, 0.015,
             "Source: HHS emPOWER (Dec 2025) + FEMA NRI (Dec 2025) + ACS 5-year (2022). "
             "n = 3,098 CONUS counties.",
             ha="center", fontsize=8.5, color="#888")

    out = VIZ_DIR / "fig5_regression_forest.png"
    fig.savefig(out, dpi=300, facecolor="white")
    plt.close(fig)
    print(f">> {out}")


if __name__ == "__main__":
    main()
