from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
import requests
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "raw_v3" / "asie_autonomous" / "openalex_reformulations"
OUT.mkdir(parents=True, exist_ok=True)
item = {
    "query_id": "A04R",
    "parent_query_id": "A04",
    "query": "algae drilling cuttings fertilizer Brazil",
    "signal": "A04 returned only 18 works, mostly generic CO2 capture and algae literature, without a direct drilling-waste/fertilizer title in the visible top results.",
    "decision_reason": "Replace biofixation/CCUS vocabulary with the concrete residue and application terms surfaced by the patent trail.",
}
params = {"search": item["query"], "filter": "from_publication_date:2000-01-01,to_publication_date:2026-12-31", "per-page": 25, "select": "id,doi,title,publication_date,publication_year,type,cited_by_count,language,authorships,primary_location,concepts,related_works"}
url = "https://api.openalex.org/works?" + urlencode(params)
r = requests.get(url, timeout=45, headers={"User-Agent": "ASIE-autonomous-experiment/0.1"})
r.raise_for_status()
data = r.json()
payload = {**item, "source": "openalex", "request_url": url, "captured_at": datetime.now(timezone.utc).isoformat(), "metadata_only": True, "http_status": r.status_code, "count": data.get("meta", {}).get("count"), "results": data.get("results", [])}
target = OUT / "a04r_openalex.json"
target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
summary = {"artifact": str(target.relative_to(ROOT)), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "query_id": item["query_id"], "query": item["query"], "count": payload["count"], "captured": len(payload["results"]), "top_titles": [x.get("title") for x in payload["results"][:12]], "source": "openalex", "metadata_only": True}
(ROOT / "asie_autonomous_carbon_reformulation_v0.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
