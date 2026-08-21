import collections
import json
from pathlib import Path

root = Path(__file__).resolve().parent
counts = collections.Counter()
for line in (root / "ingestion_manifest_v0.jsonl").read_text(encoding="utf-8").splitlines():
    if line.strip():
        row = json.loads(line)
        counts[(row.get("source"), row.get("status"))] += 1
print(json.dumps({f"{source}:{status}": count for (source, status), count in sorted(counts.items())}, ensure_ascii=False, indent=2))
