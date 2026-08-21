import hashlib
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FINDINGS = ROOT / "EXPANSION_PATENT_FINDINGS_V1.md"
QUERIES = ROOT / "EXPANSION_QUERIES_V1.json"
RAW_DIR = ROOT / "raw_v1" / "google_patents_expansion"
MANIFEST = ROOT / "ingestion_manifest_v1.jsonl"
SUMMARY = ROOT / "expansion_patent_parser_summary_v1.json"
PAGE_ROOT = ROOT.parent / "page_texts"

PATENT_ID_RE = re.compile(r"\bBR[A-Z0-9]+[ABU]\d\b")
SECTION_RE = re.compile(r"^## (?P<qid>L\d+|I\d+|T\d+|C\d+) — (?P<label>.+?)\n(?P<body>.*?)(?=^## (?:L\d+|I\d+|T\d+|C\d+) — |\Z)", re.M | re.S)

PAGE_FILES = {
    "L01": "patents.google.com__q__bioinput_fermentation_aseptic__country_BR.md",
    "L02": "patents.google.com__q__Trichoderma_sophorolipid__country_BR.md",
    "L03": "patents.google.com__q__bioinput_bioreactor_rural_property__country_BR.md",
    "L04": "patents.google.com__q__biofertilizer_kit_smallholder__country_BR.md",
    "L05": "patents.google.com__q__bioinput_quality_monitoring_thermochromia__country_BR.md",
    "I01": "patents.google.com__q__Pivot_Bio_nitrogen_fixation_phosphate__country_BR.md",
    "I02": "patents.google.com__q__microbial_nitrogen_fixation_polymer_formulation__country_BR.md",
    "I03": "patents.google.com__q__rhizosphere_nutrient_acquisition_microbial__country_BR.md",
    "I04": "patents.google.com__q__Rhizobium_inoculant_formulation__country_BR.md",
    "T01": "patents.google.com__q__Trichoderma_cellulase_ethanol__country_BR.md",
    "T02": "patents.google.com__q__Trichoderma_enzyme_fermentation__country_BR.md",
    "C01": "patents.google.com__q__biofixation_CO2_algae_Petrobras__country_BR.md",
    "C02": "patents.google.com__q__algal_biomass_drilling_cuttings__country_BR.md",
}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def clean(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[\`*_]", "", value)
    value = value.replace("—", " ").replace("–", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" \t\r\n;,.:()")


def slug(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value, flags=re.ASCII)
    return value.strip("_")[:100]


def observed_count(body):
    match = re.search(r"Volume observado:\*\*\s*([\d.,]+)\s+resultados?", body, re.I)
    if not match:
        return None
    try:
        return int(match.group(1).replace(".", "").replace(",", ""))
    except ValueError:
        return None


def extract_dates(text):
    dates = {}
    patterns = {
        "priority_date": r"(?:Priority|Prioridade)\s+(\d{4}(?:-\d{2}-\d{2})?)",
        "filed_date": r"(?:Filed|Dep[oó]sito)\s+(\d{4}(?:-\d{2}-\d{2})?)",
        "published_date": r"(?:Published|Publicado)\s+(\d{4}(?:-\d{2}-\d{2})?)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.I)
        if match:
            dates[key] = match.group(1)
    return dates


def actor_fields(actor_line):
    actor_line = clean(actor_line)
    actor_line = re.sub(r"\s+Priority.*$", "", actor_line, flags=re.I)
    actor_line = re.sub(r"\s+Filed.*$", "", actor_line, flags=re.I)
    actor_line = re.sub(r"\s+Published.*$", "", actor_line, flags=re.I)
    ids = PATENT_ID_RE.findall(actor_line)
    if not ids:
        return [], []
    tail = actor_line.split(ids[-1], 1)[1].strip(" -:;")
    parts = [clean(p) for p in re.split(r"\s{2,}", tail) if clean(p)]
    if not parts:
        return [], []
    if len(parts) == 1:
        return [parts[0]], []
    return [parts[0]], parts[1:]


def google_url(query):
    return "https://patents.google.com/?q=" + query.replace(" ", "+") + "&country=BR"


def parse_page(page_path, query_id, label, source_url, total_reported, retrieved_at):
    lines = [clean(line) for line in page_path.read_text(encoding="utf-8").splitlines()]
    rows = []
    for idx in range(len(lines) - 1):
        actor_line = lines[idx + 1]
        ids = PATENT_ID_RE.findall(actor_line)
        if not ids:
            continue
        title = lines[idx]
        if not title or title.startswith("#") or title.startswith("**"):
            continue
        end = min(idx + 5, len(lines))
        chunk = [x for x in lines[idx:end] if x]
        chunk_text = " ".join(chunk)
        inventors, assignees = actor_fields(actor_line)
        dates = extract_dates(chunk_text)
        description = lines[idx + 3] if idx + 3 < len(lines) else ""
        if description.startswith("Next") or description.startswith("About"):
            description = ""
        snippet = f"{title}. {description}".strip(". ")
        for source_id in list(dict.fromkeys(ids)):
            rows.append({
                "source": "google_patents",
                "source_kind": "browser_html",
                "round": "expansion_v1",
                "query_id": query_id,
                "query": label,
                "observed_result_count": total_reported,
                "source_url": source_url,
                "retrieved_at": retrieved_at,
                "http_status": 200,
                "raw_hash": sha256_bytes(snippet.encode("utf-8")),
                "source_id": source_id,
                "title": title or source_id,
                "description_or_abstract": snippet,
                "dates": dates,
                "actors": {"inventors": inventors, "assignees": assignees},
                "institutions": assignees,
                "geography": {"country_filter": "BR", "interpretation": "resultado com filtro de país BR; não implica origem brasileira"},
                "classifications": [],
                "identifiers": {"publication_number": source_id, "google_patents_url": f"https://patents.google.com/patent/{source_id}/en"},
                "license_or_access": "public metadata page",
                "raw_fields": {"source_snippet": snippet, "parser": "parse_expansion_patents_v1.py"},
                "status": "captured",
            })
    unique = OrderedDict((row["source_id"], row) for row in rows)
    return list(unique.values())


def fallback_from_findings(body, query_id, label, source_url, total_reported, retrieved_at):
    rows = []
    for source_id in list(dict.fromkeys(PATENT_ID_RE.findall(body))):
        line = next((clean(line) for line in body.splitlines() if source_id in line), f"ID capturado no caderno da consulta {label}")
        rows.append({
            "source": "google_patents",
            "source_kind": "browser_html_finding",
            "round": "expansion_v1",
            "query_id": query_id,
            "query": label,
            "observed_result_count": total_reported,
            "source_url": source_url,
            "retrieved_at": retrieved_at,
            "http_status": 200,
            "raw_hash": sha256_bytes(line.encode("utf-8")),
            "source_id": source_id,
            "title": f"Result captured in finding: {label}",
            "description_or_abstract": line,
            "dates": extract_dates(body),
            "actors": {"inventors": [], "assignees": []},
            "institutions": [],
            "geography": {"country_filter": "BR", "interpretation": "resultado com filtro de país BR; não implica origem brasileira"},
            "classifications": [],
            "identifiers": {"publication_number": source_id, "google_patents_url": f"https://patents.google.com/patent/{source_id}/en"},
            "license_or_access": "public metadata finding",
            "raw_fields": {"source_snippet": line, "parser": "parse_expansion_patents_v1.py", "fallback": True},
            "status": "captured",
        })
    return rows


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    config = {item["id"]: item for item in json.loads(QUERIES.read_text(encoding="utf-8"))["queries"]}
    findings = FINDINGS.read_text(encoding="utf-8") if FINDINGS.exists() else ""
    retrieved_at = datetime.now(timezone.utc).isoformat()
    manifest_rows = []
    summary = {"generated_at": retrieved_at, "metadata_only": True, "source": "google_patents", "round": "expansion_v1", "queries": {}, "unique_records_across_queries": 0}
    all_ids = set()
    for match in SECTION_RE.finditer(findings):
        query_id = match.group("qid")
        if query_id not in PAGE_FILES:
            continue
        cfg = config.get(query_id, {})
        label = cfg.get("query", clean(match.group("label")))
        total_reported = observed_count(match.group("body"))
        source_url = google_url(label)
        page_path = PAGE_ROOT / PAGE_FILES[query_id]
        rows = parse_page(page_path, query_id, label, source_url, total_reported, retrieved_at) if page_path.exists() else []
        if not rows:
            rows = fallback_from_findings(match.group("body"), query_id, label, source_url, total_reported, retrieved_at)
        output = RAW_DIR / f"expansion_{query_id.lower()}_{slug(label)}.jsonl"
        payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")
        output.write_bytes(payload)
        digest = sha256_bytes(payload)
        manifest_rows.append({
            "source": "google_patents",
            "source_kind": "browser_html",
            "round": "expansion_v1",
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
            "notes": ["Parsed from browser-captured public result metadata.", "No patent PDF or full text downloaded.", "Publication numbers deduplicated within query."],
        })
        summary["queries"][query_id] = {"query": label, "observed_result_count": total_reported, "unique_records": len(rows), "saved_path": str(output.relative_to(ROOT))}
        all_ids.update(row["source_id"] for row in rows)
    existing = []
    if MANIFEST.exists():
        existing = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
    existing = [row for row in existing if not (row.get("source") == "google_patents" and row.get("round") == "expansion_v1")]
    existing.extend(manifest_rows)
    MANIFEST.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in existing), encoding="utf-8")
    summary["unique_records_across_queries"] = len(all_ids)
    summary["query_count"] = len(summary["queries"])
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
