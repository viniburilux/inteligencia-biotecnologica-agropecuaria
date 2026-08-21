# Mapa de Sinais V0

**Laboratório:** Inteligência Biotecnológica Agropecuária  
**Gerado em:** 2026-08-21T04:50:32.918823+00:00  
**Modo:** metadata-only

O Mapa de Sinais V0 é uma leitura computável do primeiro corpus integrado. Ele combina literatura capturada via OpenAlex e Crossref com registros patentários capturados da página pública do Google Patents. Os números abaixo descrevem o que foi ingerido e normalizado; não são estimativas de mercado, validade jurídica, eficácia agronômica ou origem nacional.

## Composição do corpus

| Fonte | Obras/registros | Participação |
| --- | --- | --- |
| openalex | 162 | 42.7% |
| crossref | 146 | 38.5% |
| google_patents | 71 | 18.7% |

O corpus contém **379 obras/registros**, **1345 atores**, **353 instituições**, **1854 relações observadas** e **270 sinais de aplicação**.

## Consultas patentárias

A tabela separa o volume total observado na página de resultados (`observed_result_count`), os registros metadata-only capturados na primeira página (`returned_items`) e o número de registros únicos que chegaram ao inventário normalizado. Um mesmo documento pode aparecer em mais de uma consulta, por isso os totais por consulta não devem ser somados como documentos distintos.

| Consulta | Resultados totais observados | Registros capturados | Registros únicos no inventário | Arquivo bruto |
| --- | --- | --- | --- | --- |
| bioinsumo + BR | 50 | 9 | 9 | raw_v0/google_patents/bioinsumo_br.jsonl |
| biocontrole + BR | 1186 | 7 | 7 | raw_v0/google_patents/biocontrole_br.jsonl |
| inoculante + BR | 889 | 7 | 7 | raw_v0/google_patents/inoculante_br.jsonl |
| biopesticida + BR | 6712 | 7 | 7 | raw_v0/google_patents/biopesticida_br.jsonl |
| biofertilizante + BR | 6633 | 7 | 7 | raw_v0/google_patents/biofertilizante_br.jsonl |
| Rhizobium + BR | 3402 | 9 | 9 | raw_v0/google_patents/rhizobium_br.jsonl |
| Bacillus thuringiensis + BR | 14887 | 7 | 7 | raw_v0/google_patents/bacillus_thuringiensis_br.jsonl |
| Trichoderma + BR | 6524 | 10 | 10 | raw_v0/google_patents/trichoderma_br.jsonl |
| fixação de nitrogênio + BR | 8956 | 7 | 7 | raw_v0/google_patents/fixa_o_de_nitrog_nio_br.jsonl |
| biological control + BR | 56223 | 7 | 7 | raw_v0/google_patents/biological_control_br.jsonl |
| bioinput + BR | 49 | 9 | 9 | raw_v0/google_patents/bioinput_br.jsonl |
| microbial inoculant + BR | 4975 | 10 | 10 | raw_v0/google_patents/microbial_inoculant_br.jsonl |

## Eixos tecnológicos observados

| Sinal de aplicação | Ocorrências | Distribuição por fonte |
| --- | --- | --- |
| biocontrole | 78 | crossref: 38, openalex: 34, google_patents: 6 |
| bioinsumo | 52 | crossref: 23, openalex: 21, google_patents: 8 |
| fungo | 52 | openalex: 21, google_patents: 16, crossref: 15 |
| biopesticida | 45 | crossref: 25, openalex: 18, google_patents: 2 |
| inoculante | 40 | openalex: 21, crossref: 11, google_patents: 8 |
| promocao_crescimento | 38 | crossref: 27, openalex: 11 |
| nematoide | 14 | crossref: 9, openalex: 5 |
| biofertilizante | 13 | openalex: 6, google_patents: 6, crossref: 1 |
| soja | 11 | openalex: 8, crossref: 3 |
| milho | 8 | openalex: 6, crossref: 2 |
| fixacao_nitrogenio | 5 | google_patents: 4, openalex: 1 |
| monitoramento_qualidade | 5 | google_patents: 5 |
| solubilizacao_fosfato | 4 | google_patents: 3, openalex: 1 |
| saude_radicular | 4 | google_patents: 3, crossref: 1 |
| fermentacao_bioprocesso | 4 | google_patents: 4 |
| sequestro_carbono | 2 | google_patents: 2 |

Os sinais são derivados de termos encontrados em títulos, assuntos ou snippets capturados. Eles funcionam como ponte para exploração posterior, não como classificação definitiva de tecnologia.

## Atores mais conectados

| Ator | Relações observadas | Papéis | Fonte do registro |
| --- | --- | --- | --- |
| Pivot Bio | 6 | assignee | google_patents |
| Fernando Ferrari Putti | 3 |  | openalex |
| Mariangela Hungría | 3 |  | openalex |
| L. S. AMARAL | 3 |  | crossref |
| E. O. ARAÚJO | 3 |  | crossref |
| Frederico Keller | 3 | inventor, assignee | google_patents |
| Syngenta | 3 | assignee | google_patents |
| Sean Farmer | 3 | inventor | google_patents |
| Alvin Tamsir | 3 | inventor | google_patents |
| João Pedro dos Santos | 2 |  | openalex |
| Ana Laura Paula de Oliveira | 2 |  | openalex |
| Leonardo Elias Ferreira | 2 |  | openalex |
| Eliziete Pereira de Souza | 2 |  | openalex |
| Mariane Carvalho Vidal | 2 |  | openalex |
| Ruth Rebeca Bonilla Buitrago | 2 |  | openalex |

## Instituições mais conectadas

| Instituição | Relações observadas | Fonte do registro |
| --- | --- | --- |
| Brazilian Agricultural Research Corporation | 14 | openalex |
| Universidade de São Paulo | 7 | openalex |
| Pivot Bio | 6 | google_patents |
| Universidade Estadual Paulista (Unesp) | 4 | openalex |
| Universidade Estadual de Londrina | 4 | openalex |
| Ministério da Agricultura | 3 | openalex |
| Universidade Federal de Viçosa | 3 | openalex |
| Universidade Federal da Grande Dourados | 3 | openalex |
| North-West University | 3 | openalex |
| University of Nairobi | 3 | openalex |
| Centre National de la Recherche Scientifique | 3 | openalex |
| Syngenta | 3 | google_patents |
| Horta (Italy) | 2 | openalex |
| Instituto Tecnológico de Costa Rica | 2 | openalex |
| Colombian Corporation for Agricultural Research - AGROSAVIA | 2 | openalex |

## Distribuição temporal

### crossref

| Ano | Registros |
| --- | --- |
| 2010 | 2 |
| 2011 | 6 |
| 2012 | 5 |
| 2013 | 2 |
| 2014 | 1 |
| 2015 | 2 |
| 2016 | 3 |
| 2017 | 7 |
| 2018 | 5 |
| 2019 | 8 |
| 2020 | 5 |
| 2021 | 24 |
| 2022 | 15 |
| 2023 | 8 |
| 2024 | 16 |
| 2025 | 22 |
| 2026 | 15 |

### google_patents

| Ano | Registros |
| --- | --- |
| 2020 | 3 |
| 2021 | 8 |
| 2022 | 5 |
| 2023 | 1 |
| 2024 | 2 |
| 2026 | 1 |

### openalex

| Ano | Registros |
| --- | --- |
| 2010 | 5 |
| 2011 | 6 |
| 2012 | 9 |
| 2013 | 4 |
| 2014 | 9 |
| 2015 | 13 |
| 2016 | 5 |
| 2017 | 15 |
| 2018 | 12 |
| 2019 | 10 |
| 2020 | 17 |
| 2021 | 16 |
| 2022 | 11 |
| 2023 | 13 |
| 2024 | 11 |
| 2025 | 4 |
| 2026 | 2 |

## Leitura operacional

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

[1]: https://patents.google.com/?q=(bioinsumo)&country=BR — Google Patents, consulta `bioinsumo + BR`.
[2]: https://patents.google.com/?q=(biocontrole)&country=BR — Google Patents, consulta `biocontrole + BR`.
[3]: https://patents.google.com/?q=(inoculante)&country=BR — Google Patents, consulta `inoculante + BR`.
[4]: https://patents.google.com/?q=(biopesticida)&country=BR — Google Patents, consulta `biopesticida + BR`.
[5]: https://patents.google.com/?q=(biofertilizante)&country=BR — Google Patents, consulta `biofertilizante + BR`.
[6]: https://patents.google.com/?q=(Rhizobium)&country=BR — Google Patents, consulta `Rhizobium + BR`.
[7]: https://patents.google.com/?q=(Bacillus+thuringiensis)&country=BR — Google Patents, consulta `Bacillus thuringiensis + BR`.
[8]: https://patents.google.com/?q=(Trichoderma)&country=BR — Google Patents, consulta `Trichoderma + BR`.
[9]: https://patents.google.com/?q=(fixa%C3%A7%C3%A3o+de+nitrog%C3%AAnio)&country=BR — Google Patents, consulta `fixação de nitrogênio + BR`.
[10]: https://patents.google.com/?q=(biological+control)&country=BR — Google Patents, consulta `biological control + BR`.
[11]: https://patents.google.com/?q=(bioinput)&country=BR — Google Patents, consulta `bioinput + BR`.
[12]: https://patents.google.com/?q=(microbial+inoculant)&country=BR — Google Patents, consulta `microbial inoculant + BR`.
