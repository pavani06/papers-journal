---
id: principio-0001
title: "Controle determinístico fora do modelo — instrução em prompt não é controle"
status: adotado
camada: a
sinais:
  - "recorrencia: 21 papers independentes (2606.00152, 2607.29211, 2608.08160, 2608.11924, 2608.12307, 2608.15888, 2608.17597, 2608.19861, 2608.23740, 2608.24569, 2608.12440, 2608.13558, 2608.13900, 2608.16590, 2608.18580, 2608.20634, 2608.27260, 2608.13547, 2608.19741, 2608.21156, 2608.24979)"
  - "transversalidade: 6 repos (scripts, agent-skills, llm-council, papers-journal, agent-workloops, sisyphus-runtime)"
  - "transferencia: papers-journal usa exit-code/existencia como veredito (journal.py:489, papers-daily.sh:84) enquanto llm-council ja observa efeito/estado (engine.py:761-764)"
evidencias:
  - arxiv: 2606.00152
    data: 2026-08-10
    sinal: recorrencia
    citacao: "tese 4 — defesa por prompt deixa >metade do baseline; mecanismo fora do modelo"
  - arxiv: 2608.11924
    data: 2026-08-11
    sinal: recorrencia
    citacao: "tese 4 — gates mecanicos 14%->69% de deteccao; camada deterministica primeiro"
  - arxiv: 2608.13558
    data: 2026-08-13
    sinal: recorrencia
    citacao: "tese 2 — gate tem que rejeitar para ser gate; aviso sobre claim falso e registro do erro"
  - arxiv: 2608.17597
    data: 2026-08-14
    sinal: recorrencia
    citacao: "teses 2-3 — fronteira artefato->config exige controle deterministico; deteccao nao e gate (97,9% ASR 31,2%)"
  - arxiv: 2608.13547
    data: 2026-08-13
    sinal: recorrencia
    citacao: "tese 2 — codigo de saida nao e veredito; ~47% das falhas saem com rc 0"
  - arxiv: 2608.13900
    data: 2026-08-13
    sinal: recorrencia
    citacao: "tese 4 — sinal de confianca que nunca bloqueia tem o custo do instrumento sem o beneficio"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: 2026-08-30
---

# Controle determinístico fora do modelo

## Formulação

Onde o requisito é "não pode acontecer" (ou "tem que acontecer"), o mecanismo é código fora do modelo: validação antes da chamada/execução, fail-closed, checável. Defesa por prompt, anúncio em prosa e intenção declarada são redutores, nunca gates. Checador que emite aviso e deixa o artefato sair produz telemetria, não controle; guard que confere presença (exit code, arquivo existe) é cego para efeito parcial e truncamento — validação observa o estado final, não a terminação.

## Evidência

- **Recorrência (21 papers)** — teses convergentes em 3 grupos: (a) gate determinístico (2606.00152 t4, 2607.29211 t3, 2608.08160 t1-2, 2608.11924 t4, 2608.12307 t1-3, 2608.15888 t1, 2608.17597 t2-3, 2608.19861 t5, 2608.23740 t2, 2608.24569 t2); (b) gate que não bloqueia é telemetria (2608.12440 t5, 2608.13558 t2, 2608.13900 t4, 2608.16590 t2, 2608.17597 t3, 2608.18580 t4, 2608.20634 t4, 2608.27260 t2); (c) efeito vs. presença (2608.13547 t2-3, 2608.19741 t2-3, 2608.20634 t3, 2608.21156 t5, 2608.24979 t4).
- **Transferência** — o guard de idempotência do cron (`bin/papers-daily.sh:84`) e o `--render-only` (`journal.py:455-462`) conferem existência, não validade; o llm-council já opera o padrão oposto (digest + guardas fail-closed `engine.py:682-740`).

## Mapa de aplicação

### scripts
- ressalvas (2606.00152, 2608.19861): `preflight.sh` gate determinístico correto na natureza, mas cobre só o verbo, não o alvo.
### agent-skills
- ressalvas majoritário; agora em 2608.17597 (controle na fronteira artefato→config). Gate `integration` fantasma recorrente.
### llm-council
- ressalvas; em 2608.19861 "não aplicar" — já é a referência (guardas fail-closed nomeadas).
### papers-journal
- agora (2608.15888): delimitador determinístico de fronteira; veredito por efeito, não existência.
### agent-workloops
- ressalvas (2608.08160): compromisso como invariante checável.
### sisyphus-runtime
- agora como convenção (2608.27260): gate que não rodou não aprova.

## Valor de negócio

Onde o custo de falha é alto (cron desassistido, publicação, merge), trocar prosa/prompt/existência por código fail-closed converte "reza para não acontecer" em propriedade verificável — o custo é uma função de poucas linhas; o benefício é eliminar a classe inteira de falha silenciosa.
