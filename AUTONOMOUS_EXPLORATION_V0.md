# AUTONOMOUS_EXPLORATION_V0

**Data:** 2026-08-21T07:13:02.962274+00:00  
**Baseline:** 763 obras metadata-only, congeladas durante o teste.  
**Regra:** nenhuma trilha foi escolhida por instrução do usuário; as perguntas foram geradas a partir do estado computável, dos sinais, das lacunas e do histórico de resultados.

## Pergunta do experimento

> A partir do estado atual do laboratório, a exploração autônoma consegue escolher perguntas, abrir trilhas, reformular consultas mortas, seguir pontes inesperadas e abandonar direções que não ganham evidência?

O objetivo não foi provar que o ASIE funciona. Foi observar se o comportamento adaptativo encontra caminhos que não seriam produzidos por repetição mecânica das queries anteriores.

## Estado usado para decidir

| Elemento | Valor observado |
|---|---:|
| Obras | 763 |
| Atores normalizados | 2.680 |
| Instituições | 767 |
| Relações | 4.045 |
| Sinais de aplicação | 536 |
| Sinais de maior frequência | fungo 186; biocontrole 94; fermentação/bioprocesso 89; inoculante 73; bioinsumo 70 |
| Coocorrência escolhida | fungo–nematoide 23; fungo–soja 9; fixação de nitrogênio–saúde radicular 9; fungo–solubilização de fosfato 7 |

## Trilhas escolhidas sem confirmação do usuário

O analisador abriu quatro ramos. O primeiro veio de fungo–nematoide–soja; o segundo de fixação de nitrogênio–saúde radicular–milho; o terceiro de fungo–solubilização de fosfato–saúde radicular; o quarto preservou o corredor carbono/alga como teste de baixa densidade e alto valor surpresa.

### Ramo A — fungo, nematoide e soja

A consulta patentária em inglês retornou 465 resultados com ruído. O próprio histórico do laboratório já mostrava que a linguagem podia ser decisiva, então a pergunta foi reformulada em português. A reformulação caiu para 32 resultados e expôs `BR112019020483A2`, associado à Advanced Biological Marketing, com combinações de Trichoderma e Bacillus e aplicações de controle de nematoides, colonização radicular e tratamento de sementes/foliar na descrição visível.

A máquina então mudou de busca lexical para inspeção de família. Em paralelo, a consulta OpenAlex ampla retornou 3.550 obras. Um título direto sobre *Trichoderma citrinoviride* e *Meloidogyne incognita* virou a próxima pergunta. A reformulação específica retornou 95 obras, com o estudo direto na primeira posição. Quando a mesma combinação foi levada ao Google Patents com filtro BR, o resultado foi **nenhum resultado**.

| Estado final do ramo | Decisão |
|---|---|
| Literatura específica sustentada; corredor patentário BR não confirmado nessa formulação | **Aprofundar literatura; estacionar a afirmação patentária brasileira** |

O que apareceu aqui e não estava na busca fixa original foi o par espécie–patógeno e o uso de um identificador de família como próximo passo. O que não apareceu foi uma confirmação brasileira específica, e isso foi preservado como bloqueio.

### Ramo B — fixação de nitrogênio, saúde radicular e milho

A busca OpenAlex inicial retornou 13.618 obras, dominadas por literatura geral de rizosfera. O sistema não aceitou o volume como evidência suficiente. A pergunta foi reformulada para PGPR, fixação de nitrogênio, milho e condição de casa de vegetação. A consulta ainda retornou 6.737 obras, mas trouxe um estudo direto sobre inoculação de milho, fixação de nitrogênio e remobilização de nitrogênio, além de um corredor bibliográfico estável sobre PGPR e comercialização de bioestimulantes.

A busca patentária independente abriu uma família visível, `BR112020022643A2`, associada à Locus Agriculture IP Company, sobre produtos microbianos para saúde e imunidade radicular. A decisão foi manter Locus separado de Pivot Bio. O ramo não foi abandonado; foi rebaixado de “plataforma” para “corredor de literatura + contraste de ator”.

| Estado final do ramo | Decisão |
|---|---|
| Sinal bibliográfico forte, mas amplo; uma âncora patentária de ator | **Manter como background e estreitar por organismo/cultura em ciclo posterior** |

### Ramo C — Trichoderma, fosfato e saúde radicular

A coocorrência fungo–solubilização de fosfato e saúde radicular não estava entre as quatro trilhas históricas fechadas. A consulta patentária retornou 384 resultados e revelou que a ponte atravessava famílias da Locus sobre saúde radicular, leveduras/rizosfera e carbono, além de uma família Pivot Bio sobre solubilização de fosfato.

A interpretação operacional foi deliberadamente não colapsar a ponte. O resultado diz “há uma arquitetura de portfólios e temas que se cruzam”; não diz “há uma tecnologia Trichoderma comum a Locus e Pivot”.

| Estado final do ramo | Decisão |
|---|---|
| Ponte de portfólio observada; organismo não isolado | **Aprofundar por ator, mantendo Locus e Pivot separados** |

### Ramo D — microalgas, resíduos de perfuração e fertilizante

O ramo de carbono foi mantido porque era inesperado e estreito. A consulta OpenAlex inicial retornou apenas 18 obras, principalmente sobre captura de CO₂ por algas e CCUS. A reformulação para `algae drilling cuttings fertilizer Brazil` retornou 227 obras, mas os títulos de topo se concentraram em tratamento de água produzida, reaproveitamento de cascalho para construção e tópicos genéricos de energia/água. Não apareceu no topo uma cadeia direta algas–cascalho–fertilizante–Brasil.

| Estado final do ramo | Decisão |
|---|---|
| Ponte patentária específica; literatura independente não adicionou a cadeia esperada | **Estacionar** |

A trilha não foi apagada. Ela aguarda uma nova âncora institucional, de resíduo ou de aplicação antes de consumir mais consultas.

## Registro das execuções autônomas

| Sequência | Pergunta/ação | Fonte | Resultado | Decisão |
|---|---|---|---|---|
| A1 | fungal biocontrol nematode soybean | Google Patents BR | 465 resultados, muito ruído | Reformular |
| A1R | fungo biocontrole nematoide soja | Google Patents BR | 32 resultados; família BR112019020483A2 | Inspecionar família |
| A1F | BR112019020483A2 | Google Patents | Atores, organismos, uso e formulação visíveis | Aprofundar |
| A2 | microbial nitrogen fixation root health maize | Google Patents BR | Família Locus BR112020022643A2 | Manter independente |
| A3 | Trichoderma phosphate solubilization root health | Google Patents BR | 384; Locus e Pivot separados | Contrastar portfólios |
| A01 | Trichoderma nematode root health soybean | OpenAlex | 3.550 obras | Reformular |
| A01R | T. citrinoviride M. incognita | OpenAlex | 95 obras; estudo direto no topo | Aprofundar literatura |
| A01P | T. citrinoviride M. incognita Brazil | Google Patents BR | Nenhum resultado | Estacionar ramo BR |
| A02 | microbial nitrogen fixation root health maize rhizosphere | OpenAlex | 13.618 obras, genérico | Reformular |
| A02R | PGPR nitrogen fixation maize greenhouse | OpenAlex | 6.737; estudo direto e corredor PGPR | Estreitar depois |
| A03 | fungal biocontrol nematode plant root colonization | OpenAlex | 8.842; mistura PGPR/Bacillus/AMF/Trichoderma | Reformular |
| A03R | Trichoderma root knot nematode biocontrol | OpenAlex | 3.763; títulos diretos e coerentes | Aprofundar |
| A04 | microalgae drilling waste biofixation fertilizer | OpenAlex | 18; literatura CCUS genérica | Reformular |
| A04R | algae drilling cuttings fertilizer Brazil | OpenAlex | 227; sem cadeia direta no topo | Estacionar |
| A5 | espécie/pathógeno específico no BR | Google Patents BR | Ausência observada | Preservar bloqueio |

## O que a autonomia realmente encontrou

Há três resultados fortes. Primeiro, **reparo por linguagem**: a busca portuguesa abriu uma família que a busca inglesa não isolou. Segundo, **reparo por entidade**: um título bibliográfico abriu a pergunta espécie–patógeno, e um resultado patentário abriu a inspeção por identificador. Terceiro, **separação de portfólios**: a ponte Trichoderma–fosfato–saúde radicular levou a Locus e Pivot, mas o processo manteve os atores separados.

Há também dois resultados negativos importantes. A consulta específica da espécie/pathógeno não encontrou uma família BR nessa formulação. E a reformulação bibliográfica do corredor carbono não encontrou a cadeia direta esperada. Esses bloqueios são parte do resultado do teste; sem eles, a autonomia seria apenas expansão de narrativa.

## Julgamento do experimento

O comportamento observado é **promissor como processo de exploração**, porque a próxima pergunta mudou com base no resultado anterior e porque diferentes ramos terminaram em decisões diferentes. A evidência é **insuficiente para afirmar vantagem mensurável sobre estratégia fixa**, pois este V0 não executou uma condição-controle com o mesmo orçamento, nem mediu tempo, falsos candidatos, recall, retrabalho ou completude de provenance em comparação direta.

A conclusão operacional é clara: **não construir o ASIE ainda**. O próximo experimento informativo é um teste A/B de estratégia fixa contra estratégia adaptativa, usando o mesmo snapshot de 763 obras, o mesmo orçamento de fontes e o mesmo formato de log. O ASIE só deve virar módulo depois de sabermos se as decisões adaptativas reduzem consultas inúteis, aumentam caminhos novos ou melhoram o tempo até uma próxima ação justificável.

## Proveniência e artefatos

O registro computável completo está em [`ASIE_CYCLE_LOG_V0.jsonl`](ASIE_CYCLE_LOG_V0.jsonl). O estado usado para seleção está em [`asie_autonomy_state_v0.json`](asie_autonomy_state_v0.json). As capturas patentárias estão em [`asie_autonomous_browser_findings_v0.md`](asie_autonomous_browser_findings_v0.md). As respostas OpenAlex estão em [`asie_autonomous_openalex_findings_v0.md`](asie_autonomous_openalex_findings_v0.md) e [`asie_autonomous_openalex_reformulations_findings_v0.md`](asie_autonomous_openalex_reformulations_findings_v0.md). Os resultados brutos autônomos permanecem sob `raw_v3/asie_autonomous/`.

## Referências

[1]: https://patents.google.com/patent/BR112019020483A2/en "Google Patents — BR112019020483A2"

[2]: https://patents.google.com/patent/BR112020022643A2/en "Google Patents — BR112020022643A2"

[3]: https://patents.google.com/?q=(fungo+biocontrole+nematoide+soja)&country=BR "Google Patents — busca em português"

[4]: https://api.openalex.org/works?search=Trichoderma%20citrinoviride%20Meloidogyne%20incognita "OpenAlex — espécie/pathógeno"

[5]: https://api.openalex.org/works?search=plant%20growth%20promoting%20rhizobacteria%20nitrogen%20fixation%20maize%20greenhouse "OpenAlex — PGPR/milho"

[6]: https://api.openalex.org/works?search=Trichoderma%20root%20knot%20nematode%20biocontrol "OpenAlex — Trichoderma/nematoide"

[7]: https://api.openalex.org/works?search=algae%20drilling%20cuttings%20fertilizer%20Brazil "OpenAlex — algas/cascalho/fertilizante"
