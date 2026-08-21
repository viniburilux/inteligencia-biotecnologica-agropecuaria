import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_v0" / "openalex_second_round"
MANIFEST = ROOT / "ingestion_manifest_v0.jsonl"
QUERY_ID = "NQ14"
QUERY = "Brazilian bioinput fermentation agriculture"
URL = "https://api.openalex.org/works"
UA = "InteligenciaBiotecnologicaAgropecuaria/0.1 metadata-only research"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def slug(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")[:100]


def append_manifest(entry):
    with MANIFEST.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    params = {
        "search": QUERY,
        "filter": "from_publication_date:2010-01-01,to_publication_date:2026-12-31",
        "per-page": 25,
    }
    retrieved_at = utc_now()
    started = time.time()
    entry = {
        "source": "openalex",
        "source_kind": "literature_api",
        "query_id": QUERY_ID,
        "query": QUERY,
        "url": URL,
        "params": params,
        "retrieved_at": retrieved_at,
        "metadata_only": True,
        "download_scientific_files": False,
        "full_text_patent_download": False,
        "status": "blocked",
    }
    try:
        response = requests.get(URL, params=params, headers={"User-Agent": UA, "Accept": "application/json"}, timeout=30)
        raw = response.content
        entry.update({
            "http_status": response.status_code,
            "final_url": response.url,
            "latency_seconds": round(time.time() - started, 3),
            "response_sha256": sha256_bytes(raw),
            "response_bytes": len(raw),
        })
        if response.status_code == 200:
            payload = response.json()
            output = RAW / f"{slug(QUERY)}.json"
            output.write_bytes(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8"))
            entry.update({
                "status": "captured",
                "saved_path": str(output.relative_to(ROOT)),
                "saved_sha256": sha256_bytes(output.read_bytes()),
                "saved_bytes": output.stat().st_size,
                "total_results": payload.get("meta", {}).get("count"),
                "returned_items": len(payload.get("results", [])),
            })
        else:
            entry["error"] = response.text[:500]
    except (requests.RequestException, ValueError) as exc:
        entry["latency_seconds"] = round(time.time() - started, 3)
        entry["error"] = f"collection_error: {exc}"
    append_manifest(entry)
    summary = {
        "generated_at": utc_now(),
        "query_id": QUERY_ID,
        "query": QUERY,
        "source": "openalex",
        "metadata_only": True,
        "status": entry.get("status"),
        "total_results": entry.get("total_results"),
        "returned_items": entry.get("returned_items"),
        "saved_path": entry.get("saved_path"),
        "provenance": {"url": URL, "params": params, "retrieved_at": retrieved_at},
    }
    (ROOT / "second_round_openalex_summary_v0.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(entry, ensure_ascii=False))


if __name__ == "__main__":
    main()

