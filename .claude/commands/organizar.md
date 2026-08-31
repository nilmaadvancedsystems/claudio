---
description: Executa a rotina de organização da pasta Claudio Secretario (Orquestrador)
argument-hint: [SIMULACAO|PRODUCAO|AUDITORIA]
---

Leia `_CLAUDIO_CONTROLE\necessario para o claude\agentes\01-ORQUESTRADOR.md` e execute a
rotina descrita nele do início ao fim, em modo `$1` (padrão: `SIMULACAO` se `$1` estiver vazio).

Siga a sequência de fases exatamente como escrita no arquivo, carregando cada agente
(00, 02-09, e 10 se `modo=AUDITORIA`) do caminho local indicado na seção "Mapa de
agentes" antes da fase correspondente. Se `modo=AUDITORIA`, siga a sequência própria do
10-AUDITORIA.md (não a sequência de 8 fases normal). Ao final, entregue o relatório
gerado pelo 09-RELATOR.md (ou pelo 10-AUDITORIA.md, se aplicável).
