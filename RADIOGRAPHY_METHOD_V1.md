# Método da Radiografia Exploratória V1

A radiografia lê `normalized_v2`, que integra os manifests V0, V1 e V2. Cada obra recebe memberships por correspondência lexical explícita em título, resumo/descrição, query e atores. Os clusters são operacionais: servem para orientar investigação e não representam classificação científica definitiva.

Atores e instituições são contabilizados por relações preservadas no corpus. Organismos e tecnologias são contados por ocorrência textual e cruzados com fonte e cluster. Queries novas só entram quando há um termo, ator, organismo, instituição, ponte ou lacuna observada no corpus.

A origem patentária é exibida em três estados: `brazilian_signal_observed`, `international_presence_in_BR` e `origin_unresolved`. O filtro BR é tratado como contexto de recuperação, não como prova de origem. Aliases seguros são registrados separadamente em `ENTITY_RESOLUTION_V1`; o corpus original não é sobrescrito.

Ausência, baixa densidade e ruído são preservados como motivos para reformulação ou nova busca. Nenhum documento integral, sequência ou dado científico foi baixado.
