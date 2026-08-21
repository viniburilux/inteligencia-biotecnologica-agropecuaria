import hashlib
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FINDINGS = ROOT / "EXPANSION_PATENT_FINDINGS_V2.md"
QUERIES = ROOT / "EXPANSION_QUERIES_V2.json"
RAW_DIR = ROOT / "raw_v2" / "google_patents_expansion"
MANIFEST = ROOT / "ingestion_manifest_v2.jsonl"
SUMMARY = ROOT / "expansion_patent_parser_summary_v2.json"

PATENT_ID_RE = re.compile(r"\bBR[A-Z0-9]+[ABU]\d\b")
SECTION_RE = re.compile(
    r"^##\s+(?P<qid>L\d+|I\d+|T\d+|C\d+)\s+—\s+(?P<label>[^\n]+)\n(?P<body>.*?)(?=^##\s+(?:L\d+|I\d+|T\d+|C\d+)\s+—\s+|\Z)",
    re.M | re.S,
)


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def clean(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[\`*_]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" \t\r\n;,.:()")


def observed_count(body):
    match = re.search(r"Volume observado:\*?\*?\s*(?:cerca de\s*)?([\d.,]+)\s+resultados?", body, re.I)
    if not match:
        return None
    try:
        return int(match.group(1).replace(".", "").replace(",", ""))
    except ValueError:
        return None


def google_url(query):
    return "https://patents.google.com/?q=" + query.replace(" ", "+") + "&country=BR"


def split_names(value):
    value = clean(value)
    value = re.sub(r"\s+e\s+", ", ", value, flags=re.I)
    value = re.sub(r"\s+and\s+", ", ", value, flags=re.I)
    return [clean(part) for part in value.split(",") if clean(part)]


def section_metadata(body):
    actors = []
    institutions = []
    for pattern in [r"Atores/instituições:\s*(.+)", r"Atores/facetas:\s*(.+)", r"Ator recorrente:\s*(.+)"]:
        match = re.search(pattern, body, re.I)
        if match:
            line = clean(match.group(1))
            line = re.sub(r"; também aparecem.*$", "", line, flags=re.I)
            actors.extend(split_names(line))
    for match in re.finditer(r"(?:Atores/instituições|Atores/facetas):\s*(.+)", body, re.I):
        institutions.extend(split_names(clean(match.group(1))))
    signal_match = re.search(r"Sinal:\s*(.+?)(?=\n-\s*Proveniência:|\Z)", body, re.I | re.S)
    signal = clean(signal_match.group(1)) if signal_match else ""
    provenance_match = re.search(r"Proveniência:\s*(.+)", body, re.I)
    provenance = clean(provenance_match.group(1)) if provenance_match else ""
    return list(OrderedDict.fromkeys(actors)), list(OrderedDict.fromkeys(institutions)), signal, provenance


def visible_records(body):
    match = re.search(r"Registros visíveis:\s*(.+?)(?=\n-\s*(?:Atores|Ator recorrente|Sinal|Proveniência):|\Z)", body, re.I | re.S)
    if not match:
        return []
    text = clean(match.group(1))
    matches = list(PATENT_ID_RE.finditer(text))
    records = []
    for idx, current in enumerate(matches):
        next_start = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        tail = text[current.end():next_start]
        tail = re.sub(r"^\s*,\s*", "", tail)
        tail = re.sub(r"\s*;?\s*(?:e|and)\s*$", "", tail, flags=re.I)
        tail = clean(tail)
        actor = ""
        title = tail
        with_match = re.search(r"\s+com\s+(.+)$", tail, re.I)
        if with_match:
            actor = clean(with_match.group(1))
            title = clean(tail[:with_match.start()])
        else:
            parts = [clean(p) for p in tail.split(",") if clean(p)]
            if len(parts) >= 2:
                actor = parts[-1]
                title = clean(", ".join(parts[:-1]))
        title = title or f"Registro capturado: {current.group(0)}"
        records.append({"source_id": current.group(0), "title": title, "actor": actor, "raw_tail": tail})
    return records


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    configs = {item["id"]: item for item in json.loads(QUERIES.read_text(encoding="utf-8"))["queries"]}
    findings = FINDINGS.read_text(encoding="utf-8")
    retrieved_at = datetime.now(timezone.utc).isoformat()
    manifest_rows = []
    summary = {
        "generated_at": retrieved_at,
        "metadata_only": True,
        "source": "google_patents",
        "round": "expansion_v2",
        "queries": {},
        "unique_records_across_queries": 0,
        "notes": ["Parsed from browser-captured public result metadata and the V2 finding notebook.", "No patent PDF or full text downloaded.", "IDs are deduplicated within each query and across the summary only."],
    }
    all_ids = set()
    for match in SECTION_RE.finditer(findings):
        query_id = match.group("qid")
        cfg = configs.get(query_id)
        if not cfg or cfg.get("source") != "google_patents":
            continue
        label = cfg.get("query", clean(match.group("label")))
        body = match.group("body")
        total_reported = observed_count(body)
        source_url = google_url(label)
        section_actors, section_institutions, signal, provenance = section_metadata(body)
        rows = []
        for record in visible_records(body):
            actor = record["actor"]
            assignees = [actor] if actor else []
            institutions = [actor] if actor else []
            snippet = f"{record['title']}. {signal}".strip(". ")
            row = {
                "source": "google_patents",
                "source_kind": "browser_finding",
                "round": "expansion_v2",
                "trail": cfg.get("trail"),
                "query_id": query_id,
                "query": label,
                "observed_result_count": total_reported,
                "source_url": source_url,
                "retrieved_at": retrieved_at,
                "http_status": 200,
                "raw_hash": sha256_text(record["source_id"] + "|" + snippet),
                "source_id": record["source_id"],
                "title": record["title"],
                "description_or_abstract": snippet,
                "dates": {},
                "actors": {"inventors": [], "assignees": assignees},
                "institutions": institutions,
                "geography": {"country_filter": "BR", "interpretation": "resultado com filtro de país BR; não implica origem brasileira"},
                "classifications": [],
                "identifiers": {"publication_number": record["source_id"], "google_patents_url": f"https://patents.google.com/patent/{record['source_id']}/en"},
                "license_or_access": "public metadata finding",
                "raw_fields": {"finding_section": body.strip(), "source_snippet": record["raw_tail"], "signal": signal, "section_actors": section_actors, "section_institutions": section_institutions, "provenance_note": provenance, "parser": "parse_expansion_patents_v2.py"},
                "status": "captured",
            }
            rows.append(row)
        rows = list(OrderedDict((row["source_id"], row) for row in rows).values())
        output = RAW_DIR / f"expansion_{query_id.lower()}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:100].strip('_')}.jsonl"
        payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
        output.write_text(payload, encoding="utf-8")
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        manifest_rows.append({
            "source": "google_patents",
            "source_kind": "browser_finding",
            "round": "expansion_v2",
            "trail": cfg.get("trail"),
            "query_id": query_id,
            "query": label,
            "url": source_url,
            "params": {"country": "BR", "deduplicate": "family", "results_per_page": 10},
            "retrieved_at": retrieved_at,
            "response_sha256": digest,
            "saved_path": str(output.relative_to(ROOT)),
            "saved_sha256": digest,
            "status": "captured" if rows else "empty",
            "http_status": 200,
            "returned_items": len(rows),
            "observed_result_count": total_reported,
            "metadata_only": True,
            "notes": ["Parsed from browser-captured public result metadata and V2 findings.", "No patent PDF or full text downloaded."],
        })
        summary["queries"][query_id] = {"query": label, "trail": cfg.get("trail"), "observed_result_count": total_reported, "unique_records": len(rows), "saved_path": str(output.relative_to(ROOT))}
        all_ids.update(row["source_id"] for row in rows)
    existing = []
    if MANIFEST.exists():
        existing = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
    existing = [row for row in existing if not (row.get("source") == "google_patents" and row.get("round") == "expansion_v2")]
    existing.extend(manifest_rows)
    MANIFEST.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in existing), encoding="utf-8")
    summary["unique_records_across_queries"] = len(all_ids)
    summary["query_count"] = len(summary["queries"])
    summary["captured_records_across_queries"] = sum(item["unique_records"] for item in summary["queries"].values())
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()

