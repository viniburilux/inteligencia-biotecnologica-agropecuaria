from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "raw_v3" / "asie_autonomous" / "openalex"
OUT = ROOT / "asie_autonomous_openalex_findings_v0.md"


def norm(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def names(result: dict) -> list[str]:
    vals = []
    for a in result.get("authorships") or []:
        author = (a.get("author") or {}).get("display_name")
        if author:
            vals.append(author)
        for inst in a.get("institutions") or []:
            if inst.get("display_name"):
                vals.append(inst["display_name"])
    return vals


def main():
    files = sorted(SRC.glob("*.json"))
    lines = ["# ASIE Autonomous OpenAlex Findings V0", "", "Metadata-only. Resultados capturados via API OpenAlex; não foram baixados PDFs.", ""]
    all_rows = []
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        qid = payload.get("query_id")
        lines += [f"## {qid} — {payload.get('query')}", "", f"- Universo observado pela API: **{payload.get('count')}** obras.", f"- Registros capturados: **{len(payload.get('results', []))}**.", f"- URL: `{payload.get('request_url')}`", ""]
        entity_counter = Counter()
        for r in payload.get("results", []):
            entity_counter.update(names(r))
        lines.append("| # | Ano | Citações | Título | DOI/ID |")
        lines.append("|---:|---:|---:|---|---|")
        for i, r in enumerate(payload.get("results", [])[:12], 1):
            title = (r.get("title") or "").replace("|", "\\|")
            rid = r.get("doi") or r.get("id") or ""
            lines.append(f"| {i} | {r.get('publication_year') or ''} | {r.get('cited_by_count') or 0} | {title} | {rid} |")
        lines += ["", "Entidades/afiliações mais recorrentes nos 25 primeiros registros:"]
        for ent, n in entity_counter.most_common(12):
            lines.append(f"- {ent}: {n}")
        lines.append("")
        all_rows.append({"query_id": qid, "query": payload.get("query"), "count": payload.get("count"), "captured": len(payload.get("results", [])), "entities": entity_counter.most_common(20)})
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "asie_autonomous_openalex_findings_v0.json").write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(OUT))


if __name__ == "__main__":
    main()
