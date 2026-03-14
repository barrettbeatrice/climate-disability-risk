# Climate Disability Risk Project

## Project Context
This is a research project supporting Dr. Marcalee Alexander's 
grant on climate change effects on people with disabilities, 
specifically spinal cord injuries, at Baptist Health / Marcus 
Neuroscience Institute, Boca Raton.

The project maps electricity-dependent disability populations 
against climate hazard exposure at the county level (US) and 
WHO region level (international).

## Research Question
Which US counties and international regions have the highest 
convergent risk for electricity-dependent disabled populations 
during climate-related power disruption events?

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