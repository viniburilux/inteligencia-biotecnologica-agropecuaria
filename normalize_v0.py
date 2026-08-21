#!/usr/bin/env python3
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_v0"
OUT = ROOT / "normalized_v0"
MANIFEST = ROOT / "ingestion_manifest_v0.jsonl"

APPLICATION_TERMS = {
    "bioinsumo": ["bioinsumo", "bioinsumos", "bioinput", "bioinputs"],
    "biocontrole": ["biocontrole", "biocontrol", "biological control", "controle biologico"],
    "inoculante": ["inoculante", "inoculant", "inoculation"],
    "biopesticida": ["biopesticide", "biopesticidas"],
    "promocao_crescimento": ["promotor de crescimento", "plant growth promoting", "growth-promoting"],
    "biofertilizante": ["biofertilizante", "biofertilizer"],
    "fungo": ["fungo", "fungi", "fungal", "trichoderma", "metarhizium", "bacillus"],
    "nematoide": ["nematoide", "nematode", "meloidogyne", "pratylenchus"],
    "soja": ["soja", "soybean"],
    "milho": ["milho", "maize", "corn"],
    "fixacao_nitrogenio": ["fixação de nitrogênio", "nitrogen fixation", "nitrogen-fixing", "nitrogen fixing"],
    "solubilizacao_fosfato": ["solubilização de fosfato", "phosphate solubilization"],
    "saude_radicular": ["saúde radicular", "root health", "rhizosphere", "rizosfera", "phytosanity", "fitossanidade"],
    "sequestro_carbono": ["sequestro de carbono", "carbon sequestration", "sequestering improved carbon", "greenhouse gases"],
    "fermentacao_bioprocesso": ["fermentação", "fermentation", "bioreactor", "biorreator", "solid substrate", "substrato sólido"],
    "monitoramento_qualidade": ["monitoramento", "monitoring", "spectrometry", "espectrometria", "thermochromy", "termocromia", "physicochemical"],
}


def norm(value):
    value = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def rid(prefix, *parts):
    raw = "|".join(norm(p) for p in parts if p is not None)
    return f"{prefix}_{hashlib.sha256(raw.encode()).hexdigest()[:20]}"


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def terms_for(title, subtitle=""):
    text = norm(f"{title} {subtitle}")
    return sorted(label for label, terms in APPLICATION_TERMS.items() if any(norm(term) in text for term in terms))


def load_manifest():
    return [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]


def openalex_rows(manifest):
    works, actors, institutions, relations, signals = [], [], [], [], []
    for entry in manifest:
        if entry.get("source") != "openalex" or entry.get("status") != "captured":
            continue
        payload = json.loads((ROOT / entry["saved_path"]).read_text(encoding="utf-8"))
        for item in payload.get("results", []) or []:
            title = item.get("title") or ""
            work_id = item.get("id") or rid("work", "openalex", title, item.get("publication_year"))
            doi = item.get("doi")
            app_terms = terms_for(title)
            work = {
                "record_id": work_id,
                "entity_type": "work",
                "source": "openalex",
                "source_id": item.get("id"),
                "query": entry.get("query"),
                "title": title,
                "doi": doi,
                "publication_year": item.get("publication_year"),
                "publication_date": item.get("publication_date"),
                "type": item.get("type"),
                "language": item.get("language"),
                "cited_by_count": item.get("cited_by_count"),
                "primary_location": item.get("primary_location"),
                "best_oa_location": item.get("best_oa_location"),
                "concepts": [{"id": x.get("id"), "display_name": x.get("display_name"), "score": x.get("score")} for x in item.get("concepts", []) or []],
                "application_terms": app_terms,
                "status": "captured",
                "provenance": {"manifest_path": "ingestion_manifest_v0.jsonl", "raw_path": entry.get("saved_path"), "raw_sha256": entry.get("saved_sha256")},
            }
            works.append(work)
            if app_terms:
                signals.append({"signal_id": rid("signal", work_id, "|".join(app_terms)), "signal_type": "application_term_in_title", "work_id": work_id, "terms": app_terms, "observed_text": title, "source": "openalex", "query": entry.get("query"), "status": "captured", "provenance": work["provenance"]})
            for authorship in item.get("authorships", []) or []:
                author = authorship.get("author") or {}
                if author.get("id") or author.get("display_name"):
                    actor_id = author.get("id") or rid("actor", author.get("display_name"))
                    actors.append({"actor_id": actor_id, "entity_type": "actor", "source": "openalex", "source_id": author.get("id"), "display_name": author.get("display_name"), "works_count": author.get("works_count"), "cited_by_count": author.get("cited_by_count"), "provenance": work["provenance"]})
                    relations.append({"relation_id": rid("rel", work_id, actor_id, "authored"), "subject_id": work_id, "predicate": "authored_by", "object_id": actor_id, "status": "observed", "provenance": work["provenance"]})
                for inst in authorship.get("institutions", []) or []:
                    if not (inst.get("id") or inst.get("display_name")):
                        continue
                    inst_id = inst.get("id") or rid("institution", inst.get("display_name"))
                    institutions.append({"institution_id": inst_id, "entity_type": "institution", "source": "openalex", "source_id": inst.get("id"), "display_name": inst.get("display_name"), "ror": inst.get("ror"), "country_code": inst.get("country_code"), "type": inst.get("type"), "provenance": work["provenance"]})
                    relations.append({"relation_id": rid("rel", work_id, inst_id, "affiliated"), "subject_id": work_id, "predicate": "has_institution", "object_id": inst_id, "status": "observed", "provenance": work["provenance"]})
    return works, actors, institutions, relations, signals


def crossref_rows(manifest):
    works, actors, relations, signals = [], [], [], []
    for entry in manifest:
        if entry.get("source") != "crossref" or entry.get("status") != "captured":
            continue
        payload = json.loads((ROOT / entry["saved_path"]).read_text(encoding="utf-8"))
        for item in payload.get("message", {}).get("items", []) or []:
            title = (item.get("title") or [""])[0]
            doi = item.get("DOI")
            work_id = f"https://doi.org/{doi.lower()}" if doi else rid("work", "crossref", title, item.get("published"))
            app_terms = terms_for(title, " ".join(item.get("subject", []) or []))
            provenance = {"manifest_path": "ingestion_manifest_v0.jsonl", "raw_path": entry.get("saved_path"), "raw_sha256": entry.get("saved_sha256")}
            works.append({"record_id": work_id, "entity_type": "work", "source": "crossref", "source_id": doi, "query": entry.get("query"), "title": title, "doi": doi, "publication": item.get("published"), "container_title": item.get("container-title"), "type": item.get("type"), "subject": item.get("subject"), "url": item.get("URL"), "relation": item.get("relation"), "link": item.get("link"), "application_terms": app_terms, "status": "captured", "provenance": provenance})
            if app_terms:
                signals.append({"signal_id": rid("signal", work_id, "|".join(app_terms)), "signal_type": "application_term_in_title_or_subject", "work_id": work_id, "terms": app_terms, "observed_text": title, "source": "crossref", "query": entry.get("query"), "status": "captured", "provenance": provenance})
            for author in item.get("author", []) or []:
                name = " ".join(x for x in [author.get("given"), author.get("family")] if x)
                if name:
                    actor_id = rid("actor", name)
                    actors.append({"actor_id": actor_id, "entity_type": "actor", "source": "crossref", "source_id": author.get("ORCID"), "display_name": name, "orcid": author.get("ORCID"), "provenance": provenance})
                    relations.append({"relation_id": rid("rel", work_id, actor_id, "authored"), "subject_id": work_id, "predicate": "authored_by", "object_id": actor_id, "status": "observed", "provenance": provenance})
    return works, actors, relations, signals


def looks_like_institution(name):
    text = norm(name)
    markers = [
        "universidade", "university", "instituto", "institute", "fundacao", "foundation",
        "corporation", "corporacao", "company", "inc", "llc", "ltda", "limited", "agencia",
        "agency", "bayer", "basf", "syngenta", "pivot bio", "monsanto", "pioneer", "usp",
        "embrapa", "agrosavia", "novozymes", "terragen", "locus", "dosaggio", "mcti",
    ]
    return any(marker in text for marker in markers)


def google_patents_rows(manifest):
    works_by_id = {}
    actors_by_id = {}
    institutions_by_id = {}
    relations_by_id = {}
    signals_by_id = {}
    for entry in manifest:
        if entry.get("source") != "google_patents" or entry.get("status") != "captured":
            continue
        path = ROOT / entry["saved_path"]
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            source_id = item.get("source_id") or item.get("identifiers", {}).get("publication_number")
            if not source_id:
                continue
            work_id = f"patent:{source_id}"
            title = item.get("title") or source_id
            description = item.get("description_or_abstract") or ""
            app_terms = terms_for(title, description)
            provenance = {
                "manifest_path": "ingestion_manifest_v0.jsonl",
                "raw_path": entry.get("saved_path"),
                "raw_sha256": entry.get("saved_sha256"),
                "source_url": item.get("source_url") or entry.get("url"),
                "retrieved_at": item.get("retrieved_at") or entry.get("retrieved_at"),
            }
            if work_id not in works_by_id:
                works_by_id[work_id] = {
                    "record_id": work_id,
                    "entity_type": "patent",
                    "source": "google_patents",
                    "source_id": source_id,
                    "query": item.get("query") or entry.get("query"),
                    "matched_queries": [item.get("query") or entry.get("query")],
                    "title": title,
                    "description_or_abstract": description,
                    "dates": item.get("dates", {}),
                    "publication_number": source_id,
                    "actors": item.get("actors", {}),
                    "institutions": item.get("institutions", []),
                    "geography": item.get("geography", {}),
                    "classifications": item.get("classifications", []),
                    "identifiers": item.get("identifiers", {}),
                    "application_terms": app_terms,
                    "metadata_only": True,
                    "status": "captured",
                    "provenance": provenance,
                }
            else:
                existing = works_by_id[work_id]
                matched_query = item.get("query") or entry.get("query")
                if matched_query and matched_query not in existing["matched_queries"]:
                    existing["matched_queries"].append(matched_query)
            work = works_by_id[work_id]
            for role, predicate in (("inventors", "invented_by"), ("assignees", "assigned_to")):
                for name in item.get("actors", {}).get(role, []) or []:
                    actor_id = rid("actor", "google_patents", name)
                    actors_by_id.setdefault(actor_id, {"actor_id": actor_id, "entity_type": "actor", "source": "google_patents", "source_id": None, "display_name": name, "roles": [], "provenance": provenance})
                    if role[:-1] not in actors_by_id[actor_id]["roles"]:
                        actors_by_id[actor_id]["roles"].append(role[:-1])
                    relation_id = rid("rel", work_id, actor_id, predicate)
                    relations_by_id.setdefault(relation_id, {"relation_id": relation_id, "subject_id": work_id, "predicate": predicate, "object_id": actor_id, "status": "observed", "provenance": provenance})
                    if role == "assignees" and looks_like_institution(name):
                        inst_id = rid("institution", "google_patents", name)
                        institutions_by_id.setdefault(inst_id, {"institution_id": inst_id, "entity_type": "institution", "source": "google_patents", "source_id": None, "display_name": name, "provenance": provenance})
                        inst_rel_id = rid("rel", work_id, inst_id, "assigned_to_institution")
                        relations_by_id.setdefault(inst_rel_id, {"relation_id": inst_rel_id, "subject_id": work_id, "predicate": "assigned_to_institution", "object_id": inst_id, "status": "observed", "provenance": provenance})
            if app_terms:
                signal_id = rid("signal", work_id, "|".join(app_terms))
                signals_by_id.setdefault(signal_id, {"signal_id": signal_id, "signal_type": "application_term_in_title_or_snippet", "work_id": work_id, "terms": app_terms, "observed_text": f"{title} {description}".strip(), "source": "google_patents", "query": item.get("query") or entry.get("query"), "status": "captured", "provenance": provenance})
    return list(works_by_id.values()), list(actors_by_id.values()), list(institutions_by_id.values()), list(relations_by_id.values()), list(signals_by_id.values())


def dedup(rows, key):
    seen = {}
    duplicates = 0
    for row in rows:
        value = row.get(key)
        if not value:
            value = rid("anon", row.get("title"), row.get("display_name"), row.get("source"))
        if value in seen:
            duplicates += 1
            continue
        seen[value] = row
    return list(seen.values()), duplicates


def main():
    manifest = load_manifest()
    oworks, oactors, oinstitutions, orelations, osignals = openalex_rows(manifest)
    cworks, cactors, crelations, csignals = crossref_rows(manifest)
    pworks, pactors, pinstitutions, prelations, psignals = google_patents_rows(manifest)
    works, work_dups = dedup(oworks + cworks + pworks, "record_id")
    actors, actor_dups = dedup(oactors + cactors + pactors, "actor_id")
    institutions, institution_dups = dedup(oinstitutions + pinstitutions, "institution_id")
    relations, relation_dups = dedup(orelations + crelations + prelations, "relation_id")
    signals, signal_dups = dedup(osignals + csignals + psignals, "signal_id")
    OUT.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT / "works_v0.jsonl", works)
    write_jsonl(OUT / "actors_v0.jsonl", actors)
    write_jsonl(OUT / "institutions_v0.jsonl", institutions)
    write_jsonl(OUT / "relations_v0.jsonl", relations)
    write_jsonl(OUT / "application_signals_v0.jsonl", signals)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metadata_only": True,
        "source_manifest": "ingestion_manifest_v0.jsonl",
        "counts": {"works": len(works), "actors": len(actors), "institutions": len(institutions), "relations": len(relations), "application_signals": len(signals)},
        "duplicates_removed": {"works": work_dups, "actors": actor_dups, "institutions": institution_dups, "relations": relation_dups, "application_signals": signal_dups},
        "source_mix": dict(Counter(row.get("source") for row in works)),
        "application_term_counts": dict(Counter(term for row in signals for term in row.get("terms", []))),
        "work_source_status": {"openalex": len(oworks), "crossref": len(cworks), "google_patents": len(pworks)},
        "notes": ["No PDFs, full-text patent documents, sequences, or scientific data files were downloaded.", "Relations are observed only when returned by source authorship/affiliation metadata or visible patent result metadata.", "Cross-source actor deduplication is conservative and not entity resolution.", "Google Patents rows are parsed from browser-captured result metadata and preserve the BR search filter as context, not as origin proof."]
    }
    (OUT / "normalization_summary_v0.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
