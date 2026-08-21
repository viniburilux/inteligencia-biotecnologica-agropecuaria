# Radiografia Exploratória V0

**Laboratório:** Inteligência Biotecnológica Agropecuária  
**Corpus de partida:** 379 obras/registros normalizados  
**Gerado em:** 2026-08-21T05:08:13.832002+00:00  
**Modo:** exploratório, metadata-only

## O que apareceu primeiro

O corpus já se comporta como uma rede de **tecnologias, organismos, processos, atores e aplicações**, e não como uma lista homogênea de documentos. A estrutura mais forte da rodada atual é uma bifurcação entre **capacidade local de produção e controle de bioinsumos** e **presença de plataformas internacionais protegidas no Brasil**. Essa bifurcação é um padrão de proveniência e vocabulário, não uma conclusão sobre nacionalidade de toda a tecnologia.

O segundo sinal forte é a formação de uma trilha de **fixação de nitrogênio** que combina microrganismos, genética, formulação, estabilidade e liberação. O terceiro é a transversalidade de **Trichoderma**, que aparece em contextos de biocontrole, produção, enzimas, formulação e carbono. O quarto é metodológico: o vocabulário muda drasticamente o recall. `biological control + BR` retorna 56.223 resultados observados, enquanto `bioinput + BR` retorna 49; a diferença tornou o próprio vocabulário um objeto de investigação.

## A. Clusters operacionais encontrados

Os clusters abaixo são agrupamentos exploratórios baseados em termos e padrões observados no corpus. Um registro pode pertencer a mais de um cluster. O arquivo [`cluster_memberships_v0.jsonl`](cluster_memberships_v0.jsonl) preserva a ligação de cada membership com título, query e proveniência.

| Cluster | Descrição | Registros | Distribuição por fonte |
| --- | --- | --- | --- |
| C06_scientific_crop_context | Literatura, culturas e contexto agronômico | 212 | openalex: 112, crossref: 93, google_patents: 7 |
| C02_bioinputs_nutrition | Bioinsumos, inoculantes e nutrição biológica | 188 | openalex: 79, crossref: 74, google_patents: 35 |
| C01_biocontrol_biopesticide | Biocontrole, biopesticidas e sanidade vegetal | 141 | crossref: 66, openalex: 56, google_patents: 19 |
| C05_trichoderma_cross_context | Trichoderma como organismo transversal | 53 | openalex: 21, google_patents: 17, crossref: 15 |
| C03_nitrogen_platform | Fixação de nitrogênio e plataforma microbiana | 47 | crossref: 27, openalex: 13, google_patents: 7 |
| C00_unclassified_current_rules | Sem correspondência nas regras atuais | 31 | google_patents: 13, crossref: 10, openalex: 8 |
| C04_formulation_quality | Fermentação, formulação e monitoramento de qualidade | 9 | google_patents: 5, crossref: 3, openalex: 1 |

O cluster `C00_unclassified_current_rules` representa registros que não encontraram correspondência nas regras atuais. Ele não significa irrelevância; representa o espaço onde o corpus pode estar indicando uma taxonomia ainda ausente.

## B. Hubs e atores relevantes

### Atores por relações observadas

| Ator | Relações | Fonte | Papéis |
| --- | --- | --- | --- |
| Pivot Bio | 6 | google_patents | assignee |
| Fernando Ferrari Putti | 3 | openalex |  |
| Mariangela Hungría | 3 | openalex |  |
| L. S. AMARAL | 3 | crossref |  |
| E. O. ARAÚJO | 3 | crossref |  |
| Frederico Keller | 3 | google_patents | inventor, assignee |
| Syngenta | 3 | google_patents | assignee |
| Sean Farmer | 3 | google_patents | inventor |
| Alvin Tamsir | 3 | google_patents | inventor |
| João Pedro dos Santos | 2 | openalex |  |
| Ana Laura Paula de Oliveira | 2 | openalex |  |
| Leonardo Elias Ferreira | 2 | openalex |  |
| Eliziete Pereira de Souza | 2 | openalex |  |
| Mariane Carvalho Vidal | 2 | openalex |  |
| Ruth Rebeca Bonilla Buitrago | 2 | openalex |  |
| Gillyene Bortoloti | 2 | openalex |  |
| Renata Martins Sampaio | 2 | openalex |  |
| Paulo Teixeira Lacava | 2 | openalex |  |
| V. C. da MENDES | 2 | openalex |  |
| Ana Paula Gramulha Garcia | 2 | openalex |  |

### Instituições por relações observadas

| Instituição | Relações | Fonte |
| --- | --- | --- |
| Brazilian Agricultural Research Corporation | 14 | openalex |
| Universidade de São Paulo | 7 | openalex |
| Pivot Bio | 6 | google_patents |
| Universidade Estadual Paulista (Unesp) | 4 | openalex |
| Universidade Estadual de Londrina | 4 | openalex |
| Ministério da Agricultura | 3 | openalex |
| Universidade Federal de Viçosa | 3 | openalex |
| Universidade Federal da Grande Dourados | 3 | openalex |
| North-West University | 3 | openalex |
| University of Nairobi | 3 | openalex |
| Centre National de la Recherche Scientifique | 3 | openalex |
| Syngenta | 3 | google_patents |
| Horta (Italy) | 2 | openalex |
| Instituto Tecnológico de Costa Rica | 2 | openalex |
| Colombian Corporation for Agricultural Research - AGROSAVIA | 2 | openalex |
| Universidade Federal Rural do Rio de Janeiro | 2 | openalex |
| Instituto Biológico | 2 | openalex |
| Universidade Federal de Santa Maria | 2 | openalex |
| Instituto Federal de Educação, Ciência e Tecnologia do Pará | 2 | openalex |
| Universidade Federal Rural da Amazônia | 2 | openalex |

Os rankings acima contam relações presentes no inventário. Eles não são ranking de mercado, qualidade, titularidade econômica ou impacto.

### Atores que atravessam mais de uma camada

| Nome canônico | Fontes | Relações | Variações observadas |
| --- | --- | --- | --- |
| Fernando Ferrari Putti | crossref, openalex | 4 | Fernando Ferrari Putti |
| Gillyene Bortoloti | crossref, openalex | 4 | Gillyene Bortoloti |
| Renata Martins Sampaio | crossref, openalex | 4 | Renata Martins Sampaio |
| Ana Laura Paula de Oliveira | crossref, openalex | 3 | Ana Laura Paula de Oliveira |
| Bernard R. Glick | crossref, openalex | 3 | Bernard R. Glick |
| Eliziete Pereira de Souza | crossref, openalex | 3 | Eliziete Pereira de Souza |
| João Pedro dos Santos | crossref, openalex | 3 | João Pedro dos Santos |
| Leonardo Elias Ferreira | crossref, openalex | 3 | Leonardo Elias Ferreira |
| Ajar Nath Yadav | crossref, openalex | 2 | Ajar Nath Yadav |
| Ana Caroline Batista Da Silva | crossref, openalex | 2 | Ana Caroline Batista Da Silva; Ana Caroline Batista da Silva |
| Corporación Colombiana de Investigación Agropecuaria | google_patents, openalex | 2 | Corporación Colombiana de Investigación Agropecuaria |
| Giovana Schneider | crossref, openalex | 2 | Giovana Schneider |
| Giselle Silva de Souza | crossref, openalex | 2 | Giselle Silva de Souza |
| Jeferson Klein | crossref, openalex | 2 | Jeferson Klein |
| João Luciano de Andrade Melo Júnior | crossref, openalex | 2 | João Luciano de Andrade Melo Júnior |
| Luan Danilo Ferreira de Andrade Melo | crossref, openalex | 2 | Luan Danilo Ferreira de Andrade Melo |
| Marília Alves Grugiki | crossref, openalex | 2 | Marília Alves Grugiki |
| Miriam Hiroko Inoue | crossref, openalex | 2 | Miriam Hiroko Inoue |
| Naima da Trindade Coelho | crossref, openalex | 2 | Naima da Trindade Coelho |
| Pooja Singh | crossref, openalex | 2 | Pooja Singh |

## C. Tecnologias transversais

| Termo | Clusters atravessados | Clusters | Obras |
| --- | --- | --- | --- |
| promocao_crescimento | 3 | C02_bioinputs_nutrition, C03_nitrogen_platform, C06_scientific_crop_context | 38 |
| fixacao_nitrogenio | 2 | C02_bioinputs_nutrition, C03_nitrogen_platform | 4 |
| nematoide | 2 | C01_biocontrol_biopesticide, C06_scientific_crop_context | 14 |
| solubilizacao_fosfato | 2 | C02_bioinputs_nutrition, C03_nitrogen_platform | 4 |

A transversalidade mais concreta não é um único produto; é a recorrência de uma mesma capacidade ou organismo em diferentes camadas. `fungo` atravessa biocontrole, contexto agronômico, formulação e o cluster de Trichoderma. `promocao_crescimento` e `inoculante` conectam nutrição, nitrogênio e contexto agronômico. Os próximos passos devem separar recorrência lexical de conexão tecnológica efetiva.

### Organismos em múltiplos contextos

| Organismo/entidade | Obras | Clusters | Fontes |
| --- | --- | --- | --- |
| bacillus | 23 | 6 | openalex: 7, crossref: 5, google_patents: 11 |
| rhizobium | 12 | 6 | openalex: 2, crossref: 1, google_patents: 9 |
| bacillus thuringiensis | 9 | 6 | openalex: 1, crossref: 1, google_patents: 7 |
| trichoderma | 21 | 5 | openalex: 4, crossref: 5, google_patents: 12 |
| rhizobacteria | 8 | 4 | openalex: 3, crossref: 5 |
| pseudomonas | 4 | 4 | openalex: 1, crossref: 2, google_patents: 1 |
| yeast | 4 | 4 | openalex: 2, google_patents: 2 |
| metarhizium | 1 | 2 | openalex: 1 |
| clostridium | 1 | 1 | google_patents: 1 |

## D. Sinais brasileiros observados

Entre os 71 registros patentários, a classificação conservadora identificou **6** com marcadores institucionais ou organizacionais brasileiros explícitos no material capturado. Os sinais mais fortes estão associados a USP, UEBA, MCTI/Museu Paraense Emílio Goeldi, APTA, GI, Dosaggio e sistemas de produção ou controle de qualidade de bioinputs. Isso é um sinal de presença institucional no snippet, não prova de titularidade completa, origem de todos os inventores ou maturidade comercial.

## E. Sinais internacionais com presença BR

A mesma regra identificou **32** registros com atores globais explícitos e publicação no contexto BR, incluindo famílias ou organizações associadas a Pivot Bio, BASF, Syngenta, Monsanto, Bayer, Pioneer, Locus, Novozymes, Terragen e outras. O resultado sustenta uma trilha de investigação sobre tecnologias internacionais que chegam ao Brasil, mas não permite medir proteção de mercado ou liberdade de operação.

### Estados de origem patentária usados nesta radiografia

| Estado | Registros |
| --- | --- |
| origin_unresolved | 33 |
| international_presence_in_BR | 32 |
| brazilian_signal_observed | 6 |

Os **33** registros em `origin_unresolved` permanecem deliberadamente sem classificação de origem. A ausência de evidência é mantida como estado útil.

## F. Anomalias, concentrações e padrões inesperados

| Tipo | Evidência | Leitura operacional |
| --- | --- | --- |
| Recall amplo com captura pequena | biological control + BR | 56.223 resultados observados e 7 registros capturados; vocabulário amplo e pouco seletivo na primeira página. |
| Corpus pequeno e denso | bioinput + BR / bioinsumo + BR | 49–50 resultados observados e 9 registros capturados em cada trilha; aparecem produção, fermentação, biorreatores e monitoramento. |
| Concentração de plataforma | fixação de nitrogênio + BR | 8.956 resultados observados; a primeira página concentrou famílias com microrganismos, genes, formulação e liberação de nitrogênio. |
| Ruído lexical | Bacillus thuringiensis + BR | 14.887 resultados observados; a primeira página mistura agentes biológicos com patentes químicas que apenas mencionam a espécie. |
| Ponte organismo-processo | Trichoderma | O organismo aparece em biocontrole, produção, enzimas, formulação e carbono na amostra capturada. |

## G. Lacunas e caminhos de investigação

| Lacuna | O que o corpus mostra | Caminho |
| --- | --- | --- |
| Sinal regulatório explícito | Nenhum termo de regulação, registro, avaliação ou conformidade foi normalizado como sinal de aplicação na rodada atual. | Executar NQ20 em Crossref e expandir para fontes regulatórias públicas. |
| Resolução de família patentária | As obras patentárias estão normalizadas por publicação e ainda não foram agrupadas em famílias INPADOC ou equivalentes. | Consultar dados de família em rodada própria, mantendo publicação e prioridade separadas. |
| Origem institucional brasileira completa | A classificação local usa apenas marcadores explícitos presentes no snippet/ator; muitos registros permanecem como origem não resolvida. | Expandir busca de titular/inventor e cruzar instituições com fonte oficial, sem inferir origem pelo filtro BR. |
| Eficácia e adoção | O corpus metadata-only não contém evidência suficiente sobre desempenho agronômico, registro comercial ou adoção. | Criar trilha posterior com ensaios, registros e fontes regulatórias, sem misturar com descoberta patentária. |

## H. Recall, densidade e qualidade das consultas

| Consulta | Resultados observados | Capturados | Únicos no inventário | Com sinal | Taxa de sinal |
| --- | --- | --- | --- | --- | --- |
| bioinput + BR | 49 | 9 | 9 | 6 | 0.667 |
| bioinsumo + BR | 50 | 9 | 9 | 6 | 0.667 |
| inoculante + BR | 889 | 7 | 7 | 5 | 0.714 |
| biocontrole + BR | 1186 | 7 | 7 | 5 | 0.714 |
| Rhizobium + BR | 3402 | 9 | 9 | 4 | 0.444 |
| microbial inoculant + BR | 4975 | 10 | 10 | 7 | 0.7 |
| Trichoderma + BR | 6524 | 10 | 10 | 6 | 0.6 |
| biofertilizante + BR | 6633 | 7 | 7 | 4 | 0.571 |
| biopesticida + BR | 6712 | 7 | 7 | 3 | 0.429 |
| fixação de nitrogênio + BR | 8956 | 7 | 7 | 4 | 0.571 |
| Bacillus thuringiensis + BR | 14887 | 7 | 7 | 2 | 0.286 |
| biological control + BR | 56223 | 7 | 7 | 5 | 0.714 |

As consultas com recall mais amplo e baixa seletividade são candidatas a reformulação lexical. As consultas pequenas e densas — especialmente `bioinput`, `bioinsumo` e combinações de processo — são candidatas a expansão por termos adjacentes, atores e organismos.

## Próximo movimento: consultas derivadas

A lista completa está em [`next_queries_v0.json`](next_queries_v0.json). Ela contém 20 consultas ranqueadas pelo padrão encontrado, com bloco, evidência de origem, propósito, sinal esperado e ambiguidade a resolver. O próximo ciclo deve começar pelos blocos **B1 Trichoderma transversal**, **B2 plataforma de nitrogênio** e **B3 produção local/qualidade**, antes de ampliar consultas de maior ruído.

## Referências das páginas patentárias

[1]: https://patents.google.com/?q=(bioinsumo)&country=BR — Google Patents, consulta `bioinsumo + BR`.
[2]: https://patents.google.com/?q=(biocontrole)&country=BR — Google Patents, consulta `biocontrole + BR`.
[3]: https://patents.google.com/?q=(inoculante)&country=BR — Google Patents, consulta `inoculante + BR`.
[4]: https://patents.google.com/?q=(biopesticida)&country=BR — Google Patents, consulta `biopesticida + BR`.
[5]: https://patents.google.com/?q=(biofertilizante)&country=BR — Google Patents, consulta `biofertilizante + BR`.
[6]: https://patents.google.com/?q=(Rhizobium)&country=BR — Google Patents, consulta `Rhizobium + BR`.
[7]: https://patents.google.com/?q=(Bacillus+thuringiensis)&country=BR — Google Patents, consulta `Bacillus thuringiensis + BR`.
[8]: https://patents.google.com/?q=(Trichoderma)&country=BR — Google Patents, consulta `Trichoderma + BR`.
[9]: https://patents.google.com/?q=(fixa%C3%A7%C3%A3o+de+nitrog%C3%AAnio)&country=BR — Google Patents, consulta `fixação de nitrogênio + BR`.
[10]: https://patents.google.com/?q=(biological+control)&country=BR — Google Patents, consulta `biological control + BR`.
[11]: https://patents.google.com/?q=(bioinput)&country=BR — Google Patents, consulta `bioinput + BR`.
[12]: https://patents.google.com/?q=(microbial+inoculant)&country=BR — Google Patents, consulta `microbial inoculant + BR`.
