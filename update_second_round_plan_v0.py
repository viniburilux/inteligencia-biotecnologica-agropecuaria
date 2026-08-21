import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
path = ROOT / "SECOND_ROUND_PLAN_V0.json"
plan = json.loads(path.read_text(encoding="utf-8"))
for item in plan.get("selected_queries", []):
    item["status"] = "executed"
plan["execution"] = {
    "status": "completed",
    "executed_at": "2026-08-21",
    "patent_queries_executed": ["NQ01", "NQ02", "NQ04", "NQ06", "NQ05", "NQ07", "NQ08", "NQ10", "NQ09"],
    "literature_queries_executed": ["NQ14"],
    "patent_parser_summary": "second_round_patent_parser_summary_v0.json",
    "literature_summary": "second_round_openalex_summary_v0.json",
    "patent_records_captured_across_queries": 78,
    "patent_records_unique_across_queries": 50,
    "literature_records_captured": 25,
    "normalization_summary": "normalized_v0/normalization_summary_v0.json",
    "unexpected_signals": [
        "Trichoderma fermentation connected to industrial cellulase/ethanol and Novozymes.",
        "Bioinput quality monitoring surfaced a CO2 biofixation/algae signal linked to Petrobras.",
        "Brazilian on-farm production, aseptic fermentation and bioreactor signals formed a compact local cluster."
    ]
}
path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(plan["execution"], ensure_ascii=False))
