# Mapa de Sinais V0

**Laboratório:** Inteligência Biotecnológica Agropecuária
**Gerado em:** 2026-08-21T05:14:24.820330+00:00
**Modo:** metadata-only

O Mapa de Sinais V0 é uma leitura computável do primeiro corpus integrado. Ele combina literatura capturada via OpenAlex e Crossref com registros patentários capturados da página pública do Google Patents. Os números abaixo descrevem o que foi ingerido e normalizado; não são estimativas de mercado, validade jurídica, eficácia agronômica ou origem nacional.

## Composição do corpus

| Fonte | Obras/registros | Participação |
| --- | --- | --- |
| openalex | 186 | 43.4% |
| crossref | 146 | 34.0% |
| google_patents | 97 | 22.6% |

O corpus contém **429 obras/registros**, **1499 atores**, **381 instituições**, **2093 relações observadas** e **313 sinais de aplicação**.

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
| Trichoderma fermentation | 1907 | 10 | 10 | raw_v0/google_patents/second_round_nq01_trichoderma_fermentation.jsonl |
| Trichoderma biocontrol | 446 | 10 | 10 | raw_v0/google_patents/second_round_nq02_trichoderma_biocontrol.jsonl |
| microbial nitrogen fixation formulation | 3415 | 7 | 7 | raw_v0/google_patents/second_round_nq04_microbial_nitrogen_fixation_formulation.jsonl |
| phosphate solubilization microbial | 12970 | 6 | 6 | raw_v0/google_patents/second_round_nq06_phosphate_solubilization_microbial.jsonl |
| nitrogen fixation microbial release | 2791 | 10 | 10 | raw_v0/google_patents/second_round_nq05_nitrogen_fixation_microbial_release.jsonl |
| bioinput bioreactor | 13 | 10 | 10 | raw_v0/google_patents/second_round_nq07_bioinput_bioreactor.jsonl |
| bioinput fermentation | 19 | 9 | 9 | raw_v0/google_patents/second_round_nq08_bioinput_fermentation.jsonl |
| bioinput rural property production | 34 | 9 | 9 | raw_v0/google_patents/second_round_nq10_bioinput_rural_property_production.jsonl |
| bioinput quality monitoring spectrometry | 5 | 5 | 5 | raw_v0/google_patents/second_round_nq09_bioinput_quality_monitoring_spectrometry.jsonl |

## Eixos tecnológicos observados

| Sinal de aplicação | Ocorrências | Distribuição por fonte |
| --- | --- | --- |
| biocontrole | 80 | crossref: 38, openalex: 34, google_patents: 8 |
| fungo | 72 | google_patents: 31, openalex: 26, crossref: 15 |
| bioinsumo | 62 | openalex: 27, crossref: 23, google_patents: 12 |
| biopesticida | 47 | crossref: 25, openalex: 19, google_patents: 3 |
| inoculante | 42 | openalex: 23, crossref: 11, google_patents: 8 |
| promocao_crescimento | 39 | crossref: 27, openalex: 12 |
| fermentacao_bioprocesso | 18 | google_patents: 14, openalex: 4 |
| nematoide | 15 | crossref: 9, openalex: 5, google_patents: 1 |
| biofertilizante | 15 | google_patents: 8, openalex: 6, crossref: 1 |
| fixacao_nitrogenio | 15 | google_patents: 14, openalex: 1 |
| soja | 12 | openalex: 9, crossref: 3 |
| solubilizacao_fosfato | 10 | google_patents: 9, openalex: 1 |
| saude_radicular | 10 | google_patents: 9, crossref: 1 |
| milho | 9 | openalex: 6, crossref: 2, google_patents: 1 |
| monitoramento_qualidade | 5 | google_patents: 5 |
| sequestro_carbono | 2 | google_patents: 2 |

Os sinais são derivados de termos encontrados em títulos, assuntos ou snippets capturados. Eles funcionam como ponte para exploração posterior, não como classificação definitiva de tecnologia.

## Atores mais conectados

| Ator | Relações observadas | Papéis | Fonte do registro |
| --- | --- | --- | --- |
| Pivot Bio | 6 | assignee | google_patents |
| Mariangela Hungría | 4 |  | openalex |
| Fernando Ferrari Putti | 3 |  | openalex |
| Marco Antônio Nogueira | 3 |  | openalex |
| Gabriel Moura Mascarin | 3 |  | openalex |
| L. S. AMARAL | 3 |  | crossref |
| E. O. ARAÚJO | 3 |  | crossref |
| Frederico Keller | 3 | inventor, assignee | google_patents |
| Syngenta | 3 | assignee | google_patents |
| Sean Farmer | 3 | inventor | google_patents |
| Alvin Tamsir | 3 | inventor | google_patents |
| Sarah BLOCH Pivot Bio, Inc | 3 | inventor | google_patents |
| Alvin Tamsir Pivot Bio, Inc | 3 | inventor | google_patents |
| João Pedro dos Santos | 2 |  | openalex |
| Ana Laura Paula de Oliveira | 2 |  | openalex |

## Instituições mais conectadas

| Instituição | Relações observadas | Fonte do registro |
| --- | --- | --- |
| Brazilian Agricultural Research Corporation | 22 | openalex |
| Universidade de São Paulo | 8 | openalex |
| Universidade Estadual de Londrina | 6 | openalex |
| Pivot Bio | 6 | google_patents |
| Universidade Federal de Santa Maria | 5 | openalex |
| Universidade Estadual Paulista (Unesp) | 4 | openalex |
| Universidade de Brasília | 4 | openalex |
| Ministério da Agricultura | 3 | openalex |
| Universidade Federal Rural do Rio de Janeiro | 3 | openalex |
| Instituto Biológico | 3 | openalex |
| Universidade Federal de Viçosa | 3 | openalex |
| Universidade Federal de Santa Catarina | 3 | openalex |
| Instituto Federal Goiano | 3 | openalex |
| Universidade Federal da Grande Dourados | 3 | openalex |
| Universidade Federal Rural de Pernambuco | 3 | openalex |

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
| 2019 | 1 |
| 2020 | 8 |
| 2021 | 15 |
| 2022 | 9 |
| 2023 | 4 |
| 2024 | 3 |
| 2025 | 3 |
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
| 2021 | 20 |
| 2022 | 11 |
| 2023 | 17 |
| 2024 | 15 |
| 2025 | 14 |
| 2026 | 4 |

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
[13]: https://patents.google.com/?q=(Trichoderma+fermentation)&country=BR — Google Patents, consulta `Trichoderma fermentation`.
[14]: https://patents.google.com/?q=(Trichoderma+biocontrol)&country=BR — Google Patents, consulta `Trichoderma biocontrol`.
[15]: https://patents.google.com/?q=(microbial+nitrogen+fixation+formulation)&country=BR — Google Patents, consulta `microbial nitrogen fixation formulation`.
[16]: https://patents.google.com/?q=(phosphate+solubilization+microbial)&country=BR — Google Patents, consulta `phosphate solubilization microbial`.
[17]: https://patents.google.com/?q=(nitrogen+fixation+microbial+release)&country=BR — Google Patents, consulta `nitrogen fixation microbial release`.
[18]: https://patents.google.com/?q=(bioinput+bioreactor)&country=BR — Google Patents, consulta `bioinput bioreactor`.
[19]: https://patents.google.com/?q=(bioinput+fermentation)&country=BR — Google Patents, consulta `bioinput fermentation`.
[20]: https://patents.google.com/?q=(bioinput+rural+property+production)&country=BR — Google Patents, consulta `bioinput rural property production`.
[21]: https://patents.google.com/?q=(bioinput+quality+monitoring+spectrometry)&country=BR — Google Patents, consulta `bioinput quality monitoring spectrometry`.
