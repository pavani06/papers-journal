---
id: principio-0013
title: "Injeção de memória tem gate de admissão e política de volume por regime"
status: candidato
camada: a
sinais:
  - "recorrencia: 5 papers independentes (2608.07169, 2608.15008, 2608.20202, 2608.24189, 2608.26005)"
  - "transversalidade: 4 repos (papers-journal, scripts, sisyphus-runtime, agent-skills)"
evidencias:
  - arxiv: 2608.15008
    data: 2026-08-12
    sinal: recorrencia
    citacao: "teses 1,3,5 — k explicito por ponto de injecao; ranquear sem cortar e trabalho jogado fora; registro por tarefa de ajudou/desviou"
  - arxiv: 2608.20202
    data: 2026-08-17
    sinal: recorrencia
    citacao: "teses 1,4 — relevancia nao e autorizacao; volume e fator de risco monotonico (25% ja degrada)"
  - arxiv: 2608.24189
    data: 2026-08-21
    sinal: recorrencia
    citacao: "tese 1 — recall alto sem uso medido nao e evidencia de memoria funcionando"
  - arxiv: 2608.07169
    data: 2026-08-09
    sinal: recorrencia
    citacao: "teses 1,3 — granularidade define quando a memoria chega; cota pequena com limiar, sem preencher"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Injeção de memória tem gate de admissão e política de volume por regime

## Formulação

Relevância semântica não autoriza injeção: recuperação e admissão são critérios distintos, volume é hiperparâmetro com ótimo interno (k explícito, cota pequena, cortar de fato), e a unidade de avaliação é o momento de decisão ("ajudou ou desviou"), com contratos separados por regime (QA vs. execução). Recall alto sem uso medido não é evidência de memória funcionando.

## Evidência

- **Recorrência (5 papers)** — 2608.07169 t1-3, 2608.15008 t1-3/5, 2608.20202 t1/4, 2608.24189 t1-2 (79% recall vs 7,9% uso), 2608.26005 t1.

## Mapa de aplicação

### papers-journal
- agora (2608.24189 — conferir `ref_data`) / ressalvas (`bloco_memoria` com janela de 10 sem cota por injeção).
### scripts
- ressalvas: exploration_cache e prt sem política de volume.
### sisyphus-runtime
- ressalvas: contratos dos namespaces; já implementa parte.
### agent-skills
- veredito não extraído (2608.07169).

## Valor de negócio

Memória que injeta por relevância sem gate de admissão degrada a decisão monotonicamente com o volume (25% já degrada) — o sistema fica "mais informado" e pior. Gate de admissão + k explícito + registro por decisão transforma memória de ruído em alavanca medida.
