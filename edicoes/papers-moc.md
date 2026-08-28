---
id: papers.moc
title: "MOC: Papers Deep Dives"
type: moc
date: 2026-08-28
status: seed
tags:
  - moc
  - papers
  - navigation
relates-to:
  - "[[_moc-runtime]]"
  - "[[papers/repos-registry]]"
---

# MOC: Papers Deep Dives

Mapa do pipeline `/papers-deep`: destilação dos destaques do jornal diário e
confronto das teses com o estado atual dos repos.

## Registro e fontes

- [[papers/repos-registry|Repos Registry]] — catálogo dos repos confrontados, com frescor (`last-verified` / `verified-head`)
- Edições do jornal: `papers/AAAA/MM/YYYY-MM-DD.md` (ex.: [[papers/2026/08/2026-08-28|2026-08-28]], quando existir)
- Fonte original: `~/papers-journal/edicoes/` (cron diário)

## Deep dives por mês

### 2026/08

Execução de 2026-08-28 sobre a edição de [[papers/2026/08/2026-08-06|2026-08-06]]:

- [[papers/deep/2026/08/2608.05466|Recursive Synthesis for Long-Horizon Terminal Tasks]]
- [[papers/deep/2026/08/2608.05102|ABSeeker: Training Long-Horizon Search Agents via Answer-Backtracked Credit Assignment]]
- [[papers/deep/2026/08/2608.05013|OneDayAgent: Towards a Long-Horizon Harness for Autonomous Agents]]
- [[papers/deep/2026/08/2608.04574|When Memory Lies: An Empirical Study of Spatial Memory Staleness in VLM Agents]]
- [[papers/deep/2026/08/2607.28048|SKILL-KD: Contrastive Skill Distillation for LLM Agents]]
- [[papers/deep/2026/08/2608.03836|Resume Means Resume: A Machine-Checked Conformance Contract for Checkpoint, Interrupt, and Resume Semantics in Workflow Persistence Layers]]

Execução de 2026-08-28 sobre a edição de [[papers/2026/08/2026-08-27|2026-08-27]]:

- [[papers/deep/2026/08/2608.26005|VoiceMem: Streaming Dual-Brain Memory for Real-Time Interaction]]
- [[papers/deep/2026/08/2608.24979|FrontierChallenge: Evaluating Scientific Workflow Completion]]
- [[papers/deep/2026/08/2608.25593|JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution]]
- [[papers/deep/2026/08/2608.23564|SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration?]]
- [[papers/deep/2026/08/2608.24358|The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents]]
- [[papers/deep/2026/08/2608.26070|Prefix Sliding for efficient test-time scaling]]

## Execuções

| Data | Edição | Notas criadas | Registro atualizado? |
|---|---|---|---|
| 2026-08-28 | [[papers/2026/08/2026-08-06|2026-08-06]] | 6 (todos os destaques) | Sim — refresh profundo de `papers-journal`, `llm-council` e `agent-skills`; demais entradas frescas ou sem scan reportado |
| 2026-08-28 | [[papers/2026/08/2026-08-27|2026-08-27]] | 6 (todas as destaques) | Não — todos os repos confrontados estavam frescos (HEAD == `verified-head`, `last-verified` do dia) |
