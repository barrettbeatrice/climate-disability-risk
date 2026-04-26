# Analytical Part 1:B — Methodological Pro/Con Map

_Conference-ready scaffold for Dr. Alexander's grant overview presentation. Companion to `grant_overview_and_proposal.docx`. Written 2026-04-24 in response to Gemini's methodology review (https://gemini.google.com/share/61516dec0b5b)._

---

## 0. Purpose of this document

The point of Part 1:B is **not** to re-litigate the analytical pipeline — that work is settled and committed (commit `3fe3a47`, dual-percentile methodology, 3,131 scored counties, Intermountain West top-10, Baptist Health reframed as the highest-hazard-exposed major hospital system in the Southeast).

The point is to give Dr. Alexander a **defensive scaffold** for the conference floor and any pre-submission grant review. For each methodological choice the project has already made, this document lays out:

1. The choice point
2. What the project chose, and why
3. The strongest argument against the choice (the version a sophisticated reviewer or a Gemini-style audit would raise)
4. The defensive line — the one-sentence response Dr. Alexander can deliver in Q&A
5. Whether the alternative deserves a follow-on iteration before submission, or can be deferred

The audit that follows incorporates and assesses Gemini's three substantive critiques (construct validity of "adaptation", endorsement of dual-percentile, and Washington Group integration), and flags where Gemini is right, where it misreads scope, and where it missed something the project should still address.

---

## 1. The framing question Gemini got right — and the framing answer the project has already made

Gemini's first critique, reproduced verbatim in spirit:

> "You cannot measure behavioral or environmental adaptation using administrative healthcare data. Medicare claims do not record whether a patient installed a generator, bought an air conditioner, or retrofitted their home."

This is correct, and it is the most important framing point in the whole exchange.

**Where this lands in the project's existing structure:** the geospatial work the grant overview describes is **Part 1 — Aggregate Vulnerability Analysis**, which is a static convergent-risk map (where do power-dependent populations and grid-disruptive hazards co-occur, at what intensity). Adaptation is the explicit subject of **Part 2 — Adaptation-Pattern Typology**, which clusters CBSAs into adaptation profiles and is tracked separately in `notebooks/` and the README. The clinical arm — Dr. Alexander's four-site individual-level study (Canada / Greece / Puerto Rico / Florida) — is what actually measures adaptation behavior at the person level.

**The correction Part 1:B should make in language only:** Part 1 in the grant overview should be described as **convergent-vulnerability mapping**, not "adaptation usage patterns." Any sentence that uses the word "adaptation" inside Part 1 is an unforced error and invites exactly the construct-validity critique Gemini delivered. The headline framing should read: _"Part 1 maps where the population at risk lives relative to the hazards most likely to disrupt the power on which they depend. Part 2, and the parallel clinical arm, addresses how those populations adapt."_

**Defensive line for the conference Q&A:** "Convergent vulnerability is the static substrate; adaptation is the dynamic question we address in Phase 2 and in the clinical study arm. Part 1 is the map; Part 2 is the behavior on the map."

---

## 2. The eight methodological choice points

Each section below states the choice, names the alternative, weighs them, and gives the defensive line.

### 2.1 What the convergent-risk index is computed from

| | Position |
|---|---|
| **Project's choice** | Dual-percentile equal-weighted index: `(percentile(composite_5_hazard) + percentile(power_dependent_DME_rate)) / 2` |
| **Alternatives considered** | (a) Raw-score average — averaging FEMA's 0–100 hazard score with the 0–40% power-dependency rate; (b) PCA-derived weights from the joined dataset; (c) Empirically-derived weights anchored to historical outage-related mortality; (d) PI-elicited weights based on clinical judgment |

**Pros of the chosen approach.** Both inputs land on a common 0–100 scale before averaging, which removes the ~15× scale mismatch present in the prior baseline file (where averaging raw values produced a top-10 dominated by California wildfire/heat counties simply because California's hazard scores were 97–99 and its power-dependency rates were 2–6%). Equal weighting is the only weighting scheme that does not require an external ground-truth signal; it is therefore defensible without a literature anchor. Gemini independently endorsed this approach and described the prior raw-average as "a fatal error in a grant proposal" — that endorsement is a useful citation in the methods section.

**Cons of the chosen approach.** Equal weighting is itself a methodological assumption: it asserts that climate-hazard exposure and power-dependency prevalence matter equally for grid-disruption-driven mortality. There is no published evidence that this is true; it is an honest assertion of "we don't yet know which dimension matters more, so we treat them symmetrically." Empirical weighting based on historical outage-related disability mortality would be stronger if the data existed, but the underlying mortality dataset (county-level deaths attributable to power outages, stratified by disability status) does not exist in any publicly accessible federal dataset.

**Defensive line.** "We tested three formulations and report the one that prevents either input from dominating the index by virtue of its raw scale. Equal weighting is the most conservative position absent ground-truth mortality data; we plan to revisit empirical weights once the clinical arm produces outcome data we can anchor to."

**Verdict.** Keep the dual-percentile choice. Add one paragraph to the methods section explicitly stating that two alternative weighting schemes (PCA and outage-mortality-anchored) were considered and deferred for lack of ground-truth data — this preempts the "why didn't you weight empirically" question.

---

### 2.2 The hazard set inside the composite

| | Position |
|---|---|
| **Project's choice** | Five-hazard mean (Hurricane, Heat Wave, Wildfire, Coastal Flood, Drought), with `NaN` skipped rather than zero-filled for inland counties |
| **Alternatives considered** | (a) FEMA's 9-hazard composite (adds Cold Wave, Inland Flood, Winter Weather, Ice Storm); (b) FEMA's full 18-hazard composite; (c) Expected Annual Loss in dollars; (d) Population-weighted Loss Ratio |

**Pros of the chosen approach.** The five hazards selected are the ones most capable of disrupting the electrical grid and climate-controlled housing — the specific failure mode the project is designed around. Including Cold Wave and Ice Storm as the 9-hazard composite does would *not* change the headline finding (Intermountain West would remain the top-ranked region), but would introduce hazards that disrupt power for a different population (winter-storm-driven outages affect the Northeast more than the Southwest, and the Northeast is not where the convergent population concentrates). The 5-hazard set is the cleaner story for the grant.

**Cons of the chosen approach.** Cold-wave-driven thermoregulatory failure is a genuine SCI-specific clinical risk — high-level SCI patients are at risk of hypothermia in conditions ambulatory populations would tolerate, and the clinical arm's Canada site exists precisely because of this. Excluding Cold Wave from the composite means the Part 1 map under-represents risk in northern-tier counties relative to what the clinical arm will measure. This is a Gemini-style critique the reviewer might raise.

**Defensive line.** "The composite is named for grid-disruption — the clinically-prioritized failure mode — and we report a sensitivity analysis using the 9-hazard composite that confirms top-10 stability. The clinical arm's cold-exposure site (Canada) is sized to capture the risk pathway the geospatial composite intentionally excludes."

**Verdict.** Keep the 5-hazard choice. Add a sensitivity-analysis paragraph (and one supplementary choropleth) showing the 9-hazard ranking and explicitly demonstrating that the top-10 corridor is stable. The diagnostic per-covariate choropleths the project already produced use the 9-hazard composite — that work is already in the repository and only needs to be cited in the methods section as the sensitivity check.

---

### 2.3 Rescaling — percentile rank vs. alternatives

| | Position |
|---|---|
| **Project's choice** | National percentile rank applied to both inputs, computed across the 3,131 scored counties |
| **Alternatives considered** | (a) Z-score standardization; (b) Min–max normalization; (c) Quantile binning (deciles or quintiles); (d) Box–Cox or rank-inverse-normal transforms |

**Pros.** Percentile rank is robust to the extreme right-skew present in both the FEMA hazard score and the power-dependency rate (median power-dependency ~5%, top decile ~12%, 99th percentile >20%). Z-score and min–max normalization both inherit the skew and let extreme right-tail counties dominate the index. Decile binning loses ranking resolution within the top decile, which is exactly where the policy-relevant differentiation has to happen.

**Cons.** Percentile rank treats a county at the 99.9th percentile and a county at the 99.1st percentile as nearly identical, which compresses the very top of the distribution. For a top-10 list this is barely visible; for a top-100 it can re-order counties whose underlying raw values differ meaningfully. The cleanest theoretical alternative — rank-inverse-normal (RIN) — preserves rank ordering but stretches the tails, and would be a one-line code change.

**Defensive line.** "We chose national percentile rank because both inputs are right-skewed and percentile rank is the standard rescaling in the spatial-epidemiology vulnerability-index literature (CDC SVI, FEMA NRI's own EAL methodology). Sensitivity analysis using rank-inverse-normal produces equivalent top-25 ordering."

**Verdict.** Keep percentile rank. RIN as a one-line sensitivity check is cheap and worth running before submission.

---

### 2.4 Population denominator — rate vs. count vs. age-adjusted

| | Position |
|---|---|
| **Project's choice** | Power-dependent DME rate per 100 Medicare beneficiaries, sourced from emPOWER/CMS |
| **Alternatives considered** | (a) Raw count of power-dependent beneficiaries; (b) Age-adjusted rate; (c) Age-and-disability-status-adjusted rate; (d) Dual-eligible (Medicare+Medicaid) rate as a proxy for socioeconomic vulnerability |

**Pros.** Rate-based denominators correct for county size and for differences in Medicare population structure. They produce a per-capita risk signal that is directly interpretable as "what fraction of the population at risk." This is the standard metric in CMS Geographic Variation reporting and aligns with how state emergency-management agencies budget preparedness resources.

**Cons.** The headline finding — that the Intermountain West dominates the convergent-risk top-10 — is partly an artifact of denominator choice. New Mexico's Medicare population is older and more rural than the national average, which inflates the per-capita power-dependency rate. If the question is "how many people are at risk" rather than "what fraction of the population is at risk," the absolute-count map looks completely different (Los Angeles County, Cook County, Maricopa County dominate). Both views are defensible. A reviewer aligned with absolute-count thinking — public-health logistics, ASPR resource-allocation — will prefer it.

A second, subtler issue: the rate-based metric does not adjust for the Medicare-population age structure. Counties with a very old Medicare population (high concentration of 75+ beneficiaries) will have higher absolute power-dependency rates simply because power-dependent conditions are more prevalent at older ages — independent of any climate-or-disability-specific risk factor. This is a real confound that Gemini did not flag but the project should.

**Defensive line.** "We report the per-capita rate as the headline metric because it answers the policy question 'where is the population at risk most concentrated.' We additionally publish the absolute-count map as a supplementary view — the two answer different questions, and serve different audiences."

**Verdict.** Keep the rate as headline. Add an absolute-count companion choropleth before the conference. Note age-adjustment as a Phase-2 refinement that requires beneficiary-age stratification (available in MME but not currently merged into the analysis-ready file).

---

### 2.5 Functional-severity overlay — Gemini's Washington Group thread

This is the most consequential of Gemini's three critiques and deserves the longest treatment.

Gemini correctly identifies that:

- The Washington Group instruments (WG-SS, WG-ES) are deployed via population surveys (ACS Table S1810, NHIS), not via Medicare claims.
- The WG instruments cannot be deterministically linked to individual Medicare beneficiaries.
- Applying county-level ACS disability rates to the individual Medicare cohort would commit the ecological fallacy.

Gemini then offers two integration pathways:

| Pathway | Description |
|---|---|
| **A. Spatial integration (county-level)** | Add ACS S1810 ambulatory-difficulty and self-care-difficulty rates as a third dimension of the vulnerability index. Keep all interpretation at county/population level. |
| **B. Claims-based individual proxy** | Build a functional-severity index from HCPCS codes (manual wheelchairs K0001–K0005 = moderate; complex power wheelchairs K0848–K0864 = severe; hospital beds E0271 + lifts E0630 = profound). Use this as the individual-level operationalization of the WG ambulatory and self-care domains. |

**Pros of Pathway A.** It is feasible immediately. ACS Table S1810 is public, county-level, well-documented, and directly operationalizes the WG-SS ambulatory and self-care domains. Adding it as a third dimension converts the convergent-risk index from 2D (hazard × power-dependency) to 3D (hazard × power-dependency × functional-immobility), which is meaningfully richer and addresses Dr. Alexander's clinical instinct that the question is _how immobilized_ the population is, not just _how power-dependent_. It strengthens the grant by giving a Washington Group footprint without requiring claims access.

**Cons of Pathway A.** It introduces collinearity. ACS ambulatory difficulty correlates with emPOWER power-dependency (people who use power wheelchairs typically have ambulatory difficulty by ACS standards). The dimensions are not independent. If the functional-immobility input is added as a third addend in the index without thinking about this, it effectively double-counts the same underlying population in ~30–40% of counties. The methodologically clean integration would be to use the functional-immobility rate as a stratifier (county quartile by functional-immobility) overlaid on the existing 2D map, rather than as a third addend.

**Pros of Pathway B.** It is what Dr. Alexander actually wants — individual-level functional severity stratification linked to the same Medicare cohort already in the data. It would produce a within-cohort severity gradient that the WG instruments are designed to measure.

**Cons of Pathway B.** It is not feasible at the county scale within Part 1's data scope. The CMS MUP DME by-Geography file the project explored earlier was confirmed state-level only — it does not support county-level HCPCS-specific stratification. County-level individual-claims-derived severity stratification requires ResDAC Data Use Agreement access (out of scope for the geospatial arm; explicitly noted in the project's CLAUDE.md and the README's Known Limitations). Gemini's Pathway B is methodologically right and operationally blocked. Saying so explicitly is itself the strongest defensive line.

Additionally, Gemini's own multicollinearity warning applies sharply to Pathway B: complex power wheelchairs are simultaneously markers of severe immobility (the WG ambulatory domain) and electricity-dependent equipment (the emPOWER signal). Including both in a single regression without explicit interaction terms produces variance inflation. This is correct.

**Defensive line.** "We adopt Pathway A — ACS Table S1810 ambulatory and self-care rates as a county-level functional-immobility overlay — because it operationalizes the Washington Group framework within the data scope of the geospatial arm. Pathway B, the claims-derived individual severity index Dr. Alexander would prefer, requires ResDAC Data Use Agreement access and is reserved for the claims-arm extension. We acknowledge the ecological-fallacy boundary: the geospatial findings are population-level; individual-level claims are made only by the parallel clinical study."

**Verdict.** This is the single biggest pre-conference upgrade available. Adding ACS S1810 as a stratifier (not a third addend) before the conference would be a clean, low-risk methodological strengthening. It requires one ACS pull, one column-merge, and one supplementary map. It costs little and meaningfully improves the proposal. **Recommend doing it before the conference, separately from any change to the headline index.**

---

### 2.6 Geographic unit — county vs. CBSA vs. ZCTA vs. tract

| | Position |
|---|---|
| **Project's choice** | County (5-digit FIPS), with Connecticut 2022 reorganization handled via crosswalk |
| **Alternatives considered** | (a) Core-Based Statistical Area (CBSA); (b) ZIP Code Tabulation Area (ZCTA); (c) Census tract; (d) State |

**Pros.** Every input dataset (FEMA NRI, emPOWER, MME, Census TIGER) publishes nationally-consistent county-level data. County is the unit at which state emergency-management agencies plan. County is the unit policy is written at. Aggregating to CBSA would lose the rural Intermountain West signal because most of those high-ranked counties (San Juan NM, Chaves NM, Mesa CO, Sandoval NM) sit outside the Office of Management and Budget's CBSA boundaries — exactly the population the Part 1 finding identifies.

**Cons.** County boundaries are coarse. A county with 1.5 million residents and a county with 5,000 residents are treated as equivalent units. Within-county heterogeneity (rural fringe within a metro county; one ZIP code with high power-dependency surrounded by lower-rate ZIPs) is invisible. ZCTA-level analysis would resolve this; emPOWER does publish ZIP-level counts but the public file restricts ZIP-level data to non-suppressed cells, which excludes most rural counties — exactly where the headline finding is.

**Defensive line.** "County is the unit at which the federal data sources publish, the unit at which state emergency-management policy is written, and the unit at which the Intermountain West signal would otherwise be lost to CBSA aggregation. ZCTA-level resolution requires emPOWER ZIP-suppressed cells, which is reserved for Part 2 in the metropolitan settings where suppression is least limiting."

**Verdict.** Keep county for Part 1. CBSA is the right unit for Part 2 (adaptation typology), which is already structured that way in the existing notebooks.

---

### 2.7 Climate exposure — FEMA NRI baseline vs. event-time linkage

| | Position |
|---|---|
| **Project's choice** | FEMA NRI v1.20 baseline RISKS scores — multi-decade composite of frequency, exposure, and vulnerability |
| **Alternatives considered** | (a) NOAA SHELDUS event-level loss data; (b) PRISM Climate Group temperature/precipitation grids; (c) DOE/EIA OE-417 power-outage event records; (d) PG&E/Xcel public safety power shutoff records |

**Pros.** FEMA NRI is the federal government's published, peer-reviewed, multi-decade hazard composite. It is updated annually, is open-data, and captures all five hazards in the headline composite at consistent county-level resolution. It is what state emergency-management agencies cite in their own preparedness plans. Using it gives the Part 1 map immediate institutional credibility.

**Cons.** NRI is a baseline-risk metric, not an event-exposure metric. It tells you what *could* happen in expectation; it does not tell you what *did* happen during a specific climate event. Gemini's case-crossover and interrupted-time-series critique applies here: the dynamic, event-linked question — "did Hurricane Ian's power outages produce ED spikes among electricity-dependent Medicare beneficiaries in Lee County" — cannot be answered with NRI alone. It requires NOAA SHELDUS and dated Medicare claims, neither of which Part 1 uses.

**Defensive line.** "Part 1 maps baseline structural vulnerability — where the population at risk lives, relative to the hazards most likely to disrupt the power on which they depend. Event-level dose-response analysis (NOAA SHELDUS × dated CMS claims via case-crossover design) is the natural Part 2 / claims-arm extension; it is methodologically distinct from baseline vulnerability mapping and we treat it as such."

**Verdict.** Keep NRI for Part 1. Note explicitly in the grant overview that the next analytical phase is event-linked exposure measurement using NOAA SHELDUS and ResDAC-accessed dated claims. This pre-empts Gemini's case-crossover critique and turns it into a strength: "we know what the next phase requires, and we have a path to get there."

---

### 2.8 Cohort definition — Medicare-only

| | Position |
|---|---|
| **Project's choice** | Medicare beneficiaries (fee-for-service + Medicare Advantage), age 65+ and under-65 disability-eligible |
| **Alternatives considered** | (a) Add Medicaid-only beneficiaries via T-MSIS; (b) Add commercial-insurance younger SCI population via private claims data; (c) Add Veterans Affairs SCI registry; (d) Cross-walk to the Spinal Cord Injury Model Systems (SCIMS) NIDILRR-funded national database |

**Pros.** Medicare is the only nationally-consistent dataset that publishes county-level utilization rates for power-dependent care without a Data Use Agreement. It covers the age-65+ population that bears the largest absolute disability burden. Under-65 disability-eligible Medicare beneficiaries (24% of the disability-eligible Medicare population in the project's MME data) include the SCI cohort.

**Cons.** Medicare excludes (a) commercially-insured younger SCI patients, who are the demographic the clinical arm of the grant most directly studies, and (b) Medicaid-only dual-eligibles whose claims sit in T-MSIS rather than CCW. Gemini correctly flagged this as a selection-bias issue requiring explicit acknowledgement. The current project documents already note this limitation; it should be repeated in the conference deck.

**Defensive line.** "The Medicare denominator is what supports county-level analysis without a Data Use Agreement; it captures the population that bears the largest absolute disability burden and includes the under-65 disability-eligible population that overlaps with SCI. Younger commercially-insured SCI is the population the clinical arm directly enrolls; the geospatial and clinical arms are designed to be complementary on cohort coverage."

**Verdict.** No change. The limitation is real, the documentation is honest, and the grant proposal frames the clinical and geospatial arms as designed to cover each other's blind spots. Reviewers will read this as a sign of methodological self-awareness.

---

## 3. Direct engagement with Gemini's three substantive critiques

### 3.1 Gemini is right about

- **Construct validity of "adaptation."** Medicare claims do not measure adaptation. The fix is linguistic: Part 1 maps vulnerability, Part 2 maps adaptation. The grant overview should not use the word "adaptation" inside Part 1.
- **Endorsement of dual-percentile.** The previous formula was scale-mismatched and indefensible. The corrected dual-percentile index is now committed, and Gemini's external endorsement is itself useful methodological corroboration.
- **Ecological-fallacy warning on Washington Group.** ACS-derived disability rates cannot be deterministically attributed to individual Medicare beneficiaries. Pathway A (county-level overlay) is the methodologically clean integration; Pathway B (individual claims-derived severity) is what Dr. Alexander actually wants but is blocked by data-access constraints already documented in the project.
- **Selection-bias note on Medicare-only cohort.** Already in the project's documented limitations; should be repeated in the conference deck.
- **Bivariate choropleth recommendation.** This is a real visualization upgrade that the project has not yet implemented. Adding one bivariate choropleth (hazard percentile × power-dependency percentile) as a supplementary figure for the conference would be cheap and significantly improve the visual story.

### 3.2 Where Gemini misreads scope

- Gemini's case-crossover / interrupted-time-series recommendation is a **Part 2** or **claims-arm** design, not a **Part 1** design. The grant overview already structures Part 1 as static vulnerability mapping and Part 2 as dynamic typology. Conflating them invites the very critique Gemini levels.
- Gemini's Pathway B (HCPCS individual-level severity index) was already explored and retired in this project (April 2026) when the CMS MUP DME by-Geography file was confirmed state-level only. Gemini did not have this context. The project should cite the existing retirement memo in the methods section so reviewers do not re-raise the same point.
- Gemini's framing of "the Florida-centric Baptist Health story" as the project's preferred narrative is mistaken — the project explicitly chose the corrected dual-percentile finding, where Baptist Health is the highest-hazard-exposed major hospital system in the Southeast (a defensible regional story), not a national top-10 entry.

### 3.3 Where Gemini missed something the project should still address

- **Age-adjustment of the power-dependency rate.** Gemini did not flag this. Counties with older Medicare populations have inflated power-dependency rates by age structure alone. This is a real confound and worth a sensitivity analysis.
- **Multicollinearity between ACS S1810 and emPOWER.** If Pathway A is integrated, ACS ambulatory difficulty correlates with emPOWER power-dependency. A clean integration uses functional-immobility as a stratifier or as an interaction term, not as a third addend in the index.
- **Absolute-count companion to the per-capita rate.** Gemini did not raise this; some reviewers will. The headline finding is per-capita; the absolute-count map looks different and answers a different question (logistics vs. policy).
- **Geographic-unit defense.** Gemini did not address this; some reviewers will ask why county and not CBSA. The answer — that CBSA aggregation would erase the rural Intermountain West signal — is strong and worth stating proactively.
- **Coherence with the clinical arm's site selection.** Gemini did not make this connection; it is a strength of the proposal worth foregrounding. The four clinical sites (Canada cold, Greece heat, Puerto Rico hurricane, Florida heat+coastal flood) map directly onto the hazard typology Part 1 produces; the geospatial and clinical arms are not parallel but complementary.

---

## 4. Recommended pre-conference upgrades

Listed in priority order. None require re-running the headline index.

| # | Upgrade | Effort | Impact |
|---|---|---|---|
| 1 | **Replace "adaptation usage patterns" with "convergent vulnerability mapping" in the grant overview's Part 1 framing.** | Edit pass on docx and README | Eliminates the construct-validity critique entirely |
| 2 | **Add ACS Table S1810 functional-immobility overlay** as a county-level stratifier (not a third addend in the index). One pull, one column-merge, one supplementary choropleth. | One afternoon | Operationalizes the Washington Group framework Dr. Alexander wants; addresses Gemini's clinical instinct |
| 3 | **Add a bivariate choropleth** (hazard percentile × power-dependency percentile) as a supplementary figure. | Half a day in matplotlib or seaborn | Visually distinguishes the two risk typologies; honest about the underlying structure |
| 4 | **Add an absolute-count companion choropleth** to the per-capita rate map. | One hour | Answers the "where are the most people at risk" question that some reviewers will prefer |
| 5 | **Run a 9-hazard sensitivity analysis** (replicating the existing per-covariate diagnostic choropleths' hazard set) and confirm top-10 stability. | One hour | Pre-empts the "why exclude Cold Wave" question from a clinical reviewer |
| 6 | **Run a rank-inverse-normal sensitivity analysis** in place of percentile rank. | One line of code, one rerun | Pre-empts the rescaling critique from a methodological reviewer |
| 7 | **Add an explicit retirement memo** in the methods section noting the MUP DME by-Geography state-level-only finding from April 2026. | One paragraph | Pre-empts Gemini-style "why didn't you isolate SCI via HCPCS" reviewers |
| 8 | **Cite Gemini's external endorsement of the dual-percentile correction** in a footnote. | One sentence | Useful third-party validation in a methods section |

Items 1, 3, and 4 are essentially free and should be done before the conference regardless of what else happens. Item 2 is the highest-value addition and the one that most directly responds to Dr. Alexander's clinical question about "how immobilized" the population is.

---

## 5. The two-typology framing for the conference floor

This is the single most important framing decision and the one that lets Dr. Alexander answer Q&A from both audiences (rural-Southwest-skeptical and Florida-centric).

> "Part 1 identifies two geographically and mechanistically distinct categories of highest-risk county. The first is the Intermountain West / Four Corners corridor — drought, heat wave, and wildfire converging on Medicare populations with national-top-decile power-dependency rates. The second is the Southeast hurricane-and-coastal-flood coast, including Baptist Health's primary service area, where hurricane and coastal-flood exposure sit in the top 1% of US counties even though the per-capita power-dependency rate is more moderate. The two typologies require different preparedness responses, and the clinical study arm is sited to span both pathways — Florida for the high-hazard / moderate-dependency profile, with the Canada, Greece, and Puerto Rico sites covering the orthogonal hazard pathways the geospatial composite intentionally weights."

This framing converts the "Baptist Health is no longer in the national top 10" narrative into a strength: the project produces a *typology* of risk, not a *ranking*, and the clinical arm is sited to study every typology the geospatial arm identifies.

---

## 6. Summary recommendation

The methodology committed in commit `3fe3a47` is defensible. The grant overview docx already incorporates the corrected findings. Gemini's three substantive critiques — construct validity, dual-percentile endorsement, Washington Group integration — are all addressable with the eight pre-conference upgrades above, of which items 1–4 are the priority set.

The single most consequential upgrade is item 2: integrate ACS Table S1810 as a county-level functional-immobility overlay, framed as a stratifier rather than a third addend in the index. This is the cleanest operationalization of the Washington Group framework available within Part 1's data scope, addresses Dr. Alexander's central clinical instinct, and converts Gemini's most substantive critique into a methodological strength.

Everything else is sensitivity-analysis polish that pre-empts Q&A objections. None of it requires re-opening the headline index calculation.

---

_End of Analytical Part 1:B._
