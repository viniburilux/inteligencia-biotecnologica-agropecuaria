from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "raw_v3" / "asie_autonomous" / "openalex_reformulations"
OUT = ROOT / "asie_autonomous_openalex_reformulations_findings_v0.md"
lines = ["# ASIE Autonomous OpenAlex Reformulations V0", "", "Metadata-only. Reformulações escolhidas pelos resultados das consultas A01–A03.", ""]
for path in sorted(SRC.glob("*.json")):
    p = json.loads(path.read_text(encoding="utf-8"))
    lines += [f"## {p.get('query_id')} — {p.get('query')}", "", f"- Universo observado: **{p.get('count')}** obras.", f"- Capturadas: **{len(p.get('results', []))}**.", f"- Sinal: {p.get('signal')}", f"- Motivo da reformulação: {p.get('decision_reason')}", "", "| # | Ano | Citações | Título | DOI/ID |", "|---:|---:|---:|---|---|"]
    for i, r in enumerate(p.get("results", [])[:12], 1):
        title = (r.get("title") or "").replace("|", "\\|")
        rid = r.get("doi") or r.get("id") or ""
        lines.append(f"| {i} | {r.get('publication_year') or ''} | {r.get('cited_by_count') or 0} | {title} | {rid} |")
    lines.append("")
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(OUT)
