# Inteligência Biotecnológica Agropecuária

> **Uma infraestrutura aberta para enxergar onde a biotecnologia está indo.**

Este repositório é a parte pública de um laboratório em construção. A proposta não é apenas reunir patentes ou artigos, mas criar uma capacidade contínua para coletar sinais dispersos, organizar relações, formular novas perguntas e tornar o caminho da investigação visível para outras pessoas.

## Entre pela visão

A [GitHub Pages do projeto](https://viniburilux.github.io/inteligencia-biotecnologica-agropecuaria/) apresenta a visão, as camadas da infraestrutura, o ciclo de investigação e alguns pontos de acesso aos achados. Este README é a ponte para dentro: aqui ficam o registro de origem, o estado atual da construção e os artefatos que permitem acompanhar o trabalho de verdade.

## O que este projeto quer tornar possível

Patentes, literatura, atores, instituições, tecnologias e aplicações costumam aparecer separados. A infraestrutura pretende colocá-los em um mesmo campo investigável, sem esconder a origem dos dados e sem transformar uma primeira hipótese em certeza. O resultado esperado é uma base para **descobrir, comparar, acompanhar movimentos e abrir novas trilhas**.

> **Construir. Perguntar. Documentar. Mostrar.**

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

Uma infraestrutura aberta para investigação documental e inteligência aplicada em biotecnologia agropecuária. Metadata é apenas uma camada de entrada; a capacidade agora inclui resolver identificadores, localizar documentos, adquirir conteúdo quando a rota permite, validar identidade e integridade, preservar provenance e preparar o corpus para extração técnica e análises posteriores.

A camada pública registra:

- descoberta e organização de metadata pública de patentes e literatura;
- resolução de documentos, famílias, depositantes, inventores, instituições e aplicações;
- roteamento para fontes de conteúdo e classificação explícita de acesso;
- validação documental por formato, assinatura, identidade, conteúdo e hash;
- manifestos que conectam identificador → fonte → documento → status → provenance;
- relações entre documentos, famílias, tecnologias e evidências;
- preparação de corpus para IA, retrieval, comparação e investigação posterior;
- resultados reproduzíveis sem transformar hipótese em certeza.

A aquisição e o processamento documental detalhado permanecem no Lux-Lab privado. O objetivo não é lançar um dashboard vazio nem produzir um relatório que ninguém lê. É construir uma máquina de investigação que possa ser auditada, reutilizada e aplicada a novos domínios.

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
| Resultados em movimento | [`results/`](results/) |
| Método público de aquisição documental | [`DOCUMENT_ACQUISITION_METHOD_V0.md`](DOCUMENT_ACQUISITION_METHOD_V0.md) |
| Fontes e limites dos adapters | [`DOCUMENT_ACQUISITION_SOURCES_V0.json`](DOCUMENT_ACQUISITION_SOURCES_V0.json) |
| Schema público de manifesto | [`DOCUMENT_ACQUISITION_MANIFEST_SCHEMA_V0.json`](DOCUMENT_ACQUISITION_MANIFEST_SCHEMA_V0.json) |
| Checkpoint público da execução Agro | [`DOCUMENT_ACQUISITION_CHECKPOINT_V0.md`](DOCUMENT_ACQUISITION_CHECKPOINT_V0.md) · [`DOCUMENT_ACQUISITION_CHECKPOINT_V0.json`](DOCUMENT_ACQUISITION_CHECKPOINT_V0.json) |

## Inteligência documental

A execução documental do corpus atual foi realizada em uma camada privada de aquisição. O checkpoint público registra **718 identificadores** — **175 patentes e 543 papers** — com estados separados para `FULL_TEXT_VERIFIED`, `LINK_FOUND`, `METADATA_ONLY`, `ACCESS_RESTRICTED` e `NOT_PROVEN_FULL_TEXT`. Os documentos integrais, textos, logs operacionais e código de aquisição não são redistribuídos aqui.

O método não chama um link de documento. HTTP 200, landing page, abstract ou URL terminada em `.pdf` não bastam. A confirmação depende de conteúdo recebido, formato ou assinatura coerente, identidade, conteúdo técnico mínimo, hash e provenance. A aquisição patentária já foi demonstrada para publicações BR, US, WO/PCT e EP; uma rota publisher PDF também foi demonstrada para uma classe de paper open access. Essas afirmações são limitadas às rotas e amostras registradas nos checkpoints.

A entrega não tenta encerrar a investigação. A camada [Resultados em movimento](results/) mostra como uma trilha passa de corpus a sinal, documento, relação e próxima pergunta. O projeto cria uma base pública para perguntar **quem aparece**, **quais tecnologias se repetem**, **quais relações surgem**, **quais documentos podem ser verificados** e **onde a evidência ainda não existe**.

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
| **21/08/2026** | Início da Inteligência Documental: arquitetura de aquisição, validação documental, hashes e provenance preservada no Lux-Lab privado. |
| **22/08/2026** | Acquisition Probe internacional: Google Patents validado em publicações US, WO/PCT e EP; rota publisher PDF validada em paper OA. |
| **22/08/2026** | Primeira execução documental no corpus Agro: 175 patentes e 543 papers roteados, adquiridos quando possível e classificados por evidência. |
| Próximo marco | Reutilização do layer para uma nova execução controlada e, depois, extração técnica apenas sobre documentos que passarem o gate documental. |

A linha do tempo vai crescer junto com a investigação. O objetivo é preservar a arqueologia da descoberta, não apenas o resultado final.

## Status

**Modo exploratório ativo.** O laboratório já tem uma camada pública de ingestão, normalização, resolução conservadora de entidades, radiografia, descoberta orientada por consultas e registro sanitizado de aquisição documental. A execução privada atual adicionou validação de formato, identidade, conteúdo, hashes, status e provenance ao corpus Agro. A camada de extração técnica continua condicionada à disponibilidade e à qualidade documental; nenhuma inferência é liberada apenas porque existe metadata ou um link.

> Não estamos esperando as condições perfeitas para começar.

## Próximos passos

O ciclo agora é **corpus → descoberta → aquisição/roteamento → validação → evidência → pergunta**. A expansão já investigou a ponte brasileira entre fermentação, biorreatores, produção on-farm e bioinsumos; a trilha internacional de fixação/solubilização, formulação e estabilidade; o corredor Trichoderma–enzimas–bioprocessos; e o sinal Petrobras–microalgas–CO₂–fertilizante. A próxima etapa é aplicar o layer a execuções controladas, mantendo separados metadata, links, documentos adquiridos, conteúdo não comprovado e evidência técnica.

## Licença e uso

A licença dos componentes de software e dos artefatos públicos será definida conforme a natureza de cada material. Patentes, artigos, marcas e dados de terceiros continuam sujeitos aos direitos e termos de suas fontes originais.

Este repositório não oferece aconselhamento jurídico, técnico, científico ou de investimento. Ele registra uma investigação aberta e verificável.

---

**Constrói. Documenta. Mostra.**
