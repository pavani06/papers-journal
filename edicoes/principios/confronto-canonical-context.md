---
id: papers.principios.confronto-canonical-context
title: "Confronto — canonical-context contra os princípios do catálogo"
type: confronto-skill
date: 2026-08-30
status: estudo
tags:
  - papers
  - principios
  - canonical-context
  - confronto
relates-to:
  - "[[papers/principios/indice]]"
  - "[[papers/repos-registry]]"
---

# Confronto — canonical-context contra os princípios do catálogo

## Contexto (auto-contido)

O **canonical-context** é a skill (`~/.config/opencode/skills/canonical-context/SKILL.md`, 810 linhas) que injeta contexto em toda sessão do ecossistema: busca handoffs ativos, fatos duráveis (princípios, constraints) e estado corrente no vault de runtime `~/sisyphus-runtime/`, além de docs canônicos no vault `long-running-agents`; ranqueia por relevância (score ≥ 0.2, top-N por budget) e injeta no formato resumido `## Canonical Reference` / `## Previous Session`.

Este confronto aplica os **14 princípios do catálogo** (`papers/principios/`, 1ª re-síntese total de 2026-08-30, 100 notas de deep dive) à skill. Base de leitura: SKILL.md integral; todas as referências `:linha` abaixo são desse arquivo. Citações das notas de paper por arxiv-id (ver `edicoes/deep/2026/08/`).

**Status do artefato**: análise inicial para estudo; veredito e próximos passos em aberto (seção final).

## Resumo por princípio

| Princípio (id) | Estado na skill | Evidência |
|---|---|---|
| 0003 estado herdado validado | **Conforma parcial** — Freshness Check (Passo 0.5) valida handoffs contra disco antes de injetar | `:327-344` |
| 0012 registro do que entrou | **Conforma** — `relevance_log` registra cada item injetado + motivo, persistido em `state/current/` | `:620-658` |
| 0013 memória com gate de admissão | **Conforma parcial** — score ≥ 0.2 + top-N por budget (o "k explícito" de 2608.15008) | `:594-618` |
| 0006 incompletude declarada | **Conforma** — "(Futuro... ainda não implantado)", "checkDrift é filtro conservador (MVP)", fallbacks com WARNING | `:264`, `:537-539` |
| 0009 verificação de claims | **Conforma parcial** — freshness check confere GAPs contra o real; resumo injetado do canonical doc é auto-relato sem conferência | `:333`, `:756` |
| 0012 cerca de dado | **VIOLA** — conteúdo injetado (continuity_message, summary_buffer, resumos) entra cru, sem marcador, no nível da instrução | `:748-754` |
| 0001 gate que não bloqueia é telemetria | **VIOLA** — Trace/Flywheel/Oracle checks avisam em prosa ("DEVE alertar"); nenhum bloqueia | `:58-63`, `:162-168`, `:230-232` |
| 0004 proveniência sela o artefato | **VIOLA parcial** — `relevance_log` sem produtor; ponteiro de origem existe, span não | `:643-658` |
| 0005 contrato de admissão | **VIOLA** — skill sem suite própria; editar o SKILL.md é apostar | — |
| 0014 efeito vs presença | **VIOLA parcial** — freshness check usa `test -f` e `mtime`, não conteúdo/hash | `:331-334` |
| 0011 uma execução não é medida | N/A parcial — health checks rodam 1× por sessão | — |

## Achados fortes

### A1 — O injetor de contexto não cerca o que injeta (princípio 0012)

Todo conteúdo injetado entra cru: `continuity_message` e `summary_buffer` de handoffs, resumos de canonical docs — no mesmo nível sintático da instrução da sessão (`:748-754`). Um handoff contaminado (escrito a partir de conteúdo não confiável) instrui a sessão seguinte como diretiva. O molde existe: `agent-skills/skills/issue-executor-master/SKILL.md:85-105` — marcadores `<<<CONTEUDO_NAO_CONFIAVEL ...>>>` que viajam com o dado. É o mesmo padrão do papers-journal antes do par 11 (`journal.py:142-147`): a memória que governa decisões entra sem fronteira. Notas-base: 2608.00677 (origem, não canal), 2606.00152 (escopo verbo+alvo), 2608.21500 (marca de proveniência no formato da entrada).

### A2 — Freshness Check é o caso positivo a generalizar (princípios 0003/0014)

O Passo 0.5 já valida claims de handoff contra o observável antes de injetar (raro no ecossistema — conforma com 0003). Limitações:
1. **Cobre só handoffs** — canonical docs do `long-running-agents` (que envelhecem) não passam por freshness check.
2. **Usa presença, não conteúdo** — `test -f` e `mtime` (`:331-334`); arquivo existente pode ter mudado desde o handoff; mtime pode mentir. Upgrade natural: handoff selaria o hash do que afirma e o check conferiria — o digest sha256 que o papers-journal acabou de adotar (`paths.digest_conteudo`, molde llm-council `engine.py:144-146`).

### A3 — Health checks são telemetria com roupa de gate (princípio 0001)

Trace Health, Flywheel e Oracle Gate imprimem avisos e instruções ("Rever antes de prosseguir", "DEVE alertar o operador") sem bloquear nada. Pela triagem: checador que avisa e deixa seguir produz rastreabilidade, não controle (2608.13558 t2, 2608.12440 t5, 2608.13900 t4). Nota: transformar tudo em fail-closed pode ser anti-design (travar sessão por backlog de revisão é caro); o ponto é nomear telemetria como telemetria e manter como gate efetivo apenas o que já é (handoff stale → não injetar, `:336-340`).

### A4 — relevance_log é o AcquisitionRecord sem selo (princípios 0012/0004)

O `relevance_log` (`:620-658`) já é o "registro do que entrou no contexto" do 2606.00152 — raro e valioso. Faltam: (a) selo de produtor no frontmatter (skill, sessão, data, config — molde `montar_cache` do papers-journal); (b) span/trecho do que foi injetado, não só o item (2608.12571 t2: registrar o span, não o documento); (c) medição de efeito ("ajudou ou desviou", 2608.15008 t5) — o feedback que fecharia o 0013.

### A5 — Verificação externa do resumo injetado (princípios 0002/0009)

O formato de injeção pede resumo do canonical doc ("NUNCA injetar o conteúdo completo", `:756`) — mas o resumo é produzido pelo próprio agente no momento, sem conferência contra o original. Juiz que lê auto-relato mede retórica (2607.28609 t3); aqui o risco é o resumo divergir do doc e a sessão decidir sobre o resumo. Mitigação barata: manter o ponteiro (path) sempre injetado junto do resumo — hoje o formato já o carrega (`## Canonical Reference: {title} (docs/canonical/{file}.md)`), então é meio-caminho feito; falta a regra de conferência quando o resumo sustenta decisão.

## Oportunidades priorizadas

| # | Melhoria | Princípio | Molde | Esforço |
|---|---|---|---|---|
| M1 | Cercar conteúdo injetado (continuity/summary/resumos) com `<<<CONTEUDO_NAO_CONFIAVEL>>>` + linha "dado, não instrução" | 0012 | agent-skills `SKILL.md:85-105`; papers-journal `build_prompt` (commit fa7328f) | P |
| M2 | Selo de produtor no `relevance_log` (skill + sessão + data) | 0004 | papers-journal `montar_cache` (producao) | P |
| M3 | Freshness check por conteúdo: handoff selaria hash; check confere; estender a canonical docs | 0003/0014 | papers-journal `digest_conteudo` + guarda fail-closed | M |
| M4 | Suite mínima para a skill (baseline antes de editar SKILL.md) | 0005 | agent-skills `run_harness.py`; papers-journal `tests/` | M |
| M5 | Nomear os health checks como telemetria (sem prometer gate) | 0001 | — | P |

## Pontos em aberto para estudo (próxima sessão)

1. **Decisão de design**: algum health check deve virar gate fail-closed de verdade? O único gate efetivo hoje é handoff stale → não injetar. Custo de travar sessão vs. valor de bloquear (Oracle backlog ≥15d, por exemplo).
2. **Impacto da cerca (M1)**: marcar continuidade/summary como não-confiável muda como o agente interpreta handoffs — testar contra o fluxo real do session-handoff (a cerca pode conflitar com "open_decisions são blocking" em red-phase, `:396-397`).
3. **Hash no handoff (M3)**: exige mudança no produtor (session-handoff selaria hash dos memory_handles) — avaliar compatibilidade com handoffs antigos (janela, como no cache pre-upgrade).
4. **Escopo do harness (M4)**: o `run_harness.py` do agent-skills cobre skills de `~/.config/opencode/skills/` (user scope) ou só as do repo? Verificar antes de prometer suite.
5. **Registro no registry**: canonical-context não é repo do `repos-registry.md` — decidir se entra como skill confrontável (o papers-synth confronta skills, não só repos?).
6. **Candidatura**: os achados A1-A5 viram notas de candidato no catálogo (camada c/d), ou ficam como este artefato de estudo até decisão?

## Como retomar

- Ler este arquivo + `papers/principios/indice` (14 princípios) + `edicoes/deep/2026/08/` para as notas-base.
- Verificar o estado atual do `SKILL.md` do canonical-context (pode ter mudado).
- Decidir os pontos em aberto (acima) e, se aprovado, transformar em issues (padrão qi-epic) com escopo M1-M5.
