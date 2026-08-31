---
id: principio-0004
title: "Proveniência sela o artefato, não o log — produtor, config e ponteiro de evidência viajam dentro do registro"
status: candidato
camada: c
sinais:
  - "recorrencia: 14 papers independentes (2607.28048, 2608.05784, 2608.12571, 2608.12990, 2608.16859, 2608.23200, 2608.23283, 2608.03451, 2608.06867, 2608.09819, 2608.15242, 2608.16391, 2608.17271, 2608.22510)"
  - "transversalidade: 7 repos (scripts, sisyphus-runtime, llm-council, papers-journal, agent-workloops, agent-skills, ciot-authpay-repo)"
  - "transferencia: 4 pares confirmados — selo de produtor (papers-journal<-llm-council), trace-link (scripts<-sisyphus-runtime), reamarcacao (agent-skills<-llm-council), selo de integridade (papers-journal<-llm-council)"
evidencias:
  - arxiv: 2607.28048
    data: 2026-08-07
    sinal: recorrencia
    citacao: "tese 3 — trace-link e campo obrigatorio da regra; contagem nao permite reabrir o caso"
  - arxiv: 2608.05784
    data: 2026-08-08
    sinal: recorrencia
    citacao: "tese 2 — ponteiro de evidencia e o produto, nao o adorno"
  - arxiv: 2608.12571
    data: 2026-08-10
    sinal: recorrencia
    citacao: "tese 2-3 — registrar o span, nao o documento; verbatim conferivel offline com grep"
  - arxiv: 2608.06867
    data: 2026-08-09
    sinal: recorrencia
    citacao: "tese 1 — toda escolha de despacho vira objeto versionado com 4 campos, inclusive evidencia posterior"
  - arxiv: 2608.16391
    data: 2026-08-14
    sinal: recorrencia
    citacao: "tese 1 — modelo pedido vs. servido sao campos distintos; nome de API e alegacao"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Proveniência sela o artefato, não o log

## Formulação

A unidade versionada é o par (produtor, configuração) — modelo pedido vs. servido, código, config resolvida, critério de despacho — e todo item de memória, princípio, claim ou veredito carrega endereço resolvível de volta à linha/traço que o sustenta (span citado, path, hash). Contagem de evidência ("baseado em N handoffs") é boato, não memória; registro produzido sob configuração desconhecida é ininterpretável depois de qualquer edição; aprovação vale para um objeto (hash), não para uma intenção.

## Evidência

- **Recorrência (14 papers)** — ponteiro/trace-link (2607.28048 t3, 2608.05784 t2, 2608.12571 t2-3, 2608.12990 t3, 2608.16859 t1, 2608.23200 t2, 2608.23283 t5); selo de produtor/config (2608.03451 t5, 2608.06867 t1, 2608.09819 t1, 2608.15242 t3, 2608.16391 t1, 2608.17271 t4, 2608.22510 t1).
- **Transferência (4 pares confirmados)** — (1) papers-journal cache sem modelo/hash/prompt (`journal.py:500-504`) ← llm-council `provenance.py:107-119` selado antes de rodar (`engine.py:435-438`); (2) scripts `reflection/run.ts` gravava só contagem ← sisyphus-runtime `dispatch-rule-amendment-provenance.md` (fonte + adendos + See also) — **par já consumado pós-nota** (`run.ts:382-387`); (3) agent-skills sem SHA do HEAD revisado ← llm-council `provenance.py:122-136`; (4) selo de integridade papers-journal ← llm-council `engine.py:144-146`.

## Mapa de aplicação

### scripts
- ressalvas: proveniência ainda descartada em partes da serialização.
### sisyphus-runtime
- ressalvas: princípios com contagens, sem spans; formato completo das dispatch-rules é o molde.
### llm-council
- ressalvas + agora (2608.23283): selo de servidor/substituição de rota ainda falta.
### papers-journal
- agora (2608.15242, 2608.22510): selo de produtor no cache (modelo, horário, sha256 do prompt/interests).
### agent-workloops
- ressalvas (2608.10450): par (versão aceita, caminho) no handoff.
### agent-skills
- agora (2608.16859): evidência por teste endereçada ao artefato.
### ciot-authpay-repo
- não aplicar (2608.12571): cadeia de custódia já implementa.

## Valor de negócio

Sem selo de produtor, nenhum erro de triagem é atribuível e nenhuma série histórica é comparável (troca de modelo no meio da série é indetectável); sem ponteiro de evidência, memória e princípios viram boato não auditável. O par scripts→sisyphus-runtime já consumado prova o mecanismo: a nota apontou o molde, o molde foi adotado.
