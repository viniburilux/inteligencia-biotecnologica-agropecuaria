# Exploration Cycle V1

## O ciclo executado

Este ciclo partiu do corpus cumulativo de **763 obras metadata-only** e seguiu relações observadas em atores, organismos, tecnologias, instituições e lacunas. A execução preservou o ciclo operacional:

> **corpus → radiografia → pergunta → ingestão → nova radiografia**

A base cumulativa usada no fechamento contém 422 registros OpenAlex, 146 Crossref e 195 registros patentários capturados em resultados públicos do Google Patents. O corpus final preserva hashes, consultas, estados de captura e lote de proveniência. Não foram baixados PDFs de patentes, textos integrais ou dados científicos.

| Camada | Resultado do ciclo |
|---|---:|
| Obras cumulativas | **763** |
| Atores normalizados | **2.680** |
| Instituições normalizadas | **767** |
| Relações observadas | **4.045** |
| Sinais de aplicação | **536** |
| Queries derivadas da Radiografia V1 | **17** |
| Queries executadas | **17** |
| Reformulações que abriram resultados | **3** |
| Registros patentários capturados na Radiografia V1 | **36** entre consultas; **30 únicos** |
| Obras OpenAlex capturadas no contraste V1 | **50** |

## O que apareceu quando seguimos os dados

### A cadeia brasileira ganhou materialidade de processo

A trilha **biorreator → fermentação → produção na propriedade → controle de parâmetros → bioinsumo** deixou de ser apenas uma associação de termos. A expansão encontrou famílias e atores recorrentes em USP, Embrapa, Simple Agro e Solubio, incluindo biorreatores, formulações microbianas, controle de parâmetros, multiplicação a campo e produção rural. Isso é evidência de uma cadeia tecnológica representada por registros distintos; ainda não é prova de que todos formem uma única plataforma ou de que tenham adoção comercial comparável.

A busca nominal inicial Embrapa–Bacillus velezensis falhou. A reformulação por `CMRP 4490` e biorreator abriu um registro. A busca Solubio em inglês também foi insuficiente; a reformulação em português com **bioinsumo, fermentação, produção e propriedade rural** abriu uma família. O laboratório encontrou valor ao reformular queries mortas pela linguagem visível nos próprios registros.

### A trilha internacional se comportou como portfólio tecnológico

**Pivot Bio** reapareceu em fixação de nitrogênio, solubilização de fosfato, remodelamento microbiano, formulação polimérica, estabilidade e liberação. **Locus** apareceu na interseção entre fósforo, fitase, enzimas, matéria orgânica e agricultura microbiana, mas com maior ruído de recuperação. O sinal mais forte é a coerência interna dos temas associados a Pivot Bio; a existência de várias famílias relacionadas não prova desempenho agronômico, exclusividade ou liberdade de operação.

### Trichoderma atravessou mais contextos do que o esperado

`Trichoderma` foi o organismo mais recorrente do corpus, com **175 obras** na radiografia. Ele apareceu em biocontrole, soforolipídeos, fermentação, celulase, enzimas, etanol e biorreatores. A busca nominal USP–*Trichoderma harzianum*–soforolipídeo confirmou a ponte com **Starmerella bombicola** e biossurfactantes. O corredor industrial também trouxe **Novozymes**, *Trichoderma reesei*, celulase, biomassa e produção enzimática.

O achado operacional não é que exista uma “tecnologia Trichoderma” única. É que o organismo funciona como uma **ponte de navegação** entre bioinsumos agrícolas e bioprocessos industriais, permitindo que novas queries sejam construídas a partir de aplicações e processos, não só do nome do organismo.

### A trilha Petrobras–microalgas sobreviveu à tentativa de expansão

A consulta ampla por microalgas, resíduos industriais e biofertilizante ficou insuficiente. A reformulação com termos observados em português — **microalga, cascalho de perfuração, biofixação e fertilizante** — confirmou uma família ligada a biomassa algal e fertilizante organomineral. A trilha segue estreita: há uma relação patentária recuperada, mas ainda não há base para tratá-la como corredor industrial amplo ou solução agrícola validada.

O valor desta trilha está justamente no comportamento: ela não foi descartada quando a formulação ampla morreu, mas também não foi inflada além do que os registros suportam.

## Relações e entidades que ganharam prioridade

| Elemento | Evidência no corpus | Próxima leitura operacional |
|---|---|---|
| USP | Trichoderma, soforolipídeos, biossurfactantes e formulações | Separar pesquisa de processo, composição e aplicação. |
| Embrapa | Bacillus, biorreatores, inoculantes e formulações | Resolver famílias e espécies por identificador, não apenas por nome institucional. |
| Simple Agro | Controle de qualidade, bioinsumos e sistemas on-farm | Testar continuidade entre equipamento, processo e aplicação. |
| Solubio | Produção e multiplicação de bioinsumos na propriedade | Cruzar patentes, literatura e fontes regulatórias de uso. |
| Pivot Bio | Nitrogênio, fósforo, polímero, estabilidade e liberação | Expandir famílias e separar portfólio de empresa de coocorrência temática. |
| Locus | Fitase, fósforo, enzimas e matéria orgânica | Reformular consultas estreitas para reduzir ruído. |
| Novozymes | Trichoderma, enzimas, celulase e fermentação | Seguir o corredor industrial sem presumir ligação agrícola direta. |
| Petrobras | Microalgas, CO₂, cascalho de perfuração e fertilizante | Buscar aplicação, escala e instituições conectadas. |

## O que morreu, o que foi reformulado e o que abriu

| Estado | Exemplos | O que o laboratório fez |
|---|---|---|
| Query insuficiente | Embrapa + Bacillus velezensis + biorreator; Solubio em inglês; microalgas + resíduos industriais em inglês | Preservou o estado e reformulou com IDs, termos em português ou componentes observados. |
| Query densa | Rhizobium + polímero + shelf life; Bacillus megaterium + fósforo; Novozymes + Trichoderma + celulase | Capturou famílias e atores para nova expansão. |
| Query ruidosa | Locus + fitase + fósforo + agricultura | Manteve o resultado como corredor amplo e não o transformou em conclusão. |
| Ponte inesperada | Petrobras + microalgas + cascalho de perfuração + fertilizante | Seguiu a relação até a família específica e preservou a trilha como estreita. |

## Artefatos produzidos

| Artefato | Função |
|---|---|
| [`EXPLORATORY_RADIOGRAPHY_V1.md`](EXPLORATORY_RADIOGRAPHY_V1.md) | Nova radiografia sobre o corpus cumulativo. |
| [`cluster_memberships_v1.jsonl`](cluster_memberships_v1.jsonl) | Liga obras, sinais e trilhas operacionais. |
| [`RADIOGRAPHY_METHOD_V1.md`](RADIOGRAPHY_METHOD_V1.md) | Regras de leitura e limites do ciclo. |
| [`next_queries_v1.json`](next_queries_v1.json) | Perguntas derivadas do corpus e executadas nesta rodada. |
| [`RADIOGRAPHY_V1_QUERY_EXECUTION.json`](RADIOGRAPHY_V1_QUERY_EXECUTION.json) | Estado computável de execução das 17 queries. |
| [`RADIOGRAPHY_V1_EXECUTION_SUMMARY.md`](RADIOGRAPHY_V1_EXECUTION_SUMMARY.md) | Resumo legível das queries diretas e reformuladas. |
| [`ENTITY_RESOLUTION_V1.json`](ENTITY_RESOLUTION_V1.json) | Aliases seguros, grupos candidatos e nomes não fundidos. |
| [`REGULATORY_APPLICATION_SOURCES_V1.md`](REGULATORY_APPLICATION_SOURCES_V1.md) | Fontes oficiais do MAPA e contexto regulatório/aplicado. |
| [`normalized_v2/`](normalized_v2/) | Corpus cumulativo deduplicado com proveniência por lote. |

## Referências

[1]: https://patents.google.com/ — Google Patents, fonte de descoberta patentária metadata-only.

[2]: https://api.openalex.org/ — OpenAlex API, fonte de descoberta bibliográfica metadata-only.

[3]: https://www.gov.br/agricultura/pt-br/assuntos/inovacao/bioinsumos — Ministério da Agricultura e Pecuária, fontes oficiais sobre bioinsumos e contexto de aplicação.

[4]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria — Repositório público do laboratório e artefatos reproduzíveis.
