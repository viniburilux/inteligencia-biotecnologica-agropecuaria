# Autonomous Investigation V1 — Frontier 0

## Estado de partida

O estado inicial é `AUTONOMOUS_INVESTIGATION_V1_STATE_0.json`, sobre o corpus `normalized_v2` no commit `fabfbc1f033531318b3e66cd9e36dd031f14547a`. A leitura é metadata-only; nenhum notebook, PDF, sequência ou dado científico foi executado ou baixado.

## Como os candidatos foram gerados

Os candidatos abaixo vieram de coocorrências observadas, títulos e consultas já presentes no corpus, além de assimetrias entre densidade do sinal e especificidade da evidência. Eles são caminhos de investigação, não conclusões.

| Candidato | Sinal observado | Ganho potencial | Risco atual |
|---|---|---|---|
| `Bacillus velezensis` strain `Ag75` | Um título concreto combina biocontrole, solubilização de fosfato, promoção de crescimento, milho e soja. | A âncora de strain permite testar se a ponte é isolada ou abre uma cadeia técnica verificável. | Pode ser apenas um estudo único sem continuidade patentária ou institucional. |
| Microrganismos remodelados para fixação de nitrogênio | Coocorrência entre fixação de nitrogênio, saúde radicular, milho e formulação. | Pode revelar uma ponte entre mecanismo biológico e formulação/aplicação. | O sinal aparece em poucos registros e pode vir de busca patentária ruidosa. |
| `Trichoderma` + fermentação + enzimas + promoção de crescimento | Sinal denso e transversal em múltiplas aplicações. | Pode conectar agricultura e bioprocessos industriais. | Trilha já muito explorada; novas buscas amplas têm risco de baixo ganho marginal. |
| Inoculante + saúde radicular + monitoramento/ carbono | Um resultado de patente agrega muitos termos de aplicação. | Pode revelar uma combinação aplicada inesperada. | O texto parece snippet de patente e pode ser um pacote lexical, não uma cadeia técnica. |
| Microalgas + resíduos industriais + fertilizante | Ponte anterior entre carbono, resíduos e aplicação agrícola. | Pode revelar uma cadeia de valorização de resíduos. | A literatura anterior ficou genérica; risco elevado de repetição sem ganho. |

## Seleção do primeiro ciclo

**Pergunta selecionada:**

> A âncora `Bacillus velezensis` strain `Ag75`, que aparece combinando biocontrole, solubilização de fosfato e promoção de crescimento em milho e soja, abre uma cadeia de evidência independente e específica — ou é apenas um registro isolado no corpus?

**Por que esta pergunta venceu:** ela reduz ambiguidade usando uma entidade concreta, testa uma ponte com quatro sinais aplicados e não repete uma busca ampla já saturada. A investigação pode terminar em aprofundamento, reformulação por mecanismo/organismo/cultura ou estacionamento, conforme o resultado.

**Plano de fonte:** uma busca patentária metadata-only orientada pela strain e uma busca bibliográfica metadata-only orientada pelo título/strain. O resultado de cada modalidade será comparado; não haverá download de texto completo.

**Critério de parada do ciclo:** se ambas as modalidades forem vazias ou apenas genéricas, registrar a trilha como bloqueada/estacionada e selecionar o próximo candidato. Se surgir identificador, entidade, instituição ou mecanismo novo, transformar esse sinal na próxima pergunta em vez de retornar à busca ampla.
