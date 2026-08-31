---
id: principio-0014
title: "Promoção por execução validada — provisório vs. promovido, não por forma"
status: candidato
camada: a
sinais:
  - "recorrencia: 6 papers independentes (2608.07545, 2608.14036, 2608.25500, 2608.26005, 2608.26530, 2608.23200)"
  - "transversalidade: 6 repos (agent-skills, agent-workloops, llm-council, sisyphus-runtime, scripts, papers-journal)"
evidencias:
  - arxiv: 2608.14036
    data: 2026-08-12
    sinal: recorrencia
    citacao: "tese 2 — destilar skill exige rotulo de desfecho junto do traco (senao importa a falha)"
  - arxiv: 2608.07545
    data: 2026-08-09
    sinal: recorrencia
    citacao: "tese 2 — admissao tem duas metades (extensao + preservacao); so checar forma nao e nenhuma"
  - arxiv: 2608.23200
    data: 2026-08-19
    sinal: recorrencia
    citacao: "tese 1 — promover por proveniencia de execucao; SKILL.md bem-formado nao e evidencia de resultado"
  - arxiv: 2608.25500
    data: 2026-08-25
    sinal: recorrencia
    citacao: "promocao de receita por execucao real, nao por well-formedness"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Promoção por execução validada

## Formulação

Artefato (skill, princípio, receita, aresta) é promovido por proveniência de execução verificada, não por aparência/well-formed: nasce provisório na execução e só vira promovido por gate próprio. Aresta declarada não é aresta validada; gate de forma não é gate de resultado. (Nota de extração: relatório da camada a+b foi truncado neste tema — 3ª evidência; o padrão acima reflete o que foi registrado, re-verificação na próxima re-síntese.)

## Evidência

- **Recorrência (6 papers, extração parcial)** — 2608.07545 t2, 2608.14036 t2 (destilar exige rótulo de desfecho), 2608.25500 (promoção de receita por execução real), 2608.26005, 2608.26530, 2608.23200 t1 (proveniência de execução, não forma). Repos: agent-skills, agent-workloops, llm-council, sisyphus-runtime, scripts, papers-journal.

## Mapa de aplicação

### agent-skills
- ressalvas: skills promovidas por contrato de forma; falta gate de execução validada.
### agent-workloops
- ressalvas: playbooks promovidos por documentação, não por caso real.
### llm-council
- ressalvas: candidato vs. chamável (promoção de config por uso).
### sisyphus-runtime
- ressalvas: princípios promovidos por revisão, não por execução que os exercite.
### scripts
- ressalvas: receitas sem trilha de execução que as valide.
### papers-journal
- ressalvas: vereditos renderizados como fato sem gate de execução.

## Valor de negócio

O ciclo de skills já nasce com a semente certa (provisório → promovido por gate); o que falta é o gate ser de execução, não de forma. Artefato promovido sem execução que o valide é doutrina sem evidência — o operador confia em documento bem-formado como se fosse resultado.
