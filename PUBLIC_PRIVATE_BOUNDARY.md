# Fronteira público–privado

Este laboratório nasce público, mas abertura não significa publicar tudo indiscriminadamente. O princípio é tornar público o método verificável e preservar o que contém risco operacional, informação sensível ou valor estratégico não autorizado.

| Pode ser público | Deve permanecer privado ou ser revisado antes de publicar |
|---|---|
| Código de coleta e normalização metadata-only | Tokens, chaves de API, cookies e credenciais |
| Schemas, contratos e exemplos sintéticos ou públicos | Memória operacional e decisões estratégicas internas |
| URLs, identificadores e metadata de fontes públicas | Dados derivados que revelem informação sensível ou não licenciada |
| Manifests reproduzíveis e hashes | Resultados ainda não validados que possam ser confundidos com conclusão |
| Taxonomias e métodos genéricos | Estratégias de busca proprietárias ou listas de alvos sensíveis |
| Perguntas, hipóteses e resultados com estado epistemológico | Materiais de terceiros que não possam ser redistribuídos |
| Relatos de erros, correções e limitações | Dados científicos baixados ou arquivos que não sejam necessários ao método |

## Regras operacionais

Nenhuma credencial entra no Git. Nenhum arquivo de patente, artigo ou dataset será baixado quando a metadata pública for suficiente para o estágio da investigação. Quando um arquivo for indispensável a uma etapa posterior, a autorização, licença, finalidade e forma de armazenamento deverão ser avaliadas antes do uso.

A presença de um registro em uma fonte não prova que a tecnologia é válida, nova, comercialmente viável, adequada a uma aplicação agrícola ou disponível para licenciamento. O projeto registrará essas distinções explicitamente.

Toda publicação deverá responder a três perguntas: qual é a fonte, qual transformação foi aplicada e qual parte ainda permanece incerta?

## Estados epistemológicos

O laboratório adotará, no mínimo, os seguintes estados:

- `observed`: diretamente sustentado pelo metadata ou documento identificado;
- `inferred`: derivado de observações por uma regra explicitada;
- `hypothesis`: possibilidade que exige teste adicional;
- `insufficient`: a evidência disponível não basta;
- `blocked`: uma decisão está impedida por falta de evidência, acesso ou capacidade de verificação;
- `rejected`: a hipótese ou seleção não atende aos critérios definidos;
- `contradicted`: a fonte apresenta evidência incompatível com a afirmação avaliada.

A ausência de evidência é uma saída válida. O sistema não deve preencher lacunas com confiança artificial.
