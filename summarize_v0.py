#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_v0"
MANIFEST = ROOT / "ingestion_manifest_v0.jsonl"
OUT = ROOT / "ingestion_summary_v0.json"


def text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(text(x) for x in value)
    if isinstance(value, dict):
        return " ".join(text(v) for v in value.values())
    return str(value)


def sha256_path(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize_openalex(payload, query):
    items = payload.get("results", []) if isinstance(payload, dict) else []
    years = Counter()
    countries = Counter()
    institutions = Counter()
    concepts = Counter()
    ids = []
    titles = []
    for item in items:
        ids.append(item.get("id"))
        titles.append(item.get("title"))
        year = item.get("publication_year")
        if year:
            years[str(year)] += 1
        for auth in item.get("authorships", []) or []:
            for inst in auth.get("institutions", []) or []:
                if inst.get("display_name"):
                    institutions[inst["display_name"]] += 1
                for country in inst.get("country_code"),:
                    if country:
                        countries[country] += 1
        for concept in item.get("concepts", []) or []:
            if concept.get("display_name"):
                concepts[concept["display_name"]] += 1
    return {
        "source": "openalex",
        "query": query,
        "records": len(items),
        "years": dict(years),
        "countries": dict(countries.most_common(20)),
        "institutions": dict(institutions.most_common(20)),
        "concepts": dict(concepts.most_common(20)),
        "ids": ids,
        "titles": titles,
    }


def summarize_crossref(payload, query):
    message = payload.get("message", {}) if isinstance(payload, dict) else {}
    items = message.get("items", []) or []
    years = Counter()
    types = Counter()
    containers = Counter()
    ids = []
    titles = []
    for item in items:
        doi = item.get("DOI")
        if doi:
            ids.append(doi)
        title = (item.get("title") or [None])[0]
        titles.append(title)
        date = item.get("published", {}).get("date-parts", [[None]])[0]
        if date and date[0]:
            years[str(date[0])] += 1
        if item.get("type"):
            types[item["type"]] += 1
        for container in item.get("container-title", []) or []:
            containers[container] += 1
    return {
        "source": "crossref",
        "query": query,
        "records": len(items),
        "years": dict(years),
        "types": dict(types),
        "containers": dict(containers.most_common(20)),
        "ids": ids,
        "titles": titles,
    }


def main():
    manifest = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
    captured = [row for row in manifest if row.get("status") == "captured"]
    source_files = []
    for row in captured:
        path = ROOT / row["saved_path"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        source_files.append({
            "source": row["source"],
            "query": row["query"],
            "path": row["saved_path"],
            "sha256": sha256_path(path),
            "bytes": path.stat().st_size,
        })
    summaries = []
    for entry in source_files:
        payload = json.loads((ROOT / entry["path"]).read_text(encoding="utf-8"))
        if entry["source"] == "openalex":
            summaries.append(summarize_openalex(payload, entry["query"]))
        elif entry["source"] == "crossref":
            summaries.append(summarize_crossref(payload, entry["query"]))
        else:
            summaries.append({"source": entry["source"], "query": entry["query"], "records": entry.get("returned_items", 0)})
    output = {
        "manifest_entries": len(manifest),
        "captured_entries": len(captured),
        "blocked_entries": sum(1 for row in manifest if row.get("status") == "blocked"),
        "source_files": source_files,
        "summaries": summaries,
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUT), "captured_entries": len(captured), "summary_count": len(summaries)}))


if __name__ == "__main__":
    main()
