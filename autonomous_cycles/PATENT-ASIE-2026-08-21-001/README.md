# PATENT-ASIE-2026-08-21-001

This directory contains the public, metadata-only artifacts from the first autonomous discovery cycle over `viniburilux/inteligencia-biotecnologica-agropecuaria`. It is an `OVERNIGHT_DRAFT` and does not expose the private OI/ASIE implementation or private research state.

## Reconstructing the artifact state

From this directory, run:

```bash
python3 reconstruct_cycle.py
```

The command checks the required public artifacts and prints the final sanitized state. The raw API responses under `raw/`, `raw_reformulation_v1/`, `raw_reformulation_v2/`, `raw_reformulation_v3/`, `raw_crossref_v1/` and `raw_crossref_v2/` are preserved with the hashes referenced by the collection artifacts.

Google Patents is dynamically rendered. The direct HTTP shell responses are intentionally preserved only to document the discarded route; rendered-browser observations are captured in `browser_evidence.json` and `browser_patent_findings.md`.

The main human-readable synthesis is [`EXECUTIVE_MAP_UPDATE.md`](EXECUTIVE_MAP_UPDATE.md). The machine-readable state transition is in [`state_initial.json`](state_initial.json) and [`state_final.json`](state_final.json). Questions and decisions are in [`questions_executed.json`](questions_executed.json), [`decisions.json`](decisions.json) and [`next_questions.json`](next_questions.json).
