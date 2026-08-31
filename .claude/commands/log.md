---
description: Mostra o relatório da última execução da rotina (ou de uma data específica)
argument-hint: [AAAA-MM-DD opcional]
---

Encontre o log mais recente dentro de
`_CLAUDIO_CONTROLE\LOGS\` (estrutura `[AAAA-MM]\[DD]\EXEC-*.txt` / `.html`).

Se `$1` for passado (formato AAAA-MM-DD), procure o log daquele dia específico em vez
do mais recente; se não houver execução nesse dia, avise e mostre o mais recente disponível.

Passos:
1. Ache o arquivo `.txt` mais recente (ou do dia pedido) dentro de `_CLAUDIO_CONTROLE\LOGS\`.
2. Leia e mostre o conteúdo dele direto na conversa, em português simples — não precisa
   mostrar o arquivo bruto, resuma de forma legível: quantos arquivos foram processados,
   pra onde cada um foi, e se teve algo em "Não Identificados" ou "Falhas".
3. Abra também o `.html` correspondente no navegador padrão, para quem quiser ver o
   relatório visual completo — use `start "" "<caminho completo do .html>"` via Bash.
