import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_v2" / "openalex_followup"
MANIFEST = ROOT / "ingestion_manifest_v2.jsonl"
QUERIES = [
    ("q13_trichoderma_sophorolipids_biocontrol_brazil", "Trichoderma harzianum sophorolipids biocontrol Brazil"),
    ("q14_microbial_inoculant_polymer_stability_nitrogen", "microbial inoculant polymer stability nitrogen fixation"),
    ("q15_on_farm_bioinput_fermentation_brazil", "on farm bioinput fermentation Brazil"),
    ("q16_microalgae_co2_industrial_waste_fertilizer_brazil", "microalgae CO2 fixation industrial waste fertilizer Brazil"),
    ("q17_bacillus_velezensis_biofertilizer_nematode_brazil", "Bacillus velezensis biofertilizer nematode Brazil"),
]

RAW.mkdir(parents=True, exist_ok=True)
headers = {"User-Agent": "inteligencia-biotecnologica-agropecuaria/1.0 (metadata-only research)"}
session = requests.Session()
retry = Retry(total=4, connect=4, read=4, backoff_factor=1.0, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"])
session.mount("https://", HTTPAdapter(max_retries=retry))
manifest_rows = []
for query_id, query in QUERIES:
    url = "https://api.openalex.org/works?search=" + quote(query) + "&per-page=10&mailto=viniburilux@gmail.com"
    retrieved_at = datetime.now(timezone.utc).isoformat()
    response = session.get(url, headers=headers, timeout=(15, 90), stream=False)
    response.raise_for_status()
    payload = response.json()
    path = RAW / f"{query_id}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    raw = path.read_bytes()
    manifest_rows.append({
        "manifest_version": "v2",
        "batch": "radiography_v1_followup",
        "query_id": query_id,
        "source": "openalex",
        "query": query,
        "url": url,
        "retrieved_at": retrieved_at,
        "status": "captured",
        "raw_path": str(path.relative_to(ROOT)),
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "returned_items": len(payload.get("results", [])),
        "observed_result_count": payload.get("meta", {}).get("count"),
        "metadata_only": True,
        "notes": ["OpenAlex metadata response only; no full text or scientific data downloaded."]
    })
    time.sleep(0.4)
with MANIFEST.open("a", encoding="utf-8") as f:
    for row in manifest_rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
summary = {"batch": "radiography_v1_followup", "queries": len(manifest_rows), "returned_items": sum(row["returned_items"] for row in manifest_rows), "rows": manifest_rows}
(ROOT / "radiography_followup_openalex_summary_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"queries": len(manifest_rows), "returned_items": summary["returned_items"], "manifest": str(MANIFEST)}, ensure_ascii=False))
