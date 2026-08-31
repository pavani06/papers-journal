---
id: principio-0009
title: "Verificação de claims — existência ≠ suporte; refutação dirigida; veto não-compensatório"
status: candidato
camada: a
sinais:
  - "recorrencia: 6 papers independentes (2608.06270, 2608.11994, 2608.12571, 2608.13558, 2608.19269, 2608.23564)"
  - "transversalidade: 6 repos (papers-journal, llm-council, agent-skills, ciot-authpay-repo, koda-desafio, agent-workloops)"
evidencias:
  - arxiv: 2608.11994
    data: 2026-08-10
    sinal: recorrencia
    citacao: "teses 1-4 — condensar em claims decisivos e verificar; procurar evidencia negativa dirigida; claim derrubado inviabiliza (veto)"
  - arxiv: 2608.12571
    data: 2026-08-10
    sinal: recorrencia
    citacao: "teses 1-3 — separar existencia e suporte; registrar o span; citacao verbatim conferivel offline"
  - arxiv: 2608.13558
    data: 2026-08-13
    sinal: recorrencia
    citacao: "tese 1 — claim check e operacao deterministica sobre registro de execucao"
  - arxiv: 2608.19269
    data: 2026-08-16
    sinal: recorrencia
    citacao: "tese 1 — separar score produzido de claim licenciado (substrate, familia, claims)"
  - arxiv: 2608.23564
    data: 2026-08-20
    sinal: recorrencia
    citacao: "teses 3-4 — veto multiplicativo, nao aditivo; denuncia so vale como contraexemplo executavel"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Verificação de claims — existência ≠ suporte

## Formulação

"A fonte existe" e "a fonte sustenta esta proposição" são gates separados; o segundo exige span citado conferível (verbatim, offline). O verificador pergunta "ache o contraexemplo deste claim decisivo", e um claim decisivo derrubado é gate vermelho (veto multiplicativo), não desconto em média. Score produzido sem binding a substrate não autoriza o claim anexado ao número.

## Evidência

- **Recorrência (6 papers)** — 2608.06270 t5 (sobreposição lexical ≠ sustentação causal), 2608.11994 t1-4 (refutação dirigida; veto), 2608.12571 t1-3 (existência/suporte; span; verbatim), 2608.13558 t1 (claim check determinístico), 2608.19269 t1 (score vs. claim licenciado), 2608.23564 t3-4 (veto multiplicativo; contraexemplo executável).

## Mapa de aplicação

### papers-journal
- agora (2608.13558, 2608.11994, 2608.19269): `normalize_verdict` renderiza `relacao` (`avanca`/`contradiz`) como fato (`journal.py:337-345`) sem conferir que a edição citada existe nem que a tese é dela.
### llm-council
- ressalvas (2608.12571 fonte+trecho no veredito; 2608.13558 já implementa claim check).
### agent-skills
- ressalvas (2608.11994): issue-review reconstitui conformidade em vez de falsificar.
### ciot-authpay-repo
- não aplicar (2608.12571): já implementa custódia com span.
### koda-desafio
- ressalvas (2608.19269): witness como substrate.
### agent-workloops
- agora/ressalvas (2608.23564 auditoria estrutural; 2608.19269 ressalvas).

## Valor de negócio

O jornal publica hoje relações entre edições (`avança`/`contradiz`) que podem apontar para tese que nunca existiu — o artefato mais confiável do ecossistema com um vazamento de veracidade no meio. Verificação determinística de claim (uma função, sem LLM) fecha isso: o que sustenta o número viaja com ele.
