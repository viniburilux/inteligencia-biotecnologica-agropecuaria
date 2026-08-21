# Autonomous Patent-ASIE Cycle 001 — Executive Map Update

> **Status:** `OVERNIGHT_DRAFT` — public discovery artifact, not a legal, scientific, efficacy, market or investment conclusion.

## What the autonomous cycle did

Starting from commit `0a1e3316ddc5715ac05a9b2bd67b089d4cb25ae2` of the public repository, the cycle computed cross-cluster actor signals, technology terms, candidate patent–literature bridges and anomalies. It then allowed those signals to select reformulated searches rather than asking the user to choose a path. Searches were executed through OpenAlex, Crossref, rendered Google Patents pages and the UEL institutional repository. OpenAlex documents its `search` behavior across works, authors and institutions [1] [2]. Google describes its patent result pages as containing patent metadata and related document information [3] [4].

The cycle remained **metadata-only**. It did not download PDFs, full-text patent files, sequences or scientific datasets. Direct HTTP requests to Google Patents produced the same static application shell across queries, so that route was discarded as evidence and replaced with rendered-page capture.

## State transition

| Stage | State change | Artifact |
|---|---|---|
| Initial | 763 normalized works, 2,680 actors, 767 institutions, 4,045 observed relations and 536 application signals | `state_initial.json` |
| Frontier | 1,731 actor cross-cluster screening signals, 38 cross-context terms, 26 candidate bridge terms and 97 high-overlap records | `frontier_signals.json` |
| First test | Pivot Bio, USP, Trichoderma and Bacillus branches selected from the frontier | `questions_generated.json` |
| Reformulation | Actor identity and exact strain queries replaced broad topic-only searches | `reformulation_audit_v1.json`, `reformulation_audit_v2.json` |
| Convergence | The corpus led to a UEL multi-strain Bacillus corridor and a narrow USP Trichoderma bridge | `reformulation_audit_v3.json`, `browser_patent_findings.md` |
| Stop | Further gain now requires deliberate full-text/claim review or a larger collection decision | `state_final.json` |

## What changed in the map

### 1. USP–Trichoderma–sophorolipid continuity candidate

A rendered Google Patents search first exposed `BR102023003698A2`, filed by Universidade de São Paulo and centered on *Trichoderma harzianum* plus sophorolipids from *Starmerella bombicola* fermentation [5]. The direct page showed inventor Thiago Moura Rocha and the same technical combination in the abstract and claims-oriented text.

OpenAlex then returned the exact literature title **“Biocompatibility of Brazilian native yeast-derived sophorolipids and Trichoderma harzianum as plant-growth promoting bioformulations”**, with Thiago Moura Rocha as first author and USP affiliations [6]. Crossref independently confirmed the DOI, title, authors and journal metadata [7]. This is classified as **FACT — observed metadata/text continuity candidate**, not as proof that the article validates the patent or that the invention is effective or commercially adopted.

### 2. UEL–Bacillus–CMRP 4490 continuity candidate

The Bacillus branch produced `BR102024016682A2`, filed by Universidade Estadual de Londrina. The rendered patent page identifies *Bacillus velezensis* CMRP 4490, a stirred-tank bioreactor process, and bionematicide/inoculant formulation [8]. The page also explicitly refers to `TEIXEIRA et al., 2021`.

OpenAlex and Crossref independently identify the 2021 article **“Genomic Insights Into the Antifungal Activity and Plant Growth-Promoting Ability in Bacillus velezensis CMRP 4490”**, with UEL-associated authors including Gustavo Manoel Teixeira, Mirela Mosela and Admilton Gonçalves de Oliveira [9] [10]. The patent page lists Admilton Gonçalves de Oliveira Junior among the inventors. The name variation is preserved as a **same-name-variant identity candidate**, not silently normalized into a legal identity.

### 3. LABIM22 research-to-application corridor

Following Mirela Mosela led to `BR102020013481A2`, a UEL patent family whose direct page lists Mirela Mosela, Gustavo Manoel Teixeira and Admilton Gonçalves de Oliveira Junior among the inventors [11]. The patent concerns a *Bacillus velezensis* biofungicidal composition and a distinct strain, LABIM22.

The UEL repository then exposed a 2020 thesis titled **“Antagonismo da cepa LABIM22 de Bacillus velezensis frente a fungos fitopatógenos e biocontrole do mofo branco em sementes de soja”**, authored by AllanYukio Higashi [12]. Its public abstract links LABIM22 to genome analysis, in vitro antagonism, soybean-seed white-mold control and a medium described as being under a patent-in-process request. This is **FACT — observed public metadata/abstract continuity**, while LABIM22 remains distinct from CMRP 4490 and no strain identity has been merged.

## Epistemic classification

| Classification | Current content |
|---|---|
| **FACT** | Specific publication identifiers, titles, authors, applicants/assignees, dates, strain tokens and public abstracts/snippets observed in source records. |
| **INFERENCE** | A UEL-centered multi-strain team/institution corridor is visible across literature, institutional repository and patent metadata. |
| **HYPOTHESIS** | The map may contain a progression from strain characterization to formulation/bioreactor patenting; this is not yet established as a single project. |
| **OPPORTUNITY** | Full-text/claim review, patent-family/legal-event audit, alternate strain-name search and a larger UEL corridor analysis. |
| **DISCARDED** | Direct shell HTML as patent evidence, broad actor-count interpretation, duplicate language renderings as separate families, and any claim of efficacy/origin/validity/adoption. |

## Natural stop

The autonomous cycle stops at **state version 6** because it has reached two high-specificity cross-source continuity candidates and one multi-strain institutional corridor while remaining within the metadata-only discovery envelope. The next step would change the nature of the work: it would require deliberate full-text/claim review, broader source expansion, or a legal/technical interpretation decision. The machine therefore leaves the next questions in `next_questions.json` rather than choosing a new scope silently.

## References

[1]: https://help.openalex.org/api/ "OpenAlex API reference"  
[2]: https://help.openalex.org/api/searching/ "OpenAlex search documentation"  
[3]: https://patents.google.com/ "Google Patents"  
[4]: https://support.google.com/faqs/answer/7049724?hl=en "Google Patents result viewer"  
[5]: https://patents.google.com/patent/BR102023003698A2/en "BR102023003698A2"  
[6]: https://doi.org/10.1016/j.micres.2024.127689 "Trichoderma/sophorolipid literature article"  
[7]: https://api.crossref.org/works/10.1016%2Fj.micres.2024.127689 "Crossref record for Trichoderma/sophorolipid article"  
[8]: https://patents.google.com/patent/BR102024016682A2/en "BR102024016682A2"  
[9]: https://doi.org/10.3389/fmicb.2020.618415 "CMRP 4490 literature article"  
[10]: https://api.crossref.org/works/10.3389%2Ffmicb.2020.618415 "Crossref record for CMRP 4490 article"  
[11]: https://patents.google.com/patent/BR102020013481A2/en "BR102020013481A2"  
[12]: https://repositorio.uel.br/handle/123456789/18265 "UEL LABIM22 repository item"  
