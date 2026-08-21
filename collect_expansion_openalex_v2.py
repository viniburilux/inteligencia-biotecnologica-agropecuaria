import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
QUERY_FILE = ROOT / "EXPANSION_QUERIES_V2.json"
RAW_DIR = ROOT / "raw_v2" / "openalex"
MANIFEST = ROOT / "ingestion_manifest_v2.jsonl"
SUMMARY = ROOT / "expansion_openalex_summary_v2.json"

queries = [q for q in json.loads(QUERY_FILE.read_text(encoding="utf-8"))["queries"] if q["source"] == "openalex"]
RAW_DIR.mkdir(parents=True, exist_ok=True)
session = requests.Session()
session.headers.update({"User-Agent": "InteligenciaBiotecnologicaAgropecuaria/1.0 (metadata-only; contact: viniburilux@gmail.com)"})
results = []
with MANIFEST.open("a", encoding="utf-8") as mf:
    for q in queries:
        params = {"search": q["query"], "filter": "from_publication_date:2010-01-01,to_publication_date:2026-12-31", "per-page": 25}
        url = "https://api.openalex.org/works"
        retrieved_at = datetime.now(timezone.utc).isoformat()
        try:
            r = session.get(url, params=params, timeout=45)
            r.raise_for_status()
            payload = r.json()
            status = "captured"
            error = None
            source_url = r.url
        except Exception as exc:
            payload = {"meta": {}, "results": [], "error": str(exc)}
            status = "blocked"
            error = str(exc)
            source_url = url
        raw_bytes = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        safe_id = q["id"].lower().replace("-", "_")
        safe_query = "_".join("".join(ch if ch.isalnum() else "_" for ch in q["query"].lower()).split())[:70]
        raw_path = RAW_DIR / f"{safe_id}_{safe_query}.json"
        raw_path.write_bytes(raw_bytes)
        sha = hashlib.sha256(raw_bytes).hexdigest()
        entry = {
            "round": "expansion_v2",
            "query_id": q["id"],
            "trail": q["trail"],
            "query": q["query"],
            "source": "openalex",
            "source_url": source_url,
            "retrieved_at": retrieved_at,
            "status": status,
            "observed_total": payload.get("meta", {}).get("count"),
            "returned_items": len(payload.get("results", [])),
            "raw_path": str(raw_path.relative_to(ROOT)),
            "raw_sha256": sha,
            "evidence_ids": q.get("evidence_ids", []),
        }
        if error:
            entry["error"] = error
        mf.write(json.dumps(entry, ensure_ascii=False) + "\n")
        results.append(entry)
        time.sleep(0.4)
summary = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "round": "expansion_v2",
    "metadata_only": True,
    "query_count": len(queries),
    "captured_queries": sum(x["status"] == "captured" for x in results),
    "blocked_queries": sum(x["status"] == "blocked" for x in results),
    "total_observed": sum(x["observed_total"] or 0 for x in results),
    "total_returned": sum(x["returned_items"] for x in results),
    "queries": results,
    "notes": ["No full texts or scientific data were downloaded.", "This manifest is separate from V0, second-round V0 and expansion V1 manifests."]
}
SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
