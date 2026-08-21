# Verificação inicial de fontes — Mapa V0

Data de consulta: 2026-08-21.

## INPI — Dados Abertos

Fonte oficial: https://www.gov.br/inpi/pt-br/acesso-a-informacao/dados-abertos

A página oficial informa que o INPI mantém uma seção de Dados Abertos, com plano de dados abertos vigente, bases programadas e uma página operacional de dados em https://dadosabertos.inpi.gov.br/. A existência do canal oficial foi confirmada. A página consultada não foi usada para afirmar, sem inspeção adicional, quais arquivos específicos, campos, licenças ou cobertura histórica estão atualmente disponíveis. Essas propriedades devem ser marcadas como `UNVERIFIED` até a captura direta dos catálogos/arquivos.

## EPO Open Patent Services (OPS)

Fonte oficial: https://www.epo.org/en/searching-for-patents/data/web-services/ops

A fonte oficial identifica o Open Patent Services como um web service da EPO para acesso a dados patentários brutos por interface XML padronizada e menciona autenticação OAuth. A página também expõe o OPS como caminho de intercâmbio de dados. Quotas, custos exatos, endpoints e cobertura por coleção não foram inferidos além do que a documentação oficial consultada sustenta; devem ser confirmados na documentação de desenvolvedores antes de um adapter público.

Portal de desenvolvedores: https://developers.epo.org/

## Embrapa AgroAPI

Fonte oficial: https://www.embrapa.br/agroapi

A página oficial descreve a AgroAPI como plataforma de APIs da Embrapa para tecnologias em agricultura digital e lista, entre outras, Agrofit, Agrotermos, Bioinsumos, BlueStar Sting e PlantAnnot. O acesso exige criação de conta e tokens. A própria página informa que Agrofit, Agrotermos, Bioinsumos, Blue Star Sting, Responde Agro, SmartSolos Expert e PlantAnnot têm acesso gratuito até 100 mil requisições por mês, sem necessidade de contrato; também informa que Agritec, ClimAPI e SATVeg têm regime freemium diferente, gratuito por um mês até 1.000 requisições por API. Isso deve ser tratado como condição de acesso da fonte, não como autorização automática para redistribuir os dados.

Loja de APIs Bioinsumos: https://www.agroapi.cnptia.embrapa.br/store/apis/info?name=Bioinsumos&version=v1&provider=agroapi

## Consequência para o laboratório

O mapa enviado é uma boa arquitetura de descoberta, mas a matriz de fontes ainda mistura fatos verificados, estimativas de cobertura, condições de licença e hipóteses de acesso. O primeiro commit de coleta deve registrar por fonte: URL, data de consulta, status de acesso, autenticação, termos/licença, campos efetivamente observados e limites. A recomendação operacional é começar com fontes abertas e diretamente testáveis, mantendo Lens e EPO OPS como `credential-gated`/`NEXT_CANDIDATE` até validação de acesso, e não depender deles para o primeiro corpus público.

## Status

- INPI Dados Abertos: `observed_source_channel`; arquivos/campos específicos ainda `UNVERIFIED`.
- EPO OPS: `observed_api_service`; OAuth e interface XML observados; quotas/licença operacional ainda precisam de validação específica.
- Embrapa AgroAPI: `observed_api_platform`; token necessário; APIs e regimes de acesso documentados na página oficial.
