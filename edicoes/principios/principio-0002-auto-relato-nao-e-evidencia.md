---
id: principio-0002
title: "Auto-relato do executor não é evidência de gate — veredito é computado externamente"
status: candidato
camada: a
sinais:
  - "recorrencia: 7 papers independentes (2607.28609, 2608.03744, 2608.06270, 2608.11341, 2608.18565, 2608.19861, 2608.24979)"
  - "transversalidade: 5 repos (llm-council, papers-journal, agent-skills, agent-workloops, scripts)"
evidencias:
  - arxiv: 2607.28609
    data: 2026-08-07
    sinal: recorrencia
    citacao: "tese 3 — juiz que le auto-relato mede retorica (remover narrativa custa 7,2 pp)"
  - arxiv: 2608.03744
    data: 2026-08-05
    sinal: recorrencia
    citacao: "tese 2 — fiscal que so le a deliberacao nao e fiscal; reconsulta em privado"
  - arxiv: 2608.06270
    data: 2026-08-08
    sinal: recorrencia
    citacao: "tese 1 — chamada instrumentada (log de tool_calls) nao e evidencia de uso"
  - arxiv: 2608.24979
    data: 2026-08-25
    sinal: recorrencia
    citacao: "tese 1 — completion e estado computado (grader externo), nao declarado (970 trajetorias)"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Auto-relato do executor não é evidência de gate

## Formulação

Juiz que lê a justificativa, o relatório ou a deliberação do executado mede retórica, não resultado. Verificação de conclusão é estado computado contra artefato/log externo, nunca autodeclaração; fiscal precisa de sinal que o julgado não produziu (reconsulta em privado, grader externo, painel cego ao raciocínio).

## Evidência

- **Recorrência (7 papers)** — 2607.28609 t3 (juiz lê auto-relato = retórica; −7,2 pp sem narrativa), 2608.03744 t2 (fiscal que lê deliberação), 2608.06270 t1 (chamada instrumentada ≠ uso), 2608.11341 t5 (painel cego ao raciocínio), 2608.18565 t1-2 (gate decide o fim; claim sem log é claim não checado), 2608.19861 t4 (evidência admissível = fato do resultado da ferramenta, nunca alegação), 2608.24979 t1 (completion computado, não declarado).
- Repos tocados: llm-council, papers-journal, agent-skills, agent-workloops, scripts.

## Mapa de aplicação

### llm-council
- ressalvas (2608.06270, 2608.18565): auditoria de síntese cega ao raciocínio dos avaliadores.
### papers-journal
- agora (2608.18565): `normalize_verdict` aceita `relacao` como fato renderizado (`journal.py:337-345`) sem log que a sustente.
### agent-skills
- ressalvas (2608.03744, 2608.06270); não aplicar em 2608.24979 (já opera grader externo no harness).
### agent-workloops
- ressalvas (2608.24979): runbook pede evidência do que foi feito, não auto-relato.
### scripts
- não aplicar em 2608.24979 (preflight já é grader determinístico).

## Valor de negócio

Cada gate que hoje aceita a palavra do agente como evidência está medindo a redação do relatório, não a entrega — e o custo do erro é exatamente o custo que o gate existia para evitar. Trocar auto-relato por estado computado é o mesmo gate, com poder de decisão real.
