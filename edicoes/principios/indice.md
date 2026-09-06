---
id: papers.principios.indice
title: "Papers — Catálogo de Princípios"
type: catalogo-principios
date: 2026-09-06
status: active
tags:
  - papers
  - principios
relates-to:
  - "[[papers/repos-registry]]"
---

# Catálogo de Princípios

Índice dos princípios transversais extraídos das notas de deep dive
(`edicoes/deep/`) pelo pipeline `/papers-synth`. Cada princípio vive em um
arquivo próprio (`principio-<NNNN>-<slug>.md`) e nasce como candidato; a
promoção a adotado é decisão do operador.

Primeira re-síntese total (modo `--full`) em 2026-08-30: 100 notas analisadas
(conjunto completo de agosto/2026). Fontes: camada a+b (triagem mecânica, 21
temas extraídos), camada c (12 pares de transferência confirmados por leitura
real) e camada d (21 causas de ressalva nomeadas). Nota de extração: os logs
das camadas a+b e d terminaram parcialmente (limite de saída dos subagentes);
os princípios abaixo refletem o extraído e serão re-verificados na próxima
re-síntese.

| ID | Título | Status | Camada | Criado em |
|---|---|---|---|---|
| principio-0001 | Controle determinístico fora do modelo | adotado | a | 2026-08-30 |
| principio-0002 | Auto-relato não é evidência de gate | adotado | a | 2026-08-30 |
| principio-0003 | Estado herdado validado contra o observável | adotado | c | 2026-08-30 |
| principio-0004 | Proveniência sela o artefato, não o log | adotado | c | 2026-08-30 |
| principio-0005 | Contrato de admissão de mudança | adotado | a | 2026-08-30 |
| principio-0006 | Incompletude é estado de primeira classe | adotado | c | 2026-08-30 |
| principio-0007 | Parada por progresso, não por teto | adotado | a | 2026-08-30 |
| principio-0008 | Falha registrada com genótipo | adotado | a | 2026-08-30 |
| principio-0009 | Verificação de claims — existência ≠ suporte | adotado | a | 2026-08-30 |
| principio-0010 | Estado de trabalho é artefato em disco | adotado | a | 2026-08-30 |
| principio-0011 | Uma execução não é medida | adotado | a | 2026-08-30 |
| principio-0012 | Fronteira de aquisição — a cerca viaja com o dado | adotado | c | 2026-08-30 |
| principio-0013 | Injeção de memória com gate de admissão | adotado | a | 2026-08-30 |
| principio-0014 | Promoção por execução validada | adotado | a | 2026-08-30 |
| principio-0015 | Protocolo de controle é contrato verificável | adotado | a | 2026-09-06 |

## Síntese incremental — 2026-09-06

Modo default: 33 notas posteriores à última síntese (2026-08-30). Vinte e
quatro tinham ateste com HEAD divergente e oito não traziam atestação; só fatos
relidos no HEAD atual sustentam o candidato novo. Os demais sinais reforçam
princípios existentes, sobretudo controle determinístico, contrato de admissão,
verificação de claims, estado em disco, gate de memória e promoção por
execução.

O princípio 0015 consolida a lacuna que não era formulada pelos anteriores:
o contrato que governa uma execução precisa ser artefato verificável, separado
da narrativa e do conteúdo que circulam pelo sistema.

### Promoção aprovada pelo operador — 2026-09-06

O operador adotou os princípios 0002, 0005, 0007, 0008 e 0010–0015 como
regras de processo globais. As entradas de literatura foram acrescentadas ao
system-of-record com proveniência preservada; a adoção não implementa mudanças
em cria gates nos repos de aplicação.

**15 princípios adotados.**
