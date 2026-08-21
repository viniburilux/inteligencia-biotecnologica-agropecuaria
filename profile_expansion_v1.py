import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NORM = ROOT / "normalized_v0"

def load_jsonl(path):
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

works = load_jsonl(NORM / "works_v0.jsonl")
actors = load_jsonl(NORM / "actors_v0.jsonl")
institutions = load_jsonl(NORM / "institutions_v0.jsonl")
relations = load_jsonl(NORM / "relations_v0.jsonl")

actor_by_id = {x.get("actor_id"): x for x in actors}
inst_by_id = {x.get("institution_id"): x for x in institutions}
work_by_id = {x.get("record_id") or x.get("source_id"): x for x in works}

actor_works = defaultdict(set)
inst_works = defaultdict(set)
for rel in relations:
    subject = rel.get("subject_id")
    obj = rel.get("object_id")
    if rel.get("predicate") == "authored_by" and obj in actor_by_id:
        actor_works[obj].add(subject)
    if rel.get("predicate") == "has_institution" and obj in inst_by_id:
        inst_works[obj].add(subject)

organisms = {
    "Trichoderma": ["trichoderma"],
    "Rhizobium": ["rhizobium"],
    "Bacillus": ["bacillus"],
    "Bacillus thuringiensis": ["bacillus thuringiensis", "b. thuringiensis"],
    "Bacillus megaterium": ["bacillus megaterium"],
    "Azospirillum": ["azospirillum"],
    "Bradyrhizobium": ["bradyrhizobium"],
    "Pseudomonas": ["pseudomonas"],
    "Beauveria": ["beauveria"],
    "Metarhizium": ["metarhizium"],
    "Streptomyces": ["streptomyces"],
    "Starmerella bombicola": ["starmerella bombicola"],
    "fungi": ["fungo", "fungos", "fungal", "fungi"],
    "bacteria": ["bactéria", "bactérias", "bacterium", "bacteria"],
    "yeast": ["levedura", "leveduras", "yeast", "yeasts"],
    "algae": ["alga", "algas", "algae"],
    "microorganisms": ["microrganismo", "microrganismos", "microorganism", "microorganisms"],
}

technologies = {
    "bioinput": ["bioinsumo", "bioinsumos", "bioinput", "bioinputs"],
    "biocontrol": ["biocontrole", "biocontrol"],
    "inoculant": ["inoculante", "inoculantes", "inoculant", "inoculants"],
    "biofertilizer": ["biofertilizante", "biofertilizantes", "biofertilizer", "biofertilizers"],
    "biopesticide": ["biopesticida", "biopesticidas", "biopesticide", "biopesticides"],
    "bioreactor": ["biorreator", "biorreator", "bioreator", "bioreactor", "bioreactors"],
    "fermentation": ["fermentação", "fermentacao", "fermentation", "fermentações", "fermentations"],
    "nitrogen_fixation": ["fixação de nitrogênio", "fixacao de nitrogenio", "nitrogen fixation"],
    "phosphate_solubilization": ["solubilização de fosfato", "solubilizacao de fosfato", "phosphate solubilization"],
    "formulation": ["formulação", "formulacao", "formulation", "formulations"],
    "stability": ["estabilidade", "stability", "armazenamento", "storage"],
    "release": ["liberação", "liberacao", "release", "delivery"],
    "rhizosphere": ["rizosfera", "rhizosphere", "saúde radicular", "saude radicular", "root health"],
    "nematode": ["nematoide", "nematóide", "nematode"],
    "on_farm": ["propriedade rural", "on-farm", "on farm", "pequenos agricultores", "smallholder"],
    "quality_monitoring": ["monitoramento", "espectrometria", "spectrometry", "termocromia", "quality monitoring"],
    "co2_biofixation": ["biofixação de co2", "biofixacao de co2", "biofixation", "biomassa de algas", "algal biomass", "cascalho de perfuração", "drilling cuttings"],
    "industrial_bioprocess": ["celulase", "cellulase", "etanol", "ethanol", "enzima", "enzimas", "enzyme", "enzymes", "bioprocesso", "bioprocess", "biorefinaria", "biorefinery"],
}

focus_fields = []
for w in works:
    text_parts = [w.get("title", ""), w.get("snippet", ""), w.get("abstract", ""), " ".join(w.get("application_terms", [])), " ".join(w.get("technology_terms", []))]
    text = " ".join(str(x) for x in text_parts if x).lower()
    focus_fields.append((w, text))

organism_counts = Counter()
organism_works = defaultdict(list)
tech_counts = Counter()
tech_works = defaultdict(list)
cooccurrence = Counter()
for w, text in focus_fields:
    matched_orgs = []
    matched_techs = []
    for name, variants in organisms.items():
        if any(v in text for v in variants):
            organism_counts[name] += 1
            organism_works[name].append(w.get("record_id") or w.get("source_id"))
            matched_orgs.append(name)
    for name, variants in technologies.items():
        if any(v in text for v in variants):
            tech_counts[name] += 1
            tech_works[name].append(w.get("record_id") or w.get("source_id"))
            matched_techs.append(name)
    for i, a in enumerate(sorted(set(matched_techs))):
        for b in sorted(set(matched_techs))[i+1:]:
            cooccurrence[f"{a}__{b}"] += 1

# Focused actor/institution hubs: count works that contain one of the current expansion signals.
focus_tokens = ["bioinput", "bioinsumo", "trichoderma", "ferment", "nitrogen", "nitrogênio", "fosfato", "phosphate", "biorreator", "bioreactor", "co2", "alga", "biofix"]
def is_focus_work(w):
    t = " ".join(str(w.get(k, "")) for k in ("title", "snippet", "abstract")).lower()
    t += " " + " ".join(w.get("application_terms", [])) + " " + " ".join(w.get("technology_terms", []))
    return any(tok in t for tok in focus_tokens)
focus_work_ids = {w.get("record_id") or w.get("source_id") for w in works if is_focus_work(w)}

top_actors = []
for aid, ids in actor_works.items():
    focused = sorted(i for i in ids if i in focus_work_ids)
    if focused:
        x = actor_by_id[aid]
        top_actors.append({"actor_id": aid, "display_name": x.get("display_name"), "focused_work_count": len(focused), "total_work_count": len(ids), "evidence_work_ids": focused[:20]})
top_actors.sort(key=lambda x: (-x["focused_work_count"], -x["total_work_count"], x["display_name"] or ""))

top_institutions = []
for iid, ids in inst_works.items():
    focused = sorted(i for i in ids if i in focus_work_ids)
    if focused:
        x = inst_by_id[iid]
        top_institutions.append({"institution_id": iid, "display_name": x.get("display_name"), "country_code": x.get("country_code"), "type": x.get("type"), "focused_work_count": len(focused), "total_work_count": len(ids), "evidence_work_ids": focused[:20]})
top_institutions.sort(key=lambda x: (-x["focused_work_count"], -x["total_work_count"], x["display_name"] or ""))

source_counts = Counter(w.get("source") for w in works)
query_counts = Counter(w.get("query") for w in works)
org_contexts = {}
for name, ids in organism_works.items():
    contexts = Counter()
    for wid in ids:
        w = work_by_id.get(wid, {})
        txt = " ".join(str(w.get(k, "")) for k in ("title", "snippet", "abstract")).lower()
        for tech, variants in technologies.items():
            if any(v in txt for v in variants):
                contexts[tech] += 1
    org_contexts[name] = {"work_count": len(ids), "technology_contexts": contexts.most_common(12), "evidence_work_ids": ids[:20]}

out = {
    "generated_at": "2026-08-21",
    "metadata_only": True,
    "corpus_counts": {"works": len(works), "actors": len(actors), "institutions": len(institutions), "relations": len(relations)},
    "focus_work_count": len(focus_work_ids),
    "source_counts": source_counts,
    "query_counts": query_counts.most_common(40),
    "organism_counts": organism_counts.most_common(),
    "organism_contexts": org_contexts,
    "technology_counts": tech_counts.most_common(),
    "technology_cooccurrences": cooccurrence.most_common(60),
    "top_actors": top_actors[:60],
    "top_institutions": top_institutions[:60],
    "notes": [
        "Counts are lexical/metadata signals, not entity resolution or technology conclusions.",
        "Actor and institution hubs are ranked by observed relations to focus works.",
        "Patent filter country BR is not treated as proof of Brazilian origin."
    ]
}
(ROOT / "EXPANSION_PROFILE_V1.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"works": len(works), "focus_work_count": len(focus_work_ids), "organisms": organism_counts.most_common(12), "technologies": tech_counts.most_common(15), "top_actors": top_actors[:12], "top_institutions": top_institutions[:12]}, ensure_ascii=False))
