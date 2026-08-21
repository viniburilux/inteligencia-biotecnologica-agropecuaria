import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NEXT = ROOT / "next_queries_v1.json"
PATENT = ROOT / "radiography_patent_parser_summary_v1.json"
OPENALEX = ROOT / "radiography_followup_openalex_summary_v1.json"
OUT_JSON = ROOT / "RADIOGRAPHY_V1_QUERY_EXECUTION.json"
OUT_MD = ROOT / "RADIOGRAPHY_V1_EXECUTION_SUMMARY.md"

next_data = json.loads(NEXT.read_text(encoding="utf-8"))
patent_data = json.loads(PATENT.read_text(encoding="utf-8"))
openalex_data = json.loads(OPENALEX.read_text(encoding="utf-8"))
patent_queries = patent_data.get("queries", {})
openalex_queries = {row["query_id"].split("_", 1)[0].upper(): row for row in openalex_data.get("rows", [])}

rows = []
for item in next_data["queries"]:
    qid = item["query_id"]
    row = dict(item)
    execution = {"status": "not_found", "observed_result_count": None, "unique_records": None, "source_artifacts": []}
    if item["source"] == "google_patents":
        base = patent_queries.get(qid)
        reformulated = patent_queries.get(qid + "R")
        if reformulated and reformulated.get("status") == "captured":
            execution = {
                "status": "executed_reformulated",
                "original_status": (base or {}).get("status"),
                "reformulation": reformulated.get("query"),
                "observed_result_count": reformulated.get("observed_result_count"),
                "unique_records": reformulated.get("unique_records"),
                "source_artifacts": [reformulated.get("saved_path")],
            }
        elif base:
            execution = {
                "status": "executed",
                "observed_result_count": base.get("observed_result_count"),
                "unique_records": base.get("unique_records"),
                "source_artifacts": [base.get("saved_path")],
            }
    else:
        key = qid.upper()
        base = openalex_queries.get(key)
        if base:
            execution = {
                "status": "executed",
                "observed_result_count": base.get("observed_result_count"),
                "unique_records": base.get("returned_items"),
                "source_artifacts": [base.get("raw_path")],
            }
    row["execution"] = execution
    rows.append(row)

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source_query_file": "next_queries_v1.json",
    "metadata_only": True,
    "queries": rows,
    "summary": {
        "planned_queries": len(rows),
        "executed": sum(1 for r in rows if r["execution"]["status"] in {"executed", "executed_reformulated"}),
        "executed_direct": sum(1 for r in rows if r["execution"]["status"] == "executed"),
        "executed_reformulated": sum(1 for r in rows if r["execution"]["status"] == "executed_reformulated"),
        "insufficient_direct": sum(1 for r in rows if r["execution"]["status"] == "executed" and r["execution"]["unique_records"] == 0),
        "not_found": sum(1 for r in rows if r["execution"]["status"] == "not_found"),
    },
    "notes": [
        "Execution status is derived from browser-captured Google Patents metadata and OpenAlex metadata manifests.",
        "Reformulated queries are preserved as separate executions and do not erase the original insufficient result.",
        "No patent PDFs, full text, or scientific data were downloaded.",
    ],
}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# Radiography V1 — Query Execution Summary",
    "",
    "> This artifact links the 17 queries generated from the cumulative corpus to the searches actually executed. It is an execution log, not a conclusion about technology or market adoption.",
    "",
    f"Generated at: `{payload['generated_at']}`  ",
    f"Planned queries: **{payload['summary']['planned_queries']}**  ",
    f"Executed: **{payload['summary']['executed']}** — direct: {payload['summary']['executed_direct']}; reformulated: {payload['summary']['executed_reformulated']}  ",
    f"Not found in execution manifests: **{payload['summary']['not_found']}**",
    "",
    "| ID | Fonte | Trilha | Status | Volume observado | Registros retornados | Evidência operacional |",
    "|---|---|---|---|---:|---:|---|",
]
for row in rows:
    ex = row["execution"]
    artifacts = ", ".join(a for a in ex.get("source_artifacts", []) if a)
    evidence = artifacts or "sem artefato localizado"
    lines.append(f"| {row['query_id']} | {row['source']} | {row['block']} | {ex['status']} | {ex.get('observed_result_count') if ex.get('observed_result_count') is not None else '—'} | {ex.get('unique_records') if ex.get('unique_records') is not None else '—'} | `{evidence}` |")
lines += [
    "",
    "## Reformulações que abriram sinal",
    "",
    "Q02, Q04 e Q12 tiveram resposta insuficiente na formulação inicial. As reformulações foram preservadas separadamente: `Bacillus velezensis CMRP 4490 bioreactor Brazil`, `Solubio bioinsumo fermentação produção propriedade rural` e `microalga cascalho perfuração biofixação fertilizante`. As três abriram registros metadata-only, incluindo a família Petrobras de fertilizante organomineral com cascalho de perfuração e biomassa de algas.",
    "",
    "## Limites",
    "",
    "Um resultado recuperado por filtro BR é presença em uma busca de patentes com contexto brasileiro; não é prova suficiente de origem, titularidade brasileira, validade, adoção, desempenho agronômico ou liberdade de operação. As lacunas e páginas insuficientes permanecem registradas.",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(payload["summary"], ensure_ascii=False))
