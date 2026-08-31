# 06 — VERIFICADOR (dividido: motor determinístico + 1 chamada de LLM)

<agente id="06" nome="Verificador">

<papel>
Das 8 verificações do doc 06 original, só a #4 (Reclassificação Independente) exige
ler o conteúdo do documento e julgar — é a única que precisa de LLM. As outras 7 são
comparação de campos/strings contra o Dicionário: rodam como código, sem custo de
token nenhum.
</papel>

<procedimento titulo="Parte A — Motor determinístico (código, roda para 100% dos itens)">
Pseudocódigo (adaptar à linguagem do runtime local):

```
# 1. Integridade de volume
assert N_pais == (pais_todos_filhos_arquivado + pais_algum_filho_naoident_ou_dup
                   + pais_fora_do_escopo + pais_pdf_composto_nao_separado
                   + pais_ja_arquivado_anteriormente + pais_falha_integridade)
assert todo_item_tem_arquivo_original_existente_na_origem
assert todo_pai_separado_tem_paginas_filhas_cobrindo_100pct_sem_lacuna_sem_overlap
assert nenhum_pai_em_dois_baldes

# 2. Nomenclatura (regex contra Dicionário §2), exceto nome_original_preservado=true
assert not contem_placeholder_literal(nome_final)        # [CLIENTE], [BANCO], ...
assert data_no_formato(nome_final, "MM-AAAA|DD-MM-AAAA")
assert valor_no_formato(nome_final, "R$0000,00")
assert not termina_com_sufixo_desempate(nome_final)       # (2), _v2, _novo
if nome_original_preservado: assert nome_final == nome_original_do_documento

# 3. Destino
assert pasta_corresponde_a_estrutura_oficial_do_setor
if setor == FISCAL:
    assert usa_apenas_pasta_do_regime_do_cliente
    assert tipo_documento_compativel_com_regime  # DAS=Simples, MIT=Presumido, Controle Créditos=Real
if categoria == "relatorio_analitico_contas_a_pagar":
    assert nome_original_preservado == true
assert nome_banco_operadora_fornecedor == forma_canonica_exata(Dicionário §5)  # grafia divergente = erro

# 5. Duplicidade e colisão
assert nao_ha_dois_itens_com_mesmo_destino_final_mais_nome_final
assert nome_final_nao_colide_com_arquivo_pre_existente_no_destino
flag_se_hash_origem_ja_no_manifesto_e_recopiado

# 6. Exceções
for item in itens_naoident_ou_duplicado:
    assert item.motivo in lista_secao_4_3_dicionario and motivo_especifico
    assert item_existe_em("NÃO IDENTIFICADOS/<id_execucao>/") and nao_existe_mais_na_origem
for item in itens_fora_do_escopo_ou_pdf_composto:
    assert item.status_nao_foi_alterado  # não foram movidos

# 6b. Vocabulário de estado
assert status_e_veredito_e_motivo_sao_vocabularios_distintos_nunca_misturados
# violação aqui -> motivo=VIOLACAO_DE_CONTRATO, aborta execução (não é erro comum)

# 7. Pastas novas
listar_pastas_com(pasta_cliente_existe=false, cnpj_autorizante)
assert criacao_foi_por_cnpj_nunca_por_match_de_nome

# 8. Itens intocados
for item in itens_fora_do_escopo_ou_pdf_composto:
    assert item.caminho_atual == item.caminho_original
    assert item.hash_atual == item.hash_original
```

Qualquer `assert` falso vira uma linha em "Erros críticos" no relatório de saída (mesmo
formato do doc 06 original). Zero LLM envolvido nesta parte.
</procedimento>

<procedimento titulo="Parte B — Reclassificação independente (subagente `reclassificador`, por item ou em lote)">
Roda no subagente `reclassificador` (`.claude\agents\reclassificador.md`), despachado pelo
Orquestrador na Fase 5. **Passe apenas `id_item` e o caminho do arquivo — nunca a categoria
atribuída.**

Antes, essa verificação rodava na mesma sessão que já havia classificado o documento, e
"ignore a categoria anterior" era só uma instrução: o raciocínio da classificação original
continuava no contexto, puxando pra confirmar por inércia justamente no caso em que a
verificação mais importa. No subagente a independência é estrutural — ele não tem acesso à
categoria atribuída, então não há o que ignorar. O texto abaixo permanece como a
especificação do que o subagente faz; a comparação `atribuída × rederivada` acontece fora
dele, no Orquestrador.

Especificação aplicada pelo subagente:

```
Releia o cabeçalho/título deste documento (para XML: tags <mod>, <CFOP>, <emit>) e
derive a categoria do zero. Você não recebe a categoria atribuída: o objetivo é
derivar de forma independente para permitir refutação, não confirmar por inércia.

Aplique as tabelas de desambiguação do Dicionário §6 e docs de regime:
- BANCÁRIOS × MAQUININHAS × RECEBIMENTO DE CLIENTES × APLICAÇÕES
- DAS × DAE × DARF × DAPI
- EMITIDOS × RECEBIDOS (CNPJ emitente × CNPJ cliente)
- ESPECÍFICOS só com evidência no documento, nunca pelo ramo do cliente

Atenção: título "Comprovante" com múltiplas transações ou coluna de saldo = BANCÁRIOS,
não COMPROVANTES, mesmo que o cabeçalho diga literalmente "Comprovante" (Dicionário §6.1.1).
BANCÁRIOS × RECEBIMENTO DE CLIENTES têm nomes finais quase idênticos — é o ponto cego
estrutural do sistema, redobre a atenção.

Retorne: {id_item, categoria_rederivada, divergente_da_atribuida: bool}
```

Junte a saída da Parte B como mais uma linha de "Erros críticos" quando `divergente=true`,
e monte a seção "Reclassificação por arquivo" do relatório final (atribuída × rederivada ×
divergência) a partir daqui.
</procedimento>

<decisao titulo="Decisão final (código, junta A+B)">
```
if ha_qualquer_erro_critico_aberto (de A ou B):
    if corrigivel_automaticamente_com_dado_suficiente: CORRIGIR_E_REVERIFICAR
    elif bloqueio_tecnico (permissão/caminho/planilha/coluna_REGIME_ausente): FALHA_DE_INFRAESTRUTURA
else:
    OK_PARA_CONCLUIR
```
Nunca `OK_PARA_CONCLUIR` com erro crítico pendente — a exclusão da origem depende disso.
</decisao>

<eficiencia titulo="Ganho">
Antes: 1 chamada de LLM cobrindo 8 verificações por item (muito conteúdo de regra
carregado toda vez, a maior parte dele nunca usada para julgamento real).
Depois: 0 chamadas de LLM para 7 das 8 verificações (Parte A, roda como código na sessão
principal) + 1 subagente enxuto por item ou lote (Parte B, só a regra de reclassificação).
Nenhuma regra foi removida — todas as 8 verificações do doc 06 original continuam ativas,
só mudou onde cada uma roda.

Ganho adicional da Parte B em subagente: além de não gastar contexto da sessão principal
com o conteúdo do documento, a reclassificação passou a ser **independente de fato** — o
subagente não recebe a categoria atribuída, então não existe mais o viés de confirmar por
inércia o que a mesma sessão já havia decidido.
</eficiencia>

</agente>
