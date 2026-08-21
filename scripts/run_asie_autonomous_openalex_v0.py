from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "raw_v3" / "asie_autonomous" / "openalex"
OUT.mkdir(parents=True, exist_ok=True)

QUERIES = [
    {
        "id": "A01",
        "block": "fungus_nematode_crop",
        "query": "Trichoderma nematode root health soybean",
        "source_signal": "Fungo + nematoide + soja + biocontrole appeared as a dense cooccurrence; Portuguese patent reformulation opened BR112019020483A2.",
        "why": "Contrast the identifier-led patent signal with literature and test whether the bridge is broader than one patent family.",
    },
    {
        "id": "A02",
        "block": "microbial_root_health",
        "query": "microbial nitrogen fixation root health maize rhizosphere",
        "source_signal": "Fixacao_nitrogenio + saude_radicular cooccurred in 9 works; the autonomous patent query returned Locus family BR112020022643A2.",
        "why": "Test whether the Locus/root-health bridge has a bibliographic counterpart and identify organisms or crops that refine the next query.",
    },
    {
        "id": "A03",
        "block": "fungal_biocontrol_nematode",
        "query": "fungal biocontrol nematode plant root colonization",
        "source_signal": "Fungo + biocontrole + nematoide cooccurred in the cumulative application signal layer; patent retrieval was noisy in English and more concentrated in Portuguese.",
        "why": "Use a mechanism-oriented literature query to distinguish direct nematode control, root colonization and generic fungicide noise.",
    },
    {
        "id": "A04",
        "block": "algae_industrial_residue",
        "query": "microalgae drilling waste biofixation fertilizer",
        "source_signal": "The carbon/algae trail survived one identifier-specific patent reformulation but remains narrow and needs independent literature contrast.",
        "why": "Test whether the Petrobras-related family sits inside a broader research corridor or is an isolated patent signal.",
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
    captured_at = datetime.now(timezone.utc).isoformat()
    response = requests.get(url, timeout=45, headers={"User-Agent": "ASIE-autonomous-experiment/0.1"})
    response.raise_for_status()
    data = response.json()
    payload = {
        "query_id": item["id"],
        "block": item["block"],
        "query": item["query"],
        "source_signal": item["source_signal"],
        "why": item["why"],
        "source": "openalex",
        "request_url": url,
        "captured_at": captured_at,
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
            records.append({
                "query_id": item["id"],
                "block": item["block"],
                "query": item["query"],
                "source_signal": item["source_signal"],
                "why": item["why"],
                "source": "openalex",
                "metadata_only": True,
                "status": "blocked",
                "error": repr(exc),
            })
        time.sleep(0.2)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metadata_only": True,
        "queries": records,
        "total_queries": len(records),
        "successful_queries": sum(1 for r in records if r.get("http_status") == 200),
        "artifacts": [r.get("artifact") for r in records if r.get("artifact")],
    }
    target = ROOT / "asie_autonomous_openalex_summary_v0.json"
    target.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(target),
        "queries": [
            {"id": r.get("query_id"), "query": r.get("query"), "count": r.get("count"), "captured": r.get("result_count_captured"), "status": r.get("http_status", r.get("status"))}
            for r in records
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
