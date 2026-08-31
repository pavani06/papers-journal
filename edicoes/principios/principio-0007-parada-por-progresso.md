---
id: principio-0007
title: "Parada por progresso, não por teto — estado terminal nomeado e anti-futilidade"
status: candidato
camada: a
sinais:
  - "recorrencia: 9 papers independentes (2607.29211, 2608.06867, 2608.09802, 2608.11924, 2608.12440, 2608.16033, 2608.16425, 2608.18565, 2608.19799)"
  - "transversalidade: 5 repos (agent-skills, llm-council, papers-journal, agent-workloops, scripts)"
evidencias:
  - arxiv: 2607.29211
    data: 2026-08-07
    sinal: recorrencia
    citacao: "teses 1-4 — recusa e saida de terceiro tipo; taxa futu il e metrica barata; tentativa sem teste de avanco e gerador de futilidade"
  - arxiv: 2608.06867
    data: 2026-08-09
    sinal: recorrencia
    citacao: "tese 5 — rodada extra e custo ate prova: loops precisam evidencia de que N+1 melhorou"
  - arxiv: 2608.12440
    data: 2026-08-10
    sinal: recorrencia
    citacao: "tese 4 — parada por achados-zero (convergencia), nao por teto de tentativas"
  - arxiv: 2608.18565
    data: 2026-08-15
    sinal: recorrencia
    citacao: "tese 5 — indeterminado e falha: esgotados os retries, reportar incompletude, nunca entregar"
  - arxiv: 2608.16425
    data: 2026-08-24
    sinal: recorrencia
    citacao: "tese 4 — encerrar nao e descartar: parar o gasto preservando a evidencia/voto"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Parada por progresso, não por teto

## Formulação

Orçamento de tentativas sem critério de progresso converte custo em ruído: o limite vem acompanhado de teste de avanço verificável e de um estado terminal tipado (recusa calibrada, refutação, incompletude) — nunca "registra e segue". Rodada extra é custo até prova em contrário; quem decide o fim é o gate, não o executor.

## Evidência

- **Recorrência (9 papers)** — 2607.29211 t1-4 (recusa como saída; taxa fútil; portão de parada como condição de aborto do harness), 2608.06867 t5 (rodada extra é custo até prova), 2608.09802 t5 (ciclo improdutivo = sinal contável → abortar/escalar), 2608.11924 t2 (estado terminal de refutação), 2608.12440 t4 (achados-zero), 2608.16033 t6 (reavaliação é passo explícito, ocorre em 38-63%), 2608.16425 t4 (encerrar preservando o voto), 2608.18565 t5 (indeterminado é falha), 2608.19799 t1 (executor não escolhe quando parar).

## Mapa de aplicação

### agent-skills
- ressalvas (2607.29211): "3 tentativas e segue" é a anti-tese escrita no próprio issue-executor-master; agora em 2608.19799 item i.
### llm-council
- ressalvas: parada do estágio 2 por convergência (com ressalva de viés de latência em conselho de 4).
### papers-journal
- ressalvas (2607.29211) / agora (2608.18565).
### agent-workloops
- agora (2608.12440): seção de exceção com convergência.
### scripts
- ressalvas (2608.16425): campo `confidence` ordinal como sinal de convergência.

## Valor de negócio

Todo loop de retry sem teste de avanço paga rodadas que não aproximam — e o gargalo é atenção do operador, então cada rodada fútil é atenção desperdiçada. Estado terminal nomeado converte "desistiu" em informação (recusa calibrada, refutação, incompletude), que é o insumo de melhoria, não lixo.
