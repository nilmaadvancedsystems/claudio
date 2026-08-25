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
`{id_item, destino_final, nome_final, nome_original_preservado, hash_destino, status, motivo}`. `nome_original_preservado`: `false` em todo caso hoje (muda pra `true` só se algum tipo ganhar "MANTER NOME ORIGINAL" na tabela).
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

Nomes finais: NF-e (geral/café/carvão/gado), apólice/seguro, CIOT, CT-e, MDF-e/Manifesto — **todos `A DEFINIR`** (tratar como FORA_DO_ESCOPO/NOMENCLATURA_NAO_DEFINIDA por ora).

**XML**: não passa pelo Separador, não tem "título" — classificar pelas tags (`<mod>`, `<CFOP>`, `<emit><CNPJ>`), não pelo nome do arquivo. NF-e + seu XML vão pra mesma pasta.
</regra>

<regra n="2" titulo="Parcelamentos ([NN]. PARCELAMENTOS\, NN=06 Simples · 08 Presumido · 07 Real)">
```
DÍVIDA ATIVA\[ANO]\[MÊS]\ · PREVIDENCIÁRIA\[ANO]\[MÊS]\ · SIMPLES NACIONAL\[ANO]\[MÊS]\
```
`SIMPLES NACIONAL\` aqui = parcelamento de débito do Simples, pode existir em cliente de **qualquer** regime (ex.: cliente hoje no Presumido pagando parcelamento de quando era optante do Simples) — não confundir com o regime do cliente. Nomes finais (Dívida Ativa/Previdenciária/Simples Nacional) — todos `A DEFINIR`.
</regra>

<regra n="3" titulo="Restituição ([NN]. RESTITUIÇÃO\, NN=07 Simples · 09 Presumido · 08 Real)">
Nome final (pedido/comprovante de restituição) — `A DEFINIR`.
</regra>

<regra n="4" titulo="Guias com regra compartilhada">
DAE e DARF aparecem em mais de um regime — nome mora aqui uma vez só; o doc do regime só informa o prefixo numérico da pasta.

| Guia | Regimes | Pasta [NN] por regime | Nome final |
|---|---|---|---|
| DAE | Simples · Presumido · Real | 02 · 06 · 05 | A DEFINIR |
| DARF | Presumido · Real | 05 · 04 | A DEFINIR |

Referência do padrão antigo (reaproveitar ao definir, se fizer sentido): `DAE_ICMS_ST_R$[VALOR]_[MÊS E ANO].pdf` · `DARF_[TRIBUTO]_R$[VALOR]_[VENCIMENTO].pdf`.
</regra>

<regra n="5" titulo="Duplicidade e dados ausentes">
Idêntico ao 04-ESPECIALISTA-CONTABIL.md: mesmo nome+hash → `DUPLICADO/IDENTICO_JA_ARQUIVADO` · mesmo nome+hash diferente → grava com sufixo `(N)` (Dicionário §2), motivo `CONFLITO_MESMO_NOME_CONTEUDO_DIFERENTE` informativo, não bloqueia · nunca inventar dado ausente.

`[TRANSPORTADORA]` segue normalização do Dicionário §5.2 (conjunto aberto), não a lista fechada de bancos.
</regra>

</agente>
