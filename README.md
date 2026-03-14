# Electricity-Dependent Disability and Climate Hazard Convergence
## A County-Level Risk Analysis to Inform Rehabilitation Preparedness Policy
### Alexander Lab | Marcus Neuroscience Institute | Baptist Health South Florida

---

## Background

Individuals with spinal cord injuries and other high-level disabilities face compounding physiological vulnerabilities during climate-related emergencies: impaired thermoregulation renders them acutely susceptible to heat events, while paralysis and spasticity limit the self-protective mobility that allows ambulatory populations to evacuate or shelter effectively. Critically, a significant subset of this population depends on electricity-powered equipment — including volume ventilators, oxygen concentrators, and powered mobility devices — for survival, meaning that climate-driven power disruption is not merely a convenience failure but a life-safety event. As climate change increases the frequency and geographic reach of extreme weather capable of disrupting electrical infrastructure, the intersection of disability, medical device dependency, and hazard exposure represents an urgent and undercharacterized public health risk.

## Research Gap

No published study has systematically linked federal electricity-dependent durable medical equipment (DME) utilization data with county-level climate hazard exposure scores to identify jurisdictions where vulnerable populations and environmental risk co-occur at highest intensity. This gap persists despite the availability of geocoded federal datasets that make such linkage technically feasible. A recent scoping review of 89 climate-health impact studies spanning 35 countries found zero studies that stratified outcomes by disability status, underscoring the near-total exclusion of disabled populations from the climate-health research literature (Luyten et al., *Journal of Climate Change and Health*, 2023). The consequence is that emergency preparedness policy — at the county, state, and federal levels — is being designed without empirical evidence about where electricity-dependent disabled populations are most concentrated relative to the hazards most likely to disrupt their care.

## Research Question

Which US counties have the highest convergent risk for electricity-dependent disabled populations during climate-related power disruption, and what structural factors differentiate high-risk from low-risk counties?

## Data Sources

| Dataset | Source | Contents | Coverage |
|---------|--------|----------|----------|
| FEMA National Risk Index | fema.gov | County-level composite climate hazard scores | 3,232 counties |
| HHS emPOWER Map | empowerprogram.hhs.gov | Medicare beneficiaries on electricity-dependent DME | County-level |
| US Census TIGER Shapefiles | census.gov | County boundary geometries for spatial analysis | 2022 |
| WHO Rehabilitation Data | who.int | International extension — planned Phase 2 | Regional |

## Methods

- **Composite hazard score** calculated as the mean of hurricane, heat wave, wildfire, coastal flood, and drought RISKS scores from FEMA NRI v1.20 (December 2025); coastal flood is excluded from the composite for inland counties that carry no coastal exposure rather than treated as zero, preventing artificial score suppression for high-risk inland jurisdictions.
- **Power dependency rate** calculated as electricity-dependent Medicare DME beneficiaries divided by total county Medicare beneficiaries, multiplied by 100; this normalization adjusts for county population size so that high-beneficiary urban counties do not dominate the risk ranking on the basis of absolute counts alone.
- **Vulnerability index** calculated as the equal-weighted average of the composite hazard score (0–100) and the power dependency rate (0–100), producing a single convergent risk metric; counties scoring in the upper quartile on both dimensions are prioritized for policy and preparedness intervention.

## Key Findings (Preliminary)

Analysis of 3,217 matched counties identifies the San Joaquin Valley of California as the highest-risk region nationally, with Kern, Fresno, and Madera counties occupying the top three positions on the vulnerability index (scores 51.8, 51.5, and 51.5 respectively). This finding reflects the convergence of the nation's highest composite wildfire, drought, and heat hazard scores with a Medicare population that includes a meaningful share of electricity-dependent device users. Palm Beach and Miami-Dade counties (FL) appear in the top ten, driven by extreme hurricane and coastal flood exposure. San Juan County (NM) is a notable outlier — it ranks 11th nationally despite a moderate hazard score because it carries the highest power dependency rate (11.8%) of any top-20 county, suggesting a structurally high concentration of electricity-dependent residents relative to the broader Medicare population.

## Repository Structure

```
climate-disability-risk/
├── data/
│   ├── fema_hazard_clean.csv              # FEMA NRI filtered to 5 hazard risk scores
│   ├── cms_dme_clean.csv                  # HHS emPOWER electricity-dependent bene counts
│   └── climate_disability_vulnerability.csv  # Joined dataset with vulnerability index
├── notebooks/                             # Jupyter analysis notebooks (in development)
├── visualizations/
│   ├── make_vulnerability_map.py          # Choropleth map generation script
│   └── vulnerability_map.png             # County-level vulnerability index map (300 DPI)
└── docs/                                  # Policy brief and grant deliverables
```

## Known Limitations

- **HIPAA cell suppression**: 5 counties in the emPOWER dataset have suppressed beneficiary counts (cells of 1–10) per CMS de-identification policy and are excluded from the analysis.
- **Medicare-only coverage**: The emPOWER data captures Medicare fee-for-service and Medicare Advantage beneficiaries only; Medicaid-only and uninsured electricity-dependent individuals are not represented, likely underestimating total population at risk, particularly in younger disabled adults.
- **FEMA data gaps**: 86 counties have insufficient data across one or more FEMA NRI hazard categories and carry a null composite hazard score; these counties appear in the dataset but are excluded from vulnerability rankings.
- **Equal weighting assumption**: The vulnerability index weights hazard exposure and power dependency equally. Future iterations will explore empirically derived weights based on historical power outage duration and disability-related mortality data.

## Principal Investigator

**Marcalee Alexander, MD**
Marcus Neuroscience Institute | Baptist Health South Florida
*Grant: [Grant title and number upon award]*

## Citation

If using this dataset or methodology, please cite:

> Alexander Lab. (2026). *Electricity-Dependent Disability and Climate Hazard Convergence: A County-Level Risk Analysis.* Marcus Neuroscience Institute, Baptist Health South Florida. https://github.com/barrettbeatrice/climate-disability-risk

---

*Analysis conducted in Python 3.9 using pandas, geopandas, matplotlib, and the HHS emPOWER ArcGIS REST API. FEMA NRI v1.20 (December 2025). emPOWER data current as of March 2026.*
