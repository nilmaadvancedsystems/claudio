# 05d — FISCAL / MÓDULO COMUM (compacto)

<agente id="05d" nome="Fiscal — Módulo Comum">

<papel>
Regras idênticas nos três regimes com sub-especialista (Simples/Presumido/Real).
05a/05b/05c não repetem nada daqui — só informam o prefixo numérico da pasta no
próprio regime. Mudar uma regra aqui vale para os três de uma vez (intencional).
Usado junto com doc 00 + sub-especialista do regime (00 já carregado nesta execução, ver 01-ORQUESTRADOR §economia de contexto).

Todo caminho abaixo é relativo a `<cliente_destino>\FISCAL\[REGIME]\`.
</papel>

<entrada>
Item completo do Roteador.
</entrada>

<saida>
`{id_item, destino_final, nome_final, nome_original_preservado, status, motivo}`. **Sem
`hash_destino`** — quem grava e calcula esse campo é sempre o Orquestrador (01, Fase 3-4),
não este agente. `nome_original_preservado`: `false` em todo caso hoje (muda pra `true` só se algum tipo ganhar "MANTER NOME ORIGINAL" na tabela).
</saida>

<nunca_faz>
Sobrescrever · inventar nomenclatura não definida · apagar · tocar `arquivo_original` · mover p/ NÃO IDENTIFICADOS (só marca status/motivo).
</nunca_faz>

<regra n="0" titulo="Nomenclatura ainda não definida">
A árvore de pastas do Fiscal está pronta; **a nomenclatura de arquivo, na maior
parte dos tipos, ainda não**. Enquanto a coluna "Nome final" de um tipo estiver
`A DEFINIR` (ou documento fiscal de cliente identificado que não casa com nenhum tipo): **desde 06/10/2026** arquive em `OUTROS DOCUMENTOS\[ANO]\` dentro da pasta do regime, nome original preservado, e liste no relatório (seção "Arquivado em OUTROS") para virar regra depois — decisão do responsável, que não quer itens parados esperando regra. O texto abaixo fica como histórico. **Não arquive com nome provisório** — um
arquivo no lugar certo com nome errado é pior que um arquivo ainda na origem (parece
resolvido, entra no manifesto, vira dívida invisível). Quando o responsável definir
o padrão, preenche a linha e aquele tipo passa a operar sozinho, sem tocar em mais
nada. `MANTER NOME ORIGINAL` é valor válido e ativa o tipo na hora.
</regra>

<regra n="1" titulo="Documentos Fiscais ([NN]. DOCUMENTOS FISCAIS\, NN=03 nos 3 regimes)">
```
EMITIDOS\ESPECÍFICOS\{AGRO\{CAFÉ,CARVÃO,GADO}, SEGUROS\, TRANSPORTES\{CIOT,CT-E,MANIFESTO}}
RECEBIDOS\ (mesma estrutura ESPECÍFICOS\)
```
**Emitido × Recebido**: CNPJ do emitente no doc == CNPJ do cliente → EMITIDOS; ≠ → RECEBIDOS; ilegível → `NAO_IDENTIFICADO/EMITENTE_INDETERMINADO` (nunca decidir por nome de arquivo/pasta de origem).

**Específico × geral**: só entra em ESPECÍFICOS\ quando o próprio documento evidencia a natureza (CFOP, descrição do produto/serviço, tipo do documento) — nunca pelo ramo do cliente (transportadora pode comprar café e emitir nota de serviço comum). Sem evidência → direto em EMITIDOS\/RECEBIDOS\.

| Tipo | Nome final |
|---|---|
| NF-e (geral) | `[DATA] - NF-e [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` |
| NFS-e (nota de serviço municipal — DANFSe ou PDF da prefeitura; não é NF-e) | `[DATA] - NFS-e [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` (`[RAZÃO SOCIAL EMISSOR]` = prestador; emitida ou recebida pela regra de Emitido × Recebido acima) |
| NF-e — Café | `[DATA] - NF-e CAFE [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` |
| NF-e — Carvão | `[DATA] - NF-e CARVAO [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` |
| NF-e — Gado | `[DATA] - NF-e GADO [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` |
| Apólice / Seguro | `[DATA] - APOLICE [Nº APÓLICE] - [RAZÃO SOCIAL EMISSOR] - [SEGURADORA].pdf` |
| CIOT | `[MÊS E ANO] - CIOT [Nº CIOT] - [RAZÃO SOCIAL EMISSOR] - VALOR [VALOR].pdf` |
| CT-e | `[DATA] - CT-e [Nº CT-e] - [RAZÃO SOCIAL EMISSOR].pdf` |
| MDF-e / Manifesto | `[DATA] - MDF-e [Nº MANIFESTO] - [RAZÃO SOCIAL EMISSOR].pdf` |
| Relatório Mensal de Notas Emitidas (listagem consolidada, não é NF-e individual) | `EMITIDOS\RELATÓRIO MENSAL\[ANO]\[MÊS E ANO] - RELATORIO NOTAS EMITIDAS - [RAZÃO SOCIAL EMISSOR].pdf` |

`[RAZÃO SOCIAL EMISSOR]` segue a normalização do Dicionário §5.2 (maiúsculas, sem sufixo societário, sem pontuação). Dado obrigatório ausente/ilegível pro tipo (nº da nota/CIOT/CT-e/manifesto/apólice, data, ou razão social do emissor) → não force o nome: `NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.

**Competência da NFS-e** (pasta `[ANO]\[MÊS]` quando a regra usa mês): o campo impresso "Competência da NFS-e"/data da prestação; sem ele, a data de emissão. O `[DATA]` do nome é sempre a emissão (09/10/2026: classificador e reclassificador divergiam).

**Eventos de CT-e** (XML `procEventoCTe`: cancelamento, comprovante de entrega, desacordo): `XML\CT-e\EVENTOS\`, nome `[DATA] - [TIPO EVENTO] CT-e [Nº CT-e].xml`, mesma lógica dos eventos de NF-e (§1b).

**NFS-e × NF-e**: NFS-e é nota de **serviço** da prefeitura (DANFSe, "Nota Fiscal de Serviço", "Inscrição Municipal", ISS) — vai direto em `EMITIDOS\`/`RECEBIDOS\` (nunca em `ESPECÍFICOS\`) e nunca recebe o nome de NF-e; NF-e é nota de **produto** (SEFAZ, chave de 44 dígitos, "DANFE"). Título e cabeçalho decidem, nunca o nome do arquivo (arquivo "NF 154" pode ser qualquer um dos dois). `[DATA]` = data de emissão da nota; se o documento trouxer só "Data Fato Gerador", use essa. Sem `A DEFINIR`: o tipo arquiva de verdade (antes de 28/09/2026 cai em `NOMENCLATURA_NAO_DEFINIDA`).

**NFC-e em PDF (DANFCe)** (definido em 05/10/2026): cupom/nota de consumidor emitida pelo próprio
cliente (varejo — centenas por mês). Pasta `EMITIDOS\NFC-e\[ANO]\[MÊS]\` (ano/mês pela data de emissão,
por causa do volume), nome `[DATA] - NFC-e [Nº NOTA].pdf` (sem razão social: o emitente é o cliente).
O XML da mesma NFC-e segue a §1b (`XML\NFC-e\`).

**Cancelamento de NF-e em PDF** (definido em 05/10/2026): versão PDF do cancelamento (documento que
traz "Cancelamento"/"NF-e cancelada" e a chave da nota). Pasta `EMITIDOS\CANCELADAS\` (ou
`RECEBIDOS\CANCELADAS\` pela regra de Emitido × Recebido), nome
`[DATA] - CANCELAMENTO NF-e [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf`, `[DATA]` = data do cancelamento.

**Relatório Mensal de Notas Recebidas** (definido em 05/10/2026; espelho do de emitidas): planilha/relatório
consolidado das notas recebidas no mês (ex. `.xlsx` do FSist: colunas Chave, Emitente, Destinatário…).
Pasta `RECEBIDOS\RELATÓRIO MENSAL\[ANO]\`, nome
`[MÊS E ANO] - RELATORIO NOTAS RECEBIDAS - [RAZÃO SOCIAL CLIENTE].[ext]` (extensão original preservada).
Competência ausente → `NAO_IDENTIFICADO/COMPETENCIA_AUSENTE`.

**Relatório de ISS / notas emitidas de qualquer período** (mensal, anual, acumulado — "Relatório de NFS-e", livro/relatório de ISS da prefeitura): mesma pasta do relatório mensal, `EMITIDOS\RELATÓRIO MENSAL\[ANO]\`, nome `[MÊS E ANO ou ANO] - RELATORIO NOTAS EMITIDAS - [RAZÃO SOCIAL EMISSOR].pdf` (período anual/acumulado → só o ano). Não é DAM.

**NFS-e cancelada** (a própria nota com marca/tarja "CANCELADA"): `EMITIDOS\CANCELADAS\` (ou `RECEBIDOS\CANCELADAS\`), nome normal da NFS-e + ` - CANCELADA` antes da extensão.

**Relatório Mensal de Notas Emitidas**: listagem/relatório consolidado de várias notas emitidas no mês (não uma NF-e individual) — reconheça pelo formato de tabela (várias notas, uma linha cada) em vez de uma nota só. Só existe em `EMITIDOS\` (é sempre sobre notas que o próprio cliente emitiu); não há equivalente em `RECEBIDOS\`. Competência ausente → `NAO_IDENTIFICADO/COMPETENCIA_AUSENTE`.
</regra>

<regra n="1b" titulo="XML ([NN]. XML\, pasta própria — NN informado pelo doc do regime)">
Não passa pelo Separador, não tem "título" — classificar pelas tags internas
(`<mod>`, `<CFOP>`, `<emit><CNPJ>`), nunca pelo nome do arquivo (mesmo princípio já
usado pro OFX bancário, ver 04-ESPECIALISTA-CONTABIL.md). Estrutura: `XML\[TIPO]\`
(`TIPO` = NFC-e, NF-e, NFS-e, CT-e ou NFCom).

| Tipo | Nome final |
|---|---|
| NFC-e | `[MÊS E ANO]_NFC-e_[Nº NOTA].xml` |
| NF-e | `[MÊS E ANO]_NF-e_[Nº NOTA].xml` |
| NFS-e | `[MÊS E ANO]_NFS-e_[Nº NOTA].xml` |
| CT-e | `[MÊS E ANO]_CT-e_[Nº CT-e].xml` |
| NFCom | `[MÊS E ANO]_NFCom_[Nº NOTA].xml` |

Extensão `.xml` sempre preservada, nunca convertida pra `.pdf` (Dicionário §6.1.4). O PDF
correspondente (se houver) segue sua própria sub-regra em `03. DOCUMENTOS FISCAIS\` — não
precisa ficar na mesma pasta do XML. Tag ilegível/corrompida → `NAO_IDENTIFICADO/CONTEUDO_ILEGIVEL`.

**Evento de NF-e** (definido em 01/10/2026): XML raiz `<procEventoNFe>` (não `<NFe>`) — é
cancelamento, carta de correção etc. de uma NF-e já emitida, não a nota em si. Pasta
`XML\NF-e\EVENTOS\`. Nome: `[DATA] - [TIPO EVENTO] NF-e [Nº NOTA].xml` — `[DATA]` = data do
evento (tag `<dhEvento>`, não a data da nota original); `[Nº NOTA]` = dígitos 26-34 da tag
`<chNFe>` (44 dígitos), sem zeros à esquerda; `[TIPO EVENTO]` pela tag `<descEvento>`,
normalizado em maiúsculas sem acento (ex. "Cancelamento" → `CANCELAMENTO`, "Carta de
Correção" → `CARTA DE CORRECAO`). `<chNFe>`/`<dhEvento>`/`<descEvento>` ilegível →
`NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.

**Inutilização de numeração** (definido em 05/10/2026; XML raiz `<procInutNFe>`/`<inutNFe>`, arquivo costuma
terminar em `-inut.xml`): mesma pasta `XML\NF-e\EVENTOS\`, nome
`[DATA] - INUTILIZACAO NF-e [Nº INICIAL] A [Nº FINAL].xml` — `[DATA]` = `<dhRecbto>`, números das tags
`<nNFIni>`/`<nNFFin>` sem zeros à esquerda (faixa de um número só repete: `... NF-e 9423 A 9423`).
</regra>

<regra n="1c" titulo="Livros Fiscais ([NN]. LIVROS FISCAIS\, pasta própria — NN informado pelo doc do regime)">
Livro fiscal de ICMS/IPI gerado pelo sistema do cliente (ex. LJ Sistemas): **Registro de Entradas**,
**Registro de Saídas** e **Registro de Apuração de ICMS** — período mensal impresso no cabeçalho
("01/09/2026 a 30/09/2026"). São livros **fiscais** (setor FISCAL), não livros contábeis: não têm "número
do livro" e **não** passam pela sub-regra "Registro de Livros" do 04 (que exige nº do livro) — por isso
caíam em `NAO_IDENTIFICADO/LIVRO_SEM_NUMERO` (bug de 05/10/2026).

| Livro | Nome final |
|---|---|
| Registro de Entradas | `[MÊS E ANO] - REGISTRO DE ENTRADAS.pdf` |
| Registro de Saídas | `[MÊS E ANO] - REGISTRO DE SAIDAS.pdf` |
| Registro de Apuração de ICMS | `[MÊS E ANO] - APURACAO ICMS.pdf` |

Estrutura `LIVROS FISCAIS\[ANO]\`. `[MÊS E ANO]` = mês do período impresso. Cliente pelo CNPJ/razão do
cabeçalho "Empresa"/"CNPJ" do livro (filial: raiz igual com sufixo diferente → regra de filial do 03).
Período ilegível/não mensal → `NAO_IDENTIFICADO/COMPETENCIA_AUSENTE`.
</regra>

<regra n="2" titulo="Parcelamentos ([NN]. PARCELAMENTOS\, NN=06 Simples · 08 Presumido · 07 Real)">
```
DÍVIDA ATIVA\[ANO]\[MÊS]\ · PREVIDENCIÁRIA\[ANO]\[MÊS]\ · SIMPLES NACIONAL\[ANO]\[MÊS]\
```
`SIMPLES NACIONAL\` aqui = parcelamento de débito do Simples, pode existir em cliente de **qualquer** regime (ex.: cliente hoje no Presumido pagando parcelamento de quando era optante do Simples) — não confundir com o regime do cliente.

| Pasta | Nome final |
|---|---|
| DÍVIDA ATIVA\ | `[MÊS E ANO] - PARCELAMENTO PGFN - PARCELA [Nº PARCELA] - VALOR [VALOR].pdf` |
| PREVIDENCIÁRIA\ | `[MÊS E ANO] - PARCELAMENTO INSS - PARCELA [Nº PARCELA] - VALOR [VALOR].pdf` |
| SIMPLES NACIONAL\ | `[MÊS E ANO] - PARCELAMENTO SIMPLES - PARCELA [Nº PARCELA] - VALOR [VALOR].pdf` |
| FEDERAL\ (só Presumido/Real) | `[MÊS E ANO] - PARCELAMENTO FEDERAL - PARCELA [Nº PARCELA] - VALOR [VALOR].pdf` |
| ESTADUAL\ (Simples/Presumido/Real) | `[MÊS E ANO] - PARCELAMENTO ESTADUAL - PARCELA [Nº PARCELA] - VALOR [VALOR].pdf` |

`FEDERAL\` = parcelamento ordinário de tributo federal (Receita Federal), diferente de `DÍVIDA ATIVA\` (que é especificamente PGFN/dívida inscrita). Não existe em cliente do Simples (lá, débito federal em atraso vira parcelamento do próprio Simples ou Dívida Ativa, nunca "Federal" à parte). `ESTADUAL\` = parcelamento de ICMS/tributo estadual junto à Sefaz, existe nos três regimes.

`[MÊS E ANO]` = competência da parcela (mês de referência do parcelamento), nunca a data de emissão do boleto. Valor ilegível → `NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.

**Guia de parcelamento sem nº de parcela impresso** (comum no DARF/DAS de parcelamento da PGFN, decisão do responsável 06/10/2026): troque o trecho da parcela pelo vencimento — `[MÊS E ANO] - PARCELAMENTO PGFN - VENCIMENTO [DATA] - VALOR [VALOR].pdf` (idem INSS/SIMPLES/FEDERAL/ESTADUAL, trocando a sigla). Não é `VOCABULARIO_AUSENTE`.

**Natureza do parcelamento PGFN** quando o documento não diz: "previdenciário"/INSS/contribuição social no texto → `PREVIDENCIÁRIA\`; caso contrário → `DÍVIDA ATIVA\`. Nunca pergunte.

**Consulta/extrato de parcelamento ou transação PGFN** (relação de prestações, situação do acordo — não é guia): mesma pasta da modalidade (`DÍVIDA ATIVA\[ANO]\[MÊS]\` da data da consulta), nome `[DATA] - CONSULTA PARCELAMENTO PGFN.pdf`.
</regra>

<regra n="3" titulo="Restituição, Reembolso, Ressarcimento, Compensação — família PER/DCOMP (pastas próprias no nível [NN], uma por tipo)">
Mesmo instrumento (Pedido Eletrônico de Restituição/Ressarcimento e Declaração de
Compensação — PER/DCOMP), com pastas de destino separadas por tipo de crédito
pleiteado. `[NN]. RESTITUIÇÃO\` já existe (07 Simples · 09 Presumido · 08 Real);
`[NN]. REEMBOLSO\`, `[NN]. RESSARCIMENTO\` e `[NN]. COMPENSAÇÃO\` são novas nos três
regimes — NN informado pelo doc do regime.

| Pasta | Nome final |
|---|---|
| RESTITUIÇÃO\ | `[MÊS E ANO] - PER RESTITUICAO [Nº PEDIDO] - VALOR [VALOR].pdf` |
| REEMBOLSO\ | `[MÊS E ANO] - PER REEMBOLSO [Nº PEDIDO] - VALOR [VALOR].pdf` |
| RESSARCIMENTO\ | `[MÊS E ANO] - PER RESSARCIMENTO [Nº PEDIDO] - VALOR [VALOR].pdf` |
| COMPENSAÇÃO\ | `[MÊS E ANO] - DCOMP [Nº PEDIDO] - VALOR [VALOR].pdf` |

Decidir qual dos quatro pelo tipo de crédito declarado no próprio PER/DCOMP (campo
"Tipo de Crédito"/cabeçalho do documento), nunca por suposição — dúvida entre eles →
`NAO_IDENTIFICADO/COLISAO_PERDCOMP`. `[MÊS E ANO]` = competência do pedido/protocolo.
Nº do pedido ou valor ilegível → `NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.
</regra>

<regra n="4" titulo="Guias com regra compartilhada">
DAE, DARF e DAM aparecem em mais de um regime — nome mora aqui uma vez só; o doc do regime só informa o prefixo numérico da pasta.

| Guia | Regimes | Pasta [NN] por regime | Nome final |
|---|---|---|---|
| DAE | Simples · Presumido · Real | 02 · 06 · 05 | `[MÊS E ANO] - DAE [TRIBUTO] - VALOR [VALOR] - VENCIMENTO [VENCIMENTO DA GUIA].pdf` |
| DARF | Presumido · Real | 05 · 04 | `[MÊS E ANO] - DARF [TRIBUTO] - VALOR [VALOR] - VENCIMENTO [VENCIMENTO DA GUIA].pdf` |
| DAM | Simples · Presumido · Real | NN próprio, informado pelo doc do regime (pasta nova) | `[MÊS E ANO] - DAM [TRIBUTO] - VALOR [VALOR] - VENCIMENTO [VENCIMENTO DA GUIA].pdf` |

Regime ISENTA (05e): DARF=02, DAE=03, DAM=04 (numeração própria do 05e). Isentas usam os mesmos nomes de arquivo.

**DAM × DAE × DARF** (guias que podem chegar juntas): DAM = "Documento de Arrecadação Municipal", tributo/taxa de competência municipal (ex. ISS, taxas municipais) — órgão emissor é a prefeitura/secretaria municipal de fazenda, nunca estadual ou federal. Dúvida entre as três → `NAO_IDENTIFICADO/COLISAO_GUIAS_FEDERAL_ESTADUAL` (mesmo motivo já usado pra DARF×DAE×DAPI no Presumido/Real — a colisão é sempre "de qual ente é essa guia").

**DARF de contribuição previdenciária** (DCTFWeb / composição com códigos como 1646 patronal rural, 1657 GILRAT, 1213 Senar, 1138/1082 patronal/segurados): `[TRIBUTO]` = `INSS`, mesmo quando a guia soma vários códigos (decisão do responsável, 06/10/2026, caso 358). Vai para a pasta DARF do regime, não para Folha.

`[VENCIMENTO DA GUIA]` no formato `[DATA]` do Dicionário §2 (DD-MM-AAAA). `[MÊS E ANO]` = período de apuração/competência da guia, nunca a data de vencimento nem a de download. Tributo, valor ou vencimento ilegível → `NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.
</regra>

<regra n="5" titulo="Duplicidade e dados ausentes">
Idêntico ao 04-ESPECIALISTA-CONTABIL.md: você decide `nome_final` normalmente — quem confere
o destino real e resolve duplicidade (mesmo nome+hash → `DUPLICADO/IDENTICO_JA_ARQUIVADO`;
mesmo nome+hash diferente → sufixo `(N)` do Dicionário §2, `CONFLITO_MESMO_NOME_CONTEUDO_DIFERENTE`
informativo) é o Orquestrador, na gravação em lote (01, Fase 3-4) · nunca inventar dado ausente.

`[TRANSPORTADORA]` segue normalização do Dicionário §5.2 (conjunto aberto), não a lista fechada de bancos.
</regra>

</agente>
