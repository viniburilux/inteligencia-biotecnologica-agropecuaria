#!/usr/bin/env python3
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_v0"
MANIFEST = ROOT / "ingestion_manifest_v0.jsonl"
SEEDS = ROOT / "query_seeds_v0.json"
UA = "InteligenciaBiotecnologicaAgropecuaria/0.1 metadata-only research"
TIMEOUT = 30


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def slug(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")[:100]


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    path.write_bytes(raw)
    return sha256_bytes(raw), len(raw)


def append_manifest(entry):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def fetch_and_save(source, query, url, params, output_path, source_kind):
    started = time.time()
    retrieved_at = utc_now()
    entry = {
        "source": source,
        "source_kind": source_kind,
        "query": query,
        "url": url,
        "params": params,
        "retrieved_at": retrieved_at,
        "metadata_only": True,
        "download_scientific_files": False,
        "full_text_patent_download": False,
        "status": "blocked",
    }
    try:
        response = requests.get(url, params=params, headers={"User-Agent": UA, "Accept": "application/json"}, timeout=TIMEOUT)
        entry["http_status"] = response.status_code
        entry["final_url"] = response.url
        entry["latency_seconds"] = round(time.time() - started, 3)
        raw = response.content
        entry["response_sha256"] = sha256_bytes(raw)
        entry["response_bytes"] = len(raw)
        if response.status_code != 200:
            entry["error"] = response.text[:500]
        else:
            try:
                payload = response.json()
                digest, size = save_json(output_path, payload)
                entry["status"] = "captured"
                entry["saved_path"] = str(output_path.relative_to(ROOT))
                entry["saved_sha256"] = digest
                entry["saved_bytes"] = size
                if isinstance(payload, dict):
                    if "meta" in payload:
                        entry["source_meta"] = payload.get("meta")
                    if "message" in payload and isinstance(payload["message"], dict):
                        message = payload["message"]
                        if "total-results" in message:
                            entry["total_results"] = message.get("total-results")
                        if "items" in message and isinstance(message["items"], list):
                            entry["returned_items"] = len(message["items"])
                    if "results" in payload and isinstance(payload["results"], list):
                        entry["returned_items"] = len(payload["results"])
                    if "patents" in payload and isinstance(payload["patents"], list):
                        entry["returned_items"] = len(payload["patents"])
            except ValueError as exc:
                entry["error"] = f"invalid_json: {exc}"
    except requests.RequestException as exc:
        entry["latency_seconds"] = round(time.time() - started, 3)
        entry["error"] = f"request_error: {exc}"
    append_manifest(entry)
    print(json.dumps(entry, ensure_ascii=False))
    return entry


def collect_openalex(queries):
    for query in queries:
        params = {
            "search": query,
            "filter": "from_publication_date:2010-01-01,to_publication_date:2026-12-31",
            "per-page": 25,
        }
        output = RAW / "openalex" / f"{slug(query)}.json"
        fetch_and_save("openalex", query, "https://api.openalex.org/works", params, output, "literature_api")
        time.sleep(0.2)


def collect_crossref(queries):
    for query in queries:
        params = {
            "query": query,
            "filter": "from-pub-date:2010-01-01,until-pub-date:2026-12-31",
            "rows": 25,
            "select": "DOI,title,author,published,container-title,issued,URL,subject,type,relation,link",
        }
        output = RAW / "crossref" / f"{slug(query)}.json"
        fetch_and_save("crossref", query, "https://api.crossref.org/works", params, output, "literature_api")
        time.sleep(0.2)


def patentsview_requests(query):
    q = json.dumps({"_text_any": {"patent_title": query}}, separators=(",", ":"))
    fields = json.dumps(["patent_id", "patent_title", "patent_date", "inventor", "assignee"], separators=(",", ":"))
    options = json.dumps({"size": 25}, separators=(",", ":"))
    return [
        (
            "https://search.patentsview.org/api/v1/patent/",
            {"q": q, "f": fields, "o": options},
            "patentsview_v1",
        ),
        (
            "https://api.patentsview.org/patents/query",
            {"q": q, "f": fields, "o": options},
            "patentsview_legacy",
        ),
    ]


def collect_patentsview(queries):
    for query in queries:
        captured = False
        for endpoint, params, kind in patentsview_requests(query):
            output = RAW / "patentsview" / f"{slug(query)}_{slug(kind)}.json"
            entry = fetch_and_save("patentsview", query, endpoint, params, output, "patent_api")
            if entry.get("status") == "captured":
                captured = True
                break
        if not captured:
            print(json.dumps({"source": "patentsview", "query": query, "status": "blocked_all_endpoints"}))
        time.sleep(0.2)


def write_source_context():
    contexts = [
        {
            "source": "inpi_open_data",
            "source_url": "https://www.gov.br/inpi/pt-br/acesso-a-informacao/dados-abertos",
            "status": "next_candidate",
            "reason": "source channel identified; exact downloadable files and fields still require direct capture",
        },
        {
            "source": "epo_ops",
            "source_url": "https://www.epo.org/en/searching-for-patents/data/web-services/ops",
            "status": "blocked",
            "reason": "OAuth credentials not configured in this run",
        },
        {
            "source": "embrapa_agroapi",
            "source_url": "https://www.embrapa.br/agroapi",
            "status": "blocked",
            "reason": "token/account not configured in this run",
        },
    ]
    for context in contexts:
        append_manifest({"retrieved_at": utc_now(), "metadata_only": True, **context})


def main():
    seeds = json.loads(SEEDS.read_text(encoding="utf-8"))
    if MANIFEST.exists():
        MANIFEST.unlink()
    collect_openalex(seeds["queries"]["openalex"])
    collect_crossref(seeds["queries"]["crossref"])
    collect_patentsview(seeds["queries"]["patentsview"])
    write_source_context()


if __name__ == "__main__":
    main()
