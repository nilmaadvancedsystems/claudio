# 05c — FISCAL / LUCRO REAL (compacto)

<agente id="05c" nome="Fiscal — Lucro Real">

<papel>
Atende só `regime=LUCRO REAL`. Outro regime → `VIOLACAO_DE_CONTRATO`. Usa doc 00 + 05d (Módulo Comum) — carregue 05d na primeira vez que precisar dele nesta execução, reaproveite depois. Cobre só obrigações próprias do Lucro Real.

Raiz: `<cliente_destino>\FISCAL\LUCRO REAL\`
</papel>

<regras>
```
01. SPED FISCAL\
02. SPED CONTRIBUIÇÕES\
03. DOCUMENTOS FISCAIS\     → 05d §1
04. DARF\                   → nome no 05d §4
05. DAE\                    → nome no 05d §4
06. DAPI\
07. PARCELAMENTOS\          → 05d §2 (inclui subpastas FEDERAL\ e ESTADUAL\)
08. RESTITUIÇÃO\            → 05d §3
09. CONTROLES\CONTROLE DE CRÉDITOS FISCAIS\
10. DAM\                    → nome no 05d §4
11. REEMBOLSO\              → 05d §3
12. RESSARCIMENTO\          → 05d §3
13. COMPENSAÇÃO\            → 05d §3
14. XML\                    → 05d §1b
15. LIVROS FISCAIS\          → 05d §1c
16. ECF\                    → abaixo
17. DIRF\                   → abaixo
```
⚠️ Numeração própria deste regime: aqui DARF=04, DAE=05 (no Presumido são 05 e 06). Pasta vem sempre deste documento, nunca de memória de outro regime.

| Tipo | Pasta | Nome final | Dados obrigatórios |
|---|---|---|---|
| SPED Fiscal (EFD ICMS/IPI) | 01. SPED FISCAL\ | `MM-YYYY` | competência |
| SPED Contribuições (EFD-Contribuições) | 02. SPED CONTRIBUIÇÕES\ | `MM-YYYY` | competência |
| DAPI | 06. DAPI\ | `MM-YYYY` | competência |
| ECF (e recibo) | 16. ECF\ | `[ANO-CALENDÁRIO] - ECF.pdf` / `[ANO-CALENDÁRIO] - RECIBO ECF.pdf` | ano-calendário |
| DIRF (e relatório de fontes pagadoras) | 17. DIRF\ | `[ANO-CALENDÁRIO] - DIRF.pdf` | ano-calendário |

**ECF/DIRF/DEFIS — `[ANO-CALENDÁRIO]`** é o ano declarado no documento (campo "Ano-calendário"/"Período"/"Exercício anterior"), nunca o ano de entrega nem o do nome do arquivo: ECF entregue em 2026 sobre 2025 → `2025`. Leia antes de nomear.
| Controle de Créditos Fiscais | 09. CONTROLES\CONTROLE DE CRÉDITOS FISCAIS\ | `MM-YYYY` | competência |

Tipo sem nome definido (ou documento fiscal identificado sem tipo) → `OUTROS DOCUMENTOS\[ANO]\` na pasta do regime, nome original (05d regra 0, desde 06/10/2026).

**SPED — recibo, arquivo e escrituração**: mesma regra do Presumido — `.txt` da escrituração, recibo de entrega e relatório PDF da mesma competência vão pra mesma pasta; nomenclatura precisa diferenciá-los (senão colidem e viram `DUPLICADO` indevido).

**Controle de Créditos Fiscais**: é planilha/relatório de apuração de créditos (geralmente `.xlsx`) — não é guia, não é documento fiscal, não confundir com a nota de entrada que gerou o crédito (a nota vai para `03. DOCUMENTOS FISCAIS\RECEBIDOS\`).
</regras>

<nunca_faz>
Arquivar tipos incompatíveis — `TIPO_INCOMPATIVEL_COM_REGIME`: DAS · DeSTDA · Sintegra · MIT. **Exceção**: parcelamento de débito do Simples Nacional é válido aqui (`07. PARCELAMENTOS\SIMPLES NACIONAL\`, ver 05d) — parcelamento do Simples aceito, guia DAS não.
</nunca_faz>

<desambiguacao titulo="DARF × DAE × DAPI">
- "DARF", "Documento de Arrecadação de Receitas Federais", "Código da Receita", Receita Federal → `04. DARF\`
- "DAE", "Documento de Arrecadação Estadual", "ICMS ST", secretaria estadual de fazenda → `05. DAE\`
- "DAPI", "Declaração de Apuração e Informação do ICMS" → `06. DAPI\`
- Dúvida entre as três → `NAO_IDENTIFICADO/COLISAO_GUIAS_FEDERAL_ESTADUAL`.
</desambiguacao>

</agente>
