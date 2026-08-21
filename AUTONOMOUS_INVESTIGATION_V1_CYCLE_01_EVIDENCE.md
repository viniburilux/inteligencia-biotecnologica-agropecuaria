# Autonomous Investigation V1 — Cycle 01 Evidence

## State and selection

- State: `AUTONOMOUS_INVESTIGATION_V1_STATE_0.json`
- Frontier: `AUTONOMOUS_INVESTIGATION_V1_FRONTIER_0.md`
- Selected anchor: *Bacillus velezensis* strain Ag75.
- Selection reason: concrete strain plus four applied signals (biocontrol, phosphate solubilization, growth promotion, maize/soybean), with a direct test of whether the bridge is isolated or opens a corridor.

## Patent query P01

- URL: `https://patents.google.com/?q=(%22Bacillus+velezensis%22+Ag75)&country=BR`
- Query: `"Bacillus velezensis" Ag75`
- Observed result: **No results found** in the BR filter.
- Interpretation: no Brazilian patent-family hit was found for the exact strain anchor in this query. This blocks a direct patent confirmation, but does not disprove the biological signal or patent activity under another identifier/wording.
- Provenance page text: `/home/ubuntu/page_texts/patents.google.com__q___22Bacillus_velezensis_22_Ag75__country_BR.md`

## Bibliographic query P02/P03

- Raw response: `raw_v4/autonomous_cycle_01_openalex.json`
- Summary: `/home/ubuntu/autonomous_investigation_v1_cycle1_openalex_summary.txt`
- Query P02: `"Bacillus velezensis" Ag75`
- Query P03: `Bacillus velezensis strain Ag75 phosphate solubilization maize soybean`
- OpenAlex reported `count=30` for each query; the top result in both was:
  - `Bacillus velezensis strain Ag75 as a new multifunctional agent for biocontrol, phosphate solubilization and growth promotion in maize and soybean crops`
  - 2022, DOI `10.1038/s41598-022-19515-8`
  - authors include Mirela Mosela and Galdino Andrade
  - affiliations include Universidade Estadual de Londrina and Universidade Estadual de Maringá
- Additional signal: the exact search also returned *Bacillus velezensis* Ag109, a 2024 complete-genome paper describing a biocontrol agent against plant-parasitic nematodes and *Sclerotinia sclerotiorum*, with Instituto Agronômico do Paraná and Universidade Estadual de Londrina.
- Interpretation: the Ag75 signal is not an isolated lexical hit. It is anchored in a specific bibliographic work and sits near a related strain/institution corridor. This creates a new, narrower question: whether the Ag75/Ag109/UEL-IAP corridor connects through strains, mechanisms, crops or institutions, rather than through the original broad phrase.

## Patent query P04

- URL: `https://patents.google.com/?q=(%22Bacillus+velezensis%22+Ag109)&country=BR`
- Query: `"Bacillus velezensis" Ag109`
- Observed result: **No results found** in the BR filter.
- Interpretation: the newly surfaced Ag109 signal also lacks an exact BR patent hit under the strain name. The next question should pivot to mechanism/crop/institution or a broader *Bacillus velezensis* patent family search, not repeat the exact strain query.
- Provenance page text: `/home/ubuntu/page_texts/patents.google.com__q___22Bacillus_velezensis_22_Ag109__country_BR.md`

## Cycle decision

- Decision: **reformulate / deepen**, not abandon.
- Reason: literature specificity increased and exposed a related strain and institutional corridor, while patent exact-name searches were blocked twice.
- Next question candidate: does the UEL–IAP *Bacillus velezensis* corridor connect Ag75 and Ag109 through the observed mechanisms (biocontrol, phosphate solubilization, plant growth, nematodes) or are they independent studies sharing only genus-level vocabulary?
- Candidate sources: OpenAlex for the institutional/strain corridor; Google Patents with mechanism/crop terms rather than exact strain names.
- No conclusion of common platform, commercial product, or patent relationship is made.

## Patent query P05 — reformulation by mechanism and crop

- URL: `https://patents.google.com/?q=(Bacillus+velezensis+phosphate+solubilization+biocontrol+maize+soybean)&country=BR`
- Query: `Bacillus velezensis phosphate solubilization biocontrol maize soybean`
- Observed result: **11 results** in the BR filter.
- Relevant surfaced families/records include:
  - `BR102020013481B1` — *BIOFUNGICIDAL COMPOSITION COMPRISING BACILLUS VELEZENSIS*, assignee Universidade Estadual de Londrina; strain lineage `LABIM22`.
  - `BR102024016682A2` — *Fermentation process in a bioreactor and formulations...*, associated with Universidade Estadual de Londrina; strain `Bacillus velezensis CMRP 4490`; metadata states a fermentative production process in a stirred-tank bioreactor for a bionematicide and/or inoculant.
  - `BR112019006915B1` — composition involving strain `RTI545`, with plant-growth and nematode/fungi control claims; assignee FMC Corporation.
  - `BR112017014053B1` — microbial compositions involving Bacillus strains for plant growth and disease treatment; assignee FMC Corporation.
- Observed assignees/facets include FMC Corporation, Universidade Estadual de Londrina, Simple Agro Sistemas Ltda, Monsanto Technology LLC and Auburn University.
- Interpretation: the exact Ag75/Ag109 name was not found in BR patents, but the mechanism/crop reformulation opened a specific Brazilian patent corridor around *Bacillus velezensis* strains, biocontrol, nematodes, inoculants and bioreactor/formulation. The new identifier `CMRP 4490` is a stronger next anchor than continuing to search Ag75 by exact name.
- Provenance page text: `/home/ubuntu/page_texts/patents.google.com__q__Bacillus_velezensis_phosphate_solubilization_biocontrol_maize_soybean__countr.md`
- Operational decision: **deepen by identifier** with `CMRP 4490`, while keeping Ag75/Ag109 as literature-side entities. Do not merge LABIM22, CMRP 4490, Ag75 or Ag109 without evidence.

## Patent query P06 — direct family inspection

- URL: `https://patents.google.com/patent/BR102024016682A2/en`
- Family: `BR102024016682A2`
- Title: *Fermentation process in a bioreactor and formulations for the development of a bionematicide and/or inoculant with Bacillus velezensis CMRP 4490*.
- Applicant: Universidade Estadual de Londrina.
- Named inventors shown on the page: Admilton Gonçalves de Oliveira Junior, Guilherme Gonçalves de Godoy, Maria Luiza Abreu Nicoletto, Daniel Vieira da Silva and João Paulo de Oliveira.
- Patent page states a stirred-tank bioreactor process with controls for agitation, temperature, pH, foam and dissolved oxygen, and formulations for bionematicide and/or inoculant use.
- The page also references prior CMRP 4490 work on antifungal activity, genomic features, soybean germination/growth, metabolite stability and biological control.
- Interpretation: the CMRP 4490 corridor is now supported by a direct patent family and a direct OpenAlex article. The result is stronger than a lexical bridge: the same strain identifier links a biological characterization literature record to a process/formulation patent record. This remains an observed linkage, not proof of commercialization, efficacy, market adoption or freedom to operate.
- Provenance page text: `/home/ubuntu/page_texts/patents.google.com_patent_BR102024016682A2_en.md`

## Cycle 2 decision

- Decision: **deepen once more through the strain-to-process bridge**, then evaluate whether a second independent corridor is required.
- Next question: does the direct CMRP 4490 literature describe the same antifungal/growth-promotion mechanisms referenced by the patent, and are CMRP 4489, Ag75 and Ag109 part of the same institutional research corridor or merely neighboring records?
- Candidate source: OpenAlex exact-title/DOI and institution/strain queries; no broad new collection.
