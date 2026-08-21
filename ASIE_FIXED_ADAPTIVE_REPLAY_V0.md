# ASIE_FIXED_ADAPTIVE_REPLAY_V0

**Data:** 2026-08-21T07:15:28.991476+00:00  
**Baseline:** snapshot congelado de 763 obras metadata-only.  
**Tipo:** replay comparável de processo, não benchmark randomizado.

## Por que este replay existe

O primeiro teste autônomo mostrou comportamento adaptativo, mas ainda não permitia dizer se esse comportamento acrescentava algo em relação a uma lista fixa. Por isso, foi feito um replay com o mesmo estado inicial e o mesmo prefixo de quatro perguntas autônomas. Depois do prefixo, cada braço recebeu quatro passos:

| Braço | Regra dos quatro passos posteriores |
|---|---|
| Fixo | Seguir quatro consultas pré-comprometidas do pool histórico, sem ler o resultado para escolher a seguinte. |
| Adaptativo | Ler o resultado e transformar título, identificador, ausência ou ruído em próxima pergunta. |

A comparação não mede quem responde melhor. Mede se o braço adaptativo transforma o mesmo orçamento de exploração em **mais transições operacionais**, **mais âncoras específicas** e **mais decisões explícitas de continuar, separar ou estacionar**.

## Resultado do replay

| Métrica | Fixo | Adaptativo |
|---|---:|---:|
| Perguntas no prefixo comum | 4 | 4 |
| Passos pós-prefixo | 4 | 4 |
| Perguntas totais do replay | 8 | 8 |
| Âncoras estáveis identificadas | 3 | 6 |
| Transições acionáveis registradas | 2 | 7 |
| Reformulações | 0 | 5 |
| Decisões explícitas de estacionamento/bloqueio | 0 | 2 |
| Decisões específicas por ramo | 0 | 4 |

O prefixo comum é deliberadamente idêntico. A diferença aparece depois dele. O braço fixo continua consultando termos amplos do pool histórico: `Trichoderma fermentation`, `Trichoderma biocontrol`, `microbial nitrogen fixation formulation` e `phosphate solubilization microbial`. O braço adaptativo usa os próprios resultados para trocar a unidade de busca: `fungo biocontrole nematoide soja`, `BR112019020483A2`, `Trichoderma citrinoviride Meloidogyne incognita` e `PGPR nitrogen fixation maize greenhouse`.

## Leitura operacional

Neste replay, o braço adaptativo produziu o dobro de âncoras estáveis e mais transições acionáveis com o mesmo número total de passos. A diferença veio de operações observáveis: tradução da consulta, inspeção por identificador, extração de espécie e patógeno de um título, estreitamento por contexto experimental e decisões de estacionamento.

Isso é uma **evidência de comportamento**, não uma prova geral de superioridade. O braço fixo foi montado a partir do pool histórico e não é uma estratégia fixa ideal; o braço adaptativo também foi reconstruído a partir de um experimento já executado. O resultado autoriza uma conclusão mais limitada e mais útil:

> No estado agropecuário disponível, o comportamento adaptativo converteu o mesmo prefixo e o mesmo número de passos pós-prefixo em uma fila de investigação mais específica e com mais decisões explícitas do que a continuação fixa usada no replay.

## O que o replay não mede

O replay não mede eficácia agronômica, validade patentária, qualidade científica, liberdade de operação, adoção comercial ou verdade causal. Também não mede tempo de execução, falsos positivos ou recall contra um conjunto de verdade. Esses testes exigiriam um protocolo separado, com orçamento, critérios de relevância e avaliadores definidos antes da execução.

## Decisão

**Não construir o ASIE ainda.** O replay já mostra que existe um comportamento adaptativo que vale a pena preservar. Antes de transformá-lo em módulo, o próximo teste deve congelar, antecipadamente, uma lista fixa e uma política adaptativa, definir o que conta como âncora, próxima ação, falso candidato e bloqueio, e executar os dois braços com o mesmo orçamento e os mesmos critérios de avaliação.

## Proveniência

O estado-base e os hashes estão em [`ASIE_FIXED_ADAPTIVE_REPLAY_V0.json`](ASIE_FIXED_ADAPTIVE_REPLAY_V0.json). O histórico adaptativo está em [`ASIE_CYCLE_LOG_V0.jsonl`](ASIE_CYCLE_LOG_V0.jsonl). A lista fixa histórica está em [`next_queries_v1.json`](next_queries_v1.json). As capturas de resultados estão em [`asie_autonomous_browser_findings_v0.md`](asie_autonomous_browser_findings_v0.md), [`asie_autonomous_openalex_findings_v0.md`](asie_autonomous_openalex_findings_v0.md) e [`asie_autonomous_openalex_reformulations_findings_v0.md`](asie_autonomous_openalex_reformulations_findings_v0.md).

## Referências

[1]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/next_queries_v1.json "Pool histórico de queries V1"

[2]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/blob/main/ASIE_CYCLE_LOG_V0.jsonl "Log computável ASIE V0"

[3]: https://patents.google.com/patent/BR112019020483A2/en "Família patentária BR112019020483A2"

[4]: https://api.openalex.org/works?search=Trichoderma%20citrinoviride%20Meloidogyne%20incognita "OpenAlex — espécie e patógeno"
