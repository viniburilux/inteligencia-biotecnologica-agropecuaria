import hashlib
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FINDINGS = ROOT / "PATENT_SOURCE_FINDINGS_V0.md"
RAW_DIR = ROOT / "raw_v0" / "google_patents"
MANIFEST = ROOT / "ingestion_manifest_v0.jsonl"
SUMMARY = ROOT / "patent_parser_summary_v0.json"

PATENT_ID_RE = re.compile(r"\bBR[A-Z0-9]+[ABU]\d\b")
QUERY_RE = re.compile(r"^## Query: (.+?)\n(?P<body>.*?)(?=^## Query: |\Z)", re.M | re.S)
DATE_RE = re.compile(r"\b(\d{4}(?:-\d{2}-\d{2})?)\b")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value, flags=re.ASCII)
    return value.strip("_")


def clean(value: str) -> str:
    value = value.replace("—", " ").replace("–", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" \t\r\n;,.:")


def canonical_query(query: str) -> str:
    query = re.sub(r"\s+", " ", query.strip())
    return re.sub(r"\s*\(registro consolidado\)$", "", query, flags=re.I)


def observed_result_count(body: str):
    match = re.search(r"\*\*([\d.,]+)\s+resultados?\*\*", body, re.I)
    if not match:
        return None
    value = match.group(1).replace(".", "").replace(",", "")
    try:
        return int(value)
    except ValueError:
        return None


def section_url(body: str) -> str:
    match = re.search(r"^URL: (https://[^\n]+)", body, re.M)
    return match.group(1).strip() if match else ""


def section_date(body: str) -> str:
    match = re.search(r"^Data de consulta: (\d{4}-\d{2}-\d{2})", body, re.M)
    return match.group(1) if match else datetime.now(timezone.utc).date().isoformat()


def _metadata_start(rest: str):
    return re.search(r"\s*(?:;|,)\s*(?:prioridade|priority|dep[oó]sito|filed|published|publicado|inventor(?:a|/depositante)?|depositante)\b", rest, re.I)


def _compact_actor_tail(pre: str):
    if "," not in pre:
        return "", ""
    candidate = pre.rsplit(",", 1)[1].strip()
    # Compact records in the findings use "title, inventor / assignee".
    # Only split when the tail looks like a person or organization, not a title clause.
    if "/" not in candidate and not (2 <= len(candidate.split()) <= 8):
        return "", ""
    if "/" in candidate:
        inventor_text, assignee_text = candidate.split("/", 1)
        return clean(inventor_text), clean(assignee_text)
    return clean(candidate), ""


def cut_title(rest: str) -> str:
    match = _metadata_start(rest)
    pre = rest[: match.start()] if match else rest
    # Explicit labels are always authoritative.
    labeled = re.search(r"\s*;\s*(?:inventor(?:a|/depositante)?|depositante)\b", pre, re.I)
    if labeled:
        pre = pre[: labeled.start()]
    inventor_text, assignee_text = _compact_actor_tail(pre)
    if inventor_text:
        pre = pre[: pre.rfind(",")]
    return clean(pre)


def extract_dates(rest: str) -> dict:
    dates = {}
    patterns = {
        "priority_date": r"(?:prioridade|priority)\s+(\d{4}(?:-\d{2}-\d{2})?)",
        "filed_date": r"(?:dep[oó]sito|filed)\s+(\d{4}(?:-\d{2}-\d{2})?)",
        "published_date": r"(?:publicado|published)\s+(\d{4}(?:-\d{2}-\d{2})?)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, rest, re.I)
        if match:
            dates[key] = match.group(1)
    return dates


def split_names(value: str) -> list[str]:
    value = clean(value)
    value = re.split(r"\s+(?:prioridade|priority|dep[oó]sito|filed|publicado|published)\b", value, maxsplit=1, flags=re.I)[0]
    names = []
    for part in re.split(r"\s*/\s*|\s+e\s+|\s+and\s+", value):
        part = clean(part)
        if part and len(part) > 2:
            names.append(part)
    return list(dict.fromkeys(names))


def extract_actors(rest: str) -> tuple[list[str], list[str]]:
    inventors = []
    assignees = []
    explicit = re.search(r"inventor(?:a|/depositante)?\s+(.+?)(?=;\s*depositante|;\s*prioridade|;\s*publicado|\.|$)", rest, re.I)
    if explicit:
        names = split_names(explicit.group(1))
        inventors.extend(names)
        if "inventor/depositante" in explicit.group(0).lower():
            assignees.extend(names)
    assigned = re.search(r"depositante\s+(.+?)(?=;\s*prioridade|;\s*publicado|\.|$)", rest, re.I)
    if assigned:
        assignees.extend(split_names(assigned.group(1)))

    # Compact records use: title, inventor / assignee, followed by optional dates.
    if not inventors:
        match = _metadata_start(rest)
        pre = rest[: match.start()] if match else rest
        inventor_text, assignee_text = _compact_actor_tail(pre)
        if inventor_text:
            inventors.extend(split_names(inventor_text))
            if assignee_text:
                assignees.extend(split_names(assignee_text))
    return list(dict.fromkeys(inventors)), list(dict.fromkeys(assignees))


def parse_section(query: str, body: str) -> list[dict]:
    core = body.split("URL:", 1)[0]
    total_reported = observed_result_count(body)
    matches = list(PATENT_ID_RE.finditer(core))
    rows = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(core)
        rest = core[start:end]
        rest = re.sub(r"^\s*[-—–:]\s*", "", rest)
        rest = clean(rest)
        if not rest:
            continue
        publication_number = match.group(0)
        title = cut_title(rest)
        dates = extract_dates(rest)
        inventors, assignees = extract_actors(rest)
        snippet_hash = sha256_bytes(rest.encode("utf-8"))
        rows.append({
            "source": "google_patents",
            "source_kind": "browser_html",
            "query": canonical_query(query),
            "observed_result_count": total_reported,
            "source_url": section_url(body),
            "retrieved_at": f"{section_date(body)}T00:00:00+00:00",
            "http_status": 200,
            "raw_hash": snippet_hash,
            "source_id": publication_number,
            "title": title or publication_number,
            "description_or_abstract": rest,
            "dates": dates,
            "actors": {"inventors": inventors, "assignees": assignees},
            "institutions": assignees,
            "geography": {"country_filter": "BR", "interpretation": "resultado com filtro de país BR; não implica origem brasileira"},
            "classifications": [],
            "identifiers": {"publication_number": publication_number, "google_patents_url": f"https://patents.google.com/patent/{publication_number}/en"},
            "license_or_access": "public metadata page",
            "raw_fields": {"source_snippet": rest, "parser": "parse_google_patents_v0.py"},
            "status": "captured",
        })
    return rows


def main() -> None:
    text = FINDINGS.read_text(encoding="utf-8")
    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    query_urls: dict[str, str] = {}
    query_dates: dict[str, str] = {}
    for match in QUERY_RE.finditer(text):
        query = canonical_query(match.group(1))
        rows = parse_section(query, match.group("body"))
        grouped.setdefault(query, []).extend(rows)
        if rows:
            query_urls.setdefault(query, rows[0]["source_url"])
            query_dates.setdefault(query, rows[0]["retrieved_at"][:10])

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
    manifest_rows = [row for row in manifest_rows if row.get("source") != "google_patents"]
    query_summary = {}
    total_occurrences = 0
    total_unique = 0

    for query, occurrences in grouped.items():
        unique = OrderedDict()
        for row in occurrences:
            unique.setdefault(row["source_id"], row)
        rows = list(unique.values())
        path = RAW_DIR / f"{slug(query)}.jsonl"
        payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")
        path.write_bytes(payload)
        digest = sha256_bytes(payload)
        manifest_rows.append({
            "source": "google_patents",
            "source_kind": "browser_html",
            "query": query,
            "url": query_urls.get(query),
            "params": {"country": "BR", "deduplicate": "family", "results_per_page": 10},
            "retrieved_at": f"{query_dates.get(query, datetime.now(timezone.utc).date().isoformat())}T00:00:00+00:00",
            "response_sha256": digest,
            "saved_path": str(path.relative_to(ROOT)),
            "saved_sha256": digest,
            "status": "captured",
            "http_status": 200,
            "returned_items": len(rows),
            "observed_result_count": max((row.get("observed_result_count") or 0 for row in occurrences), default=None) or None,
            "metadata_only": True,
            "notes": ["Parsed from browser-captured public result metadata.", "No patent PDF or full text downloaded.", "Duplicate publication numbers within the same query were collapsed."]
        })
        query_summary[query] = {"occurrences": len(occurrences), "unique_records": len(rows), "observed_result_count": max((row.get("observed_result_count") or 0 for row in occurrences), default=None) or None, "saved_path": str(path.relative_to(ROOT))}
        total_occurrences += len(occurrences)
        total_unique += len(rows)

    MANIFEST.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in manifest_rows), encoding="utf-8")
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metadata_only": True,
        "source": "google_patents",
        "query_count": len(query_summary),
        "occurrences_parsed": total_occurrences,
        "unique_records_across_queries": len({row["source_id"] for rows in grouped.values() for row in rows}),
        "unique_records_by_query_sum": total_unique,
        "queries": query_summary,
        "parser_notes": [
            "The parser preserves source snippets and query-level provenance.",
            "Publication numbers are deduplicated within each query and later merged conservatively by the normalizer.",
            "Actor extraction is best-effort from visible result text; it is not entity resolution.",
            "Country BR is retained as the search filter and not interpreted as inventor or assignee origin."
        ]
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
