# Ingestion Contract V0

## Objetivo

Coletar um primeiro mapa heterogêneo de sinais em bioinsumos e biocontrole agropecuário, sem baixar arquivos científicos, sem exigir classificação semântica antes da captura e sem transformar coincidência nominal em relação tecnológica.

## Unidade de registro

Cada resposta será preservada como um registro metadata-only com `source`, `source_url`, `query`, `retrieved_at`, `http_status`, `raw_hash`, `source_id`, `title`, `description_or_abstract`, `dates`, `actors`, `institutions`, `geography`, `classifications`, `identifiers`, `license_or_access`, `raw_fields` e `status`.

## Tipos de objeto

A ingestão aceita `patent`, `work`, `actor`, `institution`, `application_signal` e `relation_candidate`. Os objetos não precisam estar completos para entrar no inventário; ausência vira campo vazio ou `unknown`, preservando a origem.

## Regras de captura

A coleta inicial é ampla. Queries em português e inglês são permitidas. Resultados duplicados entre fontes não são descartados na captura; recebem uma chave de origem e serão deduplicados depois por identificador, DOI, número de publicação ou combinação de título/ano/ator.

Nenhum PDF, texto integral de patente, sequência biológica, arquivo de dataset ou anexo será baixado nesta fase. Apenas respostas de metadata e os campos devolvidos pelas APIs serão preservados.

## Estados operacionais

`captured` significa que a fonte respondeu e o registro foi salvo. `partial` significa que a resposta foi válida, mas campos relevantes faltaram. `blocked` significa que a fonte exigiu autenticação, excedeu limite ou não respondeu. `candidate` é apenas um rótulo de triagem e não equivale a relevância comprovada. `next_candidate` registra fonte, campo ou expansão que exige próxima rodada.

## Provenance

Cada lote terá manifest com URL, parâmetros, timestamp UTC, status HTTP, hash SHA-256 da resposta, quantidade de registros e erro textual quando houver. A coleta não será considerada perdida só porque uma fonte está bloqueada.

## Primeiro escopo

Subdomínio: bioinsumos, inoculantes, biocontrole, biopesticidas, bioestimulantes microbianos e promoção de crescimento vegetal.

Período de interesse: 2010–2026, sem excluir registros fora do período quando a fonte os retornar.

Geografia: Brasil como eixo, com literatura e patentes internacionais mantidas para comparação.
