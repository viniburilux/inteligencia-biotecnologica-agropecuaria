# ASIE_BEHAVIOR_V0

**Status:** reconstrução empírica do comportamento adaptativo observado no laboratório agropecuário.

**Data do artefato:** 2026-08-21T07:13:02.962274+00:00

## Escopo

Este documento não cria o ASIE e não altera o núcleo privado do OI. Ele trata o laboratório agropecuário como um experimento já executado e reconstrói o comportamento adaptativo que apareceu entre estado, sinal, decisão, pergunta, execução, resultado e atualização de estado.

O ponto de partida do teste autônomo foi o estado cumulativo congelado em **763 obras metadata-only**, com 2.680 atores normalizados, 767 instituições, 4.045 relações observadas e 536 sinais de aplicação. O corpus-base não foi alterado durante a exploração autônoma. As novas evidências ficaram em `raw_v3/asie_autonomous/`.

## A sequência observada

| Fase | Estado | Sinal | Decisão | Atualização observada |
|---|---|---|---|---|
| V0 | 379 registros | Recorrências ainda sem mapa operacional | Construir radiografia | 20 perguntas derivadas |
| Segunda rodada | 379 registros + radiografia V0 | Quatro blocos: Trichoderma, nutrientes microbianos, produção local e carbono/alga | Executar blocos em paralelo | 429 registros e quatro trilhas mais concretas |
| Expansões | 429 registros | Atores, organismos e processos recorrentes | Expandir por entidades e termos, não repetir consultas | Novos lotes V1/V2; estado cumulativo fechado depois em 763 obras |
| Radiografia V1 | 763 obras | Hubs, organismos, aplicações, lacunas e queries insuficientes | Executar 17 queries, reformular três e preservar estados mortos | Famílias, literatura, proveniência e resolução conservadora |
| Teste autônomo | 763 obras congeladas | Coocorrências escolhidas pelo estado, não pelo usuário | Abrir quatro ramos, reparar consultas e estacionar trilhas fracas | Evidence queue em `raw_v3/asie_autonomous/` |

## Operadores adaptativos que apareceram

### 1. Radiografar antes de buscar novamente

A primeira mudança não foi uma query. Foi transformar registros em sinais, relações, clusters e lacunas. A radiografia converteu um corpus em uma superfície de decisão. Esse operador aparece nos artefatos V0 e V1 e é o que permite gerar perguntas que não estavam na lista inicial.

### 2. Usar densidade como prioridade, não como conclusão

`fungo`, `biocontrole` e `fermentacao_bioprocesso` eram sinais densos. Coocorrências como fungo–nematoide, fungo–soja e fixação de nitrogênio–saúde radicular foram usadas para abrir perguntas. A densidade escolheu onde olhar; ela não foi usada para afirmar que existia uma plataforma tecnológica única.

### 3. Reformular consultas mortas com termos observados

A busca Embrapa–*Bacillus velezensis*–biorreator falhou e foi substituída por `CMRP 4490`. A busca Solubio em inglês falhou e foi substituída por termos brasileiros de bioinsumo, fermentação, produção e propriedade rural. A busca ampla de microalgas e resíduos foi substituída por microalga, cascalho de perfuração, biofixação e fertilizante. Esse é um comportamento adaptativo explícito: o resultado negativo altera a próxima pergunta.

### 4. Trocar palavras por identificadores

Quando `BR112019020483A2` apareceu na busca em português, a exploração abriu a página da família. A unidade de trabalho mudou de combinação lexical para identificador, ator, organismo, uso e atributo de formulação. Esse salto não seria recuperado repetindo a mesma consulta ampla.

### 5. Seguir pontes inesperadas sem colapsar as entidades

Trichoderma levou a biocontrole, soforolipídeos, fermentação, celulase e enzimas. Petrobras levou a microalgas, biofixação de CO₂, cascalho de perfuração e fertilizante. Na exploração autônoma, Trichoderma–fosfato–saúde radicular levou a Locus e Pivot Bio, mas a decisão foi manter os portfólios separados.

### 6. Manter trilhas paralelas

O teste autônomo não escolheu entre fungos, nutrientes, rizosfera e carbono. Abriu quatro ramos e aplicou a mesma lógica de recuperação, reparo e decisão a cada um. O resultado foi assimétrico: Trichoderma–nematoide ganhou prioridade, Locus/Pivot virou contraste de portfólio, e o corredor carbono foi estacionado.

### 7. Tratar ausência como atualização de estado

A consulta patentária `Trichoderma citrinoviride Meloidogyne incognita Brazil` não encontrou resultados. A literatura para a mesma espécie/pathógeno foi densa. O estado atualizado não é “a tecnologia não existe”; é “a ponte é bibliográfica sob esta formulação e está bloqueada como corredor patentário brasileiro”.

### 8. Parar sem apagar

A trilha algas–resíduos–fertilizante recebeu uma busca inicial e uma reformulação. A reformulação abriu literatura de água produzida e reaproveitamento de cascalho, mas não uma cadeia direta até fertilizante no topo observado. A decisão foi estacionar, preservar os artefatos e exigir uma nova âncora antes de gastar mais consultas.

## Onde está a inteligência adaptativa

A inteligência não está em uma função isolada. Ela aparece na **transição entre estados**. O padrão observado é:

> **estado → leitura de sinais → escolha de uma pergunta informativa → execução → leitura do resultado → reparo, bifurcação, aprofundamento ou estacionamento → novo estado**

A parte mais forte é a escolha da próxima representação do problema. O pipeline troca `nome de ator` por `identificador`, `inglês` por `português`, `organismo` por `processo`, `consulta ampla` por `família`, e `trilha surpreendente` por `contraste independente`.

A parte ainda fraca é a formalização. As decisões foram reproduzíveis por artefatos e scripts, mas ainda dependeram de lógica distribuída entre radiografia, leitura de resultados, parser, resolução de entidades e decisão operacional. Portanto, a evidência atual sustenta **comportamento ASIE distribuído**, não um motor ASIE pronto.

## Resultado do teste de autonomia

O teste encontrou evidência **positiva, mas não definitiva**, de que a exploração adaptativa abre caminhos que uma estratégia fixa provavelmente não abriria: o salto para a família BR112019020483A2 veio de uma reformulação linguística; o salto para *Trichoderma citrinoviride* e *Meloidogyne incognita* veio de um título bibliográfico retornado pela própria busca; a consulta Trichoderma–fosfato separou Locus de Pivot Bio; e a trilha de carbono foi estacionada após uma busca independente não acrescentar a ponte esperada.

O replay comparável posterior usou o mesmo estado congelado, o mesmo prefixo de quatro perguntas e quatro passos pós-prefixo em cada braço. A continuação fixa produziu 3 âncoras estáveis, 2 transições acionáveis, nenhuma reformulação e nenhuma decisão explícita de estacionamento/bloqueio. A continuação adaptativa produziu 6 âncoras estáveis, 7 transições acionáveis, 5 reformulações, 2 decisões explícitas de estacionamento/bloqueio e 4 decisões específicas por ramo. O resultado favorece o comportamento adaptativo em **especificidade da fila de investigação e produção de decisões**, dentro desse replay.

Isso ainda não é um benchmark randomizado nem uma prova geral de superioridade. O replay usa uma lista fixa histórica e uma trilha adaptativa já observada; os dois braços não respondem exatamente às mesmas perguntas semânticas. Ainda não foram medidos, com critérios previamente congelados, tempo, falsos candidatos, recall, completude de provenance ou qualidade da resposta final. O próximo teste deve executar esses critérios com o mesmo orçamento e registro paralelo.

## Referências

[1]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/EXPLORATION_CYCLE_V1_SUMMARY.md "Resumo do ciclo exploratório V1"

[2]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/RADIOGRAPHY_V1_QUERY_EXECUTION.json "Registro computável da Radiografia V1"

[3]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/ENTITY_RESOLUTION_V1.json "Resolução conservadora de entidades V1"

[4]: https://patents.google.com/patent/BR112019020483A2/en "Google Patents — BR112019020483A2"

[5]: https://api.openalex.org/works?search=Trichoderma%20citrinoviride%20Meloidogyne%20incognita "OpenAlex — Trichoderma citrinoviride / Meloidogyne incognita"

[6]: https://patents.google.com/?q=(Trichoderma+citrinoviride+Meloidogyne+incognita+Brazil)&country=BR "Google Patents — espécie/pathógeno com filtro BR"

[7]: ASIE_FIXED_ADAPTIVE_REPLAY_V0.md "Replay fixo versus adaptativo V0"
