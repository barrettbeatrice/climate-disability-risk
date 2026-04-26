"""
build_dashboard_payload.py
==========================
Pre-aggregate the analysis-ready table and the Census TIGER county
shapefile into the two payloads that power grant_overview_dashboard.html:

  - countiesTopo (TopoJSON) — simplified CONUS county geometry
  - data         (Array<Record>) — one row per scored county with the
                  fields the dashboard charts and tables consume

Both are written as plain JSON (a python dict) and saved next to this
script. The HTML dashboard `cat`s them inline at build time.

Comments here are written for the clinical-research audience: this is
the bridge that takes the Pythonic analysis output and hands it to the
web layer.
"""

import json
from pathlib import Path

import pandas as pd
import geopandas as gpd
import topojson as tp

# ------------------------------------------------------------------
PROJECT_ROOT = Path("/sessions/charming-dreamy-thompson/mnt/climate-disability-risk")
DATA_DIR = PROJECT_ROOT / "data"
VIZ_DIR = PROJECT_ROOT / "visualizations"
SHAPEFILE = DATA_DIR / "cb_2022_us_county_5m" / "cb_2022_us_county_5m.shp"
ANALYSIS_CSV = DATA_DIR / "part1_analysis_ready.csv"

# Drop AK, HI, and the small territories (AS, GU, MP, VI) — keep CONUS + PR.
# Puerto Rico (state FIPS 72) is included because it is a key climate-and-
# disability site even though FEMA NRI marks it Insufficient Data; the
# dashboard will show PR on layers that don't require a hazard score.
EXCLUDED_STATEFP = {"02", "15", "60", "66", "69", "78"}

# Output files
TOPO_OUT = VIZ_DIR / "_dashboard_counties_topo.json"
DATA_OUT = VIZ_DIR / "_dashboard_county_data.json"


def main():
    print(">> Loading CSV ...")
    df = pd.read_csv(ANALYSIS_CSV, dtype={"FIPS": str, "BENE_GEO_CD": str, "STCOFIPS": str})
    df["FIPS"] = df["FIPS"].str.zfill(5)

    # Compute a national power-dependency percentile that includes PR
    # municipios. The original `power_pctile` was computed over scored
    # counties only (PR excluded because FEMA NRI is missing). The
    # dashboard needs PR to render on the power-dep layer, so we add a
    # parallel percentile here that's defined for every county/municipio
    # with a power-dependency rate.
    df["power_pctile_natl_pr"] = (
        df["total_power_dependent_rate"].rank(pct=True, na_option="keep") * 100
    )

    keep_cols = [
        "FIPS", "County", "State",
        "total_medicare_benes", "total_power_dependent_benes",
        "o2_services_benes", "home_health_benes", "hospice_benes",
        "any_healthcare_benes",
        "total_power_dependent_rate", "o2_services_rate", "home_health_rate",
        "hospice_rate", "any_healthcare_rate", "dsbld_rate",
        "composite_hazard_score", "composite_hazard_5",
        "hazard_pctile_5", "power_pctile", "power_pctile_natl_pr",
        "vulnerability_index_dual_pct",
    ]
    df_lean = df[keep_cols].copy()

    # Round numeric columns to keep JSON size reasonable
    for c in df_lean.columns:
        if pd.api.types.is_float_dtype(df_lean[c]):
            df_lean[c] = df_lean[c].round(2)

    df_lean = df_lean[~df_lean["FIPS"].str[:2].isin(EXCLUDED_STATEFP)]

    # Records list
    records = df_lean.where(pd.notnull(df_lean), None).to_dict(orient="records")
    DATA_OUT.write_text(json.dumps(records, separators=(",", ":")))
    print(f"   wrote {DATA_OUT}  ({DATA_OUT.stat().st_size/1024:.0f} KB)  rows={len(records)}")

    print(">> Loading shapefile ...")
    gdf = gpd.read_file(SHAPEFILE)
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)
    gdf = gdf[~gdf["GEOID"].str[:2].isin(EXCLUDED_STATEFP)].copy()
    gdf = gdf[["GEOID", "STATEFP", "geometry"]].rename(columns={"GEOID": "FIPS"})

    print(f"   counties: {len(gdf)}")

    # Reproject to a US-friendly equal area projection for the map.
    # Albers Equal Area is the standard choice; we keep it in EPSG:4269
    # (NAD83 lat/lon) for the dashboard since D3.geoAlbersUsa expects
    # geographic coordinates.
    gdf = gdf.to_crs("EPSG:4326")

    # Simplify geometries — preserve topology via topojson.
    print(">> Building TopoJSON (simplification on shared arcs) ...")
    topo = tp.Topology(
        gdf,
        prequantize=True,
        topology=True,
    ).toposimplify(
        epsilon=0.01,           # ~1 km in degrees — fine for slide-quality choropleth
        simplify_algorithm="dp",
        simplify_with="shapely",
    )
    topo_obj = json.loads(topo.to_json())
    TOPO_OUT.write_text(json.dumps(topo_obj, separators=(",", ":")))
    print(f"   wrote {TOPO_OUT}  ({TOPO_OUT.stat().st_size/1024:.0f} KB)")

    print(">> Done.")


if __name__ == "__main__":
    main()
