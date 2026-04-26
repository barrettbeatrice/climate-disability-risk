"""
build_fig4_lisa_map.py
======================
Render the LISA cluster map produced by part1_statistical_analysis.py.

LISA = Local Moran's I on the dual-percentile vulnerability index. Each
county is classified into one of:
  HH — high-high : significantly high VI surrounded by significantly high VI
  LL — low-low   : significantly low VI surrounded by significantly low VI
  HL — outlier   : high VI surrounded by low VI
  LH — outlier   : low VI surrounded by high VI
  ns — not significant at p<0.05

This is the formal statistical analog of the "two-typology" choropleth:
the HH cluster identifies the Intermountain West and parts of the South
Florida coast as significantly clustered convergent vulnerability, the
LL cluster identifies the Plains/Midwest low-risk corridor, and the
outliers flag interesting individual counties for follow-up.
"""

from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

PROJECT_ROOT = Path("/sessions/charming-dreamy-thompson/mnt/climate-disability-risk")
DATA_DIR = PROJECT_ROOT / "data"
VIZ_DIR = PROJECT_ROOT / "visualizations"
SHAPEFILE = DATA_DIR / "cb_2022_us_county_5m" / "cb_2022_us_county_5m.shp"
LISA_CSV = DATA_DIR / "lisa_county_classification.csv"
ANALYSIS_CSV = DATA_DIR / "part1_analysis_ready.csv"

# Stevens.pinkblue-aligned palette so this figure reads as the same family
# as fig1: deep navy = HH (convergent), magenta = HL outlier, teal = LH
# outlier, neutral = LL, light grey = ns.
LISA_COLORS = {
    "HH": "#3b4994",   # deep navy — high/high cluster
    "LL": "#cfd2db",   # cool light grey — low/low cluster
    "HL": "#be64ac",   # magenta — high VI in low-VI neighborhood
    "LH": "#5ac8c8",   # teal — low VI in high-VI neighborhood
    "ns": "#f3f3f0",   # near-background — not significant
}
LISA_LABELS = {
    "HH": "High-high cluster (convergent vulnerability)",
    "LL": "Low-low cluster (low convergent risk)",
    "HL": "High VI outlier (in low-VI neighborhood)",
    "LH": "Low VI outlier (in high-VI neighborhood)",
    "ns": "Not significant (p ≥ 0.05)",
}


def main():
    print(">> Loading LISA + shapefile ...")
    lisa = pd.read_csv(LISA_CSV, dtype={"FIPS": str})
    lisa["FIPS"] = lisa["FIPS"].str.zfill(5)

    gdf = gpd.read_file(SHAPEFILE)
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)

    excl = {"02", "15", "60", "66", "69", "72", "78"}
    conus = gdf[~gdf["STATEFP"].isin(excl)].copy()

    merged = conus.merge(lisa[["FIPS", "lisa_label", "vulnerability_index_dual_pct",
                               "County", "State", "lisa_p"]],
                         left_on="GEOID", right_on="FIPS", how="left")
    merged["lisa_label"] = merged["lisa_label"].fillna("ns")
    merged["color"] = merged["lisa_label"].map(LISA_COLORS).fillna(LISA_COLORS["ns"])

    merged = merged.to_crs("ESRI:102003")

    fig = plt.figure(figsize=(17, 10), facecolor="white")
    ax = fig.add_axes([0.02, 0.06, 0.96, 0.86])

    states = merged.dissolve(by="STATEFP", as_index=False)
    states.boundary.plot(ax=ax, color="#888888", linewidth=0.6, zorder=2)

    merged.plot(
        ax=ax,
        color=merged["color"].values,
        edgecolor="white",
        linewidth=0.08,
        zorder=1,
    )

    ax.set_axis_off()
    ax.set_title(
        "LISA cluster map — convergent vulnerability hotspots and coldspots",
        loc="left", pad=18, fontsize=22,
    )
    ax.text(
        0.005, 1.005,
        "Local Moran's I on dual-percentile vulnerability index, Queen contiguity, p < 0.05",
        transform=ax.transAxes,
        fontsize=14, color="#444444", va="bottom",
    )

    # Legend in the lower-left
    handles = [
        mpatches.Patch(color=LISA_COLORS["HH"], label=LISA_LABELS["HH"]),
        mpatches.Patch(color=LISA_COLORS["LL"], label=LISA_LABELS["LL"]),
        mpatches.Patch(color=LISA_COLORS["HL"], label=LISA_LABELS["HL"]),
        mpatches.Patch(color=LISA_COLORS["LH"], label=LISA_LABELS["LH"]),
        mpatches.Patch(color=LISA_COLORS["ns"], label=LISA_LABELS["ns"], ec="#888"),
    ]
    leg = ax.legend(
        handles=handles, loc="lower left",
        bbox_to_anchor=(0.02, 0.02),
        fontsize=10, frameon=True, framealpha=0.96,
        title="LISA classification",
        title_fontsize=11,
    )
    leg.get_frame().set_edgecolor("#cccccc")

    # County-count footer
    counts = merged["lisa_label"].value_counts().to_dict()
    fig.text(
        0.5, 0.025,
        f"HH = {counts.get('HH', 0)} counties · LL = {counts.get('LL', 0)} · "
        f"HL = {counts.get('HL', 0)} · LH = {counts.get('LH', 0)} · "
        f"ns = {counts.get('ns', 0)} of {sum(counts.values())} CONUS counties scored",
        ha="center", fontsize=10, color="#444",
    )
    fig.text(
        0.5, 0.010,
        "999 conditional permutations. CONUS-only; Puerto Rico excluded from spatial model "
        "(FEMA NRI Insufficient Data). Population: HHS emPOWER electricity-dependent Medicare beneficiaries.",
        ha="center", fontsize=8.5, color="#777",
    )

    out = VIZ_DIR / "fig4_lisa_cluster_map.png"
    fig.savefig(out, dpi=300, facecolor="white")
    plt.close(fig)
    print(f">> {out}")


if __name__ == "__main__":
    main()
