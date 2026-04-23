# Climate Change Impacts on Electricity-Dependent Medicare Populations
## County-Level Geospatial Analysis of Electricity-Dependent Disability and Climate Hazard Convergence
### Alexander Lab | Marcus Neuroscience Institute | Baptist Health South Florida

> **Scope and framing.** The clinical grant supported by this work focuses on persons with spinal cord injuries (SCI). This geospatial arm uses the best available public federal data, which identifies **electricity-dependent Medicare beneficiaries in aggregate** — a population that includes SCI, ALS, COPD, neuromuscular disease, and others who rely on powered durable medical equipment for daily function. SCI is the motivating clinical lens: it frames device selection, hazard prioritization, and policy interpretation throughout. SCI cannot be directly isolated from public CMS files; direct identification requires claims-level data obtained through a CMS Data Use Agreement (ResDAC), which is out of scope for this phase. Quantitative findings describe the electricity-dependent Medicare population as a whole; SCI-specific conclusions are drawn cautiously and explicitly triangulated with the clinical study arm.

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

## Two-Part Analysis Structure

### Part 1: Aggregate Vulnerability Analysis (Complete)

Six Medicare variables measuring electricity-dependent population density are joined with nine FEMA National Risk Index hazard scores across approximately 3,200 US counties. A percentile-rank rescaled vulnerability index identifies counties where high population dependence and high climate hazard exposure co-occur.

**Medicare Variables (Part 1):**

| Variable | Source | Description |
|----------|--------|-------------|
| `power_dependency_rate` | HHS emPOWER | Electricity-dependent DME beneficiaries per 100 Medicare beneficiaries |
| `o2_services_rate` | HHS emPOWER | Oxygen services beneficiaries per 100 Medicare beneficiaries |
| `home_health_rate` | HHS emPOWER | Home health beneficiaries per 100 Medicare beneficiaries |
| `hospice_rate` | HHS emPOWER | Hospice beneficiaries per 100 Medicare beneficiaries |
| `any_healthcare_rate` | HHS emPOWER | Any electricity-dependent healthcare beneficiaries per 100 Medicare beneficiaries |
| `dsbld_rate` | MME Dec 2025 | Disabled (under-65) Medicare beneficiaries per 100 total beneficiaries |

**FEMA NRI Hazard Types (9):**

Hurricane (HRCN), Heat Wave (HWAV), Wildfire (WFIR), Coastal Flood (CFLD), Drought (DRGT), Cold Wave (CWAV), Inland Flood (IFLD), Winter Weather (WNTW), Ice Storm (ISTM)

### Part 2: Adaptation-Pattern Typology (In Progress)

Part 2 shifts from *where is vulnerability located* (Part 1) to *how are electricity-dependent populations adapting to climate exposure differently across US locales and metropolitan areas*. Using the six Medicare utilization variables from Part 1 plus the FEMA hazard composite, Part 2 clusters US counties and Core-Based Statistical Areas (CBSAs) into adaptation profiles — distinct patterns of coping defined by the co-occurrence of hazard exposure, power dependency, home-health uptake, hospice rate, and service engagement. The working hypothesis is that electricity-dependent Medicare populations adapt along at least five distinguishable pathways (shelter-in-place with dense clinical support; medical migration to low-hazard metros; stranded rural dependency; hospice-as-adaptation; urban-infrastructure-enabled high-dependency), with meaningful equity consequences across them.

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

The composite hazard score is the mean of all applicable FEMA NRI RISK scores across the nine hazard types. Coastal flood is excluded from the composite for inland counties (those carrying no coastal exposure) rather than treated as zero, preventing artificial score suppression for high-risk inland jurisdictions.

### Vulnerability Index

For each of the six Medicare variables, a vulnerability index is computed as:

```
vuln_V = (composite_hazard_score_rescaled + V_rate_rescaled) / 2
```

This equal-weighted average identifies counties where both dimensions — climate hazard exposure and population dependence — are simultaneously elevated.

### Regression Specification

```
V_rate ~ β₁(HRCN) + β₂(HWAV) + β₃(WFIR) + β₄(CFLD) + β₅(DRGT)
       + β₆(CWAV) + β₇(IFLD) + β₈(WNTW) + β₉(ISTM) + γ₁(dsbld_rate) + ε
```

The disability rate (`dsbld_rate`) from the Medicare Monthly Enrollment file serves as the sole covariate. Dual eligibility, race/ethnicity, and Medicare Advantage share were evaluated and excluded as out of scope for this phase of the analysis; each could be reintroduced in a follow-on equity-focused extension.

## Key Findings (Part 1)

**Regional shift with disability rate inclusion.** The addition of `dsbld_rate` from the Medicare Monthly Enrollment file shifts the convergent risk geography from California's San Joaquin Valley (which dominated the original power-dependency-only ranking) toward the Gulf Coast and Deep South. California's low state-level disability rate (7.05%) suppresses those counties' combined vulnerability scores, while high-disability states in the Southeast rise.

**Disability rate as a distinct construct.** Spearman correlation between `dsbld_rate` and `power_dependency_rate` is ρ = 0.286, confirming that the two variables capture meaningfully different populations. The disability rate variable produces 18 counties in its top-25 that do not appear in any other variable's top-25 — the most distinct of all six indices.

**Negative inland-flood correlations.** The Spearman correlation heatmap reveals negative correlations between most emPOWER variables and inland flood risk scores, suggesting that electricity-dependent populations are not concentrated in inland flood zones. This warrants further investigation in Part 2.

**Cross-index overlap.** The top-25 overlap matrix shows moderate convergence among the five emPOWER-derived indices (sharing 10–20 counties) but limited overlap with the disability-derived index, reinforcing its value as an independent dimension of vulnerability.

## Visualizations

All visualizations are in `visualizations/` at 300 DPI.

### Choropleth Maps (8)

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
| ~~MUP DME by Geography~~ | ~~data.cms.gov~~ | ~~RY2024 / DY2022~~ | *Retired — confirmed state-level only; superseded by adaptation-pattern analysis* |

**Join key:** Five-digit FIPS county code. Connecticut's 2022 FIPS reorganization (8 legacy counties → 9 planning regions) is handled via crosswalk.

## Repository Structure

```
climate-disability-risk/
├── README.md
├── requirements.txt
├── data/
│   ├── cms_dme_clean.csv                  # HHS emPOWER — electricity-dependent DME (3,233 counties)
│   ├── NRI_Table_Counties.csv             # FEMA NRI v1.20 — 9 hazard risk scores (3,232 counties)
│   ├── mme_dec2025_county_clean.csv       # MME Dec 2025 — enrollment + disability rate (3,278 counties)
│   ├── POS_File_QIES_Q4_2025.csv         # Provider of Services Q4 2025
│   ├── ct_fips_crosswalk.csv              # Connecticut FIPS reorganization crosswalk
│   ├── part1_analysis_ready.csv           # Merged analysis-ready dataset (3,212 counties × 41 cols)
│   ├── fema_hazard_clean.csv              # Filtered FEMA hazard scores
│   ├── climate_disability_vulnerability.csv  # Legacy vulnerability index
│   └── cb_2022_us_county_5m/             # Census TIGER shapefiles (county boundaries)
├── visualizations/
│   ├── choropleth_vuln_power_dependency.png
│   ├── choropleth_vuln_o2_services.png
│   ├── choropleth_vuln_home_health.png
│   ├── choropleth_vuln_hospice.png
│   ├── choropleth_vuln_any_healthcare.png
│   ├── choropleth_vuln_disability.png
│   ├── choropleth_composite_hazard.png
│   ├── choropleth_dsbld_rate_raw.png
│   ├── correlation_heatmap_6x10.png
│   ├── top25_overlap_matrix.png
│   ├── bump_chart_rankings.png
│   ├── distributions_raw_vs_pctile.png
│   └── rescaling_comparison_scatter.png
├── docs/
│   ├── mme_dec2025_profile.md             # MME data profiling report
│   └── policy_brief.html                  # Policy brief (draft)
├── Climate and Disabilities: Medicare Focus copy/
│   ├── methodology_and_data_dictionary.md # Full methodology — Part 1 of 2
│   ├── cms_data_pull_guide.md             # Download instructions for remaining CMS data
│   └── medicare_variable_eda_report.md    # Exploratory data analysis report
├── Marcalee Climate Health copy/
│   ├── Grant Proposal -- DraftsProtocols/ # Grant proposal narrative and drafts
│   └── Chapter 4.pdf                      # Alexander & Alexander (2025), Elsevier
└── notebooks/                             # Analysis notebooks (in development)
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

*Part 1 of 2 — Aggregate Vulnerability Analysis complete. Part 2 (adaptation-pattern typology across US locales and CBSAs) in progress.*

*Analysis conducted in Python 3.x using pandas, geopandas, matplotlib, seaborn, and scipy. Data: FEMA NRI v1.20 (Dec 2025), HHS emPOWER (Mar 2026), CMS MME (Dec 2025).*
