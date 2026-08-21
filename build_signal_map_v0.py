import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NORMALIZED = ROOT / "normalized_v0"
MANIFEST = ROOT / "ingestion_manifest_v0.jsonl"
OUT_JSON = ROOT / "signal_map_v0.json"
OUT_MD = ROOT / "SIGNAL_MAP_V0.md"
INVENTORY_JSON = ROOT / "inventory_catalog_v0.json"
INVENTORY_MD = ROOT / "INVENTORY_V0.md"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return "\n".join(lines)


def year_for(work):
    if work.get("publication_year"):
        return str(work["publication_year"])
    publication = work.get("publication") or {}
    if isinstance(publication, dict):
        parts = publication.get("date-parts") or publication.get("date_parts") or []
        if parts and parts[0]:
            return str(parts[0][0])
    dates = work.get("dates") or {}
    for key in ("published_date", "priority_date", "filed_date"):
        value = dates.get(key)
        if value:
            return str(value)[:4]
    return "unknown"


def safe_count(counter, limit=20):
    return [[key, value] for key, value in counter.most_common(limit)]


def main():
    works = read_jsonl(NORMALIZED / "works_v0.jsonl")
    actors = read_jsonl(NORMALIZED / "actors_v0.jsonl")
    institutions = read_jsonl(NORMALIZED / "institutions_v0.jsonl")
    relations = read_jsonl(NORMALIZED / "relations_v0.jsonl")
    signals = read_jsonl(NORMALIZED / "application_signals_v0.jsonl")
    manifest = read_jsonl(MANIFEST)

    actors_by_id = {row.get("actor_id"): row for row in actors}
    institutions_by_id = {row.get("institution_id"): row for row in institutions}

    source_counts = Counter(row.get("source") for row in works)
    entity_counts = Counter(row.get("entity_type") for row in works)
    signal_counts = Counter(term for row in signals for term in row.get("terms", []))
    signal_source_counts = defaultdict(Counter)
    for row in signals:
        for term in row.get("terms", []):
            signal_source_counts[term][row.get("source")] += 1

    query_counts = Counter()
    for work in works:
        if work.get("source") != "google_patents":
            continue
        queries = work.get("matched_queries") or [work.get("query")]
        for query in queries:
            if query:
                query_counts[query] += 1

    year_counts = defaultdict(Counter)
    for work in works:
        year_counts[work.get("source")][year_for(work)] += 1

    actor_relation_counts = Counter()
    institution_relation_counts = Counter()
    predicate_counts = Counter()
    for relation in relations:
        predicate = relation.get("predicate")
        predicate_counts[predicate] += 1
        if predicate in {"authored_by", "invented_by", "assigned_to"}:
            actor_relation_counts[relation.get("object_id")] += 1
        if predicate in {"has_institution", "assigned_to_institution"}:
            institution_relation_counts[relation.get("object_id")] += 1

    top_actors = []
    for actor_id, count in actor_relation_counts.most_common(20):
        row = actors_by_id.get(actor_id, {})
        top_actors.append({"id": actor_id, "display_name": row.get("display_name"), "count": count, "source": row.get("source"), "roles": row.get("roles", [])})
    top_institutions = []
    for institution_id, count in institution_relation_counts.most_common(20):
        row = institutions_by_id.get(institution_id, {})
        top_institutions.append({"id": institution_id, "display_name": row.get("display_name"), "count": count, "source": row.get("source")})

    patent_manifest = [row for row in manifest if row.get("source") == "google_patents" and row.get("status") == "captured"]
    patent_query_results = []
    for row in patent_manifest:
        patent_query_results.append({"query": row.get("query"), "observed_result_count": row.get("observed_result_count"), "returned_items": row.get("returned_items"), "url": row.get("url"), "saved_path": row.get("saved_path")})

    signal_map = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metadata_only": True,
        "corpus": {"works": len(works), "actors": len(actors), "institutions": len(institutions), "relations": len(relations), "application_signals": len(signals)},
        "source_mix": dict(source_counts),
        "entity_mix": dict(entity_counts),
        "patent_query_unique_work_counts": dict(query_counts),
        "patent_query_capture_counts": patent_query_results,
        "application_signal_counts": dict(signal_counts),
        "application_signal_by_source": {term: dict(counter) for term, counter in sorted(signal_source_counts.items())},
        "work_year_counts_by_source": {source: dict(sorted(counter.items())) for source, counter in sorted(year_counts.items())},
        "relation_predicate_counts": dict(predicate_counts),
        "top_actors_by_observed_relations": top_actors,
        "top_institutions_by_observed_relations": top_institutions,
        "notes": [
            "Counts are generated from normalized metadata-only JSONL files.",
            "Patent query counts represent unique normalized publication records matched to each query; the same patent can match multiple queries.",
            "Actor and institution rankings count observed relations, not market share, legal ownership, activity, or commercial success.",
            "Google Patents country BR remains a search context and is not treated as proof of Brazilian origin."
        ]
    }
    OUT_JSON.write_text(json.dumps(signal_map, ensure_ascii=False, indent=2), encoding="utf-8")

    source_rows = [[source, count, f"{count / len(works):.1%}"] for source, count in source_counts.most_common()]
    term_rows = [[term, count, ", ".join(f"{source}: {value}" for source, value in signal_source_counts[term].most_common())] for term, count in signal_counts.most_common()]
    query_rows = [[row["query"], row["observed_result_count"] or "não registrado", row["returned_items"], query_counts.get(row["query"], 0), row["saved_path"]] for row in patent_query_results]
    actor_rows = [[row["display_name"], row["count"], ", ".join(row.get("roles", [])), row.get("source") or ""] for row in top_actors[:15]]
    institution_rows = [[row["display_name"], row["count"], row.get("source") or ""] for row in top_institutions[:15]]

    references = []
    for index, row in enumerate(patent_manifest, start=1):
        references.append(f"[{index}]: {row.get('url')} — Google Patents, consulta `{row.get('query')}`.")

    map_md = f"""# Mapa de Sinais V0

**Laboratório:** Inteligência Biotecnológica Agropecuária  
**Gerado em:** {signal_map['generated_at']}  
**Modo:** metadata-only

O Mapa de Sinais V0 é uma leitura computável do primeiro corpus integrado. Ele combina literatura capturada via OpenAlex e Crossref com registros patentários capturados da página pública do Google Patents. Os números abaixo descrevem o que foi ingerido e normalizado; não são estimativas de mercado, validade jurídica, eficácia agronômica ou origem nacional.

## Composição do corpus

{md_table(['Fonte', 'Obras/registros', 'Participação'], source_rows)}

O corpus contém **{len(works)} obras/registros**, **{len(actors)} atores**, **{len(institutions)} instituições**, **{len(relations)} relações observadas** e **{len(signals)} sinais de aplicação**.

## Consultas patentárias

A tabela separa o volume total observado na página de resultados (`observed_result_count`), os registros metadata-only capturados na primeira página (`returned_items`) e o número de registros únicos que chegaram ao inventário normalizado. Um mesmo documento pode aparecer em mais de uma consulta, por isso os totais por consulta não devem ser somados como documentos distintos.

{md_table(['Consulta', 'Resultados totais observados', 'Registros capturados', 'Registros únicos no inventário', 'Arquivo bruto'], query_rows)}

## Eixos tecnológicos observados

{md_table(['Sinal de aplicação', 'Ocorrências', 'Distribuição por fonte'], term_rows)}

Os sinais são derivados de termos encontrados em títulos, assuntos ou snippets capturados. Eles funcionam como ponte para exploração posterior, não como classificação definitiva de tecnologia.

## Atores mais conectados

{md_table(['Ator', 'Relações observadas', 'Papéis', 'Fonte do registro'], actor_rows)}

## Instituições mais conectadas

{md_table(['Instituição', 'Relações observadas', 'Fonte do registro'], institution_rows)}

## Distribuição temporal

"""
    for source, counts in sorted(year_counts.items()):
        ordered = [[year, count] for year, count in sorted(counts.items()) if year != "unknown"]
        map_md += f"### {source}\n\n{md_table(['Ano', 'Registros'], ordered)}\n\n"

    map_md += """## Leitura operacional

O primeiro mapa já permite trabalhar com quatro trilhas de exploração: **bioinsumos e sistemas locais de produção**, **biocontrole e biopesticidas**, **fixação de nitrogênio e solubilização de fosfato**, e **processos de formulação, fermentação e monitoramento de qualidade**. A separação entre volume de recall e precisão ainda deve ser feita em uma camada posterior; nesta rodada, o objetivo foi colocar volume heterogêneo no inventário e preservar as rotas de origem.

> O corpus preserva ausência de evidência como estado operacional. A presença de um registro ou termo no mapa não comprova produto comercial, eficácia, validade, liberdade de operação, adoção por agricultores ou titularidade econômica.

## Arquivos de apoio

| Artefato | Função |
|---|---|
| `normalized_v0/works_v0.jsonl` | Obras científicas e patentes normalizadas. |
| `normalized_v0/actors_v0.jsonl` | Atores extraídos das fontes. |
| `normalized_v0/institutions_v0.jsonl` | Instituições observadas. |
| `normalized_v0/relations_v0.jsonl` | Relações de autoria, invenção, atribuição e afiliação. |
| `normalized_v0/application_signals_v0.jsonl` | Sinais de aplicação derivados dos metadados. |
| `signal_map_v0.json` | Mesmo mapa em formato computável. |
| `patent_parser_summary_v0.json` | Resumo do parser patentário. |
| `PATENT_SOURCE_FINDINGS_V0.md` | Registro de captura e limites das páginas consultadas. |

## Referências das páginas patentárias

""" + "\n".join(references) + "\n"
    OUT_MD.write_text(map_md, encoding="utf-8")

    inventory = {
        "generated_at": signal_map["generated_at"],
        "metadata_only": True,
        "inventory_version": "v0",
        "counts": signal_map["corpus"],
        "source_mix": signal_map["source_mix"],
        "files": {
            "works": "normalized_v0/works_v0.jsonl",
            "actors": "normalized_v0/actors_v0.jsonl",
            "institutions": "normalized_v0/institutions_v0.jsonl",
            "relations": "normalized_v0/relations_v0.jsonl",
            "application_signals": "normalized_v0/application_signals_v0.jsonl",
            "normalization_summary": "normalized_v0/normalization_summary_v0.json",
            "signal_map_json": "signal_map_v0.json",
            "signal_map_markdown": "SIGNAL_MAP_V0.md",
            "patent_raw": "raw_v0/google_patents/",
            "manifest": "ingestion_manifest_v0.jsonl",
        },
        "scope": ["biotecnologia agropecuaria brasileira", "bioinsumos", "biocontrole", "inoculantes", "biofertilizantes", "biopesticidas", "fixação de nitrogênio", "solubilização de fosfato", "saúde radicular", "fermentação e monitoramento de bioinputs"],
        "limits": ["metadata-only", "sem PDFs ou texto integral", "sem desserialização de dados científicos", "sem resolução de entidades entre fontes", "filtro BR do Google Patents não implica origem brasileira"],
    }
    INVENTORY_JSON.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    inventory_md = f"""# Inventário Metadata-only V0

**Laboratório:** Inteligência Biotecnológica Agropecuária  
**Gerado em:** {inventory['generated_at']}

O inventário V0 reúne **{len(works)} obras/registros**, **{len(actors)} atores**, **{len(institutions)} instituições**, **{len(relations)} relações** e **{len(signals)} sinais de aplicação**. A mistura de fontes é: {', '.join(f'{source}={count}' for source, count in source_counts.items())}.

## Entregáveis

| Camada | Arquivo | Registros |
|---|---|---:|
| Obras e patentes | `normalized_v0/works_v0.jsonl` | {len(works)} |
| Atores | `normalized_v0/actors_v0.jsonl` | {len(actors)} |
| Instituições | `normalized_v0/institutions_v0.jsonl` | {len(institutions)} |
| Relações | `normalized_v0/relations_v0.jsonl` | {len(relations)} |
| Sinais de aplicação | `normalized_v0/application_signals_v0.jsonl` | {len(signals)} |
| Mapa computável | `signal_map_v0.json` | 1 |
| Mapa legível | `SIGNAL_MAP_V0.md` | 1 |

## Cobertura

O escopo de ingestão cobre bioinsumos, biocontrole, inoculantes, biofertilizantes, biopesticidas, fixação de nitrogênio, solubilização de fosfato, saúde radicular, fermentação e monitoramento de bioinputs. A camada patentária contém **{source_counts.get('google_patents', 0)} registros de publicação BR normalizados**, deduplicados por identificador de publicação no corpus integrado.

## Proveniência e limites

Cada registro normalizado mantém referência ao manifesto, ao arquivo bruto e ao hash da captura. Os registros do Google Patents foram extraídos de páginas públicas de resultados e mantêm a consulta e o filtro de país BR. Nenhum PDF, documento integral, sequência, anexo ou dado científico foi baixado. Os artefatos são adequados para descoberta e organização de sinais; não devem ser usados isoladamente para conclusão jurídica, regulatória, comercial ou agronômica.

Para a leitura dos sinais, consulte [`SIGNAL_MAP_V0.md`](SIGNAL_MAP_V0.md). Para a cadeia de captura patentária, consulte [`PATENT_SOURCE_FINDINGS_V0.md`](PATENT_SOURCE_FINDINGS_V0.md).
"""
    INVENTORY_MD.write_text(inventory_md, encoding="utf-8")
    print(json.dumps({"inventory": inventory["counts"], "source_mix": source_counts, "top_terms": signal_counts.most_common(10)}, ensure_ascii=False, default=dict))


if __name__ == "__main__":
    main()
