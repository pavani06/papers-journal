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
- arquitetura: Python stdlib + OpenAI API; `src/journal.py` (busca/triagem/edição), `src/render_html.py` (portal), `src/index.py` (capa do arquivo), `src/deepdive.py` (leitura profunda sob demanda), `src/deep_html.py` (publica as notas do papers-deep em `docs/deep/AAAA/MM/` e reconcilia a seção `## Deep dives` no HTML das edições, card com o "Sumário de ação" de cada nota; idempotente), `src/paths.py` (único lugar que conhece o layout, override por `PAPERS_HOME`/`PAPERS_DATA_DIR`), `bin/papers-daily.sh` (wrapper de cron com flock/log/notificação/fail-loud, guard de idempotência por existência de arquivo, staging restritivo via `src/paths.py:publicaveis`); edições em `edicoes/AAAA/MM/`, notas deep em `edicoes/deep/AAAA/MM/`, catálogo de princípios transversais em `edicoes/principios/` (gerado pelo papers-synth: `indice.md`, `glossario-causas.md`, `capacidades-repos.md`, um arquivo por princípio), site em `docs/` e `docs/deep/AAAA/MM/`, cache de veredito em `.cache/`. Duas passadas: geração no próprio dia e reconciliação de D-1..D-3. Suíte offline (`tests/`) com CI em `.github/workflows/tests.yml`; `src/confrontos.py` extrai os blocos de confronto das notas e resolve cada citação `file:line` contra o disco (`:104-119` confere existência do arquivo e faixa dentro do tamanho, não o conteúdo da linha); o modo `--gate` é o executor estrito do gate mecânico do fechamento (resolve RAW, não grava, sai não-zero nomeando as não resolvidas). `src/deepdive.py` grava em `deep/` na raiz, fora do glob do conversor (`src/paths.py`: `deep_notas()` só lê `edicoes/deep/`): saída nunca publicada, mas `src/journal.py:405` publica em todo destaque o convite `aprofundar: python3 src/deepdive.py <id>` para esse caminho morto. `Fonte` rotula `completo`/`truncado`/`abstract` com `lidos`/`total` (`src/deepdive.py:59-81`), o corte volta como fato (`:103-108`), o prompt avisa o modelo (`:169`) e o cabeçalho da nota carrega o aviso (`:202-208`); o tail truncado morre em `text[:MAX_CHARS]` (`:106`) sem índice nem sumário recuperável. O objeto `relacao` tem gate: `chapeu_md` confere tipo válido, formato de `ref_data` e existência em disco da edição citada, degradando com log em vez de derrubar (`src/journal.py:400-417`, rejeição registrada por `_relacao_rejeitada`, `:364-375`); `normalize_verdict` resolve ids contra o catálogo e falha alto em órfão (`:308-328`); o `ref_tese` segue publicado verbatim sem conferir que a tese é da edição citada (`:421-422`). A escrita publicada é atômica, centralizada em `escrever` (`src/paths.py:78-101`), mas o guard de idempotência do cron (`bin/papers-daily.sh:84`) e a verificação pós-execução (`:106-108`) conferem existência do arquivo, não integridade: interrupção no meio da escrita marca o dia como feito com artefato truncado. Nenhuma das duas chamadas de LLM declara `max_tokens` — o único limite é timeout (`src/journal.py:247`, `src/deepdive.py:92`). O conversor monta `href` da URL do markdown da nota só com escape de HTML, sem allowlist de esquema (`src/deep_html.py:111-115`); `_parse_frontmatter` (`:62-92`) tira as aspas externas sem desfazer escape: título com `\"` sai com barras literais no `<title>`, no `<h1>` e no card. O prompt do deepdive interpola o HTML de terceiro cru, sem delimitador de fronteira (`src/deepdive.py:138`). `--render-only` (`src/journal.py:441-442`) exige o cache, gravado só depois de renderizar (`:482`, `:499-504`): inalcançável na falha que recuperaria. `bin/papers-daily.sh:131` reanexa ao log o stderr que `:98` já anexara, depois da linha terminal `FALHOU`: o log rebobina após o estado final, só no caminho de falha. O conversor resolve wikilinks de edição e de nota deep para links HTML (`src/deep_html.py:28-33`, aplicados em `:116-125`) e reduz qualquer outro wikilink a texto puro (`:126`); o alvo é montado por concatenação do caminho, sem conferir que a nota ou a edição existe — link quebrado é possível. Refresh de 2026-09-01 (subagente papers-deep, confronto do 2608.27455): cinco commits desde a verificação anterior (13de006 deep dive 26175; 3439b0a staging do cron; bd12895 gitignore de skill; f28b858 modo `--gate`; c96662f compactação desta entrada); claims de `journal.py` re-verificadas por leitura direta.
- last-verified: 2026-09-01
- verified-head: c96662fa7b9a3711900eed6f9b2353e837cbbf43

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
- arquitetura: markdown com frontmatter padronizado, wikilinks e MOCs; `obsidian-eval` para consulta sem app; `papers/` é symlink para `/home/pavanpavan/papers-journal/edicoes` — mesmo arquivo físico, não cópia (constraint: `facts/_global/constraints.md:67`); commits de sessão (`sessions/`, `state/`, `oracle-reviews/`) são rotina esperada e tendem a classificar drift `externo` inofensivo. A evolução das regras globais acontece aqui: `facts/_global/principles.md` acumula princípios com evidência por contagem agregada ("evidence: 2 handoffs", "evidence: 21 papers + 1 par de transferência", `facts/_global/principles.md:16-22`), e a promoção automática é por recorrência textual com limiar de 3 ocorrências, sem estratificação nem holdout (`facts/_global/promote-patterns-validation.md:27-39`, modo fuzzy em `:58-64`). Adoções recentes vieram do catálogo de princípios do papers-synth sob aprovação nomeada do operador.
- last-verified: 2026-08-31
- verified-head: 0b6a0dd73fe64418985982ca7dc8ee03943225bf

## ciot-authpay-repo

- path: `/home/pavanpavan/ciot-authpay-repo`
- propósito: acervo de conhecimento (não código) da tese de investimento em antecipação de recebíveis de frete apoiada no CIOT, operada pela AuthPay (FreteCash); preserva quem afirmou o quê, quando e com que grau de comprovação — erro histórico é dado, não é corrigido.
- arquitetura: acervo de documentos com regras próprias de custódia (`CLAUDE.md` obrigatório para agentes); entrada quase diária de informação.
- last-verified: 2026-08-28
- verified-head: 36e8ac93dc47a5f47c736203dcbcc3569bc3d900

## scripts

- path: `/home/pavanpavan/scripts`
- propósito: utilitários do operador: cron (`reflect-daily.sh`), CLI Sisyphus (`sisyphus/`, Python), dispatch, incidents, maintenance, papers-deep, reflection, telemetry, ciot-vault.
- arquitetura: shell scripts + pacote Python; organizado por domínio em subdiretórios; sem README na raiz. `papers-deep/` é novo: utilitários do orquestrador deste pipeline (`varre_registro.py`, varredura mecânica read-only que classifica cada entrada do registro nos dois eixos da tabela de precedência, `papers-deep/varre_registro.py:2-6`, `:84-89`; `idempotencia.sh`; `confrontos/` com um arquivo por repo mais `INDICE.md`). `dispatch/preflight.sh` valida a gramática do bloco inteiro antes de executar qualquer linha (`:41-69`), com allowlist por segmento e git read-only (`:16-17`, `:98-130`) e PIN de proveniência por md5 antes da allowlist (`:71-96`) — gate pré-execução estático, sem ciclo de controle durante o run. `sisyphus/trajectory.py` grava a trajetória write-only no fim da sessão (`:4`), com delegações e desfecho final (`:26-36`, `:39-57`) e nenhum evento de edição de contexto; `sisyphus/exploration_cache.py` casa por hash exato com invalidação por SHA do git. `telemetry/warmup-invocation-rate.py` é novo (medidor da sonda fase0). `project-runtime/` foi esvaziado no intervalo desde a última verificação (kernel, CLI, testes e bin removidos; README e docs reduzidos).
- last-verified: 2026-08-31
- verified-head: 86b426c8e9a060cc37dc56c5f195a2418bcf78b7

## agent-skills

- path: `/home/pavanpavan/agent-skills`
- propósito: source of truth único das Agent Skills do ambiente (padrão agentskills.io: `SKILL.md` com frontmatter `name` + `description`), servindo OpenCode, Claude Code e Codex dos mesmos arquivos.
- arquitetura: `skills/<nome>/SKILL.md` por skill, mais `commands/` para comandos opencode versionados aqui sem cair na descoberta por `iterdir()` do harness (hoje `commands/papers-deep.md` e `commands/papers-synth.md` — destilação de destaques e síntese transversal dos deep dives, respectivamente — dos quais só `papers-deep.md` está de fato servido por symlink em `~/.config/opencode/command/`, verificado em 2026-08-31: `papers-synth.md` existe no repo sem symlink correspondente, então a superfície de serving diverge do repo e nenhum rollback do repo a reconcilia); ciclo de issues (issue-start, issue-review, issue-finish, issue-executor-master) como skills principais; harness próprio (`scripts/run_harness.py`) com três gates por skill (contract, modules, integration) rodando em CI, e gate sem arquivo de teste permanece `passes: false`. `task-wrapper.sh` estopado pelo operador em 2026-08-28: nenhuma fase do `issue-executor-master` o invoca. `commands/` tem `papers-synth.md` ao lado do `papers-deep.md` (que exige calibragem); `skills/` inclui `handoff` versionada e as vendorizadas `artifact-evidence-review` e `doc-coauthoring`; o harness tem gate `integration` com terceiro estado `executed`, e o gate sem arquivo de teste é idempotente e fail-closed (`scripts/run_harness.py:90-97`, `:102-115`, testes lidos de `<skill>/harness/tests`, `:67`); a CI reprova drift de `test-results.json` em pull_request; `issue-start` ganhou gates por blast radius e `issue-review` roteamento de reviewer por tipo de tarefa. Refresh de 2026-09-01 (subagente papers-deep, confronto do 2608.27455): 18 commits desde `ab46271e`, comandos e skills do papers-deep re-verificados por leitura direta. Todos os gates são pós-hoc em relação à execução da skill, e o próprio `issue-executor-master` declara que `allowed-tools` é blast radius para revisor, não controle imposto (`skills/issue-executor-master/SKILL.md:34-35`); a fronteira de conteúdo não confiável com quatro regras em camadas está em `skills/issue-executor-master/SKILL.md:75-147`, e o fluxo nunca bloqueia por `uncertainty_score` alto (`:196-200`).
- last-verified: 2026-09-01
- verified-head: 3bf078baa0947158c772461f3b4df38145ca3173

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

## long-running-agents

- path: `/home/pavanpavan/long-running-agents`
- propósito: vault Obsidian de conhecimento sobre agentes long-running: padrões canônicos extraídos de fontes analisadas, currículo de 12 semanas aplicado ao KODA, análises de artigos com pipeline próprio; fonte conceitual do ecossistema (convenções Obsidian e taxonomia daqui foram adaptadas pelo mhc-knowledge-base).
- arquitetura: markdown Obsidian com frontmatter e wikilinks validados (`npx tsx scripts/validate-obsidian.ts`, gate de CI); `docs/canonical/` com ~180 padrões, `docs/analysis/` gerado pelo pipeline analyze-and-improve (analysis, mental-model, patterns, classification por fonte), `docs/system-of-record.md` com precedência documental e os domínios que governam a taxonomia de tags, `docs/cross-vault-taxonomy.md` mapeando equivalências com os outros vaults, `curriculum/` (níveis 1-4 + core concepts + case studies), `harness/` (guia e templates do analyze-and-improve), portal web estático em `web/`; sem código de runtime além dos scripts de validação frontmatter.
- last-verified: 2026-09-01
- verified-head: 3e6e124de0aae1b939a931f1d82815d73b689330

## chatbot-ai

- path: `/home/pavanpavan/chatbot-ai`
- propósito: umbrella repo da frota `chatshop-io`: mapa (`repos.yaml`) e controle remoto (`justfile`) dos sub-repos; não é monorepo — clones vivem em `repos/<grupo>/<nome>`, git-ignored e independentes, com worktrees ativos do mhc-backend no topo.
- arquitetura: `repos.yaml` regenerado por `scripts/gen-manifest.py` (gh + scan local), `justfile` com clone/pull/status/exec pela frota (repos sem acesso são pulados, não erro), ambiente declarado em `devenv.nix` carregado por direnv com segredos machine-local (`.env`), `.agent-roles/` com rulesets por papel e `AGENTS.local.md` por máquina, vault de docs do projeto em `chatbot-ai-docs/`, DB OpenCode isolada por projeto (`.opencode-db/` via `OPENCODE_DB`).
- last-verified: 2026-09-01
- verified-head: 46270972ac1d44238f2ebf6ef1352c769cdeef67

## mhc-knowledge-base

- path: `/home/pavanpavan/mhc-knowledge-base`
- propósito: knowledge base IDSD para o ecossistema KODA: governança humana em Markdown (intents, expectations, decisions) compilada em contratos de decisão executáveis consumidos pelo mhc-backend como dependência npm pinada por SHA imutável.
- arquitetura: monorepo pnpm de duas camadas: `domains/` (Markdown Obsidian com taxonomia controlada `domain/*`, `artifact/*`, `capability/*`, `runtime/*`, `concern/*` referenciada em `system-of-record.md`) e `packages/` (`@mhc/decision-runtime`, `@mhc/koda-decision-kb`); `pnpm validate` confere frontmatter, referências, órfãos, versionamento e testes, `pnpm kb:generate` gera contract manifest + skeletons com gate `kb:validate` em CI; piloto: fatia vertical `checkout.preCreateOrder`; status pre-bootstrap, rastreado por GitHub Issues.
- last-verified: 2026-09-01
- verified-head: 0c450c5b315def264981bd993fccaa4b447143c3

## obsidian-eval

- path: `/home/pavanpavan/obsidian-eval`
- propósito: CLI que transforma vaults Obsidian em runtime de conhecimento consultável sem o app: scan, grafo, queries, escrita e cross-vault wikilinks; runtime de fato do ecossistema de vaults (long-running-agents, mhc-knowledge-base, raw-knowledge, sisyphus-runtime), inclusive do warmup de memória das sessões.
- arquitetura: TypeScript publicado como `@pavani/obsidian-eval`; parse de frontmatter YAML e resolução de wikilinks constroem grafo direcionado em memória; DSL de query por pattern matching sem `eval()`/`Function()` (`filter`, `findByTag`, `orphans`, `brokenLinks`, `inbound`/`outbound`); binário de gate (`obsidian-eval-gate.js`) para validações que bloqueiam; testes vitest.
- last-verified: 2026-09-01
- verified-head: 2eeb774c98af1f4b7b195ba7ae147fd223c73e5e
