/**
 * build_grant_overview_docx.js
 *
 * Produces: docs/grant_overview_and_proposal.docx
 *
 * Scope (per PI/analyst directive, 2026-04-22):
 *   - Six Medicare-derived covariates at the county level.
 *   - Their shared dependence on continuous electrical power.
 *   - Elevated risk to disabled beneficiaries when extreme climate events
 *     (heat, cold, floods, storms, wildfire) disrupt that power.
 *   - No clustering, no CBSA typology, no LISA. Plain overview + proposal.
 */

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, PageOrientation, LevelFormat,
  ExternalHyperlink, TabStopType, TabStopPosition, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
} = require("docx");

const OUT = "/sessions/charming-dreamy-thompson/mnt/climate-disability-risk/docs/grant_overview_and_proposal.docx";

// ---------- helpers ----------
const P = (text, opts = {}) =>
  new Paragraph({
    spacing: { after: 120, line: 300 },
    alignment: AlignmentType.JUSTIFIED,
    ...opts,
    children: [new TextRun({ text, font: "Calibri", size: 22, ...(opts.run || {}) })],
  });

const H1 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 300, after: 160 },
    children: [new TextRun({ text, font: "Calibri", size: 32, bold: true, color: "8B1A1A" })],
  });

const H2 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 220, after: 120 },
    children: [new TextRun({ text, font: "Calibri", size: 26, bold: true, color: "1A1A1A" })],
  });

const BULLET = (text) =>
  new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, font: "Calibri", size: 22 })],
  });

const CALLOUT = (text) =>
  new Paragraph({
    spacing: { before: 120, after: 160 },
    alignment: AlignmentType.LEFT,
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: "8B1A1A", space: 12 } },
    indent: { left: 240 },
    children: [new TextRun({ text, italics: true, font: "Calibri", size: 22, color: "2A0000" })],
  });

const border = { style: BorderStyle.SINGLE, size: 4, color: "B0B0B0" };
const borders = { top: border, bottom: border, left: border, right: border };

const cell = (content, opts = {}) =>
  new TableCell({
    borders,
    width: { size: opts.width || 2340, type: WidthType.DXA },
    shading: opts.head ? { fill: "F1E4E4", type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({
          text: content,
          font: "Calibri",
          size: opts.head ? 20 : 20,
          bold: !!opts.head,
          color: opts.head ? "1A1A1A" : undefined,
        })],
      }),
    ],
  });

// ---------- document content ----------
const sections = [];

// ===== TITLE BLOCK =====
sections.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({
      text: "GRANT OVERVIEW AND PROPOSAL",
      font: "Calibri", size: 20, bold: true, color: "8B1A1A",
      characterSpacing: 30,
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({
      text: "Electricity-Dependent Disability and Climate Hazard Convergence",
      font: "Calibri", size: 36, bold: true, color: "1A1A1A",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 220 },
    children: [new TextRun({
      text: "A County-Level Risk Analysis to Inform Rehabilitation Preparedness Policy",
      font: "Calibri", size: 24, italics: true, color: "444444",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({
      text: "Alexander Lab  \u2022  Marcus Neuroscience Institute  \u2022  Baptist Health South Florida",
      font: "Calibri", size: 20, color: "555555",
    })],
  }),
);

// ===== EXECUTIVE SUMMARY =====
sections.push(
  H1("Executive Summary"),
  P("Climate change is increasing the frequency, intensity, and geographic reach of extreme heat, cold, flooding, and storms. For most of the US population, a resulting power outage is an inconvenience. For Medicare beneficiaries who depend on electricity for survival \u2014 ventilators, home oxygen, powered mobility devices, in-home dialysis, infusion pumps, refrigerated medications \u2014 the same outage is a life-safety event. This population is not only dependent on continuous current at the device level; individuals with high-level spinal cord injury (above T6) and related neurological disabilities also lose the autonomic capacity to thermoregulate, making climate-disaster-driven loss of heating, cooling, and climate-controlled housing independently life-threatening."),
  P("This project links two federal data sources at the US county level \u2014 the Centers for Medicare & Medicaid Services (CMS) Medicare Monthly Enrollment / Geographic Variation files and the FEMA National Risk Index (NRI) v1.20 \u2014 to identify the counties in which electrically-dependent, disabled Medicare beneficiaries are most concentrated relative to the climate hazards most likely to disrupt their care. It does so using six county-level Medicare utilization covariates, each of which tracks an aspect of the population\u2019s dependence on a functioning electrical grid and on continuous access to in-home or near-home medical services."),
  P("The analysis is intentionally narrow: six covariates, one composite climate-hazard score, one convergence index, 3,131 counties. The deliverable is a county-level vulnerability map and a short list of highest-risk counties that can be used to direct preparedness funding, tele-rehabilitation infrastructure, and grid-hardening prioritization toward the jurisdictions where loss of power is most likely to become loss of life."),
);

// ===== SPECIFIC AIMS =====
sections.push(
  H1("Specific Aims"),
  P("This proposal documents Part 1: a static, cross-sectional geospatial analysis of where convergent climate-and-disability risk is structurally located across US counties. Behavioral adaptation, coping, and individual-level outcomes are out of scope for Part 1 and are carried by Phase 2 and Dr. Alexander's parallel clinical study arm."),
  H2("Aim 1. Characterize the electrically-dependent Medicare population at the county level."),
  P("Using six publicly available, county-level Medicare utilization covariates (detailed below), produce a national dataset that quantifies, for every US county, the share of the Medicare population whose continued health and safety depends on uninterrupted access to electrical power and electricity-mediated care delivery."),
  H2("Aim 2. Quantify county-level convergence of power-dependent disability and climate hazard."),
  P("Using the FEMA NRI v1.20 composite score across the five hazards most capable of disrupting the electrical grid \u2014 hurricanes, heat waves, wildfires, coastal flooding, and drought \u2014 compute a convergent-risk index that equally weights (a) the population\u2019s structural dependence on power and (b) its exposure to climate hazards that remove it."),
  H2("Aim 3. Translate the national risk map into preparedness policy guidance."),
  P("Identify the top-quartile counties on the convergent-risk index and deliver a one-page policy brief \u2014 aimed at state emergency-management agencies, rehabilitation networks, and CMS \u2014 that names the highest-risk jurisdictions, documents the specific hazard profile driving each one, and recommends preparedness actions scaled to the risk."),
);

// ===== BACKGROUND =====
sections.push(
  H1("Background and Significance"),
  H2("The population at stake"),
  P("Several overlapping Medicare sub-populations share a single structural vulnerability: their survival or baseline function depends on continuous access to electrical power. This includes beneficiaries using powered durable medical equipment (DME) \u2014 ventilators, BiPAP/CPAP, powered wheelchairs, hospital beds, suction machines, enteral feeding pumps \u2014 as well as beneficiaries receiving home oxygen services, home health visits, or hospice care in the home. Beyond the device level, individuals with high-level spinal cord injury, multiple sclerosis, ALS, and advanced COPD or heart failure also depend on climate-controlled housing: the loss of cooling in a heat wave or heating in a winter storm is, for these patients, not a discomfort but a clinical emergency."),
  P("The Luyten et al. (2023) scoping review of 89 climate-health impact studies across 35 countries found zero studies that stratified outcomes by disability status. Emergency-preparedness policy \u2014 at the county, state, and federal levels \u2014 is therefore being designed in the absence of systematic evidence about where these populations actually live, and which climate hazards they are most exposed to."),
  H2("Why Medicare data is the right lens"),
  P("Medicare administrative data is the only US dataset that simultaneously (a) captures electricity-dependent care utilization at a nationally consistent geographic level, (b) covers the population most likely to rely on powered medical equipment, and (c) is publicly available in a form that supports county-level analysis without a Data Use Agreement. The Medicare Geographic Variation Public Use File reports utilization rates for exactly the kinds of care that are either power-dependent (oxygen services, DME) or delivered into climate-sensitive residential environments (home health, hospice). Joined to the FEMA NRI, it produces the evidence base that disaster-preparedness policy currently lacks."),
);

// ===== DATA & COVARIATES =====
sections.push(
  H1("Data and Covariates"),
  H2("Primary datasets"),
);

// Data sources table
sections.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2080, 2080, 3600, 1600],
  rows: [
    new TableRow({ tableHeader: true, children: [
      cell("Dataset", { head: true, width: 2080 }),
      cell("Source", { head: true, width: 2080 }),
      cell("Contents used", { head: true, width: 3600 }),
      cell("Coverage", { head: true, width: 1600 }),
    ]}),
    new TableRow({ children: [
      cell("Medicare Monthly Enrollment / Geographic Variation PUF", { width: 2080 }),
      cell("data.cms.gov", { width: 2080 }),
      cell("Six county-level utilization rates + total and disability enrollment counts", { width: 3600 }),
      cell("3,212 counties, Dec 2025", { width: 1600 }),
    ]}),
    new TableRow({ children: [
      cell("FEMA National Risk Index v1.20", { width: 2080 }),
      cell("fema.gov", { width: 2080 }),
      cell("Per-hazard RISKS scores (hurricane, heat wave, wildfire, coastal flood, drought, etc.)", { width: 3600 }),
      cell("3,232 counties, Dec 2025", { width: 1600 }),
    ]}),
    new TableRow({ children: [
      cell("HHS emPOWER Map", { width: 2080 }),
      cell("empowerprogram.hhs.gov", { width: 2080 }),
      cell("Corroborating electricity-dependent DME beneficiary counts (validation sidecar)", { width: 3600 }),
      cell("County-level", { width: 1600 }),
    ]}),
    new TableRow({ children: [
      cell("US Census TIGER shapefile", { width: 2080 }),
      cell("census.gov", { width: 2080 }),
      cell("County boundary geometries for choropleth mapping", { width: 3600 }),
      cell("2022 vintage", { width: 1600 }),
    ]}),
  ],
}));

// Covariates table
sections.push(
  H2("The six Medicare covariates"),
  P("Each covariate is a per-100-Medicare-beneficiary rate at the county level, computed from the most recent publicly available CMS data. All six share one property: their continued delivery depends on a working electrical grid, climate-controlled housing, or both."),
);

sections.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2600, 3800, 2960],
  rows: [
    new TableRow({ tableHeader: true, children: [
      cell("Covariate (variable name)", { head: true, width: 2600 }),
      cell("What it captures", { head: true, width: 3800 }),
      cell("Why it is power-sensitive", { head: true, width: 2960 }),
    ]}),
    new TableRow({ children: [
      cell("Power-dependent DME rate (total_power_dependent_rate)", { width: 2600 }),
      cell("Medicare beneficiaries using electrically-powered durable medical equipment per 100 beneficiaries.", { width: 3800 }),
      cell("Ventilators, BiPAP, powered mobility, suction, feeding pumps all fail when power fails.", { width: 2960 }),
    ]}),
    new TableRow({ children: [
      cell("Home oxygen services rate (o2_services_rate)", { width: 2600 }),
      cell("Medicare beneficiaries receiving home oxygen services per 100 beneficiaries.", { width: 3800 }),
      cell("Oxygen concentrators draw continuous current; tank backup lasts hours, not days.", { width: 2960 }),
    ]}),
    new TableRow({ children: [
      cell("Home health rate (home_health_rate)", { width: 2600 }),
      cell("Medicare beneficiaries receiving Medicare-reimbursed home health services per 100 beneficiaries.", { width: 3800 }),
      cell("Care delivered into the home is disrupted by both power loss and road-access loss during disasters.", { width: 2960 }),
    ]}),
    new TableRow({ children: [
      cell("Hospice rate (hospice_rate)", { width: 2600 }),
      cell("Medicare beneficiaries receiving hospice care per 100 beneficiaries.", { width: 3800 }),
      cell("In-home hospice relies on continuous nursing access and functioning medication refrigeration.", { width: 2960 }),
    ]}),
    new TableRow({ children: [
      cell("Any-healthcare-service rate (any_healthcare_rate)", { width: 2600 }),
      cell("Composite Medicare utilization across DME, home health, oxygen, and hospice per 100 beneficiaries.", { width: 3800 }),
      cell("Summary signal of the county\u2019s overall dependence on power-sensitive Medicare services.", { width: 2960 }),
    ]}),
    new TableRow({ children: [
      cell("Medicare disability enrollment rate (dsbld_rate)", { width: 2600 }),
      cell("Share of Medicare beneficiaries enrolled on the basis of disability (rather than age alone).", { width: 3800 }),
      cell("Identifies the population most exposed to thermoregulatory and mobility-related climate risk.", { width: 2960 }),
    ]}),
  ],
}));

// ===== APPROACH =====
sections.push(
  H1("Approach"),
  H2("1. Composite hazard score."),
  P("From the FEMA NRI v1.20, extract the county-level RISKS scores for the five hazard types most capable of disrupting the electrical grid and climate-controlled housing: hurricanes, heat waves, wildfires, coastal flooding, and drought. Compute the composite hazard score as the mean of the applicable scores, with coastal flood excluded for inland counties rather than treated as zero (to prevent artificial score suppression for high-risk inland jurisdictions)."),
  H2("2. Power-dependence signature."),
  P("For each county, compute the six covariates as per-100-beneficiary rates. Rank each covariate to its national percentile to put the six signatures on a common 0\u2013100 scale."),
  H2("3. Convergent-risk index (dual-percentile)."),
  P("Compute the equal-weighted convergent-risk index as the mean of two national percentile ranks: (a) the percentile rank of the county\u2019s composite 5-hazard score, and (b) the percentile rank of the county\u2019s power-dependent DME rate. Both inputs are rescaled to 0\u2013100 before averaging; this is necessary because the raw composite hazard score spans 0\u2013100 while the raw power-dependency rate spans approximately 0\u201340% (median ~5%), so averaging the raw values would under-weight power dependency by roughly 15-fold and artificially privilege high-hazard California counties. Under the dual-percentile formulation, a county ranks highest when it scores near the national top on both dimensions simultaneously. Counties scoring in the top quartile on both dimensions are flagged as priority jurisdictions for preparedness intervention."),
  H2("4. Covariate-specific vulnerability maps."),
  P("Render a choropleth map for each of the six covariates individually against the composite hazard score, so that policymakers can see whether a county\u2019s risk is driven by high-DME-dependency populations, high home-health intensity, high disability enrollment, or a combination."),
  H2("5. Sensitivity checks."),
  P("Re-run the convergent index with (a) the HHS emPOWER electricity-dependent DME count as an alternative to the CMS DME rate, (b) un-weighted vs. hazard-duration-weighted scores, and (c) the exclusion of the five HIPAA-suppressed counties. Report rank stability for the top-50 counties."),
);

// ===== PRELIMINARY FINDINGS =====
sections.push(
  H1("Preliminary Findings"),
  P("Phase 1 analysis of 3,131 matched counties (out of 3,212 total joined; 81 excluded due to insufficient FEMA hazard data, 5 additional counties suppressed under HIPAA cell-size rules) produces three findings of immediate policy relevance:"),
  BULLET("The Intermountain West / Four Corners corridor dominates the national convergent-risk ranking. San Juan, NM leads the nation (index 96.9), with El Paso, CO (94.5), Bernalillo, NM (94.2), Sandoval, NM (94.1), and Adams, CO (93.8) completing the top five. All ten of the top-ranked counties sit in New Mexico, Colorado, or Utah \u2014 a corridor jointly exposed to drought, heat wave, and wildfire hazard at or above the 90th national percentile and carrying power-dependent Medicare populations in the top decile. This is the region where structural power-dependency and grid-disruptive climate hazard converge most sharply."),
  BULLET("A second, distinct risk profile emerges along the Southeast coast \u2014 and directly within Baptist Health\u2019s primary service area. Palm Beach (hazard percentile 99.8) and Miami-Dade (99.7) sit in the top 1% of US counties on the composite hazard score, driven by hurricane and coastal-flood exposure, making Baptist Health South Florida the highest-climate-hazard-exposed major hospital system in the Southeast. Their convergent-risk ranks (1,558 and 1,013 respectively) are held below the Intermountain West only because South Florida\u2019s Medicare power-dependency rate sits in the bottom tercile nationally \u2014 a profile of extreme climate exposure convergent with moderate device-dependency. The finding nonetheless places the grant-holder institution at the frontline of the hurricane/coastal-flood pathway and identifies it as the largest-scale US hospital system operating in a top-1%-hazard environment."),
  BULLET("Power dependency operates as an independent vulnerability pathway. Several counties in the top 25 \u2014 including Pueblo, CO (rank 12, hazard 86.7 / power 98.2), Iron, UT (rank 13, hazard 87.0 / power 97.5), Millard, UT (rank 14, hazard 86.9 / power 97.0), and Garfield, UT (rank 21, hazard 82.1 / power 98.9) \u2014 reach top-ranked positions on moderate hazard scores but extreme power-dependency rates near the national ceiling. This confirms that electricity-dependent disability cannot be treated as a secondary amplifier of climate exposure; in multiple US regions it is itself the dominant driver of disaster risk."),
  CALLOUT("Together, these findings identify two geographically and mechanistically distinct categories of highest-risk county \u2014 the Intermountain West drought-and-dependency corridor, and the Southeast hurricane-and-coastal-flood coast including Baptist Health\u2019s service area \u2014 each of which requires a different preparedness response."),
  H2("Top 10 counties by convergent-risk index (dual-percentile)"),
);

sections.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [600, 2600, 1800, 1400, 1480, 1480],
  rows: [
    new TableRow({ tableHeader: true, children: [
      cell("#", { head: true, width: 600 }),
      cell("County", { head: true, width: 2600 }),
      cell("State", { head: true, width: 1800 }),
      cell("Hazard pctile", { head: true, width: 1400 }),
      cell("Power pctile", { head: true, width: 1480 }),
      cell("Vuln. index", { head: true, width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("1", { width: 600 }), cell("San Juan", { width: 2600 }), cell("NM", { width: 1800 }),
      cell("98.3", { width: 1400 }), cell("95.6", { width: 1480 }), cell("96.9", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("2", { width: 600 }), cell("El Paso", { width: 2600 }), cell("CO", { width: 1800 }),
      cell("92.0", { width: 1400 }), cell("97.1", { width: 1480 }), cell("94.5", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("3", { width: 600 }), cell("Bernalillo", { width: 2600 }), cell("NM", { width: 1800 }),
      cell("97.4", { width: 1400 }), cell("91.0", { width: 1480 }), cell("94.2", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("4", { width: 600 }), cell("Sandoval", { width: 2600 }), cell("NM", { width: 1800 }),
      cell("97.2", { width: 1400 }), cell("91.1", { width: 1480 }), cell("94.1", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("5", { width: 600 }), cell("Adams", { width: 2600 }), cell("CO", { width: 1800 }),
      cell("92.0", { width: 1400 }), cell("95.6", { width: 1480 }), cell("93.8", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("6", { width: 600 }), cell("Chaves", { width: 2600 }), cell("NM", { width: 1800 }),
      cell("96.4", { width: 1400 }), cell("90.4", { width: 1480 }), cell("93.4", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("7", { width: 600 }), cell("Utah", { width: 2600 }), cell("UT", { width: 1800 }),
      cell("98.4", { width: 1400 }), cell("88.2", { width: 1480 }), cell("93.3", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("8", { width: 600 }), cell("Mesa", { width: 2600 }), cell("CO", { width: 1800 }),
      cell("92.6", { width: 1400 }), cell("93.3", { width: 1480 }), cell("92.9", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("9", { width: 600 }), cell("Santa Fe", { width: 2600 }), cell("NM", { width: 1800 }),
      cell("95.7", { width: 1400 }), cell("89.7", { width: 1480 }), cell("92.7", { width: 1480 }),
    ]}),
    new TableRow({ children: [
      cell("10", { width: 600 }), cell("Weber", { width: 2600 }), cell("UT", { width: 1800 }),
      cell("91.4", { width: 1400 }), cell("93.7", { width: 1480 }), cell("92.6", { width: 1480 }),
    ]}),
  ],
}));

// ===== POLICY RELEVANCE =====
sections.push(
  H1("Policy Relevance and Deliverables"),
  P("The project\u2019s target audience is state emergency-management agencies, rehabilitation networks, CMS, and the ASPR emPOWER program. The three deliverables are designed to be directly actionable at that policy layer:"),
  BULLET("A county-level vulnerability map naming the top-quartile counties on the convergent-risk index, suitable for publication and for use in state-level preparedness planning."),
  BULLET("A one-page policy brief written for emergency-management and rehabilitation audiences, summarizing the two risk pathways and recommending tele-rehabilitation and grid-hardening investment priorities consistent with Alexander & Alexander (2025)."),
  BULLET("A replicable analysis pipeline (public GitHub repository) that state agencies can re-run on updated CMS and FEMA data as new releases publish, without requiring a Data Use Agreement."),
);

// ===== TIMELINE =====
sections.push(
  H1("Timeline"),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1800, 3500, 4060],
    rows: [
      new TableRow({ tableHeader: true, children: [
        cell("Phase", { head: true, width: 1800 }),
        cell("Activity", { head: true, width: 3500 }),
        cell("Target delivery", { head: true, width: 4060 }),
      ]}),
      new TableRow({ children: [
        cell("Phase 1", { width: 1800 }),
        cell("National county-level convergent-risk analysis (six CMS covariates + FEMA NRI composite)", { width: 3500 }),
        cell("Complete \u2014 analysis-ready dataset, six choropleth maps, and one-page policy brief delivered", { width: 4060 }),
      ]}),
      new TableRow({ children: [
        cell("Phase 2", { width: 1800 }),
        cell("Sensitivity checks; cross-validation against HHS emPOWER; policy-brief publication; GitHub release", { width: 3500 }),
        cell("In progress \u2014 targeted for completion this grant cycle", { width: 4060 }),
      ]}),
      new TableRow({ children: [
        cell("Phase 3", { width: 1800 }),
        cell("International extension (WHO rehabilitation access + World Bank electricity access + IPCC regional projections)", { width: 3500 }),
        cell("Planned next cycle", { width: 4060 }),
      ]}),
    ],
  }),
);

// ===== LIMITATIONS =====
sections.push(
  H1("Known Limitations"),
  BULLET("HIPAA cell suppression: 5 counties in the emPOWER dataset have suppressed beneficiary counts (cells of 1\u201310) per CMS de-identification policy and are excluded from the analysis."),
  BULLET("Medicare-only coverage: the data captures Medicare fee-for-service and Medicare Advantage beneficiaries only; Medicaid-only, dual-eligible, and uninsured electricity-dependent individuals are not represented, likely underestimating total population at risk, particularly in younger disabled adults."),
  BULLET("FEMA data gaps: 81 counties (approximately 2.5% of the national total) have insufficient data across one or more FEMA NRI hazard categories and carry a null composite hazard score; these counties appear in the dataset but are excluded from the vulnerability rankings."),
  BULLET("Equal-weighting assumption: the convergent-risk index weights hazard exposure and power dependency equally. Empirically derived weights based on historical power-outage duration and disability-related mortality are a logical Phase 2 extension."),
  BULLET("Ecological unit: all findings describe county-level risk. Individual-level claims require the clinical study arm and are not made from this geospatial data."),
);

// ===== TEAM =====
sections.push(
  H1("Team"),
  P("Marcalee Alexander, MD \u2014 Principal Investigator. Marcus Neuroscience Institute, Baptist Health South Florida. Clinical expertise in spinal cord injury and climate-and-disability policy."),
  P("Barrett Jackson \u2014 Data analyst. Quantitative design, Python/geospatial implementation, and policy-brief authorship."),
);

// ===== REFERENCES =====
sections.push(
  H1("References"),
  P("Alexander M, Alexander J. The need for new paradigms to assess and respond to the impacts of climate change on disability. In: Climate Change and Disability: A Collaborative Approach to a Sustainable Future. Elsevier, 2025."),
  P("Alexander M, et al. A bellweather for climate change and disability. Spinal Cord Series and Cases. 2019."),
  P("Luyten J, et al. Health impact studies of climate change adaptation and mitigation measures \u2014 a scoping review. Journal of Climate Change and Health. 2023."),
  P("Federal Emergency Management Agency. National Risk Index, version 1.20, December 2025."),
  P("Centers for Medicare & Medicaid Services. Medicare Geographic Variation Public Use File and Medicare Monthly Enrollment, December 2025."),
  P("US Department of Health and Human Services, ASPR. emPOWER Map. Accessed March 2026."),
);

// ===== ASSEMBLE DOC =====
const doc = new Document({
  creator: "Alexander Lab",
  title: "Grant Overview and Proposal \u2014 Electricity-Dependent Disability and Climate Hazard Convergence",
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Calibri", color: "8B1A1A" },
        paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Calibri", color: "1A1A1A" },
        paragraph: { spacing: { before: 220, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({
            text: "Alexander Lab  \u2022  Climate-Disability Risk",
            font: "Calibri", size: 18, color: "888888",
          })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", font: "Calibri", size: 18, color: "888888" }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Calibri", size: 18, color: "888888" }),
            new TextRun({ text: "  \u2022  April 2026 draft", font: "Calibri", size: 18, color: "888888" }),
          ],
        })],
      }),
    },
    children: sections,
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(OUT, buffer);
  console.log("Wrote:", OUT, buffer.length, "bytes");
});
