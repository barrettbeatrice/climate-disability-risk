"""
Join CMS Provider of Services (POS) File to Climate-Disability Vulnerability Dataset.

PURPOSE
-------
Adds hospital/facility-level Medicare variables — aggregated to county — to the
existing vulnerability index. Enables three new analytical dimensions:
  1. Proximity / access  — count of IRFs, SNFs, and SCI-relevant facilities per county
  2. Capacity            — total certified beds and ICU beds per county
  3. Facility mix        — breakdown by provider type (hospital, rehab, SNF, HHA, hospice)

INPUTS
------
  data/climate_disability_vulnerability.csv   — existing joined FEMA + emPOWER file
  Downloaded live from CMS open data portal:
    https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/
    provider-of-services-file-hospital-non-hospital-facilities

OUTPUT
------
  data/vulnerability_with_facilities.csv      — enriched county-level dataset

CMS POS PROVIDER TYPE CODES (relevant subset)
---------------------------------------------
  01  Short-term acute care hospital
  02  Long-term care hospital
  06  Psychiatric hospital
  10  Rehabilitation hospital (IRF — most relevant for SCI population)
  11  Children's hospital
  13  Critical Access Hospital (CAH)
  14  Rural Emergency Hospital
  20  Skilled Nursing Facility (SNF)
  33  Home Health Agency (HHA)
  34  Hospice
  71  All-inclusive care for elderly (PACE)

JOIN KEY
--------
  Both datasets use 5-digit FIPS county code (zero-padded string).
  POS file field: FIPS_STATE_CD + FIPS_CNTY_CD  → must be concatenated.

NOTES FOR CLINICAL RESEARCHERS
-------------------------------
  - "Certified beds" = beds approved by CMS for Medicare/Medicaid patients.
    This is a regulatory minimum floor, not actual staffed capacity.
  - IRF count per county is the most policy-relevant metric for the SCI
    population: it measures whether electricity-dependent beneficiaries have
    access to inpatient rehabilitation if evacuated or hospitalized.
  - Counties with zero IRFs are particularly vulnerable — high hazard + high
    power dependency + no in-county rehab access = triple jeopardy.

USAGE
-----
  pip install pandas requests tqdm
  python notebooks/join_cms_pos.py
"""

import pandas as pd
import requests
import io
import os
import sys
from pathlib import Path

# ── 0. Paths ──────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent   # project root
DATA = ROOT / "data"
VULN_PATH  = DATA / "climate_disability_vulnerability.csv"
POS_CACHE  = DATA / "cms_pos_raw.csv"            # cached download
OUT_PATH   = DATA / "vulnerability_with_facilities.csv"

# ── 1. Download CMS POS file ──────────────────────────────────────────────────

CMS_POS_URL = (
    "https://data.cms.gov/sites/default/files/2024-10/"
    "8d5c28aa-4f58-4b2c-a14f-8b9f2e2a4a1a/"
    "pos2024.csv"
)

# Fallback: the CMS DKAN API endpoint for the POS dataset
CMS_API_URL = (
    "https://data.cms.gov/api/1/datastore/query/"
    "provider-of-services-file-hospital-non-hospital-facilities/0"
    "?limit=500000&offset=0"
)

def download_pos(cache_path: Path) -> pd.DataFrame:
    """
    Download the CMS Provider of Services file.
    Tries direct CSV download first; falls back to the DKAN query API.
    Caches locally so subsequent runs don't re-download.
    """
    if cache_path.exists():
        print(f"  Using cached POS file: {cache_path}")
        return pd.read_csv(cache_path, dtype=str, low_memory=False)

    print("  Downloading CMS POS file (this may take ~1–2 min)…")

    # Try direct CSV first
    for url in [CMS_POS_URL]:
        try:
            r = requests.get(url, timeout=120, stream=True)
            if r.status_code == 200 and "text/csv" in r.headers.get("Content-Type", ""):
                content = r.content
                df = pd.read_csv(io.BytesIO(content), dtype=str, low_memory=False)
                df.to_csv(cache_path, index=False)
                print(f"  Downloaded {len(df):,} rows → cached at {cache_path}")
                return df
        except Exception as e:
            print(f"  Direct download failed ({e}), trying API…")

    # Fallback: paginated DKAN API
    rows = []
    offset = 0
    page_size = 10000
    while True:
        api_url = (
            "https://data.cms.gov/api/1/datastore/query/"
            "provider-of-services-file-hospital-non-hospital-facilities/0"
            f"?limit={page_size}&offset={offset}&keys=true"
        )
        r = requests.get(api_url, timeout=60)
        if r.status_code != 200:
            raise RuntimeError(f"CMS API returned {r.status_code} at offset {offset}")
        data = r.json()
        page = data.get("results", [])
        if not page:
            break
        rows.extend(page)
        offset += len(page)
        print(f"    … fetched {offset:,} rows", end="\r")
        if len(page) < page_size:
            break

    df = pd.DataFrame(rows)
    df.to_csv(cache_path, index=False)
    print(f"\n  Downloaded {len(df):,} rows → cached at {cache_path}")
    return df


# ── 2. Clean and standardize POS columns ─────────────────────────────────────

# CMS POS uses inconsistent column name casing across annual releases.
# Map known aliases → canonical names used in this script.
COLUMN_MAP = {
    # FIPS fields
    "fips_state_cd":  "fips_state_cd",
    "FIPS_STATE_CD":  "fips_state_cd",
    "fips_cnty_cd":   "fips_cnty_cd",
    "FIPS_CNTY_CD":   "fips_cnty_cd",
    # Provider type
    "prvdr_ctgry_cd": "provider_type_cd",
    "PRVDR_CTGRY_CD": "provider_type_cd",
    "prvdr_ctgry_sbtyp_cd": "provider_subtype_cd",
    "PRVDR_CTGRY_SBTYP_CD": "provider_subtype_cd",
    # Bed counts
    "crtfd_bed_cnt":  "certified_beds",
    "CRTFD_BED_CNT":  "certified_beds",
    "bed_cnt":        "certified_beds",
    "BED_CNT":        "certified_beds",
    # ICU beds (not all releases include this)
    "icu_bed_cnt":    "icu_beds",
    "ICU_BED_CNT":    "icu_beds",
    # Active status
    "gnrl_cntl_type_cd": "control_type",
    "GNRL_CNTL_TYPE_CD": "control_type",
    "pgm_trmntn_cd":  "termination_cd",
    "PGM_TRMNTN_CD":  "termination_cd",
    # Provider NPI
    "npi": "npi",
    "NPI": "npi",
}

# Provider type codes to keep (Medicare-relevant acute/post-acute/rehab/HHA/hospice)
RELEVANT_PROVIDER_TYPES = {
    "01": "short_term_hospital",
    "02": "long_term_hospital",
    "06": "psychiatric_hospital",
    "10": "inpatient_rehab_facility",  # IRF — most relevant for SCI
    "11": "childrens_hospital",
    "13": "critical_access_hospital",
    "14": "rural_emergency_hospital",
    "20": "skilled_nursing_facility",
    "33": "home_health_agency",
    "34": "hospice",
}

def clean_pos(raw: pd.DataFrame) -> pd.DataFrame:
    """Rename columns, filter to active Medicare-certified facilities, build FIPS."""
    # Normalize column names
    raw.columns = [COLUMN_MAP.get(c, c.lower()) for c in raw.columns]

    # Build 5-digit county FIPS (zero-pad state to 2, county to 3)
    if "fips_state_cd" in raw.columns and "fips_cnty_cd" in raw.columns:
        raw["county_fips"] = (
            raw["fips_state_cd"].str.strip().str.zfill(2) +
            raw["fips_cnty_cd"].str.strip().str.zfill(3)
        )
    else:
        raise KeyError(
            "Could not find FIPS_STATE_CD / FIPS_CNTY_CD in POS file. "
            "Column names present: " + str(raw.columns.tolist()[:20])
        )

    # Filter to active facilities only (termination_cd == '00' means active)
    if "termination_cd" in raw.columns:
        raw = raw[raw["termination_cd"].str.strip() == "00"].copy()

    # Filter to relevant provider types
    if "provider_type_cd" not in raw.columns:
        raise KeyError("provider_type_cd not found. Check column mapping.")

    raw["provider_type_cd"] = raw["provider_type_cd"].str.strip().str.zfill(2)
    raw = raw[raw["provider_type_cd"].isin(RELEVANT_PROVIDER_TYPES)].copy()
    raw["provider_type_label"] = raw["provider_type_cd"].map(RELEVANT_PROVIDER_TYPES)

    # Coerce bed counts to numeric
    for col in ["certified_beds", "icu_beds"]:
        if col in raw.columns:
            raw[col] = pd.to_numeric(raw[col], errors="coerce").fillna(0)
        else:
            raw[col] = 0

    return raw[["county_fips", "provider_type_cd", "provider_type_label",
                "certified_beds", "icu_beds"]].copy()


# ── 3. Aggregate POS to county level ─────────────────────────────────────────

def aggregate_to_county(pos: pd.DataFrame) -> pd.DataFrame:
    """
    Produce one row per county with:
      - Facility counts by type (wide format)
      - Total certified beds and ICU beds
      - Total facility count
    """
    # Total beds and ICU beds across all facility types
    beds = (
        pos.groupby("county_fips")[["certified_beds", "icu_beds"]]
        .sum()
        .rename(columns={
            "certified_beds": "total_certified_beds",
            "icu_beds":        "total_icu_beds",
        })
    )

    # Facility count by provider type (pivot)
    counts = (
        pos.groupby(["county_fips", "provider_type_label"])
        .size()
        .unstack(fill_value=0)
        .add_prefix("n_")
    )

    # Ensure all expected columns exist even if no facilities of that type in data
    expected_cols = [f"n_{v}" for v in RELEVANT_PROVIDER_TYPES.values()]
    for col in expected_cols:
        if col not in counts.columns:
            counts[col] = 0

    # Total facility count
    counts["n_total_facilities"] = counts[expected_cols].sum(axis=1)

    county_pos = beds.join(counts, how="outer").fillna(0).reset_index()
    county_pos.rename(columns={"county_fips": "BENE_GEO_CD"}, inplace=True)
    return county_pos


# ── 4. Derive capacity metrics ────────────────────────────────────────────────

def add_derived_metrics(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Add policy-relevant derived columns.
    All rates are per 1,000 power-dependent Medicare beneficiaries.
    """
    benes = merged["total_power_dependent_benes"].replace(0, float("nan"))

    # Beds per 1,000 power-dependent beneficiaries
    merged["beds_per_1k_power_dep"] = (
        merged["total_certified_beds"] / benes * 1000
    ).round(1)

    merged["icu_beds_per_1k_power_dep"] = (
        merged["total_icu_beds"] / benes * 1000
    ).round(1)

    # IRF access flag: 1 if at least one inpatient rehab facility in county
    merged["has_inpatient_rehab"] = (
        merged["n_inpatient_rehab_facility"] > 0
    ).astype(int)

    # Critical access hospital flag
    merged["has_critical_access_hospital"] = (
        merged["n_critical_access_hospital"] > 0
    ).astype(int)

    # Triple jeopardy flag: top-quartile vulnerability + no IRF + low bed ratio
    # (computed after we know the distribution)
    q75_vuln = merged["vulnerability_index"].quantile(0.75)
    q25_beds = merged["beds_per_1k_power_dep"].quantile(0.25)

    merged["triple_jeopardy"] = (
        (merged["vulnerability_index"] >= q75_vuln) &
        (merged["has_inpatient_rehab"] == 0) &
        (merged["beds_per_1k_power_dep"] <= q25_beds)
    ).astype(int)

    print(f"\n  Triple-jeopardy counties (high risk + no IRF + low beds): "
          f"{merged['triple_jeopardy'].sum():,}")

    return merged


# ── 5. Main ───────────────────────────────────────────────────────────────────

def main():
    print("\n=== CMS POS → Vulnerability Join Pipeline ===\n")

    # Load existing vulnerability dataset
    if not VULN_PATH.exists():
        sys.exit(f"ERROR: {VULN_PATH} not found. Run the main analysis pipeline first.")
    vuln = pd.read_csv(VULN_PATH, dtype={"BENE_GEO_CD": str})
    vuln["BENE_GEO_CD"] = vuln["BENE_GEO_CD"].str.zfill(5)
    print(f"  Loaded vulnerability dataset: {len(vuln):,} counties")

    # Download and clean POS
    raw_pos = download_pos(POS_CACHE)
    print(f"  Raw POS rows: {len(raw_pos):,} | columns: {len(raw_pos.columns)}")
    pos = clean_pos(raw_pos)
    print(f"  After filtering to active Medicare facilities: {len(pos):,} rows")

    # Aggregate to county
    county_pos = aggregate_to_county(pos)
    print(f"  Aggregated to {len(county_pos):,} counties with facility data")

    # Join
    merged = vuln.merge(county_pos, on="BENE_GEO_CD", how="left")
    # Counties with no matched POS data get 0 facilities (not NaN)
    facility_cols = [c for c in merged.columns if c.startswith("n_") or
                     c in ["total_certified_beds", "total_icu_beds"]]
    merged[facility_cols] = merged[facility_cols].fillna(0)
    print(f"  Merged dataset: {len(merged):,} counties")

    # Derived metrics
    merged = add_derived_metrics(merged)

    # Save
    merged.to_csv(OUT_PATH, index=False)
    print(f"\n  Saved → {OUT_PATH}")

    # Quick summary
    print("\n── Summary of new facility variables ──────────────────────────────")
    summary_cols = [
        "total_certified_beds", "total_icu_beds",
        "n_inpatient_rehab_facility", "n_short_term_hospital",
        "n_skilled_nursing_facility", "n_home_health_agency",
        "n_critical_access_hospital",
        "beds_per_1k_power_dep", "has_inpatient_rehab",
    ]
    print(merged[summary_cols].describe().round(1).to_string())

    no_irf = (merged["n_inpatient_rehab_facility"] == 0).sum()
    print(f"\n  Counties with ZERO inpatient rehab facilities: {no_irf:,} "
          f"({no_irf/len(merged)*100:.1f}%)")

    return merged


if __name__ == "__main__":
    main()
