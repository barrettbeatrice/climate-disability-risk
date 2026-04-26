"""
fetch_acs_covariates.py
=======================
Pull a small, targeted ACS 5-year (2022) county-level table for the four
structural covariates used in the Part-1 spatial regression:

  - Pct of population age 65+        DP05_0024PE
  - Median household income (USD)    DP03_0062E
  - Pct families below poverty       DP03_0119PE
  - Pct without health insurance     DP03_0099PE

Output: data/acs_county_2022.csv  (FIPS, pct_65plus, median_hh_income,
        pct_poverty, pct_uninsured)

Includes Puerto Rico (state 72) in a separate call against the Puerto
Rico Community Survey (PRCS) endpoint, which uses the same DP variable
names. PR is reported here for completeness but is excluded from the
CONUS regression because FEMA NRI hazard scores are missing.
"""

import json
import urllib.request
from pathlib import Path

import pandas as pd

DATA_DIR = Path("/sessions/charming-dreamy-thompson/mnt/climate-disability-risk/data")
OUT = DATA_DIR / "acs_county_2022.csv"

VARS = ["DP05_0024PE", "DP03_0062E", "DP03_0119PE", "DP03_0099PE"]
COL_MAP = {
    "DP05_0024PE": "pct_65plus",
    "DP03_0062E": "median_hh_income",
    "DP03_0119PE": "pct_poverty",
    "DP03_0099PE": "pct_uninsured",
}

US_URL = (
    "https://api.census.gov/data/2022/acs/acs5/profile?"
    f"get=NAME,{','.join(VARS)}&for=county:*&in=state:*"
)
PR_URL = (
    "https://api.census.gov/data/2022/acs/acs5/profile?"
    f"get=NAME,{','.join(VARS)}&for=county:*&in=state:72"
)


def fetch(url):
    req = urllib.request.urlopen(url, timeout=30)
    raw = req.read()
    arr = json.loads(raw)
    df = pd.DataFrame(arr[1:], columns=arr[0])
    return df


def main():
    print(">> Pulling ACS 5-year 2022 (US counties) ...")
    us = fetch(US_URL)
    print(f"   rows: {len(us)}")

    # PR is included in the US endpoint via state 72 already. No second call needed.
    df = us.copy()
    df["FIPS"] = df["state"].astype(str).str.zfill(2) + df["county"].astype(str).str.zfill(3)

    # Cast numerics — ACS uses sentinel values like "-666666666" for "missing".
    for v in VARS:
        df[v] = pd.to_numeric(df[v], errors="coerce")
        df.loc[df[v] < -100, v] = pd.NA

    df = df.rename(columns=COL_MAP)
    keep = ["FIPS", "NAME"] + list(COL_MAP.values())
    df = df[keep].copy()

    print(">> Sample:")
    print(df.head().to_string(index=False))

    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"\n>> Wrote {OUT}  rows={len(df)}  ({OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
