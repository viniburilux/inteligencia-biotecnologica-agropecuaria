from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NORM = ROOT / "normalized_v2"
OUT = ROOT / "asie_autonomy_state_v0.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9áéíóúãõçüàèìòùâêîôûñ_]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def contains(text: str, terms: list[str]) -> bool:
    value = normalize(text)
    return all(normalize(t) in value for t in terms)


def main() -> None:
    works = read_jsonl(NORM / "works_v2.jsonl")
    signals = read_jsonl(NORM / "application_signals_v2.jsonl")
    relations = read_jsonl(NORM / "relations_v2.jsonl")
    summary = json.loads((NORM / "normalization_summary_v2.json").read_text(encoding="utf-8"))

    source_counts = collections.Counter(w.get("source") for w in works)
    query_counts = collections.Counter(w.get("query") for w in works)
    title_records = []
    for w in works:
        title_records.append({
            "record_id": w.get("record_id"),
            "source": w.get("source"),
            "title": w.get("title"),
            "query": w.get("query"),
            "year": w.get("publication_year"),
            "doi": w.get("doi"),
            "provenance": w.get("provenance"),
        })

    signal_counts = collections.Counter()
    signal_work_ids: dict[str, set[str]] = collections.defaultdict(set)
    signal_text_examples: dict[str, list[str]] = collections.defaultdict(list)
    for s in signals:
        for term in s.get("terms", []):
            term = str(term)
            signal_counts[term] += 1
            wid = s.get("work_id")
            if wid:
                signal_work_ids[term].add(wid)
            if s.get("observed_text") and len(signal_text_examples[term]) < 5:
                signal_text_examples[term].append(s["observed_text"])

    # Co-occurrence of application terms within the same work. This is a signal
    # inventory, not a semantic conclusion.
    work_terms: dict[str, set[str]] = collections.defaultdict(set)
    for s in signals:
        wid = s.get("work_id")
        if wid:
            work_terms[wid].update(str(t) for t in s.get("terms", []))
    cooccurrence = collections.Counter()
    for terms in work_terms.values():
        terms = sorted(terms)
        for i, a in enumerate(terms):
            for b in terms[i + 1:]:
                cooccurrence[(a, b)] += 1

    # Extract common names/processes directly from titles and queries for human
    # inspection, while keeping the underlying corpus untouched.
    anchors = [
        "Trichoderma", "Bacillus", "Rhizobium", "Azospirillum", "Pseudomonas",
        "microalgae", "algae", "bioinput", "bioinsumo", "inoculant", "inoculante",
        "fermentation", "fermentação", "bioreactor", "biorreator", "spectroscopy",
        "espectrometria", "quality", "qualidade", "nematode", "nematoide",
        "phosphate", "phosphorus", "nitrogen", "nitrogênio", "sophorolipid",
        "cellulase", "ethanol", "CO2", "carbon", "carbono", "drilling", "cascalho",
        "smallholder", "pequeno agricultor", "rhizosphere", "rizosfera",
    ]
    anchor_hits = {}
    for anchor in anchors:
        hits = [r for r in title_records if contains((r.get("title") or "") + " " + (r.get("query") or ""), [anchor])]
        anchor_hits[anchor] = {
            "count": len(hits),
            "records": hits[:25],
        }

    # Relation predicate distribution and high-degree nodes from observed edges.
    predicate_counts = collections.Counter(r.get("predicate") for r in relations)
    degree = collections.Counter()
    for r in relations:
        degree[r.get("subject_id")] += 1
        degree[r.get("object_id")] += 1

    payload = {
        "metadata_only": True,
        "generated_at": "2026-08-21",
        "corpus_root": str(ROOT),
        "input_files": [
            "normalized_v2/works_v2.jsonl",
            "normalized_v2/application_signals_v2.jsonl",
            "normalized_v2/relations_v2.jsonl",
            "normalized_v2/normalization_summary_v2.json",
        ],
        "input_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [NORM / "works_v2.jsonl", NORM / "application_signals_v2.jsonl", NORM / "relations_v2.jsonl", NORM / "normalization_summary_v2.json"]
        },
        "summary": summary,
        "source_counts": dict(source_counts),
        "query_counts": dict(query_counts),
        "top_signal_counts": signal_counts.most_common(80),
        "top_cooccurrences": [
            {"terms": list(pair), "work_count": n}
            for pair, n in cooccurrence.most_common(120)
        ],
        "predicate_counts": dict(predicate_counts),
        "top_degree_nodes": degree.most_common(80),
        "anchor_hits": anchor_hits,
        "signal_examples": {k: v for k, v in sorted(signal_text_examples.items())},
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUT),
        "works": len(works),
        "signals": len(signals),
        "relations": len(relations),
        "top_signals": signal_counts.most_common(20),
        "top_cooccurrences": [{"terms": list(k), "work_count": v} for k, v in cooccurrence.most_common(20)],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
