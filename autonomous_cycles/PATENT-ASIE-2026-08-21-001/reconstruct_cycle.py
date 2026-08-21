from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

required = ["state_initial.json", "state_final.json", "questions_executed.json", "decisions.json", "evidence_collection.json", "browser_evidence.json", "new_relations.json", "next_questions.json", "source_references.json"]
missing = [name for name in required if not (ROOT / name).exists()]
if missing:
    raise SystemExit("missing required artifacts: " + ", ".join(missing))
state = json.loads((ROOT / "state_final.json").read_text(encoding="utf-8"))
queries = json.loads((ROOT / "queries_executed.json").read_text(encoding="utf-8"))
print(json.dumps({"cycle_id": state["cycle_id"], "state_version": state["state_version"], "status": state["status"], "metadata_api_queries": len(queries["metadata_api_queries"]), "rendered_browser_queries": len(queries["rendered_browser_queries"]), "stop_reason": state["stop_reason"]}, ensure_ascii=False, indent=2))
