# Inventário Metadata-only V0

**Laboratório:** Inteligência Biotecnológica Agropecuária  
**Gerado em:** 2026-08-21T04:50:32.918823+00:00

O inventário V0 reúne **379 obras/registros**, **1345 atores**, **353 instituições**, **1854 relações** e **270 sinais de aplicação**. A mistura de fontes é: openalex=162, crossref=146, google_patents=71.

## Entregáveis

| Camada | Arquivo | Registros |
|---|---|---:|
| Obras e patentes | `normalized_v0/works_v0.jsonl` | 379 |
| Atores | `normalized_v0/actors_v0.jsonl` | 1345 |
| Instituições | `normalized_v0/institutions_v0.jsonl` | 353 |
| Relações | `normalized_v0/relations_v0.jsonl` | 1854 |
| Sinais de aplicação | `normalized_v0/application_signals_v0.jsonl` | 270 |
| Mapa computável | `signal_map_v0.json` | 1 |
| Mapa legível | `SIGNAL_MAP_V0.md` | 1 |

## Cobertura

O escopo de ingestão cobre bioinsumos, biocontrole, inoculantes, biofertilizantes, biopesticidas, fixação de nitrogênio, solubilização de fosfato, saúde radicular, fermentação e monitoramento de bioinputs. A camada patentária contém **71 registros de publicação BR normalizados**, deduplicados por identificador de publicação no corpus integrado.

## Proveniência e limites

Cada registro normalizado mantém referência ao manifesto, ao arquivo bruto e ao hash da captura. Os registros do Google Patents foram extraídos de páginas públicas de resultados e mantêm a consulta e o filtro de país BR. Nenhum PDF, documento integral, sequência, anexo ou dado científico foi baixado. Os artefatos são adequados para descoberta e organização de sinais; não devem ser usados isoladamente para conclusão jurídica, regulatória, comercial ou agronômica.

Para a leitura dos sinais, consulte [`SIGNAL_MAP_V0.md`](SIGNAL_MAP_V0.md). Para a cadeia de captura patentária, consulte [`PATENT_SOURCE_FINDINGS_V0.md`](PATENT_SOURCE_FINDINGS_V0.md).
