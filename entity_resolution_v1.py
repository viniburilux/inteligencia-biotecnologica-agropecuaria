import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NORM = ROOT / "normalized_v2"
OUT_JSON = ROOT / "ENTITY_RESOLUTION_V1.json"
OUT_MD = ROOT / "ENTITY_RESOLUTION_V1.md"


def read_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def fold(value):
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("—", "-")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()

actors = read_jsonl(NORM / "actors_v2.jsonl")
institutions = read_jsonl(NORM / "institutions_v2.jsonl")

name_counts = Counter()
name_records = defaultdict(list)
for row in actors + institutions:
    name = (row.get("display_name") or "").strip()
    if not name:
        continue
    name_counts[name] += 1
    name_records[name].append({
        "id": row.get("actor_id") or row.get("institution_id"),
        "source": row.get("source"),
        "source_id": row.get("source_id"),
        "provenance": row.get("provenance"),
    })

safe_aliases = [
    {
        "canonical_name": "Universidade de São Paulo",
        "entity_type": "institution",
        "status": "observed_alias",
        "confidence": "high",
        "aliases": ["Universidade de São Paulo", "Universidade de São Paulo — USP", "USP"],
        "evidence": [
            "As três formas aparecem no corpus V2 em registros de literatura e patentes.",
            "A forma expandida e a sigla aparecem associadas ao mesmo contexto institucional no caderno de expansão.",
        ],
    },
    {
        "canonical_name": "Empresa Brasileira de Pesquisa Agropecuária (Embrapa)",
        "entity_type": "institution",
        "status": "observed_alias",
        "confidence": "high",
        "aliases": ["Embrapa", "Embrapa Pesquisa Agropecuaria"],
        "evidence": [
            "As formas aparecem em registros patentários V1/V2 ligados a formulações, biorreatores e biofertilizantes.",
            "A abreviação é explicitamente usada como forma curta da instituição nos próprios resultados capturados.",
        ],
    },
    {
        "canonical_name": "Pivot Bio, Inc.",
        "entity_type": "organization",
        "status": "observed_alias",
        "confidence": "high",
        "aliases": ["Pivot Bio", "Pivot Bio, Inc", "Pivot Bio, Inc."],
        "evidence": [
            "O mesmo portfólio aparece repetidamente em registros sobre fixação de nitrogênio, fósforo, formulação e estabilidade.",
            "As variações de pontuação e sufixo corporativo são observadas nos resultados capturados.",
        ],
    },
]

candidate_groups = [
    {
        "group_id": "locus_family",
        "label": "Locus / Locus IP / Locus Agriculture / Locus Oil",
        "status": "candidate_group_not_merged",
        "members": ["Locus", "Locus IP", "Locus Agriculture", "Locus Oil"],
        "reason": "A recorrência conjunta é forte, mas o corpus metadata-only não prova identidade jurídica única; mantidos separados.",
        "evidence_queries": ["Trichoderma sophorolipid fermentation biocontrol", "Locus microbial phosphate enzyme organic matter Brazil"],
    },
    {
        "group_id": "novozymes_family",
        "label": "Novozymes / Novozymes BioAg",
        "status": "candidate_group_not_merged",
        "members": ["Novozymes", "Novozymes Bioag"],
        "reason": "A semelhança nominal e a recorrência em enzimas/bioprocessos motivam expansão, mas não autorizam fusão automática.",
        "evidence_queries": ["Trichoderma fermentation", "Trichoderma enzyme fermentation", "Trichoderma industrial enzyme Novozymes"],
    },
    {
        "group_id": "basf_family",
        "label": "BASF / BASF Corporation / BASF Agrochemical Products",
        "status": "candidate_group_not_merged",
        "members": ["BASF", "BASF Corporation", "BASF Agrochemical Products"],
        "reason": "Possível grupo corporativo, porém o corpus atual não contém prova suficiente para resolver a entidade jurídica.",
        "evidence_queries": ["biocontrole BR", "Bacillus thuringiensis BR"],
    },
]

resolved = []
for item in safe_aliases:
    alias_rows = []
    for alias in item["aliases"]:
        alias_rows.append({"alias": alias, "folded": fold(alias), "observed_count": name_counts.get(alias, 0), "records": name_records.get(alias, [])})
    resolved.append({**item, "aliases": alias_rows})

payload = {
    "version": "entity_resolution_v1",
    "metadata_only": True,
    "source_corpus": "normalized_v2",
    "policy": "Only high-confidence observed aliases are grouped; candidate corporate families remain unmerged.",
    "safe_aliases": resolved,
    "candidate_groups": candidate_groups,
    "unresolved_examples": [
        {"name": name, "count": count} for name, count in name_counts.most_common(60)
        if any(token in fold(name) for token in ["locus", "novozymes", "basf", "syngenta", "monsanto", "usp", "pivot bio", "embrapa"])
        and not any(name in item["aliases"] for item in safe_aliases)
    ][:30],
}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

lines = [
    "# Entity Resolution V1",
    "",
    "> Registro conservador de aliases observados no corpus V2. Este artefato não altera os nomes originais nem afirma identidade jurídica onde o corpus metadata-only não é suficiente.",
    "",
    "## Aliases observados com alta confiança",
    "",
    "| Canonicalização operacional | Aliases observados | Estado |",
    "|---|---|---|",
]
for item in resolved:
    aliases = ", ".join(a["alias"] for a in item["aliases"])
    lines.append(f"| {item['canonical_name']} | {aliases} | {item['status']} |")
lines += ["", "## Grupos relacionados mantidos separados", "", "| Grupo | Estado | Motivo |", "|---|---|---|"]
for group in candidate_groups:
    lines.append(f"| {group['label']} | {group['status']} | {group['reason']} |")
lines += [
    "",
    "## Regra operacional",
    "",
    """A resolução segura é aplicada somente como camada de leitura e consulta. O corpus `normalized_v2` continua preservando os nomes capturados, os IDs de origem e a proveniência de cada ocorrência. Grupos como Locus, Novozymes e BASF são tratados como famílias candidatas para novas buscas, não como entidades fundidas.""",
    "",
    "## Fonte",
    "",
    "Corpus cumulativo `normalized_v2`, incluindo manifests V0, V1 e V2; buscas Google Patents metadata-only e lotes OpenAlex preservados no repositório.",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"safe_aliases": len(resolved), "candidate_groups": len(candidate_groups), "output": str(OUT_JSON)}, ensure_ascii=False))
