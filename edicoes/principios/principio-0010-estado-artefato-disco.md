---
id: principio-0010
title: "Estado de trabalho é artefato endereçável em disco, não contexto de sessão"
status: candidato
camada: a
sinais:
  - "recorrencia: 9 papers independentes (2608.10450, 2608.10875, 2608.11924, 2608.19861, 2608.21156, 2608.23283, 2608.23552, 2608.24358, 2608.26070)"
  - "transversalidade: 6 repos (agent-workloops, papers-journal, llm-council, agent-skills, scripts, sisyphus-runtime)"
evidencias:
  - arxiv: 2608.10450
    data: 2026-08-09
    sinal: recorrencia
    citacao: "teses 1-2 — estado dura vel e o par (versao aceita, caminho); delegar muda caminho, so aceitar avanca versao"
  - arxiv: 2608.11924
    data: 2026-08-10
    sinal: recorrencia
    citacao: "tese 6 — comunicacao entre skills por arquivo em diretorio compartilhado; o estado e o disco"
  - arxiv: 2608.19861
    data: 2026-08-16
    sinal: recorrencia
    citacao: "tese 3 — o codigo e dono do estado; grafo conhecido-do-agente sem dono externo nao compra nada"
  - arxiv: 2608.23552
    data: 2026-08-20
    sinal: recorrencia
    citacao: "teses 1-2 — estado vivo e objeto enderecavel; falha de harness nao pode ser lida como falha de modelo"
  - arxiv: 2608.24358
    data: 2026-08-21
    sinal: recorrencia
    citacao: "tese 1 — handoff passa estado persistente verificado, nao transcript"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Estado de trabalho é artefato endereçável em disco

## Formulação

O que atravessa fronteira (fase, sessão, handoff, retomada) é artefato observável com identificador estável — manifesto, task board, par (versão aceita, caminho) — nunca contexto vivo. Nó órfão (produtor sem consumidor) é bug arquitetural; código é dono do estado, não o modelo.

## Evidência

- **Recorrência (9 papers)** — 2608.10450 t1-2, 2608.10875 t2, 2608.11924 t6, 2608.19861 t3, 2608.21156 t3-4, 2608.23283 t1-2, 2608.23552 t1-2, 2608.24358 t1, 2608.26070 t1.

## Mapa de aplicação

### agent-workloops
- agora (2608.26070) / ressalvas (já pratica artefatos persistidos no tracker).
### papers-journal
- agora (2608.23552 itens a+c): `deep/` na raiz é nó órfão (o conversor só lê `edicoes/deep/`); ressalvas em 2608.21156.
### llm-council
- agora (2608.23283) / não aplicar (2608.19861 — implementação de referência).
### agent-skills
- ressalvas: manifest como âncora, estado das fases no contexto.
### scripts
- ressalvas (2608.19861).
### sisyphus-runtime
- não aplicar (2608.24358) / ressalvas (2608.26070).

## Valor de negócio

Estado que vive só em contexto de sessão morre com a sessão — e cada sessão nova paga para redescobrir o que já foi decidido. Artefato endereçável em disco é o que torna o trabalho retomável por qualquer sessão sem contexto prévio (a propriedade que as issues do próprio ciclo de skills prometem).
