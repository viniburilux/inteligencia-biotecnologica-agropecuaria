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

log_path = ROOT / "ASIE_CYCLE_LOG_V0.jsonl"
rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
if not any(row.get("cycle_id") == "A10" for row in rows):
    rows.append({
        "cycle_id": "A10",
        "timestamp": STAMP,
        "mode": "architecture_replay",
        "state_before": {
            "corpus_works": 763,
            "actors": 2680,
            "institutions": 767,
            "relations": 4045,
            "application_signals": 536,
            "baseline_sha256": sha256("asie_autonomy_state_v0.json"),
        },
        "signal": "The autonomous run generated result-dependent transitions, but V0 had not compared them with a fixed continuation under the same seed and step budget.",
        "why_signal_deserves_exploration": "The next architectural question is whether adaptation changes the investigation queue, rather than merely producing a different narrative after the fact.",
        "question_generated": "Under the same frozen state, same four seed queries and four post-seed steps, does a result-dependent policy produce more specific anchors and actionable decisions than a pre-committed fixed query list?",
        "sources_chosen": ["historical query pool", "ASIE autonomous evidence", "Google Patents", "OpenAlex"],
        "result": "The fixed replay produced 3 stable anchors, 2 actionable transitions, 0 reformulations and 0 explicit park/block decisions. The adaptive replay produced 6 stable anchors, 7 actionable transitions, 5 reformulations, 2 explicit park/block decisions and 4 branch-specific decisions.",
        "operational_interpretation": "The adaptive policy changed the search unit from broad terms to language variants, identifiers, species/pathogen pairs, experimental contexts and explicit branch decisions. The fixed policy continued broad pre-committed queries. This supports a process-level advantage in specificity and decision production for this replay, not a general superiority claim.",
        "decision": "preserve_behavior; do_not_build_module",
        "next_question": "Run a preregistered or otherwise frozen A/B trial with identical source budgets, explicit relevance labels, wall-clock time, false-candidate counts, provenance completeness and time to next justified action.",
        "evidence": [
            {"path": "ASIE_FIXED_ADAPTIVE_REPLAY_V0.md", "sha256": sha256("ASIE_FIXED_ADAPTIVE_REPLAY_V0.md")},
            {"path": "ASIE_FIXED_ADAPTIVE_REPLAY_V0.json", "sha256": sha256("ASIE_FIXED_ADAPTIVE_REPLAY_V0.json")},
            {"path": "next_queries_v1.json", "sha256": sha256("next_queries_v1.json")},
            {"path": "ASIE_CYCLE_LOG_V0.jsonl", "sha256": None},
        ],
        "limits": "This is a non-randomized process replay. The fixed and adaptive post-seed queries are not semantically identical, so the result concerns adaptive behavior and queue specificity, not answer quality or scientific truth.",
        "state_update": "The frozen corpus remains unchanged. A comparison artifact was added; the experiment state now contains both the autonomous queue and the fixed/adaptive replay result.",
    })
    log_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

behavior_path = ROOT / "ASIE_BEHAVIOR_V0.md"
behavior = behavior_path.read_text(encoding="utf-8")
old = """## Resultado do teste de autonomia

O teste encontrou evidência **positiva, mas não definitiva**, de que a exploração adaptativa abre caminhos que uma estratégia fixa provavelmente não abriria: o salto para a família BR112019020483A2 veio de uma reformulação linguística; o salto para *Trichoderma citrinoviride* e *Meloidogyne incognita* veio de um título bibliográfico retornado pela própria busca; a consulta Trichoderma–fosfato separou Locus de Pivot Bio; e a trilha de carbono foi estacionada após uma busca independente não acrescentar a ponte esperada.

Isso ainda não é um benchmark contra uma estratégia fixa. Não foram medidos, neste V0, tempo, falsos candidatos, recall de uma estratégia fixa, retrabalho ou taxa de decisões bloqueadas. O próximo teste arquitetural informativo é comparar, no mesmo estado congelado, **perguntas fixas pré-definidas** contra **perguntas adaptadas pelos resultados**, mantendo fontes e orçamento comparáveis.
"""
new = """## Resultado do teste de autonomia

O teste encontrou evidência **positiva, mas não definitiva**, de que a exploração adaptativa abre caminhos que uma estratégia fixa provavelmente não abriria: o salto para a família BR112019020483A2 veio de uma reformulação linguística; o salto para *Trichoderma citrinoviride* e *Meloidogyne incognita* veio de um título bibliográfico retornado pela própria busca; a consulta Trichoderma–fosfato separou Locus de Pivot Bio; e a trilha de carbono foi estacionada após uma busca independente não acrescentar a ponte esperada.

O replay comparável posterior usou o mesmo estado congelado, o mesmo prefixo de quatro perguntas e quatro passos pós-prefixo em cada braço. A continuação fixa produziu 3 âncoras estáveis, 2 transições acionáveis, nenhuma reformulação e nenhuma decisão explícita de estacionamento/bloqueio. A continuação adaptativa produziu 6 âncoras estáveis, 7 transições acionáveis, 5 reformulações, 2 decisões explícitas de estacionamento/bloqueio e 4 decisões específicas por ramo. O resultado favorece o comportamento adaptativo em **especificidade da fila de investigação e produção de decisões**, dentro desse replay.

Isso ainda não é um benchmark randomizado nem uma prova geral de superioridade. O replay usa uma lista fixa histórica e uma trilha adaptativa já observada; os dois braços não respondem exatamente às mesmas perguntas semânticas. Ainda não foram medidos, com critérios previamente congelados, tempo, falsos candidatos, recall, completude de provenance ou qualidade da resposta final. O próximo teste deve executar esses critérios com o mesmo orçamento e registro paralelo.
"""
if old not in behavior:
    raise SystemExit("behavior target paragraph not found")
behavior = behavior.replace(old, new)
behavior = behavior.replace("[6]: https://patents.google.com/?q=(Trichoderma+citrinoviride+Meloidogyne+incognita+Brazil)&country=BR \"Google Patents — espécie/pathógeno com filtro BR\"\n", "[6]: https://patents.google.com/?q=(Trichoderma+citrinoviride+Meloidogyne+incognita+Brazil)&country=BR \"Google Patents — espécie/pathógeno com filtro BR\"\n\n[7]: ASIE_FIXED_ADAPTIVE_REPLAY_V0.md \"Replay fixo versus adaptativo V0\"\n")
behavior_path.write_text(behavior, encoding="utf-8")

aut_path = ROOT / "AUTONOMOUS_EXPLORATION_V0.md"
aut = aut_path.read_text(encoding="utf-8")
insert_before = "## Proveniência e artefatos\n"
replay_section = """## Replay fixo versus adaptativo

Depois da exploração autônoma, foi executado um replay comparável no mesmo snapshot congelado. Os dois braços receberam o mesmo prefixo de quatro perguntas e quatro passos posteriores. O braço fixo seguiu uma continuação pré-comprometida do pool histórico; o braço adaptativo seguiu transições dependentes dos resultados já capturados.

| Métrica | Fixo | Adaptativo |
|---|---:|---:|
| Âncoras estáveis | 3 | 6 |
| Transições acionáveis | 2 | 7 |
| Reformulações | 0 | 5 |
| Decisões explícitas de estacionamento/bloqueio | 0 | 2 |
| Decisões específicas por ramo | 0 | 4 |

O resultado não prova que a estratégia adaptativa sempre vence. Ele mostra que, neste estado e neste replay, a política adaptativa mudou a unidade de investigação — idioma, identificador, espécie/pathógeno, contexto experimental e portfólio — enquanto a política fixa continuou consumindo consultas amplas. O artefato completo está em [`ASIE_FIXED_ADAPTIVE_REPLAY_V0.md`](ASIE_FIXED_ADAPTIVE_REPLAY_V0.md) e [`ASIE_FIXED_ADAPTIVE_REPLAY_V0.json`](ASIE_FIXED_ADAPTIVE_REPLAY_V0.json).

"""
if insert_before not in aut:
    raise SystemExit("autonomous insertion point not found")
aut = aut.replace(insert_before, replay_section + insert_before, 1)
aut = aut.replace("A conclusão operacional é clara: **não construir o ASIE ainda**. O próximo experimento informativo é um teste A/B de estratégia fixa contra estratégia adaptativa, usando o mesmo snapshot de 763 obras, o mesmo orçamento de fontes e o mesmo formato de log. O ASIE só deve virar módulo depois de sabermos se as decisões adaptativas reduzem consultas inúteis, aumentam caminhos novos ou melhoram o tempo até uma próxima ação justificável.", "A conclusão operacional permanece: **não construir o ASIE ainda**. O replay já mostrou uma diferença de processo favorável à adaptação, mas não mediu ainda tempo, falsos candidatos, recall, completude de provenance ou qualidade de resposta. O próximo passo é um A/B pré-congelado com esses critérios e orçamento comparável.")
aut = aut.replace("O registro computável completo está em [`ASIE_CYCLE_LOG_V0.jsonl`](ASIE_CYCLE_LOG_V0.jsonl).", "O registro computável completo está em [`ASIE_CYCLE_LOG_V0.jsonl`](ASIE_CYCLE_LOG_V0.jsonl). O replay fixo versus adaptativo está em [`ASIE_FIXED_ADAPTIVE_REPLAY_V0.md`](ASIE_FIXED_ADAPTIVE_REPLAY_V0.md) e [`ASIE_FIXED_ADAPTIVE_REPLAY_V0.json`](ASIE_FIXED_ADAPTIVE_REPLAY_V0.json).")
aut_path.write_text(aut, encoding="utf-8")

print(json.dumps({"updated": ["ASIE_CYCLE_LOG_V0.jsonl", "ASIE_BEHAVIOR_V0.md", "AUTONOMOUS_EXPLORATION_V0.md"], "cycles": len(rows)}, ensure_ascii=False))
