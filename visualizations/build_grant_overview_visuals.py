"""
build_grant_overview_visuals.py
================================
Generate three slide-ready visualizations for Dr. Alexander's grant overview:

  (1) Bivariate choropleth — hazard percentile × power-dependency percentile.
      The lead visual. Encodes the two-typology framing in a single map:
      Intermountain West counties light up on the power-dependency axis;
      South Florida coastal counties light up on the hazard axis; San
      Juan NM lights up on both. Puerto Rico shown in a dedicated inset
      along the power-dependency axis only (FEMA NRI: Insufficient Data).

  (2) Top-10 horizontal bar chart with split bars.
      For each of the top-10 most vulnerable counties, shows hazard pctile
      and power-dependency pctile side-by-side so the audience can SEE
      the two pathways into the top 10.

  (3) Scatter quadrant plot.
      Every US county plotted on (hazard pctile, power pctile). The four
      quadrants make the typology framing literal. Key counties annotated:
      Intermountain West (San Juan NM, El Paso CO, Bernalillo NM, Mesa CO)
      vs. South Florida coast (Palm Beach FL, Miami-Dade FL, Broward FL).

Population denominator in all three figures: electricity-dependent
Medicare beneficiaries (HHS emPOWER). SCI is the clinical motivation
but cannot be isolated in public data; all rates and percentiles
describe the electricity-dependent Medicare population.

Audience: Dr. Marcalee Alexander; clinical-research / preparedness-policy
audience. Comments are written for that reader, not for software engineers.
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.lines import Line2D

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
PROJECT_ROOT = Path("/sessions/charming-dreamy-thompson/mnt/climate-disability-risk")
DATA_DIR = PROJECT_ROOT / "data"
VIZ_DIR = PROJECT_ROOT / "visualizations"
SHAPEFILE = DATA_DIR / "cb_2022_us_county_5m" / "cb_2022_us_county_5m.shp"
ANALYSIS_CSV = DATA_DIR / "part1_analysis_ready.csv"

# ------------------------------------------------------------------
# Visual identity — single palette across all three figures
# ------------------------------------------------------------------
# Bivariate choropleth uses the canonical Stevens.pinkblue palette
# (Joshua Stevens 2015, codified in the R `biscale` package). Pink along
# the hazard axis, teal along the power-dependency axis, deep navy where
# both are high — perceptually balanced, peer-tested, colorblind-safe.
#
#                       power_low   power_mid   power_hi
#       hazard_low   :  #e8e8e8     #ace4e4     #5ac8c8
#       hazard_mid   :  #dfb0d6     #a5add3     #5698b9
#       hazard_high  :  #be64ac     #8c62aa     #3b4994
BIVARIATE_PALETTE = {
    (0, 0): "#e8e8e8",  # low haz / low power      — neutral grey
    (0, 1): "#ace4e4",  # low haz / mid power      — light teal
    (0, 2): "#5ac8c8",  # low haz / high power     — vivid teal
    (1, 0): "#dfb0d6",  # mid haz / low power      — light pink
    (1, 1): "#a5add3",  # mid / mid                 — mauve
    (1, 2): "#5698b9",  # mid haz / high power     — blue
    (2, 0): "#be64ac",  # high haz / low power     — vivid pink (S. Florida)
    (2, 1): "#8c62aa",  # high haz / mid power     — violet
    (2, 2): "#3b4994",  # high / high              — deep navy (San Juan NM)
}

# Single-axis power-dependency ramp — used for Puerto Rico, where FEMA NRI
# returns "Insufficient Data" for all 78 municipios so we cannot place PR
# on the bivariate plane. Same teal hue as the power-dep axis above so PR
# reads as "this is the same dependency axis" without implying a hazard
# value we don't actually have.
POWER_RAMP = ["#e8e8e8", "#bee5e5", "#7fcaca", "#5ac8c8", "#3a9c9c"]

# Annotation reference counties — the named two-typology anchors
INTERMOUNTAIN_ANCHORS = [
    ("San Juan", "NM"),
    ("El Paso", "CO"),
    ("Bernalillo", "NM"),
    ("Mesa", "CO"),
    ("Utah", "UT"),
]
SOUTHEAST_ANCHORS = [
    ("Palm Beach", "FL"),
    ("Miami-Dade", "FL"),
    ("Broward", "FL"),
]

# Matplotlib defaults — generous, slide-friendly
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#222222",
    "axes.titlecolor": "#111111",
    "axes.titleweight": "bold",
    "axes.titlesize": 18,
    "axes.labelsize": 13,
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "font.family": "DejaVu Sans",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


# ------------------------------------------------------------------
# Data load
# ------------------------------------------------------------------
def load_data():
    """Load the analysis-ready county table and the Census TIGER county
    shapefile, joining on FIPS. Returns:
      conus  — county GeoDataFrame for the contiguous 48 (Albers projected)
      pr     — Puerto Rico municipios GeoDataFrame (separate for inset)
      df     — full analytical table including a fresh national power-dep
               percentile that includes PR municipios (for the inset)."""
    df = pd.read_csv(ANALYSIS_CSV, dtype={"FIPS": str, "BENE_GEO_CD": str, "STCOFIPS": str})
    df["FIPS"] = df["FIPS"].str.zfill(5)

    # Compute a US+PR national percentile for power-dependency rate. The
    # existing power_pctile in the file is over CONUS-scored counties only;
    # PR municipios were dropped at scoring because they have no FEMA
    # hazard data. For the inset we want PR to read off a national
    # distribution that includes PR itself.
    df["power_pctile_natl_pr"] = (
        df["total_power_dependent_rate"].rank(pct=True, na_option="keep") * 100
    )

    gdf = gpd.read_file(SHAPEFILE)
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)

    merged = gdf.merge(df, left_on="GEOID", right_on="FIPS", how="left")

    # CONUS = lower-48 + DC. Excluded: 02 AK, 15 HI, 60 AS, 66 GU, 69 MP,
    # 72 PR, 78 VI. PR is split out and shown in its own inset axis.
    conus_excl = {"02", "15", "60", "66", "69", "72", "78"}
    conus = merged[~merged["GEOID"].str[:2].isin(conus_excl)].copy()
    pr = merged[merged["GEOID"].str[:2] == "72"].copy()

    # Project both to US-friendly equal-area projections.
    conus = conus.to_crs("ESRI:102003")  # USA Contiguous Albers
    # For PR we use a Puerto Rico State Plane projection (NAD83 / PR & VI)
    # to keep municipios undistorted in the inset.
    if not pr.empty:
        pr = pr.to_crs("EPSG:32161")

    return conus, pr, df


# ------------------------------------------------------------------
# Helper — bivariate bin assignment
# ------------------------------------------------------------------
def assign_bivariate_bins(df, hazard_col="hazard_pctile_5", power_col="power_pctile"):
    """Assign each county to a 3x3 bivariate cell by tertiles within the
    SCORED universe (counties with both percentiles non-null).

    Tertiles are explicit at the 33.3 / 66.7 percentile cutoffs of each
    axis. We use percentile cutoffs (not raw value cutoffs) to keep cell
    counts roughly balanced — important for a readable map.
    """
    df = df.copy()

    def tertile(val):
        if pd.isna(val):
            return np.nan
        if val < 33.34:
            return 0
        if val < 66.67:
            return 1
        return 2

    df["_hazard_bin"] = df[hazard_col].apply(tertile)
    df["_power_bin"] = df[power_col].apply(tertile)

    def bin_color(row):
        h, p = row["_hazard_bin"], row["_power_bin"]
        if pd.isna(h) or pd.isna(p):
            return "#f5f5f5"  # not scored — soft grey
        return BIVARIATE_PALETTE[(int(h), int(p))]

    df["_bivariate_color"] = df.apply(bin_color, axis=1)
    return df


# ------------------------------------------------------------------
# Figure 1 — Bivariate choropleth (the LEAD visual)
# ------------------------------------------------------------------
def fig1_bivariate_choropleth(conus, pr):
    """Render the bivariate choropleth and save as PNG.

    Visual encoding (Stevens.pinkblue palette):
      - hazard axis (rows) = light grey → light pink → vivid magenta
      - power-dep axis (cols) = light grey → light teal → vivid teal
      - diagonal high/high → deep navy (the most vulnerable counties)

    Puerto Rico is shown as a separate inset because FEMA NRI returns
    "Insufficient Data" for all 78 PR municipios. PR is shaded along the
    power-dependency axis only (using a single-hue teal ramp matching the
    main palette's power axis), with an explicit data-gap callout.
    """
    conus = assign_bivariate_bins(conus)

    fig = plt.figure(figsize=(17, 10))
    ax = fig.add_axes([0.02, 0.06, 0.96, 0.86])

    # Soft state outlines underneath: dissolve counties to states
    states = conus.dissolve(by="STATEFP", as_index=False)
    states.boundary.plot(ax=ax, color="#888888", linewidth=0.6, zorder=2)

    # Plot counties in their bivariate color
    conus.plot(
        ax=ax,
        color=conus["_bivariate_color"].values,
        edgecolor="white",
        linewidth=0.08,
        zorder=1,
    )

    # Headline title
    ax.set_title(
        "Convergent climate-and-disability vulnerability — US counties",
        loc="left",
        pad=18,
        fontsize=22,
    )
    ax.text(
        0.005, 1.005,
        "FEMA NRI hazard percentile × electricity-dependent Medicare beneficiary rate",
        transform=ax.transAxes,
        fontsize=14,
        color="#444444",
        va="bottom",
    )

    ax.set_axis_off()

    # ---- Inset legend: 3x3 bivariate swatch -----------------------
    legend_ax = fig.add_axes([0.04, 0.10, 0.13, 0.16])
    for hi in range(3):
        for pi in range(3):
            color = BIVARIATE_PALETTE[(hi, pi)]
            legend_ax.add_patch(
                mpatches.Rectangle((pi, hi), 1, 1, facecolor=color, edgecolor="white", linewidth=1.2)
            )
    legend_ax.set_xlim(0, 3)
    legend_ax.set_ylim(0, 3)
    legend_ax.set_aspect("equal")
    legend_ax.set_xticks([])
    legend_ax.set_yticks([])
    legend_ax.spines[:].set_visible(False)
    legend_ax.invert_yaxis()  # high-hazard at bottom (matches map convention)

    legend_ax.annotate(
        "", xy=(3.1, 3.0), xytext=(0, 3.0),
        arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
        annotation_clip=False,
    )
    legend_ax.annotate(
        "", xy=(0, -0.1), xytext=(0, 3.0),
        arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
        annotation_clip=False,
    )
    legend_ax.text(1.5, 3.45, "More power-dependent →", ha="center", va="top", fontsize=10, color="#222")
    legend_ax.text(-0.18, 1.5, "More climate hazard →", ha="right", va="center", fontsize=10, color="#222", rotation=90)
    legend_ax.text(1.5, -0.30, "Bivariate legend (Stevens.pinkblue)", ha="center", va="bottom", fontsize=11, fontweight="bold", color="#111")

    # ---- Puerto Rico inset --------------------------------------
    # Lower-right corner. Power-dependency only; FEMA NRI insufficient.
    pr_ax = fig.add_axes([0.78, 0.06, 0.20, 0.22])
    if not pr.empty:
        # Color PR municipios along the power-dependency ramp using
        # power_pctile_natl_pr (computed against US+PR distribution).
        from matplotlib.colors import LinearSegmentedColormap
        pr_cmap = LinearSegmentedColormap.from_list("pr_power", POWER_RAMP)

        pr_colored = pr.copy()
        # Default to neutral grey if rate missing
        def pr_color(v):
            if pd.isna(v):
                return "#eaeaea"
            return pr_cmap(v / 100.0)
        pr_colored["_pr_color"] = pr_colored["power_pctile_natl_pr"].apply(pr_color)

        pr_colored.plot(
            ax=pr_ax,
            color=pr_colored["_pr_color"].values,
            edgecolor="white",
            linewidth=0.3,
        )
        # Hatch overlay to flag the "no FEMA hazard data" status
        pr_colored.boundary.plot(ax=pr_ax, color="#444444", linewidth=0.4)

    pr_ax.set_axis_off()
    pr_ax.set_title("Puerto Rico", fontsize=12, fontweight="bold", color="#111", loc="left", pad=2)
    pr_ax.text(
        0, -0.05,
        "78 municipios shown by power-dependency percentile.\n"
        "FEMA NRI: Insufficient Data — hazard score not available.",
        transform=pr_ax.transAxes,
        fontsize=8.5, color="#555", va="top",
    )

    # Tiny colorbar for the PR ramp
    pr_cb_ax = fig.add_axes([0.78, 0.04, 0.20, 0.012])
    pr_cb_ax.imshow(
        np.linspace(0, 1, 256).reshape(1, -1),
        aspect="auto", cmap=LinearSegmentedColormap.from_list("pr_power", POWER_RAMP),
    )
    pr_cb_ax.set_xticks([0, 128, 255])
    pr_cb_ax.set_xticklabels(["low", "median", "high"], fontsize=8, color="#555")
    pr_cb_ax.set_yticks([])
    for spine in pr_cb_ax.spines.values():
        spine.set_visible(False)

    # ---- Two-typology callouts on the map ------------------------
    iw_label_xy = _state_centroid(conus, ["NM", "CO", "UT", "AZ"])
    se_label_xy = _state_centroid(conus, ["FL"])

    # Intermountain West — high/high navy in the palette
    ax.annotate(
        "Intermountain West\n"
        "high power-dependency,\n"
        "moderate-to-high hazard",
        xy=iw_label_xy,
        xytext=(iw_label_xy[0] - 800_000, iw_label_xy[1] + 700_000),
        fontsize=12, fontweight="bold", color="#3b4994",
        ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#3b4994", lw=1.2, alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#3b4994", lw=1.2),
        zorder=10,
    )
    # South Florida coast — high-hazard pink in the palette. Pulled
    # north of the Florida label point so it doesn't collide with the
    # Puerto Rico inset in the lower-right.
    ax.annotate(
        "South Florida coast\n"
        "Top 1% climate hazard nationally,\n"
        "large absolute beneficiary count",
        xy=se_label_xy,
        xytext=(se_label_xy[0] - 1_500_000, se_label_xy[1] - 250_000),
        fontsize=12, fontweight="bold", color="#9c2d80",
        ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#be64ac", lw=1.2, alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#be64ac", lw=1.2),
        zorder=10,
    )

    # Footer — name the population and the framing
    fig.text(
        0.5, 0.025,
        "Population: electricity-dependent Medicare beneficiaries (HHS emPOWER). "
        "SCI is the clinical motivation; not isolatable in public data.",
        ha="center", fontsize=9, color="#444444",
    )
    fig.text(
        0.5, 0.010,
        "FEMA NRI (Dec 2025) · CMS HHS emPOWER (Dec 2025) · Census TIGER 2022   "
        "│   3,131 US counties scored + 78 PR municipios (FEMA NRI: Insufficient Data)",
        ha="center", fontsize=8.5, color="#777777",
    )

    out = VIZ_DIR / "fig1_bivariate_choropleth.png"
    fig.savefig(out, dpi=300, facecolor="white")
    plt.close(fig)
    return out


def _state_centroid(conus, state_abbrs):
    """Approximate centroid of a set of states, in projected coords."""
    rows = conus[conus["State"].isin(state_abbrs)]
    if rows.empty:
        # fallback to STUSPS column if present
        rows = conus[conus.get("STUSPS", pd.Series([])).isin(state_abbrs)] if "STUSPS" in conus.columns else rows
    if rows.empty:
        return (0, 0)
    diss = rows.dissolve()
    pt = diss.geometry.centroid.iloc[0]
    return (pt.x, pt.y)


# ------------------------------------------------------------------
# Figure 2 — Top-10 horizontal bar chart with split bars
# ------------------------------------------------------------------
def fig2_top10_split_bars(df):
    """Top-10 most vulnerable counties (by dual-percentile vulnerability index).
    Each county gets two stacked horizontal bars: hazard percentile (top)
    and power-dependency percentile (bottom). Color encodes the typology
    each county fits."""
    top = df.dropna(subset=["vulnerability_index_dual_pct"]).sort_values(
        "vulnerability_index_dual_pct", ascending=False
    ).head(10).copy()
    top["label"] = top["County"] + ", " + top["State"]
    top = top.iloc[::-1].reset_index(drop=True)  # reverse so rank 1 is at top

    fig, ax = plt.subplots(figsize=(14, 9))

    bar_h = 0.36
    y_positions = np.arange(len(top))

    hazard_color = "#c08b3f"
    power_color = "#5a9b9b"

    bars_h = ax.barh(
        y_positions + bar_h / 2,
        top["hazard_pctile_5"],
        height=bar_h,
        color=hazard_color,
        label="Climate-hazard percentile (FEMA NRI 5-hazard composite)",
        edgecolor="white", linewidth=0.6,
    )
    bars_p = ax.barh(
        y_positions - bar_h / 2,
        top["power_pctile"],
        height=bar_h,
        color=power_color,
        label="Power-dependency percentile (Medicare beneficiaries)",
        edgecolor="white", linewidth=0.6,
    )

    # Value labels at end of each bar
    for bar, val in zip(bars_h, top["hazard_pctile_5"]):
        ax.text(val + 0.6, bar.get_y() + bar.get_height() / 2, f"{val:.1f}",
                va="center", ha="left", fontsize=10, color="#444")
    for bar, val in zip(bars_p, top["power_pctile"]):
        ax.text(val + 0.6, bar.get_y() + bar.get_height() / 2, f"{val:.1f}",
                va="center", ha="left", fontsize=10, color="#444")

    # Vulnerability index column on the right
    for i, row in top.iterrows():
        ax.text(
            104, i,
            f"VI {row['vulnerability_index_dual_pct']:.1f}",
            va="center", ha="left",
            fontsize=11, fontweight="bold", color="#2a3f33",
        )

    # County names on the left axis
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f"#{r}  {l}" for r, l in zip(range(len(top), 0, -1), top["label"])], fontsize=12)

    ax.set_xlim(0, 110)
    ax.set_xlabel("National percentile (0 = lowest, 100 = highest)")
    ax.set_title("Top 10 most vulnerable US counties — two pathways into the top", loc="left", pad=42, fontsize=20)
    ax.text(
        0, 1.02,
        "Population denominator: electricity-dependent Medicare beneficiaries (HHS emPOWER). "
        "Some counties enter the top 10 via hazard exposure, others via power-dependency density. Most show both.",
        transform=ax.transAxes,
        fontsize=11.5, color="#555",
    )

    # Vertical reference lines at key percentiles
    for x, label in [(50, "median"), (90, "top 10%")]:
        ax.axvline(x, color="#bbbbbb", linewidth=0.8, linestyle="--", zorder=0)
        ax.text(x, len(top) - 0.3, label, ha="center", va="bottom", fontsize=9, color="#888")

    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=11)

    fig.text(
        0.5, 0.01,
        "Vulnerability index (VI) = mean of the two percentile axes (equal-weighted dual-percentile rescaling). "
        "Vulnerability is a property of the infrastructure-population system, not of individuals.",
        ha="center", fontsize=9, color="#555",
    )

    out = VIZ_DIR / "fig2_top10_split_bars.png"
    fig.savefig(out, dpi=300, facecolor="white")
    plt.close(fig)
    return out


# ------------------------------------------------------------------
# Figure 3 — Scatter quadrant plot with annotated anchors
# ------------------------------------------------------------------
def fig3_scatter_quadrants(df):
    """Scatter every scored county on the (hazard pctile, power pctile)
    plane. Quadrants make the typology framing explicit; key counties
    annotated by name."""
    s = df.dropna(subset=["hazard_pctile_5", "power_pctile", "vulnerability_index_dual_pct"]).copy()

    # Marker size scales with absolute count of power-dependent beneficiaries
    # so the audience can see that some "moderate-rate" Florida counties carry
    # very large absolute populations.
    sz = s["total_power_dependent_benes"].fillna(0)
    sz = 10 + 90 * (sz - sz.min()) / (sz.max() - sz.min() + 1e-9)

    fig, ax = plt.subplots(figsize=(13, 10))

    # Quadrant background tint — matches Stevens.pinkblue palette corners
    ax.axhspan(50, 100, xmin=0.5, xmax=1.0, facecolor="#3b4994", alpha=0.06, zorder=0)  # high/high navy
    ax.axhspan(50, 100, xmin=0.0, xmax=0.5, facecolor="#5ac8c8", alpha=0.08, zorder=0)  # power-only teal
    ax.axhspan(0, 50, xmin=0.5, xmax=1.0, facecolor="#be64ac", alpha=0.06, zorder=0)    # hazard-only pink

    # All counties as small dots, color-coded by VI
    sc = ax.scatter(
        s["hazard_pctile_5"],
        s["power_pctile"],
        c=s["vulnerability_index_dual_pct"],
        s=sz,
        cmap="viridis",
        alpha=0.65,
        edgecolor="white",
        linewidth=0.3,
        zorder=2,
    )

    # Quadrant gridlines at the medians
    ax.axvline(50, color="#888", linewidth=0.8, linestyle="--", zorder=1)
    ax.axhline(50, color="#888", linewidth=0.8, linestyle="--", zorder=1)

    # Quadrant labels — palette-coded to the typology each quadrant evokes
    ax.text(2, 53, "High dependency,\nlow hazard",
            fontsize=10, color="#3a9c9c", fontweight="bold", va="bottom")
    ax.text(52, 53, "HIGH ON BOTH — convergent risk",
            fontsize=11, color="#3b4994", fontweight="bold", va="bottom", ha="left")
    ax.text(98, 47, "High hazard,\nlow dependency",
            fontsize=10, color="#9c2d80", fontweight="bold", va="top", ha="right")
    ax.text(2, 47, "Low on both",
            fontsize=10, color="#888", va="top")

    # Annotate Intermountain West anchors — fan labels out into the
    # upper-left so they don't overlap with the SE anchors or the quadrant
    # label.
    iw_label_offsets = {
        "San Juan":   (-30,  -6),
        "El Paso":    (-30, -12),
        "Bernalillo": (-30, -18),
        "Mesa":       (-30, -24),
        "Utah":       (-30, -30),
    }
    for cname, st in INTERMOUNTAIN_ANCHORS:
        row = s[(s["County"] == cname) & (s["State"] == st)]
        if row.empty:
            continue
        x, y = row["hazard_pctile_5"].iloc[0], row["power_pctile"].iloc[0]
        dx, dy = iw_label_offsets.get(cname, (-25, 5))
        ax.annotate(
            f"{cname}, {st}",
            xy=(x, y),
            xytext=(x + dx, y + dy),
            fontsize=10, fontweight="bold", color="#3b4994",
            arrowprops=dict(arrowstyle="-", color="#3b4994", lw=0.6, alpha=0.7),
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#3b4994", lw=0.6, alpha=0.92),
        )

    # Southeast anchors — labels fan out below their points so they sit
    # in clean space along the bottom right of the plot. We keep them
    # well above the x-axis so they don't clip.
    se_label_offsets = {
        "Palm Beach":  (-32, 18),
        "Miami-Dade":  (-32, 12),
        "Broward":     (-32, 24),
    }
    for cname, st in SOUTHEAST_ANCHORS:
        row = s[(s["County"] == cname) & (s["State"] == st)]
        if row.empty:
            continue
        x, y = row["hazard_pctile_5"].iloc[0], row["power_pctile"].iloc[0]
        dx, dy = se_label_offsets.get(cname, (-15, -15))
        ax.annotate(
            f"{cname}, {st}",
            xy=(x, y),
            xytext=(x + dx, y + dy),
            fontsize=10, fontweight="bold", color="#9c2d80",
            arrowprops=dict(arrowstyle="-", color="#9c2d80", lw=0.6, alpha=0.7),
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#be64ac", lw=0.6, alpha=0.92),
        )

    ax.set_xlim(-2, 102)
    ax.set_ylim(-2, 102)
    ax.set_xlabel("Climate-hazard percentile (FEMA NRI 5-hazard composite)")
    ax.set_ylabel("Power-dependency percentile (Medicare beneficiaries)")
    ax.set_title("Two pathways to convergent risk — every US county on one plot", loc="left", pad=42, fontsize=20)
    ax.text(
        0, 1.02,
        "Population: electricity-dependent Medicare beneficiaries (HHS emPOWER). "
        "Marker size = absolute count; color = vulnerability index.",
        transform=ax.transAxes,
        fontsize=11, color="#555",
    )

    cbar = fig.colorbar(sc, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label("Vulnerability index (dual-percentile)")
    ax.spines[["top", "right"]].set_visible(False)

    fig.text(
        0.5, 0.01,
        "n = 3,131 US counties scored. Annotated counties are headline reference points for the two-typology narrative. "
        "Puerto Rico (78 municipios) excluded from this plot — FEMA NRI returns Insufficient Data on the hazard axis.",
        ha="center", fontsize=9, color="#555",
    )

    out = VIZ_DIR / "fig3_scatter_quadrants.png"
    fig.savefig(out, dpi=300, facecolor="white")
    plt.close(fig)
    return out


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    VIZ_DIR.mkdir(exist_ok=True)
    print(">> Loading data ...")
    conus, pr, df = load_data()
    print(f"   conus: {len(conus)} county geometries")
    print(f"   PR municipios: {len(pr)}")
    print(f"   scored counties: {df['vulnerability_index_dual_pct'].notna().sum()}")

    print(">> Figure 1 — bivariate choropleth ...")
    p1 = fig1_bivariate_choropleth(conus, pr)
    print(f"   {p1}")

    print(">> Figure 2 — top-10 split bars ...")
    p2 = fig2_top10_split_bars(df)
    print(f"   {p2}")

    print(">> Figure 3 — scatter quadrants ...")
    p3 = fig3_scatter_quadrants(df)
    print(f"   {p3}")

    print(">> Done.")


if __name__ == "__main__":
    main()
