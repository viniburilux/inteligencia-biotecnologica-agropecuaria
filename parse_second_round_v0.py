import hashlib
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FINDINGS = ROOT / "SECOND_ROUND_PATENT_FINDINGS_V0.md"
RAW_DIR = ROOT / "raw_v0" / "google_patents"
MANIFEST = ROOT / "ingestion_manifest_v0.jsonl"
SUMMARY = ROOT / "second_round_patent_parser_summary_v0.json"

PATENT_ID_RE = re.compile(r"\bBR[A-Z0-9]+[ABU]\d\b")
SECTION_RE = re.compile(r"^## (NQ\d+) — (?P<label>.+?)\n(?P<body>.*?)(?=^## NQ\d+ — |\Z)", re.M | re.S)
DATE_RE = re.compile(r"(?:Priority|Priority date|Filed|Published|Prioridade|Depósito|Publicado)\s+(\d{4}(?:-\d{2}-\d{2})?)", re.I)
PAGE_FILES = {
    "NQ01": "patents.google.com__q__Trichoderma_fermentation__country_BR.md",
    "NQ02": "patents.google.com__q__Trichoderma_biocontrol__country_BR.md",
    "NQ04": "patents.google.com__q__microbial_nitrogen_fixation_formulation__country_BR.md",
    "NQ06": "patents.google.com__q__phosphate_solubilization_microbial__country_BR.md",
    "NQ05": "patents.google.com__q__nitrogen_fixation_microbial_release__country_BR.md",
    "NQ07": "patents.google.com__q__bioinput_bioreactor__country_BR.md",
    "NQ08": "patents.google.com__q__bioinput_fermentation__country_BR.md",
    "NQ10": "patents.google.com__q__bioinput_rural_property_production__country_BR.md",
    "NQ09": "patents.google.com__q__bioinput_quality_monitoring_spectrometry__country_BR.md",
}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def clean(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[`*_]", "", value)
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


def url_from_body(body):
    match = re.search(r"^- \*\*URL:\*\*\s*(https://\S+)", body, re.M)
    return match.group(1).strip() if match else ""


def split_actor_line(line):
    line = clean(line)
    line = re.sub(r"^#+\s*", "", line)
    line = re.sub(r"\s+Priority.*$", "", line, flags=re.I)
    line = re.sub(r"\s+Filed.*$", "", line, flags=re.I)
    line = re.sub(r"\s+Published.*$", "", line, flags=re.I)
    match = PATENT_ID_RE.search(line)
    if not match:
        return [], []
    tail = line[match.end():].strip(" -:;")
    if not tail:
        return [], []
    parts = [clean(x) for x in re.split(r"\s{2,}", tail) if clean(x)]
    if not parts:
        return [], []
    if len(parts) == 1:
        return [parts[0]], []
    return [parts[0]], parts[1:]


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
        end = min(idx + 4, len(lines))
        chunk = lines[idx:end]
        chunk_text = " ".join(x for x in chunk if x)
        inventors, assignees = split_actor_line(actor_line)
        dates = extract_dates(chunk_text)
        description = lines[idx + 3] if idx + 3 < len(lines) else ""
        if description.startswith("Next") or description.startswith("About"):
            description = ""
        for source_id in list(dict.fromkeys(ids)):
            snippet = f"{title}. {description}".strip(". ")
            snippet_hash = sha256_bytes(snippet.encode("utf-8"))
            rows.append({
                "source": "google_patents",
                "source_kind": "browser_html",
                "round": "second_round",
                "query_id": query_id,
                "query": label,
                "observed_result_count": total_reported,
                "source_url": source_url,
                "retrieved_at": retrieved_at,
                "http_status": 200,
                "raw_hash": snippet_hash,
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
                "raw_fields": {"source_snippet": snippet, "parser": "parse_second_round_v0.py"},
                "status": "captured",
            })
    unique = OrderedDict((row["source_id"], row) for row in rows)
    return list(unique.values())


def append_manifest(rows):
    existing = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()] if MANIFEST.exists() else []
    second_ids = {"NQ01", "NQ02", "NQ04", "NQ06", "NQ05", "NQ07", "NQ08", "NQ10", "NQ09"}
    existing = [row for row in existing if not (row.get("source") == "google_patents" and row.get("query_id") in second_ids)]
    existing.extend(rows)
    MANIFEST.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in existing), encoding="utf-8")


def main():
    findings = FINDINGS.read_text(encoding="utf-8")
    retrieved_at = datetime.now(timezone.utc).isoformat()
    manifest_rows = []
    summary = {"generated_at": retrieved_at, "metadata_only": True, "source": "google_patents", "round": "second_round", "queries": {}, "unique_records_across_queries": 0}
    all_ids = set()
    for match in SECTION_RE.finditer(findings):
        query_id = match.group(1)
        if query_id not in PAGE_FILES:
            continue
        label = clean(match.group("label").replace(" + BR", ""))
        body = match.group("body")
        page_path = ROOT.parent / "page_texts" / PAGE_FILES[query_id]
        if not page_path.exists():
            continue
        source_url = url_from_body(body)
        total_reported = observed_count(body)
        rows = parse_page(page_path, query_id, label, source_url, total_reported, retrieved_at)
        if not rows:
            # Algumas páginas dinâmicas foram preservadas apenas com volume e sinais no caderno.
            # Nesse caso, ingerimos os IDs explícitos do caderno com título genérico e snippet exato.
            fallback_ids = list(dict.fromkeys(PATENT_ID_RE.findall(body)))
            for source_id in fallback_ids:
                source_lines = [clean(line) for line in body.splitlines() if source_id in line]
                snippet = source_lines[0] if source_lines else f"ID capturado no caderno da consulta {label}"
                rows.append({
                    "source": "google_patents",
                    "source_kind": "browser_html_finding",
                    "round": "second_round",
                    "query_id": query_id,
                    "query": label,
                    "observed_result_count": total_reported,
                    "source_url": source_url,
                    "retrieved_at": retrieved_at,
                    "http_status": 200,
                    "raw_hash": sha256_bytes(snippet.encode("utf-8")),
                    "source_id": source_id,
                    "title": f"Result captured in finding: {label}",
                    "description_or_abstract": snippet,
                    "dates": {},
                    "actors": {"inventors": [], "assignees": []},
                    "institutions": [],
                    "geography": {"country_filter": "BR", "interpretation": "resultado com filtro de país BR; não implica origem brasileira"},
                    "classifications": [],
                    "identifiers": {"publication_number": source_id, "google_patents_url": f"https://patents.google.com/patent/{source_id}/en"},
                    "license_or_access": "public metadata finding",
                    "raw_fields": {"source_snippet": snippet, "parser": "parse_second_round_v0.py", "fallback": True},
                    "status": "captured",
                })
        output = RAW_DIR / f"second_round_{query_id.lower()}_{slug(label)}.jsonl"
        payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")
        output.write_bytes(payload)
        digest = sha256_bytes(payload)
        manifest_rows.append({
            "source": "google_patents",
            "source_kind": "browser_html",
            "round": "second_round",
            "query_id": query_id,
            "query": label,
            "url": source_url,
            "params": {"country": "BR", "deduplicate": "family", "results_per_page": 10},
            "retrieved_at": retrieved_at,
            "response_sha256": digest,
            "saved_path": str(output.relative_to(ROOT)),
            "saved_sha256": digest,
            "status": "captured",
            "http_status": 200,
            "returned_items": len(rows),
            "observed_result_count": total_reported,
            "metadata_only": True,
            "notes": ["Parsed from browser-captured public result metadata.", "No patent PDF or full text downloaded.", "Publication numbers deduplicated within query."]
        })
        summary["queries"][query_id] = {"query": label, "observed_result_count": total_reported, "unique_records": len(rows), "saved_path": str(output.relative_to(ROOT))}
        all_ids.update(row["source_id"] for row in rows)
    append_manifest(manifest_rows)
    summary["unique_records_across_queries"] = len(all_ids)
    summary["query_count"] = len(summary["queries"])
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()

