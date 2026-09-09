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
`A DEFINIR`: `status=FORA_DO_ESCOPO`, `motivo=NOMENCLATURA_NAO_DEFINIDA: <tipo>`.
Arquivo intocado na origem, reportado. **Não arquive com nome provisório** — um
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
| NF-e — Café | `[DATA] - NF-e CAFE [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` |
| NF-e — Carvão | `[DATA] - NF-e CARVAO [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` |
| NF-e — Gado | `[DATA] - NF-e GADO [Nº NOTA] - [RAZÃO SOCIAL EMISSOR].pdf` |
| Apólice / Seguro | `[DATA] - APOLICE [Nº APÓLICE] - [RAZÃO SOCIAL EMISSOR] - [SEGURADORA].pdf` |
| CIOT | `[MÊS E ANO] - CIOT [Nº CIOT] - [RAZÃO SOCIAL EMISSOR] - VALOR [VALOR].pdf` |
| CT-e | `[DATA] - CT-e [Nº CT-e] - [RAZÃO SOCIAL EMISSOR].pdf` |
| MDF-e / Manifesto | `[DATA] - MDF-e [Nº MANIFESTO] - [RAZÃO SOCIAL EMISSOR].pdf` |

`[RAZÃO SOCIAL EMISSOR]` segue a normalização do Dicionário §5.2 (maiúsculas, sem sufixo societário, sem pontuação). Dado obrigatório ausente/ilegível pro tipo (nº da nota/CIOT/CT-e/manifesto/apólice, data, ou razão social do emissor) → não force o nome: `NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.

**XML**: não passa pelo Separador, não tem "título" — classificar pelas tags (`<mod>`, `<CFOP>`, `<emit><CNPJ>`), não pelo nome do arquivo. NF-e + seu XML vão pra mesma pasta.
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

`[MÊS E ANO]` = competência da parcela (mês de referência do parcelamento), nunca a data de emissão do boleto. Nº da parcela ou valor ilegível → `NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.
</regra>

<regra n="3" titulo="Restituição ([NN]. RESTITUIÇÃO\, NN=07 Simples · 09 Presumido · 08 Real)">
Nome final: `[MÊS E ANO] - PER RESTITUICAO [Nº PEDIDO] - VALOR [VALOR].pdf`. `[MÊS E ANO]` = competência do pedido/protocolo. Nº do pedido ou valor ilegível → `NAO_IDENTIFICADO/VOCABULARIO_AUSENTE`.
</regra>

<regra n="4" titulo="Guias com regra compartilhada">
DAE e DARF aparecem em mais de um regime — nome mora aqui uma vez só; o doc do regime só informa o prefixo numérico da pasta.

| Guia | Regimes | Pasta [NN] por regime | Nome final |
|---|---|---|---|
| DAE | Simples · Presumido · Real | 02 · 06 · 05 | `[MÊS E ANO] - DAE [TRIBUTO] - VALOR [VALOR] - VENCIMENTO [VENCIMENTO DA GUIA].pdf` |
| DARF | Presumido · Real | 05 · 04 | `[MÊS E ANO] - DARF [TRIBUTO] - VALOR [VALOR] - VENCIMENTO [VENCIMENTO DA GUIA].pdf` |

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
