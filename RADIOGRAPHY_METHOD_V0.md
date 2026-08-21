# Método da Radiografia Exploratória V0

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

**Registros processados:** 379  
**Memberships geradas:** 681  
**Clusters com registros:** 7  
**Consultas derivadas:** 20  
**Gerado em:** 2026-08-21T05:08:13.832317+00:00
