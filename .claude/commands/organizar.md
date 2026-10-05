---
description: Executa a rotina de organização da pasta Claudio Secretario (Orquestrador)
argument-hint: [SIMULACAO|PRODUCAO|AUDITORIA] [pasta=<subpasta da origem>] [limite=<N pais>]
---

Resolva primeiro `<RAIZ_REGRAS>` com `git rev-parse --show-toplevel` — é a raiz do
repositório de regras desta sessão, e todo caminho de regra abaixo é relativo a ela
(Dicionário §1(a)). Capture também a branch (`git rev-parse --abbrev-ref HEAD`). Informe ao
usuário `<RAIZ_REGRAS>` e a branch antes de começar: **produção é identificada pela branch
(`main`), nunca pelo caminho absoluto** — o caminho muda de máquina pra máquina.

Leia `<RAIZ_REGRAS>\necessario para o claude\agentes\01-ORQUESTRADOR.md` e execute a
rotina descrita nele do início ao fim, em modo `$1` (padrão: `SIMULACAO` se `$1` estiver vazio).

**Rodar aos poucos** (argumentos opcionais depois do modo, em qualquer ordem; sem eles a
execução é a normal, a mesma da tarefa agendada):
- `pasta=<caminho relativo à origem>` — o inventário (Fase 1) olha **só** essa subpasta
  (recursivo), ignorando o resto da origem. Ex.: `/organizar PRODUCAO pasta="2026-09/GRANMIX COMERCIO DE ALIMENTOS LTDA"`
  ou `pasta="413 BRAZILIAN filiais"`. Caminho que não existe na origem → pare e avise, não varra tudo.
- `limite=N` — usa `N` no lugar de `LIMITE_ITENS` (60) nesta execução, ex. `limite=20` pra um
  lote bem pequeno ou `limite=200` pra um maior. `LIMITE_DERIVADOS` (01) continua valendo.
- `pasta=?` — **não processa nada**: lista as pastas de primeiro nível da origem com a
  contagem de arquivos de cada uma (ordem decrescente), para você escolher por onde começar.
Repita o comando quantas vezes quiser: o que já foi arquivado sai da origem e o manifesto
impede refazer, então cada rodada continua de onde a anterior parou.

Siga a sequência de fases exatamente como escrita no arquivo. Carregue na sessão principal
apenas o Dicionário (00) e os procedimentos mecânicos (06 Parte A, 07, 08, 09 — e 10 se
`modo=AUDITORIA`); as regras de julgamento (02, 03, 04, 04b, 05 e 05a-d) são carregadas
pelos subagentes `separador`/`classificador`/`reclassificador`, não por você. Se
`modo=AUDITORIA`, siga a sequência própria do 10-AUDITORIA.md (não a sequência de fases
normal). Ao final, entregue o relatório gerado pelo 09-RELATOR.md (ou pelo
10-AUDITORIA.md, se aplicável).

⚠️ Se a branch **não** for `main` e `$1` for `PRODUCAO`, pare e confirme com o usuário antes
de qualquer escrita: é um clone de teste (ou branch de trabalho) apontando para os
documentos reais dos clientes (caminho de dado é o mesmo em qualquer branch), e arquivaria
pra valer com regra possivelmente não aprovada. `SIMULACAO`/`AUDITORIA` fora da `main` são o
uso esperado e não precisam de confirmação.
