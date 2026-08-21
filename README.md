# Inteligência Biotecnológica Agropecuária — O Laboratório de Fronteira

> "Não estamos esperando as condições perfeitas. Estamos mapeando a evidência."

## A História por trás do Código
A biotecnologia agrícola e industrial avança em ritmos vertiginosos, mas a maior parte do conhecimento global está enterrada em milhões de patentes opacas e literatura fragmentada. Este laboratório nasceu para resolver esse problema. Usando agentes autônomos e motores de busca semântica, mapeamos em tempo real o que as gigantes internacionais e as instituições de ponta estão construindo — da proteção de cultivos ao aproveitamento de biorreatores.

Para quem busca entender a soberania biológica brasileira, este repositório é a porta de entrada.

---

## Início:

**21 DE AGOSTO DE 2026.**
DIA ZERO

Começamos.

Não sabemos ainda onde a investigação vai chegar.

Já sabemos que vamos descobrir olhando para os dados.

379 → 429 registros em dois ciclos.
Patentes · Ciência · Atores · Tecnologias · Aplicações

> **Construir. Perguntar. Documentar. Mostrar.**

## O problema

Existe uma quantidade enorme de patentes, artigos, tecnologias, empresas, universidades e sinais de inovação espalhados pelo mundo. O problema não é apenas encontrar informação. É transformar informação dispersa em inteligência utilizável.

Este laboratório vai investigar quem está desenvolvendo o quê, quais tecnologias estão emergindo, onde estão as fronteiras tecnológicas, quais aplicações estão surgindo, onde existem lacunas e onde aparecem oportunidades.

Patentes serão uma das principais fontes. Não serão a única. A investigação deverá cruzar evidências de propriedade intelectual, literatura científica, organizações, tecnologias, aplicações e contexto de mercado quando isso for justificável.

## O que estamos construindo

Uma infraestrutura aberta para:

- coletar e organizar metadata pública de patentes e literatura;
- acompanhar famílias tecnológicas, depositantes, inventores, instituições e aplicações;
- comparar tecnologias e sinais de atividade;
- tornar relações, lacunas e anomalias investigáveis;
- registrar como perguntas se transformam em evidência, análise e descoberta;
- publicar resultados reproduzíveis sem fingir certeza onde existe apenas hipótese.

O objetivo não é lançar um dashboard vazio nem produzir um relatório que ninguém lê. É construir algo que possa ser usado para descobrir, comparar, decidir e criar valor.

## Primeira entrega: Inventário Metadata-only V0

A primeira rodada colocou no ar um corpus integrado com **379 obras e registros**, incluindo **71 publicações patentárias capturadas via Google Patents**, além de 1.345 atores, 353 instituições, 1.854 relações observadas e 270 sinais de aplicação. Essa base foi congelada como ponto de partida da Radiografia Exploratória V0. A camada científica combina OpenAlex e Crossref; a camada patentária preserva consultas, snippets, identificadores, hashes e o filtro BR sem transformar esse filtro em prova de origem brasileira.

A segunda rodada, orientada pela radiografia, acrescentou **50 registros patentários únicos entre consultas** e **25 obras OpenAlex**. Após deduplicação conservadora entre fontes e consultas, o corpus passou a **429 obras e registros**, com 97 registros patentários, 1.499 atores, 381 instituições, 2.093 relações observadas e 313 sinais de aplicação.

A expansão V1/V2 seguiu atores, organismos, tecnologias e lacunas que apareceram no próprio corpus. Foram investigados biorreatores, fermentação asséptica, produção on-farm, controle de qualidade, Trichoderma, Bacillus, Rhizobium, Azospirillum, Pivot Bio, Locus, Novozymes e Petrobras. A Radiografia V1 incorporou cinco consultas OpenAlex, 12 consultas patentárias e três reformulações que abriram registros onde as perguntas originais eram insuficientes. O corpus cumulativo publicado passou a **763 obras**, com **195 registros patentários**, **2.680 atores**, **767 instituições**, **4.045 relações observadas** e **536 sinais de aplicação**. A camada regulatória adicionou fontes oficiais do MAPA sobre bioinsumos, sem misturar contexto regulatório com evidência de patente.

| Entrega | Acesso |
|---|---|
| Inventário legível | [`INVENTORY_V0.md`](INVENTORY_V0.md) |
| Mapa de Sinais V0 | [`SIGNAL_MAP_V0.md`](SIGNAL_MAP_V0.md) |
| Mapa computável | [`signal_map_v0.json`](signal_map_v0.json) |
| Corpus normalizado | [`normalized_v0/`](normalized_v0/) |
| Contrato de ingestão | [`INGESTION_CONTRACT_V0.md`](INGESTION_CONTRACT_V0.md) |
| Registro da coleta patentária | [`PATENT_SOURCE_FINDINGS_V0.md`](PATENT_SOURCE_FINDINGS_V0.md) |
| Parser patentário V0 | [`parse_google_patents_v0.py`](parse_google_patents_v0.py) |
| Radiografia Exploratória V0 | [`EXPLORATORY_RADIOGRAPHY_V0.md`](EXPLORATORY_RADIOGRAPHY_V0.md) |
| Memberships de clusters | [`cluster_memberships_v0.jsonl`](cluster_memberships_v0.jsonl) |
| Próximas consultas derivadas | [`next_queries_v0.json`](next_queries_v0.json) |
| Método da radiografia | [`RADIOGRAPHY_METHOD_V0.md`](RADIOGRAPHY_METHOD_V0.md) |
| Plano da segunda rodada | [`SECOND_ROUND_PLAN_V0.json`](SECOND_ROUND_PLAN_V0.json) |
| Achados patentários da segunda rodada | [`SECOND_ROUND_PATENT_FINDINGS_V0.md`](SECOND_ROUND_PATENT_FINDINGS_V0.md) |
| Resumo da segunda rodada | [`SECOND_ROUND_INGESTION_SUMMARY_V0.md`](SECOND_ROUND_INGESTION_SUMMARY_V0.md) |
| Perfil de expansão V1 | [`EXPANSION_PROFILE_V1.json`](EXPANSION_PROFILE_V1.json) |
| Perfil cumulativo V2 | [`EXPANSION_PROFILE_V2.json`](EXPANSION_PROFILE_V2.json) |
| Queries de expansão V1/V2 | [`EXPANSION_QUERIES_V1.json`](EXPANSION_QUERIES_V1.json) · [`EXPANSION_QUERIES_V2.json`](EXPANSION_QUERIES_V2.json) |
| Achados patentários da expansão | [`EXPANSION_PATENT_FINDINGS_V1.md`](EXPANSION_PATENT_FINDINGS_V1.md) · [`EXPANSION_PATENT_FINDINGS_V2.md`](EXPANSION_PATENT_FINDINGS_V2.md) |
| Radiografia Exploratória V1 | [`EXPLORATORY_RADIOGRAPHY_V1.md`](EXPLORATORY_RADIOGRAPHY_V1.md) |
| Método da Radiografia V1 | [`RADIOGRAPHY_METHOD_V1.md`](RADIOGRAPHY_METHOD_V1.md) |
| Execução das queries V1 | [`RADIOGRAPHY_V1_EXECUTION_SUMMARY.md`](RADIOGRAPHY_V1_EXECUTION_SUMMARY.md) · [`RADIOGRAPHY_V1_QUERY_EXECUTION.json`](RADIOGRAPHY_V1_QUERY_EXECUTION.json) |
| Achados patentários da Radiografia V1 | [`RADIOGRAPHY_V1_PATENT_FINDINGS.md`](RADIOGRAPHY_V1_PATENT_FINDINGS.md) |
| Resolução conservadora de entidades | [`ENTITY_RESOLUTION_V1.md`](ENTITY_RESOLUTION_V1.md) · [`ENTITY_RESOLUTION_V1.json`](ENTITY_RESOLUTION_V1.json) |
| Fontes regulatórias e de aplicação | [`REGULATORY_APPLICATION_SOURCES_V1.md`](REGULATORY_APPLICATION_SOURCES_V1.md) |
| Corpus cumulativo | [`normalized_v2/`](normalized_v2/) |

A entrega não tenta encerrar a investigação. Ela cria uma base pública para perguntar **quem aparece**, **quais tecnologias se repetem**, **quais relações surgem** e **onde a evidência ainda não existe**.

## Sem esperar condições perfeitas

Esta investigação não nasceu para parecer acadêmica, nem para esperar milhões em investimento antes de começar. Ela será construída com dados públicos, automação, inteligência artificial, computação disponível e método.

**Velocidade** para construir e testar rápido.  
**Rigor** para rastrear afirmações importantes até suas fontes.  
**Competência** para demonstrar, não apenas declarar.  
**Inovação** para encontrar relações, lacunas e possibilidades.  
**Tecnologia** para multiplicar a capacidade de investigação.

Não é preciso acreditar antecipadamente. **Acompanhe.**

Cada fonte relevante será identificada. Cada etapa importante será registrada. Cada hipótese poderá ser contestada. Cada resultado poderá estar errado. Se estiver errado, corrigimos. Se funcionar, mostramos.

## Como ler este repositório

A investigação separará explicitamente quatro estados:

| Estado | Significado |
|---|---|
| **Observado** | Informação diretamente presente em uma fonte identificada. |
| **Inferido** | Padrão derivado de evidências observadas, com a regra de inferência explicitada. |
| **Hipótese** | Possibilidade ainda não validada. Não é conclusão. |
| **Descoberto** | Resultado que sobreviveu a verificações e comparação com as fontes relevantes. |

A ausência de evidência também será registrada. Um candidato não será chamado de adequado, inovador, comercialmente viável ou cientificamente relevante apenas porque aparece em uma busca.

## O que estará público — e o que não estará

A camada pública poderá conter infraestrutura, contratos, schemas, métodos genéricos, queries, fixtures metadata-only, manifests, resultados reproduzíveis e a história da investigação.

A camada privada continuará reservada para credenciais, memória operacional, dados derivados sensíveis, decisões estratégicas, experimentos não publicados, análises proprietárias e qualquer material cuja divulgação possa prejudicar o trabalho ou terceiros.

## Linha do tempo

| Data | Marco |
|---|---|
| **21/08/2026** | Dia zero: nascimento do laboratório e publicação da origem. |
| **21/08/2026** | Primeira ingestão heterogênea: OpenAlex, Crossref e Google Patents. |
| **21/08/2026** | Inventário Metadata-only V0 e Mapa de Sinais V0 publicados. |
| **21/08/2026** | Radiografia Exploratória V0 executada sobre o corpus congelado de 379 registros. |
| **21/08/2026** | Segunda rodada orientada pelo corpus: Trichoderma, nitrogênio, fosfato, fermentação, produção on-farm e controle de qualidade. |
| **21/08/2026** | Expansão V1/V2: atores, organismos, tecnologias, relações, fontes regulatórias e consultas de contraste. |
| **21/08/2026** | Radiografia Exploratória V1: 17 queries executadas; reformulações abriram lacunas antes insuficientes. |
| **21/08/2026** | Corpus cumulativo atualizado para 763 obras, com proveniência e deduplicação publicadas. |
| Próximo marco | Continuar o ciclo com as perguntas V2 derivadas da Radiografia V1, sem congelar as trilhas abertas. |

A linha do tempo vai crescer junto com a investigação. O objetivo é preservar a arqueologia da descoberta, não apenas o resultado final.

## Status

**Modo exploratório ativo.** O laboratório já tem uma camada pública de ingestão, normalização, resolução conservadora de entidades, radiografia e descoberta orientada por consultas. O corpus original de 379 registros derivou a segunda rodada; as expansões V1/V2 e a Radiografia V1 foram executadas e incorporadas ao corpus cumulativo de 763 obras.

> Não estamos esperando as condições perfeitas para começar.

## Próximos passos

O ciclo agora é **corpus → radiografia → pergunta → ingestão → nova radiografia**. A expansão já investigou a ponte brasileira entre fermentação, biorreatores, produção on-farm e bioinsumos; a trilha internacional de fixação/solubilização, formulação e estabilidade; o corredor Trichoderma–enzimas–bioprocessos; e o sinal Petrobras–microalgas–CO₂–fertilizante. As próximas perguntas serão derivadas do corpus cumulativo, preservando as trilhas fortes, as reformulações que funcionaram e as lacunas que ainda precisam de fonte.

## Licença e uso

A licença dos componentes de software e dos artefatos públicos será definida conforme a natureza de cada material. Patentes, artigos, marcas e dados de terceiros continuam sujeitos aos direitos e termos de suas fontes originais.

Este repositório não oferece aconselhamento jurídico, técnico, científico ou de investimento. Ele registra uma investigação aberta e verificável.

---

**Constrói. Documenta. Mostra.**
