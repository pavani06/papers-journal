---
id: principio-0012
title: "Fronteira de aquisição — a cerca viaja com o dado; registro do que entrou no contexto"
status: candidato
camada: c
sinais:
  - "recorrencia: 10 papers independentes (2606.00152, 2608.00677, 2608.03744, 2608.09867, 2608.21500, 2608.10692, 2608.13417, 2608.15008, 2608.24189, 2608.26005)"
  - "transversalidade: 6 repos (scripts, agent-skills, llm-council, papers-journal, sisyphus-runtime, koda-desafio)"
  - "transferencia: 2 pares confirmados — cerca de dado nao confiavel (papers-journal<-agent-skills) e registro de aquisicao (scripts<-llm-council)"
evidencias:
  - arxiv: 2606.00152
    data: 2026-08-10
    sinal: recorrencia
    citacao: "teses 1-2 — dois registros (dito vs. adquirido); escopo tem duas metades, verbo e alvo"
  - arxiv: 2608.00677
    data: 2026-08-02
    sinal: recorrencia
    citacao: "tese 2 — a pergunta e 'isso e controlado por alguem fora do meu perimetro?', nao 'de onde veio o canal'"
  - arxiv: 2608.21500
    data: 2026-08-17
    sinal: recorrencia
    citacao: "tese 1 — fronteira existe no formato da entrada (marca de proveniencia); conteudo nao confiavel fora do corpus do verificador"
  - arxiv: 2608.24189
    data: 2026-08-21
    sinal: recorrencia
    citacao: "teses 1-2 — recall e uso sao descorrelacionados (79% vs 7,9%); avalia-se o momento de decisao"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Fronteira de aquisição — a cerca viaja com o dado

## Formulação

A fronteira de conteúdo não confiável cobre a origem (quem controla o conteúdo), não o canal (GitHub vs. config vs. texto de paper); texto de terceiro entra com marca de proveniência conferível por máquina, nunca no mesmo nível sintático da instrução. Escopo de dispatch tem duas metades: verbo e alvo. E a trilha registra o que foi adquirido (entrou no contexto) e a cobertura da busca — não só o output e o custo.

## Evidência

- **Recorrência (10 papers)** — fronteira de aquisição (2606.00152 t1-2, 2608.00677 t2, 2608.03744 t4, 2608.09867 t5, 2608.21500 t1/4); registro de cobertura/aquisição (2608.10692 t1-3, 2608.13417 t3, 2608.15008 t5, 2608.24189 t1, 2608.26005 t1).
- **Transferência (2 pares confirmados)** — (1) papers-journal catálogo/abstract de terceiro interpolado cru no prompt (`journal.py:142-147`) ← agent-skills cerca `<<<CONTEUDO_NAO_CONFIAVEL ...>>>` que viaja nos prompts repassados (`issue-executor-master/SKILL.md:85-105`); (2) scripts `trajectory.py:26-57` grava só o que foi dito ← llm-council `masked_terms` (`engine.py:498-506`) como trilha do que entrou.

## Mapa de aplicação

### scripts
- ressalvas (2606.00152): verbo `SCOPE` opt-in no `preflight.sh` (allowlist de alvo).
### agent-skills
- ressalvas (2608.00677; 2606.00152): allowed-tools como declaração, não gate de aquisição.
### llm-council
- ressalvas (2608.21500): bundle de evidência interpolado com cabeçalho em prosa.
### papers-journal
- ressalvas (2608.00677): texto do arXiv interpolado na instrução sem marcador de fronteira.
### sisyphus-runtime
- ressalvas (2608.09867): regras em prosa como instrução de mesma sintaxe.
### koda-desafio
- não aplicar (2608.21500): já implementa em `verificar_pii.py`.

## Valor de negócio

O vetor de injeção não é o canal, é a fronteira: qualquer texto que um terceiro controla (paper do arXiv, issue body, resposta de ferramenta) pode instruir o editor se entrar sem cerca. A marca de proveniência que viaja com o dado é o que mantém a distinção dado/instrução em todos os repasses — custo de tokens de marcador, eliminação de uma classe de incidente.
