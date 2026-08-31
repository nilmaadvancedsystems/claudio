---
description: Executa a rotina de organização da pasta Claudio Secretario (Orquestrador)
argument-hint: [SIMULACAO|PRODUCAO|AUDITORIA]
---

Resolva primeiro `<RAIZ_REGRAS>` com `git rev-parse --show-toplevel` — é a raiz do
repositório de regras desta sessão, e todo caminho de regra abaixo é relativo a ela
(Dicionário §1(a)). Informe ao usuário qual `<RAIZ_REGRAS>` você resolveu, antes de
começar: é o que deixa claro se esta execução está usando as regras de produção
(`C:\Users\DPTO FISCAL 004\GUSTAVO\claudio`, branch `main`) ou as de um clone de teste.

Leia `<RAIZ_REGRAS>\necessario para o claude\agentes\01-ORQUESTRADOR.md` e execute a
rotina descrita nele do início ao fim, em modo `$1` (padrão: `SIMULACAO` se `$1` estiver vazio).

Siga a sequência de fases exatamente como escrita no arquivo, carregando cada agente
(00, 02-09, e 10 se `modo=AUDITORIA`) do caminho indicado na seção "Mapa de agentes" antes
da fase correspondente. Se `modo=AUDITORIA`, siga a sequência própria do 10-AUDITORIA.md
(não a sequência de 8 fases normal). Ao final, entregue o relatório gerado pelo
09-RELATOR.md (ou pelo 10-AUDITORIA.md, se aplicável).

⚠️ Se `<RAIZ_REGRAS>` **não** for a pasta de produção e `$1` for `PRODUCAO`, pare e
confirme com o usuário antes de qualquer escrita: é um clone de teste apontando para os
documentos reais dos clientes (caminho de dado é o mesmo nos dois ambientes), e arquivaria
pra valer com regra possivelmente não aprovada. `SIMULACAO` a partir de clone é o uso
esperado e não precisa de confirmação.
