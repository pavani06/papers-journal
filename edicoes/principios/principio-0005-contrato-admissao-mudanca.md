---
id: principio-0005
title: "Contrato de admissão de mudança em skill/prompt/harness — baseline congelado, extensão + preservação, corpus binário"
status: candidato
camada: a
sinais:
  - "recorrencia: 10 papers independentes (2608.05466, 2608.06301, 2608.06352, 2608.07545, 2608.08722, 2608.09802, 2608.19197, 2608.19880, 2608.23041, 2608.27260)"
  - "transversalidade: 6 repos (agent-skills, llm-council, papers-journal, agent-workloops, koda-desafio, sisyphus-runtime)"
  - "transferencia: suíte offline + golden byte a byte (papers-journal<-llm-council) e fixture negativa (agent-skills<-koda-desafio) confirmadas"
evidencias:
  - arxiv: 2608.07545
    data: 2026-08-09
    sinal: recorrencia
    citacao: "teses 1-3 — mudanca de skill e candidato, nao commit no vivo; extensao+preservacao obrigatorias; corpus binario e pre-requisito material"
  - arxiv: 2608.05466
    data: 2026-08-06
    sinal: recorrencia
    citacao: "teses 1,3,4 — duplo portao (oraculo + contrato); sandbox fresco; baseline auto-gravado e aprovacao sem evidencia"
  - arxiv: 2608.06301
    data: 2026-08-08
    sinal: recorrencia
    citacao: "tese 1 — semente imutavel com E(H0) gravado; cada candidato e commit imutavel"
  - arxiv: 2608.19197
    data: 2026-08-16
    sinal: recorrencia
    citacao: "tese 2 — gate que nunca reprovou nada nao tem poder discriminante, e isso e mensuravel"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Contrato de admissão de mudança em skill/prompt/harness

## Formulação

Nenhuma mudança em skill/prompt/fluxo entra no artefato vivo sem: baseline congelado com score gravado, corpus de tarefas com veredito binário, e as duas metades do contrato — extensão (resolve algo novo) e preservação (o já resolvido continua resolvido). Verificador que se auto-aprova (golden que se grava sozinho, fixture persistente) é falso verde; gate que nunca reprovou não tem poder discriminante mensurável.

## Evidência

- **Recorrência (10 papers)** — 2608.05466 t1-4, 2608.06301 t1/4, 2608.06352 t1-3, 2608.07545 t1-3, 2608.08722 t3, 2608.09802 t1-2, 2608.19197 t2, 2608.19880 t3, 2608.23041 t3, 2608.27260 t1-2.
- **Transferência (2 pares confirmados)** — (1) papers-journal sem `tests/` nem `.github/` em cron diário ← llm-council `test_offline.py:450-505` (golden byte a byte + bootstrap) e `.github/workflows/tests.yml:1-14`; (2) agent-skills gate `contract` sem fixture negativa ← koda-desafio `guard/run-fixtures.sh:2-4,11-12` (cada guard tem um fixture que PRECISA reprovar) — parcialmente consumado (`pytest.raises` já corrigido no harness do agent-skills).

## Mapa de aplicação

### agent-skills
- agora (2608.09802 a+d, 2608.19197, 2608.27260 — gate `integration` morto): fixture negativo por skill no molde do koda-desafio.
### llm-council
- ressalvas + não agora (2608.09802): backlog pós-1-vs-N; já tem golden e prereg.
### papers-journal
- agora (2608.09802, 2608.27260): suíte offline + golden de render + CI de 14 linhas.
### agent-workloops
- ressalvas (2608.05466, 2608.06352): corpus de casos antes de doutrinar.
### koda-desafio
- ressalvas (2608.08722, 2608.19197): já pratica guards com fixture negativo.
### sisyphus-runtime
- agora como convenção (2608.27260).

## Valor de negócio

O maior risco de mudança em skill é regressão silenciosa de comportamento já resolvido — a preservação é a metade que ninguém mede. Com baseline + corpus binário, toda edição de skill vira candidato com evidência; sem isso, editar skill é apostar.
