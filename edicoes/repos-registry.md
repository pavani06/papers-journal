---
id: papers.repos-registry
title: "Papers — Repos Registry"
type: registry
date: 2026-08-28
status: seed
tags:
  - papers
  - registry
  - repos
relates-to:
  - "[[_moc-runtime]]"
  - "[[papers/papers-moc]]"
---

# Repos Registry

Catálogo dos repos confrontados pelo pipeline `/papers-deep`. Cada entrada carrega
`last-verified` e `verified-head`: se o HEAD atual do repo difere de `verified-head`,
ou `last-verified` tem mais de 7 dias, o confronto dispara refresh da entrada antes
de afirmar qualquer coisa. O registro é pista a verificar, nunca fato.

## papers-journal

- path: `/home/pavanpavan/papers-journal`
- propósito: jornal diário dos Daily Papers do Hugging Face; busca, triagem por LLM contra `interests.md`, edição em markdown + HTML via cron.
- arquitetura: Python stdlib + OpenAI API; `src/journal.py` (busca/triagem), `src/render_html.py` (portal), `src/deepdive.py` (leitura profunda sob demanda), `bin/papers-daily.sh` (wrapper de cron com lock/log/notificação); edições em `edicoes/AAAA/MM/`, site em `docs/`.
- last-verified: 2026-08-28
- verified-head: 7c6bea168365cca94712135998684eaf3091be76

## agent-workloops

- path: `/home/pavanpavan/agent-workloops`
- propósito: kit de workflows para agentes de IA executarem trabalho longo, encadeado e verificável sob gates humanos; cada workflow documentado com evidência de execução real.
- arquitetura: playbooks em markdown (`playbooks/workloop.md`), docs de caso e anatomia (`docs/`); sem código de runtime, é repositório de processo.
- last-verified: 2026-08-28
- verified-head: 2f3c64c2f401a31ea2116bd4bf5b4966c3348725

## koda-desafio

- path: `/home/pavanpavan/koda-desafio`
- propósito: produzir o processo seletivo do épico #1 (Desafio KODA Re-engajamento); o repo gera a rubrica, não o sistema — construir o sistema aqui contamina o teste.
- arquitetura: `AGENTS.md` com regras anti-contaminação, `decisoes/`, `docs/`; repositório de especificação e avaliação.
- last-verified: 2026-08-28
- verified-head: 1e534d9a4b45a654c01795fd8287deac040e90d3

## hop-ecosystem-atlas

- path: `/home/pavanpavan/hop-ecosystem-atlas`
- propósito: atlas de ecossistema da repo `pavani06/HoP` (hop-control-tower) gerado por análise estática read-only: arquitetura C4, catálogo de serviços, métricas, findings de segurança, dívida técnica.
- arquitetura: artefato de documentação viva (75 arquivos gerados + README e guia); snapshot de 2026-08-24, cobertura 415 arquivos JS / 113.826 LOC.
- last-verified: 2026-08-28
- verified-head: 8d8396a3a70a1cd5d783f1e6e8142487f4cc14b8

## sisyphus-runtime

- path: `/home/pavanpavan/sisyphus-runtime`
- propósito: vault Obsidian do runtime do Sisyphus; system-of-record do ecossistema: fatos duráveis (`facts/`), estado corrente (`state/`), handoffs (`sessions/`), jornal de papers (`papers/`), telemetria.
- arquitetura: markdown com frontmatter padronizado, wikilinks e MOCs; `obsidian-eval` para consulta sem app; espelha edições do papers-journal.
- last-verified: 2026-08-28
- verified-head: 10a3a4de25fe1c53826ab8bd9f15142249ab0f6f

## ciot-authpay-repo

- path: `/home/pavanpavan/ciot-authpay-repo`
- propósito: acervo de conhecimento (não código) da tese de investimento em antecipação de recebíveis de frete apoiada no CIOT, operada pela AuthPay (FreteCash); preserva quem afirmou o quê, quando e com que grau de comprovação — erro histórico é dado, não é corrigido.
- arquitetura: acervo de documentos com regras próprias de custódia (`CLAUDE.md` obrigatório para agentes); entrada quase diária de informação.
- last-verified: 2026-08-28
- verified-head: 36e8ac93dc47a5f47c736203dcbcc3569bc3d900

## scripts

- path: `/home/pavanpavan/scripts`
- propósito: utilitários do operador: cron (`reflect-daily.sh`), CLI Sisyphus (`sisyphus/`, Python), dispatch, incidents, maintenance, project-runtime, reflection, ciot-vault.
- arquitetura: shell scripts + pacote Python; organizado por domínio em subdiretórios.
- last-verified: 2026-08-28
- verified-head: 91acbcb65e95981cf0c230ee33e24f92baf9dc4a

## agent-skills

- path: `/home/pavanpavan/agent-skills`
- propósito: source of truth único das Agent Skills do ambiente (padrão agentskills.io: `SKILL.md` com frontmatter `name` + `description`), servindo OpenCode, Claude Code e Codex dos mesmos arquivos.
- arquitetura: `skills/<nome>/SKILL.md` por skill; ciclo de issues (issue-start, issue-review, issue-finish, issue-executor-master) como skills principais.
- last-verified: 2026-08-28
- verified-head: ab87c55238bea6d97ff047cfbd8a7205ebc27829

## govevo-site

- path: `/home/pavanpavan/govevo-site`
- propósito: site estático do GovEvo ("Governando o que passa a valer").
- arquitetura: `index.html` + `assets/` (css, js, favicon); sem build, sem dependências.
- last-verified: 2026-08-28
- verified-head: fffd0711d05baa9155ece5f53eaab9922ce1dd12

## llm-council

- path: `/home/pavanpavan/llm-council`
- propósito: conselho de LLMs de provedores diferentes respondem à mesma pergunta, avaliam-se às cegas, presidente sintetiza; CLI + servidor MCP. Derivado do llm-council do Karpathy com correções (cegamento real, agregação por Borda, falha nunca silenciosa).
- arquitetura: stdlib pura para OpenAI, DeepSeek e z.ai; SDK `anthropic` como única dependência (venv próprio); conselho atual gpt-5.6-terra, deepseek-v4-pro, claude-opus-5, glm-5.3; presidente gpt-5.6-sol.
- last-verified: 2026-08-28
- verified-head: 1518d4c193b5c9edf2313d77695e2842af03fcc9
