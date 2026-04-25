# Notion Project Brief — Source of Truth for Grant Overview

_Pulled from Notion page "🌎 🌡️ A County, National & International-Level Risk Analysis to Inform Rehabilitation Preparedness Policy" on 2026-04-22._

**Notion URL:** https://www.notion.so/32356834683c81f59293e357eb733f47
**GitHub URL:** https://github.com/barrettbeatrice/climate-disability-risk

---

## Project Title
**A County-Level Risk Analysis to Inform Rehabilitation Preparedness Policy**
Alexander Lab · Marcus Neuroscience Institute · Baptist Health South Florida · March 2026

## Research Question (Part 1)
Which US counties have the highest convergent risk for electricity-dependent disabled populations during climate-related power disruption, and what structural factors differentiate high-risk from low-risk counties?

## Background
People with spinal cord injuries and other disabilities requiring electricity-dependent medical equipment face compounding vulnerability during climate events. High-level SCI above T6 interrupts the autonomic nervous system's ability to thermoregulate — leaving individuals vulnerable to hyperthermia or hypothermia even in mild ambient temperatures. When extreme weather causes power outages, this population faces life-threatening risk that current disaster preparedness frameworks do not adequately address.

No published study has systematically mapped where these populations are most concentrated relative to climate hazard exposure. A 2023 scoping review of 89 climate-health impact studies across 35 countries found **zero studies that stratified outcomes by disability status** (Luyten et al., *Journal of Climate Change and Health*, 2023).

## Data Sources
| Dataset | Source | Description | Coverage |
|---|---|---|---|
| FEMA National Risk Index | fema.gov | County-level composite climate hazard scores | 3,232 counties |
| HHS emPOWER Map | empowerprogram.hhs.gov | Medicare beneficiaries on electricity-dependent DME | County-level |
| US Census TIGER Shapefiles | census.gov | County boundary geometries | 2022 |
| WHO Rehabilitation Data | who.int | International extension — Phase 2 | Global |

## Methods
- **Composite Hazard Score** — mean of five FEMA RISKS scores (grid-disruptive hazards): hurricane, heat wave, wildfire, coastal flood, drought. Coastal flood excluded for inland counties rather than treated as zero.
- **Power Dependency Rate** — total electricity-dependent DME beneficiaries ÷ total Medicare beneficiaries × 100. Normalized by county Medicare population.
- **Vulnerability Index (dual-percentile)** — equal-weighted mean of (a) the national percentile rank of the composite hazard score and (b) the national percentile rank of the power-dependency rate. Dual-percentile rescaling is necessary because the raw hazard score spans 0–100 while the raw power-dependency rate spans roughly 0–40%; averaging the raw values would under-weight power dependency by ~15×.

## Key Findings
- **3,131 counties** successfully scored out of 3,212 joined (81 excluded — insufficient FEMA hazard data; 5 additional suppressed under HIPAA cell-size rules)
- **Intermountain West / Four Corners corridor** dominates the national ranking — all 10 top-ranked counties sit in New Mexico, Colorado, or Utah
- **Two distinct risk profiles**:
  - **(a) Intermountain drought-and-dependency corridor** — the dominant top-10 pattern
  - **(b) Southeast hurricane-and-coastal-flood coast** — Palm Beach (hazard percentile 99.8) and Miami-Dade (99.7) sit in the top 1% of US counties on hazard exposure, making Baptist Health South Florida the highest-climate-hazard-exposed major hospital system in the Southeast
- **Power dependency operates as an independent pathway** — Pueblo CO, Iron UT, Millard UT, and Garfield UT reach top-25 positions on moderate hazard scores paired with power-dependency rates near the national ceiling
- **San Juan County, NM** leads the nation (vulnerability index 96.9) on both dimensions simultaneously

### Top 10 Most Vulnerable Counties (dual-percentile)
| Rank | County | State | Hazard pctile | Power pctile | Vuln. Index |
|---|---|---|---|---|---|
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

## Planned Extensions
- **Phase 2 — International**: WHO rehabilitation access + World Bank electricity access + IPCC regional temperature projections, integrated with InSCI community survey (31 countries, 15,051 participants, 2022–2024).
- **Phase 3 — Smart Device Monitoring**: prospective disability-specific climate impact tracking per Alexander & Alexander (2025).

## Citations
- Alexander M, Alexander J. *The need for new paradigms to assess and respond to the impacts of climate change on disability.* In: Climate Change and Disability: A Collaborative Approach to a Sustainable Future. Elsevier, 2025.
- Alexander M et al. *A bellweather for climate change and disability.* Spinal Cord Series and Cases. 2019.
- Luyten et al. *Health impact studies of climate change adaptation and mitigation measures — a scoping review.* Journal of Climate Change and Health. 2023.

## Status
🟢 Phase 1 Complete · Phase 2 In Progress
**PI:** Dr. Marcalee Alexander · Marcus Neuroscience Institute · Baptist Health
**Analyst:** Barrett Jackson

## Part 2 note from the Notion page
> _retrospective, different usage patterns in different locales and cities_

---

## GitHub repository structure (as of pull)
```
climate-disability-risk/
├── .claude/
├── data/
│   ├── fema_hazard_clean.csv              (344 KB)
│   ├── cms_dme_clean.csv                  (169 KB)
│   └── climate_disability_vulnerability.csv  (628 KB)
├── docs/
│   └── policy_brief.html                  (12 KB)
├── visualizations/
│   ├── make_vulnerability_map.py          (8 KB)
│   └── vulnerability_map.png              (2.5 MB)
├── .gitignore
├── CLAUDE.md
├── README.md
└── requirements.txt
```
