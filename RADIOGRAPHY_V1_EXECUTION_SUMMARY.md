# Radiography V1 — Query Execution Summary

> This artifact links the 17 queries generated from the cumulative corpus to the searches actually executed. It is an execution log, not a conclusion about technology or market adoption.

Generated at: `2026-08-21T06:17:11.894839+00:00`  
Planned queries: **17**  
Executed: **17** — direct: 14; reformulated: 3  
Not found in execution manifests: **0**

| ID | Fonte | Trilha | Status | Volume observado | Registros retornados | Evidência operacional |
|---|---|---|---|---:|---:|---|
| Q01 | google_patents | local_trichoderma_bridge | executed | 2 | 1 | `raw_v2/google_patents_radiography_v1/radiography_q01_usp_trichoderma_harzianum_sophorolipid_brazil.jsonl` |
| Q02 | google_patents | local_bioreactor | executed_reformulated | 2 | 1 | `raw_v2/google_patents_radiography_v1/radiography_q02r_bacillus_velezensis_cmrp_4490_bioreactor_brazil.jsonl` |
| Q03 | google_patents | local_quality_onfarm | executed | 3 | 3 | `raw_v2/google_patents_radiography_v1/radiography_q03_simple_agro_bioinput_quality_control_brazil_patent.jsonl` |
| Q04 | google_patents | local_quality_onfarm | executed_reformulated | 1 | 1 | `raw_v2/google_patents_radiography_v1/radiography_q04r_solubio_bioinsumo_fermenta_o_produ_o_propriedade_rural.jsonl` |
| Q05 | google_patents | local_stability | executed | 66 | 3 | `raw_v2/google_patents_radiography_v1/radiography_q05_azospirillum_inoculant_polymer_stability_brazil.jsonl` |
| Q06 | google_patents | local_stability | executed | 94 | 5 | `raw_v2/google_patents_radiography_v1/radiography_q06_rhizobium_inoculant_polymer_shelf_life_brazil.jsonl` |
| Q07 | google_patents | local_nutrition | executed | 17 | 6 | `raw_v2/google_patents_radiography_v1/radiography_q07_bacillus_megaterium_phosphorus_biofertilizer_brazil.jsonl` |
| Q08 | google_patents | international_platform | executed | 2 | 2 | `raw_v2/google_patents_radiography_v1/radiography_q08_pivot_bio_nitrogen_fixation_phosphorus_formulation.jsonl` |
| Q09 | google_patents | international_platform | executed | 27 | 5 | `raw_v2/google_patents_radiography_v1/radiography_q09_locus_phytase_phosphorus_microbial_agriculture.jsonl` |
| Q10 | google_patents | industrial_trichoderma | executed | 63 | 6 | `raw_v2/google_patents_radiography_v1/radiography_q10_novozymes_trichoderma_cellulase_fermentation_brazil.jsonl` |
| Q11 | google_patents | carbon_algae | executed | 2 | 2 | `raw_v2/google_patents_radiography_v1/radiography_q11_petrobras_microalgae_co2_fixation_fertilizer_brazil.jsonl` |
| Q12 | google_patents | carbon_algae | executed_reformulated | 1 | 1 | `raw_v2/google_patents_radiography_v1/radiography_q12r_microalga_cascalho_perfura_o_biofixa_o_fertilizante.jsonl` |
| Q13 | openalex | literature_local_bridge | executed | 16 | 10 | `raw_v2/openalex_followup/q13_trichoderma_sophorolipids_biocontrol_brazil.json` |
| Q14 | openalex | literature_stability | executed | 1601 | 10 | `raw_v2/openalex_followup/q14_microbial_inoculant_polymer_stability_nitrogen.json` |
| Q15 | openalex | literature_local_production | executed | 67 | 10 | `raw_v2/openalex_followup/q15_on_farm_bioinput_fermentation_brazil.json` |
| Q16 | openalex | literature_carbon | executed | 431 | 10 | `raw_v2/openalex_followup/q16_microalgae_co2_industrial_waste_fertilizer_brazil.json` |
| Q17 | openalex | literature_local_organism | executed | 210 | 10 | `raw_v2/openalex_followup/q17_bacillus_velezensis_biofertilizer_nematode_brazil.json` |

## Reformulações que abriram sinal

Q02, Q04 e Q12 tiveram resposta insuficiente na formulação inicial. As reformulações foram preservadas separadamente: `Bacillus velezensis CMRP 4490 bioreactor Brazil`, `Solubio bioinsumo fermentação produção propriedade rural` e `microalga cascalho perfuração biofixação fertilizante`. As três abriram registros metadata-only, incluindo a família Petrobras de fertilizante organomineral com cascalho de perfuração e biomassa de algas.

## Limites

Um resultado recuperado por filtro BR é presença em uma busca de patentes com contexto brasileiro; não é prova suficiente de origem, titularidade brasileira, validade, adoção, desempenho agronômico ou liberdade de operação. As lacunas e páginas insuficientes permanecem registradas.
