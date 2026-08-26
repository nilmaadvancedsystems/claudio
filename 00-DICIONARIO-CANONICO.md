00 — DICIONÁRIO CANÔNICO

<dicionario>

<papel>
Documento de referência compartilhado. Todo agente carrega este documento antes de agir. Ele é a única fonte de verdade para formatos, vocabulário e caminhos. Nenhum agente pode inventar um valor que deveria estar aqui: se o valor necessário não consta, o item recebe motivo VOCABULARIO_AUSENTE e o log registra o pedido de inclusão.
</papel>

<secao n="1" titulo="CAMINHOS FIXOS">
Papel
	Caminho
	Origem
	G:\Meu Drive\Claudio Secretario
	Raiz de clientes
	G:\Meu Drive\2026
	Não identificados
	G:\Meu Drive\Claudio Secretario\NÃO IDENTIFICADOS
	Staging (fragmentos de PDF, modo PRODUCAO)
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\STAGING
	Staging de simulação (fragmentos de PDF, modo SIMULACAO)
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\STAGING-SIMULACAO
	Quarentena de exclusão (retenção de 7 dias antes de apagar em definitivo)
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\BACKUP ROTINA\<DD-MM-AAAA>
	Logs de auditoria
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\LOGS\AUDITORIA
	Manifesto
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\MANIFESTO\manifesto.jsonl
	Logs de execução
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\LOGS
	Dados de referência (planilhas de cliente)
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\necessario para o claude\dados agentes
	Exemplos de Referência
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\necessario para o claude\dados agentes\EXEMPLOS DE ARQUIVOS
	Agentes (prompts locais)
	G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\necessario para o claude\agentes
	

Regra de varredura da origem: a varredura é RECURSIVA — entra em qualquer subpasta dentro da origem, em qualquer profundidade, e trata cada arquivo encontrado como um item próprio (arquivo_original), igual a um arquivo solto na raiz. A estrutura de subpasta não importa para a classificação — o Roteador e os Especialistas decidem pelo conteúdo do documento, não pelo caminho onde ele estava. Excluídas da varredura, em qualquer profundidade: a própria pasta NÃO IDENTIFICADOS, CLAUDE FAVOR NÃO MEXER (e tudo dentro dela, inclusive _CLAUDIO_CONTROLE) e qualquer pasta iniciada por _.

Regra de extração de .zip: um arquivo `.zip` encontrado na varredura não vira item direto — é extraído para `STAGING\<id_execucao>\` (Fase 1b do Orquestrador, procedimento mecânico). Cada arquivo extraído vira item próprio, apontando para o `.zip` como `arquivo_original` — mesmo modelo já usado para PDF composto: o `.zip` só sai da origem (via Executor) quando todos os itens extraídos dele estiverem resolvidos. Se um arquivo extraído for ele mesmo um `.zip`, extraia de novo, recursivamente, até não sobrar `.zip`.

Regra de escrita: arquivos de cliente só podem ser gravados dentro de G:\Meu Drive\2026. CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE é área de controle da própria rotina e não é destino de arquivo de cliente.

Regra de quarentena: o Executor de Exclusão (08) nunca apaga o arquivo original em definitivo — ele move para BACKUP ROTINA\<DD-MM-AAAA>\, preservando o caminho relativo do arquivo dentro da origem (evita colisão de nome entre clientes diferentes movidos no mesmo dia), onde <DD-MM-AAAA> é a data da própria execução. Arquivo em quarentena é recuperável manualmente por até 7 dias corridos. A purga definitiva (apagar a pasta-dia inteira) roda na Fase 0 de toda execução PRODUCAO, antes de processar qualquer arquivo novo: qualquer pasta-dia cuja data tenha mais de 7 dias corridos é apagada por completo. BACKUP ROTINA está fora da árvore de origem (dentro de CLAUDE FAVOR NÃO MEXER) e por isso nunca é reprocessada como item novo.

Regra de identificação por exemplos: a pasta "Exemplos de Referência" contém modelos reais de arquivo por banco/operadora (hoje: BANCO DO BRASIL, BNB, BRADESCO, CAIXA, INFINITEPAY, ITAÚ, MERCADO PAGO, NUBANK, PAGBANK, SANTANDER, SICOOB). Consulte no máximo **uma vez por banco/operadora por execução** (na primeira vez que um documento daquele emissor aparecer, ou se surgir dúvida real de classificação) — não releia o exemplo a cada documento novo do mesmo emissor na mesma execução, o gabarito não muda no meio da execução.

Regra de índice de NÃO IDENTIFICADOS: toda vez que um item vira `NAO_IDENTIFICADO`/`DUPLICADO` e é movido pelo Orquestrador (Fase 4b), grave também uma linha em `NÃO IDENTIFICADOS\<id_execucao>\_nao_identificados.jsonl` (ver §10) — sem isso, depois de alguns dias ninguém sabe por que um arquivo específico está ali sem abrir relatório antigo.
</secao>

<secao n="2" titulo="FORMATOS OBRIGATÓRIOS">
Token
	Formato
	Exemplo
	[MÊS E ANO]
	MM-AAAA
	07-2026
	[DATA]
	DD-MM-AAAA
	30-04-2026
	[VENCIMENTO]
	DD-MM-AAAA
	20-08-2026
	[PERÍODO]
	MM-AAAA (competência apurada)
	07-2026
	[ANO]
	AAAA
	2026
	[MÊS] (pasta)
	MM
	07
	[VALOR]
	R$ + inteiro + vírgula + 2 decimais, sem separador de milhar
	R$29680,50
	[CNPJ]
	14 dígitos, sem pontuação
	07613875000108
	[Nº CONTRATO]
	dígitos e hífens como no documento, sem espaços
	123-456789
	[NÚMERO DO LIVRO]
	3 dígitos, com zeros à esquerda
	001
	[TRIBUTO]
	sigla em maiúsculas, sem pontuação
	IRPJ, CSLL, PIS, COFINS, INSS
	[SÉRIE] / [NÚMERO]
	dígitos como no documento, sem zeros à esquerda adicionais
	1 / 4471
	

Qualquer desvio destes formatos é erro crítico na auditoria. Token usado em alguma regra e ausente desta tabela é defeito do sistema — reporte VOCABULARIO_AUSENTE em vez de improvisar um formato.

Regra de numeração em nome duplicado: quando o nome final gerado por template (ex.
`[MÊS E ANO].pdf`) já existir no destino com um `hash_destino` diferente do que está sendo
gravado agora (documento diferente, mesmo nome — comum em Comprovantes, onde é normal ter
mais de um por mês), acrescente um contador antes da extensão: ` (1)`, ` (2)`, ... — teste
em ordem crescente a partir de 1 até achar o primeiro nome livre naquela pasta. Nunca
sobrescreva um arquivo existente para resolver a colisão. Isso vale para qualquer categoria
onde o nome final é gerado por competência, não só Comprovantes. Motivo
CONFLITO_MESMO_NOME_CONTEUDO_DIFERENTE passa a ser informativo (registra que houve
renumeração), não bloqueio — ver §4.4 E402.
</secao>

<secao n="2.1" titulo="REGIME — enum fechado e fonte de dados">
Fonte: G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\necessario para o claude\dados agentes\regime.xls
(colunas: ERP, Cliente, Enquadramento — ERP é o mesmo código da coluna "Código" do
razão social.PDF/nome fantasia.PDF; é assim que Roteador cruza cliente → regime).

Enquadramento (planilha)
	Regime canônico
	Simples
	SIMPLES NACIONAL
	Presumido
	LUCRO PRESUMIDO
	Real
	LUCRO REAL
	MEI
	MEI
	Física
	PESSOA FISICA
	Isentas
	ISENTA
	Domésticas
	DOMESTICA

Nunca use o texto da planilha diretamente — sempre normalize para o valor canônico
desta tabela. Valor da planilha fora desta lista → NAO_IDENTIFICADO, motivo
VOCABULARIO_AUSENTE (regime novo, decisão humana antes de adicionar aqui).

MEI, PESSOA FISICA, ISENTA e DOMESTICA ainda não têm sub-especialista com regras de
documento definidas (só SIMPLES NACIONAL/LUCRO PRESUMIDO/LUCRO REAL têm, via 05a/05b/05c).
Até existirem: item com um desses 4 regimes → FORA_DO_ESCOPO, motivo
REGIME_SEM_ESPECIALISTA. Intocado na origem, mesmo tratamento dado a setor sem
especialista.
</secao>

<secao n="3" titulo="LIMIARES E PARÂMETROS">
Parâmetro
	Valor
	Confiança mínima do Roteador
	0.85 — abaixo disso, NAO_IDENTIFICADO
	Confiança mínima do Separador para cortar um PDF
	0.90
	Máximo de ciclos CORRIGIR_E_REVERIFICAR
	3
	Algoritmo de hash
	SHA-256
	Retenção da quarentena de exclusão
	7 dias corridos, contados a partir da data da pasta-dia
	Limiar de adiamento de purga
	pasta-dia com mais arquivos que 3× a média das últimas 5 purgas realizadas (mínimo absoluto de 30 arquivos se não houver histórico) → adia a purga daquela pasta em +5 dias, no máximo 2 adiamentos (17 dias de retenção total no pior caso, depois disso purga mesmo sem confirmação humana)
	Limiar de envelhecimento de pendência (só AUDITORIA)
	item em NÃO IDENTIFICADOS ou fragmento em STAGING parado há mais de 7 dias corridos desde a data embutida no nome da pasta de execução → achado PENDENCIA_ENVELHECIDA
	Limiar de disjuntor de qualidade de roteamento
	`nao_identificados_count` desta execução maior que 3× a média das últimas 5 execuções registradas em `MANIFESTO\qualidade.jsonl` (mínimo absoluto de 10 itens se não houver histórico) → sinaliza VOLUME_NAO_IDENTIFICADO_INCOMUM com destaque no relatório e no e-mail. Nunca trava a execução nem impede o fechamento.
	
</secao>

<secao n="4" titulo="VOCABULÁRIO DE ESTADO">
São três vocabulários distintos. Não os misture: um status de item nunca aparece como veredito, e um código de motivo nunca aparece no campo status.

<subsecao n="4.1" titulo="STATUS DE ITEM — enum fechado">
Descreve o que aconteceu com um arquivo. Nenhum agente pode criar valor fora desta lista.

Status
	Significado
	Arquivo fica onde
	PENDENTE
	ainda em processamento
	—
	ARQUIVADO
	copiado ao destino e integridade confirmada
	destino
	DUPLICADO
	já existe no destino com mesmo nome
	origem → NÃO IDENTIFICADOS
	NAO_IDENTIFICADO
	não classificável, dado essencial ausente, vocabulário ausente
	origem → NÃO IDENTIFICADOS
	FORA_DO_ESCOPO
	setor ou tipo sem regra ativa nesta fase
	intocado na origem
	PDF_COMPOSTO_NAO_SEPARADO
	PDF múltiplo cujos limites não puderam ser determinados
	intocado na origem
	JA_ARQUIVADO_ANTERIORMENTE
	manifesto registra arquivamento prévio, confirmado no destino
	destino (já lá)
	FALHA_INTEGRIDADE
	cópia no destino não confere com a origem
	origem (nunca excluir)
	NAO_ELEGIVEL
	não atendeu ao portão de exclusão
	origem
	EXCLUIDO_DA_ORIGEM
	ciclo completo, original removido da origem e movido para quarentena (BACKUP ROTINA, 7 dias corridos antes da purga definitiva)
	destino (cópia) + quarentena (original, temporário)
	FALHA_AO_EXCLUIR
	exclusão tentada e falhou
	origem e destino
	

Quem move um arquivo para NÃO IDENTIFICADOS é sempre o Orquestrador (Fase 4b), nunca o agente que detectou o problema. O agente 10 (Arquivista de Exceções) foi descontinuado; suas funções mecânicas foram absorvidas pelo Orquestrador. Toda movimentação também grava uma linha em `_nao_identificados.jsonl` (§10), dentro da própria subpasta de execução.
</subsecao>

<subsecao n="4.2" titulo="VEREDITOS DE EXECUÇÃO — enum fechado">
Descreve o estado do lote, não de um arquivo. Produzidos pelo Verificador e pelo Orquestrador.

Veredito
	Significado
	OK_PARA_CONCLUIR
	nenhum erro crítico aberto; exclusão liberada
	CORRIGIR_E_REVERIFICAR
	há desvio corrigível; reprocessar e auditar de novo
	FALHA_DE_INFRAESTRUTURA
	bloqueio técnico (permissão, caminho, planilha ilegível)
	FALHA_DE_CONVERGENCIA
	3 ciclos de correção sem resolver; escalar ao humano
	

Nenhum veredito autoriza exclusão exceto OK_PARA_CONCLUIR.
</subsecao>

<subsecao n="4.3" titulo="CÓDIGOS DE MOTIVO — lista aberta">
Preenchem o campo motivo, obrigatório sempre que status ≠ ARQUIVADO. Esta lista é extensível: um agente pode criar um código novo, em MAIÚSCULAS_COM_UNDERSCORE, desde que seja específico. Motivo genérico ("não identificado") é insuficiente.

Roteamento: CLIENTE_NAO_LOCALIZADO · CLIENTE_AMBIGUO · PLANILHAS_DIVERGENTES · REGIME_INDEFINIDO · SETOR_INDETERMINADO · CONFIANCA_ABAIXO_DO_LIMIAR · SETOR_SEM_ESPECIALISTA · REGIME_SEM_ESPECIALISTA · VOLUME_NAO_IDENTIFICADO_INCOMUM (nível execução, não item — ver §3)

Classificação: VOCABULARIO_AUSENTE · TIPO_INCOMPATIVEL_COM_REGIME · NOMENCLATURA_NAO_DEFINIDA · DESTINO_NAO_DEFINIDO · EMITENTE_INDETERMINADO · COLISAO_BANCARIO_RECEBIMENTO · COLISAO_DAS_DAE · COLISAO_GUIAS_FEDERAL_ESTADUAL

Dados ausentes: CONTRATO_SEM_NUMERO · LIVRO_SEM_NUMERO · COMPETENCIA_AUSENTE · VALOR_AUSENTE · BANCO_AUSENTE · TIPO_AUSENTE · CONTEUDO_ILEGIVEL

Duplicidade: IDENTICO_JA_ARQUIVADO · CONFLITO_MESMO_NOME_CONTEUDO_DIFERENTE (uso restrito — ver regra de numeração automática em §2)

Integridade: DESTINO_INEXISTENTE · DESTINO_VAZIO · TAMANHO_DIVERGENTE · HASH_DIVERGENTE · ARQUIVO_CORROMPIDO · ORIGEM_ALTERADA_DURANTE_EXECUCAO · MANIFESTO_DESATUALIZADO

Exclusão: HASH_MUDOU_ANTES_DA_EXCLUSAO · DESTINO_NAO_CONFIRMAVEL · EXCLUSAO_NAO_EFETIVADA · ITEM_PENDENTE · PURGA_ADIADA_VOLUME_INCOMUM · PASTA_QUARENTENA_DATA_INVALIDA · PENDENCIA_ENVELHECIDA

Separação: SEPARACAO_AMBIGUA · PAGINAS_NAO_COBREM_O_ORIGINAL

Simulação: SIMULACAO_SEM_DESTINO · SIMULACAO_SEM_FRAGMENTO

Sistema: VIOLACAO_DE_CONTRATO — um agente recebeu ou devolveu campo fora do contrato. Ao receber este motivo de qualquer agente, o Orquestrador aborta a execução e não aciona exclusão. Não é defeito de documento; é defeito de pipeline.
</subsecao>

<subsecao n="4.4" titulo="CATÁLOGO DE CÓDIGOS — referência rápida">
Cada motivo da seção 4.3 tem um código curto correspondente, pra facilitar identificar e comunicar um problema sem precisar escrever o nome inteiro (ex.: "deu E504" em vez de "deu HASH_DIVERGENTE"). O código é só uma etiqueta de apresentação — o agente continua usando o nome completo internamente; o código aparece pro humano no relatório (Relator, seção "Legenda de códigos").

Faixa por categoria: E1xx Roteamento · E2xx Classificação · E3xx Dados ausentes · E4xx Duplicidade · E5xx Integridade (mais grave) · E6xx Exclusão · E7xx Separação · E8xx Simulação (não é erro) · E9xx Sistema (aborta execução).

Código | Motivo | O que significa, em uma linha | Ação esperada
E101 | CLIENTE_NAO_LOCALIZADO | Nenhum cliente bateu com os dados do documento | Cadastrar cliente ou revisar CNPJ manualmente
E102 | CLIENTE_AMBIGUO | Nome bate com mais de um cliente, sem CNPJ pra desempatar | Confirmar manualmente qual cliente é
E103 | PLANILHAS_DIVERGENTES | As duas fontes de cliente discordam em código/CNPJ | Corrigir a planilha divergente
E104 | REGIME_INDEFINIDO | Documento fiscal de cliente sem regime tributário cadastrado | Cadastrar regime na planilha
E105 | SETOR_INDETERMINADO | Não deu pra saber se é Contábil, Fiscal ou Folha/Societário | Revisar manualmente o tipo de documento
E106 | CONFIANCA_ABAIXO_DO_LIMIAR | O sistema teve dúvida real (abaixo de 85% de certeza) | Revisar manualmente
E107 | SETOR_SEM_ESPECIALISTA | Setor identificado, mas ainda sem regra de arquivamento (Folha/Societário) | Nenhuma — aguardando regra ser criada
E108 | REGIME_SEM_ESPECIALISTA | Regime identificado (MEI/Física/Isenta/Doméstica), mas ainda sem regra de arquivamento | Nenhuma — aguardando regra ser criada
E109 | VOLUME_NAO_IDENTIFICADO_INCOMUM | Esta execução gerou muito mais NAO_IDENTIFICADO que o normal — possível bug na classificação, não erro de documento individual | **Investigar** — revisar itens não identificados desta execução e a regra de roteamento antes da próxima execução
E201 | VOCABULARIO_AUSENTE | Banco, fornecedor ou termo não reconhecido | Adicionar ao vocabulário do Dicionário, se for caso recorrente
E202 | TIPO_INCOMPATIVEL_COM_REGIME | Tipo de guia fiscal não existe no regime desse cliente | Confirmar regime do cliente ou se o documento é de outro cliente
E203 | NOMENCLATURA_NAO_DEFINIDA | Tipo de documento reconhecido, mas sem regra de nome de arquivo ainda | Nenhuma — aguardando regra ser criada
E204 | DESTINO_NAO_DEFINIDO | Tipo de documento sem pasta de destino definida | Nenhuma — aguardando regra ser criada
E205 | EMITENTE_INDETERMINADO | Não deu pra saber quem emitiu o documento | Revisar manualmente
E206 | COLISAO_BANCARIO_RECEBIMENTO | Dúvida entre extrato bancário e recebimento de cliente | Revisar manualmente pelo título do documento
E207 | COLISAO_DAS_DAE | Dúvida entre guia DAS e guia DAE | Revisar manualmente pelo órgão emissor
E208 | COLISAO_GUIAS_FEDERAL_ESTADUAL | Dúvida entre DARF, DAE e DAPI | Revisar manualmente pelo órgão emissor
E301 | CONTRATO_SEM_NUMERO | Número do contrato não aparece no documento | Revisar o documento manualmente
E302 | LIVRO_SEM_NUMERO | Número do livro contábil não aparece no documento | Revisar o documento manualmente
E303 | COMPETENCIA_AUSENTE | Mês/ano de referência não aparece no documento | Revisar o documento manualmente
E304 | VALOR_AUSENTE | Valor obrigatório não aparece no documento | Revisar o documento manualmente
E305 | BANCO_AUSENTE | Banco não identificável no documento | Revisar o documento manualmente
E306 | TIPO_AUSENTE | Tipo de operação (consórcio/empréstimo/financiamento) não identificável | Revisar o documento manualmente
E307 | CONTEUDO_ILEGIVEL | PDF escaneado sem texto extraível, arquivo corrompido, ou conteúdo insuficiente pra classificar | Revisar o documento manualmente — pode precisar de OCR ou substituição do arquivo
E401 | IDENTICO_JA_ARQUIVADO | Já existe cópia idêntica no destino | Nenhuma — duplicata real, pode ignorar
E402 | CONFLITO_MESMO_NOME_CONTEUDO_DIFERENTE | Nome gerado já existia com conteúdo diferente | Nenhuma — sistema renomeou sozinho acrescentando "(N)" (ver §2, regra de numeração); revisar só se o padrão se repetir excessivamente no mesmo mês
E501 | DESTINO_INEXISTENTE | Arquivo devia estar no destino mas não está | **Investigar antes de confiar na exclusão** — chamar responsável técnico
E502 | DESTINO_VAZIO | Arquivo no destino está com 0 bytes | **Investigar** — chamar responsável técnico
E503 | TAMANHO_DIVERGENTE | Tamanho da cópia não bate com o original | **Investigar** — chamar responsável técnico
E504 | HASH_DIVERGENTE | Conteúdo da cópia não é idêntico ao original | **Investigar** — chamar responsável técnico
E505 | ARQUIVO_CORROMPIDO | Arquivo no destino não abre corretamente | **Investigar** — chamar responsável técnico
E506 | ORIGEM_ALTERADA_DURANTE_EXECUCAO | Algo mexeu no arquivo original durante a execução | **Investigar** — chamar responsável técnico
E507 | MANIFESTO_DESATUALIZADO | Registro de arquivamento anterior não bate mais com a realidade | Sistema reprocessa sozinho, sem ação necessária
E601 | HASH_MUDOU_ANTES_DA_EXCLUSAO | Original mudou entre a conferência e a tentativa de apagar | **Investigar** — chamar responsável técnico
E602 | DESTINO_NAO_CONFIRMAVEL | Não deu pra confirmar que a cópia existe antes de apagar o original | **Investigar** — chamar responsável técnico
E603 | EXCLUSAO_NAO_EFETIVADA | Tentou apagar o original e não conseguiu (bloqueio/permissão) | Apagar manualmente depois de conferir
E604 | ITEM_PENDENTE | Um documento derivado do mesmo arquivo ainda não terminou de processar | Nenhuma — resolve sozinho quando o pendente terminar
E605 | PURGA_ADIADA_VOLUME_INCOMUM | Uma pasta-dia da quarentena tinha volume incomum de arquivos e a purga definitiva foi adiada por segurança | Revisar a pasta-dia indicada antes que os adiamentos se esgotem
E606 | PASTA_QUARENTENA_DATA_INVALIDA | Nome de pasta-dia da quarentena não bate com o formato DD-MM-AAAA esperado | **Investigar** — chamar responsável técnico, pasta não foi purgada por segurança
E607 | PENDENCIA_ENVELHECIDA | Item em NÃO IDENTIFICADOS ou fragmento em STAGING parado há mais de 7 dias sem ação (achado só de AUDITORIA) | Revisar manualmente — decidir se arquiva, corrige a regra que travou, ou descarta
E701 | SEPARACAO_AMBIGUA | PDF com mais de um documento dentro, mas sem certeza de onde cortar | Revisar manualmente e separar à mão se necessário
E702 | PAGINAS_NAO_COBREM_O_ORIGINAL | Fragmentos de um PDF separado não cobrem todas as páginas do original | Revisar manualmente
E801 | SIMULACAO_SEM_DESTINO | Só ocorre em modo teste — não é erro real | Nenhuma
E802 | SIMULACAO_SEM_FRAGMENTO | Só ocorre em modo teste — não é erro real | Nenhuma
E901 | VIOLACAO_DE_CONTRATO | Um agente devolveu dado fora do formato esperado — bug do sistema, não do documento | **Parar e chamar responsável técnico**
</subsecao>
</secao>

<secao n="5" titulo="VOCABULÁRIO DE ENTIDADES">
<subsecao n="5.1" titulo="BANCOS E OPERADORAS — lista fechada">
Conjunto finito e estável. O nome da pasta é exatamente o texto da coluna "Canônico". Nunca use a grafia do documento.

Canônico
	Grafias aceitas no documento
	SICOOB
	Sicoob, SICOOB, Sistema Sicoob, Sicoob + qualquer sufixo de singular
	BNB
	BNB, Banco do Nordeste, Banco do Nordeste do Brasil, Banco do Nordeste S.A.
	BRADESCO
	Bradesco, Banco Bradesco, Bradesco S.A.
	ITAU
	Itaú, Itau, Banco Itaú, Itaú Unibanco
	BANCO DO BRASIL
	Banco do Brasil, BB, B. do Brasil
	CAIXA
	Caixa, CEF, Caixa Econômica Federal
	SANTANDER
	Santander, Banco Santander
	SICREDI
	Sicredi, Sistema Sicredi
	BANESE
	Banese
	BANRISUL
	Banrisul
	SAFRA
	Safra, Banco Safra
	INTER
	Inter, Banco Inter
	NUBANK
	Nubank, Nu Pagamentos
	C6
	C6, C6 Bank
	MERCADO PAGO
	Mercado Pago, MercadoPago, Mercado Pago IP
	PAGBANK
	PagBank, PagSeguro, PagSeguro Internet IP
	STONE
	Stone, Stone Pagamentos, Stone IP
	CIELO
	Cielo, Cielo S.A.
	REDE
	Rede, Redecard, Rede Itaú, Itaú Rede (operadora de maquininha ligada ao Itaú — documento pode trazer marca "Itaú" mas continua sendo REDE, não ITAU: emissor não decide categoria, ver §6.1)
	GETNET
	Getnet
	INFINITEPAY
	InfinitePay, Infinite Pay
	SUMUP
	SumUp
	

Emissor fora desta tabela: NAO_IDENTIFICADO, motivo VOCABULARIO_AUSENTE: <nome lido no documento>. Nunca crie pasta com nome novo — incluir um banco é decisão humana, e a lista é curta o bastante para isso ser viável.
</subsecao>

<subsecao n="5.2" titulo="FORNECEDORES, CLIENTES E TRANSPORTADORAS — normalização">
Conjunto aberto: são centenas e mudam toda semana. Lista fechada aqui seria inexequível e travaria a rotina inteira. A regra é normalizar, não consultar lista.

Algoritmo, nesta ordem:

1. Tome a razão social como aparece no documento.
2. Converta para MAIÚSCULAS, preservando acentos.
3. Remova sufixos societários no fim do nome: LTDA, LTDA., ME, EPP, EIRELI, S.A., S/A, SA, CIA, & CIA, e o traço que os antecede.
4. Remova pontuação final, e colapse espaços duplos em um.
5. O resultado é o nome da pasta.

Exemplo: Mitra Transporte e Serviços Ltda - ME → MITRA TRANSPORTE E SERVIÇOS

Antes de criar pasta nova, liste as pastas já existentes no mesmo caminho ([ANO]\[MÊS]\) e aplique a mesma normalização a cada uma. Se alguma normalizar para o mesmo valor, use a pasta existente — não crie uma segunda.

Apelidos conhecidos (quando o mesmo fornecedor aparece com nomes que a normalização não unifica). Tabela extensível:

Canônico
	Também aparece como
	(preencher conforme surgirem)
	

Nome ilegível ou ausente no documento → NAO_IDENTIFICADO, motivo VOCABULARIO_AUSENTE. Aqui o motivo significa "não consegui ler o nome", não "não está numa lista".
</subsecao>
</secao>

<secao n="6" titulo="DESAMBIGUAÇÃO POR TIPO DE DOCUMENTO">
O emissor nunca decide a categoria. O título/cabeçalho do documento decide.

<subsecao n="6.1" titulo="BANCÁRIOS × MAQUININHAS × RECEBIMENTO DE CLIENTES × APLICAÇÕES">
REGRA DE DUPLO PAPEL (CONTA DIGITAL vs. ADQUIRENTE): fintechs e operadoras de maquininha (Mercado Pago, PagBank, Stone, Cielo, InfinitePay, Getnet, SumUp) não emitem só documento de maquininha — várias delas, InfinitePay incluída, também oferecem conta bancária digital completa (recebimento de PIX, pagamentos, transferências, saldo), igual a um banco tradicional. Nunca presuma a categoria pelo nome do emissor só porque ele é conhecido como "operadora de cartão". A decisão sempre vem do título/cabeçalho do documento — leia o título:

Título contém
	Categoria
	"Extrato de Conta", "Extrato Financeiro", "Extrato da Conta Digital", "Extrato de Conta Corrente"
	EXTRATOS/BANCÁRIOS
	"Relatório de Vendas", "Extrato de Liquidação", "Extrato de Recebíveis", "Resumo de Vendas no Cartão", "Vendas por Bandeira", "Relatório de Conciliação", "Conciliação de Vendas", "Relatório de Conciliação de Recebíveis"
	EXTRATOS/MAQUININHAS
	"Relatório de Recebimentos", "Títulos Liquidados", "Cobrança — Títulos Baixados", "Relatório de Cobrança"
	RECEBIMENTO DE CLIENTES
	"Extrato de Aplicação", "Extrato de Investimentos", "Posição de Investimentos", "Rendimentos de Aplicação"
	EXTRATOS/APLICAÇÕES
	"Comprovante de Pagamento", "Comprovante de Transferência", "Comprovante PIX"
	EXTRATOS/COMPROVANTES
	

"Relatório de Conciliação" (e variações) da maquininha usa exatamente o mesmo destino e a
mesma regra de nome final que o extrato comum de maquininha (ver
04-ESPECIALISTA-CONTABIL.md, linha Maquininhas): `MAQUININHAS\[OPERADORA]\[MÊS E ANO].pdf`.
Não é uma categoria à parte — é só mais um título aceito para a mesma categoria.

⚠️ BANCÁRIOS e RECEBIMENTO DE CLIENTES produzem nomes finais quase idênticos (banco + competência). Esta é a colisão de maior risco do sistema — a decisão precisa vir do título, nunca do emissor nem do nome do arquivo original.
</subsecao>

<subsecao n="6.1.1" titulo="Quando o título mente — critério de estrutura">
Alguns bancos nomeiam o extrato completo como "Comprovante" no próprio cabeçalho do documento — caso conhecido do Banco do Brasil, cujo extrato de movimentação de conta (várias transações, saldo corrente, intervalo de dias) é rotulado "Comprovante" ou "Comprovante de Movimentação". Aplicar a tabela 6.1 apenas pelo título classificaria isso incorretamente como COMPROVANTES.

Quando o título contiver "Comprovante" mas o conteúdo tiver características de extrato, decida pela estrutura, não pela palavra do cabeçalho:

Estrutura do conteúdo
	Categoria
	mesmo que o título diga
	Uma transação: uma data, um valor, um remetente/destinatário
	EXTRATOS/COMPROVANTES
	"extrato"
	Várias transações em sequência, coluna de saldo corrente, ou intervalo de dias cobrindo mais de uma operação
	EXTRATOS/BANCÁRIOS
	"Comprovante" / "Comprovante de Movimentação"
	

Este critério é o desempate, usado apenas quando o título por si só levaria à categoria errada. Para o caso comum (título claro e coerente com o conteúdo), a tabela 6.1 basta.
</subsecao>

<subsecao n="6.1.2" titulo="Quando a informação está em outra página — SANTANDER">
No SANTANDER, as informações que identificam o documento (título/cabeçalho, competência, titular) costumam estar na **página 2**, não na página 1 (a primeira página pode ser capa, propaganda ou resumo genérico sem esses dados). Antes de concluir VOCABULARIO_AUSENTE, EMITENTE_INDETERMINADO ou qualquer motivo de dado ausente num documento do Santander, verifique a página 2 do PDF — é lá que normalmente está o que falta. Não é exclusivo do Santander: se um documento de qualquer banco parecer sem informação suficiente na primeira página, checar as páginas seguintes antes de desistir é prática padrão, não exceção.
</subsecao>

<subsecao n="6.1.3" titulo="Quando não há título nenhum — planilha crua de conciliação de maquininha">
Algumas operadoras de maquininha exportam a conciliação como planilha sem título/cabeçalho de documento nenhum — só uma tabela de dados (ex.: colunas "Data da venda", "Valor bruto", "Taxa/tarifa", "Nota fiscal"). Nesse caso não há título pra aplicar a tabela 6.1 — decida pela estrutura das colunas: presença de colunas de **tarifa/taxa** junto com **débito/crédito** ou **valor bruto/valor líquido** (linguagem de liquidação de vendas de cartão, não de extrato bancário comum) é o sinal de que a planilha é conciliação de maquininha, mesmo sem nenhum texto de título. Classifique como EXTRATOS/MAQUININHAS, mesmo destino/nome do extrato comum da operadora (04-ESPECIALISTA-CONTABIL.md, linha Maquininhas) — nunca em APLICAÇÕES nem BANCÁRIOS só porque é uma planilha de números.

Este critério só vale quando não há título nenhum no documento. Havendo qualquer texto de cabeçalho, use a tabela 6.1 (ou 6.1.1 se o título for "Comprovante" mas a estrutura for de extrato) — este item aqui é o último recurso, para planilha sem nenhuma pista textual.
</subsecao>

<subsecao n="6.2" titulo="Informe de Rendimentos">
Ainda sem destino definido. Enquanto não houver decisão: FORA_DO_ESCOPO, motivo DESTINO_NAO_DEFINIDO: informe de rendimentos. Nunca alocar em APLICAÇÕES.
</subsecao>
</secao>

<secao n="7" titulo="MODO DE EXECUÇÃO">
Modo
	Comportamento
	SIMULACAO
	Nenhuma escrita definitiva (cópia em 2026, movimentação, exclusão, gravação de manifesto). PDFs compostos SÃO fragmentados normalmente — em staging próprio e exclusivo de simulação, nunca no staging real — permitindo simular a classificação completa, inclusive de documentos que precisariam ser separados primeiro. Todos os agentes calculam o que fariam e reportam. O Relator marca o relatório com "SIMULAÇÃO".
	PRODUCAO
	Execução real.
	AUDITORIA
	Não toca na origem nem processa arquivo novo. Varre o que já está arquivado em G:\Meu Drive\2026 procurando inconsistência (duplicidade de conteúdo, pasta fora do padrão canônico, arquivo não rastreado no manifesto, nomenclatura fora do padrão). Somente leitura — nunca move, renomeia, copia ou apaga. Ver 10-AUDITORIA.md.
	

A rotina roda de forma autônoma em PRODUCAO por padrão, inclusive na primeira execução em um cliente novo. SIMULACAO permanece disponível como modo opcional, para quando você quiser testar uma regra nova sem gravar nem excluir nada — mas nenhum agente deve exigi-lo. AUDITORIA roda sob demanda, não faz parte do ciclo diário automático.

Staging de simulação: os fragmentos gravados em STAGING-SIMULACAO durante uma execução SIMULACAO são sempre apagados ao final daquela mesma execução (Fase 8), independente de o item ter sido "resolvido" ou não — diferente do STAGING real de PRODUCAO, que preserva fragmentos de itens não resolvidos para a próxima execução. Simulação não tem estado a preservar entre execuções.
</secao>

<secao n="8" titulo="MANIFESTO — ESTRUTURA">
manifesto.jsonl, append-only, uma linha JSON por arquivo arquivado:

{"hash_origem":"<sha256>","hash_original":"<sha256>","nome_original":"<nome>","destino_final":"<caminho>","nome_final":"<nome>","id_execucao":"<id>","timestamp":"<ISO-8601>"}

Serve para: detectar reprocessamento após queda, evitar recópia, e permitir auditoria histórica de duplicidade contra execuções anteriores.
</secao>

<secao n="9" titulo="LOG DE PURGAS DA QUARENTENA — ESTRUTURA">
`G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\MANIFESTO\purgas.jsonl`, append-only,
uma linha por pasta-dia de `BACKUP ROTINA` avaliada na Fase 0 de cada execução
PRODUCAO (não só as purgadas — toda avaliação, inclusive adiada ou inválida, pra manter
histórico completo):

{"data_pasta":"<DD-MM-AAAA>","timestamp_avaliacao":"<ISO-8601>","arquivos_count":<N>,"resultado":"PURGADA|ADIADA|DATA_INVALIDA","adiamentos_acumulados":<N>,"id_execucao":"<id>"}

Serve para: dar ao disjuntor de volume (§3) uma base real de comparação. Antes de decidir
se a pasta-dia de hoje é "volume incomum", leia as últimas 5 linhas com
`resultado=PURGADA` e calcule a média de `arquivos_count` entre elas — sem histórico
suficiente (menos de 5 entradas), use o mínimo absoluto de 30 arquivos como limiar (§3).
Depois de decidir, grave uma linha nova para a pasta-dia avaliada, mesmo se o resultado for
`ADIADA` ou `DATA_INVALIDA` (essas não entram na média, mas registram o histórico).

Rotação: mesma regra do manifesto (§1 Rotação do manifesto, aplicada no Orquestrador) —
na primeira execução de um ano novo, `purgas.jsonl` atual vira `purgas-[ANO_ANTERIOR].jsonl`
(histórico, nunca apagado) e um `purgas.jsonl` vazio começa. A média do disjuntor de
volume só olha as últimas 5 entradas do arquivo ativo — não precisa consultar os
históricos, então a rotação nunca afeta essa conta.
</secao>

<secao n="10" titulo="LOG DE ÍNDICE DE NÃO IDENTIFICADOS — ESTRUTURA">
`NÃO IDENTIFICADOS\<id_execucao>\_nao_identificados.jsonl` (dentro da própria subpasta de
execução, um arquivo por execução — não um único arquivo global), append-only, uma linha
por item movido para `NAO_IDENTIFICADO`/`DUPLICADO` naquela execução:

{"arquivo":"<nome do arquivo movido>","status":"NAO_IDENTIFICADO|DUPLICADO","motivo":"<motivo>","cliente_tentativa":"<cliente_id ou null>","id_execucao":"<id>","timestamp":"<ISO-8601>"}

Serve para: permitir que qualquer pessoa abrindo a pasta `NÃO IDENTIFICADOS\<id_execucao>\`
entenda, sem procurar relatório antigo, por que cada arquivo ali está sem classificar. Não
precisa de rotação — cada execução já tem sua própria subpasta, o log nasce e morre com ela
(inclusive se a subpasta um dia for arquivada/limpa manualmente pelo responsável).
</secao>

<secao n="11" titulo="LOG DE QUALIDADE DE ROTEAMENTO — ESTRUTURA">
`G:\Meu Drive\CLAUDE FAVOR NÃO MEXER\_CLAUDIO_CONTROLE\MANIFESTO\qualidade.jsonl`,
append-only, uma linha por execução PRODUCAO, gravada ao final da Fase 4b:

{"id_execucao":"<id>","timestamp":"<ISO-8601>","N_pais":<N>,"nao_identificados_count":<N>,"alerta":"NENHUM|VOLUME_NAO_IDENTIFICADO_INCOMUM"}

Serve para: dar ao disjuntor de qualidade (§3) uma base real de comparação — leia as
últimas 5 linhas e calcule a média de `nao_identificados_count`; sem histórico suficiente,
use o mínimo absoluto de 10 itens (§3). O alerta nunca bloqueia a execução, só entra com
destaque no relatório e no e-mail daquela execução.

Rotação: mesma regra do manifesto e do purgas.jsonl — vira `qualidade-[ANO_ANTERIOR].jsonl`
na primeira execução de um ano novo. A média do disjuntor só usa as últimas 5 entradas do
arquivo ativo, então a rotação nunca afeta esse cálculo.
</secao>

</dicionario>
