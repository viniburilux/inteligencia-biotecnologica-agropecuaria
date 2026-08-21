# ASIE_QUESTION_TRANSFORMATION_GRAMMAR_V0

**Status:** reconstrução da mecânica de transformação de perguntas observada nos ciclos ASIE V0. Este artefato não implementa um engine, não seleciona novas queries e não executa coleta.
**Gerado em:** `2026-08-21T14:31:41.081897+00:00`
**Unidade analisada:** `P → R → S → P'` — pergunta, resultado, sinal interpretado e próxima pergunta.

## 1. Escopo e leitura correta

O objetivo aqui é tirar a mecânica de reformulação de dentro da narrativa e colocá-la em uma forma observável. Cada registro foi reconstruído a partir dos logs, dos manifestos, das queries e dos cadernos de proveniência já existentes. A classificação dos tipos de operação é uma **inferência analítica sobre transições observadas**; ela não deve ser lida como uma política geral já implementada.

Não houve nova coleta ampla. O artefato também não tenta decidir qual pergunta seria melhor em um corpus novo. Ele apenas responde: **quando uma pergunta recebeu determinado resultado, qual sinal foi lido e que mudança efetivamente apareceu na pergunta seguinte?**

## 2. Gramática operacional observada

A forma mínima extraída dos ciclos é:

```text
P  = objetivo + fonte + entidades + restrições + modalidade + contexto
R  = resultado de recuperação + ruído + âncoras + ausência + contradição
S  = sinal operacional extraído de R
P' = P + delta(S, problema_de_P)

P → R → S → P'
```

A transformação observada não é “o modelo teve uma ideia”. Ela tem a forma mais concreta:

> **Quando P falha, fica ampla demais, abre ruído, revela uma âncora, produz ausência ou separa entidades, o próximo passo muda a representação da pergunta.**

A função `delta` não foi formalizada no ciclo V0. O que existe são instâncias repetidas de operações reconhecíveis: estreitar, expandir, traduzir, trocar a âncora, mudar o mecanismo, trocar a modalidade, bifurcar, separar portfólios, contrastar independentemente, estacionar e congelar o estado.

## 3. Taxonomia operacional

| Operação | O que muda na pergunta | Ocorrências observadas |
|---|---|---:|
| `reframing` | Mudar a unidade de trabalho sem ainda mudar o domínio: registros passam a ser sinais, lacunas e perguntas. | 1 |
| `branching` | Uma pergunta agregada vira duas ou mais perguntas independentes que podem seguir em paralelo. | 2 |
| `expansion` | Adicionar atores, organismos, processos ou aplicações observados para testar se o sinal sobrevive a outra âncora. | 1 |
| `narrowing` | Adicionar restrições explícitas — espécie, patógeno, cultura, mecanismo, material ou contexto experimental — para reduzir ruído. | 7 |
| `language_change` | Trocar o idioma ou a forma lexical quando a indexação da primeira formulação não abre evidência suficiente. | 2 |
| `identifier_pivot` | Trocar uma combinação de palavras por identificador de família, strain, código ou outro handle observado. | 3 |
| `anchor_substitution` | Substituir uma âncora frágil por outra observada no resultado; isso não declara que as entidades são equivalentes. | 1 |
| `mechanism_change` | Trocar uma categoria ou objeto amplo por mecanismo/processo/material específico que explica melhor o sinal. | 2 |
| `contextualization` | Adicionar geografia, cultivo, modalidade de uso ou contexto experimental/aplicado. | 2 |
| `title_anchor` | Extrair uma entidade nova de um título retornado e convertê-la na próxima pergunta. | 1 |
| `source_switch` | Levar a mesma ponte para outra modalidade de fonte, como patente → literatura ou literatura → patente. | 3 |
| `independent_contrast` | Usar outra fonte para testar se o sinal reaparece sem confundir coincidência com confirmação. | 7 |
| `portfolio_split` | Separar atores ou famílias quando uma coocorrência parece uma plataforma comum, mas os resultados não sustentam essa unidade. | 1 |
| `entity_resolution` | Classificar nomes como alias seguro, candidato ou separado antes de criar a próxima relação. | 1 |
| `parking` | Estacionar a trilha quando a reformulação aumenta cobertura mas não cria uma ponte mais específica. | 1 |
| `state_freeze` | Manter o baseline intacto e registrar a exploração como fila de evidência até que um critério de incorporação seja atendido. | 1 |

A contagem é de **rótulos aplicados às transições**, não de desempenho. Uma mesma transição pode conter mais de uma operação; por isso, as contagens não somam o número de registros.

## 4. As transformações mais informativas

### 4.1 Da coleção para a superfície de decisão

No H0, a primeira transformação não foi uma busca adicional. O corpus de 379 registros virou radiografia, sinais e 20 perguntas derivadas. Esse é o primeiro operador: **mudar o estado representado antes de mudar a query**. Sem essa passagem, a pergunta seguinte seria apenas outra busca manual sobre a mesma coleção.

### 4.2 Da pergunta ampla para uma fila de ramos

No H1 e no A0, uma pergunta agregada se abriu em blocos paralelos. A bifurcação não foi uma preferência estética: os sinais combinavam recorrência com mecanismos e aplicações diferentes. O resultado foi manter fungos, nutrientes microbianos, produção local e carbono como ramos com destinos próprios.

### 4.3 Da consulta morta para uma consulta reparada

Q02, Q04 e Q12 mostram três reparos diferentes. Em Q02, a âncora foi trocada por `CMRP 4490`; em Q04, o inglês foi trocado por vocabulário brasileiro; em Q12, a categoria `industrial waste` foi trocada por cascalho de perfuração e biofixação. O padrão comum é: **o resultado insuficiente não encerra a trilha; ele informa qual dimensão da pergunta precisa mudar**.

### 4.4 Do resultado para o identificador

Em A1/A2, a reformulação em português abriu `BR112019020483A2`. A pergunta seguinte deixou de ser uma combinação lexical e passou a ser uma inspeção por identificador, com extração de atores, organismos e atributos de uso. O identificador funciona como uma nova unidade de navegação.

### 4.5 Do título para uma entidade biológica precisa

Em A3, o título sobre *Trichoderma citrinoviride* e *Meloidogyne incognita* reduziu uma pergunta ampla para um par espécie–patógeno. A próxima pergunta ganhou precisão biológica e foi levada a outra modalidade de fonte. O título não foi tratado como conclusão; foi tratado como **âncora para a próxima investigação**.

### 4.6 Da coocorrência para a separação de portfólios

Em A6/A8, Locus e Pivot Bio apareceram na vizinhança de saúde radicular, fosfato e nitrogênio. A transformação correta não foi unir tudo numa plataforma: foi separar os atores e gerar uma comparação centrada em portfólio. Aqui, a inteligência está também em **não colapsar uma ponte**.

### 4.7 Da ausência para o estacionamento

Em A7, a reformulação da trilha de microalgas aumentou o universo bibliográfico, mas não trouxe a cadeia direta algas–cascalho–fertilizante–Brasil. A próxima pergunta deixou de ser outra expansão ampla e passou a ser uma condição de retomada: só continuar se surgir nova âncora. Isso é estacionamento operacional, não descarte.

## 5. Catálogo de transições observadas

| ID | P resumida | R observado | S | Operação dominante | P' |
|---|---|---|---|---|---|
| T01 | Que estruturas, hubs, organismos e lacunas são visíveis no corpus de 379 registros? | A Radiografia V0 produziu 20 queries derivadas e um caminho de execução para a segunda rodada. | O corpus era grande o bastante para mostrar recorrências, mas ainda não era um mapa de investigação. | `reframing`, `state_representation_change`, `radiography` | Executar os primeiros blocos que combinem organismo, processo, aplicação e contexto local. |
| T02 | Os quatro blocos abrem famílias patentárias ou literatura, e qual tem maior densidade local ou industrial? | Nove queries patentárias e uma bibliográfica foram executadas; o estado conservador passou a 429 registros com quatro trilhas mais concretas. | Trichoderma/fermentação industrial, nutrientes microbianos/formulação, produção local de bioinsumos e o corredor inesperado carbono/alga. | `branching`, `parallelization`, `expansion`, `entity_expansion` | Usar os atores, organismos e termos técnicos recém-visíveis para gerar queries de expansão em vez de repetir os blocos originais. |
| T03 | As trilhas observadas podem ser expandidas por atores, organismos, tecnologias e pontes de aplicação? | Foram executadas expansões V1 e V2 por entidades e processos; o estado acumulado foi posteriormente fechado em 763 obras. | A expansão revelou recorrências, mas também produziu colisões e ruído que precisavam ser reagregados antes de novas perguntas. | `state_update`, `reaggregation`, `iteration`, `radiography` | Qual ator, organismo, tecnologia ou relação de aplicação merece a próxima query, e qual formulação deve ser reformulada se falhar? |
| T04 | Embrapa Bacillus velezensis bioreactor formulation Brazil | A formulação direta foi insuficiente; a reformulação `Bacillus velezensis CMRP 4490 bioreactor Brazil` retornou 2 ocorrências e 1 registro único. | O identificador/âncora `CMRP 4490` era mais recuperável do que a combinação institucional ampla. | `query_repair`, `identifier_pivot`, `anchor_substitution`, `narrowing` | Bacillus velezensis CMRP 4490 bioreactor Brazil |
| T05 | Solubio on farm bioinput production Brazil patent | A formulação direta foi insuficiente; `Solubio bioinsumo fermentação produção propriedade rural` retornou 1 ocorrência e 1 registro único. | Termos brasileiros de domínio e aplicação foram mais informativos que a formulação em inglês. | `query_repair`, `language_change`, `lexical_reexpression`, `contextualization` | Solubio bioinsumo fermentação produção propriedade rural |
| T06 | microalgae industrial waste biofertilizer Brazil | A formulação direta foi insuficiente; `microalga cascalho perfuração biofixação fertilizante` retornou 1 ocorrência e 1 registro único. | O elo ficou recuperável quando `industrial waste` foi trocado por um resíduo concreto e por um mecanismo/processo específico. | `query_repair`, `narrowing`, `mechanism_change`, `material_pivot`, `contextualization` | microalga cascalho perfuração biofixação fertilizante |
| T07 | USP Trichoderma harzianum sophorolipid Brazil | A busca patentária abriu 2 ocorrências e 1 registro; a pergunta foi convertida em contraste bibliográfico, com 16 obras e 10 registros únicos. | O sinal patentário precisava de uma modalidade independente para verificar se a ponte reaparecia na literatura. | `independent_contrast`, `source_switch`, `modality_switch` | Trichoderma harzianum sophorolipids biocontrol Brazil |
| T08 | microbial inoculant polymer stability nitrogen fixation | A consulta bibliográfica retornou 1.601 obras no universo e 10 registros capturados. | A formulação polimérica recorrente na patente tinha um corredor bibliográfico amplo, útil como contexto mas não como prova de uma plataforma única. | `independent_contrast`, `source_switch`, `scope_calibration` | Verificar, em futura rodada, organismo, aplicação e contexto experimental específicos dentro do corredor de estabilidade. |
| T09 | on farm bioinput fermentation Brazil | A consulta bibliográfica retornou 67 obras no universo e 10 registros capturados. | A cadeia local de produção precisava de literatura de aplicação para não ficar restrita a famílias patentárias. | `independent_contrast`, `source_switch`, `application_pivot` | Narrowing futuro por organismo, cultura ou contexto de produção local. |
| T10 | Quais nomes podem ser unificados com segurança, quais permanecem candidatos e quais devem ficar separados? | A resolução conservadora separou aliases seguros, grupos candidatos e nomes deliberadamente mantidos separados. | Colisões de nomes poderiam criar pontes falsas e contaminar as próximas perguntas. | `entity_resolution`, `uncertainty_preservation`, `false_bridge_control` | Usar apenas aliases seguros como uma mesma âncora; manter candidatos e separados em trilhas distintas. |
| T11 | Quais pontes de coocorrência do estado congelado abrem um caminho de evidência quando pesquisadas independentemente? | O analisador do estado escolheu quatro ramos: fungo–nematoide–soja; fixação de nitrogênio–saúde radicular–milho; Trichoderma–fosfato–saúde radicular; carbono/alga como ramo de contraste negativo. | Coocorrências combinavam recorrência com mecanismo ou aplicação e não eram cópias diretas da lista de prioridades do usuário. | `branching`, `parallelization`, `signal_to_question`, `independent_contrast` | Executar uma pergunta patentária e uma bibliográfica por ramo; reformular ou estacionar conforme o resultado. |
| T12 | fungal biocontrol nematode soybean | A busca em inglês retornou 465 resultados com muito ruído; a reformulação em português retornou 32 e abriu BR112019020483A2. | A linguagem era variável de recuperação, e a formulação brasileira reduziu o ruído. | `query_repair`, `language_change`, `narrowing`, `noise_reduction` | fungo biocontrole nematoide soja |
| T13 | O resultado BR112019020483A2 conecta quais organismos, aplicações, formulações ou modos de uso? | A página da família expôs identificador estável, atores, Trichoderma, Bacillus, colonização radicular, uso em semente/foliar e linguagem de estabilidade de formulação. | O identificador e os atributos observados eram âncoras mais precisas que a combinação lexical inicial. | `identifier_pivot`, `result_inspection`, `attribute_extraction` | Pesquisar a espécie/pathógeno observado e manter a pergunta de patente brasileira separada do corredor bibliográfico. |
| T14 | Trichoderma nematode root health soybean | A busca bibliográfica retornou 3.550 obras e trouxe no título `Trichoderma citrinoviride` com `Meloidogyne incognita`; a query desse par retornou 95 obras e a patente BR filtrada não retornou resultados. | Um título direto forneceu espécie e patógeno, criando âncora mais informativa que o resultado agregado. | `title_anchor`, `entity_extraction`, `narrowing`, `independent_contrast`, `modality_split` | Trichoderma citrinoviride Meloidogyne incognita; depois testar o mesmo par no corredor patentário BR. |
| T15 | microbial nitrogen fixation root health maize rhizosphere | A busca ampla retornou 13.618 obras dominadas por literatura genérica; a reformulação para `plant growth promoting rhizobacteria nitrogen fixation maize greenhouse` retornou 6.737 e expôs estudo direto de inoculação em milho sob casa de vegetação. | O contexto experimental `greenhouse` e a categoria PGPR tornaram a pergunta mais operacional. | `narrowing`, `mechanism_change`, `experimental_context_addition`, `lexical_reexpression` | Narrowing futuro por organismo específico ou ensaio de campo brasileiro; não executar nova expansão ampla nesta rodada. |
| T16 | fungal biocontrol nematode plant root colonization | A busca ampla retornou 8.842 obras e misturou PGPR, Bacillus, AMF e Trichoderma; a reformulação para `Trichoderma root knot nematode biocontrol` retornou 3.763 com títulos diretos sobre espécies e mecanismos. | O organismo e o tipo de patógeno eram melhores restrições que `fungal` e `nematode` isolados. | `narrowing`, `entity_swap`, `mechanism_preservation`, `noise_reduction` | Comparar espécies, patógeno, formulação e atributos de aplicação com BR112019020483A2 e os registros locais Bacillus/Trichoderma. |
| T17 | Trichoderma phosphate root health | A query retornou 384 resultados, expondo famílias Locus sobre saúde/imunidade radicular e uma família Pivot Bio sobre solubilização de fosfato. | A ponte atravessava portfólios distintos; não isolava uma plataforma comum de Trichoderma. | `portfolio_split`, `entity_separation`, `independent_contrast`, `uncertainty_preservation` | Contrastar famílias Locus de raiz/rizosfera/carbono com famílias Pivot de fosfato/nitrogênio. |
| T18 | microalgae drilling waste biofixation fertilizer | A query bibliográfica inicial retornou 18 obras genéricas; a reformulação `algae drilling cuttings fertilizer Brazil` retornou 227, mas os títulos de topo ficaram em água produzida, reaproveitamento de cascalho e CCUS, sem a cadeia direta esperada. | A reformulação aumentou cobertura, mas não aumentou a especificidade da ponte. | `independent_contrast`, `lexical_reexpression`, `scope_check`, `parking` | Retomar apenas se aparecer nova âncora institucional, de resíduo específico ou de aplicação. |
| T19 | microbial nitrogen fixation root health maize | A query patentária com filtro BR mostrou uma família visível, BR112020022643A2, associada à Locus Agriculture IP Company, LLC, sobre produtos microbianos para saúde e imunidade radicular. | Um resultado escasso tornou-se útil quando convertido em âncora de ator, não em continuação genérica da query. | `actor_pivot`, `identifier_pivot`, `entity_separation`, `narrowing` | Comparar famílias Locus de raiz/rizosfera com famílias Pivot de fosfato/nitrogênio e com o corredor bibliográfico PGPR/milho. |
| T20 | O que deve ser atualizado após a exploração autônoma e o que deve permanecer pendente? | As saídas foram armazenadas em `raw_v3/asie_autonomous/`; o baseline `normalized_v2` não foi alterado. | Os resultados eram uma fila de evidência com decisões, não um novo corpus validado. | `state_freeze`, `provenance_preservation`, `queue_update`, `uncertainty_preservation` | Comparar a fila adaptativa com uma estratégia fixa no mesmo estado congelado antes de construir um módulo. |
| T21 | Sob o mesmo estado congelado, prefixo e orçamento, a política dependente de resultado produz perguntas mais específicas e decisões mais acionáveis que uma lista fixa? | O replay fixo produziu 3 âncoras, 2 transições acionáveis e 0 reformulações; o adaptativo produziu 6 âncoras, 7 transições acionáveis, 5 reformulações e decisões explícitas de estacionamento/bloqueio. | A diferença veio da transformação da unidade de busca: termos → idioma, identificador, espécie/pathógeno, contexto e decisão de ramo. | `controlled_replay`, `adaptive_vs_fixed_contrast`, `decision_production` | Congelar um A/B futuro com orçamento, labels de relevância, tempo, falsos candidatos, completude de provenance e próxima ação definidos antes da execução. |

O registro computável completo, incluindo problema da pergunta anterior, decisão, caveats e hashes, está em [`ASIE_QUESTION_TRANSITIONS_V0.jsonl`](ASIE_QUESTION_TRANSITIONS_V0.jsonl).

## 6. O que a gramática sustenta

A evidência sustenta uma gramática de **reformulação orientada por resultado**, não apenas uma lista de consultas. A pergunta seguinte muda porque o resultado oferece uma das seguintes coisas: ruído que pede restrição; ausência que pede reparo; entidade nova que pede ancoragem; ponte que pede contraste; ou divergência entre atores que pede separação.

O núcleo da mecânica pode ser resumido assim:

```text
se R é ruidoso       → P' adiciona restrições ou troca idioma
se R é insuficiente  → P' troca a âncora, o material ou o mecanismo
se R revela ID       → P' pivota para o identificador/família
se R revela entidade → P' estreita por espécie, patógeno, ator ou contexto
se R cruza fontes    → P' muda a modalidade para contraste independente
se R separa atores   → P' bifurca ou mantém portfólios distintos
se R não acrescenta  → P' estaciona e registra condição de retomada
```

Essas regras são uma **gramática descritiva**, derivada depois dos ciclos. Elas ainda não formam um engine, não definem pesos, não resolvem a escolha entre operações concorrentes e não garantem que a mesma transformação funcione em outro domínio.

## 7. O que ainda não aparece nos dados

Não há evidência suficiente de uma função geral que calcule a melhor próxima pergunta, de um ranking estável entre operações, de um critério quantitativo único para distinguir ruído de sinal, de uma política formal de parada ou de uma avaliação em corpora independentes. Também não está demonstrado que toda reformulação adaptativa supera uma estratégia fixa; o replay V0 apenas mostrou vantagem processual dentro daquele desenho.

A distinção importante é: **a gramática foi observada; a política geral ainda não foi validada**.

## 8. Proveniência

Os registros deste documento apontam para os artefatos de origem por caminho relativo e SHA-256. Os resultados patentários e bibliográficos continuam metadata-only; nenhum PDF, dado científico bruto ou corpus normalizado novo foi incorporado por este trabalho.

| Artefato de origem | SHA-256 no momento da reconstrução |
|---|---|
| `ASIE_FIXED_ADAPTIVE_REPLAY_V0.json` | `efcb8ec4e5b21369b3439ff8fb2da86a7b00e1edd83249b29527a40df3dc52fa` |
| `ASIE_FIXED_ADAPTIVE_REPLAY_V0.md` | `2bb7b1b78302281f0b5767fdb34030b77ee949bb1716f5579a0633aab649c175` |
| `ENTITY_RESOLUTION_V1.json` | `09ead7c4df22485bc8df3279af726feead6dd4683be3c82b8508c25bce50fba6` |
| `EXPANSION_QUERIES_V1.json` | `1e483ce681734d360f1a6ba14e041d61f4c451755167b4a76f6e0048b70bafd5` |
| `EXPANSION_QUERIES_V2.json` | `3bc3efdca0e5d4235280c82cc6b7b5c1e19826262299659d9fbe2c8968a60f31` |
| `EXPLORATORY_RADIOGRAPHY_V0.md` | `cc0a65a263869f0f6296e533a5127104ba14f3a500d449fec87d2f5966d965e4` |
| `EXPLORATORY_RADIOGRAPHY_V1.md` | `eb19ef119427e1541ffc4ba19bcc6039eaf262302347f14f16800d357bda89e3` |
| `RADIOGRAPHY_METHOD_V0.md` | `3fc132f9966ddfff977671501f16194246ae0de19a3dd7d03eac6ade977cda07` |
| `RADIOGRAPHY_V1_PATENT_FINDINGS.md` | `f4af141ee6cd07e80d765a2013f951b97ea25ed646c8fce14527ce05c90c0ad9` |
| `RADIOGRAPHY_V1_QUERY_EXECUTION.json` | `ab7495dc2b217e53053b17a8048168825fd46e79551b90221f0ba962b6c5d15d` |
| `SECOND_ROUND_INGESTION_SUMMARY_V0.md` | `cf6d62ae34baed429bf9f8a893d50b22a9493dcda93d0172da6dc2b86ff5c1e1` |
| `SECOND_ROUND_PATENT_FINDINGS_V0.md` | `d5cfa537acb4b4cbe2c6b3560f87c596f4d9becc1e01122bd59c6b2e03f7600b` |
| `SECOND_ROUND_PLAN_V0.json` | `389a25c72203cdc75a28bb85014d989e36dcd449891356d7f9e29b9fcbe77069` |
| `asie_autonomous_browser_findings_v0.md` | `dac005717bb13220769ed191f69d40102bbbd2d6b164b9f1823b1cb40b309042` |
| `asie_autonomous_openalex_findings_v0.md` | `490349a5886853d1f116ded2ef634818136f6c0256f8aa138a1b31d7e0198d31` |
| `asie_autonomous_openalex_reformulations_findings_v0.md` | `b67564e1b1213807c6bbdca0a12ad42a5c448cf93f317d41417778c1fd7f9cf3` |
| `asie_autonomy_state_v0.json` | `b00ad658717e07efe941483a07748dd324f7390b8f03b560695ae7dfcac47e1b` |
| `ingestion_manifest_v1.jsonl` | `a0d48bf52aa4c9f89975ed64c12be0f117005fa04c26ae30f5a00c4c31954f1c` |
| `ingestion_manifest_v2.jsonl` | `51a3d18aaa0cf279818ca1fe8f6fcaa44275682db9fbd68bb08b921b62181b2f` |
| `next_queries_v0.json` | `731fe25701fe738934f3fa15fd2ccbcc4effeed1c818b8dd4a6a46bddadf67f1` |
| `normalized_v2/normalization_summary_v2.json` | `31144a6e2e48f88c77b9edff47b98e58697d9d8e62fe24cc6423a18015cb58b3` |
| `raw_v2/openalex_followup/q13_trichoderma_sophorolipids_biocontrol_brazil.json` | `6efd5e87496101f1c1a6eaedf8bda4685e9443334f511e3988cbf5c0afecc1ad` |
| `raw_v2/openalex_followup/q14_microbial_inoculant_polymer_stability_nitrogen.json` | `4edfda311a1ef54f6156bebe97d803384b307df0cce0bfa9a2ba6c2e380d0dcb` |
| `raw_v2/openalex_followup/q15_on_farm_bioinput_fermentation_brazil.json` | `65c01230a470e3c5afa381b83ad8fcb3b5181fa2cd74f3c963ec3c493851a269` |

## Referências

[1]: ASIE_BEHAVIOR_V0.md "Reconstrução do comportamento adaptativo ASIE V0"
[2]: ASIE_CYCLE_LOG_V0.jsonl "Log computável dos ciclos ASIE V0"
[3]: ASIE_FIXED_ADAPTIVE_REPLAY_V0.md "Replay fixo versus adaptativo"
[4]: RADIOGRAPHY_V1_QUERY_EXECUTION.json "Execução das queries da Radiografia V1"
[5]: asie_autonomous_openalex_findings_v0.md "Achados bibliográficos autônomos"
[6]: asie_autonomous_browser_findings_v0.md "Achados patentários autônomos"

