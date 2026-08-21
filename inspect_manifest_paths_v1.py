import json
from pathlib import Path

root = Path(__file__).resolve().parent
for name in ["ingestion_manifest_v0.jsonl", "ingestion_manifest_v1.jsonl"]:
    path = root / name
    if not path.exists():
        continue
    missing = []
    samples = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not row.get("saved_path"):
            missing.append({"line": line_no, "source": row.get("source"), "round": row.get("round"), "query_id": row.get("query_id"), "keys": sorted(row.keys())})
        elif len(samples) < 2:
            samples.append({"line": line_no, "source": row.get("source"), "round": row.get("round"), "saved_path": row.get("saved_path")})
    print(json.dumps({"manifest": name, "missing_count": len(missing), "missing_examples": missing[:8], "samples": samples}, ensure_ascii=False))
