# Part 1 — Statistical Findings

Population denominator: **electricity-dependent Medicare beneficiaries** (HHS emPOWER). SCI is the clinical motivation but is not isolatable in public data.

All spatial models cover CONUS counties only (n = 3,099). Puerto Rico is reported separately on the power-dependency axis because FEMA NRI returns *Insufficient Data* for all 78 municipios.

## 1. Spearman correlation — hazard percentile vs. power-dependency percentile

- **National rho = -0.218** (95% bootstrap CI -0.250 … -0.181; p = 1.08e-34; n = 3,099). A near-zero national correlation means the two pathways into convergent vulnerability — climate hazard and power-dependency density — are statistically near-independent at the national county level. This is the two-typology framing as a single number.

- Most negatively correlated states (high-hazard counties tend to be lower on power-dep within the state):
  - NH: rho = -0.770 (n = 10)
  - AZ: rho = -0.729 (n = 15)
  - NY: rho = -0.715 (n = 62)
  - FL: rho = -0.667 (n = 67)
  - PA: rho = -0.604 (n = 67)
- Most positively correlated states:
  - MA: rho = +0.011 (n = 14)
  - OR: rho = +0.099 (n = 36)
  - OH: rho = +0.152 (n = 88)
  - KY: rho = +0.187 (n = 120)
  - NJ: rho = +0.548 (n = 21)

## 2. Spatial autocorrelation — Global Moran's I (Queen contiguity)

- Vulnerability index : I = **+0.707** (z = +65.53; p = 0.0010)
- Hazard percentile   : I = **+0.670** (z = +62.05; p = 0.0010)
- Power-dep percentile: I = **+0.748** (z = +69.32; p = 0.0010)
All three indices reject the null of spatial randomness at p < 0.001 — the regional clustering visible in the choropleth is statistically real, not a visual artifact.

## 3. LISA cluster classification (n = 3,099 counties; p < 0.05)

- High-high (convergent vulnerability cluster): **676** counties
- Low-low (low convergent risk cluster): **578** counties
- High-low (outlier — high VI surrounded by low): **16** counties
- Low-high (outlier — low VI surrounded by high): **27** counties
- Not significant: 1,802 counties
Per-county LISA classifications saved to `data/lisa_county_classification.csv`.

## 4. Attributable burden — electricity-dependent Medicare beneficiaries by FEMA hazard threshold

| Hazard pctile cutoff | Counties | Electricity-dep. benes | RR vs. national-rate counterfactual | Share of national total |
|---|---|---|---|---|
| ≥ P50 | 1,566 | 2,219,976 | 0.953 | 75.0% |
| ≥ P75 | 783 | 1,505,311 | 0.911 | 50.8% |
| ≥ P90 | 314 | 793,431 | 0.909 | 26.8% |
| ≥ P95 | 157 | 503,131 | 0.864 | 17.0% |
| ≥ P99 | 32 | 148,276 | 0.828 | 5.0% |

National electricity-dependent total: **2,960,586** beneficiaries (4.40% of all Medicare beneficiaries in the joined denominator). The risk ratio compares the actual electricity-dependent count in high-hazard counties to a counterfactual in which the population were distributed proportional to total Medicare population — RR > 1 means electricity-dependent beneficiaries are over-concentrated in high-hazard counties.

## 5. Spatial-error regression — drivers of vulnerability

Outcome: dual-percentile vulnerability index. Predictors: ACS 5-year (2022) structural covariates plus state fixed effects. Spatial error (Kelejian-Prucha GM) corrects for autocorrelation in OLS residuals.

- OLS R² = **0.581**, n = 3,098
- Moran's I on OLS residuals = +0.366 (p = 0.0020) → spatial error specification justified
- Spatial autoregressive parameter λ = **+0.604** (SE 4.056) → moderately strong residual spatial dependence
- Spatial pseudo-R² = **0.548**

**Standardized covariate effects (spatial-error model):**

| Covariate | Coef | SE | p |
|---|---|---|---|
| pct_65plus | -0.075 | 0.049 | 0.1295 |
| log_income | -33.001 | 3.406 | 0 |
| pct_poverty | +0.050 | 0.064 | 0.4326 |
| pct_uninsured | +0.220 | 0.059 | 0.0001742 |
| log_medicare | +7.244 | 0.437 | 0 |

## Limitations

- Cross-sectional analysis at a single time point. Does not measure behavioral adaptation, recovery, or coping at the individual or system level.
- The electricity-dependent Medicare denominator excludes working-age people with disabilities not on Medicare. The broader Medicare-disability population (SSDI-entitled beneficiaries) is wider but is not the operational denominator for survival-critical power dependency.
- SCI cannot be isolated from public data; SCI-specific conclusions are triangulated through the parallel clinical study arm.
- Puerto Rico (78 municipios; ~49,000 electricity-dependent beneficiaries) is excluded from spatial models because FEMA NRI hazard scores are unavailable.