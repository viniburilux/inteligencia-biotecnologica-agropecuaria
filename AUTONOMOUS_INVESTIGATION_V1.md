# Autonomous Investigation V1

## Status

`NATURAL_STOP_METADATA_EXPLORATION` — investigação executada sobre o laboratório público, metadata-only, sem engine novo, sem alteração do OI privado e sem conclusão jurídica, comercial, de eficácia ou de adoção.

## Pergunta operacional

> Dado o estado atual do laboratório, qual é a investigação mais informativa que pode ser executada agora, e o que o resultado permite perguntar em seguida?

A execução começou a partir do `STATE_0` congelado. A primeira investigação não foi escolhida por preferência tecnológica: foi selecionada porque a frontier apresentava uma strain concreta, sinais aplicados em múltiplos contextos e uma oportunidade de testar se o sinal abria um corredor.

## Estado e orçamento

| Campo | Valor |
|---|---|
| `STATE_0` | `AUTONOMOUS_INVESTIGATION_V1_STATE_0.json` |
| Corpus de partida | 763 obras, 2.680 atores, 767 instituições, 4.045 relações e 536 sinais de aplicação |
| Fontes | OpenAlex, Google Patents renderizado, Crossref e metadados públicos do repositório UEL |
| Modalidade | metadata-only |
| Execução | 3 ciclos adaptativos, com reformulações internas |
| Limite | parar quando o ganho exigisse texto integral/claims, expansão deliberada ou nova decisão de escopo |

## Trajetória executada

### CYCLE_01 — Ag75 → Ag109 → mecanismo/cultura

A pergunta inicial foi se *Bacillus velezensis* Ag75 abria um corredor entre biocontrole, solubilização de fosfato, promoção de crescimento, milho, soja e instituições. A patente exata por Ag75 não retornou família brasileira. A literatura, porém, encontrou o trabalho específico de Ag75 e revelou Ag109 como nova strain relacionada no entorno UEL–IAP.

O sinal não foi “a trilha falhou”. Foi: **a âncora exata de strain falha na patente, mas a literatura abre uma entidade e um corredor institucional**. A representação mudou de “nome exato da strain” para “strain–mecanismo–cultura–instituição”. A próxima pergunta deixou de repetir Ag75 e Ag109 e passou a testar mecanismo/cultura em patentes brasileiras.

### CYCLE_02 — mecanismo/cultura → CMRP 4490

A reformulação por *Bacillus velezensis*, solubilização de fosfato, biocontrole, milho e soja abriu 11 resultados BR. Entre eles apareceu `BR102024016682A2`, com *Bacillus velezensis* CMRP 4490, processo em biorreator agitado e formulação para bionematicida/inoculante. A literatura OpenAlex retornou o artigo direto de CMRP 4490 sobre atividade antifúngica e promoção de crescimento.

O sinal foi um **identificador de alta especificidade**. A representação mudou de um corredor lexical de strains para uma cadeia concreta `strain → mecanismo → bioprocesso → formulação`. A próxima pergunta foi um contraste institucional e mecanístico entre CMRP 4490, CMRP 4489, Ag75, Ag109 e UEL.

### CYCLE_03 — identificador → corredor institucional multi-strain

O contraste bibliográfico encontrou CMRP 4490, CMRP 4489, Ag75 e Ag109 no mesmo entorno institucional UEL/IAP, com recorrência de autores e tecnologias próximas. Isso abriu um mapa mais amplo: não uma única strain e não necessariamente um único produto, mas um **corredor institucional multi-strain** que atravessa caracterização, biocontrole, promoção de crescimento, nematoides, formulação e bioprocesso.

A evidência não permite fundir strains, provar um projeto único ou afirmar progressão temporal consolidada. Por isso, o estado foi atualizado com três perguntas futuras e o ciclo foi encerrado no ponto natural de parada.

## O que mudou enquanto a investigação investigava

```text
corpus amplo
  → strain Ag75
  → entidade nova Ag109 + corredor UEL/IAP
  → falha das buscas por nome exato
  → mecanismo/cultura como nova âncora
  → identificador CMRP 4490
  → cadeia strain–processo–formulação
  → contraste entre strains, autores e instituições
  → corredor UEL multi-strain
  → frontier futura e parada natural
```

A operação adaptativa central foi **mudar a representação quando a unidade atual deixava de produzir ganho informacional**. A investigação não insistiu em uma narrativa única: manteve Ag75, Ag109, CMRP 4490, CMRP 4489 e LABIM22 separados.

## Resultados e limites

### Observado

- A busca exata por Ag75 e Ag109 não retornou família brasileira no filtro utilizado.
- A reformulação por mecanismo/cultura abriu famílias brasileiras, incluindo CMRP 4490 e LABIM22.
- A família CMRP 4490 e o artigo de 2021 compartilham o identificador da strain e apresentam continuidade pública de instituição/nomes, com variação nominal preservada.
- O contraste bibliográfico mostrou um corredor UEL/IAP envolvendo múltiplas strains e temas.

### Inferido

- Existe um corredor institucional multi-strain com continuidade entre caracterização, aplicação e processo.
- CMRP 4490 é uma âncora mais informativa que a recuperação nominal de Ag75/Ag109 para investigar processo e formulação.

### Ainda não demonstrado

- Que todas as strains pertencem ao mesmo projeto.
- Que existe uma progressão temporal única de caracterização para formulação/bioprocesso.
- Validade, escopo ou liberdade de operação de qualquer patente.
- Eficácia, adoção comercial ou existência de produto de mercado.

## Parada natural

O ciclo para na versão de estado 6. A próxima unidade de informação exigiria uma escolha nova: auditoria de texto integral/claims, ampliação deliberada das fontes, ordenação temporal sistemática ou investigação institucional mais profunda. Essas perguntas foram preservadas em `NEXT_FRONTIER_V1.json`, não executadas silenciosamente.

## Provenance

A reconstrução está ancorada em `AUTONOMOUS_INVESTIGATION_V1_STATE_0.json`, `AUTONOMOUS_INVESTIGATION_V1_FRONTIER_0.md`, `AUTONOMOUS_INVESTIGATION_V1_CYCLE_01_EVIDENCE.md`, no pacote público `autonomous_cycles/PATENT-ASIE-2026-08-21-001/` e nos quatro arquivos brutos metadata-only em `raw_v4/`. O manifesto computável registra hashes e caminhos relativos.
