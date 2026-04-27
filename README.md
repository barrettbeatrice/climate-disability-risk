# Climate Change Impacts on Electricity-Dependent Medicare Populations
## County-Level Geospatial Analysis of Electricity-Dependent Disability and Climate Hazard Convergence
### Alexander Lab | Marcus Neuroscience Institute | Baptist Health South Florida

> **Scope and framing.** The clinical grant supported by this work focuses on persons with spinal cord injuries (SCI). This geospatial arm uses the best available public federal data, which identifies **electricity-dependent Medicare beneficiaries in aggregate** — a population that includes SCI, ALS, COPD, neuromuscular disease, and others who rely on powered durable medical equipment for daily function. SCI is the motivating clinical lens: it frames device selection, hazard prioritization, and policy interpretation throughout. SCI cannot be directly isolated from public CMS files; direct identification requires claims-level data obtained through a CMS Data Use Agreement (ResDAC), which is out of scope for this phase. Quantitative findings describe the electricity-dependent Medicare population as a whole; SCI-specific conclusions are drawn cautiously and explicitly triangulated with the clinical study arm.

---

## Project Deliverables — Single-Source Index

This README is the canonical written summary for the project. Everything else is derived from or feeds into the analysis it describes.

| Deliverable | Location | Purpose |
|---|---|---|
| Canonical README | `README.md` (this file) | Comprehensive single-source narrative |
| Grant overview & proposal | `docs/grant_overview_and_proposal.docx` | Word-format grant narrative |
| Policy brief (one-page) | `docs/policy_brief.html` | Two-column letter-size handout |
| Statistical findings | `docs/part1_statistical_findings.md` | Hard numbers (ρ, Moran's I, LISA, burden, regression) |
| Slide deck | `docs/slide_deck.html` | 11-slide self-contained presentation (open in browser; arrow keys) |
| Methodology pros/cons | `docs/analytical_part1b_methodology_pros_cons.md` | Internal methodology decision log |
| Notion analyst page | [34b56834683c81f6aab1e686691faa28](https://www.notion.so/34b56834683c81f6aab1e686691faa28) | Full analyst documentation |
| Notion portfolio page | [32356834683c81f59293e357eb733f47](https://www.notion.so/32356834683c81f59293e357eb733f47) | Visual portfolio entry |
| Bivariate choropleth | `visualizations/fig1_bivariate_choropleth.png` | Q1: where convergent risk concentrates |
| Top-10 split bars | `visualizations/fig2_top10_split_bars.png` | Q1: who's at the top |
| Scatter quadrants | `visualizations/fig3_scatter_quadrants.png` | Q1: two-typology framing |
| LISA cluster map | `visualizations/fig4_lisa_cluster_map.png` | Q1: statistical hotspots (676 HH counties) |
| Regression forest | `visualizations/fig5_regression_forest.png` | Q2: structural drivers (income dominates) |
| Interactive dashboard | `visualizations/grant_overview_dashboard_standalone.html` | KPI + layer-toggle d3 explorer |
| Analysis-ready dataset | `data/part1_analysis_ready.csv` | Joined county-level frame (3,212 rows × 41 cols) |
| LISA classification | `data/lisa_county_classification.csv` | Per-county LISA label (3,099 CONUS counties) |
| Spatial pipeline | `notebooks/part1_statistical_analysis.py` | Reproducible statistical pipeline |
| ACS covariate fetch | `notebooks/fetch_acs_covariates.py` | ACS 5-year (2022) county covariates |
| Dual-percentile recompute | `notebooks/recompute_vulnerability_dual_percentile.py` | Vulnerability index methodology |

---

## Background

Individuals with spinal cord injuries (SCI) face compounding physiological vulnerabilities during climate-related emergencies. Impaired thermoregulation renders them acutely susceptible to heat events; paralysis and spasticity limit the self-protective mobility that allows ambulatory populations to evacuate or shelter effectively. Critically, a significant subset of this population depends on electricity-powered equipment — volume ventilators, oxygen concentrators, CPAP/BiPAP devices, suction apparatus, and powered wheelchairs — for survival. Climate-driven power disruption is therefore not merely a convenience failure but a life-safety event.

These same vulnerabilities — powered-equipment dependency, narrow thermoregulatory window, evacuation constraints — are shared by other populations including those with ALS, advanced COPD, neuromuscular disease, and chronic respiratory failure. The CMS and HHS public data used here measures this broader electricity-dependent Medicare population in aggregate. SCI-specific physiology motivates the analytical choices (device categories examined, hazard thresholds, post-acute facility types), but the measured population is broader than SCI alone.

Existing disability classification systems — the Functional Independence Measure (FIM), ACS disability questions, and WHODAS 2.0 — were not designed to capture the dimensions most relevant to climate vulnerability: thermoregulatory capacity, equipment power dependency, and medical supply chain resilience (Alexander & Alexander, 2025). This geospatial analysis addresses that gap by mapping *where* convergent risk exists between climate hazard exposure and electricity-dependent disabled Medicare populations at the county level across the United States.

## Relationship to the Clinical Study Grant

This repository provides the geospatial complement to Dr. Marcalee Alexander's international, multicenter, mixed-methods clinical study "Climate Change Impacts on Persons with Spinal Cord Injuries." The clinical study enrolls participants at four sites selected to represent distinct climate exposure profiles:

| Site | Primary Climate Exposure | N (Quantitative) |
|------|--------------------------|-------------------|
| Canada | Extreme cold / winter storms | 100 |
| Greece | Extreme heat | 100 |
| Puerto Rico | Hurricanes / tropical cyclones | 100 |
| Florida (Baptist Health) | Heat + coastal flood convergence | 100 |

The clinical arm administers the Washington Group Extended Set (WG-ES), the Hogg Eco-Anxiety Scale, and the Climate Change Perceptual Awareness Scale to 400 participants (quantitative) plus 80 semi-structured qualitative interviews. This geospatial analysis identifies the US counties where electricity-dependent Medicare populations face the highest convergent climate risk, with device categories and hazard thresholds prioritized through an SCI clinical lens. Together, the two arms answer *who is affected at the individual level* (clinical study, SCI-specific) and *where aggregate convergent risk concentrates geographically* (this geospatial arm, electricity-dependent Medicare populations including SCI). The geospatial findings support the clinical study's site selection rationale and the broader policy argument for disability-inclusive emergency preparedness.

The theoretical framing draws from Chapter 4 of Alexander & Alexander (2025, Elsevier), which calls for "disruptive practices" — specifically GIS-based spatial analysis combined with individual-level tracking — to overcome the limitations of existing disability surveillance frameworks in the climate-health domain.

## Part 1: Convergent Vulnerability Mapping (Complete)

Part 1 is a static, cross-sectional geospatial analysis. Six Medicare variables measuring electricity-dependent population density are joined with FEMA National Risk Index hazard scores across 3,212 US counties (3,131 scored on the headline vulnerability index; 81 counties excluded due to insufficient FEMA hazard data; 5 counties suppressed under HIPAA cell-size rules). A dual-percentile rescaled vulnerability index identifies counties where high population dependence and high grid-disruptive climate hazard exposure co-occur. Part 1 answers *where* convergent climate-and-disability risk is structurally located. It does not measure behavioral adaptation, coping, or response — those constructs require event-time data and individual-level outcomes that public Medicare files cannot provide on their own, and are reserved for Phase 2 / international extension and Dr. Alexander's parallel clinical study arm.

**Medicare Variables (Part 1):**

| Variable | Source | Description |
|----------|--------|-------------|
| `power_dependency_rate` | HHS emPOWER | Electricity-dependent DME beneficiaries per 100 Medicare beneficiaries |
| `o2_services_rate` | HHS emPOWER | Oxygen services beneficiaries per 100 Medicare beneficiaries |
| `home_health_rate` | HHS emPOWER | Home health beneficiaries per 100 Medicare beneficiaries |
| `hospice_rate` | HHS emPOWER | Hospice beneficiaries per 100 Medicare beneficiaries |
| `any_healthcare_rate` | HHS emPOWER | Any electricity-dependent healthcare beneficiaries per 100 Medicare beneficiaries |
| `dsbld_rate` | MME Dec 2025 | Disabled (under-65) Medicare beneficiaries per 100 total beneficiaries |

**FEMA NRI Hazard Types:**

The headline vulnerability index uses the *5-hazard grid-disruptive composite*: Hurricane (HRCN), Heat Wave (HWAV), Wildfire (WFIR), Coastal Flood (CFLD), Drought (DRGT). These are the hazards most capable of disrupting the electrical grid and climate-controlled housing on which electricity-dependent Medicare populations depend.

The per-covariate diagnostic choropleths and correlation heatmap additionally include Cold Wave (CWAV), Inland Flood (IFLD), Winter Weather (WNTW), and Ice Storm (ISTM) — giving a 9-hazard view used only for secondary diagnostic analysis.

### Future work

Subsequent phases (international extension and the parallel clinical study arm) will address the behavioral and individual-level questions that Part 1's ecological design cannot answer. Those phases are out of scope for this README, which documents Part 1 only.

An earlier Part 2 design targeted HCPCS device-level isolation via the CMS MUP DME file. That approach was retired on April 18, 2026 after the by-geography release was confirmed state-level only and therefore incapable of supporting county-level device-specific analysis. The device categorization survives here as *clinical framing* — the SCI-motivated lens through which we interpret the broader electricity-dependent population's behavior. The HCPCS-level direct identification remains a future-work item pending claims-level data access.

**SCI-relevant device categories (interpretive framing, not direct measurement):**

| Device Category | HCPCS Codes | Clinical Relevance |
|----------------|-------------|-------------------|
| Powered wheelchairs | K0856–K0864 | Primary mobility for tetraplegia / high paraplegia |
| Ventilators | E0450–E0480 | Life-sustaining for C3–C5 injuries |
| CPAP / BiPAP | E0601, E0470 | Sleep-disordered breathing (prevalence up to 60% in tetraplegia) |
| Suction equipment | E0600 | Airway clearance for high-level SCI |
| Oxygen concentrators | E1390–E1392 | Respiratory comorbidity in chronic SCI |

## Methodology

### Rescaling

All Medicare rate variables are percentile-rank rescaled (0–100) rather than min–max normalized. Percentile ranking is robust to the extreme right-skew and outliers present in county-level healthcare utilization data. For a given variable, each county's rescaled value represents the percentage of counties with equal or lower raw rates.

### Composite Hazard Score

The headline composite hazard score is the mean of the five FEMA NRI RISK scores for grid-disruptive hazards: hurricane, heat wave, wildfire, coastal flood, and drought. Coastal flood is excluded from the composite for inland counties (those carrying no coastal exposure) rather than treated as zero, preventing artificial score suppression for high-risk inland jurisdictions.

### Vulnerability Index (dual-percentile)

The headline convergent-risk index is the equal-weighted mean of two national percentile ranks:

```
vulnerability_index = (hazard_percentile + power_dependency_percentile) / 2
```

where `hazard_percentile` is the national percentile rank of the county's composite 5-hazard score and `power_dependency_percentile` is the national percentile rank of the county's power-dependent DME rate. Both inputs are rescaled to 0–100 before averaging; this is necessary because the raw composite hazard score spans 0–100 while the raw power-dependency rate spans approximately 0–40% (median ≈ 5%), so averaging the raw values would under-weight power dependency by roughly 15-fold. Under the dual-percentile formulation, a county ranks highest only when both dimensions — climate hazard exposure and population dependence — are simultaneously elevated.

For each of the six Medicare variables individually, a diagnostic vulnerability choropleth is additionally rendered using the broader 9-hazard composite from part1 as a secondary lens; these maps are for covariate-by-covariate pattern inspection only and do not override the headline dual-percentile index.

### Regression Specification

```
V_rate ~ β₁(HRCN) + β₂(HWAV) + β₃(WFIR) + β₄(CFLD) + β₅(DRGT)
       + β₆(CWAV) + β₇(IFLD) + β₈(WNTW) + β₉(ISTM) + γ₁(dsbld_rate) + ε
```

The disability rate (`dsbld_rate`) from the Medicare Monthly Enrollment file serves as the sole covariate. Dual eligibility, race/ethnicity, and Medicare Advantage share were evaluated and excluded as out of scope for this phase of the analysis; each could be reintroduced in a follow-on equity-focused extension.

## Key Findings (Part 1)

**The Intermountain West / Four Corners corridor dominates the national convergent-risk ranking.** Under the dual-percentile methodology, San Juan, NM leads the nation (vulnerability index 96.9), followed by El Paso, CO (94.5), Bernalillo, NM (94.2), Sandoval, NM (94.1), and Adams, CO (93.8). All ten of the top-ranked counties sit in New Mexico, Colorado, or Utah — a corridor jointly exposed to drought, heat wave, and wildfire hazard at or above the 90th national percentile and carrying power-dependent Medicare populations in the top decile. This is the region where structural power-dependency and grid-disruptive climate hazard converge most sharply.

**Top 10 counties (dual-percentile convergent-risk index):**

| # | County | State | Hazard pctile | Power pctile | Vulnerability index |
|---|--------|-------|---------------|--------------|---------------------|
| 1 | San Juan | NM | 98.3 | 95.6 | 96.9 |
| 2 | El Paso | CO | 92.0 | 97.1 | 94.5 |
| 3 | Bernalillo | NM | 97.4 | 91.0 | 94.2 |
| 4 | Sandoval | NM | 97.2 | 91.1 | 94.1 |
| 5 | Adams | CO | 92.0 | 95.6 | 93.8 |
| 6 | Chaves | NM | 96.4 | 90.4 | 93.4 |
| 7 | Utah | UT | 98.4 | 88.2 | 93.3 |
| 8 | Mesa | CO | 92.6 | 93.3 | 92.9 |
| 9 | Santa Fe | NM | 95.7 | 89.7 | 92.7 |
| 10 | Weber | UT | 91.4 | 93.7 | 92.6 |

**A second, distinct risk profile emerges along the Southeast coast — directly within Baptist Health's primary service area.** Palm Beach (hazard percentile 99.8) and Miami-Dade (99.7) sit in the top 1% of US counties on the composite hazard score, driven by hurricane and coastal-flood exposure, making Baptist Health South Florida the highest-climate-hazard-exposed major hospital system in the Southeast. Their convergent-risk ranks (1,558 and 1,013 respectively) are held below the Intermountain West only because South Florida's Medicare power-dependency rate sits in the bottom tercile nationally — a profile of extreme climate exposure convergent with moderate device-dependency. The finding nonetheless places the grant-holder institution at the frontline of the hurricane/coastal-flood pathway.

**Power dependency operates as an independent vulnerability pathway.** Several counties in the top 25 — including Pueblo, CO (rank 12, hazard 86.7 / power 98.2), Iron, UT (rank 13, hazard 87.0 / power 97.5), Millard, UT (rank 14, hazard 86.9 / power 97.0), and Garfield, UT (rank 21, hazard 82.1 / power 98.9) — reach top-ranked positions on moderate hazard scores but extreme power-dependency rates near the national ceiling. This confirms that electricity-dependent disability cannot be treated as a secondary amplifier of climate exposure; in multiple US regions it is itself the dominant driver of disaster risk.

**Disability rate as a distinct construct.** Spearman correlation between `dsbld_rate` and `power_dependency_rate` is ρ = 0.286, confirming that the two variables capture meaningfully different populations. The disability rate variable produces 18 counties in its top-25 that do not appear in any other variable's top-25 — the most distinct of all six indices.

**Negative inland-flood correlations.** The Spearman correlation heatmap reveals negative correlations between most emPOWER variables and inland flood risk scores, suggesting that electricity-dependent populations are not concentrated in inland flood zones. This warrants further investigation in Part 2.

## Statistical Findings (Part 1)

These statistics formalize the visual patterns reported above. All headline numbers were independently re-derived from `data/part1_analysis_ready.csv` and `data/lisa_county_classification.csv` during a `/data:validate-data` review on April 27, 2026.

**Spearman ρ = −0.218** between hazard percentile and power-dependency percentile (95% bootstrap CI [−0.250, −0.181]; p = 1.08×10⁻³⁴; n = 3,099 CONUS counties). The two pathways into convergent risk — climate hazard density and power-dependency density — are statistically near-independent at the county level. The two-typology framing is recovered as a single coefficient.

**Global Moran's I (Queen contiguity, 999 permutations):** vulnerability index I = +0.707, hazard percentile I = +0.670, power-dependency percentile I = +0.748 — all p < 0.001. Regional clustering is statistically real, not a visual artifact.

**LISA cluster classification (p < 0.05, 999 conditional permutations):** **676 high-high counties** (the formal convergent-vulnerability bloc), 578 low-low counties, 16 high-VI outliers, 27 low-VI outliers, 1,802 not significant. Per-county labels in `data/lisa_county_classification.csv`.

**Attributable burden — electricity-dependent Medicare beneficiaries by FEMA hazard threshold:**

| Hazard pctile cutoff | Counties | Electricity-dep. benes | Share of national total |
|---|---|---|---|
| ≥ P50 | 1,566 | 2,219,976 | 75.0% |
| ≥ P75 | 783 | 1,505,311 | 50.8% |
| ≥ P90 | 314 | 793,431 | 26.8% |
| ≥ P95 | 157 | 503,131 | 17.0% |
| ≥ P99 | 32 | 148,276 | 5.0% |

National electricity-dependent total (joined denominator): **2,960,586** beneficiaries.

**Spatial-error regression** of dual-percentile vulnerability index on ACS 5-year (2022) covariates plus state fixed effects (n = 3,098, OLS R² = 0.581, spatial pseudo-R² = 0.548, λ = +0.604):

| Covariate | Standardized β | SE | p |
|---|---|---|---|
| log Median Income | **−33.001** | 3.406 | < 0.001 |
| log Medicare Population | +7.244 | 0.437 | < 0.001 |
| Pct Uninsured | +0.220 | 0.059 | < 0.001 |
| Pct 65+ | −0.075 | 0.049 | 0.130 |
| Pct Below Poverty | +0.050 | 0.064 | 0.433 |

Higher-income counties carry meaningfully lower convergent vulnerability conditional on FEMA hazard, regional context, and Medicare-population scale. Age 65+ share and poverty rate fall out of significance once income is controlled for. The forest-plot rendering is `visualizations/fig5_regression_forest.png`.

## Visualizations

All visualizations are in `visualizations/` at 300 DPI.

### Canonical Five-Figure Suite

| File | What it answers | Visual style |
|------|-----------------|---------------|
| `fig1_bivariate_choropleth.png` | **Q1: Where convergent risk concentrates** — national bivariate choropleth, Stevens.pinkblue palette, Puerto Rico inset on power-dependency axis only | Map |
| `fig2_top10_split_bars.png` | **Q1: Who's at the top** — Top-10 counties paired across hazard and power-dependency percentile axes | Bar chart |
| `fig3_scatter_quadrants.png` | **Q1: Two-typology framing** — hazard × power-dependency scatter with quadrant cuts at the 50th-percentile thresholds | Scatter |
| `fig4_lisa_cluster_map.png` | **Q1: Statistical hotspots** — LISA cluster map (HH/LL/HL/LH/ns); HH bloc = 676 counties | Map |
| `fig5_regression_forest.png` | **Q2: Structural drivers** — spatial-error regression coefficient forest plot (income dominates) | Forest plot |

### Interactive

| File | Description |
|------|-------------|
| `grant_overview_dashboard_standalone.html` | **Interactive d3 dashboard** — KPI cards, layer-toggle choropleth (vulnerability index / hazard / power-dependency / absolute count), Stevens.pinkblue bivariate palette, Puerto Rico inset, South Florida regional pin. Single-file standalone (open in browser, no server). |
| `docs/slide_deck.html` | **11-slide presentation deck** — self-contained HTML with arrow-key navigation, soft-teal accent on dark theme. Covers: gap → clinical hook → methodology → typologies → top-10 → statistical evidence → attributable burden → structural drivers → limitations → takeaway. |

### Diagnostic Choropleths (per-covariate, 9-hazard composite)

County-level maps of the contiguous United States:

| File | Description |
|------|-------------|
| `choropleth_vuln_power_dependency.png` | Vulnerability index — power dependency rate |
| `choropleth_vuln_o2_services.png` | Vulnerability index — oxygen services rate |
| `choropleth_vuln_home_health.png` | Vulnerability index — home health rate |
| `choropleth_vuln_hospice.png` | Vulnerability index — hospice rate |
| `choropleth_vuln_any_healthcare.png` | Vulnerability index — any healthcare rate |
| `choropleth_vuln_disability.png` | Vulnerability index — disability rate |
| `choropleth_composite_hazard.png` | Raw composite hazard score (no Medicare overlay) |
| `choropleth_dsbld_rate_raw.png` | Raw disability rate (no hazard overlay) |

### Analytical Figures (5)

| File | Description |
|------|-------------|
| `correlation_heatmap_6x10.png` | Spearman correlations: 6 Medicare variables × 10 hazard scores |
| `top25_overlap_matrix.png` | Overlap of top-25 counties across all 6 vulnerability indices |
| `bump_chart_rankings.png` | Rank shifts for counties appearing in top-15 of 2+ indices |
| `distributions_raw_vs_pctile.png` | 6×2 panel comparing raw and percentile-rescaled distributions |
| `rescaling_comparison_scatter.png` | Min–max vs. percentile rescaling comparison |

## Data Sources and Recency

| Dataset | Source | Vintage | File |
|---------|--------|---------|------|
| HHS emPOWER DME | empowerprogram.hhs.gov | March 2026 | `data/cms_dme_clean.csv` |
| FEMA National Risk Index v1.20 | fema.gov | December 2025 | `data/NRI_Table_Counties.csv` |
| Medicare Monthly Enrollment | data.cms.gov | December 2025 | `data/mme_dec2025_county_clean.csv` |
| Provider of Services (POS) | data.cms.gov | Q4 2025 | `data/POS_File_QIES_Q4_2025.csv` |
| CT FIPS Crosswalk | census.gov | 2022 | `data/ct_fips_crosswalk.csv` |
| ~~MUP DME by Geography~~ | ~~data.cms.gov~~ | ~~RY2024 / DY2022~~ | *Retired — confirmed state-level only, incapable of supporting county-level device-specific analysis. Superseded by the six-covariate Medicare composite (Part 1) and deferred to Part 2's event-time design.* |

**Join key:** Five-digit FIPS county code. Connecticut's 2022 FIPS reorganization (8 legacy counties → 9 planning regions) is handled via crosswalk.

## Repository Structure

```
climate-disability-risk/
├── README.md                                       # ← canonical single-source narrative (this file)
├── CLAUDE.md                                       # project context for analyst handoff
├── requirements.txt
├── data/
│   ├── part1_analysis_ready.csv                    # joined analysis-ready frame (3,212 × 41)
│   ├── lisa_county_classification.csv              # per-county LISA label (3,099 CONUS counties)
│   ├── acs_county_2022.csv                         # ACS 5-year (2022) covariates feeding regression
│   ├── cms_dme_clean.csv                           # HHS emPOWER — electricity-dependent DME
│   ├── NRI_Table_Counties.csv                      # FEMA NRI v1.20 — 9 hazard risk scores
│   ├── mme_dec2025_county_clean.csv                # MME Dec 2025 — enrollment + disability rate
│   ├── ct_fips_crosswalk.csv                       # Connecticut FIPS reorganization crosswalk
│   ├── fema_hazard_clean.csv                       # Filtered FEMA hazard scores
│   ├── climate_disability_vulnerability.csv        # Dual-percentile vulnerability index
│   ├── top25_vulnerability_dual_pctile.csv         # Top-25 convergent-risk counties
│   └── cb_2022_us_county_5m/                       # Census TIGER shapefiles
├── notebooks/
│   ├── part1_statistical_analysis.py               # Spatial pipeline: ρ, Moran's I, LISA, GM regression
│   ├── recompute_vulnerability_dual_percentile.py  # Dual-percentile methodology
│   └── fetch_acs_covariates.py                     # ACS 5-year (2022) county covariate fetch
├── visualizations/
│   ├── fig1_bivariate_choropleth.png               # ★ canonical Q1 visual
│   ├── fig2_top10_split_bars.png                   # ★ top-10 ranking
│   ├── fig3_scatter_quadrants.png                  # ★ two-typology framing
│   ├── fig4_lisa_cluster_map.png                   # ★ statistical hotspots
│   ├── fig5_regression_forest.png                  # ★ canonical Q2 visual
│   ├── grant_overview_dashboard_standalone.html    # interactive d3 dashboard
│   ├── build_grant_overview_visuals.py             # fig1–fig3 generator
│   ├── build_fig4_lisa_map.py                      # fig4 generator
│   ├── build_fig5_regression_forest.py             # fig5 generator
│   ├── build_dashboard_payload.py                  # dashboard data prep
│   ├── make_vulnerability_map.py                   # legacy headline map (superseded by fig1)
│   └── (diagnostic per-covariate choropleths and rescaling-comparison panels)
├── docs/
│   ├── policy_brief.html                           # ★ one-page two-column handout
│   ├── slide_deck.html                             # ★ 11-slide self-contained presentation
│   ├── grant_overview_and_proposal.docx            # ★ Word-format grant narrative
│   ├── part1_statistical_findings.md               # ★ hard numbers for the spatial pipeline
│   ├── analytical_part1b_methodology_pros_cons.md  # internal methodology decision log
│   ├── notion_project_brief.md                     # Notion page source-of-truth
│   └── mme_dec2025_profile.md                      # MME data profiling report
├── Climate and Disabilities: Medicare Focus copy/  # legacy reference docs
└── Marcalee Climate Health copy/                   # grant proposal source materials
```

## Known Limitations

1. **Medicare-only coverage.** The emPOWER and MME data capture Medicare fee-for-service and Medicare Advantage beneficiaries. Medicaid-only and uninsured electricity-dependent individuals are not represented, likely underestimating total population at risk — particularly among younger adults with SCI.

2. **HIPAA cell suppression.** Counties with beneficiary counts between 1 and 10 are suppressed to `*` per CMS de-identification policy. These are converted to `NaN` and excluded from rate calculations.

3. **Measured population is broader than SCI.** This analysis measures electricity-dependent Medicare beneficiaries in aggregate — a population that includes SCI alongside ALS, COPD, neuromuscular disease, advanced cardiovascular disease, and other conditions requiring powered DME. Direct SCI identification requires ICD-10 diagnosis codes (S14.x, S24.x, S34.x, G82.x) available only in claims-level files (CCW or MAX/TAF) accessed through a CMS ResDAC Data Use Agreement, which is out of scope for this phase. SCI physiology, device prevalence, and post-acute care pathways motivate the analytical choices throughout (device categories examined, facility types prioritized, hazard thresholds). Readers should interpret quantitative findings as describing the electricity-dependent Medicare population; SCI-specific conclusions are triangulated with Dr. Alexander's parallel clinical study arm. This is the central scope qualifier of the geospatial analysis.

4. **Equal weighting assumption.** The vulnerability index weights hazard exposure and population dependence equally. Future iterations may explore empirically derived weights based on historical power outage duration and disability-related mortality data.

5. **Ecological fallacy.** County-level associations between hazard scores and population rates do not imply individual-level risk. The clinical study's individual-level data collection is designed to complement this ecological analysis.

6. **Connecticut FIPS reorganization.** Connecticut's 2022 transition from 8 legacy counties to 9 planning regions creates join ambiguity. A crosswalk file is applied, but some county-level comparisons across datasets may reflect boundary changes rather than true population differences.

## References

- Alexander, M., & Alexander, J. (2025). Climate change and disability. In *Climate Change and Human Health* (Chapter 4). Elsevier.
- Luyten, A., et al. (2023). Climate change and health: A scoping review of the inclusion of persons with disabilities. *Journal of Climate Change and Health*.
- FEMA. (2025). National Risk Index v1.20: Technical documentation. Federal Emergency Management Agency.
- HHS. (2026). emPOWER Map 3.0: At-risk electricity-dependent Medicare beneficiaries. U.S. Department of Health and Human Services.
- CMS. (2025). Medicare Monthly Enrollment: December 2025 data release. Centers for Medicare & Medicaid Services.

## Principal Investigator

**Marcalee Alexander, MD**
Marcus Neuroscience Institute | Baptist Health South Florida

## Citation

> Alexander Lab. (2026). *Climate Change Impacts on Electricity-Dependent Medicare Populations: County-Level Geospatial Analysis with Spinal Cord Injury as Clinical Lens.* Marcus Neuroscience Institute, Baptist Health South Florida. https://github.com/barrettbeatrice/climate-disability-risk

---

*Part 1 — Convergent Vulnerability Mapping complete (US, 3,131 counties scored). International extension and clinical study arm (Dr. Alexander) ongoing.*

*Analysis conducted in Python 3.x using pandas, geopandas, matplotlib, seaborn, and scipy. Data: FEMA NRI v1.20 (Dec 2025), HHS emPOWER (Mar 2026), CMS MME (Dec 2025).*
