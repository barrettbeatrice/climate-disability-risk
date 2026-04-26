# Climate Disability Risk Project

## Project Context
This is a research project supporting Dr. Marcalee Alexander's 
grant on climate change effects on people with disabilities at 
Baptist Health / Marcus Neuroscience Institute, Boca Raton.

The clinical grant focuses on persons with spinal cord injuries 
(SCI). This geospatial analysis uses the best available public 
federal data — which identifies **electricity-dependent Medicare 
beneficiaries** as an aggregate population (including SCI, ALS, 
COPD, neuromuscular disease, and other conditions requiring 
powered DME). SCI is the motivating clinical lens: it frames 
device selection, distance thresholds, climate-hazard prioritization, 
and policy interpretation. SCI cannot be isolated from this data 
without access to claims-level files through a CMS Data Use 
Agreement (ResDAC), which is out of scope for this phase. All 
quantitative findings describe the electricity-dependent 
Medicare population; SCI-specific conclusions are drawn 
cautiously and triangulated with the clinical study arm.

The project maps electricity-dependent Medicare populations 
against climate hazard exposure at the county level (US) and 
WHO region level (international).

## Research Question (Part 1)

Which US counties have the highest convergent risk for 
electricity-dependent disabled populations during climate-related 
power disruption, and what structural factors differentiate 
high-risk from low-risk counties?

Part 1 is a static, cross-sectional geospatial analysis: it maps 
where convergent climate-and-disability risk is structurally located. 
It does not measure behavioral adaptation, coping, or response — 
those constructs require event-time data and individual-level 
outcomes that the public Medicare files cannot provide on their 
own. They are out of scope for Part 1 and reserved for future work 
(Phase 2 / international extension and Dr. Alexander's parallel 
clinical study arm).

## Primary Data Sources
- CMS Medicare DME Dataset (data.cms.gov) — county-level, 
  HCPCS codes for electricity-dependent equipment
- FEMA National Risk Index (fema.gov) — county-level composite 
  climate hazard scores
- HHS Empower Map data — Medicare beneficiaries on 
  electricity-dependent DME by geography
- WHO Rehabilitation Data — international extension
- World Bank electricity access indicators — international extension

## Join Key
US analysis joins on FIPS county code.
International analysis joins on WHO region / country ISO code.

## Tech Stack
- Python (pandas, geopandas, matplotlib, seaborn)
- Jupyter notebooks for analysis
- Tableau Public for final dashboard
- PostgreSQL if data volume requires it

## Output Goals (by Monday)
1. GitHub repository with research-grade README
2. Data model / entity-relationship diagram
3. At least one working choropleth map
4. One-page policy brief PDF

## Conventions
- All data files go in /data
- All notebooks go in /notebooks  
- All visualizations go in /visualizations
- All written deliverables go in /docs
- Use snake_case for all file names
- Comment code as if the audience is a clinical researcher, 
  not a software engineer