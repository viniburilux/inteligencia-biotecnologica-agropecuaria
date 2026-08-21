from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = datetime.now(timezone.utc).isoformat()


def sha256(rel: str) -> str | None:
    path = ROOT / rel
    if not path.exists() or path.is_dir():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(*paths: str) -> list[dict]:
    return [{"path": p, "sha256": sha256(p)} for p in paths]


def cycle(
    cycle_id: str,
    mode: str,
    state_before: dict,
    signal: str,
    why: str,
    question: str,
    sources: list[str],
    result: str,
    interpretation: str,
    decision: str,
    next_question: str | None,
    ev: list[dict],
    limits: str,
) -> dict:
    return {
        "cycle_id": cycle_id,
        "timestamp": STAMP,
        "mode": mode,
        "state_before": state_before,
        "signal": signal,
        "why_signal_deserves_exploration": why,
        "question_generated": question,
        "sources_chosen": sources,
        "result": result,
        "operational_interpretation": interpretation,
        "decision": decision,
        "next_question": next_question,
        "evidence": ev,
        "limits": limits,
        "state_update": "Evidence appended to the experiment record; historical corpus remains reproducible and the autonomous baseline is frozen at 763 works.",
    }


cycles: list[dict] = []

cycles.append(cycle(
    "H0", "historical_reconstruction",
    {"corpus_works": 379, "state_artifact": "EXPLORATORY_RADIOGRAPHY_V0.md"},
    "The initial corpus was large enough to show recurring organisms, actors and application terms, but not yet organized as an investigation map.",
    "A radiography was the smallest operation capable of converting a collection into explicit signals and candidate questions.",
    "What structures, hubs, organisms and gaps are visible in the 379-record corpus?",
    ["local corpus", "EXPLORATORY_RADIOGRAPHY_V0.md"],
    "Radiography V0 produced 20 derived queries and an execution path for a second round.",
    "The first adaptive move was not retrieval; it was changing the state representation from records to signals and questions.",
    "continue",
    "Execute the first blocks whose signals combine organism, process, application and local context.",
    evidence("EXPLORATORY_RADIOGRAPHY_V0.md", "next_queries_v0.json", "RADIOGRAPHY_METHOD_V0.md"),
    "The V0 radiography is an operational artifact; it does not prove that the clusters represent real technological systems.",
))

cycles.append(cycle(
    "H1", "historical_reconstruction",
    {"corpus_works": 379, "active_state": "V0 radiography + 20 questions"},
    "V0 exposed four actionable blocks: Trichoderma processes, microbial nitrogen/phosphate platform, local bioinput production/quality and an unexpected carbon/algae corridor.",
    "The blocks were supported by different terms and actors, so testing them in parallel had higher information value than choosing one narrative.",
    "Do the four blocks open patent families or literature, and which one has the densest local or industrial signal?",
    ["Google Patents", "OpenAlex"],
    "Nine patent queries and one OpenAlex contrast query were executed. Patent capture produced 76 occurrences and 50 unique identifiers; OpenAlex returned 25 works. The conservative merged state became 429 records, 97 patent records, 1,499 actors, 381 institutions, 2,093 relations and 313 application signals.",
    "The loop learned that Trichoderma linked to industrial fermentation, Pivot Bio concentrated nitrogen/phosphate/formulation, local bioinput production formed a compact Brazilian corridor, and the carbon/algae signal was unexpected but worth preserving.",
    "continue_and_expand",
    "Use the newly visible actors, organisms and technical terms to generate expansion queries rather than repeating the original blocks.",
    evidence("SECOND_ROUND_INGESTION_SUMMARY_V0.md", "SECOND_ROUND_PLAN_V0.json", "SECOND_ROUND_PATENT_FINDINGS_V0.md", "normalized_v0/"),
    "Google Patents results were metadata/snippet captures; the BR filter is context, not proof of Brazilian origin or adoption.",
))

cycles.append(cycle(
    "H2", "historical_reconstruction",
    {"corpus_works": 429, "active_state": "four tracks with actors and technical terms"},
    "The second round exposed recurring actors and process terms: USP, Embrapa, Simple Agro, Solubio, Pivot Bio, Locus, Novozymes, Petrobras, bioractor, fermentation, polymer, stability and quality monitoring.",
    "Expansion by actor, organism and process tests whether a signal survives when its original wording changes.",
    "Can the observed tracks be expanded through specific actors, organisms, technologies and application bridges?",
    ["Google Patents", "OpenAlex"],
    "The expansion manifests recorded 11 OpenAlex and 13 Google Patents entries in expansion_v1, followed by 4 OpenAlex and 17 Google Patents entries in expansion_v2. The subsequent cumulative normalization used these manifests and the V1 follow-up batch.",
    "The intelligence moved from term co-occurrence to navigation rules: use identifiers when names fail, translate terms when language blocks recovery, separate portfolios when a hub is noisy, and follow unexpected bridges instead of deleting them.",
    "continue_to_radiography",
    "Freeze the expanded cumulative state and let a new radiography choose the next 17 questions.",
    evidence("EXPANSION_QUERIES_V1.json", "EXPANSION_QUERIES_V2.json", "ingestion_manifest_v1.jsonl", "ingestion_manifest_v2.jsonl", "EXPANSION_PROFILE_V1.json", "EXPANSION_PROFILE_V2.json"),
    "The exact post-dedup count immediately after expansion_v1 is not published as a separate state. The next closed cumulative state is 763 works.",
))

cycles.append(cycle(
    "H3", "historical_reconstruction",
    {"corpus_works": 763, "actors": 2680, "institutions": 767, "relations": 4045, "application_signals": 536},
    "The cumulative state showed dense corridors and gaps: Trichoderma was the most recurrent organism; local production joined bioractor, fermentation, on-farm production and quality; Pivot Bio and Locus formed international hubs; Petrobras/algae remained narrow.",
    "A radiography over the expanded state can convert recurrence and gaps into ranked questions, while preserving weak or surprising signals.",
    "Which actor, organism, technology or application relation deserves the next query, and which formulation should be reformulated if it fails?",
    ["Google Patents", "OpenAlex"],
    "Seventeen queries were executed: 14 direct and 3 reformulated. Q02, Q04 and Q12 were insufficient in their first form and opened records after reformulation. The patent batch captured 36 occurrences across 30 unique records; the OpenAlex follow-up captured 50 works.",
    "The strongest adaptive behavior was query repair from evidence: CMRP 4490 replaced a failed Embrapa/Bacillus formulation; Portuguese bioinput/fermentation/property terms replaced a dead Solubio query; microalga/cascalho de perfuração/biofixação/fertilizante reopened the carbon trail.",
    "update_state_and_resolve_entities",
    "Normalize the cumulative evidence, resolve only safe aliases and preserve ambiguous names separately.",
    evidence("EXPLORATORY_RADIOGRAPHY_V1.md", "next_queries_v1.json", "RADIOGRAPHY_V1_QUERY_EXECUTION.json", "RADIOGRAPHY_V1_EXECUTION_SUMMARY.md", "RADIOGRAPHY_V1_PATENT_FINDINGS.md"),
    "A result count is a retrieval signal, not evidence of technological unity, performance, adoption, validity or freedom to operate.",
))

cycles.append(cycle(
    "H4", "historical_reconstruction",
    {"corpus_works": 763, "raw_relations": 4045, "raw_application_signals": 536},
    "The expanded corpus contained aliases, recurring names and cross-source collisions that could create false bridges.",
    "The loop needs a conservative identity step before treating recurring actors or institutions as connected entities.",
    "Which names can be safely unified, which remain candidates, and which must stay separate?",
    ["normalized corpus", "entity-resolution rules"],
    "The entity-resolution artifact records safe aliases, candidate groups and names deliberately kept separate. The normalized state remains 763 works, 2,680 actors, 767 institutions, 4,045 relations and 536 application signals.",
    "Entity resolution is part of the adaptive behavior because it changes what counts as a valid next signal without pretending that string similarity is identity.",
    "freeze_baseline",
    "Use the normalized state as the control state for an autonomous exploration; do not merge new autonomous results into it during the test.",
    evidence("ENTITY_RESOLUTION_V1.json", "normalized_v2/normalization_summary_v2.json"),
    "This is conservative normalization, not external authority verification of every entity.",
))

cycles.append(cycle(
    "A0", "autonomous_experiment",
    {"corpus_works": 763, "signals": {"fungo": 186, "biocontrole": 94, "fermentacao_bioprocesso": 89, "fixacao_nitrogenio": 26, "saude_radicular": 26, "solubilizacao_fosfato": 12, "nematoide": 32, "soja": 17, "milho": 20}},
    "The autonomous analyzer found high-value co-occurrences not identical to the four historical tracks: fungo–nematoide–soja, fixação de nitrogênio–saúde radicular–milho, fungo–solubilização de fosfato, and saúde radicular–solubilização de fosfato.",
    "These bridges combine high recurrence with an application or mechanism and were not simply copied from the user's priority list.",
    "Which of these bridges opens a new evidence-backed path when searched independently?",
    ["normalized_v2 works, relations and application signals", "Google Patents", "OpenAlex"],
    "Four autonomous branches were opened in parallel: fungal biocontrol/nematode/soybean; microbial nitrogen fixation/root health/maize; Trichoderma/phosphate/root health; and the carbon/algae residue bridge as a negative-control-like branch.",
    "The autonomous behavior began from the state representation itself, not from a user-selected track.",
    "continue_in_parallel",
    "Execute one patent and one bibliographic question per branch, then repair or park each branch based on evidence.",
    evidence("asie_autonomy_state_v0.json", "normalized_v2/normalization_summary_v2.json"),
    "The branches are hypotheses for navigation, not scientific conclusions.",
))

cycles.append(cycle(
    "A1", "autonomous_experiment",
    {"branch": "fungal_biocontrol_nematode_soybean", "source": "Google Patents"},
    "The state contained 23 works with fungo–nematoide, 9 with fungo–soja and 10 with biocontrole–nematoide.",
    "The combination is dense enough to test, but its English formulation may be lexically unstable in the Brazilian patent index.",
    "Does fungal biocontrol of nematodes in soybean open a Brazilian patent corridor?",
    ["Google Patents, BR filter"],
    "English query returned 465 results with high noise. Portuguese reformulation returned 32 results and surfaced BR112019020483A2, a microbial and biorational plant-nematode control family with Trichoderma and Bacillus combinations.",
    "Language was an active retrieval variable. The result did not validate a soybean-specific corridor, but it converted a noisy bridge into a concrete family and a next identifier-level question.",
    "reformulate_then_deepen",
    "Inspect BR112019020483A2 and contrast its organism/application claims with literature.",
    evidence("asie_autonomous_browser_findings_v0.md"),
    "The family page is metadata only; no efficacy, Brazilian origin, exclusivity or adoption is inferred.",
))

cycles.append(cycle(
    "A2", "autonomous_experiment",
    {"branch": "BR112019020483A2", "prior_decision": "reformulate_then_deepen"},
    "The Portuguese result exposed a stable family identifier and named actors, organisms and application modes.",
    "An identifier is more precise than repeating a broad lexical query and can expose the structure of the signal.",
    "What does the surfaced family actually connect: organism, application, formulation or use mode?",
    ["Google Patents family page"],
    "BR112019020483A2 was associated with Advanced Biological Marketing; the visible summary named Gary Harman, Molly Cadle-Davidson and Walid Nosir and described Trichoderma strains/combination microbes, root colonization, seed/foliar use, pest/disease resistance and formulation stability language.",
    "The adaptive unit is not the query result alone; it is the transition from lexical search to family inspection, where a next search can be generated from observed identifiers and attributes.",
    "deepen_by_literature_and_related_families",
    "Search the surfaced species/pathogen pair and keep the Brazil-specific patent question separate from the broader literature corridor.",
    evidence("asie_autonomous_browser_findings_v0.md"),
    "The visible family summary is not a full-text legal or technical analysis.",
))

cycles.append(cycle(
    "A3", "autonomous_experiment",
    {"branch": "fungal_biocontrol_nematode_soybean", "source": "OpenAlex", "prior_signal": "A1/A2 family attributes"},
    "The first bibliographic query returned 3,550 works and a direct title on Trichoderma citrinoviride and Meloidogyne incognita.",
    "A direct species/pathogen title is more informative than the broad result count and gives a new query anchor.",
    "Does the species/pathogen pair form a coherent literature corridor, and does it reappear in Brazilian patents?",
    ["OpenAlex", "Google Patents, BR filter"],
    "A01R using `Trichoderma citrinoviride Meloidogyne incognita` returned 95 OpenAlex works with the direct study in the first position. The follow-up patent query with the same pair and BR returned no results.",
    "The bridge is supported bibliographically but blocked as a Brazil-specific patent corridor under this formulation. This is a useful asymmetry, not a failure: literature can support a mechanism while the patent search remains insufficient.",
    "deepen_literature; park_BR_patent_branch",
    "Keep the literature branch available for a later organism/application comparison; do not continue Brazil patent expansion without a new anchor.",
    evidence("asie_autonomous_openalex_findings_v0.md", "asie_autonomous_openalex_reformulations_findings_v0.md", "asie_autonomous_browser_findings_v0.md"),
    "No result in one patent formulation is not proof of absence from all patent families.",
))

cycles.append(cycle(
    "A4", "autonomous_experiment",
    {"branch": "microbial_nitrogen_fixation_root_health_maize", "source": "OpenAlex"},
    "The state contained 9 works with fixação de nitrogênio–saúde radicular and 6 with inoculante–milho.",
    "The bridge links a nutrient mechanism to an application context and is independent of the Pivot Bio narrative.",
    "Is there a focused literature corridor for plant-growth-promoting rhizobacteria, nitrogen fixation and maize under an explicit experimental context?",
    ["OpenAlex"],
    "The broad query returned 13,618 works dominated by generic rhizosphere literature. Reformulation to `plant growth promoting rhizobacteria nitrogen fixation maize greenhouse` returned 6,737 works and surfaced a direct maize greenhouse inoculation study plus a stable PGPR commercialization corridor.",
    "The signal survived reformulation but remains broad. The correct operational use is to treat it as a literature background and generate a future organism/field-specific query, not as evidence of a single platform.",
    "maintain_as_background; future_narrowing",
    "Next useful narrowing would require an organism or Brazilian field/crop anchor; no further broad query was executed in this cycle.",
    evidence("asie_autonomous_openalex_findings_v0.md", "asie_autonomous_openalex_reformulations_findings_v0.md"),
    "Large OpenAlex result counts measure retrieval breadth, not scientific relevance or commercialization.",
))

cycles.append(cycle(
    "A5", "autonomous_experiment",
    {"branch": "fungal_biocontrol_nematode_plant_root_colonization", "source": "OpenAlex"},
    "The state contained 28 works with fungo–biocontrole, 23 with fungo–nematoide and 8 with fungo–saude radicular.",
    "This is the densest autonomous bridge with a clear organism/mechanism/application interpretation.",
    "Can the broad fungal bridge be narrowed to Trichoderma and root-knot nematode biocontrol without losing the signal?",
    ["OpenAlex"],
    "The broad query returned 8,842 works and mixed PGPR, Bacillus, AMF and Trichoderma. Reformulation to `Trichoderma root knot nematode biocontrol` returned 3,763 works with direct titles on Trichoderma harzianum, Meloidogyne javanica/incognita and biocontrol mechanisms.",
    "This was the strongest autonomous literature path. It converged with the patent family found through the independent A1 branch, but the convergence is only a cross-source navigation signal, not proof of one technology or product.",
    "deepen",
    "Compare the species, pathogen, formulation and application attributes of the literature corridor with BR112019020483A2 and local Bacillus/Trichoderma records.",
    evidence("asie_autonomous_openalex_findings_v0.md", "asie_autonomous_openalex_reformulations_findings_v0.md", "asie_autonomous_browser_findings_v0.md"),
    "No full texts were downloaded; the result is metadata-level convergence.",
))

cycles.append(cycle(
    "A6", "autonomous_experiment",
    {"branch": "Trichoderma_phosphate_root_health", "source": "Google Patents"},
    "The state contained 7 works with fungo–solubilizacao_fosfato and 6 with fixacao_nitrogenio–solubilizacao_fosfato, while root health co-occurred with phosphate six times.",
    "This bridge was not a preselected historical track; it connects organism, nutrient acquisition and plant application.",
    "Does the Trichoderma–phosphate–root-health bridge identify a common technical portfolio?",
    ["Google Patents, BR filter"],
    "The query returned 384 results. The first page exposed Locus families on root health/immunity, yeast/rhizosphere and carbon, and a Pivot Bio family on phosphate solubilization.",
    "The query found a portfolio-level bridge, not a single Trichoderma platform. Locus and Pivot Bio must remain separate actors; the useful output is a new contrast question about portfolio architecture.",
    "keep_as_separate_portfolios",
    "Contrast Locus root/rhizosphere/carbon families with Pivot phosphate/nitrogen families in a future actor-centered pass.",
    evidence("asie_autonomous_browser_findings_v0.md"),
    "The broad query did not isolate Trichoderma; do not infer organism ownership from co-occurrence.",
))

cycles.append(cycle(
    "A7", "autonomous_experiment",
    {"branch": "microalgae_drilling_waste_biofixation_fertilizer", "source": "OpenAlex"},
    "The historical carbon bridge was narrow but surprising, and the current state contained only 5 sequestro_carbono signals.",
    "A low-density unexpected bridge is worth one independent contrast before it is parked.",
    "Does the patent bridge have a matching literature corridor involving algae, drilling waste and fertilizer in Brazil?",
    ["OpenAlex"],
    "The initial query returned only 18 works, mostly generic algae/CO2 capture and CCUS. Reformulation to `algae drilling cuttings fertilizer Brazil` returned 227 works, but the top titles concerned produced-water treatment, drill-cuttings reuse for construction and generic energy/water topics; no direct algae–drill-cuttings–fertilizer–Brazil chain appeared in the visible top results.",
    "The autonomous process preserved the surprising patent signal but stopped treating it as a growing corridor when the independent literature route failed to add a direct bridge.",
    "park",
    "Resume only if a new institutional, residue-specific or application-specific anchor appears in later corpus updates.",
    evidence("asie_autonomous_openalex_findings_v0.md", "asie_autonomous_openalex_reformulations_findings_v0.md", "EXPLORATION_CYCLE_V1_SUMMARY.md"),
    "The park decision is based on this query path, not a claim that no related literature exists.",
))

cycles.append(cycle(
    "A8", "autonomous_experiment",
    {"branch": "microbial_nitrogen_fixation_root_health_maize", "source": "Google Patents"},
    "The OpenAlex branch produced a direct maize/PGPR study but an extremely broad retrieval universe.",
    "A patent result can reveal a named actor or composition that literature alone does not expose.",
    "Does microbial nitrogen fixation plus root health plus maize open an identifiable BR patent family independent of Pivot Bio?",
    ["Google Patents, BR filter"],
    "The query returned one visible family, BR112020022643A2, associated with Locus Agriculture IP Company, LLC, on microbe-based products for plant root health and immunity.",
    "This keeps the Locus branch independent from Pivot Bio and turns a low-density patent result into an actor-centered next question rather than a generic continuation.",
    "deepen_actor_contrast",
    "Compare Locus root-health/rhizosphere families with Pivot phosphate/nitrogen families and with the OpenAlex PGPR/maize corridor.",
    evidence("asie_autonomous_browser_findings_v0.md"),
    "One visible result is a weak signal; it is not a market or technical maturity assessment.",
))

cycles.append(cycle(
    "A9", "autonomous_experiment",
    {"corpus_works": 763, "autonomous_raw_state": "raw_v3/asie_autonomous", "baseline_frozen": True},
    "The autonomous branches produced convergences, negative results and portfolio separations, but no new evidence justified merging into the public normalized corpus during the test.",
    "The experiment must preserve the control state; otherwise the result cannot be reconstructed as behavior from a fixed input.",
    "What should be updated in the state after autonomous exploration, and what should remain pending?",
    ["local evidence artifacts", "hashes", "autonomous logs"],
    "Raw patent and OpenAlex outputs were stored under `raw_v3/asie_autonomous/`; the baseline `normalized_v2` corpus was not modified. The next state is an evidence queue with branch decisions, not a new scientific corpus release.",
    "The machine's current useful unit is a provenance-preserving exploration queue: state snapshot, signal, query, result, decision and next question. The adaptive behavior is real as a process, but not yet a standalone runnable engine.",
    "close_v0; propose_next_architectural_test",
    "A future test should compare this adaptive queue against a fixed-query strategy on the same frozen state; no ASIE architecture should be built before that comparison.",
    evidence("asie_autonomy_state_v0.json", "asie_autonomous_browser_findings_v0.md", "asie_autonomous_openalex_findings_v0.md", "asie_autonomous_openalex_reformulations_findings_v0.md"),
    "This cycle did not measure wall-clock time, false-candidate rate or fixed-strategy recall; it is evidence of behavior, not a benchmark.",
))

# Write machine log.
log_path = ROOT / "ASIE_CYCLE_LOG_V0.jsonl"
with log_path.open("w", encoding="utf-8") as f:
    for row in cycles:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

# Build behavior document.
behavior = f"""# ASIE_BEHAVIOR_V0

**Status:** reconstrução empírica do comportamento adaptativo observado no laboratório agropecuário.

**Data do artefato:** {STAMP}

## Escopo

Este documento não cria o ASIE e não altera o núcleo privado do OI. Ele trata o laboratório agropecuário como um experimento já executado e reconstrói o comportamento adaptativo que apareceu entre estado, sinal, decisão, pergunta, execução, resultado e atualização de estado.

O ponto de partida do teste autônomo foi o estado cumulativo congelado em **763 obras metadata-only**, com 2.680 atores normalizados, 767 instituições, 4.045 relações observadas e 536 sinais de aplicação. O corpus-base não foi alterado durante a exploração autônoma. As novas evidências ficaram em `raw_v3/asie_autonomous/`.

## A sequência observada

| Fase | Estado | Sinal | Decisão | Atualização observada |
|---|---|---|---|---|
| V0 | 379 registros | Recorrências ainda sem mapa operacional | Construir radiografia | 20 perguntas derivadas |
| Segunda rodada | 379 registros + radiografia V0 | Quatro blocos: Trichoderma, nutrientes microbianos, produção local e carbono/alga | Executar blocos em paralelo | 429 registros e quatro trilhas mais concretas |
| Expansões | 429 registros | Atores, organismos e processos recorrentes | Expandir por entidades e termos, não repetir consultas | Novos lotes V1/V2; estado cumulativo fechado depois em 763 obras |
| Radiografia V1 | 763 obras | Hubs, organismos, aplicações, lacunas e queries insuficientes | Executar 17 queries, reformular três e preservar estados mortos | Famílias, literatura, proveniência e resolução conservadora |
| Teste autônomo | 763 obras congeladas | Coocorrências escolhidas pelo estado, não pelo usuário | Abrir quatro ramos, reparar consultas e estacionar trilhas fracas | Evidence queue em `raw_v3/asie_autonomous/` |

## Operadores adaptativos que apareceram

### 1. Radiografar antes de buscar novamente

A primeira mudança não foi uma query. Foi transformar registros em sinais, relações, clusters e lacunas. A radiografia converteu um corpus em uma superfície de decisão. Esse operador aparece nos artefatos V0 e V1 e é o que permite gerar perguntas que não estavam na lista inicial.

### 2. Usar densidade como prioridade, não como conclusão

`fungo`, `biocontrole` e `fermentacao_bioprocesso` eram sinais densos. Coocorrências como fungo–nematoide, fungo–soja e fixação de nitrogênio–saúde radicular foram usadas para abrir perguntas. A densidade escolheu onde olhar; ela não foi usada para afirmar que existia uma plataforma tecnológica única.

### 3. Reformular consultas mortas com termos observados

A busca Embrapa–*Bacillus velezensis*–biorreator falhou e foi substituída por `CMRP 4490`. A busca Solubio em inglês falhou e foi substituída por termos brasileiros de bioinsumo, fermentação, produção e propriedade rural. A busca ampla de microalgas e resíduos foi substituída por microalga, cascalho de perfuração, biofixação e fertilizante. Esse é um comportamento adaptativo explícito: o resultado negativo altera a próxima pergunta.

### 4. Trocar palavras por identificadores

Quando `BR112019020483A2` apareceu na busca em português, a exploração abriu a página da família. A unidade de trabalho mudou de combinação lexical para identificador, ator, organismo, uso e atributo de formulação. Esse salto não seria recuperado repetindo a mesma consulta ampla.

### 5. Seguir pontes inesperadas sem colapsar as entidades

Trichoderma levou a biocontrole, soforolipídeos, fermentação, celulase e enzimas. Petrobras levou a microalgas, biofixação de CO₂, cascalho de perfuração e fertilizante. Na exploração autônoma, Trichoderma–fosfato–saúde radicular levou a Locus e Pivot Bio, mas a decisão foi manter os portfólios separados.

### 6. Manter trilhas paralelas

O teste autônomo não escolheu entre fungos, nutrientes, rizosfera e carbono. Abriu quatro ramos e aplicou a mesma lógica de recuperação, reparo e decisão a cada um. O resultado foi assimétrico: Trichoderma–nematoide ganhou prioridade, Locus/Pivot virou contraste de portfólio, e o corredor carbono foi estacionado.

### 7. Tratar ausência como atualização de estado

A consulta patentária `Trichoderma citrinoviride Meloidogyne incognita Brazil` não encontrou resultados. A literatura para a mesma espécie/pathógeno foi densa. O estado atualizado não é “a tecnologia não existe”; é “a ponte é bibliográfica sob esta formulação e está bloqueada como corredor patentário brasileiro”.

### 8. Parar sem apagar

A trilha algas–resíduos–fertilizante recebeu uma busca inicial e uma reformulação. A reformulação abriu literatura de água produzida e reaproveitamento de cascalho, mas não uma cadeia direta até fertilizante no topo observado. A decisão foi estacionar, preservar os artefatos e exigir uma nova âncora antes de gastar mais consultas.

## Onde está a inteligência adaptativa

A inteligência não está em uma função isolada. Ela aparece na **transição entre estados**. O padrão observado é:

> **estado → leitura de sinais → escolha de uma pergunta informativa → execução → leitura do resultado → reparo, bifurcação, aprofundamento ou estacionamento → novo estado**

A parte mais forte é a escolha da próxima representação do problema. O pipeline troca `nome de ator` por `identificador`, `inglês` por `português`, `organismo` por `processo`, `consulta ampla` por `família`, e `trilha surpreendente` por `contraste independente`.

A parte ainda fraca é a formalização. As decisões foram reproduzíveis por artefatos e scripts, mas ainda dependeram de lógica distribuída entre radiografia, leitura de resultados, parser, resolução de entidades e decisão operacional. Portanto, a evidência atual sustenta **comportamento ASIE distribuído**, não um motor ASIE pronto.

## Resultado do teste de autonomia

O teste encontrou evidência **positiva, mas não definitiva**, de que a exploração adaptativa abre caminhos que uma estratégia fixa provavelmente não abriria: o salto para a família BR112019020483A2 veio de uma reformulação linguística; o salto para *Trichoderma citrinoviride* e *Meloidogyne incognita* veio de um título bibliográfico retornado pela própria busca; a consulta Trichoderma–fosfato separou Locus de Pivot Bio; e a trilha de carbono foi estacionada após uma busca independente não acrescentar a ponte esperada.

Isso ainda não é um benchmark contra uma estratégia fixa. Não foram medidos, neste V0, tempo, falsos candidatos, recall de uma estratégia fixa, retrabalho ou taxa de decisões bloqueadas. O próximo teste arquitetural informativo é comparar, no mesmo estado congelado, **perguntas fixas pré-definidas** contra **perguntas adaptadas pelos resultados**, mantendo fontes e orçamento comparáveis.

## Referências

[1]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/EXPLORATION_CYCLE_V1_SUMMARY.md "Resumo do ciclo exploratório V1"

[2]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/RADIOGRAPHY_V1_QUERY_EXECUTION.json "Registro computável da Radiografia V1"

[3]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/ENTITY_RESOLUTION_V1.json "Resolução conservadora de entidades V1"

[4]: https://patents.google.com/patent/BR112019020483A2/en "Google Patents — BR112019020483A2"

[5]: https://api.openalex.org/works?search=Trichoderma%20citrinoviride%20Meloidogyne%20incognita "OpenAlex — Trichoderma citrinoviride / Meloidogyne incognita"

[6]: https://patents.google.com/?q=(Trichoderma+citrinoviride+Meloidogyne+incognita+Brazil)&country=BR "Google Patents — espécie/pathógeno com filtro BR"
"""
(ROOT / "ASIE_BEHAVIOR_V0.md").write_text(behavior, encoding="utf-8")

# Build autonomous exploration document.
autonomous = f"""# AUTONOMOUS_EXPLORATION_V0

**Data:** {STAMP}  
**Baseline:** 763 obras metadata-only, congeladas durante o teste.  
**Regra:** nenhuma trilha foi escolhida por instrução do usuário; as perguntas foram geradas a partir do estado computável, dos sinais, das lacunas e do histórico de resultados.

## Pergunta do experimento

> A partir do estado atual do laboratório, a exploração autônoma consegue escolher perguntas, abrir trilhas, reformular consultas mortas, seguir pontes inesperadas e abandonar direções que não ganham evidência?

O objetivo não foi provar que o ASIE funciona. Foi observar se o comportamento adaptativo encontra caminhos que não seriam produzidos por repetição mecânica das queries anteriores.

## Estado usado para decidir

| Elemento | Valor observado |
|---|---:|
| Obras | 763 |
| Atores normalizados | 2.680 |
| Instituições | 767 |
| Relações | 4.045 |
| Sinais de aplicação | 536 |
| Sinais de maior frequência | fungo 186; biocontrole 94; fermentação/bioprocesso 89; inoculante 73; bioinsumo 70 |
| Coocorrência escolhida | fungo–nematoide 23; fungo–soja 9; fixação de nitrogênio–saúde radicular 9; fungo–solubilização de fosfato 7 |

## Trilhas escolhidas sem confirmação do usuário

O analisador abriu quatro ramos. O primeiro veio de fungo–nematoide–soja; o segundo de fixação de nitrogênio–saúde radicular–milho; o terceiro de fungo–solubilização de fosfato–saúde radicular; o quarto preservou o corredor carbono/alga como teste de baixa densidade e alto valor surpresa.

### Ramo A — fungo, nematoide e soja

A consulta patentária em inglês retornou 465 resultados com ruído. O próprio histórico do laboratório já mostrava que a linguagem podia ser decisiva, então a pergunta foi reformulada em português. A reformulação caiu para 32 resultados e expôs `BR112019020483A2`, associado à Advanced Biological Marketing, com combinações de Trichoderma e Bacillus e aplicações de controle de nematoides, colonização radicular e tratamento de sementes/foliar na descrição visível.

A máquina então mudou de busca lexical para inspeção de família. Em paralelo, a consulta OpenAlex ampla retornou 3.550 obras. Um título direto sobre *Trichoderma citrinoviride* e *Meloidogyne incognita* virou a próxima pergunta. A reformulação específica retornou 95 obras, com o estudo direto na primeira posição. Quando a mesma combinação foi levada ao Google Patents com filtro BR, o resultado foi **nenhum resultado**.

| Estado final do ramo | Decisão |
|---|---|
| Literatura específica sustentada; corredor patentário BR não confirmado nessa formulação | **Aprofundar literatura; estacionar a afirmação patentária brasileira** |

O que apareceu aqui e não estava na busca fixa original foi o par espécie–patógeno e o uso de um identificador de família como próximo passo. O que não apareceu foi uma confirmação brasileira específica, e isso foi preservado como bloqueio.

### Ramo B — fixação de nitrogênio, saúde radicular e milho

A busca OpenAlex inicial retornou 13.618 obras, dominadas por literatura geral de rizosfera. O sistema não aceitou o volume como evidência suficiente. A pergunta foi reformulada para PGPR, fixação de nitrogênio, milho e condição de casa de vegetação. A consulta ainda retornou 6.737 obras, mas trouxe um estudo direto sobre inoculação de milho, fixação de nitrogênio e remobilização de nitrogênio, além de um corredor bibliográfico estável sobre PGPR e comercialização de bioestimulantes.

A busca patentária independente abriu uma família visível, `BR112020022643A2`, associada à Locus Agriculture IP Company, sobre produtos microbianos para saúde e imunidade radicular. A decisão foi manter Locus separado de Pivot Bio. O ramo não foi abandonado; foi rebaixado de “plataforma” para “corredor de literatura + contraste de ator”.

| Estado final do ramo | Decisão |
|---|---|
| Sinal bibliográfico forte, mas amplo; uma âncora patentária de ator | **Manter como background e estreitar por organismo/cultura em ciclo posterior** |

### Ramo C — Trichoderma, fosfato e saúde radicular

A coocorrência fungo–solubilização de fosfato e saúde radicular não estava entre as quatro trilhas históricas fechadas. A consulta patentária retornou 384 resultados e revelou que a ponte atravessava famílias da Locus sobre saúde radicular, leveduras/rizosfera e carbono, além de uma família Pivot Bio sobre solubilização de fosfato.

A interpretação operacional foi deliberadamente não colapsar a ponte. O resultado diz “há uma arquitetura de portfólios e temas que se cruzam”; não diz “há uma tecnologia Trichoderma comum a Locus e Pivot”.

| Estado final do ramo | Decisão |
|---|---|
| Ponte de portfólio observada; organismo não isolado | **Aprofundar por ator, mantendo Locus e Pivot separados** |

### Ramo D — microalgas, resíduos de perfuração e fertilizante

O ramo de carbono foi mantido porque era inesperado e estreito. A consulta OpenAlex inicial retornou apenas 18 obras, principalmente sobre captura de CO₂ por algas e CCUS. A reformulação para `algae drilling cuttings fertilizer Brazil` retornou 227 obras, mas os títulos de topo se concentraram em tratamento de água produzida, reaproveitamento de cascalho para construção e tópicos genéricos de energia/água. Não apareceu no topo uma cadeia direta algas–cascalho–fertilizante–Brasil.

| Estado final do ramo | Decisão |
|---|---|
| Ponte patentária específica; literatura independente não adicionou a cadeia esperada | **Estacionar** |

A trilha não foi apagada. Ela aguarda uma nova âncora institucional, de resíduo ou de aplicação antes de consumir mais consultas.

## Registro das execuções autônomas

| Sequência | Pergunta/ação | Fonte | Resultado | Decisão |
|---|---|---|---|---|
| A1 | fungal biocontrol nematode soybean | Google Patents BR | 465 resultados, muito ruído | Reformular |
| A1R | fungo biocontrole nematoide soja | Google Patents BR | 32 resultados; família BR112019020483A2 | Inspecionar família |
| A1F | BR112019020483A2 | Google Patents | Atores, organismos, uso e formulação visíveis | Aprofundar |
| A2 | microbial nitrogen fixation root health maize | Google Patents BR | Família Locus BR112020022643A2 | Manter independente |
| A3 | Trichoderma phosphate solubilization root health | Google Patents BR | 384; Locus e Pivot separados | Contrastar portfólios |
| A01 | Trichoderma nematode root health soybean | OpenAlex | 3.550 obras | Reformular |
| A01R | T. citrinoviride M. incognita | OpenAlex | 95 obras; estudo direto no topo | Aprofundar literatura |
| A01P | T. citrinoviride M. incognita Brazil | Google Patents BR | Nenhum resultado | Estacionar ramo BR |
| A02 | microbial nitrogen fixation root health maize rhizosphere | OpenAlex | 13.618 obras, genérico | Reformular |
| A02R | PGPR nitrogen fixation maize greenhouse | OpenAlex | 6.737; estudo direto e corredor PGPR | Estreitar depois |
| A03 | fungal biocontrol nematode plant root colonization | OpenAlex | 8.842; mistura PGPR/Bacillus/AMF/Trichoderma | Reformular |
| A03R | Trichoderma root knot nematode biocontrol | OpenAlex | 3.763; títulos diretos e coerentes | Aprofundar |
| A04 | microalgae drilling waste biofixation fertilizer | OpenAlex | 18; literatura CCUS genérica | Reformular |
| A04R | algae drilling cuttings fertilizer Brazil | OpenAlex | 227; sem cadeia direta no topo | Estacionar |
| A5 | espécie/pathógeno específico no BR | Google Patents BR | Ausência observada | Preservar bloqueio |

## O que a autonomia realmente encontrou

Há três resultados fortes. Primeiro, **reparo por linguagem**: a busca portuguesa abriu uma família que a busca inglesa não isolou. Segundo, **reparo por entidade**: um título bibliográfico abriu a pergunta espécie–patógeno, e um resultado patentário abriu a inspeção por identificador. Terceiro, **separação de portfólios**: a ponte Trichoderma–fosfato–saúde radicular levou a Locus e Pivot, mas o processo manteve os atores separados.

Há também dois resultados negativos importantes. A consulta específica da espécie/pathógeno não encontrou uma família BR nessa formulação. E a reformulação bibliográfica do corredor carbono não encontrou a cadeia direta esperada. Esses bloqueios são parte do resultado do teste; sem eles, a autonomia seria apenas expansão de narrativa.

## Julgamento do experimento

O comportamento observado é **promissor como processo de exploração**, porque a próxima pergunta mudou com base no resultado anterior e porque diferentes ramos terminaram em decisões diferentes. A evidência é **insuficiente para afirmar vantagem mensurável sobre estratégia fixa**, pois este V0 não executou uma condição-controle com o mesmo orçamento, nem mediu tempo, falsos candidatos, recall, retrabalho ou completude de provenance em comparação direta.

A conclusão operacional é clara: **não construir o ASIE ainda**. O próximo experimento informativo é um teste A/B de estratégia fixa contra estratégia adaptativa, usando o mesmo snapshot de 763 obras, o mesmo orçamento de fontes e o mesmo formato de log. O ASIE só deve virar módulo depois de sabermos se as decisões adaptativas reduzem consultas inúteis, aumentam caminhos novos ou melhoram o tempo até uma próxima ação justificável.

## Proveniência e artefatos

O registro computável completo está em [`ASIE_CYCLE_LOG_V0.jsonl`](ASIE_CYCLE_LOG_V0.jsonl). O estado usado para seleção está em [`asie_autonomy_state_v0.json`](asie_autonomy_state_v0.json). As capturas patentárias estão em [`asie_autonomous_browser_findings_v0.md`](asie_autonomous_browser_findings_v0.md). As respostas OpenAlex estão em [`asie_autonomous_openalex_findings_v0.md`](asie_autonomous_openalex_findings_v0.md) e [`asie_autonomous_openalex_reformulations_findings_v0.md`](asie_autonomous_openalex_reformulations_findings_v0.md). Os resultados brutos autônomos permanecem sob `raw_v3/asie_autonomous/`.

## Referências

[1]: https://patents.google.com/patent/BR112019020483A2/en "Google Patents — BR112019020483A2"

[2]: https://patents.google.com/patent/BR112020022643A2/en "Google Patents — BR112020022643A2"

[3]: https://patents.google.com/?q=(fungo+biocontrole+nematoide+soja)&country=BR "Google Patents — busca em português"

[4]: https://api.openalex.org/works?search=Trichoderma%20citrinoviride%20Meloidogyne%20incognita "OpenAlex — espécie/pathógeno"

[5]: https://api.openalex.org/works?search=plant%20growth%20promoting%20rhizobacteria%20nitrogen%20fixation%20maize%20greenhouse "OpenAlex — PGPR/milho"

[6]: https://api.openalex.org/works?search=Trichoderma%20root%20knot%20nematode%20biocontrol "OpenAlex — Trichoderma/nematoide"

[7]: https://api.openalex.org/works?search=algae%20drilling%20cuttings%20fertilizer%20Brazil "OpenAlex — algas/cascalho/fertilizante"
"""
(ROOT / "AUTONOMOUS_EXPLORATION_V0.md").write_text(autonomous, encoding="utf-8")

print(json.dumps({
    "generated_at": STAMP,
    "cycles": len(cycles),
    "files": ["ASIE_BEHAVIOR_V0.md", "ASIE_CYCLE_LOG_V0.jsonl", "AUTONOMOUS_EXPLORATION_V0.md"],
    "baseline_frozen": True,
    "baseline_works": 763,
}, ensure_ascii=False, indent=2))
