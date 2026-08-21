# Patent source findings V0

## Source

URL consultada: https://patents.google.com/?q=(biocontrole)&country=BR

Data de consulta: 2026-08-21.

## Observed

A página pública do Google Patents respondeu sem login e exibiu **1.186 resultados** para `biocontrole` com filtro de país `BR`. A página informa deduplicação por família e permite até 10 resultados por página. Também expõe um endpoint de download/consulta em `/xhr/query?url=...&download=true`, que deve ser testado como caminho de metadata, sem baixar PDFs.

A primeira página mostrou títulos, identificadores BR, prioridades, datas, inventores, depositantes e excertos. Exemplos observados:

- BR112021002698A2 — RNA-based biocontrol methods to protect plants against pathogenic bacteria and/or promote beneficial effects of symbiotic and commensal bacteria; inventor Lionel Navarro; depositante Centre National De La Recherche Scientifique.
- BR112020016351A2 — Microbial compositions for the prevention or reduction of the growth of plant pathogenic fungi; inventor Robert McBride; depositante Boost Biomes, Inc.
- BR112021005052A2 — Methods and compositions to improve phosphate solubilization; inventor Sarah Bloch; depositante Pivot Bio, Inc.
- BR112021010947A2 — Polymer compositions with improved stability for microbial nitrogen fixing; inventor Farzaneh Rezaei; depositante Pivot Bio, Inc.
- BR112020026771A2 — Agricultural compositions that understand remodeled nitrogen fixation microbes; inventor Mark Reisinger; depositante Pivot Bio, Inc.
- BR112020026676A2 — Guided microbial remodeling, a platform for the rational improvement of microbial species for agriculture; inventor Sarah Bloch; depositante Pivot Bio, Inc.
- BR112021000268A2 — Dynamic nitrogen release temporally and spatially driven by remodeled microbes; inventor Alvin Tamsir; depositante Pivot Bio, Inc.
- BR112020008002A2 — Gene targets for nitrogen fixation to enhance plant traits.
- BR112020022659A2 — Methods of applying one or more certain heteroaryl-1,2,4-triazole...
- BR112020008035A2 — Methods and compositions for enhancing genetically modified microbes that fix...

## Limits

Os resultados e excertos são metadata de descoberta. Não foram baixados PDFs, claims completas, sequências, anexos ou dados científicos. A página não prova validade, novidade, vigência, liberdade de operação ou relevância final. A filtragem por país indica presença/resultado relacionado ao Brasil, não necessariamente origem brasileira.

## Next technical step

Implementar um adapter privado para o endpoint `/xhr/query` com queries URL-encoded e paginação, salvando JSON bruto, URL final, timestamp e hash. Testar primeiro cinco sementes: `biocontrole`, `bioinsumo`, `inoculante`, `biopesticide`, `plant growth promoting bacteria`, com filtro BR quando suportado. Se o endpoint falhar, preservar o bloqueio e manter esta página como fonte de descoberta manual.

## Access event

Após a página de resultados funcionar, o endpoint de download `/xhr/query?...&download=true` respondeu HTTP 429 (Too Many Requests) tanto por requisição direta quanto pelo botão Download da página. O HTML da página de resultados continua sendo uma fonte pública de descoberta metadata-only; o download tabular fica registrado como `BLOCKED_RATE_LIMITED` e não será insistido neste lote.

Data do evento: 2026-08-21.


## Query: bioinsumo + BR

A página pública respondeu com **50 resultados**. A primeira página exibiu, entre outros:

- BR102020013946A2 — Nutrition manufacturing process for agricultural bio inputs and fertilizers for...; prioridade 2020-07-08; publicado 2022-01-18; inventor/depositante Frederico Keller.
- BR102021005600A2 — Microbial bio inputs, soil bioconditioners, production system, aerobic...; prioridade 2021-03-24; publicado 2022-09-27; inventor/depositante Antônio Reinaldo Lodo / Inovar Planejamento e Consultoria Agropecuária Eireli.
- BR102023006896A2 — Process for obtaining biofertilizer and product for reducing the population of...; depósito 2023-04-13; publicado 2024-10-22; inventora/depositante Camila Cruz de Oliveira Araújo.
- BR102024014113A2 — Bacterial Composition and Its Uses; depósito 2024-07-10; publicado 2026-01-21; inventora María Eugenia Guazzaroni; depositante Universidade de São Paulo.
- BR112018012451B1 — Composição biopesticida à base de vírus; prioridade 2015-12-21; publicado 2022-07-12; inventora Gloria Patricia Barrera Cubillos; depositante Corporación Colombiana de Investigación Agropecuaria.
- BR102023003698A2 — Bioinsumo à base de T. harzianum e soforolipídeos; depósito 2023-02-28; publicado 2024-09-10; inventor Thiago Moura Rocha; depositante Universidade de São Paulo.
- BR102021017152A2 — Sistema de produção de bioinsumos para propriedades rurais; prioridade 2021-08-30; publicado 2023-03-14; inventor/depositante Rafael Winterfeld Barbieri.

A página exibiu também inventores/depositantes e facetas, incluindo MCTI/Museu Paraense Emílio Goeldi, USP, Universidade do Estado da Bahia e Agência Paulista de Tecnologia dos Agronegócios.

URL: https://patents.google.com/?q=(bioinsumo)&country=BR
Data da consulta: 2026-08-21.


## Query: biocontrole + BR

A página pública respondeu com **1.186 resultados**. A primeira página exibiu sinais concentrados em biocontrole microbiano, solubilização de fosfato, fixação de nitrogênio e remodelamento microbiano, incluindo:

- BR112021002698A2 — RNA-based biocontrol methods to protect plants against pathogenic bacteria and/or promote beneficial effects of symbiotic and commensal bacteria; prioridade 2018-08-17; publicado 2021-08-10; Lionel Navarro / Centre National de la Recherche Scientifique.
- BR112020016351A2 — Microbial compositions for prevention or reduction of growth of plant pathogens; prioridade 2018-02-12; publicado 2020-12-15; Robert McBride / Boost Biomes, Inc.
- BR112021005052A2 — Methods and compositions to improve phosphate solubilization; prioridade 2018-09-21; publicado 2021-06-08; Sarah Bloch / Pivot Bio, Inc.
- BR112021010947A2 — Polymer compositions with improved stability for microbial nitrogen-fixing products; prioridade 2018-12-07; publicado 2021-08-31; Farzaneh Rezaei / Pivot Bio, Inc.
- BR112020026771A2 — Agricultural compositions using remodeled nitrogen-fixation microbes; prioridade 2018-06-27; publicado 2021-03-30; Mark Reisinger / Pivot Bio, Inc.
- BR112020026676A2 — Guided microbial remodeling for rational improvement of microbial species for agriculture; prioridade 2018-06-27; publicado 2021-08-03; Sarah Bloch / Pivot Bio, Inc.
- BR112021000268A2 — Dynamic nitrogen release driven by remodeled microbes; prioridade 2018-07-11; publicado 2021-05-11; Alvin Tamsir / Pivot Bio, Inc.

As facetas exibiram atores como BASF, Syngenta, Monsanto Technology, Bayer e Pioneer Hi-Bred. A consulta revela imediatamente um eixo tecnológico internacional que chega ao Brasil via famílias com publicação BR; isso não prova operação, comercialização ou validade no Brasil.

URL: https://patents.google.com/?q=(biocontrole)&country=BR
Data da consulta: 2026-08-21.


## Query: bioinsumo + BR (registro consolidado)

A busca retornou **50 resultados** e mostrou uma distribuição mais brasileira na primeira página, com registros nacionais BR102 e atores como MCTI/Museu Paraense Emílio Goeldi, Universidade do Estado da Bahia, Universidade de São Paulo, GI Indústria, Comércio e Tecnologia e Agência Paulista de Tecnologia dos Agronegócios.

Os oito resultados visíveis foram: BR102020013946A2, processo de fabricação de nutrição para bioinsumos e fertilizantes, Frederico Keller; BR102021005600A2, bioinsumos microbianos e biocondicionadores do solo, Antônio Reinaldo Lodo / Inovar Planejamento e Consultoria Agropecuária; BR102023006896A2, processo de obtenção de biofertilizante e produto para reduzir população de pragas, Camila Cruz de Oliveira Araújo; BR102024014113A2, Bacterial Composition and Its Uses, María Eugenia Guazzaroni / Universidade de São Paulo; BR112018012451B1, composição biopesticida à base de vírus, Gloria Patricia Barrera Cubillos / Agrosavia; BR102023003698A2, bioinsumo à base de T. harzianum e soforolipídeos, Thiago Moura Rocha / Universidade de São Paulo; BR102021017152A2, sistema de produção de bioinsumos para propriedades rurais, Rafael Winterfeld Barbieri; BR202021011674U2, processo para composição sólida de imobilizado microbiológico e método de monitoramento físico-químico de bioinsumos. Também apareceu BR102023023945A2, composição bioherbicida dessecante de contato.

Os snippets indicam aplicações em nutrição microbiana, biocondicionamento de solo, biofertilizantes, biopesticidas, fermentação de Trichoderma, produção na propriedade rural e monitoramento físico-químico. Estes são sinais de conteúdo de patente, não confirmação de produto comercial, eficácia ou status jurídico.

URL: https://patents.google.com/?q=(bioinsumo)&country=BR
Data da consulta: 2026-08-21.


## Query: inoculante + BR

A página respondeu com **889 resultados**. A primeira página combinou aplicações agrícolas, nutrição animal e tecnologias de formulação/veículo. Os registros visíveis foram:

BR102020006754A2 — Process for obtaining and application of water insolubles phosphate and ..., Frederico Keller, prioridade 2020-04-03, publicado 2021-10-13; o excerto menciona organismos inoculantes liofilizados associados a fosfato de amônio e magnésio. BR112020002927A2 — Use of inoculants and enzymes to increase nutrient release in animal diets, Shukun Yu / Dupont Nutrition Biosciences APS, prioridade 2017-08-14, publicado 2020-07-28. BR102020013946A2 — Nutrition manufacturing process for agricultural bio inputs and fertilizers, Frederico Keller, prioridade 2020-07-08, publicado 2022-01-18. BRPI1100001B1 — Process of obtaining solid vehicles for microbial inoculants from biological ..., Diva de Souza Andrade / Petrobras, prioridade 2011-01-04, publicado 2021-02-17. BR202020014385U2 — Technical provision introduced in inoculator kit, Tarike Yasuhiko Hoshino, prioridade 2020-07-14, publicado 2022-01-25. BR102020015433A2 — Composition and process for obtaining sustainable products with a function to ..., Miguel Arcadio Rigon Caires / Dieter Schultz, prioridade 2020-07-29, publicado 2022-02-08. BR102018070167A2 — Chestnut “pequi” whole, processing to add value, Paulo de Tarso de Souza Dayrell, prioridade 2018-09-30, publicado 2020-04-14; apareceu como ruído lexical da consulta.

As facetas exibiram Bayer, BASF, FMC, Bayer Cropscience e Syngenta. O lote sugere que `inoculante` amplia o corpus para formulação, logística/veículos, aplicação conjunta e uso em alimentação animal, além do núcleo de bioinsumos agrícolas.

URL: https://patents.google.com/?q=(inoculante)&country=BR
Data da consulta: 2026-08-21.


## Query: biopesticida + BR

A página respondeu com **6.712 resultados**. A primeira página é mais ampla e contém tanto biopesticidas quanto patentes agroquímicas que mencionam o termo. Os registros visíveis incluem BR112020023032A2 — composições de controle de pragas e seus usos, Maria Helena Christine Van Rooijen / Flagship Pioneering Innovations VI; BR122023004057B1 — molécula com utilidade pesticida, Yu Zhang / Corteva Agriscience; BR112017019208B1 — misturas pesticidas e tratamento de sementes com biopesticida, Tatjana Sikuljak / BASF Agrochemical Products; BR112015018853B1 — mistura com Bacillus subtilis FB17 e biopesticida, Thorsten Jabs / BASF Corporation; BR112016000299B1 — composições para fungos fitopatogênicos, Frederik Menges / BASF Agro; BR112015019289B1 — mistura para tratamento de sementes com Bacillus subtilis FB17, Thorsten Jabs / BASF Corporation; e BR112014014702A2 — método para controlar praga e biopesticida combinado com enzimas de degradação de cutícula, E. Leland Jarrod / Novozymes.

As facetas exibiram BASF, Syngenta, Dow AgroSciences, Sumitomo Chemical e Monsanto Technology. A consulta deve ser normalizada com cuidado porque o volume inclui ruído lexical e famílias internacionais; a primeira página ainda fornece sinais úteis sobre combinações entre cepas microbianas, tratamento de sementes, enzimas e químicos convencionais.

URL: https://patents.google.com/?q=(biopesticida)&country=BR
Data da consulta: 2026-08-21.


## Query: biofertilizante + BR

A página respondeu com **6.633 resultados**. A primeira página trouxe ruído de patentes de fertilizantes, mas também sinais diretos de biotecnologia agropecuária. Os registros visíveis incluem BR112019015945B1 — método para conversão biológica de CO2/CO em produto alimentício, Lisa Dyson / Kiverdi; BR112019022106A2 — método e composição para melhorar aquisição de nutrientes de plantas, Neumann Günter / EuroChem Agro; BR112022001668A2 — composição biopesticida e biofertilizante à base de Pseudoxanthomonas indica, Nordelo Valdivia Aylin / CT Ingeniería Genética Biotecnología; BR112014010650B1 — composições fertilizantes com inoculantes microbianos e métodos para melhoria do solo, Wayne Finlayson / Terragen Holdings; BR112015006330A2 — rizobactérias Bacillus firmus solubilizadoras de fosfato como biofertilizante, Ranjan Banerjee Manas / Xitebio Tech; BR112021001574A2 — processo para fabricar composições nutricionais para plantas e solos, Sushil K. Bhalla / Envirokure; BRPI0811002B1 — método para estimular crescimento e desenvolvimento fenológico de plantas, Jesús Mena Campos / Centro de Ingeniería Genética y Biotecnología.

As facetas exibiram BASF, Sergio Massao Watanabe, USP, The Mosaic Company e Yara International. A semente conecta fertilização biológica, aquisição de nutrientes, solubilização de fosfato, rizobactérias, conversão de resíduos e biopesticidas; o corpus normalizado deverá separar menção lexical de aplicação central.

URL: https://patents.google.com/?q=(biofertilizante)&country=BR
Data da consulta: 2026-08-21.


## Query: Rhizobium + BR

A página respondeu com **3.402 resultados**. A primeira página mostrou BR112020018646A2 — Methods for plant transformation, Ajith Anand / Pioneer Hi-Bred; BR112021005052A2 — methods and compositions to improve phosphate solubilization, Sarah Bloch / Pivot Bio; BR112020013023B1 — compostos heterocíclicos para controle de artrópodes, Ayaka Tanaka / Sumitomo Chemical; BR112021010947A2 — polymer compositions with improved stability for microbial nitrogen fixing, Farzaneh Rezaei / Pivot Bio; BRPI0817934B1 — composição para melhorar rendimento vegetal com Rhizobium leguminosarum, Smith Raymond / Merck; BR112016029884B1 — método para aumentar parâmetro de crescimento de planta leguminosa, Christopher Milton Mathew Franco / Flinders University; BRPI0711672A2 — uso de espécies bacterianas não Agrobacterium para transformação vegetal, Xudong Ye / Monsanto Technology; BR112016000299B1 — composição e método contra fungos fitopatogênicos; e BR112017000877B1 — intensificação sinérgica do crescimento vegetal.

Os excertos conectam Rhizobium/rizóbios a solubilização de fosfato, fixação simbiótica de nitrogênio, rendimento de leguminosas, transformação vegetal e combinações microbianas. As facetas exibiram Monsanto Technology, Bayer, Dow AgroSciences, Bayer Cropscience e BASF.

URL: https://patents.google.com/?q=(Rhizobium)&country=BR
Data da consulta: 2026-08-21.


## Query: Bacillus thuringiensis + BR

A página respondeu com **14.887 resultados**. A primeira página foi dominada por patentes agroquímicas que usam a espécie como referência ou agente biológico em combinações. Os registros visíveis incluem BR112021007399A2 — pesticidally active azole-amide compounds, Julien Daniel Henri Gagnepain / Syngenta; BR112020022659A2 — métodos de aplicação de heteroaril-triazóis e tetrazóis, Roger Graham Hall / Syngenta Crop Protection; BR112021008675A2 — pesticide active azole-amide compounds, Amandine Kolleth Krieger / Syngenta; BR112020013023B1 — compostos heterocíclicos, Ayaka Tanaka / Sumitomo Chemical; BR112021010947A2 — composições poliméricas para estabilidade de produtos microbianos de fixação de nitrogênio, Farzaneh Rezaei / Pivot Bio; BR112021011372A2 — novos sistemas CRISPR-Cas para edição genômica, Zhenglin Hou / Pioneer Hi-Bred; BR112019020253B1 — composições fungicidas e controle de doenças fitopatogênicas, Thomas James Hoffman / Syngenta, cujo excerto lista Bacillus thuringiensis, baculovírus, bactérias entomopatogênicas, vírus e fungos como agentes biológicos.

As facetas exibiram Syngenta, Bayer, Bayer Cropscience, BASF e Monsanto Technology. A semente apresenta grande recall, mas baixa precisão lexical na primeira página; será útil para relações entre organismos, agentes de controle, tecnologias de edição e formulações, desde que o normalizador preserve o contexto do termo.

URL: https://patents.google.com/?q=(Bacillus+thuringiensis)&country=BR
Data da consulta: 2026-08-21.


## Query: Trichoderma + BR

A página respondeu com **6.524 resultados**. A primeira página mostrou usos em biocontrole, produção industrial, alimentos, enzimas e sequestro de carbono. Os registros visíveis incluem BR112021006854A2 — materiais e métodos para uso/sequestro de carbono melhorado, Sean Farmer / Locus IP; o excerto combina Trichoderma harzianum e Bacillus amyloliquefaciens para reduzir gases de efeito estufa, melhorar utilização de carbono ou aumentar sequestro. BR112021001282A2 — yeast expressing enzymes for ethanol production, Michael Glenn Catlett / Novozymes; BR112020022659A2 — métodos de aplicação de compostos heteroaril, Roger Graham Hall / Syngenta; BR112020013023B1 — compostos heterocíclicos, Ayaka Tanaka / Sumitomo Chemical; BR112021007367A2 — componentes recombinantes para produtos alimentícios, Timothy Geistlinger / Perfect Day; BR112012013205B1 — mutante de Trichoderma reesei para produção de enzimas, Suchindra Maiyuran / Novozymes; BR102022007118A2 — formulações de agente de controle biológico incluindo Trichoderma, Jose Antonio De Cote / Shared-X; BR112020006362A2 — produção em larga escala de produtos líquidos e sólidos de Trichoderma, Sean Farmer / Locus Agriculture; BRPI0822486B1 — Trichoderma atroviride SC1 para controle biológico de doenças fúngicas, Ilaria Pertot / Trentino Sviluppo; e BR112016001583B1 — uso para germinação e redução de fungos não Trichoderma.

As facetas exibiram Novozymes, Bayer, IFP Energies Nouvelles, Danisco e Syngenta. A consulta trouxe um sinal transversal relevante para o corpus: o mesmo organismo aparece em agricultura, manufatura biológica, enzimas, alimentos e carbono, devendo ser preservado como relação tecnológica sem presumir que todos os documentos pertencem ao mesmo mercado.

URL: https://patents.google.com/?q=(Trichoderma)&country=BR
Data da consulta: 2026-08-21.


## Query: fixação de nitrogênio + BR

A página respondeu com **8.956 resultados**. A primeira página ficou fortemente concentrada na plataforma da Pivot Bio e em micróbios de fixação biológica de nitrogênio. Os registros visíveis incluem BR112021010947A2 — composições poliméricas com estabilidade aprimorada para produtos microbianos de fixação de nitrogênio, Farzaneh Rezaei / Pivot Bio; BR112020026771A2 — composições agrícolas com micróbios de fixação de nitrogênio remodelados, Mark Reisinger / Pivot Bio; BR112020008002A2 — alvos gênicos para fixação de nitrogênio para aprimorar traços de plantas, Alvin Tamsir / Pivot Bio; BR112021000268A2 — liberação dinâmica de nitrogênio temporal e espacialmente direcionada, Alvin Tamsir / Pivot Bio; BR112020008035A2 — métodos e composições para aprimorar micróbios geneticamente modificados que fixam nitrogênio, Alvin Tamsir / Pivot Bio; BR112020026676A2 — remodelação microbiana guiada, Sarah Bloch / Pivot Bio; e BR112021015218A2 — consistência aprimorada de rendimento de cultura por fixação biológica de nitrogênio, Ernest Sanders / Pivot Bio.

Os excertos mencionam nitrogenase, sistemas biológicos em contraste com Haber-Bosch, rizóbios, ensaios de redução de acetileno, genes nifA/nifL/ntrB/ntrC e fornecimento sustentável de nitrogênio às culturas. As facetas exibiram BASF, Precision Planting, Bayer Cropscience, Bayer e Ricoh. A consulta reforça um eixo tecnológico de eficiência de insumos e agricultura de baixo impacto, mas o lote ainda é majoritariamente composto por famílias internacionais com publicação BR.

URL: https://patents.google.com/?q=(fixa%C3%A7%C3%A3o+de+nitrog%C3%AAnio)&country=BR
Data da consulta: 2026-08-21.


## Query: biological control + BR

A página respondeu com **56.223 resultados**. A primeira página mostrou resultados amplos, incluindo BR112019024241A2 — aparato para detectar, medir e quantificar, M. Thompson Brian / Spogen Biotech; BR112020016351A2 — microbial compositions for prevention or reduction of plant pathogenic fungi, Robert McBride / Boost Biomes; BR112020005803A2 — composições e métodos para produção/administração modular de compostos biologicamente ativos, Ameer Hamza Shakeel / Agrospheres; BR112020004812A2 — methods and compositions for biological control of plant pathogens, Margaret Roper / CSIRO; BR112020026771A2 — agricultural compositions using remodeled nitrogen-fixation microbes, Mark Reisinger / Pivot Bio; BR112021010947A2 — polymer compositions with improved stability for microbial nitrogen fixing, Farzaneh Rezaei / Pivot Bio; e BR112020008035A2 — methods and compositions for enhancing genetically modified microbes that fix atmospheric nitrogen, Alvin Tamsir / Pivot Bio.

Os excertos conectam controle biológico de patógenos, microrganismos antifúngicos, formulações agrícolas, fixação de nitrogênio e detecção/quantificação de agroquímicos. O volume é muito mais amplo que a busca `biocontrole`, reforçando que a semente em inglês tem alto recall e deverá ser tratada como sinal de descoberta, não como conjunto de alta precisão.

URL: https://patents.google.com/?q=(biological+control)&country=BR
Data da consulta: 2026-08-21.


## Query: bioinput + BR

A página respondeu com **49 resultados**. A primeira página mostrou forte concentração em documentos brasileiros de bioinsumos, incluindo BR112018012451B1 — composição biopesticida à base de vírus, Gloria Patricia Barrera Cubillos / Corporación Colombiana de Investigación Agropecuaria-Agrosavia; BR102023003698A2 — bioinputs based on T. harzianum and sophorolipids, Thiago Moura Rocha / Universidade de São Paulo; BR102021017152A2 — bio-inputs production system for rural properties, Rafael Winterfeld Barbieri; BR102024003835A2 — composição sólida de microbiológico imobilizado, Carla Geane Brandenburg Brenner; BR202021011674U2 — biorreator descartável e método de monitoramento físico-químico de bioinputs por termocromia e espectrometria, Hercules Gustavo dos Santos Sarmento / Fernando Augusto da Silveira; BR202023007866U2 e BR202022014268U2 — módulos de fermentação asséptica para bioinputs, Carlos Henrique Alves de Paula / Dosaggio e GI Indústria; BR102020013946A2 — processo de fabricação de nutrição para bioinsumos agrícolas e fertilizantes; e BR102023023945A2 — composição bioherbicida dessecante de contato.

Os excertos indicam fermentação sólida de Trichoderma, produção personalizada em propriedades rurais, biorreatores descartáveis, monitoramento físico-químico, módulos assépticos e aplicação direta no sulco. A consulta em inglês confirmou que a terminologia `bioinput` recupera um núcleo brasileiro de sistemas de produção e controle de qualidade, com menor volume que `biocontrole` e `biofertilizante`.

Facetas observadas: MCTI/Museu Paraense Emílio Goeldi, Universidade de São Paulo, Universidade do Estado da Bahia, GI Indústria, Comércio e Tecnologia Ltda - ME e Dosaggio Máquinas e Equipamentos Ltda.

URL: https://patents.google.com/?q=(bioinput)&country=BR
Data da consulta: 2026-08-21.


## Query: microbial inoculant + BR

A página respondeu com **4.975 resultados**. A primeira página exibiu BR112021006854A2 — materiais e métodos para uso/sequestro melhorado de carbono, Sean Farmer / Locus IP; BR112020002401A2 e BR112020002388A2 — microbial inoculant compositions and methods com espécies aquáticas de Pseudomonas e Clostridium, Tony Hagen / Raison; BR112016013509B1 — microbial inoculant system to promote plant growth and aerobic microbes, Brian B. McSpadden Gardener / Ohio State Innovation Foundation; BR112021010332A2 — yeast-based compositions to improve rhizosphere and plant health properties, Sean Farmer / Locus Agriculture; BR112014010650B1 — fertilizer compositions comprising microbial inoculants, Wayne Finlayson / Terragen Holdings; BR112021011024A2 — método para melhorar crescimento e sobrevivência de microrganismos, Mike Whiting / Danstar Ferment; BR112018068739B1 — métodos para estimular crescimento vegetal e fitossanidade; BR112019024241A2 — aparato para detectar, medir e quantificar; e BR112020022643A2 — produtos baseados em microrganismos para saúde e imunidade radicular.

Os excertos conectam inoculantes a saúde radicular, crescimento vegetal, qualidade do solo, rizosfera, formulações fertilizantes, culturas estáveis, microrganismos aquáticos, sequestro de carbono e monitoramento. As facetas exibiram Bioreset Biotecnologia, BASF, FMC, Monsanto Technology e Universidade de São Paulo. A semente amplia o corpus para tecnologias de formulação e desempenho biológico, com sobreposição relevante com `inoculante`, `biofertilizante` e `Trichoderma`.

URL: https://patents.google.com/?q=(microbial+inoculant)&country=BR
Data da consulta: 2026-08-21.

