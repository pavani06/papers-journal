---
id: principio-0006
title: "Incompletude é estado de primeira classe — truncagem declarada e campo estruturado atravessando fronteiras"
status: candidato
camada: c
sinais:
  - "recorrencia: 8 papers independentes (2608.04569, 2608.05013, 2608.08160, 2608.08389, 2608.11079, 2608.24358, 2608.24569, 2608.26070)"
  - "transversalidade: 6 repos (papers-journal, llm-council, agent-workloops, agent-skills, sisyphus-runtime, scripts)"
  - "transferencia: 2 pares confirmados — flag de truncagem (papers-journal<-llm-council) e blind spot NOT_FOUND (papers-journal<-agent-skills)"
evidencias:
  - arxiv: 2608.04569
    data: 2026-08-05
    sinal: recorrencia
    citacao: "teses 4-5 — truncar por caractere e selecao com funcao degenerada; carimbar 'completo' sobre corte e o dano"
  - arxiv: 2608.05013
    data: 2026-08-06
    sinal: recorrencia
    citacao: "tese 4 — pressao de contexto merece compressao instrumentada, nao truncagem cega"
  - arxiv: 2608.08160
    data: 2026-08-08
    sinal: recorrencia
    citacao: "tese 5 — comprimir memoria realoca a falha: preservar atos/decisoes literais, nao o resumo"
  - arxiv: 2608.11079
    data: 2026-08-09
    sinal: recorrencia
    citacao: "teses 5-6 — sob incerteza, travar verbatim; compressao liga a cada escrita, nao na faxina anual"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Incompletude é estado de primeira classe

## Formulação

`[:N]` é o pior compressor (corta resultados/conclusões) e declarar "completo" sobre truncado é o dano real: todo corte é declarado, com o flag propagado na fronteira da função. Nas fronteiras (handoff, fase, sessão) o que passa é campo estruturado e verificado, não resumo — sumário automático perde para promoção explícita; e o que não foi achado vira `NOT_FOUND` com locais procurados, nunca silêncio.

## Evidência

- **Recorrência (8 papers)** — 2608.04569 t4-5, 2608.05013 t4, 2608.08160 t5, 2608.08389 t2-4, 2608.11079 t5-6, 2608.24358 t1, 2608.24569 t5, 2608.26070 t1-2.
- **Transferência (2 pares confirmados)** — (1) papers-journal `deepdive.py:74-76` retorna `text[:MAX_CHARS], True` (flag `full` mesmo com corte) ← llm-council avisos nomeados de truncagem por estágio (`engine.py:487-493`, `:552-557`); (2) papers-journal `paths.py:101-104` engole erros de leitura em silêncio ← agent-skills `not_found[]` com `locations_searched` obrigatório (`fases-0-2.md:229-238`, `SKILL.md:230`).

## Mapa de aplicação

### papers-journal
- agora/ressalvas: `MAX_CHARS=160k` com flag "texto completo" citado em 3 notas (2608.04569, 2608.10692, 2608.23283); `bloco_memoria` sem blind spot.
### llm-council
- ressalvas: política de truncamento no checkpoint (aviso já existe, falta registro no dado).
### agent-workloops
- agora (2608.24358/2608.26070): escalada passa estado persistente verificado, não transcript.
### agent-skills
- ressalvas: compressão de handoff e manifesto.
### sisyphus-runtime
- não aplicar em 2608.24358 (já encarna), ressalvas em 2608.26070.
### scripts
- ressalvas (2608.26070).

## Valor de negócio

A nota de deep dive publicada hoje afirma por escrito leitura completa de um texto do qual foram amputadas exatamente as seções que a nota preenche (conclusão, limitações) — promessa falsa de 3 linhas para corrigir, custo zero. Blind spot distingue "não havia nada" de "não consegui ler" no insumo que governa relações entre edições.
