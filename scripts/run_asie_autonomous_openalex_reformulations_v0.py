from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "raw_v3" / "asie_autonomous" / "openalex_reformulations"
OUT.mkdir(parents=True, exist_ok=True)

QUERIES = [
    {
        "id": "A01R",
        "parent": "A01",
        "query": "Trichoderma citrinoviride Meloidogyne incognita",
        "signal": "A01 returned a highly cited direct-study title on T. citrinoviride and M. incognita.",
        "decision_reason": "Replace broad semantic terms with the organism/pathogen pair surfaced by the result list.",
    },
    {
        "id": "A02R",
        "parent": "A02",
        "query": "plant growth promoting rhizobacteria nitrogen fixation maize greenhouse",
        "signal": "A02 returned a direct maize inoculation study and a dense rhizosphere literature corridor.",
        "decision_reason": "Narrow to an application and experimental context instead of the broad rhizosphere universe.",
    },
    {
        "id": "A03R",
        "parent": "A03",
        "query": "Trichoderma root knot nematode biocontrol",
        "signal": "A03 mixed generic PGPR, Bacillus, AMF and Trichoderma results.",
        "decision_reason": "Keep the organism and pest mechanism while removing generic root-colonization vocabulary.",
    },
]


def fetch(item: dict) -> dict:
    params = {
        "search": item["query"],
        "filter": "from_publication_date:2000-01-01,to_publication_date:2026-12-31",
        "per-page": 25,
        "select": "id,doi,title,publication_date,publication_year,type,cited_by_count,language,authorships,primary_location,concepts,related_works",
    }
    url = "https://api.openalex.org/works?" + urlencode(params)
    response = requests.get(url, timeout=45, headers={"User-Agent": "ASIE-autonomous-experiment/0.1"})
    response.raise_for_status()
    data = response.json()
    payload = {
        "query_id": item["id"],
        "parent_query_id": item["parent"],
        "query": item["query"],
        "signal": item["signal"],
        "decision_reason": item["decision_reason"],
        "source": "openalex",
        "request_url": url,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "metadata_only": True,
        "http_status": response.status_code,
        "count": data.get("meta", {}).get("count"),
        "results": data.get("results", []),
    }
    target = OUT / f"{item['id'].lower()}_openalex.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    payload["artifact"] = str(target.relative_to(ROOT))
    payload["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    payload["result_count_captured"] = len(payload["results"])
    payload["top_titles"] = [r.get("title") for r in payload["results"][:10]]
    return payload


def main() -> None:
    records = []
    for item in QUERIES:
        try:
            records.append(fetch(item))
        except Exception as exc:
            records.append({"query_id": item["id"], "parent_query_id": item["parent"], "query": item["query"], "status": "blocked", "error": repr(exc)})
        time.sleep(0.2)
    target = ROOT / "asie_autonomous_openalex_reformulations_v0.json"
    target.write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "metadata_only": True, "queries": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps([{ "id": r.get("query_id"), "query": r.get("query"), "count": r.get("count"), "captured": r.get("result_count_captured"), "status": r.get("http_status", r.get("status")) } for r in records], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
