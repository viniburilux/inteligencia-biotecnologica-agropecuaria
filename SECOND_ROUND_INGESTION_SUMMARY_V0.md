# Segunda Rodada de Ingestão V0

**Data da execução:** 21/08/2026  
**Modo:** metadata-only  
**Ponto de partida:** Radiografia Exploratória V0 sobre o corpus congelado de 379 registros.

## O que foi executado

A segunda rodada seguiu os blocos definidos em [`SECOND_ROUND_PLAN_V0.json`](SECOND_ROUND_PLAN_V0.json). Foram executadas nove consultas patentárias no Google Patents, todas com filtro `country:BR`, e uma consulta bibliográfica de contraste no OpenAlex. Nenhum PDF de patente, texto integral, sequência, dado científico ou arquivo de pesquisa foi baixado.

| Bloco | Consultas | Fonte | Registros capturados |
|---|---|---|---:|
| B1 — Trichoderma transversal | `Trichoderma fermentation`; `Trichoderma biocontrol` | Google Patents [1] [2] | 20 |
| B2 — Plataforma de nitrogênio | `microbial nitrogen fixation formulation`; `phosphate solubilization microbial`; `nitrogen fixation microbial release` | Google Patents [3] [4] [5] | 23 |
| B3 — Produção local e qualidade | `bioinput bioreactor`; `bioinput fermentation`; `bioinput rural property production`; `bioinput quality monitoring spectrometry` | Google Patents [6] [7] [8] [9] | 33 |
| B3 — Contraste bibliográfico | `Brazilian bioinput fermentation agriculture` | OpenAlex [10] | 25 |

As consultas patentárias produziram **76 ocorrências capturadas** e **50 identificadores únicos entre consultas**. A consulta OpenAlex retornou **25 obras** de um universo observado de 140 resultados. Após a integração e deduplicação conservadora com o corpus anterior, o inventário passou a **429 obras e registros**, com 97 registros patentários, 1.499 atores, 381 instituições, 2.093 relações observadas e 313 sinais de aplicação.

## O que o segundo ciclo revelou

O primeiro sinal forte foi uma ponte de **Trichoderma** para processos industriais: a consulta de fermentação recuperou repetidamente vocabulário de enzimas, degradação de material celulósico, fermentação e etanol, com presença recorrente de Novozymes. Isso não deve ser tratado como prova de convergência tecnológica; é uma ponte observada que abriu uma trilha própria de bioprocessos industriais e bioenergia.

O segundo sinal foi uma plataforma internacional concentrada em **fixação de nitrogênio, solubilização de fosfato, remodelamento microbiano, formulação, estabilidade e liberação direcionada**. A repetição de famílias associadas à Pivot Bio indica concentração do resultado de busca, mas não demonstra capacidade brasileira. O filtro BR foi preservado apenas como contexto de presença patentária no país.

O terceiro sinal foi um núcleo brasileiro compacto envolvendo **biorreatores, fermentação asséptica, multiplicação de Trichoderma, controle físico-químico, produção on-farm e kits de biofertilizante**. As consultas `bioinput bioreactor`, `bioinput fermentation` e `bioinput rural property production` formaram a trilha local mais concreta desta rodada, com USP, Universidade do Estado da Bahia, GI Indústria, Dosaggio, Simple Agro Sistemas e outros atores visíveis nas páginas capturadas.

O quarto sinal, inesperado, surgiu em `bioinput quality monitoring spectrometry`: além do biorreator monitorado por termocromia e espectrometria, apareceu uma ligação com **biofixação de CO2, produção de biomassa de algas e Petrobras**. Esse sinal foi preservado como trilha exploratória de Clean Tech e resíduos industriais, sem ser reclassificado como parte do núcleo de bioinsumos agrícolas.

## Limites de leitura

Os registros patentários são metadados de páginas públicas e snippets de resultados. Um resultado com filtro BR não significa que inventor, depositante, prioridade ou origem tecnológica sejam brasileiros. A extração de atores é best-effort e não equivale a resolução de entidades. Registros capturados apenas no caderno, quando a página dinâmica não expôs a lista na captura textual, foram marcados com `source_kind: browser_html_finding`, título genérico e snippet explícito, sem completar campos ausentes.

A literatura OpenAlex foi usada como contraste de recuperação. A presença ou ausência de obras para a consulta não mede maturidade, eficácia agronômica, novidade jurídica ou potencial comercial.

## Artefatos do ciclo

| Artefato | Função |
|---|---|
| [`EXPLORATORY_RADIOGRAPHY_V0.md`](EXPLORATORY_RADIOGRAPHY_V0.md) | Radiografia congelada sobre os 379 registros originais. |
| [`next_queries_v0.json`](next_queries_v0.json) | Vinte consultas derivadas do corpus. |
| [`SECOND_ROUND_PLAN_V0.json`](SECOND_ROUND_PLAN_V0.json) | Seleção, ordem, execução e evidências dos blocos. |
| [`SECOND_ROUND_PATENT_FINDINGS_V0.md`](SECOND_ROUND_PATENT_FINDINGS_V0.md) | Caderno de achados patentários da segunda rodada. |
| [`second_round_patent_parser_summary_v0.json`](second_round_patent_parser_summary_v0.json) | Contagens e caminhos dos JSONL patentários. |
| [`second_round_openalex_summary_v0.json`](second_round_openalex_summary_v0.json) | Resumo da consulta bibliográfica de contraste. |
| [`normalized_v0/`](normalized_v0/) | Corpus integrado após normalização e deduplicação. |

## Próxima trilha

O próximo ciclo deve separar explicitamente três trilhas: a capacidade brasileira de produção local de bioinsumos; a plataforma internacional de microrganismos fixadores e solubilizadores; e a ponte Trichoderma–fermentação–bioprocessos industriais. A própria coleta já mostrou que essas trilhas compartilham vocabulário, mas não devem ser colapsadas antes de uma nova camada de evidência.

## Referências

[1]: https://patents.google.com/?q=(Trichoderma+fermentation)&country=BR "Google Patents — Trichoderma fermentation + BR"
[2]: https://patents.google.com/?q=(Trichoderma+biocontrol)&country=BR "Google Patents — Trichoderma biocontrol + BR"
[3]: https://patents.google.com/?q=(microbial+nitrogen+fixation+formulation)&country=BR "Google Patents — microbial nitrogen fixation formulation + BR"
[4]: https://patents.google.com/?q=(phosphate+solubilization+microbial)&country=BR "Google Patents — phosphate solubilization microbial + BR"
[5]: https://patents.google.com/?q=(nitrogen+fixation+microbial+release)&country=BR "Google Patents — nitrogen fixation microbial release + BR"
[6]: https://patents.google.com/?q=(bioinput+bioreactor)&country=BR "Google Patents — bioinput bioreactor + BR"
[7]: https://patents.google.com/?q=(bioinput+fermentation)&country=BR "Google Patents — bioinput fermentation + BR"
[8]: https://patents.google.com/?q=(bioinput+rural+property+production)&country=BR "Google Patents — bioinput rural property production + BR"
[9]: https://patents.google.com/?q=(bioinput+quality+monitoring+spectrometry)&country=BR "Google Patents — bioinput quality monitoring spectrometry + BR"
[10]: https://api.openalex.org/works?search=Brazilian%20bioinput%20fermentation%20agriculture&filter=from_publication_date:2010-01-01,to_publication_date:2026-12-31&per-page=25 "OpenAlex — Brazilian bioinput fermentation agriculture"
