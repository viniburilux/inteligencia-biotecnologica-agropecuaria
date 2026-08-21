# Entity Resolution V1

> Registro conservador de aliases observados no corpus V2. Este artefato não altera os nomes originais nem afirma identidade jurídica onde o corpus metadata-only não é suficiente.

## Aliases observados com alta confiança

| Canonicalização operacional | Aliases observados | Estado |
|---|---|---|
| Universidade de São Paulo | Universidade de São Paulo, Universidade de São Paulo — USP, USP | observed_alias |
| Empresa Brasileira de Pesquisa Agropecuária (Embrapa) | Embrapa, Embrapa Pesquisa Agropecuaria | observed_alias |
| Pivot Bio, Inc. | Pivot Bio, Pivot Bio, Inc, Pivot Bio, Inc. | observed_alias |

## Grupos relacionados mantidos separados

| Grupo | Estado | Motivo |
|---|---|---|
| Locus / Locus IP / Locus Agriculture / Locus Oil | candidate_group_not_merged | A recorrência conjunta é forte, mas o corpus metadata-only não prova identidade jurídica única; mantidos separados. |
| Novozymes / Novozymes BioAg | candidate_group_not_merged | A semelhança nominal e a recorrência em enzimas/bioprocessos motivam expansão, mas não autorizam fusão automática. |
| BASF / BASF Corporation / BASF Agrochemical Products | candidate_group_not_merged | Possível grupo corporativo, porém o corpus atual não contém prova suficiente para resolver a entidade jurídica. |

## Regra operacional

A resolução segura é aplicada somente como camada de leitura e consulta. O corpus `normalized_v2` continua preservando os nomes capturados, os IDs de origem e a proveniência de cada ocorrência. Grupos como Locus, Novozymes e BASF são tratados como famílias candidatas para novas buscas, não como entidades fundidas.

## Fonte

Corpus cumulativo `normalized_v2`, incluindo manifests V0, V1 e V2; buscas Google Patents metadata-only e lotes OpenAlex preservados no repositório.
