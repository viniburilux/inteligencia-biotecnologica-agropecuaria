# Teste de Reutilização Estrutural V1

## Pergunta

A estrutura reconstruída no corredor agropecuário — entidade → caracterização → mecanismo/propriedade → contexto de aplicação → processo/transformação → artefato/documento → lacunas — pode representar trajetórias anteriores em outros domínios sem depender dos nomes do Agro?

## Método

O teste usou apenas trajetórias já existentes no acervo. Não houve nova coleta, execução de notebook, download de dado ou alteração de repositório. A comparação não tenta igualar semanticamente os domínios; ela verifica se os papéis estruturais podem ser preservados quando os objetos mudam.

## Resultado curto

> A estrutura transfere-se como **contrato de papéis e relações**, não como uma cadeia rígida de etapas.

Nos casos não agropecuários, nem sempre existe uma formulação ou patente. O equivalente estrutural pode ser um modelo, um dataset, um mapa, um documento-fonte, uma interface, um cluster ou uma decisão de aquisição. A operação reutilizável é preservar a relação entre **objeto**, **propriedade observada**, **contexto de uso**, **transformação executada**, **artefato produzido**, **limite** e **próxima decisão**.

## Mapeamentos observados

| Domínio | Entidade/objeto | Caracterização/propriedade | Aplicação/contexto | Transformação/processo | Artefato ou fonte | Resultado |
|---|---|---|---|---|---|---|
| Organoides | sinais neurais, rótulos, população | firing-rate, network features, incompatibilidade de alvo | previsão de desempenho/estado futuro | troca de target e split temporal | experimento OI 002/003 | Estrutura transferível; formulação vira target/representação |
| Datasets públicos | dataset/candidato | modalidade, licença, acesso, relação paper–dataset | compatibilidade com eletrofisiologia | validação metadata-only e gate de aquisição | fixture TraceFoundry | Estrutura transferível; patente vira documento de proveniência |
| SIGMINE/GhostWorks | território, tile, embedding, cluster | similaridade, silhouette, atividade operacional | detectar mineral ou comportamento | troca de objeto e âncora | mapa, arquétipo, superfície consultável | Forte transferência; aplicação e processo mudam de papel |
| Patentes/mineração | material, impureza, rota técnica | estanho, arsênio, antimônio, lixiviação | recuperação de material | pivot material/mecanismo e branching | família patentária e queries | Quase isomorfismo com Agro |
| Satélite | embedding/vetor/portal | similaridade, escala, bloqueio de API, produto escalar inadequado | mapa/interface/monitoramento | correção de mecanismo e sequenciamento dados → lógica → interface | dataset, método, outputs | Transferência forte; o processo é computacional |
| PNCP Bahia | registro/anomalia | anoCompra, tema, concentração, ausência de prova financeira | triagem de contratação pública | pivot de provenance e source switch | documento de origem | Transferência forte; documento-fonte ocupa lugar de patente |

## Cadeia generalizada

A cadeia agropecuária pode ser generalizada assim:

```text
O  = objeto ou entidade
C  = caracterização/propriedade observada
M  = mecanismo, comportamento ou explicação operacional
U  = uso, contexto ou decisão que se quer suportar
T  = transformação, experimento ou processo aplicado
A  = artefato/fonte produzido ou consultado
L  = lacuna, bloqueio, contradição ou limite
D  = decisão seguinte

O → C → M → U → T → A → L → D
```

Em Agro, `O` pode ser uma strain, `C` uma caracterização genômica, `M` biocontrole, `U` soja ou milho, `T` fermentação/biorreator, `A` patente/formulação e `D` revisão futura.

Em SIGMINE, `O` é território/embedding, `C` é cluster/similaridade, `M` é comportamento minerário, `U` é busca de áreas similares, `T` é recuperação/arquétipo, `A` é mapa ou superfície queryable e `D` é mudar a pergunta de mineral para atividade.

Em PNCP, `O` é registro, `C` é anomalia, `M` é sinal de inconsistência, `U` é verificação de contratação, `T` é drilldown/source switch, `A` é documento original e `D` é bloquear conclusão até obter prova.

## O que foi validado

| Proposição | Resultado |
|---|---|
| Os domínios possuem objetos diferentes, mas podem ser descritos por papéis estruturais equivalentes. | **Sustentado pelos exemplos existentes.** |
| A cadeia precisa manter exatamente os mesmos nós Agro. | **Rejeitado.** O papel de formulação/patente é substituído por modelo, dataset, mapa, documento ou interface. |
| A estrutura pode ser usada para separar observado, inferido, lacuna e decisão. | **Sustentado.** Isso aparece nos experimentos OI, TraceFoundry, SIGMINE, satélite e PNCP. |
| A estrutura já é um engine geral. | **Não demonstrado.** O teste mostra um contrato descritivo, não uma política de seleção ou execução. |
| A reconstrução estrutural é uma capacidade distinta de reformular perguntas. | **Sustentado como hipótese operacional forte.** Reformulação muda `P`; reconstrução organiza `O, C, M, U, T, A, L` para escolher a próxima decisão. |

## A segunda capacidade da máquina

O Agro tornou visível uma possível segunda capacidade:

```text
Capacidade 1: resultado → nova pergunta
Capacidade 2: evidências heterogêneas → estrutura → próxima decisão
```

A primeira opera sobre a trajetória de busca. A segunda opera sobre a representação do que foi encontrado. Elas se alimentam, mas não são a mesma coisa. Uma pergunta pode ser reformulada sem que a estrutura tecnológica esteja completa; uma estrutura pode ser reconstruída mesmo quando a próxima pergunta ainda está bloqueada.

A formulação mais precisa, neste momento, é **reconstrução estrutural orientada por evidência**. Ela não significa “montar uma cadeia bonita”. Significa colocar cada relação em um papel, registrar modalidade e proveniência, manter lacunas visíveis e impedir que a proximidade entre documentos seja convertida automaticamente em continuidade.

## Limites

O teste não compara desempenho quantitativo entre domínios, não mede recall, não calcula similaridade de grafos e não prova que a operação funcionará em qualquer corpus. A evidência vem de trajetórias já documentadas e algumas são mais completas que outras. O resultado é suficiente para justificar uma validação futura em um segundo domínio, mas não para implementar um mecanismo geral.

## Frontier de validação

A próxima validação deve escolher um domínio não agropecuário com evidência heterogênea já disponível — preferencialmente SIGMINE/GhostWorks ou organoides — e reconstruir a mesma estrutura sem usar o vocabulário Agro. O critério de sucesso não deve ser produzir a mesma cadeia, mas preservar:

1. objeto e entidade sem colapso indevido;
2. propriedade/mecanismo com fonte;
3. contexto de uso;
4. transformação realizada;
5. artefato resultante;
6. lacuna ou bloqueio;
7. próxima decisão justificável.

## Provenance

- `archaeology_transitions_v0.jsonl`.
- `archaeology_behavioral_v0.md`.
- `oi_discovery_build/experiments/EXPERIMENT_002.md`.
- `oi_discovery_build/experiments/EXPERIMENT_003_PLAN.md`.
- `oi_discovery_public/examples/research_move_v0/v001_investigation_state.json`.
- `oi_discovery_public/examples/research_move_v0/v001_research_move.json`.
- `lux_lab/sigmine_mineral_retrieval/docs/context/user_intent_context.md`.
- `lux_lab/pncp_bahia_intelligence/runs/2026-08-21/run_log.md`.
- `luxmemory/conversation-memory/data/process_transformation/transform_02.json`.
- `luxmemory/conversation-memory/data/process_transformation/transform_14.json`.
