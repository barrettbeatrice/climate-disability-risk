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
- **Composite Hazard Score** — mean of five FEMA RISKS scores: hurricane, heat wave, wildfire, coastal flood, drought. Coastal flood excluded for inland counties rather than treated as zero.
- **Power Dependency Rate** — total electricity-dependent DME beneficiaries ÷ total Medicare beneficiaries × 100. Normalized by county Medicare population.
- **Vulnerability Index** — mean of composite hazard score and power dependency rate (both on 0–100 scales).

## Key Findings
- **3,144 counties** successfully scored out of 3,232 (88 excluded — insufficient FEMA hazard data)
- **San Joaquin Valley** counties dominate top rankings (wildfire/heat/drought at 97th–99th percentile)
- **Palm Beach and Miami-Dade rank in the national top 10** — placing Baptist Health's primary service area within the highest-risk zone in the country
- **Two distinct risk pathways**: (a) extreme climate hazard exposure (California), (b) extreme power dependency concentration (rural Southwest)
- **San Juan County NM** — highest power dependency rate in the top 20 (11.8%)
- **5 counties suppressed** in emPOWER due to HIPAA cell-size masking (1–10 counts)

### Top 10 Most Vulnerable Counties
| Rank | County | State | Hazard | Power Dep. | Vuln. Index |
|---|---|---|---|---|---|
| 1 | Kern | CA | 97.9 | 5.7% | 51.8 |
| 2 | Fresno | CA | 98.8 | 4.3% | 51.5 |
| 3 | Madera | CA | 99.0 | 4.0% | 51.5 |
| 7 | San Joaquin | CA | 96.4 | 3.7% | 50.0 |
| **8** | **Palm Beach** | **FL** | **96.2** | **2.7%** | **49.5** |
| **9** | **Miami-Dade** | **FL** | **95.0** | **4.0%** | **49.5** |
| 10 | San Juan | NM | 86.8 | 11.8% | 49.3 |

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
