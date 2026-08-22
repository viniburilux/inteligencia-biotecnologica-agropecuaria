# Document Acquisition Layer V0 — Método Público

O Agro-Biotech Lab evoluiu de um inventário de metadata para um método de investigação documental. A camada pública descreve a arquitetura e os resultados agregados; os documentos e componentes operacionais permanecem no Lux-Lab privado.

## Arquitetura observável

```text
identificador
  → fonte e URL
  → resolução do documento
  → aquisição quando permitida
  → validação de formato e assinatura
  → validação de identidade
  → validação de conteúdo técnico
  → hash SHA-256
  → manifesto de provenance
  → status documental
```

## Diferença entre descoberta e aquisição

Crossref, OpenAlex e Unpaywall podem fornecer metadata, links, licenças ou ponteiros de conteúdo. Esses resultados são úteis para discovery/routing, mas não são tratados automaticamente como documento integral. O status só muda para `FULL_TEXT_VERIFIED` depois que o conteúdo é efetivamente recebido e validado.

## Critério de validação

A validação considera o tipo de documento. Para patentes HTML, exige identidade de publicação, descrição, claims e seções localizáveis. Para PDFs, exige resposta com conteúdo, MIME ou assinatura PDF, tamanho, extração textual não trivial e SHA-256. HTML intersticial, landing page, abstract, arquivo curto e HTTP 200 isolado são mantidos como falha ou não comprovados.

## Provenance

Cada tentativa mantém identificador, fonte, URL, timestamp, adapter lógico, status de acesso, status documental, formato, tamanho, hash e resultado dos checks. A camada pública expõe somente a versão sanitizada de IDs, URLs, hashes, estados e cobertura agregada.

## Limites

A cobertura é específica às rotas, fontes e ambiente do run. `FULL_TEXT_VERIFIED` significa que o arquivo passou pelos checks do método; não significa que o conteúdo seja de domínio público nem que possa ser redistribuído. Direitos, licenças e termos de cada fonte continuam aplicáveis.
