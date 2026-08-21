import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "next_queries_v0.json"
OUTPUT = ROOT / "SECOND_ROUND_PLAN_V0.json"


def main():
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = payload["queries"]
    selected_ids = {"NQ01", "NQ02", "NQ04", "NQ05", "NQ06", "NQ07", "NQ08", "NQ09", "NQ10", "NQ14"}
    selected = [row for row in rows if row["query_id"] in selected_ids]
    selected.sort(key=lambda row: (row["block"], -row["priority_score"], row["rank"]))
    blocks = {
        "B1_trichoderma_transversal": {
            "decision": "executar_primeiro",
            "why": "Organismo com presença em cinco clusters operacionais; precisa separar produção, biocontrole e carbono.",
            "queries": [row["query_id"] for row in selected if row["block"] == "B1_trichoderma_transversal"],
        },
        "B2_nitrogen_platform": {
            "decision": "executar_primeiro",
            "why": "Cluster concentrado com fixação, liberação, formulação e fosfato; maior chance de revelar uma plataforma tecnológica coerente.",
            "queries": [row["query_id"] for row in selected if row["block"] == "B2_nitrogen_platform"],
        },
        "B3_local_production_quality": {
            "decision": "executar_primeiro",
            "why": "Sinal mais diretamente ligado à hipótese de capacidade brasileira: biorreatores, fermentação, produção on-farm e controle de qualidade.",
            "queries": [row["query_id"] for row in selected if row["block"] == "B3_local_production_quality"],
        },
    }
    execution_order = ["B1_trichoderma_transversal", "B2_nitrogen_platform", "B3_local_production_quality"]
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "next_queries_v0.json",
        "decision": "execute_selected_blocks_without_waiting",
        "selection_rule": "Top evidence-linked queries from B1/B2/B3; include one literature contrast query to test whether the patent signals have a scientific counterpart.",
        "execution_order": execution_order,
        "blocks": blocks,
        "selected_query_ids": [row["query_id"] for row in selected],
        "selected_queries": selected,
        "not_selected_now": [row["query_id"] for row in rows if row["query_id"] not in selected_ids],
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"selected": output["selected_query_ids"], "blocks": {key: value["queries"] for key, value in blocks.items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
