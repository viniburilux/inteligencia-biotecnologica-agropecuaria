from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = datetime.now(timezone.utc).isoformat()


def sha256(rel: str) -> str | None:
    p = ROOT / rel
    if not p.exists() or p.is_dir():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()

# The replay starts with the same four autonomous seed questions. The fixed arm
# then follows four pre-committed broad queries from the historical query pool,
# without reading the outcomes. The adaptive arm follows four result-dependent
# transitions from the autonomous log. This is a process replay, not a randomized
# benchmark and not a claim that the two arms had identical scientific coverage.
fixed = {
    "arm": "fixed",
    "initial_seed_queries": [
        "fungal biocontrol nematode soybean (Google Patents BR)",
        "microbial nitrogen fixation root health maize (Google Patents BR)",
        "Trichoderma phosphate solubilization root health (Google Patents BR)",
        "microalgae drilling waste biofixation fertilizer (OpenAlex)",
    ],
    "post_seed_queries": [
        {"query": "Trichoderma fermentation", "observed_count": 10},
        {"query": "Trichoderma biocontrol", "observed_count": 5},
        {"query": "microbial nitrogen fixation formulation", "observed_count": 1},
        {"query": "phosphate solubilization microbial", "observed_count": 1},
    ],
    "policy": "Continue the pre-committed list in order; do not reformulate from returned titles, identifiers or negative results.",
    "stable_anchors": ["Locus", "Pivot Bio", "generic CCUS/algae literature"],
    "actionable_transitions": [
        "contrast Locus and Pivot Bio",
        "keep carbon as a generic CCUS signal",
    ],
    "negative_or_park_decisions": 0,
    "reformulations": 0,
}

adaptive = {
    "arm": "adaptive",
    "initial_seed_queries": fixed["initial_seed_queries"],
    "post_seed_queries": [
        {"query": "fungo biocontrole nematoide soja", "transition": "reformulation from noisy English patent query"},
        {"query": "BR112019020483A2", "transition": "identifier-level family inspection"},
        {"query": "Trichoderma citrinoviride Meloidogyne incognita", "transition": "species/pathogen extracted from OpenAlex title"},
        {"query": "PGPR nitrogen fixation maize greenhouse", "transition": "narrowing of generic rhizosphere result"},
    ],
    "policy": "Read each result, repair or branch when the result provides a better anchor, preserve negative evidence, and stop a branch when the next query is not justified.",
    "stable_anchors": [
        "BR112019020483A2",
        "Trichoderma citrinoviride",
        "Meloidogyne incognita",
        "BR112020022643A2",
        "Locus",
        "Pivot Bio",
    ],
    "actionable_transitions": [
        "inspect BR112019020483A2",
        "compare species/pathogen literature with the surfaced family",
        "park the Brazil-specific species/pathogen patent branch",
        "narrow PGPR/nitrogen/maize by greenhouse context",
        "contrast Locus and Pivot portfolios",
        "deepen Trichoderma/root-knot-nematode literature",
        "park the carbon bridge after independent literature failure",
    ],
    "negative_or_park_decisions": 2,
    "reformulations": 5,
}

metrics = {
    "same_frozen_baseline": {
        "works": 763,
        "actors": 2680,
        "institutions": 767,
        "relations": 4045,
        "application_signals": 536,
        "state_sha256": sha256("asie_autonomy_state_v0.json"),
    },
    "same_seed_prefix": True,
    "fixed": {
        "seed_queries": len(fixed["initial_seed_queries"]),
        "post_seed_queries": len(fixed["post_seed_queries"]),
        "total_queries_in_replay": 8,
        "stable_anchor_count": len(fixed["stable_anchors"]),
        "actionable_transition_count": len(fixed["actionable_transitions"]),
        "negative_or_park_decision_count": fixed["negative_or_park_decisions"],
        "reformulation_count": fixed["reformulations"],
        "branch_specific_decisions": 0,
    },
    "adaptive": {
        "seed_queries": len(adaptive["initial_seed_queries"]),
        "post_seed_queries": len(adaptive["post_seed_queries"]),
        "total_queries_in_replay": 8,
        "stable_anchor_count": len(adaptive["stable_anchors"]),
        "actionable_transition_count": len(adaptive["actionable_transitions"]),
        "negative_or_park_decision_count": adaptive["negative_or_park_decisions"],
        "reformulation_count": adaptive["reformulations"],
        "branch_specific_decisions": 4,
    },
}

replay = {
    "artifact": "ASIE_FIXED_ADAPTIVE_REPLAY_V0",
    "generated_at": STAMP,
    "metadata_only": True,
    "design": "same frozen baseline + same four seed queries + four post-seed queries per arm",
    "interpretation": "The fixed arm follows a pre-committed historical query list; the adaptive arm follows result-dependent transitions already captured in the autonomous experiment.",
    "limits": [
        "This is not randomized.",
        "The fixed and adaptive post-seed queries are not semantically identical; the comparison concerns process behavior, not scientific answer quality.",
        "Observed counts are metadata retrieval counts, not relevance or efficacy.",
        "No full texts were downloaded.",
        "The replay uses already captured evidence; it does not claim a fresh independent trial.",
    ],
    "fixed_arm": fixed,
    "adaptive_arm": adaptive,
    "metrics": metrics,
    "evidence": [
        {"path": "asie_autonomy_state_v0.json", "sha256": sha256("asie_autonomy_state_v0.json")},
        {"path": "ASIE_CYCLE_LOG_V0.jsonl", "sha256": sha256("ASIE_CYCLE_LOG_V0.jsonl")},
        {"path": "next_queries_v1.json", "sha256": sha256("next_queries_v1.json")},
        {"path": "asie_autonomous_browser_findings_v0.md", "sha256": sha256("asie_autonomous_browser_findings_v0.md")},
        {"path": "asie_autonomous_openalex_findings_v0.md", "sha256": sha256("asie_autonomous_openalex_findings_v0.md")},
        {"path": "asie_autonomous_openalex_reformulations_findings_v0.md", "sha256": sha256("asie_autonomous_openalex_reformulations_findings_v0.md")},
    ],
}

(ROOT / "ASIE_FIXED_ADAPTIVE_REPLAY_V0.json").write_text(json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = f"""# ASIE_FIXED_ADAPTIVE_REPLAY_V0

**Data:** {STAMP}  
**Baseline:** snapshot congelado de 763 obras metadata-only.  
**Tipo:** replay comparável de processo, não benchmark randomizado.

## Por que este replay existe

O primeiro teste autônomo mostrou comportamento adaptativo, mas ainda não permitia dizer se esse comportamento acrescentava algo em relação a uma lista fixa. Por isso, foi feito um replay com o mesmo estado inicial e o mesmo prefixo de quatro perguntas autônomas. Depois do prefixo, cada braço recebeu quatro passos:

| Braço | Regra dos quatro passos posteriores |
|---|---|
| Fixo | Seguir quatro consultas pré-comprometidas do pool histórico, sem ler o resultado para escolher a seguinte. |
| Adaptativo | Ler o resultado e transformar título, identificador, ausência ou ruído em próxima pergunta. |

A comparação não mede quem responde melhor. Mede se o braço adaptativo transforma o mesmo orçamento de exploração em **mais transições operacionais**, **mais âncoras específicas** e **mais decisões explícitas de continuar, separar ou estacionar**.

## Resultado do replay

| Métrica | Fixo | Adaptativo |
|---|---:|---:|
| Perguntas no prefixo comum | 4 | 4 |
| Passos pós-prefixo | 4 | 4 |
| Perguntas totais do replay | 8 | 8 |
| Âncoras estáveis identificadas | {metrics['fixed']['stable_anchor_count']} | {metrics['adaptive']['stable_anchor_count']} |
| Transições acionáveis registradas | {metrics['fixed']['actionable_transition_count']} | {metrics['adaptive']['actionable_transition_count']} |
| Reformulações | {metrics['fixed']['reformulation_count']} | {metrics['adaptive']['reformulation_count']} |
| Decisões explícitas de estacionamento/bloqueio | {metrics['fixed']['negative_or_park_decision_count']} | {metrics['adaptive']['negative_or_park_decision_count']} |
| Decisões específicas por ramo | {metrics['fixed']['branch_specific_decisions']} | {metrics['adaptive']['branch_specific_decisions']} |

O prefixo comum é deliberadamente idêntico. A diferença aparece depois dele. O braço fixo continua consultando termos amplos do pool histórico: `Trichoderma fermentation`, `Trichoderma biocontrol`, `microbial nitrogen fixation formulation` e `phosphate solubilization microbial`. O braço adaptativo usa os próprios resultados para trocar a unidade de busca: `fungo biocontrole nematoide soja`, `BR112019020483A2`, `Trichoderma citrinoviride Meloidogyne incognita` e `PGPR nitrogen fixation maize greenhouse`.

## Leitura operacional

Neste replay, o braço adaptativo produziu o dobro de âncoras estáveis e mais transições acionáveis com o mesmo número total de passos. A diferença veio de operações observáveis: tradução da consulta, inspeção por identificador, extração de espécie e patógeno de um título, estreitamento por contexto experimental e decisões de estacionamento.

Isso é uma **evidência de comportamento**, não uma prova geral de superioridade. O braço fixo foi montado a partir do pool histórico e não é uma estratégia fixa ideal; o braço adaptativo também foi reconstruído a partir de um experimento já executado. O resultado autoriza uma conclusão mais limitada e mais útil:

> No estado agropecuário disponível, o comportamento adaptativo converteu o mesmo prefixo e o mesmo número de passos pós-prefixo em uma fila de investigação mais específica e com mais decisões explícitas do que a continuação fixa usada no replay.

## O que o replay não mede

O replay não mede eficácia agronômica, validade patentária, qualidade científica, liberdade de operação, adoção comercial ou verdade causal. Também não mede tempo de execução, falsos positivos ou recall contra um conjunto de verdade. Esses testes exigiriam um protocolo separado, com orçamento, critérios de relevância e avaliadores definidos antes da execução.

## Decisão

**Não construir o ASIE ainda.** O replay já mostra que existe um comportamento adaptativo que vale a pena preservar. Antes de transformá-lo em módulo, o próximo teste deve congelar, antecipadamente, uma lista fixa e uma política adaptativa, definir o que conta como âncora, próxima ação, falso candidato e bloqueio, e executar os dois braços com o mesmo orçamento e os mesmos critérios de avaliação.

## Proveniência

O estado-base e os hashes estão em [`ASIE_FIXED_ADAPTIVE_REPLAY_V0.json`](ASIE_FIXED_ADAPTIVE_REPLAY_V0.json). O histórico adaptativo está em [`ASIE_CYCLE_LOG_V0.jsonl`](ASIE_CYCLE_LOG_V0.jsonl). A lista fixa histórica está em [`next_queries_v1.json`](next_queries_v1.json). As capturas de resultados estão em [`asie_autonomous_browser_findings_v0.md`](asie_autonomous_browser_findings_v0.md), [`asie_autonomous_openalex_findings_v0.md`](asie_autonomous_openalex_findings_v0.md) e [`asie_autonomous_openalex_reformulations_findings_v0.md`](asie_autonomous_openalex_reformulations_findings_v0.md).

## Referências

[1]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/next_queries_v1.json "Pool histórico de queries V1"

[2]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/ASIE_CYCLE_LOG_V0.jsonl "Log computável ASIE V0"

[3]: https://patents.google.com/patent/BR112019020483A2/en "Família patentária BR112019020483A2"

[4]: https://api.openalex.org/works?search=Trichoderma%20citrinoviride%20Meloidogyne%20incognita "OpenAlex — espécie e patógeno"
"""
(ROOT / "ASIE_FIXED_ADAPTIVE_REPLAY_V0.md").write_text(md, encoding="utf-8")
print(json.dumps({"generated_at": STAMP, "files": ["ASIE_FIXED_ADAPTIVE_REPLAY_V0.md", "ASIE_FIXED_ADAPTIVE_REPLAY_V0.json"]}, ensure_ascii=False))
