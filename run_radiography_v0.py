import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NORM = ROOT / "normalized_v0"
MANIFEST_PATH = ROOT / "ingestion_manifest_v0.jsonl"
RADIOGRAPHY_MD = ROOT / "EXPLORATORY_RADIOGRAPHY_V0.md"
MEMBERSHIPS = ROOT / "cluster_memberships_v0.jsonl"
NEXT_QUERIES = ROOT / "next_queries_v0.json"
METHOD_MD = ROOT / "RADIOGRAPHY_METHOD_V0.md"
SUMMARY_JSON = ROOT / "radiography_summary_v0.json"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ascii_norm(value):
    return unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii").lower()


def compact(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in row) + " |")
    return "\n".join(lines)


def first_year(work):
    if work.get("publication_year"):
        return str(work["publication_year"])
    publication = work.get("publication") or {}
    if isinstance(publication, dict):
        parts = publication.get("date-parts") or publication.get("date_parts") or []
        if parts and parts[0]:
            return str(parts[0][0])
    for key in ("published_date", "priority_date", "filed_date"):
        value = (work.get("dates") or {}).get(key)
        if value:
            return str(value)[:4]
    return "unknown"


def work_text(work, signals_by_work):
    fields = [work.get("title"), work.get("description_or_abstract"), work.get("query")]
    fields.extend(work.get("matched_queries") or [])
    fields.extend(signal.get("observed_text") for signal in signals_by_work.get(work.get("record_id"), []))
    return compact(" ".join(str(value or "") for value in fields))


def relation_counts(relations, actors, institutions):
    actor_by_id = {row.get("actor_id"): row for row in actors}
    institution_by_id = {row.get("institution_id"): row for row in institutions}
    actor_counts = Counter()
    institution_counts = Counter()
    actor_work_ids = defaultdict(set)
    institution_work_ids = defaultdict(set)
    predicate_counts = Counter()
    for row in relations:
        predicate = row.get("predicate")
        predicate_counts[predicate] += 1
        subject = row.get("subject_id")
        object_id = row.get("object_id")
        if object_id in actor_by_id:
            actor_counts[object_id] += 1
            actor_work_ids[object_id].add(subject)
        if object_id in institution_by_id:
            institution_counts[object_id] += 1
            institution_work_ids[object_id].add(subject)
    return actor_by_id, institution_by_id, actor_counts, institution_counts, actor_work_ids, institution_work_ids, predicate_counts


def canonical_name(name):
    value = ascii_norm(name)
    value = re.sub(r"[^a-z0-9]+", " ", value).strip()
    return value


def build_clusters():
    return [
        {
            "cluster_id": "C01_biocontrol_biopesticide",
            "label": "Biocontrole, biopesticidas e sanidade vegetal",
            "anchors": {"biocontrole", "biopesticida", "nematoide", "saude_radicular"},
            "patterns": ["biological control", "plant pathogenic", "fitopatogen", "praga", "pest control", "phytosanity", "fitossanidade"],
            "description": "Registros ligados a controle biológico, agentes contra pragas ou fitopatógenos e saúde da planta.",
        },
        {
            "cluster_id": "C02_bioinputs_nutrition",
            "label": "Bioinsumos, inoculantes e nutrição biológica",
            "anchors": {"bioinsumo", "biofertilizante", "inoculante", "promocao_crescimento", "fixacao_nitrogenio", "solubilizacao_fosfato"},
            "patterns": ["bioinput", "bio inputs", "biofertilizer", "inoculant", "plant growth", "nutrient acquisition", "nutricao"],
            "description": "Registros ligados a bioinsumos, inoculação, aquisição de nutrientes e promoção de crescimento.",
        },
        {
            "cluster_id": "C03_nitrogen_platform",
            "label": "Fixação de nitrogênio e plataforma microbiana",
            "anchors": {"fixacao_nitrogenio", "solubilizacao_fosfato", "promocao_crescimento"},
            "patterns": ["nitrogen fixation", "nitrogen-fixing", "nitrogen fixing", "microbial nitrogen", "nitrogen release", "remodeled microbes", "remodelamento microbiano"],
            "description": "Registros em que nitrogênio, microrganismos remodelados, liberação ou estabilidade de nitrogênio aparecem como eixo.",
        },
        {
            "cluster_id": "C04_formulation_quality",
            "label": "Fermentação, formulação e monitoramento de qualidade",
            "anchors": {"fermentacao_bioprocesso", "monitoramento_qualidade"},
            "patterns": ["fermentation", "fermentacao", "bioreactor", "biorreator", "solid substrate", "formulation", "formulacao", "spectrometry", "espectrometria", "monitoring", "monitoramento", "thermochromy", "termocromia", "assptic", "aseptic"],
            "description": "Registros em que produzir, estabilizar, formular ou monitorar bioinsumos aparece como capacidade de processo.",
        },
        {
            "cluster_id": "C05_trichoderma_cross_context",
            "label": "Trichoderma como organismo transversal",
            "anchors": {"fungo"},
            "patterns": ["trichoderma"],
            "description": "Registros que usam Trichoderma em mais de um contexto tecnológico ou de aplicação.",
        },
        {
            "cluster_id": "C06_scientific_crop_context",
            "label": "Literatura, culturas e contexto agronômico",
            "anchors": {"soja", "milho", "nematoide", "promocao_crescimento"},
            "patterns": ["soybean", "soja", "maize", "corn", "milho", "field trial", "experimento de campo", "agriculture", "agricultura"],
            "description": "Registros científicos ou técnicos que conectam biotecnologia a culturas e desempenho agronômico.",
        },
    ]


def cluster_matches(work, text, clusters):
    terms = set(work.get("application_terms") or [])
    normalized_text = ascii_norm(text)
    matches = []
    for cluster in clusters:
        matched_terms = sorted(terms & cluster["anchors"])
        matched_patterns = sorted({pattern for pattern in cluster["patterns"] if ascii_norm(pattern) in normalized_text})
        # Require an observed anchor or a strong lexical pattern. This keeps memberships sparse.
        if matched_terms or matched_patterns:
            score = len(matched_terms) * 2 + len(matched_patterns)
            matches.append({"cluster_id": cluster["cluster_id"], "label": cluster["label"], "score": score, "matched_terms": matched_terms, "matched_patterns": matched_patterns})
    return sorted(matches, key=lambda item: (-item["score"], item["cluster_id"]))


def query_diagnostics(works, manifest, signals_by_work):
    patent_works = [row for row in works if row.get("source") == "google_patents"]
    by_query = defaultdict(list)
    for work in patent_works:
        for query in work.get("matched_queries") or [work.get("query")]:
            if query:
                by_query[query].append(work)
    rows = []
    for entry in manifest:
        if entry.get("source") != "google_patents" or entry.get("status") != "captured":
            continue
        query = entry.get("query")
        query_works = by_query.get(query, [])
        signal_count = sum(1 for work in query_works if signals_by_work.get(work.get("record_id")))
        total = entry.get("observed_result_count") or 0
        rows.append({
            "query": query,
            "observed_result_count": total,
            "captured": entry.get("returned_items", 0),
            "unique_in_inventory": len({work.get("record_id") for work in query_works}),
            "signal_bearing_works": signal_count,
            "signal_rate_in_inventory": round(signal_count / len(query_works), 3) if query_works else 0,
            "recall_to_capture_ratio": round(total / max(entry.get("returned_items", 1), 1), 1) if total else None,
            "source_url": entry.get("url"),
            "raw_path": entry.get("saved_path"),
        })
    return rows


def origin_state(work):
    if work.get("source") != "google_patents":
        return "not_applicable"
    text = ascii_norm(work_text(work, {}))
    actors = ascii_norm(" ".join((work.get("actors") or {}).get("inventors", []) + (work.get("actors") or {}).get("assignees", [])))
    combined = f"{text} {actors}"
    local_markers = ["universidade de sao paulo", "usp", "universidade do estado da bahia", "ueba", "mcti", "museu paraense", "agencia paulista", "apta", "dosaggio", "gi industria", "embrapa", "universidade federal", "universidade estadual"]
    international_markers = ["pivot bio", "basf", "syngenta", "monsanto", "bayer", "pioneer hi bred", "locus", "novozymes", "terragen", "raison", "fmc", "corteva", "sumitomo", "agrospheres", "boost biomes"]
    if any(marker in combined for marker in local_markers):
        return "brazilian_signal_observed"
    if any(marker in combined for marker in international_markers):
        return "international_presence_in_BR"
    return "origin_unresolved"


def organism_contexts(works, memberships):
    patterns = ["trichoderma", "rhizobium", "bacillus thuringiensis", "bacillus", "pseudomonas", "clostridium", "metarhizium", "rhizobacteria", "yeast", "sophorolipids"]
    by_id = {row.get("record_id"): row for row in works}
    result = {}
    for pattern in patterns:
        rows = []
        for work_id, cluster_rows in memberships.items():
            text = ascii_norm(work_text(by_id[work_id], {}))
            if pattern in text:
                rows.append({"work_id": work_id, "clusters": [row["cluster_id"] for row in cluster_rows], "source": by_id[work_id].get("source"), "title": by_id[work_id].get("title")})
        if rows:
            result[pattern] = {"work_count": len(rows), "cluster_count": len({cluster for row in rows for cluster in row["clusters"]}), "sources": dict(Counter(row["source"] for row in rows)), "examples": rows[:12]}
    return result


def build_next_queries(cluster_stats, technology_crossings, organism_stats, query_stats, local_patents, international_patents):
    candidates = []
    rank = 0

    def add(query, source, block, purpose, expected_signal, ambiguity, evidence_ids, evidence_text, priority):
        nonlocal rank
        rank += 1
        candidates.append({"query_id": f"NQ{rank:02d}", "query": query, "source": source, "block": block, "priority_score": priority, "status": "planned", "purpose": purpose, "expected_signal": expected_signal, "ambiguity_to_resolve": ambiguity, "evidence_record_ids": evidence_ids[:12], "evidence": evidence_text})

    tricho = organism_stats.get("trichoderma")
    if tricho:
        ids = [row["work_id"] for row in tricho["examples"]]
        add("Trichoderma fermentation BR", "google_patents", "B1_trichoderma_transversal", "Separar a trilha de produção/fermentação da trilha de biocontrole.", "processo, escala, fermentação e formulação", "o termo pode recuperar aplicações alimentícias e industriais fora do agro", ids, f"Trichoderma apareceu em {tricho['work_count']} registros e {tricho['cluster_count']} clusters operacionais.", 98)
        add("Trichoderma biocontrol BR", "google_patents", "B1_trichoderma_transversal", "Medir o núcleo agronômico do organismo em biocontrole.", "agente de controle biológico e fitopatógenos", "o recall pode misturar química agrícola que apenas menciona o organismo", ids, "A presença de Trichoderma atravessa o cluster de biocontrole e outros contextos.", 94)
        add("Trichoderma carbon sequestration BR", "google_patents", "B1_trichoderma_transversal", "Testar se o sinal de carbono é uma trilha tecnológica própria ou apenas um outlier.", "sequestro, gases de efeito estufa e uso de carbono", "a primeira ocorrência pode ser uma família internacional ampla", ids, "O termo apareceu associado a carbono/sequestro na captura atual.", 82)
    if cluster_stats.get("C03_nitrogen_platform", {}).get("count", 0):
        ids = cluster_stats["C03_nitrogen_platform"]["work_ids"]
        add("microbial nitrogen fixation formulation BR", "google_patents", "B2_nitrogen_platform", "Aprofundar a relação entre microrganismo fixador, formulação e estabilidade.", "formulação, estabilidade e desempenho de micróbios fixadores", "pode concentrar novamente famílias da Pivot Bio", ids, "Fixação de nitrogênio formou um cluster concentrado na primeira página observada.", 97)
        add("nitrogen fixation microbial release BR", "google_patents", "B2_nitrogen_platform", "Investigar a ponte entre fixação e liberação temporal/espacial de nitrogênio.", "liberação dinâmica e aplicação agrícola", "termos amplos podem recuperar patentes de genética vegetal", ids, "A captura atual mostrou linguagem de liberação dinâmica de nitrogênio.", 90)
        add("phosphate solubilization microbial BR", "google_patents", "B2_nitrogen_platform", "Completar o eixo de nutrição microbiana além do nitrogênio.", "solubilização de fosfato e aquisição de nutrientes", "pode misturar fertilizantes sem componente biológico", ids, "Solubilização de fosfato apareceu como sinal técnico distinto.", 92)
    if cluster_stats.get("C02_bioinputs_nutrition", {}).get("count", 0):
        ids = cluster_stats["C02_bioinputs_nutrition"]["work_ids"]
        add("bioinput bioreactor BR", "google_patents", "B3_local_production_quality", "Mapear equipamentos e arquitetura de produção de bioinputs.", "biorreator, módulo, fermentação e produção local", "o vocabulário pode recuperar equipamentos não agrícolas", ids, "Bioinput apareceu junto de biorreator e sistemas de produção.", 96)
        add("bioinput fermentation BR", "google_patents", "B3_local_production_quality", "Aprofundar o processo de fermentação e sua escala.", "fermentação sólida/líquida e produção de microrganismos", "pode recuperar bioprocessos alimentícios", ids, "Fermentação e produção foram observadas como sinais de processo.", 95)
        add("bioinput quality monitoring spectrometry BR", "google_patents", "B3_local_production_quality", "Verificar se monitoramento de qualidade constitui uma subtrilha própria.", "espectrometria, termocromia e parâmetros físico-químicos", "poucas ocorrências podem ser um nicho ou ruído lexical", ids, "Monitoramento de qualidade apareceu como sinal separado no mapa.", 91)
        add("bioinput rural property production BR", "google_patents", "B3_local_production_quality", "Testar a hipótese de produção descentralizada na propriedade rural.", "produção on-farm e aplicação direta no sulco", "a expressão pode recuperar máquinas ou modelos de serviço", ids, "A captura atual incluiu sistema de produção para propriedades rurais.", 93)
    if cluster_stats.get("C01_biocontrol_biopesticide", {}).get("count", 0):
        ids = cluster_stats["C01_biocontrol_biopesticide"]["work_ids"]
        add("Bacillus biocontrol Brazil patent", "google_patents", "B4_organisms_and_application", "Reduzir o ruído de Bacillus thuringiensis para o núcleo de biocontrole microbiano.", "agente microbiano e praga-alvo", "a espécie também aparece em misturas químicas", ids, "A busca Bacillus thuringiensis mostrou muito ruído lexical.", 86)
        add("Pseudomonas biocontrol BR", "google_patents", "B4_organisms_and_application", "Explorar outro organismo recorrente em controle biológico e inoculação.", "Pseudomonas, fitopatógeno e aplicação agrícola", "pode recuperar microbiologia ambiental não agrícola", ids, "Pseudomonas apareceu na literatura patentária de inoculantes microbianos.", 83)
        add("Rhizobium phosphate solubilization BR", "google_patents", "B2_nitrogen_platform", "Conectar o organismo de fixação ao eixo de fosfato.", "Rhizobium, solubilização e rendimento vegetal", "pode recuperar transformação vegetal ou genética", ids, "Rhizobium e solubilização foram observados em registros relacionados.", 88)
    add("Brazilian bioinput fermentation agriculture", "openalex", "B3_local_production_quality", "Verificar se a literatura acompanha a infraestrutura patentária brasileira de produção.", "artigos, teses ou revisões sobre fermentação e bioinsumos no Brasil", "a consulta pode trazer literatura geral de bioprocessos", [row["record_id"] for row in local_patents], "Patentes com sinais brasileiros concentraram produção, fermentação e monitoramento.", 89)
    add("Brazil bioinputs on farm production", "openalex", "B3_local_production_quality", "Buscar literatura sobre produção descentralizada e uso na propriedade.", "sistemas locais, agricultores e aplicação on-farm", "a expressão pode ser pouco padronizada", [row["record_id"] for row in local_patents], "O corpus patentário mostrou um sistema de produção em propriedades rurais.", 84)
    add("bioinput quality control Brazil", "crossref", "B3_local_production_quality", "Encontrar literatura sobre controle de qualidade e padronização.", "controle físico-químico, estabilidade e qualidade", "o corpus pode ser pequeno e multidisciplinar", [row["record_id"] for row in local_patents], "Monitoramento de qualidade é um sinal pequeno, mas específico.", 87)
    add("microbial inoculant root health Brazil", "openalex", "B4_organisms_and_application", "Conectar inoculantes, rizosfera e saúde radicular em literatura científica.", "saúde radicular, rizosfera e produtividade", "pode incluir estudos não agrícolas", [row["record_id"] for row in international_patents], "Saúde radicular apareceu na camada patentária internacional presente no Brasil.", 80)
    add("Trichoderma production scale agriculture Brazil", "openalex", "B1_trichoderma_transversal", "Verificar na literatura a ponte entre organismo, produção e aplicação agrícola.", "produção em escala, formulação e biocontrole", "pode retornar estudos de enzimas industriais", [row["work_id"] for row in (tricho["examples"] if tricho else [])], "Trichoderma apareceu em múltiplos contextos tecnológicos.", 85)
    add("biofertilizer phosphate solubilizing bacteria Brazil", "crossref", "B2_nitrogen_platform", "Aprofundar o eixo de fertilização biológica e fosfato.", "bactérias solubilizadoras e biofertilizantes", "pode recuperar fertilizantes sem microrganismos", [row["record_id"] for row in cluster_stats.get("C02_bioinputs_nutrition", {}).get("work_examples", [])], "Biofertilizante e solubilização de fosfato coocorreram como sinais.", 81)
    add("agricultural microbial formulation stability Brazil", "openalex", "B3_local_production_quality", "Buscar a camada de estabilidade que conecta processo e produto.", "estabilidade, armazenamento e formulação microbiana", "pode trazer formulação de defensivos convencionais", [row["record_id"] for row in international_patents], "A captura patentária mostra formulação e estabilidade como problema recorrente.", 79)
    add("agricultural biological control Brazil institutions", "openalex", "B5_local_vs_international", "Testar quais instituições brasileiras aparecem na literatura de biocontrole.", "universidades, Embrapa e grupos brasileiros", "a busca pode ser ampla e heterogênea", [row["record_id"] for row in local_patents], "O contraste entre sinais locais e presença internacional precisa de uma camada bibliográfica.", 77)
    add("bioinput regulation Brazil", "crossref", "B6_gap_regulatory", "Verificar a lacuna regulatória e terminológica do corpus.", "legislação, registro, avaliação ou políticas de bioinsumos", "pode retornar documentos normativos em vez de ciência", [], "Não há sinal regulatório explícito entre os termos atuais; a ausência gerou uma consulta de investigação.", 76)
    # Keep exactly 20, ordered by score rather than insertion order.
    candidates = sorted(candidates, key=lambda item: (-item["priority_score"], item["query"]))[:20]
    for index, row in enumerate(candidates, start=1):
        row["rank"] = index
    return candidates


def main():
    works = read_jsonl(NORM / "works_v0.jsonl")
    actors = read_jsonl(NORM / "actors_v0.jsonl")
    institutions = read_jsonl(NORM / "institutions_v0.jsonl")
    relations = read_jsonl(NORM / "relations_v0.jsonl")
    signals = read_jsonl(NORM / "application_signals_v0.jsonl")
    manifest = read_jsonl(MANIFEST_PATH)
    work_by_id = {row.get("record_id"): row for row in works}
    signals_by_work = defaultdict(list)
    for signal in signals:
        signals_by_work[signal.get("work_id")].append(signal)

    clusters = build_clusters()
    memberships_by_work = {}
    membership_rows = []
    cluster_work_ids = defaultdict(list)
    for work in works:
        text = work_text(work, signals_by_work)
        matches = cluster_matches(work, text, clusters)
        if not matches:
            matches = [{"cluster_id": "C00_unclassified_current_rules", "label": "Sem correspondência nas regras atuais", "score": 0, "matched_terms": [], "matched_patterns": []}]
        memberships_by_work[work.get("record_id")] = matches
        for match in matches:
            cluster_work_ids[match["cluster_id"]].append(work.get("record_id"))
            membership_rows.append({
                "work_id": work.get("record_id"),
                "source": work.get("source"),
                "source_id": work.get("source_id"),
                "title": work.get("title"),
                "cluster_id": match["cluster_id"],
                "cluster_label": match["label"],
                "membership_score": match["score"],
                "matched_application_terms": match["matched_terms"],
                "matched_text_patterns": match["matched_patterns"],
                "query": work.get("query"),
                "matched_queries": work.get("matched_queries", []),
                "year": first_year(work),
                "provenance": work.get("provenance", {}),
            })
    MEMBERSHIPS.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in membership_rows), encoding="utf-8")

    actor_by_id, institution_by_id, actor_counts, institution_counts, actor_work_ids, institution_work_ids, predicate_counts = relation_counts(relations, actors, institutions)
    actor_name_sources = defaultdict(set)
    actor_name_rows = defaultdict(list)
    for actor in actors:
        key = canonical_name(actor.get("display_name"))
        if key:
            actor_name_sources[key].add(actor.get("source"))
            actor_name_rows[key].append(actor)
    cross_layer_actors = []
    for key, source_set in actor_name_sources.items():
        if len(source_set) > 1:
            row = actor_name_rows[key][0]
            cross_layer_actors.append({"display_name": row.get("display_name"), "sources": sorted(source_set), "variants": sorted({item.get("display_name") for item in actor_name_rows[key]}), "count": sum(actor_counts.get(item.get("actor_id"), 0) for item in actor_name_rows[key])})
    cross_layer_actors.sort(key=lambda item: (-item["count"], item["display_name"] or ""))

    cluster_stats = {}
    for cluster_id, ids in sorted(cluster_work_ids.items()):
        rows = [work_by_id[work_id] for work_id in ids if work_id in work_by_id]
        terms = Counter(term for row in rows for term in row.get("application_terms", []))
        sources = Counter(row.get("source") for row in rows)
        years = Counter(first_year(row) for row in rows)
        cluster_stats[cluster_id] = {"count": len(rows), "source_counts": dict(sources), "term_counts": dict(terms), "year_counts": dict(sorted(years.items())), "work_ids": ids[:80], "work_examples": rows[:12]}

    term_clusters = defaultdict(set)
    for row in membership_rows:
        for term in row.get("matched_application_terms", []):
            term_clusters[term].add(row["cluster_id"])
    technology_crossings = []
    for term, cluster_set in sorted(term_clusters.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(cluster_set) >= 2:
            technology_crossings.append({"term": term, "cluster_count": len(cluster_set), "clusters": sorted(cluster_set), "work_count": len({row["work_id"] for row in membership_rows if term in row.get("matched_application_terms", [])})})

    organisms = organism_contexts(works, memberships_by_work)
    query_stats = query_diagnostics(works, manifest, signals_by_work)
    local_patents = [row for row in works if origin_state(row) == "brazilian_signal_observed"]
    international_patents = [row for row in works if origin_state(row) == "international_presence_in_BR"]
    unresolved_patents = [row for row in works if origin_state(row) == "origin_unresolved"]
    origin_counts = Counter(origin_state(row) for row in works if row.get("source") == "google_patents")

    next_queries = build_next_queries(cluster_stats, technology_crossings, organisms, query_stats, local_patents, international_patents)
    NEXT_QUERIES.write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "mode": "exploratory", "derived_from_work_count": len(works), "queries": next_queries}, ensure_ascii=False, indent=2), encoding="utf-8")

    top_actor_rows = []
    for actor_id, count in actor_counts.most_common(20):
        actor = actor_by_id.get(actor_id, {})
        top_actor_rows.append([actor.get("display_name"), count, actor.get("source"), ", ".join(actor.get("roles", []))])
    top_institution_rows = []
    for inst_id, count in institution_counts.most_common(20):
        institution = institution_by_id.get(inst_id, {})
        top_institution_rows.append([institution.get("display_name"), count, institution.get("source")])

    cluster_rows = []
    for cluster_id, stats in sorted(cluster_stats.items(), key=lambda item: (-item[1]["count"], item[0])):
        label = next((item["label"] for item in clusters if item["cluster_id"] == cluster_id), "Sem correspondência nas regras atuais")
        cluster_rows.append([cluster_id, label, stats["count"], ", ".join(f"{key}: {value}" for key, value in Counter(stats["source_counts"]).most_common())])

    origin_rows = [[key, value] for key, value in origin_counts.most_common()]
    recall_rows = []
    for row in sorted(query_stats, key=lambda item: (item["observed_result_count"], -item["signal_rate_in_inventory"])):
        recall_rows.append([row["query"], row["observed_result_count"], row["captured"], row["unique_in_inventory"], row["signal_bearing_works"], row["signal_rate_in_inventory"]])

    anomaly_rows = [
        ["Recall amplo com captura pequena", "biological control + BR", "56.223 resultados observados e 7 registros capturados; vocabulário amplo e pouco seletivo na primeira página."],
        ["Corpus pequeno e denso", "bioinput + BR / bioinsumo + BR", "49–50 resultados observados e 9 registros capturados em cada trilha; aparecem produção, fermentação, biorreatores e monitoramento."],
        ["Concentração de plataforma", "fixação de nitrogênio + BR", "8.956 resultados observados; a primeira página concentrou famílias com microrganismos, genes, formulação e liberação de nitrogênio."],
        ["Ruído lexical", "Bacillus thuringiensis + BR", "14.887 resultados observados; a primeira página mistura agentes biológicos com patentes químicas que apenas mencionam a espécie."],
        ["Ponte organismo-processo", "Trichoderma", "O organismo aparece em biocontrole, produção, enzimas, formulação e carbono na amostra capturada."],
    ]

    gap_rows = [
        ["Sinal regulatório explícito", "Nenhum termo de regulação, registro, avaliação ou conformidade foi normalizado como sinal de aplicação na rodada atual.", "Executar NQ20 em Crossref e expandir para fontes regulatórias públicas."],
        ["Resolução de família patentária", "As obras patentárias estão normalizadas por publicação e ainda não foram agrupadas em famílias INPADOC ou equivalentes.", "Consultar dados de família em rodada própria, mantendo publicação e prioridade separadas."],
        ["Origem institucional brasileira completa", "A classificação local usa apenas marcadores explícitos presentes no snippet/ator; muitos registros permanecem como origem não resolvida.", "Expandir busca de titular/inventor e cruzar instituições com fonte oficial, sem inferir origem pelo filtro BR."],
        ["Eficácia e adoção", "O corpus metadata-only não contém evidência suficiente sobre desempenho agronômico, registro comercial ou adoção.", "Criar trilha posterior com ensaios, registros e fontes regulatórias, sem misturar com descoberta patentária."],
    ]

    refs = []
    for index, row in enumerate(query_stats, 1):
        refs.append(f"[{index}]: {row['source_url']} — Google Patents, consulta `{row['query']}`.")

    radiography = f"""# Radiografia Exploratória V0

**Laboratório:** Inteligência Biotecnológica Agropecuária  
**Corpus de partida:** {len(works)} obras/registros normalizados  
**Gerado em:** {datetime.now(timezone.utc).isoformat()}  
**Modo:** exploratório, metadata-only

## O que apareceu primeiro

O corpus já se comporta como uma rede de **tecnologias, organismos, processos, atores e aplicações**, e não como uma lista homogênea de documentos. A estrutura mais forte da rodada atual é uma bifurcação entre **capacidade local de produção e controle de bioinsumos** e **presença de plataformas internacionais protegidas no Brasil**. Essa bifurcação é um padrão de proveniência e vocabulário, não uma conclusão sobre nacionalidade de toda a tecnologia.

O segundo sinal forte é a formação de uma trilha de **fixação de nitrogênio** que combina microrganismos, genética, formulação, estabilidade e liberação. O terceiro é a transversalidade de **Trichoderma**, que aparece em contextos de biocontrole, produção, enzimas, formulação e carbono. O quarto é metodológico: o vocabulário muda drasticamente o recall. `biological control + BR` retorna 56.223 resultados observados, enquanto `bioinput + BR` retorna 49; a diferença tornou o próprio vocabulário um objeto de investigação.

## A. Clusters operacionais encontrados

Os clusters abaixo são agrupamentos exploratórios baseados em termos e padrões observados no corpus. Um registro pode pertencer a mais de um cluster. O arquivo [`cluster_memberships_v0.jsonl`](cluster_memberships_v0.jsonl) preserva a ligação de cada membership com título, query e proveniência.

{md_table(['Cluster', 'Descrição', 'Registros', 'Distribuição por fonte'], cluster_rows)}

O cluster `C00_unclassified_current_rules` representa registros que não encontraram correspondência nas regras atuais. Ele não significa irrelevância; representa o espaço onde o corpus pode estar indicando uma taxonomia ainda ausente.

## B. Hubs e atores relevantes

### Atores por relações observadas

{md_table(['Ator', 'Relações', 'Fonte', 'Papéis'], top_actor_rows)}

### Instituições por relações observadas

{md_table(['Instituição', 'Relações', 'Fonte'], top_institution_rows)}

Os rankings acima contam relações presentes no inventário. Eles não são ranking de mercado, qualidade, titularidade econômica ou impacto.

### Atores que atravessam mais de uma camada

"""
    bridge_rows = [[row["display_name"], ", ".join(row["sources"]), row["count"], "; ".join(row["variants"][:3])] for row in cross_layer_actors[:20]]
    radiography += md_table(['Nome canônico', 'Fontes', 'Relações', 'Variações observadas'], bridge_rows) if bridge_rows else "Nenhum ator com o mesmo nome canônico apareceu em mais de uma fonte na rodada atual."

    radiography += f"""

## C. Tecnologias transversais

{md_table(['Termo', 'Clusters atravessados', 'Clusters', 'Obras'], [[row['term'], row['cluster_count'], ', '.join(row['clusters']), row['work_count']] for row in technology_crossings])}

A transversalidade mais concreta não é um único produto; é a recorrência de uma mesma capacidade ou organismo em diferentes camadas. `fungo` atravessa biocontrole, contexto agronômico, formulação e o cluster de Trichoderma. `promocao_crescimento` e `inoculante` conectam nutrição, nitrogênio e contexto agronômico. Os próximos passos devem separar recorrência lexical de conexão tecnológica efetiva.

### Organismos em múltiplos contextos

{md_table(['Organismo/entidade', 'Obras', 'Clusters', 'Fontes'], [[key, value['work_count'], value['cluster_count'], ', '.join(f'{source}: {count}' for source, count in value['sources'].items())] for key, value in sorted(organisms.items(), key=lambda item: (-item[1]['cluster_count'], -item[1]['work_count'], item[0]))])}

## D. Sinais brasileiros observados

Entre os 71 registros patentários, a classificação conservadora identificou **{origin_counts.get('brazilian_signal_observed', 0)}** com marcadores institucionais ou organizacionais brasileiros explícitos no material capturado. Os sinais mais fortes estão associados a USP, UEBA, MCTI/Museu Paraense Emílio Goeldi, APTA, GI, Dosaggio e sistemas de produção ou controle de qualidade de bioinputs. Isso é um sinal de presença institucional no snippet, não prova de titularidade completa, origem de todos os inventores ou maturidade comercial.

## E. Sinais internacionais com presença BR

A mesma regra identificou **{origin_counts.get('international_presence_in_BR', 0)}** registros com atores globais explícitos e publicação no contexto BR, incluindo famílias ou organizações associadas a Pivot Bio, BASF, Syngenta, Monsanto, Bayer, Pioneer, Locus, Novozymes, Terragen e outras. O resultado sustenta uma trilha de investigação sobre tecnologias internacionais que chegam ao Brasil, mas não permite medir proteção de mercado ou liberdade de operação.

### Estados de origem patentária usados nesta radiografia

{md_table(['Estado', 'Registros'], origin_rows)}

Os **{origin_counts.get('origin_unresolved', 0)}** registros em `origin_unresolved` permanecem deliberadamente sem classificação de origem. A ausência de evidência é mantida como estado útil.

## F. Anomalias, concentrações e padrões inesperados

{md_table(['Tipo', 'Evidência', 'Leitura operacional'], anomaly_rows)}

## G. Lacunas e caminhos de investigação

{md_table(['Lacuna', 'O que o corpus mostra', 'Caminho'], gap_rows)}

## H. Recall, densidade e qualidade das consultas

{md_table(['Consulta', 'Resultados observados', 'Capturados', 'Únicos no inventário', 'Com sinal', 'Taxa de sinal'], recall_rows)}

As consultas com recall mais amplo e baixa seletividade são candidatas a reformulação lexical. As consultas pequenas e densas — especialmente `bioinput`, `bioinsumo` e combinações de processo — são candidatas a expansão por termos adjacentes, atores e organismos.

## Próximo movimento: consultas derivadas

A lista completa está em [`next_queries_v0.json`](next_queries_v0.json). Ela contém 20 consultas ranqueadas pelo padrão encontrado, com bloco, evidência de origem, propósito, sinal esperado e ambiguidade a resolver. O próximo ciclo deve começar pelos blocos **B1 Trichoderma transversal**, **B2 plataforma de nitrogênio** e **B3 produção local/qualidade**, antes de ampliar consultas de maior ruído.

## Referências das páginas patentárias

""" + "\n".join(refs) + "\n"
    RADIOGRAPHY_MD.write_text(radiography, encoding="utf-8")

    method = f"""# Método da Radiografia Exploratória V0

## Escopo

A radiografia usa exclusivamente os arquivos normalizados do corpus atual: `works_v0.jsonl`, `actors_v0.jsonl`, `institutions_v0.jsonl`, `relations_v0.jsonl`, `application_signals_v0.jsonl` e o manifesto de ingestão. Nenhuma fonte externa foi consultada para produzir os quatro artefatos desta etapa.

## Regras de agrupamento

Cada obra foi convertida em uma representação textual formada por título, resumo/snippet quando disponível, query, matched queries e sinais observados. As memberships foram atribuídas quando um registro continha um termo de aplicação normalizado ou um padrão lexical associado ao cluster. Os clusters são regras operacionais transparentes, não uma classificação definitiva e não um modelo semântico treinado.

Um registro pode pertencer a múltiplos clusters. Quando nenhuma regra atual encontrou correspondência, foi atribuído a `C00_unclassified_current_rules`. Essa categoria preserva o espaço de descoberta e evita que uma regra incompleta transforme ausência de match em irrelevância.

## Hubs e pontes

Hubs foram calculados pela contagem de relações observadas em `relations_v0.jsonl`. Atores e instituições são rankings de conectividade documental. Pontes de atores foram identificadas por nomes canonicamente normalizados que aparecem em mais de uma fonte; isso não constitui resolução de identidade entre pessoas homônimas.

## Brasileiro, internacional e origem não resolvida

A classificação de patentes usa somente marcadores explícitos presentes nos atores, depositantes, instituições ou snippets já capturados. `brazilian_signal_observed` exige marcador institucional/organizacional brasileiro; `international_presence_in_BR` exige marcador explícito de organização internacional e presença no conjunto filtrado BR; os demais ficam em `origin_unresolved`. O filtro de país BR não é interpretado como origem.

## Recall e densidade

Para cada consulta patentária, o método mantém o volume total observado na página, o número de registros capturados e o número de obras únicas que chegaram ao inventário. A taxa de sinal é calculada apenas dentro dos registros capturados/normalizados daquela consulta. Ela não estima precisão global nem qualidade tecnológica.

## Geração das próximas consultas

As próximas consultas foram geradas a partir de clusters, termos transversais, organismos, sinais de processo, contrastes local/internacional e lacunas explícitas do corpus. Cada consulta carrega seus `evidence_record_ids`, propósito, sinal esperado e ambiguidade. A lista é um plano de investigação, não uma afirmação de que os resultados já existam.

## Proveniência

Cada membership preserva a proveniência do registro de origem. A radiografia usa links para os mesmos arquivos e URLs do manifesto. Nenhum PDF, texto integral ou dado científico foi baixado ou desserializado.

**Registros processados:** {len(works)}  
**Memberships geradas:** {len(membership_rows)}  
**Clusters com registros:** {len(cluster_stats)}  
**Consultas derivadas:** {len(next_queries)}  
**Gerado em:** {datetime.now(timezone.utc).isoformat()}
"""
    METHOD_MD.write_text(method, encoding="utf-8")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "work_count": len(works),
        "membership_count": len(membership_rows),
        "cluster_counts": {key: value["count"] for key, value in cluster_stats.items()},
        "source_counts": dict(Counter(row.get("source") for row in works)),
        "origin_counts_patents": dict(origin_counts),
        "cross_layer_actor_count": len(cross_layer_actors),
        "organism_contexts": organisms,
        "technology_crossings": technology_crossings,
        "query_diagnostics": query_stats,
        "next_query_count": len(next_queries),
        "next_query_blocks": dict(Counter(row["block"] for row in next_queries)),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"works": len(works), "memberships": len(membership_rows), "clusters": {key: value["count"] for key, value in cluster_stats.items()}, "next_queries": len(next_queries), "blocks": dict(Counter(row["block"] for row in next_queries))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
