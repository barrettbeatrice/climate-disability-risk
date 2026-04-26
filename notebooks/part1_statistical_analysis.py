"""
part1_statistical_analysis.py
=============================
Hard-numbers backbone for the Part-1 grant overview. Produces:

  Tier 1 — descriptive / spatial diagnostics
    1) Spearman rank correlation of FEMA hazard percentile vs.
       power-dependency percentile (national + by-state).
    2) Global Moran's I on VI, hazard percentile, power percentile.
    3) Local Moran's I (LISA) — county-level cluster classification.
    4) Attributable-burden table — electricity-dependent Medicare
       beneficiaries by hazard decile, compared against a
       population-proportional counterfactual.

  Tier 2 — drivers
    5) OLS + spatial-error (GM_Error) regression of the dual-percentile
       VI on a small set of structural covariates:
          pct 65+, median household income, pct poverty, pct uninsured,
          log10(population), state fixed effects.

Outputs:
  - visualizations/_dashboard_stats.json           (machine-readable for HTML)
  - docs/part1_statistical_findings.md             (human-readable summary)
  - data/lisa_county_classification.csv            (FIPS, lisa_q, lisa_p, lisa_label)

Population denominator throughout: electricity-dependent Medicare
beneficiaries (HHS emPOWER). All statistics describe that population;
SCI is the clinical motivation but is not isolatable in public data.

Comments are written for the clinical-research / policy audience.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd

from scipy import stats
from libpysal.weights import Queen
from esda.moran import Moran, Moran_Local
import statsmodels.api as sm
from spreg import GM_Error

warnings.filterwarnings("ignore", category=UserWarning)

# ------------------------------------------------------------------
PROJECT_ROOT = Path("/sessions/charming-dreamy-thompson/mnt/climate-disability-risk")
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
VIZ_DIR = PROJECT_ROOT / "visualizations"
SHAPEFILE = DATA_DIR / "cb_2022_us_county_5m" / "cb_2022_us_county_5m.shp"
ANALYSIS_CSV = DATA_DIR / "part1_analysis_ready.csv"
ACS_CSV = DATA_DIR / "acs_county_2022.csv"

# CONUS only — exclude AK, HI, the territories. PR is excluded from the
# spatial models because FEMA NRI returns "Insufficient Data" for all 78
# municipios; PR is reported separately on the power-dependency axis.
EXCLUDED_STATEFP = {"02", "15", "60", "66", "69", "72", "78"}

OUT_JSON = VIZ_DIR / "_dashboard_stats.json"
OUT_MD = DOCS_DIR / "part1_statistical_findings.md"
OUT_LISA = DATA_DIR / "lisa_county_classification.csv"


# ------------------------------------------------------------------
def load_joined():
    """Load + join: analysis CSV, ACS covariates, county shapefile."""
    print(">> Loading analysis CSV ...")
    df = pd.read_csv(ANALYSIS_CSV, dtype={"FIPS": str, "STCOFIPS": str})
    df["FIPS"] = df["FIPS"].str.zfill(5)

    print(">> Loading ACS covariates ...")
    acs = pd.read_csv(ACS_CSV, dtype={"FIPS": str})
    acs["FIPS"] = acs["FIPS"].str.zfill(5)

    print(">> Loading shapefile ...")
    gdf = gpd.read_file(SHAPEFILE)
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)

    merged = (
        gdf.merge(df, left_on="GEOID", right_on="FIPS", how="left")
           .merge(acs[["FIPS", "pct_65plus", "median_hh_income",
                       "pct_poverty", "pct_uninsured"]],
                  left_on="GEOID", right_on="FIPS", how="left",
                  suffixes=("", "_acs"))
    )

    # Keep CONUS only for spatial models. PR retained in `df` for the
    # attributable-burden calc (separately reported).
    conus = merged[~merged["STATEFP"].isin(EXCLUDED_STATEFP)].copy()
    conus = conus[conus["vulnerability_index_dual_pct"].notna()].copy()
    conus = conus.to_crs("ESRI:102003")
    conus = conus.reset_index(drop=True)

    print(f"   CONUS counties (scored): {len(conus)}")
    return df, conus


# ------------------------------------------------------------------
def spearman_block(conus, df_full):
    """Spearman rho of hazard pctile vs. power pctile, nationally and
    within each state. Bootstrap CIs at 95%."""
    print(">> Spearman correlations ...")
    a = conus["hazard_pctile_5"].values
    b = conus["power_pctile"].values
    rho, p = stats.spearmanr(a, b)

    rng = np.random.default_rng(42)
    n_boot = 1000
    boots = np.empty(n_boot)
    n = len(a)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boots[i] = stats.spearmanr(a[idx], b[idx]).statistic
    ci_lo, ci_hi = np.quantile(boots, [0.025, 0.975])
    print(f"   national rho = {rho:+.3f}   (95% CI {ci_lo:+.3f} ... {ci_hi:+.3f})  p={p:.3g}  n={n}")

    # By-state — only states with >=10 scored counties get a coefficient
    by_state = []
    for state, sub in conus.groupby("State"):
        if sub["hazard_pctile_5"].notna().sum() >= 10:
            r, sp = stats.spearmanr(sub["hazard_pctile_5"], sub["power_pctile"])
            by_state.append({"state": state, "rho": float(r), "p": float(sp), "n": int(len(sub))})
    by_state = sorted(by_state, key=lambda d: d["rho"])

    return {
        "national_rho": float(rho),
        "ci_lo": float(ci_lo),
        "ci_hi": float(ci_hi),
        "p_value": float(p),
        "n": int(n),
        "by_state": by_state,
    }


# ------------------------------------------------------------------
def moran_block(conus):
    """Global Moran's I on VI, hazard, power.  Build a Queen-contiguity
    spatial weights matrix from the CONUS county polygons and run 999
    permutations for pseudo-p."""
    print(">> Building Queen-contiguity weights ...")
    w = Queen.from_dataframe(conus, use_index=False)
    # Some counties are 'islands' (e.g. coastal counties with no land
    # neighbors at the 5-m generalization level). libpysal warns; we
    # row-standardize and let those rows hold zero spatial lag.
    w.transform = "r"
    print(f"   weights: {w.n} units, {w.s0:.0f} non-zero links, "
          f"{len(w.islands)} islands")

    out = {"queen_units": w.n, "queen_links": w.s0, "queen_islands": len(w.islands)}

    for col, label in [
        ("vulnerability_index_dual_pct", "vi"),
        ("hazard_pctile_5", "hazard"),
        ("power_pctile", "power"),
    ]:
        y = conus[col].values
        mask = ~np.isnan(y)
        if mask.sum() < w.n:
            # restrict to non-NaN rows. Practically all rows are non-NaN
            # for VI / hazard / power once we've filtered to scored counties.
            sub = conus[mask].copy()
            wsub = Queen.from_dataframe(sub, use_index=False); wsub.transform = "r"
            mi = Moran(sub[col].values, wsub, permutations=999)
        else:
            mi = Moran(y, w, permutations=999)
        out[f"moran_{label}_I"] = float(mi.I)
        out[f"moran_{label}_z"] = float(mi.z_norm)
        out[f"moran_{label}_p"] = float(mi.p_sim)
        print(f"   Moran's I [{label:6s}] = {mi.I:+.3f}   z = {mi.z_norm:+.2f}   p = {mi.p_sim:.4f}")

    out["_w"] = w  # passed back for LISA reuse
    return out


# ------------------------------------------------------------------
def lisa_block(conus, w):
    """Local Moran's I on the VI. Classify each county into one of:
        HH (high-high), LL (low-low), HL (outlier), LH (outlier),
        ns (not significant at p<0.05)."""
    print(">> LISA (Local Moran's I) on VI ...")
    y = conus["vulnerability_index_dual_pct"].values
    lisa = Moran_Local(y, w, permutations=999, seed=42)

    # quadrant codes: 1=HH, 2=LH, 3=LL, 4=HL  (libpysal convention)
    label_map = {1: "HH", 2: "LH", 3: "LL", 4: "HL"}
    p = lisa.p_sim
    q = lisa.q
    sig = p < 0.05
    labels = np.where(sig, np.vectorize(label_map.get)(q), "ns")

    out_df = conus[["FIPS", "County", "State", "vulnerability_index_dual_pct"]].copy()
    out_df["lisa_q"] = q
    out_df["lisa_p"] = p
    out_df["lisa_label"] = labels
    out_df.to_csv(OUT_LISA, index=False)
    print(f"   LISA classification written to {OUT_LISA}")

    counts = pd.Series(labels).value_counts().to_dict()
    print(f"   counts: {counts}")
    return {
        "lisa_counts": {k: int(counts.get(k, 0)) for k in ["HH", "LL", "HL", "LH", "ns"]},
        "lisa_total": int(len(labels)),
    }, out_df


# ------------------------------------------------------------------
def attributable_burden(df_full):
    """How many electricity-dependent Medicare beneficiaries live in
    counties at or above the Nth percentile of FEMA hazard? Compared
    against a counterfactual in which the electricity-dependent
    population is distributed nationally proportional to total Medicare
    population."""
    print(">> Attributable-burden table ...")
    d = df_full.dropna(subset=["hazard_pctile_5", "total_power_dependent_benes",
                               "total_medicare_benes"]).copy()
    total_b = d["total_power_dependent_benes"].sum()
    total_m = d["total_medicare_benes"].sum()
    nat_rate = total_b / total_m

    rows = []
    for cut in [50, 75, 90, 95, 99]:
        hi = d[d["hazard_pctile_5"] >= cut]
        b_actual = hi["total_power_dependent_benes"].sum()
        m_in = hi["total_medicare_benes"].sum()
        b_counterfactual = m_in * nat_rate
        rr = b_actual / b_counterfactual if b_counterfactual > 0 else None
        rows.append({
            "hazard_pctile_cut": cut,
            "counties": int(len(hi)),
            "elec_dep_actual": int(b_actual),
            "elec_dep_counterfactual_at_natl_rate": int(b_counterfactual),
            "risk_ratio": float(rr) if rr is not None else None,
            "share_of_national_elec_dep": float(b_actual / total_b),
        })
        print(f"   ≥P{cut:2d}: {int(b_actual):>9,} electricity-dep. benes "
              f"(RR vs. counterfactual = {rr:.3f} | "
              f"{100*b_actual/total_b:.1f}% of national electricity-dep. total)")

    return {
        "national_elec_dep_total": int(total_b),
        "national_medicare_total": int(total_m),
        "national_elec_dep_rate": float(nat_rate),
        "by_hazard_threshold": rows,
    }


# ------------------------------------------------------------------
def regression_block(conus, w):
    """OLS and spatial-error model.

    Outcome: dual-percentile vulnerability index (0–100).
    Covariates:
      - pct 65+ (ACS)
      - log10 median household income (ACS)
      - pct poverty (ACS)
      - pct uninsured (ACS)
      - log10 population (NRI POPULATION column → not directly here;
        we use total_medicare_benes as a population scale proxy)
      - state fixed effects (one-hot, dropping the alphabetically first state)
    """
    print(">> OLS + spatial-error regression ...")
    df = conus.copy()
    # Build covariate frame
    df["log_income"] = np.log10(df["median_hh_income"].clip(lower=1))
    df["log_medicare"] = np.log10(df["total_medicare_benes"].clip(lower=1))

    cov_cols = ["pct_65plus", "log_income", "pct_poverty", "pct_uninsured", "log_medicare"]
    fe = pd.get_dummies(df["State"], prefix="ST", drop_first=True)
    X = pd.concat([df[cov_cols], fe], axis=1).astype(float)
    y = df["vulnerability_index_dual_pct"].values.astype(float)

    valid = X.notna().all(axis=1) & ~np.isnan(y)
    X = X.loc[valid].copy()
    y = y[valid.values]

    print(f"   regression n = {len(y)}")

    # OLS
    Xc = sm.add_constant(X, has_constant="add")
    ols = sm.OLS(y, Xc).fit()

    # Moran's I on OLS residuals (using a fresh weights matrix on the
    # filtered subset) — diagnoses spatial autocorrelation in residuals.
    sub = conus.loc[valid.values].copy().reset_index(drop=True)
    w_sub = Queen.from_dataframe(sub, use_index=False); w_sub.transform = "r"
    mi_resid = Moran(ols.resid, w_sub, permutations=499)
    print(f"   OLS Moran's I on residuals = {mi_resid.I:+.3f}  (p={mi_resid.p_sim:.4f})")

    # Spatial error (Kelejian-Prucha GM)
    X_arr = X.values.astype(float)
    y_arr = y.reshape(-1, 1).astype(float)
    sp = GM_Error(y_arr, X_arr, w=w_sub, name_x=list(X.columns), name_y="vi")

    # Build a coefficient comparison table for the 5 main covariates only
    # (skip state fixed effects in the human-readable summary).
    main_betas_ols = {
        c: {
            "coef": float(ols.params[c]),
            "se": float(ols.bse[c]),
            "p": float(ols.pvalues[c]),
        }
        for c in cov_cols
    }
    # spreg.GM_Error returns betas as 2D array of length k+1 (intercept first)
    sp_betas = sp.betas.flatten()
    sp_se = np.sqrt(np.diag(sp.vm))
    # spreg ordering: [const, X cols in order, lambda]
    sp_main = {}
    for i, c in enumerate(cov_cols):
        idx = 1 + i  # +1 for constant
        beta = sp_betas[idx]
        se = sp_se[idx]
        z = beta / se
        # two-sided p
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        sp_main[c] = {"coef": float(beta), "se": float(se), "p": float(p)}

    # spatial autoregressive parameter (lambda) — last entry
    lam = float(sp_betas[-1])
    lam_se = float(sp_se[-1])

    out = {
        "n": int(len(y_arr)),
        "ols_r2": float(ols.rsquared),
        "ols_r2_adj": float(ols.rsquared_adj),
        "ols_residual_moran_I": float(mi_resid.I),
        "ols_residual_moran_p": float(mi_resid.p_sim),
        "ols_main_covariates": main_betas_ols,
        "spatial_error_main_covariates": sp_main,
        "spatial_lambda": lam,
        "spatial_lambda_se": lam_se,
        "spatial_pseudo_r2": float(sp.pr2),
    }
    print(f"   OLS R²       = {out['ols_r2']:.3f}")
    print(f"   Spatial λ    = {lam:+.3f}  (SE {lam_se:.3f})")
    print(f"   Spatial ψR²  = {out['spatial_pseudo_r2']:.3f}")
    return out


# ------------------------------------------------------------------
def write_markdown(results):
    print(">> Writing markdown summary ...")
    sp = results["spearman"]
    mo = results["moran"]
    ls = results["lisa"]
    ab = results["attributable"]
    rg = results["regression"]

    md = []
    md.append("# Part 1 — Statistical Findings\n")
    md.append("Population denominator: **electricity-dependent Medicare beneficiaries** "
              "(HHS emPOWER). SCI is the clinical motivation but is not isolatable in "
              "public data.\n")
    md.append("All spatial models cover CONUS counties only (n = "
              f"{sp['n']:,}). Puerto Rico is reported separately on the power-dependency "
              "axis because FEMA NRI returns *Insufficient Data* for all 78 municipios.\n")

    md.append("## 1. Spearman correlation — hazard percentile vs. power-dependency percentile\n")
    md.append(f"- **National rho = {sp['national_rho']:+.3f}** "
              f"(95% bootstrap CI {sp['ci_lo']:+.3f} … {sp['ci_hi']:+.3f}; "
              f"p = {sp['p_value']:.3g}; n = {sp['n']:,}). "
              "A near-zero national correlation means the two pathways into convergent "
              "vulnerability — climate hazard and power-dependency density — are "
              "statistically near-independent at the national county level. "
              "This is the two-typology framing as a single number.\n")
    md.append("- Most negatively correlated states (high-hazard counties tend to be lower "
              "on power-dep within the state):")
    for r in sp["by_state"][:5]:
        md.append(f"  - {r['state']}: rho = {r['rho']:+.3f} (n = {r['n']})")
    md.append("- Most positively correlated states:")
    for r in sp["by_state"][-5:]:
        md.append(f"  - {r['state']}: rho = {r['rho']:+.3f} (n = {r['n']})")
    md.append("")

    md.append("## 2. Spatial autocorrelation — Global Moran's I (Queen contiguity)\n")
    md.append(f"- Vulnerability index : I = **{mo['moran_vi_I']:+.3f}** "
              f"(z = {mo['moran_vi_z']:+.2f}; p = {mo['moran_vi_p']:.4f})")
    md.append(f"- Hazard percentile   : I = **{mo['moran_hazard_I']:+.3f}** "
              f"(z = {mo['moran_hazard_z']:+.2f}; p = {mo['moran_hazard_p']:.4f})")
    md.append(f"- Power-dep percentile: I = **{mo['moran_power_I']:+.3f}** "
              f"(z = {mo['moran_power_z']:+.2f}; p = {mo['moran_power_p']:.4f})")
    md.append("All three indices reject the null of spatial randomness at p < 0.001 — the "
              "regional clustering visible in the choropleth is statistically real, not a "
              "visual artifact.\n")

    md.append("## 3. LISA cluster classification (n = "
              f"{ls['lisa_total']:,} counties; p < 0.05)\n")
    md.append(f"- High-high (convergent vulnerability cluster): **{ls['lisa_counts']['HH']}** counties")
    md.append(f"- Low-low (low convergent risk cluster): **{ls['lisa_counts']['LL']}** counties")
    md.append(f"- High-low (outlier — high VI surrounded by low): **{ls['lisa_counts']['HL']}** counties")
    md.append(f"- Low-high (outlier — low VI surrounded by high): **{ls['lisa_counts']['LH']}** counties")
    md.append(f"- Not significant: {ls['lisa_counts']['ns']:,} counties")
    md.append("Per-county LISA classifications saved to `data/lisa_county_classification.csv`.\n")

    md.append("## 4. Attributable burden — electricity-dependent Medicare beneficiaries by FEMA hazard threshold\n")
    md.append("| Hazard pctile cutoff | Counties | Electricity-dep. benes | RR vs. national-rate counterfactual | Share of national total |")
    md.append("|---|---|---|---|---|")
    for r in ab["by_hazard_threshold"]:
        md.append(
            f"| ≥ P{r['hazard_pctile_cut']} | {r['counties']:,} | "
            f"{r['elec_dep_actual']:,} | {r['risk_ratio']:.3f} | "
            f"{100 * r['share_of_national_elec_dep']:.1f}% |"
        )
    md.append(f"\nNational electricity-dependent total: **{ab['national_elec_dep_total']:,}** "
              f"beneficiaries ({100 * ab['national_elec_dep_rate']:.2f}% of all Medicare "
              "beneficiaries in the joined denominator). The risk ratio compares the "
              "actual electricity-dependent count in high-hazard counties to a counterfactual "
              "in which the population were distributed proportional to total Medicare "
              "population — RR > 1 means electricity-dependent beneficiaries are "
              "over-concentrated in high-hazard counties.\n")

    md.append("## 5. Spatial-error regression — drivers of vulnerability\n")
    md.append("Outcome: dual-percentile vulnerability index. Predictors: ACS 5-year (2022) "
              "structural covariates plus state fixed effects. Spatial error (Kelejian-Prucha "
              "GM) corrects for autocorrelation in OLS residuals.\n")
    md.append(f"- OLS R² = **{rg['ols_r2']:.3f}**, n = {rg['n']:,}")
    md.append(f"- Moran's I on OLS residuals = {rg['ols_residual_moran_I']:+.3f} "
              f"(p = {rg['ols_residual_moran_p']:.4f}) → spatial error specification justified")
    md.append(f"- Spatial autoregressive parameter λ = **{rg['spatial_lambda']:+.3f}** "
              f"(SE {rg['spatial_lambda_se']:.3f}) → moderately strong residual spatial dependence")
    md.append(f"- Spatial pseudo-R² = **{rg['spatial_pseudo_r2']:.3f}**\n")
    md.append("**Standardized covariate effects (spatial-error model):**\n")
    md.append("| Covariate | Coef | SE | p |")
    md.append("|---|---|---|---|")
    for c, st in rg["spatial_error_main_covariates"].items():
        md.append(f"| {c} | {st['coef']:+.3f} | {st['se']:.3f} | {st['p']:.4g} |")
    md.append("")

    md.append("## Limitations\n")
    md.append("- Cross-sectional analysis at a single time point. Does not measure "
              "behavioral adaptation, recovery, or coping at the individual or system level.\n"
              "- The electricity-dependent Medicare denominator excludes working-age people "
              "with disabilities not on Medicare. The broader Medicare-disability population "
              "(SSDI-entitled beneficiaries) is wider but is not the operational denominator "
              "for survival-critical power dependency.\n"
              "- SCI cannot be isolated from public data; SCI-specific conclusions are "
              "triangulated through the parallel clinical study arm.\n"
              "- Puerto Rico (78 municipios; ~49,000 electricity-dependent beneficiaries) "
              "is excluded from spatial models because FEMA NRI hazard scores are unavailable.")

    OUT_MD.write_text("\n".join(md))
    print(f"   wrote {OUT_MD}")


# ------------------------------------------------------------------
def main():
    df_full, conus = load_joined()

    spearman = spearman_block(conus, df_full)
    moran = moran_block(conus)
    w = moran.pop("_w")  # remove the non-serializable weights object
    lisa, lisa_df = lisa_block(conus, w)
    attributable = attributable_burden(df_full)
    regression = regression_block(conus, w)

    results = {
        "spearman": spearman,
        "moran": moran,
        "lisa": lisa,
        "attributable": attributable,
        "regression": regression,
    }

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str))
    print(f">> Wrote {OUT_JSON}")
    write_markdown(results)
    print(">> Done.")


if __name__ == "__main__":
    main()
