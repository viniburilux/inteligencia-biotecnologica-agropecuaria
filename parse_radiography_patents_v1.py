import hashlib
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FINDINGS = ROOT / "RADIOGRAPHY_V1_PATENT_FINDINGS.md"
QUERIES = ROOT / "next_queries_v1.json"
RAW_DIR = ROOT / "raw_v2" / "google_patents_radiography_v1"
MANIFEST = ROOT / "ingestion_manifest_v2.jsonl"
SUMMARY = ROOT / "radiography_patent_parser_summary_v1.json"

PATENT_ID_RE = re.compile(r"\bBR[A-Z0-9]+[ABU]\d\b")
SECTION_RE = re.compile(
    r"^##\s+(?P<qid>Q\d+)(?P<reformulated>\s+reformulada)?\s+—\s+(?P<label>[^\n]+)\n(?P<body>.*?)(?=^##\s+Q\d+(?:\s+reformulada)?\s+—\s+|\Z)",
    re.M | re.S,
)


def clean(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[\`*_]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" \t\r\n;,.:()")


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def number(value):
    if not value:
        return None
    value = value.strip().replace(".", "").replace(",", "")
    try:
        return int(value)
    except ValueError:
        return None


def observed_count(body):
    patterns = [
        r"Volume observado:\s*([\d.,]+)\s+resultados?",
        r"About\s+([\d.,]+)\s+results?",
    ]
    for pattern in patterns:
        match = re.search(pattern, body, re.I)
        if match:
            return number(match.group(1))
    return None


def query_url(query):
    return "https://patents.google.com/?q=" + query.replace(" ", "+") + "&country=BR"


def section_status(body):
    lower = body.lower()
    if "insufficient" in lower or "no results found" in lower or "sem volume" in lower or "não expôs volume" in lower or "não exibiu resultados" in lower:
        return "insufficient"
    return "captured"


def extract_after(body, labels):
    for label in labels:
        match = re.search(label + r"\s*([^\n]+)", body, re.I)
        if match:
            return clean(match.group(1))
    return ""


def parse_dates(text):
    dates = {}
    for label, key in [("prioridade", "priority_date"), ("depósito", "filing_date"), ("publicação", "publication_date")]:
        match = re.search(label + r"\s+(\d{4}-\d{2}-\d{2})", text, re.I)
        if match:
            dates[key] = match.group(1)
    return dates


def extract_record(body, patent_id, start, end):
    window = body[start:end]
    lines = [clean(line.lstrip("- ")) for line in window.splitlines() if clean(line)]
    id_index = 0
    for idx, line in enumerate(lines):
        if patent_id in line:
            id_index = idx
            break
    record_line = lines[id_index]
    title = ""
    for idx in range(id_index - 1, -1, -1):
        candidate = lines[idx]
        if candidate.startswith("##") or candidate.startswith("URL:") or candidate.startswith("Volume observado"):
            continue
        if candidate.startswith("Título:"):
            title = clean(candidate.split(":", 1)[1])
            break
        if len(candidate) > 18 and not re.search(r"(?:inventor|inventora|assignee|depositante|datas observadas|excerto|proveniência|sinal|limite|estado|resultado observado)", candidate, re.I):
            title = candidate
            break
    if not title:
        title_match = re.search(re.escape(patent_id) + r"\s*:\s*([^;\n]+)", window, re.I)
        if title_match:
            title = clean(title_match.group(1))
    inventor = ""
    inventor_match = re.search(r"inventor(?:a)?(?: observado)?\s*:\s*([^.;\n]+)", window, re.I)
    if inventor_match:
        inventor = clean(inventor_match.group(1))
    assignee = ""
    assignee_match = re.search(r"(?:depositante/assignee observado|assignee observado|assignee)\s*:\s*([^.;\n]+)", window, re.I)
    if assignee_match:
        assignee = clean(assignee_match.group(1))
    if not assignee:
        assignee_match = re.search(r"assignee\s+([^.;\n]+)", window, re.I)
        if assignee_match:
            assignee = clean(assignee_match.group(1))
    date_text = " ".join(lines)
    dates = parse_dates(date_text)
    excerpt = extract_after(window, [r"Excerto observado:", r"O excerto destaca:", r"O excerto descreve:", r"O excerto menciona:", r"O excerto trata de:"])
    if not excerpt:
        excerpt = extract_after(window, [r"Excerto:"])
    raw_tail = clean(window)
    return {
        "source_id": patent_id,
        "title": title or f"Registro capturado: {patent_id}",
        "inventor": inventor,
        "assignee": assignee,
        "dates": dates,
        "excerpt": excerpt,
        "raw_tail": raw_tail,
    }


def records_from_body(body):
    matches = list(PATENT_ID_RE.finditer(body))
    records = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        records.append(extract_record(body, match.group(0), match.start(), end))
    unique = OrderedDict()
    for record in records:
        unique[record["source_id"]] = record
    return list(unique.values())


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    configs = {item["query_id"]: item for item in json.loads(QUERIES.read_text(encoding="utf-8"))["queries"]}
    findings = FINDINGS.read_text(encoding="utf-8")
    retrieved_at = datetime.now(timezone.utc).isoformat()
    summary = {
        "generated_at": retrieved_at,
        "metadata_only": True,
        "source": "google_patents",
        "round": "radiography_v1_followup",
        "queries": {},
        "captured_records_across_queries": 0,
        "unique_records_across_queries": 0,
        "notes": [
            "Parsed from browser-captured public result metadata and RADIOGRAPHY_V1_PATENT_FINDINGS.md.",
            "No patent PDF or full text downloaded.",
            "Insufficient or no-result pages are preserved as query status, not interpreted as absence.",
        ],
    }
    manifest_rows = []
    all_ids = set()
    reformulated_queries = {
        "Q02": "Bacillus velezensis CMRP 4490 bioreactor Brazil",
        "Q04": "Solubio bioinsumo fermentação produção propriedade rural",
        "Q12": "microalga cascalho perfuração biofixação fertilizante",
    }
    for section in SECTION_RE.finditer(findings):
        base_query_id = section.group("qid")
        is_reformulated = bool(section.group("reformulated"))
        query_id = base_query_id + "R" if is_reformulated else base_query_id
        cfg = configs.get(base_query_id)
        if not cfg or cfg.get("source") != "google_patents":
            continue
        body = section.group("body")
        query = reformulated_queries.get(base_query_id, cfg["query"]) if is_reformulated else cfg["query"]
        status = section_status(body)
        total = observed_count(body)
        records = records_from_body(body) if status == "captured" else []
        payload_rows = []
        source_url = query_url(query)
        for record in records:
            snippet = ". ".join(part for part in [record["title"], record["excerpt"]] if part).strip(". ")
            row = {
                "source": "google_patents",
                "source_kind": "browser_finding",
                "round": "radiography_v1_followup",
                "trail": cfg.get("block"),
                "query_id": query_id,
                "query": query,
                "observed_result_count": total,
                "source_url": source_url,
                "retrieved_at": retrieved_at,
                "http_status": 200,
                "raw_hash": sha256_text(record["source_id"] + "|" + snippet),
                "source_id": record["source_id"],
                "title": record["title"],
                "description_or_abstract": snippet,
                "dates": record["dates"],
                "actors": {"inventors": [record["inventor"]] if record["inventor"] else [], "assignees": [record["assignee"]] if record["assignee"] else []},
                "institutions": [record["assignee"]] if record["assignee"] else [],
                "geography": {"country_filter": "BR", "interpretation": "resultado com filtro de país BR; não implica origem brasileira"},
                "classifications": [],
                "identifiers": {"publication_number": record["source_id"], "google_patents_url": f"https://patents.google.com/patent/{record['source_id']}/en"},
                "license_or_access": "public metadata finding",
                "raw_fields": {"finding_section": body.strip(), "source_snippet": record["raw_tail"], "parser": "parse_radiography_patents_v1.py"},
                "status": "captured",
            }
            payload_rows.append(row)
        output = RAW_DIR / f"radiography_{query_id.lower()}_{re.sub(r'[^a-z0-9]+', '_', query.lower())[:90].strip('_')}.jsonl"
        payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in payload_rows)
        output.write_text(payload, encoding="utf-8")
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        manifest_rows.append({
            "source": "google_patents",
            "source_kind": "browser_finding",
            "round": "radiography_v1_followup",
            "trail": cfg.get("block"),
            "query_id": query_id,
            "base_query_id": base_query_id,
            "reformulated": is_reformulated,
            "query": query,
            "url": source_url,
            "params": {"country": "BR", "deduplicate": "family", "results_per_page": 10},
            "retrieved_at": retrieved_at,
            "response_sha256": digest,
            "saved_path": str(output.relative_to(ROOT)),
            "saved_sha256": digest,
            "status": "captured" if payload_rows else status,
            "http_status": 200,
            "returned_items": len(payload_rows),
            "observed_result_count": total,
            "metadata_only": True,
            "notes": ["Parsed from browser-captured public result metadata and Radiography V1 findings.", "No patent PDF or full text downloaded.", "Insufficient pages preserved without synthetic records."],
        })
        summary["queries"][query_id] = {"query": query, "base_query_id": base_query_id, "reformulated": is_reformulated, "block": cfg.get("block"), "status": status, "observed_result_count": total, "unique_records": len(payload_rows), "saved_path": str(output.relative_to(ROOT))}
        summary["captured_records_across_queries"] += len(payload_rows)
        all_ids.update(row["source_id"] for row in payload_rows)
    existing = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()] if MANIFEST.exists() else []
    existing = [row for row in existing if not (row.get("source") == "google_patents" and row.get("round") == "radiography_v1_followup")]
    existing.extend(manifest_rows)
    MANIFEST.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in existing), encoding="utf-8")
    summary["unique_records_across_queries"] = len(all_ids)
    summary["query_count"] = len(summary["queries"])
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()

