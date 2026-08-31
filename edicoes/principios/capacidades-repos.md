---
id: papers.principios.capacidades-repos
title: "Papers — Capacidades por Repo"
type: catalogo-principios
date: 2026-08-30
status: active
tags:
  - papers
  - principios
relates-to:
  - "[[papers/repos-registry]]"
---

# Capacidades por Repo

Índice "quem já resolveu o quê" do padrão de segunda ordem (camada c) do
papers-synth: capacidades já implementadas em cada repo do ecossistema, com
evidência `file:line`. Uma recomendação contra o repo A que corresponde a uma
capacidade existente no repo B é um par de transferência — o fato (1 par, 2
citações) e, com 3+ pares em repos diferentes, o princípio "o ecossistema não
sabe o que ele mesmo já sabe".

Origem: primeira re-síntese total (2026-08-30) — 12 pares de transferência
confirmados por leitura real dos dois lados (2 com adoção pós-nota detectada);
7 pistas não confirmadas listadas ao final.

## Capacidades confirmadas

| Repo | Capacidade | Evidência |
|---|---|---|
| llm-council | Escrita atômica de parcial (.tmp + os.replace) | `council/engine.py:761-764` |
| llm-council | Digest sha256 do registro | `council/engine.py:144-146` |
| llm-council | Guardas fail-closed nomeadas de resume (config_drift incluída) | `council/engine.py:682-740` |
| llm-council | Selo de produtor code/git/config (aplicado antes de rodar) | `council/provenance.py:107-119`, `engine.py:435-438` |
| llm-council | Compare de deriva selo↔árvore | `council/provenance.py:122-136` |
| llm-council | Scrub de identidade com trilha de hits | `council/ranking.py:201-217`, `engine.py:498-506` |
| llm-council | Truncagem nomeada por estágio (aviso distinguindo parcial) | `council/engine.py:487-493`, `:552-557` |
| llm-council | Golden byte a byte de render + bootstrap | `test_offline.py:450-505` |
| llm-council | CI offline em push/PR | `.github/workflows/tests.yml:1-14` |
| papers-journal | Casamento tolerante de ids com normalização de forma | `src/journal.py:271-282` |
| papers-journal | Higiene causal da memória por filtro de data | `src/paths.py:88-92` |
| papers-journal | Carimbo de frescor last-verified/verified-head com janela | `edicoes/repos-registry.md:19-21`, `:28-29` |
| papers-journal | Cache de re-render sem rede | `src/journal.py:455-462`, `:500-504` |
| agent-skills | Cerca de dado não confiável que viaja com o dado | `skills/issue-executor-master/SKILL.md:85-105` |
| agent-skills | NOT_FOUND obrigatório com locais procurados | `references/fases-0-2.md:229-238`, `SKILL.md:230` |
| agent-skills | Gate sem teste permanece `passes: false` | `scripts/run_harness.py:8-10`, `:102-115` |
| agent-skills | CI vermelho como parada dura sem downgrade silencioso | `skills/issue-review/SKILL.md:163-167` |
| koda-desafio | Fixture negativa obrigatória por guard | `guard/run-fixtures.sh:2-4`, `:11-12` |
| sisyphus-runtime | Regra durável estruturada com proveniência, adendos e See also | `facts/_global/dispatch-rule-amendment-provenance.md:7`, `:45-55`, `:65-69` |
| scripts | Determinismo declarado na ordenação do clustering | `reflection/run.ts:348-370` |
| scripts | Trace-link de evidência na persistência de princípios (adotado pós-nota) | `reflection/run.ts:382-387` |

## Pares de transferência confirmados (12)

1. Escrita atômica: papers-journal (`journal.py:489,493`) ← llm-council (`engine.py:761-764`) — notas 2608.03836, 2608.23283, 2608.13900
2. Selo de produtor: papers-journal (`journal.py:500-504`) ← llm-council (`provenance.py:107-119`) — 2608.06867, 2608.06301, 2608.15242, 2608.10450
3. Flag de truncagem/completude: papers-journal (`deepdive.py:74-76`) ← llm-council (`engine.py:487-493,552-557`) — 2608.04569, 2608.05013, 2608.10692
4. Selo de integridade + guardas fail-closed: papers-journal (`journal.py:455-462`, `paths.py:88-107`) ← llm-council (`engine.py:144-146,682-740`) — 2608.00677, 2608.04574
5. Registro de aquisição: scripts (`trajectory.py:26-57`) ← llm-council (`engine.py:498-506`) — 2606.00152
6. Proveniência/trace-link em regra durável: scripts (`run.ts`, contagem) ← sisyphus-runtime (`dispatch-rule-amendment-provenance.md`) — 2607.28048, 2608.05784 — **consumado pós-nota** (`run.ts:382-387`)
7. Suíte offline + golden: papers-journal (sem tests/CI) ← llm-council (`test_offline.py:450-505`, `tests.yml:1-14`) — 2608.05466, 2608.03451, 2608.09802
8. Reamarração revisado↔publicado: agent-skills (`issue-review/SKILL.md:169-179`, `issue-finish/SKILL.md:127-134`) ← llm-council (`provenance.py:122-136`) — 2608.08311, 2608.05219, 2608.10875
9. Fixture negativa em gate: agent-skills (`test_contract.py` sem negativo) ← koda-desafio (`guard/run-fixtures.sh:2-4,11-12`) — 2608.19197 — **parcialmente consumado** (`pytest.raises` corrigido)
10. Blind spot como campo obrigatório: papers-journal (`paths.py:101-104`) ← agent-skills (`fases-0-2.md:229-238`, `SKILL.md:230`) — 2608.05703
11. Cerca de dado não confiável que viaja: papers-journal (`journal.py:142-147`) ← agent-skills (`SKILL.md:85-105`) — 2608.00677, 2608.15888
12. Casamento tolerante por normalização de forma: llm-council (`audit.py:207-208` substring crua) ← papers-journal (`journal.py:271-282` resolve_id) — 2608.03451

## Pistas não confirmadas (orquestrador/operador decidem)

- Verbo `SCOPE` no `scripts/dispatch/preflight.sh` (2606.00152): molde intra-repo (`PIN`); nenhum repo tem gate de aquisição por path.
- Validação de `relacao` no `normalize_verdict` (2607.28609, 2608.12571, 2608.13558, 2608.16859, 2608.19269, 2608.20202): molde intra-repo (`resolve_id`); enum do llm-council valida escolha, não referência contra memória.
- Selo sha256 + modo do `issue_body` no context_manifest (2608.05703): schema de manifesto não existe literalmente em B.
- Commitment ledger nas fases do issue-executor-master (2608.08160): a nota usa `engine.py:685-691` como espécime de estilo, não capacidade existente.
- Estado terminal por esgotamento (`ABORTED_NO_PROGRESS`) (2607.29211, 2608.11924): agent-workloops tem parada por divergência, não por futilidade.
- Teto de custo pré-voo fail-closed (2608.15888, 2608.16033): `estimate` existe no llm-council (intra); gate de teto não existe em nenhum repo.
- Gate de consumo (consume-once) no resume (2608.03836): intra-repo llm-council, deliberadamente não aplicado pela nota.
