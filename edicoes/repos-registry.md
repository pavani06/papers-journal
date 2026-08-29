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
- arquitetura: Python stdlib + OpenAI API; `src/journal.py` (busca/triagem/edição), `src/render_html.py` (portal), `src/index.py` (capa do arquivo), `src/deepdive.py` (leitura profunda sob demanda), `src/deep_html.py` (publica as notas do papers-deep em `docs/deep/AAAA/MM/` e reconcilia a seção `## Deep dives` no HTML das edições, com o card de cada nota exibindo o seu "Sumário de ação"; idempotente), `src/paths.py` (único lugar que conhece o layout, com override por `PAPERS_HOME`/`PAPERS_DATA_DIR`), `bin/papers-daily.sh` (wrapper de cron com flock/log/notificação/fail-loud, guard de idempotência por existência de arquivo); edições em `edicoes/AAAA/MM/`, notas deep em `edicoes/deep/AAAA/MM/`, site em `docs/` e `docs/deep/AAAA/MM/`, cache de veredito em `.cache/`. Sem suite de testes e sem CI. `src/deepdive.py` grava em `deep/` na raiz (`deep/2608.16425.md`), caminho que o conversor não varre (`src/paths.py`: `deep_notas()` só lê `edicoes/deep/`), então sua saída nunca é publicada. `fetch_fulltext` trunca em `MAX_CHARS = 160_000` e ainda assim devolve o flag de texto completo, então a nota sai com `fonte: texto completo` sem registrar o corte (`src/deepdive.py:34`, `:76`, `:169`). A validação do veredito do LLM em `normalize_verdict` é estrutural e cobre só ids de paper: o objeto `relacao` (`avanca`/`contradiz` + `ref_data` + `ref_tese`) é renderizado como fato por `chapeu_md` (`src/journal.py:337-345`), com o link montado por concatenação da data, sem conferir que a edição citada existe nem que a tese é dela. Nenhuma escrita de artefato publicado é atômica (`src/journal.py:489`, `:493`; `src/deep_html.py:284`, `:293`, `:302` usam `write_text` direto), e o guard de idempotência do cron (`bin/papers-daily.sh:84`) e a verificação pós-execução (`:106-108`) conferem existência do arquivo, não integridade: uma interrupção no meio da escrita marca o dia como feito com artefato truncado. Nenhuma das duas chamadas de LLM declara `max_tokens` — o único limite é timeout (`src/journal.py:247`, `src/deepdive.py:92`). O conversor monta `href` a partir da URL do markdown da nota apenas com escape de HTML, sem allowlist de esquema (`src/deep_html.py:104-107`). O prompt do deepdive interpola o HTML de terceiro cru, sem delimitador de fronteira (`src/deepdive.py:138`). `--render-only` (`src/journal.py:441-442`) exige o cache, que só é gravado depois de renderizar (`:482`, `:499-504`), então é inalcançável na falha que recuperaria. `src/journal.py:405` imprime em todo destaque de toda edição o convite `aprofundar: python3 src/deepdive.py <id>` — ponto de entrada cuja saída o conversor nunca varre, então o site publica diariamente um convite para um caminho morto.
- last-verified: 2026-08-29
- verified-head: aff151e4102e4a069b2d2100e1502f0df318792f

## agent-workloops

- path: `/home/pavanpavan/agent-workloops`
- propósito: kit de workflows para agentes de IA executarem trabalho longo, encadeado e verificável sob gates humanos; cada workflow documentado com evidência de execução real.
- arquitetura: playbooks em markdown (`playbooks/workloop.md`), docs de caso e anatomia (`docs/`); sem código de runtime, é repositório de processo.
- last-verified: 2026-08-28
- verified-head: 2f3c64c2f401a31ea2116bd4bf5b4966c3348725

## koda-desafio

- path: `/home/pavanpavan/koda-desafio`
- propósito: produzir o processo seletivo do épico #1 (Desafio KODA Re-engajamento); o repo gera a rubrica, não o sistema — construir o sistema aqui contamina o teste.
- arquitetura: `AGENTS.md` com regras anti-contaminação, `decisoes/`, `docs/`; deixou de ser só especificação — ganhou `rubrica/` (rubrica fechada), `guard/` (scripts de auditoria com fixtures positivas e negativas) e `tools/mascarar.py` com suíte própria.
- last-verified: 2026-08-28
- verified-head: e8464a23ae0b6bbc48f0eba8fc8d7148185714d1

## hop-ecosystem-atlas

- path: `/home/pavanpavan/hop-ecosystem-atlas`
- propósito: atlas de ecossistema da repo `pavani06/HoP` (hop-control-tower) gerado por análise estática read-only: arquitetura C4, catálogo de serviços, métricas, findings de segurança, dívida técnica.
- arquitetura: artefato de documentação viva (75 arquivos gerados + README e guia); snapshot de 2026-08-24, cobertura 415 arquivos JS / 113.826 LOC.
- last-verified: 2026-08-28
- verified-head: 8d8396a3a70a1cd5d783f1e6e8142487f4cc14b8

## sisyphus-runtime

- path: `/home/pavanpavan/sisyphus-runtime`
- propósito: vault Obsidian do runtime do Sisyphus; system-of-record do ecossistema: fatos duráveis (`facts/`), estado corrente (`state/`), handoffs (`sessions/`), jornal de papers (`papers/`), telemetria.
- arquitetura: markdown com frontmatter padronizado, wikilinks e MOCs; `obsidian-eval` para consulta sem app; `papers/` é symlink para `/home/pavanpavan/papers-journal/edicoes` — mesmo arquivo físico, não cópia (constraint: `facts/_global/constraints.md:67`); commits de sessão (`sessions/`, `state/`, `oracle-reviews/`) são rotina esperada e tendem a classificar drift `externo` inofensivo.
- last-verified: 2026-08-28
- verified-head: 9e46136c1c1a02a6101dab200aad08d1247339c8

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
- arquitetura: `skills/<nome>/SKILL.md` por skill; ciclo de issues (issue-start, issue-review, issue-finish, issue-executor-master) como skills principais; harness próprio (`scripts/run_harness.py`) com três gates por skill (contract, modules, integration) rodando em CI, e gate sem arquivo de teste permanece `passes: false`. `task-wrapper.sh` estopado pelo operador em 2026-08-28: nenhuma fase do `issue-executor-master` o invoca.
- last-verified: 2026-08-28
- verified-head: 6bf42e9bfa1653f130aa0356b07b3544f51f1472

## govevo-site

- path: `/home/pavanpavan/govevo-site`
- propósito: site estático do GovEvo ("Governando o que passa a valer").
- arquitetura: `index.html` + `assets/` (css, js, favicon); sem build, sem dependências.
- last-verified: 2026-08-28
- verified-head: fffd0711d05baa9155ece5f53eaab9922ce1dd12

## llm-council

- path: `/home/pavanpavan/llm-council`
- propósito: conselho de LLMs de provedores diferentes respondem à mesma pergunta, avaliam-se às cegas, presidente sintetiza; CLI + servidor MCP. Derivado do llm-council do Karpathy com correções (cegamento real, agregação por Borda, falha nunca silenciosa).
- arquitetura: stdlib pura para OpenAI, DeepSeek e z.ai; SDK `anthropic` como única dependência (venv próprio); conselho atual gpt-5.6-terra, deepseek-v4-pro, claude-opus-5, glm-5.3; presidente gpt-5.6-sol; `council ask --resume` retoma execução parcial por composição (estágios 1-2 herdados, consenso recomputado por Borda sem rede, guardas fail-closed incluindo `config_drift`; parcial gravado por troca atômica em cada limite de estágio; schema com `resumed_from`); `council ask --rank-lite` torna o estágio 2 orçável, registrando `stage2_mode`; `council cost` faz ledger e pré-voo sem rede; `council/audit.py` classifica achados em estruturais e de prosa; suite offline `test_offline.py` com CI em `.github/workflows/tests.yml`; pré-registros e emendas em `docs/prereg/`. Emendas de schema são aditivas por regra. A superfície MCP (`mcp_server.py`) não expõe resume nem interrupção.
- last-verified: 2026-08-28
- verified-head: a558dab1c557fc524251a6ebc41d9ba255858694
