# Reconstrução Estrutural V1 — Corredor UEL–Bacillus

## Objetivo

Este artefato reconstrói a estrutura tecnológica que emergiu da Investigação Autônoma V1 a partir de evidências heterogêneas: literatura, patentes, repositório institucional, atores, instituições, strains, mecanismos, culturas, processos e formulações.

O objetivo não é afirmar que existe uma única plataforma, produto ou invenção. O objetivo é testar se a operação investigativa consegue montar uma representação reutilizável do corredor sem colapsar entidades distintas e sem transformar proximidade metadata-only em continuidade jurídica ou técnica.

A entrada foi congelada no estado `STATE_VERSION_6`, derivado de `normalized_v2`, com 763 obras, 2.680 atores, 767 instituições, 4.045 relações e 536 sinais de aplicação. Não houve nova coleta ampla nesta reconstrução.

## Resultado em uma frase

> A estrutura mais informativa não é uma linha única `strain → produto`; é um grafo de continuidade parcial em que diferentes strains atravessam nós de caracterização, mecanismos de ação, culturas e aplicações, enquanto CMRP 4490 possui a ponte mais específica entre literatura, processo em biorreator e formulação patentária.

## Estrutura reconstruída

```text
UEL / IAP / parceiros
        │
        ├── CMRP 4490 ── caracterização genômica/antifúngica
        │                   ├── promoção de crescimento
        │                   ├── rizobactéria / rizosfera
        │                   └── processo em biorreator agitado
        │                                  └── formulação
        │                                      ├── bionematicida
        │                                      └── inoculante
        │
        ├── LABIM22 ───── antagonismo contra fungos
        │                   └── controle de mofo branco em sementes de soja
        │                                  └── composição biofungicida patentária
        │
        ├── Ag75 ──────── biocontrole + solubilização de fosfato
        │                   └── promoção de crescimento em milho e soja
        │
        ├── Ag109 ─────── biocontrole contra nematoides e Sclerotinia
        │                   └── trabalho genômico / caracterização
        │
        └── CMRP 4489 / LABIM40 / CMRP 6330
                            └── nós de continuidade a auditar
```

As linhas acima representam relações de investigação. Elas não significam que todas as strains pertencem ao mesmo projeto, que compartilham uma formulação ou que formam uma única família comercial.

## Camadas tecnológicas observadas

| Camada | Conteúdo observado | Estado |
|---|---|---|
| Identidade biológica | *Bacillus velezensis* CMRP 4490, LABIM22, Ag75, Ag109 e outras strains CMRP/LABIM | Observado; manter entidades separadas |
| Caracterização | Genoma, atividade antifúngica, antagonismo e estudos de rizosfera | Observado em literatura/repositório |
| Mecanismos | Antifúngico, biocontrole, solubilização de fosfato, promoção de crescimento, controle de nematoides | Observado em títulos, palavras-chave, abstracts e facetas |
| Cultura/contexto | Soja, milho, sementes, rizosfera, fungos fitopatogênicos e nematoides | Observado em registros específicos |
| Processo | Fermentação em biorreator de tanque agitado; controle de agitação, temperatura, pH, espuma e oxigênio dissolvido | Observado diretamente na página da família BR102024016682A2 |
| Formulação/aplicação | Bionematicida e/ou inoculante; composição biofungicida | Observado em famílias patentárias distintas |
| Instituição | UEL como recorrência principal; IAP e Embrapa aparecem em parte da literatura | Observado; corredor institucional é inferência agregada |
| Temporalidade | LABIM22 2020; CMRP 4490 2021; Ag75 2022; Ag109 2024; família CMRP 4490 publicada/apresentada em 2024 | Ordenação metadata-only, não progressão provada |

## Relações de maior valor

### CMRP 4490: literatura → processo → formulação

A relação mais forte liga o artigo `10.3389/fmicb.2020.618415`, publicado em 2021, à família `BR102024016682A2`. O mesmo identificador de strain aparece nos dois lados. A literatura descreve atividade antifúngica e promoção de crescimento; a família patentária descreve processo fermentativo em biorreator de tanque agitado e formulações para bionematicida e/ou inoculante. UEL aparece como afiliação no artigo e como requerente da patente; Admilton Gonçalves de Oliveira aparece com variação nominal entre os registros.

Classificação: **continuidade de metadata/texto observada**. A relação não prova validade da patente, eficácia, adoção comercial, liberdade de operação ou identidade legal perfeita do nome do autor.

### LABIM22: repositório institucional → aplicação → patente

O item `123456789/18265`, de 2020, descreve antagonismo da strain LABIM22 contra fungos fitopatogênicos e controle de mofo branco em sementes de soja. A família `BR102020013481A2` trata de composição biofungicida envolvendo LABIM22 e UEL. O repositório menciona pedido de patente em processo para meio/formulação.

Classificação: **continuidade pública observada entre strain, aplicação e família patentária**, com a ressalva de que o abstract do repositório não substitui auditoria de claims nem estabelece a identidade do projeto completo.

### Ag75: mecanismo/cultura → literatura específica → corredor institucional

Ag75 aparece em artigo de 2022 como agente multifuncional de biocontrole, solubilização de fosfato e promoção de crescimento em milho e soja. A busca patentária exata por Ag75 não retornou família brasileira no filtro usado. O sinal bibliográfico, entretanto, abriu a conexão com Ag109 e UEL/IAP.

Classificação: **âncora literária observada; continuidade patentária não demonstrada**.

### Ag109: entidade nova → mecanismo específico → reformulação

Ag109 apareceu como strain relacionada em trabalho de genoma/biocontrole contra nematoides e *Sclerotinia sclerotiorum*. A busca patentária exata por Ag109 também não retornou família brasileira no filtro usado. O papel adaptativo do sinal foi deslocar a representação de “nome exato da strain” para mecanismo, cultura, instituição e corredor de pesquisa.

Classificação: **entidade e mecanismos observados; conexão com a família CMRP 4490 não demonstrada**.

## O que a temporalidade permite e não permite

A ordenação disponível sugere uma sequência potencial:

```text
2020  LABIM22: antagonismo e biocontrole em sementes de soja
  ↓
2021  CMRP 4490: genoma, atividade antifúngica e promoção de crescimento
  ↓
2022  Ag75: biocontrole, fosfato e promoção de crescimento em milho/soja
  ↓
2024  Ag109: genoma, nematoides e Sclerotinia
  ↓
2024  CMRP 4490: biorreator, fermentação e formulação
```

Essa sequência é uma **ordenação de registros**, não uma história causal. Não se pode afirmar, com o estado atual, que LABIM22 levou a CMRP 4490, que Ag75 levou a Ag109, que houve desenvolvimento linear de caracterização até formulação ou que todas as linhas fazem parte de um único programa.

O valor da temporalidade é outro: ela permite formular uma pergunta estrutural mais precisa — se o corredor UEL mostra, em múltiplos casos, uma passagem recorrente de caracterização biológica para controle de processo e formulação — sem assumir a resposta.

## Separação epistemológica

| Categoria | Conteúdo |
|---|---|
| **Observado** | Identificadores, títulos, anos, autores, instituições, strains, mecanismos e modalidades presentes nos registros; ausência de resultado para Ag75/Ag109 em buscas exatas BR; família CMRP 4490 com biorreator e formulação. |
| **Inferido** | Existe um corredor institucional UEL multi-strain; CMRP 4490 é uma ponte mais específica entre biologia e processo/formulação; LABIM22 forma um corredor separado de aplicação biofungicida. |
| **Hipótese** | A temporalidade pode revelar progressão recorrente de caracterização para formulação/bioprocesso; a equipe UEL pode reaparecer em múltiplas strains e tecnologias. |
| **Lacuna** | Claims, eventos legais, texto integral, identidade nominal definitiva, continuidade de projeto, desempenho, adoção e liberdade de operação. |
| **Oportunidade** | Construir futuramente uma camada de relações que preserve entidades distintas e ligue evidência biológica a processo, formulação e aplicação. |
| **Não sustentado** | Uma única plataforma UEL, um único produto, eficácia comercial, relação de propriedade entre famílias ou equivalência entre strains. |

## Reutilização da estrutura

A estrutura é reutilizável porque não depende dos nomes `Bacillus`, `UEL` ou `CMRP`. Ela separa:

```text
entidade biológica ou técnica
→ evidência de caracterização
→ mecanismo ou propriedade
→ contexto de aplicação
→ processo de produção
→ formulação ou modalidade de uso
→ documento/família
→ relação e limite
```

Em outro domínio, a entidade pode ser um dataset, sensor, material, território, modelo ou objeto experimental. O importante é preservar o tipo de relação e a modalidade da evidência. Uma ponte “artigo → patente” pode ser marcada como continuidade de metadata; uma ponte “resultado → nova pergunta” pode ser marcada como transição investigativa; uma ponte “mesmo ator” deve permanecer como candidato de identidade até resolução suficiente.

## Teste de reutilização em outros domínios

A estrutura foi testada contra trajetórias já existentes de organoides, datasets públicos, SIGMINE/GhostWorks, patentes de mineração, embeddings de satélite e PNCP Bahia. O teste não fez nova coleta e não tentou forçar os nós agropecuários nesses domínios. Ele verificou se os papéis estruturais podiam ser preservados quando os objetos e artefatos mudavam.

O resultado foi positivo como **contrato de representação**, não como engine. A cadeia específica `strain → caracterização → mecanismo → aplicação → processo → formulação → patente` precisa ser generalizada para:

```text
objeto/entidade
→ propriedade ou caracterização observada
→ mecanismo, comportamento ou explicação operacional
→ contexto de uso ou decisão
→ transformação, experimento ou processo
→ artefato/fonte produzido ou consultado
→ lacuna, bloqueio ou contradição
→ próxima decisão
```

Em organoides, o objeto foi sinal neural e o artefato foi um experimento com mudança de target. Em SIGMINE, o objeto foi território/embedding e o resultado foi um arquétipo de comportamento minerário. Em satélite, o processo foi computacional e o valor migrou do mapa para dados, lógica e interface. Em PNCP, o documento de origem ocupou o papel que a patente ocupa no Agro. Em patentes de mineração, o mapeamento foi quase isomórfico: material → propriedade/impureza → mecanismo → rota técnica → família patentária.

Isso sustenta uma segunda capacidade distinta da reformulação de perguntas:

```text
Capacidade 1: resultado → nova pergunta
Capacidade 2: evidências heterogêneas → estrutura → próxima decisão
```

A primeira transforma a pergunta. A segunda reorganiza o que foi encontrado, preserva a modalidade da evidência e mantém lacunas explícitas antes de decidir. O teste não demonstrou seleção automática, ranking de relações ou generalização universal. Para validá-la em outro domínio, seria necessário reconstruir a mesma estrutura em uma trajetória não agropecuária e medir se sete papéis permanecem preservados: objeto, propriedade, mecanismo/comportamento, contexto, transformação, artefato e lacuna/decisão.

O detalhamento dos mapeamentos está em `STRUCTURAL_REUSE_TEST_V1.md` e `STRUCTURAL_REUSE_TEST_V1.jsonl`.

## Próxima frontier estrutural

1. **Auditar a recorrência da equipe UEL** em múltiplas strains e tecnologias, mantendo CMRP 4490, LABIM22, Ag75, Ag109, CMRP 4489, LABIM40 e CMRP 6330 separados.
2. **Testar aliases de LABIM22** em fontes públicas, sem inferir que grafia alternativa equivale a strain diferente ou à mesma entidade.
3. **Ordenar literatura e patentes por data e camada tecnológica**, procurando padrões de caracterização → mecanismo → aplicação → processo/formulação.
4. **Repetir o esquema em uma trajetória não agropecuária já existente**, para verificar se a estrutura funciona como contrato de representação e não apenas como descrição do corredor UEL.

## Provenance principal

- Estado: `autonomous_cycles/PATENT-ASIE-2026-08-21-001/state_final.json`.
- Relações: `autonomous_cycles/PATENT-ASIE-2026-08-21-001/new_relations.json`.
- Registros-chave: `autonomous_cycles/PATENT-ASIE-2026-08-21-001/key_records_v1.json`.
- Log de ciclos: `AUTONOMOUS_INVESTIGATION_V1.jsonl`.
- Evidência dos ciclos: `AUTONOMOUS_INVESTIGATION_V1_CYCLE_01_EVIDENCE.md`.
- Mapa executivo: `autonomous_cycles/PATENT-ASIE-2026-08-21-001/EXECUTIVE_MAP_UPDATE.md`.

## Limite desta reconstrução

Este artefato não implementa seleção adaptativa, não executa nova coleta, não baixa documentos científicos ou patentes, não revisa claims e não atribui valor comercial. Ele transforma evidências já coletadas em uma representação explícita para que a próxima pergunta possa ser escolhida sem confundir continuidade, proximidade e hipótese.

## Referências

[1]: https://patents.google.com/patent/BR102024016682A2/en "BR102024016682A2 — CMRP 4490"
[2]: https://doi.org/10.3389/fmicb.2020.618415 "Genomic Insights Into the Antifungal Activity and Plant Growth-Promoting Ability in Bacillus velezensis CMRP 4490"
[3]: https://patents.google.com/patent/BR102020013481A2/en "BR102020013481A2 — LABIM22"
[4]: https://repositorio.uel.br/handle/123456789/18265 "UEL repository item — LABIM22"
[5]: https://doi.org/10.1038/s41598-022-19515-8 "Bacillus velezensis strain Ag75"
[6]: https://github.com/viniburilux/inteligencia-biotecnologica-agropecuaria/tree/main "Laboratório público de Inteligência Biotecnológica Agropecuária"

---

**Status:** reconstrução estrutural metadata-only V1; não é conclusão legal, de eficácia, mercado ou propriedade intelectual.
