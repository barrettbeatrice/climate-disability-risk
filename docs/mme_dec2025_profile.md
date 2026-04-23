# Medicare Monthly Enrollment (MME) — December 2025 Profile

**Source:** CMS Medicare Monthly Enrollment Data, December 2025 release  
**File:** `Medicare Monthly Enrollment Data_December 2025.csv`  
**Profiled:** 2026-04-18  

---

## 1. File Summary

| Attribute | Value |
|-----------|-------|
| Total rows | 563,758 |
| Columns | 60 |
| Geography levels | National (169), State (9,802), County (553,787) |
| Year range | 2013–2025 (13 calendar years) |
| Month granularity | Monthly + annual ("Year") aggregation |
| County-level, Dec 2025 slice | **3,278 counties** |

This dataset provides 13 years of monthly enrollment counts stratified by geography (FIPS code), eligibility category (aged, disabled, ESRD), race/ethnicity, age group, dual-eligible status, and plan type (Original Medicare vs. Medicare Advantage, Part A/B/D). The December 2025 snapshot is the most recent available and will serve as the enrollment denominator for this grant.

---

## 2. Key Variables for Grant

### 2.1 Disability Enrollment

| Variable | Definition | Coverage (Dec 2025 county) |
|----------|-----------|---------------------------|
| `DSBLD_TOT_BENES` | Total disabled Medicare beneficiaries | 3,198 of 3,278 (80 suppressed) |
| `DSBLD_NO_ESRD_BENES` | Disabled without End-Stage Renal Disease | 2,170 of 3,278 (1,108 suppressed) |
| `DSBLD_ESRD_AND_ESRD_ONLY_BENES` | Disabled with ESRD + ESRD-only | 2,170 of 3,278 (1,108 suppressed) |

**Distribution of county-level disability rate** (`DSBLD_TOT_BENES / TOT_BENES`):

| Statistic | Value |
|-----------|-------|
| Mean | 11.68% |
| Median | 11.20% |
| Std Dev | 4.34% |
| IQR | 8.56% – 14.53% |
| Min | 0.00% |
| Max | 28.63% |
| Skewness | 0.56 |

The disability rate distribution is approximately normal with a mild right skew — substantially less skewed than the emPOWER power dependency rate (skewness 5.22–5.73 for home health/hospice). Percentile-rank rescaling remains appropriate for consistency but the impact of rescaling choice is smaller for this variable.

**Top counties by disability rate (≥500 beneficiaries):**

1. Martin County, KY — 28.63%
2. Buchanan County, VA — 28.28%
3. Dickenson County, VA — 27.45%
4. Clay County, KY — 27.44%
5. Floyd County, KY — 27.38%

The Appalachian coal counties (KY, VA, WV) dominate the disability-rate ranking, consistent with established literature on disability prevalence in Central Appalachia (historically high rates of occupational injury, black lung disease, and opioid-related disability).

### 2.2 Dual Eligibility (SES Proxy)

| Variable | Definition | Coverage |
|----------|-----------|---------|
| `DUAL_TOT_BENES` | Total dually eligible (Medicare + Medicaid) | 3,203 counties |
| `FULL_DUAL_TOT_BENES` | Full dual eligibles | 3,120 counties |
| `NODUAL_TOT_BENES` | Medicare-only (no Medicaid) | 3,203 counties |

Mean dual-eligibility rate: 16.01%, median 14.64%. Dual status is the strongest available proxy for low socioeconomic status in Medicare administrative data and should be included as a covariate in the regression model (§4.2).

### 2.3 Race/Ethnicity

| Variable | Numeric counties | Suppressed |
|----------|-----------------|-----------|
| `WHITE_TOT_BENES` | 3,209 | 69 |
| `BLACK_TOT_BENES` | 2,536 | 742 |
| `HSPNC_TOT_BENES` | 2,894 | 384 |
| `API_TOT_BENES` | 2,263 | 1,015 |
| `NATIND_TOT_BENES` | 1,663 | 1,615 |

Heavy cell suppression in minority-population columns, particularly for American Indian/Alaska Native (49% suppressed) and Asian/Pacific Islander (31% suppressed). This limits multivariate analysis in rural/low-population counties.

### 2.4 Plan Type

| Metric | Count | Share |
|--------|-------|-------|
| Original Medicare | 33,671,311 | 48.6% |
| Medicare Advantage | 35,614,209 | 51.4% |

Medicare Advantage has overtaken Original Medicare in enrollment as of December 2025. This is methodologically significant: MA plan data is not included in CMS fee-for-service utilization files. The emPOWER DME data captures both FFS and MA beneficiaries, while the Geographic Variation PUF and MUP DME files are FFS-only. This divergence should be noted in grant limitations.

---

## 3. FIPS Join Integrity

| Dataset pair | Intersection |
|-------------|-------------|
| MME ∩ emPOWER DME ∩ FEMA NRI | 2,906 counties |
| MME ∩ FEMA (not in DME) | 1 county |
| MME ∩ DME (not in FEMA) | 306 counties |
| MME only | 65 counties |
| Total MME counties | 3,278 |

The three-way join yields 2,906 counties. The 306 in MME+DME but missing from FEMA are primarily territories (PR, VI, GU) and some independent cities.

### Connecticut FIPS Reorganization

CMS has adopted the new Connecticut planning regions (FIPS 09110–09190) as of this release:

| New FIPS | Planning Region | Total Benes | Disabled |
|----------|----------------|-------------|----------|
| 09110 | Capitol | 208,439 | 19,446 |
| 09120 | Greater Bridgeport | 57,262 | 5,023 |
| 09130 | Lower CT River Valley | 46,211 | 3,082 |
| 09140 | Naugatuck Valley | 100,383 | 10,048 |
| 09150 | Northeastern CT | 23,054 | 2,621 |
| 09160 | Northwest Hills | 31,036 | 2,361 |
| 09170 | South Central CT | 122,797 | 11,774 |
| 09180 | Southeastern CT | 65,613 | 7,000 |
| 09190 | Western CT | 117,667 | 6,060 |

Plus one `09999 — Unknown` row (suppressed counts). The FEMA NRI still uses legacy 8-county FIPS codes (09001–09015). The `ct_fips_crosswalk.csv` maps between systems; population-weighted apportionment is recommended for the join.

---

## 4. Correlation with Existing Vulnerability Index

| Metric | Value |
|--------|-------|
| Pearson r (disability rate, power dependency rate) | 0.1944 |
| Spearman ρ | 0.2862 (p = 4.04 × 10⁻⁶¹) |

The weak-to-moderate correlation is expected and informative: **the MME disability rate and the emPOWER power dependency rate measure related but distinct constructs.** The disability rate captures all Medicare beneficiaries qualifying via disability (predominantly SSA-determined disability under age 65), while the power dependency rate captures the subset using electricity-dependent durable medical equipment (ventilators, O₂ concentrators, electric wheelchairs). The two variables together provide a richer vulnerability assessment than either alone.

### Convergent Risk Ranking (Disability Rate + Vulnerability Index)

Top 10 counties by combined percentile rank:

| Rank | County | State | Disability Rate (Pctile) | Vulnerability Index (Pctile) | Convergent Score |
|------|--------|-------|--------------------------|-----------------------------|-----------------| 
| 1 | Robeson County | NC | 19.9% (P96) | 44.8 (P98) | 97.0 |
| 2 | Sequoyah County | OK | 20.7% (P97) | 43.0 (P97) | 96.8 |
| 3 | Washington Parish | LA | 18.7% (P94) | 46.6 (P99) | 96.3 |
| 4 | Le Flore County | OK | 18.6% (P94) | 46.4 (P99) | 96.2 |
| 5 | Escambia County | AL | 18.9% (P94) | 42.3 (P96) | 95.2 |
| 6 | Rapides Parish | LA | 18.0% (P92) | 46.3 (P99) | 95.2 |
| 7 | Talladega County | AL | 21.9% (P98) | 39.3 (P91) | 94.8 |
| 8 | Crawford County | AR | 19.9% (P96) | 40.7 (P94) | 94.7 |
| 9 | Panola County | MS | 20.2% (P96) | 39.2 (P91) | 93.8 |
| 10 | Holmes County | MS | 21.6% (P98) | 37.8 (P88) | 93.0 |

This ranking shifts the geographic focus toward the Gulf Coast / Deep South — consistent with hurricane, heat wave, and flood exposure overlapping with high disability prevalence. Notably absent: the San Joaquin Valley (CA) counties that topped the power-dependency-only ranking; California's low overall disability rate (7.05%, second-lowest state) suppresses those counties in the combined metric.

---

## 5. State-Level Disability Rates

**Top 5 states:** Arkansas (16.18%), Kentucky (15.68%), Mississippi (15.63%), Alabama (15.51%), Puerto Rico (15.25%)

**Bottom 5 states:** US Virgin Islands (5.64%), Hawaii (5.79%), California (7.05%), Colorado (7.06%), Arizona (8.10%)

---

## 6. Suppression and Data Quality

All cell suppression uses the CMS standard `*` marker (counts < 11 beneficiaries). Suppression rates by variable class:

| Variable class | Typical suppression rate | Impact |
|---------------|------------------------|--------|
| Total enrollment | 54/3,278 (1.6%) | Minimal |
| Disabled totals | 80/3,278 (2.4%) | Low |
| ESRD subcategories | 1,108/3,278 (33.8%) | Moderate — limits ESRD-specific analysis |
| Race/ethnicity | 69–1,615 (2.1%–49.3%) | High for minority groups |
| Under-25 age group | 1,513/3,278 (46.1%) | Expected — few pediatric Medicare benes |

---

## 7. Methodology Implications

1. **New variable for vulnerability index:** `DSBLD_TOT_BENES` should be added as a 14th variable-specific vulnerability index (§3.1), computed as `dsbld_rate = DSBLD_TOT_BENES / TOT_BENES`, percentile-rank rescaled to 0–100.

2. **Dual eligibility as regression covariate:** `dual_rate` replaces or supplements the poverty/low-income covariate in §4.2 that was previously unavailable without the Geographic Variation PUF. This is computable NOW from existing data.

3. **MA enrollment share as covariate:** The `ma_share` variable (51.4% nationally) captures variation in care delivery model that may confound DME utilization patterns.

4. **Denominators are now available:** Total enrollment by county enables proper rate computation for any CMS utilization file, not just the emPOWER-sourced denominators.

5. **Temporal analysis enabled:** With 13 years of monthly data, longitudinal analysis of disability enrollment trends is feasible.

---

## 8. Output Files

| File | Location | Description |
|------|----------|-------------|
| `mme_dec2025_county_clean.csv` | `/data/` | 3,278 rows × 31 columns, Dec 2025 county-level extract with derived rates |
| `mme_dec2025_profile.md` | `/docs/` | This profiling report |

---

*Generated 2026-04-18. Source: CMS Medicare Monthly Enrollment Data, December 2025.*
