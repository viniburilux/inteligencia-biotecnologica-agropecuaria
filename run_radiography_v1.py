import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NORM = ROOT / "normalized_v2"
WORKS = NORM / "works_v2.jsonl"
ACTORS = NORM / "actors_v2.jsonl"
INSTITUTIONS = NORM / "institutions_v2.jsonl"
RELATIONS = NORM / "relations_v2.jsonl"
SIGNALS = NORM / "application_signals_v2.jsonl"
OUT_MD = ROOT / "EXPLORATORY_RADIOGRAPHY_V1.md"
OUT_MEMBERSHIPS = ROOT / "cluster_memberships_v1.jsonl"
OUT_QUERIES = ROOT / "next_queries_v1.json"
OUT_METHOD = ROOT / "RADIOGRAPHY_METHOD_V1.md"
OUT_SUMMARY = ROOT / "radiography_summary_v1.json"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def fold(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).lower()
    value = value.replace("—", "-")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value)).strip()


def text_of(work):
    values = [work.get("title"), work.get("description_or_abstract"), work.get("query")]
    values.extend(work.get("matched_queries") or [])
    values.extend((work.get("actors") or {}).get("inventors", []))
    values.extend((work.get("actors") or {}).get("assignees", []))
    return " ".join(str(v or "") for v in values)


def year_of(work):
    for key in ("published_date", "priority_date", "filed_date"):
        value = (work.get("dates") or {}).get(key)
        if value:
            match = re.search(r"(19|20)\d{2}", str(value))
            if match:
                return int(match.group(0))
    if work.get("publication_year"):
        try:
            return int(work["publication_year"])
        except (TypeError, ValueError):
            pass
    return None


def origin_state(work):
    if work.get("source") != "google_patents":
        return "not_applicable"
    value = fold(text_of(work))
    local = ["universidade de sao paulo", "usp", "ueba", "mcti", "museu paraense", "apta", "embrapa", "universidade federal", "universidade estadual", "simple agro", "solubio", "petrobras", "dosaggio", "gi industria"]
    international = ["pivot bio", "basf", "syngenta", "monsanto", "bayer", "pioneer hi bred", "locus", "novozymes", "terragen", "agrospheres", "boost biomes", "fmc", "corteva"]
    if any(marker in value for marker in local):
        return "brazilian_signal_observed"
    if any(marker in value for marker in international):
        return "international_presence_in_BR"
    return "origin_unresolved"


clusters = [
    {
        "id": "R1_local_production_quality",
        "label": "Biorreatores, fermentação, produção on-farm e qualidade",
        "patterns": ["bioinput", "bioinsumo", "bioreactor", "biorreator", "fermentation", "fermentacao", "aseptic", "assptica", "rural property", "on farm", "on-farm", "quality control", "controle de qualidade", "spectrometry", "espectrometria", "thermochrom", "termocrom"],
        "description": "Cadeia de produção, formulação, controle e aplicação local de bioinsumos.",
    },
    {
        "id": "R2_nitrogen_phosphate_stability",
        "label": "Nitrogênio, fosfato, formulação, estabilidade e liberação",
        "patterns": ["nitrogen fixation", "nitrogen fixation", "nitrogen release", "fixacao de nitrogenio", "phosphate solubilization", "solubilizacao de fosfato", "phytase", "polymer formulation", "polymer stability", "shelf life", "inoculant formulation", "inoculante", "stability", "estabilidade", "release device"],
        "description": "Plataforma de aquisição de nutrientes e entrega estável de microrganismos ou compostos.",
    },
    {
        "id": "R3_trichoderma_bioprocess",
        "label": "Trichoderma, biocontrole, enzimas e bioprocessos",
        "patterns": ["trichoderma", "cellulase", "celulase", "enzyme", "enzima", "sophorolipid", "soforolipid", "ethanol", "etanol", "bioprocess", "bioprocesso", "starmerella bombicola", "fermentation", "fermentacao"],
        "description": "Organismo transversal atravessando agricultura, biossurfactantes, enzimas, biomassa e indústria.",
    },
    {
        "id": "R4_carbon_algae_industrial_waste",
        "label": "Biofixação de CO2, microalgas, resíduos e Petrobras",
        "patterns": ["biofixation", "biofixacao", "co2", "carbon dioxide", "microalgae", "microalga", "algal biomass", "biomassa de algas", "drilling cuttings", "cascalho de perfuracao", "industrial waste", "residuo industrial", "petrobras"],
        "description": "Corredor inesperado entre carbono, biomassa algal, resíduos de processo e aplicação agronômica.",
    },
    {
        "id": "R5_biocontrol_plant_health",
        "label": "Biocontrole, nematoides e saúde vegetal",
        "patterns": ["biocontrol", "biocontrole", "biopesticide", "biopesticida", "nematode", "nematoide", "plant disease", "doenca de plantas", "phytopathogen", "fitopatogeno", "plant growth", "promocao de crescimento"],
        "description": "Controle biológico, sanidade vegetal, nematoides e promoção de crescimento.",
    },
    {
        "id": "R6_literature_agro_context",
        "label": "Literatura, culturas e contexto agropecuário",
        "patterns": ["agriculture", "agricultura", "soybean", "soja", "maize", "milho", "field trial", "experimento de campo", "rhizosphere", "rizosfera", "biofertilizer", "biofertilizante"],
        "description": "Literatura e registros ligados a culturas, campo, rizosfera e aplicação agropecuária.",
    },
]

works = read_jsonl(WORKS)
actors = read_jsonl(ACTORS)
institutions = read_jsonl(INSTITUTIONS)
relations = read_jsonl(RELATIONS)
signals = read_jsonl(SIGNALS)
signal_by_work = defaultdict(list)
for row in signals:
    signal_by_work[row.get("work_id")].append(row)

memberships = []
cluster_work_ids = defaultdict(list)
organism_work_ids = defaultdict(list)
for work in works:
    text = fold(text_of(work))
    matches = []
    for cluster in clusters:
        hits = sorted({pattern for pattern in cluster["patterns"] if fold(pattern) in text})
        if hits:
            score = len(hits)
            matches.append({"cluster_id": cluster["id"], "label": cluster["label"], "score": score, "matched_patterns": hits, "evidence": {"record_id": work.get("record_id"), "source": work.get("source"), "title": work.get("title"), "provenance": work.get("provenance")}})
            cluster_work_ids[cluster["id"]].append(work.get("record_id"))
    for organism in ["trichoderma", "rhizobium", "bacillus", "pseudomonas", "azospirillum", "starmerella bombicola", "wickerhamomyces anomalus", "microalgae", "microalga", "microalgas"]:
        if organism in text:
            organism_work_ids[organism].append(work.get("record_id"))
    memberships.append({"record_id": work.get("record_id"), "source": work.get("source"), "title": work.get("title"), "year": year_of(work), "origin_state": origin_state(work), "clusters": sorted(matches, key=lambda item: (-item["score"], item["cluster_id"]))})

with OUT_MEMBERSHIPS.open("w", encoding="utf-8") as f:
    for row in memberships:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

work_by_id = {w.get("record_id"): w for w in works}
cluster_summary = []
for cluster in clusters:
    ids = cluster_work_ids[cluster["id"]]
    rows = [work_by_id[i] for i in ids if i in work_by_id]
    cluster_summary.append({
        "cluster_id": cluster["id"],
        "label": cluster["label"],
        "description": cluster["description"],
        "work_count": len(set(ids)),
        "sources": dict(Counter(row.get("source") for row in rows)),
        "years": dict(Counter(str(year_of(row)) for row in rows if year_of(row))),
        "origin_states": dict(Counter(origin_state(row) for row in rows)),
        "examples": [{"record_id": row.get("record_id"), "title": row.get("title"), "source": row.get("source"), "year": year_of(row)} for row in rows[:8]],
    })

actor_work = Counter()
actor_titles = defaultdict(list)
for relation in relations:
    if relation.get("predicate") not in ("authored_by", "invented_by", "assigned_to", "affiliated_with"):
        continue
    oid = relation.get("object_id")
    if oid in {a.get("actor_id") for a in actors}:
        subject = relation.get("subject_id")
        actor_work[oid] += 1
        if subject in work_by_id:
            actor_titles[oid].append(work_by_id[subject].get("title"))
actor_by_id = {a.get("actor_id"): a for a in actors}
actor_hubs = []
for oid, count in actor_work.most_common(30):
    row = actor_by_id.get(oid, {})
    actor_hubs.append({"id": oid, "name": row.get("display_name"), "relation_count": count, "sources": [row.get("source")], "examples": actor_titles[oid][:5]})

tech_patterns = [
    "biorreactor", "bioreactor", "fermentacao", "fermentation", "aseptic", "on farm", "quality control", "controle de qualidade", "spectrometry", "espectrometria", "polymer", "polimero", "stability", "estabilidade", "shelf life", "release", "liberacao", "nitrogen fixation", "fixacao de nitrogenio", "phosphate", "fosfato", "phytase", "cellulase", "celulase", "enzyme", "enzima", "sophorolipid", "soforolipid", "microalgae", "microalga", "biofixation", "biofixacao", "industrial waste", "residuo industrial"
]
tech_counts = Counter()
tech_cross_sources = defaultdict(set)
tech_cross_clusters = defaultdict(set)
for work in works:
    text = fold(text_of(work))
    matched_clusters = {m["cluster_id"] for m in next(row for row in memberships if row["record_id"] == work.get("record_id"))["clusters"]}
    for tech in tech_patterns:
        if fold(tech) in text:
            tech_counts[tech] += 1
            tech_cross_sources[tech].add(work.get("source"))
            tech_cross_clusters[tech].update(matched_clusters)
tech_hubs = [{"term": term, "work_count": count, "sources": sorted(tech_cross_sources[term]), "clusters": sorted(tech_cross_clusters[term])} for term, count in tech_counts.most_common()]

organism_hubs = [{"organism": org, "work_count": len(ids), "sources": dict(Counter(work_by_id[i].get("source") for i in ids if i in work_by_id)), "examples": [{"record_id": i, "title": work_by_id[i].get("title")} for i in ids[:8] if i in work_by_id]} for org, ids in sorted(organism_work_ids.items(), key=lambda item: (-len(item[1]), item[0])) if ids]

# Query generation from observed hubs, not generic brainstorming.
queries = []
def add(qid, query, source, block, reason, target_gap, evidence_terms, priority):
    queries.append({"query_id": qid, "query": query, "source": source, "block": block, "priority_score": priority, "status": "planned", "reason": reason, "target_gap": target_gap, "evidence_terms": evidence_terms})

add("Q01", "USP Trichoderma harzianum sophorolipid Brazil", "google_patents", "local_trichoderma_bridge", "A família USP reaparece com Trichoderma harzianum, soforolipídeos e fermentação de Starmerella bombicola.", "Confirmar a família e localizar atores/instituições associados sem tratar a ponte como produto único.", ["Trichoderma", "sophorolipid", "USP"], 99)
add("Q02", "Embrapa Bacillus velezensis bioreactor formulation Brazil", "google_patents", "local_bioreactor", "Bacillus velezensis, Embrapa e biorreator apareceram juntos na V2.", "Expandir a cadeia local de organismo a processo e formulação.", ["Bacillus velezensis", "Embrapa", "bioreactor"], 98)
add("Q03", "Simple Agro bioinput quality control Brazil patent", "google_patents", "local_quality_onfarm", "Simple Agro reapareceu em controle de qualidade e sistemas on-farm.", "Testar se qualidade é capacidade própria de processo ou apenas ocorrência isolada.", ["Simple Agro", "quality control", "bioinput"], 96)
add("Q04", "Solubio on farm bioinput production Brazil patent", "google_patents", "local_quality_onfarm", "Solubio e produção on-farm apareceram no mesmo corredor de automação rural.", "Verificar arquitetura de produção/aplicação e atores recorrentes.", ["Solubio", "on-farm", "bioinput"], 95)
add("Q05", "Azospirillum inoculant polymer stability Brazil", "google_patents", "local_stability", "Azospirillum entrou na expansão V2 junto de inoculantes e estabilidade.", "Conectar o organismo a shelf life e formulação.", ["Azospirillum", "inoculant", "polymer", "stability"], 94)
add("Q06", "Rhizobium inoculant polymer shelf life Brazil", "google_patents", "local_stability", "Rhizobium apareceu na trilha de inoculante-polímero-estabilidade.", "Verificar convergência de formulação entre organismos.", ["Rhizobium", "inoculant", "shelf life"], 93)
add("Q07", "Bacillus megaterium phosphorus biofertilizer Brazil", "google_patents", "local_nutrition", "Bacillus megaterium e fósforo reapareceram em famílias locais.", "Expandir aquisição de fósforo e aplicações agronômicas.", ["Bacillus megaterium", "phosphorus", "biofertilizer"], 92)
add("Q08", "Pivot Bio nitrogen fixation phosphorus formulation", "google_patents", "international_platform", "Pivot Bio forma o hub internacional mais coerente de nitrogênio, fósforo e formulação.", "Mapear famílias e possíveis continuidades do portfólio.", ["Pivot Bio", "nitrogen fixation", "phosphorus", "formulation"], 98)
add("Q09", "Locus phytase phosphorus microbial agriculture", "google_patents", "international_platform", "Locus reaparece em liberação de fósforo por enzimas e matéria orgânica.", "Separar aplicação agrícola de biorremediação/óleo.", ["Locus", "phytase", "phosphorus"], 91)
add("Q10", "Novozymes Trichoderma cellulase fermentation Brazil", "google_patents", "industrial_trichoderma", "Novozymes e Trichoderma atravessam enzimas, celulose e fermentação.", "Testar se existe família comum ou apenas hub de bioprocessos.", ["Novozymes", "Trichoderma", "cellulase", "fermentation"], 95)
add("Q11", "Petrobras microalgae CO2 fixation fertilizer Brazil", "google_patents", "carbon_algae", "Petrobras, microalgas, biofixação e fertilizante reapareceram no corredor inesperado.", "Verificar se o corredor chega a produto/agricultura ou termina em processo industrial.", ["Petrobras", "microalgae", "CO2", "fertilizer"], 97)
add("Q12", "microalgae industrial waste biofertilizer Brazil", "google_patents", "carbon_algae", "Resíduos industriais e biomassa algal abriram famílias adjacentes.", "Testar o elo de valorização de resíduos e fertilizante.", ["microalgae", "industrial waste", "biofertilizer"], 90)
add("Q13", "Trichoderma harzianum sophorolipids biocontrol Brazil", "openalex", "literature_local_bridge", "A ponte USP–Trichoderma–soforolipídeos exige contraste bibliográfico.", "Encontrar literatura que confirme, refine ou contradiga a ponte patentária.", ["Trichoderma harzianum", "sophorolipids", "biocontrol"], 96)
add("Q14", "microbial inoculant polymer stability nitrogen fixation", "openalex", "literature_stability", "A formulação polimérica é recorrente na patente internacional.", "Verificar base científica para estabilidade e viabilidade.", ["microbial inoculant", "polymer", "stability", "nitrogen fixation"], 94)
add("Q15", "on farm bioinput fermentation Brazil", "openalex", "literature_local_production", "O núcleo brasileiro de biorreator e produção on-farm precisa de literatura de aplicação.", "Preencher lacuna entre arquitetura patentária e evidência técnico-agronômica.", ["on farm", "bioinput", "fermentation", "Brazil"], 93)
add("Q16", "microalgae CO2 fixation industrial waste fertilizer Brazil", "openalex", "literature_carbon", "A trilha Petrobras–microalgas–resíduos precisa de contraste fora das patentes.", "Verificar se há literatura sobre conversão de resíduos e destino agronômico.", ["microalgae", "CO2 fixation", "industrial waste", "fertilizer"], 89)
add("Q17", "Bacillus velezensis biofertilizer nematode Brazil", "openalex", "literature_local_organism", "Bacillus atravessa biorreator, biofertilizante e nematoide.", "Comparar as funções de biocontrole e promoção de crescimento.", ["Bacillus velezensis", "biofertilizer", "nematode"], 90)

summary = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source_corpus": "normalized_v2",
    "work_count": len(works),
    "source_mix": dict(Counter(row.get("source") for row in works)),
    "cluster_summary": cluster_summary,
    "actor_hubs": actor_hubs,
    "organism_hubs": organism_hubs,
    "technology_hubs": tech_hubs,
    "origin_states": dict(Counter(origin_state(row) for row in works)),
    "years": dict(Counter(str(year_of(row)) for row in works if year_of(row))),
    "queries_generated": len(queries),
    "notes": [
        "Clusters são operacionais e derivam de termos observados em títulos, abstracts, queries e atores.",
        "A divisão brasileiro/internacional é contextual: filtro BR não prova origem brasileira.",
        "Entity resolution segura está separada em ENTITY_RESOLUTION_V1; nomes originais permanecem preservados.",
        "Ausências e resultados ruidosos viram lacunas de investigação, não conclusões negativas.",
    ],
}
OUT_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_QUERIES.write_text(json.dumps({"version": "next_queries_v1", "generated_from": "normalized_v2", "queries": queries, "selection_rule": "queries are grounded in recurring terms, actors, organisms or unresolved bridges from the cumulative corpus"}, ensure_ascii=False, indent=2), encoding="utf-8")

md = [
    "# Radiografia Exploratória V1",
    "",
    "> Leitura operacional do corpus cumulativo de 734 obras após a segunda rodada e as expansões V1/V2. A radiografia procura relações para investigar, não transforma coocorrência em conclusão.",
    "",
    f"**Corpus analisado:** {len(works)} obras; fontes: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(row.get('source') for row in works).items())) + ".",
    "",
    "## 1. Trilhas que ganharam densidade",
    "",
]

def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in row) + " |")
    return "\n".join(lines)

md.append(table(["Trilha", "Obras", "Fontes", "Leitura operacional"], [[row["label"], row["work_count"], ", ".join(f"{k}:{v}" for k,v in row["sources"].items()), row["description"]] for row in cluster_summary]))
md += ["", "## 2. Hubs de atores", "", table(["Ator", "Relações", "Fonte", "Como aparece"], [[row["name"], row["relation_count"], ", ".join(row["sources"]), "; ".join(str(x) for x in row["examples"][:2])] for row in actor_hubs[:20]]), "", "## 3. Organismos e entidades biológicas recorrentes", "", table(["Organismo/entidade", "Obras", "Fontes", "Exemplos"], [[row["organism"], row["work_count"], ", ".join(f"{k}:{v}" for k,v in row["sources"].items()), "; ".join(str(x["title"]) for x in row["examples"][:2])] for row in organism_hubs[:20]]), "", "## 4. Tecnologias que atravessam contextos", "", table(["Termo", "Obras", "Fontes", "Clusters"], [[row["term"], row["work_count"], ", ".join(row["sources"]), ", ".join(row["clusters"])] for row in tech_hubs[:25]]), "", "## 5. Estado das quatro trilhas", "", "### Trilha brasileira", "", "A cadeia biorreator–fermentação–produção on-farm–qualidade ganhou novos registros e atores, incluindo USP, Embrapa, Simple Agro e Solubio. O próximo problema informacional não é mais encontrar a existência da cadeia; é separar equipamento, formulação, controle de parâmetros e evidência de aplicação.", "", "### Trilha internacional", "", "Pivot Bio aparece como portfólio coerente entre fixação de nitrogênio, fósforo, remodelamento microbiano, formulação e estabilidade. Locus aparece em fósforo, enzimas, matéria orgânica e biossurfactantes. A próxima expansão deve testar continuidade de famílias e contraste bibliográfico, sem fundir as empresas.", "", "### Trilha transversal de Trichoderma", "", "Trichoderma atravessa biocontrole, soforolipídeos, fermentação, celulase, enzimas, etanol e biorreatores. A família USP–Trichoderma harzianum–soforolipídeos–Starmerella bombicola é uma ponte específica que merece busca nominal e literatura de contraste.", "", "### Trilha inesperada de carbono", "", "Petrobras, microalgas, biofixação de CO2, resíduos industriais e fertilizante reaparecem, mas a trilha ainda é estreita. A busca seguinte deve testar se o corredor chega a aplicação agronômica ou permanece em processo industrial/ambiental.", "", "## 6. Lacunas que viraram perguntas executáveis", "", table(["Query", "Fonte", "Prioridade", "Lacuna"], [[q["query"], q["source"], q["priority_score"], q["target_gap"]] for q in queries]), "", "## 7. O que apareceu e não estava no mapa inicial", "", "A expansão trouxe como sinais adicionais: a família USP de soforolipídeos produzidos por Starmerella bombicola; Bacillus velezensis e Bacillus megaterium ligados a biorreatores/formulação; uma convergência operacional entre controle de qualidade, produção on-farm e automação; e a possibilidade de a trilha de carbono algal possuir destino fertilizante, embora ainda não esteja resolvida.", "", "## Proveniência e limites", "", "Os registros continuam metadata-only. As páginas Google Patents foram capturadas por consulta e filtro BR, o que não prova origem brasileira. Os lotes OpenAlex preservam payloads, queries e hashes. A resolução segura de aliases está em `ENTITY_RESOLUTION_V1.md`; famílias candidatas não foram fundidas.", ""]
OUT_MD.write_text("\n".join(md), encoding="utf-8")

method = """# Método da Radiografia Exploratória V1\n\nA radiografia lê `normalized_v2`, que integra os manifests V0, V1 e V2. Cada obra recebe memberships por correspondência lexical explícita em título, resumo/descrição, query e atores. Os clusters são operacionais: servem para orientar investigação e não representam classificação científica definitiva.\n\nAtores e instituições são contabilizados por relações preservadas no corpus. Organismos e tecnologias são contados por ocorrência textual e cruzados com fonte e cluster. Queries novas só entram quando há um termo, ator, organismo, instituição, ponte ou lacuna observada no corpus.\n\nA origem patentária é exibida em três estados: `brazilian_signal_observed`, `international_presence_in_BR` e `origin_unresolved`. O filtro BR é tratado como contexto de recuperação, não como prova de origem. Aliases seguros são registrados separadamente em `ENTITY_RESOLUTION_V1`; o corpus original não é sobrescrito.\n\nAusência, baixa densidade e ruído são preservados como motivos para reformulação ou nova busca. Nenhum documento integral, sequência ou dado científico foi baixado.\n"""
OUT_METHOD.write_text(method, encoding="utf-8")
print(json.dumps({"works": len(works), "clusters": len(clusters), "queries": len(queries), "output": str(OUT_MD)}, ensure_ascii=False))
