---
id: principio-0003
title: "Estado herdado se valida contra o observável antes do uso — fail-closed com erro nomeado"
status: adotado
camada: c
sinais:
  - "recorrencia: 5 papers independentes (2608.04574, 2608.05219, 2608.05703, 2608.10875, 2608.21156)"
  - "transversalidade: 5 repos (sisyphus-runtime, papers-journal, llm-council, agent-skills, agent-workloops)"
  - "transferencia: 3 pares confirmados — selo de integridade (papers-journal<-llm-council), reamarcacao revisado<-publicado (agent-skills<-llm-council), casamento tolerante (llm-council<-papers-journal)"
evidencias:
  - arxiv: 2608.04574
    data: 2026-08-05
    sinal: recorrencia
    citacao: "teses 1-3 — memoria sem audit perde para nao carregar; audit na modalidade em que a verdade vive (hash/HEAD/mtime); barato-e-presente vence caro-e-ausente"
  - arxiv: 2608.05219
    data: 2026-08-05
    sinal: recorrencia
    citacao: "teses 1-3 — gate de compatibilidade de estado antes de aplicar orientacao passada; assinatura explicita, deterministica, comparavel"
  - arxiv: 2608.21156
    data: 2026-08-17
    sinal: recorrencia
    citacao: "tese 5 — guarda de idempotencia olha evidencia (integridade), nao existencia"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: 2026-08-30
---

# Estado herdado se valida contra o observável antes do uso

## Formulação

Nenhuma leitura de memória persistente, cache ou parcial de retomada entra como fato: entra como evidência contestável, validada contra o observável (hash, HEAD, mtime, byte) e contra assinatura de compatibilidade de estado. Existência de arquivo não é validade; casar uma dimensão só (config) e ignorar outra (código) é pior que não casar nada. Divergência aborta com erro nomeado, nunca gravando.

## Evidência

- **Recorrência (5 papers)** — 2608.04574 t1-3, 2608.05219 t1-3, 2608.05703 t1, 2608.10875 t1-2, 2608.21156 t5.
- **Transferência (3 pares confirmados por leitura)** — (1) papers-journal `--render-only` reidrata cache sem confronto (`journal.py:455-462`, `paths.py:88-107`) ← llm-council digest sha256 + guardas fail-closed (`engine.py:144-146`, `:682-740`); (2) agent-skills revisão não registra SHA do HEAD revisado (`issue-review/SKILL.md:169-179`) ← llm-council `provenance.py:122-136` (`compare()`); (3) llm-council `audit.py:207-208` casamento por substring crua ← papers-journal `resolve_id` (`journal.py:271-282`, normalização de forma + contenção bidirecional).

## Mapa de aplicação

### sisyphus-runtime
- ressalvas (2608.04574): facts/state entram como fato; falta carimbo verified-against/last-verified (molde: repos-registry.md:19-21).
### papers-journal
- agora (2608.04574, 2608.21156): cache e memória reidratados sem selo; guard de idempotência por existência.
### llm-council
- não aplicar em 2608.04574 (já implementa); ressalvas em 2608.05219 (falta guarda `code_drift` no resume).
### agent-skills
- ressalvas (2608.05219, 2608.10875): `main_head` gravado e nunca comparado.
### agent-workloops
- agora (2608.05219): objeto comparável no handoff (versão aceita vs. caminho).

## Valor de negócio

Estado herdado é o que governa decisões futuras (memória de 6 edições, retomada de execução paga, aprovação de merge). Validar contra o observável antes do uso elimina a classe "cache/estado corrompido ou adulterado republia e contamina silenciosamente" — o padrão que 3 notas independentes apontam no mesmo par de repos.
