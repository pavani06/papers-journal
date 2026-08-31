---
id: principio-0008
title: "Falha registrada com genótipo — memória de fracasso consultável e comparação contrastiva"
status: candidato
camada: a
sinais:
  - "recorrencia: 5 papers independentes (2607.28048, 2608.07645, 2608.22510, 2608.23041, 2608.27454)"
  - "transversalidade: 5 repos (scripts, sisyphus-runtime, agent-skills, papers-journal, llm-council)"
evidencias:
  - arxiv: 2608.07645
    data: 2026-08-09
    sinal: recorrencia
    citacao: "teses 1-4 — interseccao de falhas localiza; fracasso com genotipo anexado; erro com chave estavel, nao prosa"
  - arxiv: 2607.28048
    data: 2026-08-07
    sinal: recorrencia
    citacao: "tese 2 — contraste falha-x-sucesso e a fonte (96 regras verbosas vs 38 com o par)"
  - arxiv: 2608.22510
    data: 2026-08-18
    sinal: recorrencia
    citacao: "tese 4 — falha e evidencia a preservar (checker, hash antes/depois, status)"
  - arxiv: 2608.27454
    data: 2026-08-26
    sinal: recorrencia
    citacao: "tese 2 — trilha de impacto programatica: memoria de fracasso e arquivo consultavel (evita repetir intervencao falhada)"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Falha registrada com genótipo

## Formulação

O arquivo que só guarda sucesso não sustenta melhoria: fracasso é registrado com a versão do artefato que o produziu (genótipo), em chave estável/código (não prosa), e a edição é dirigida à interseção de falhas (ou ao par falha×sucesso), não à falha isolada. Falha preservada com hash antes/depois é evidência, não linha a descartar.

## Evidência

- **Recorrência (5 papers)** — 2607.28048 t2 (contraste falha×sucesso), 2608.07645 t1-4 (interseção de falhas; sobreposição deliberada de tarefas; genótipo; chave estável), 2608.22510 t4 (falha como evidência preservada), 2608.23041 t4 (trace de falha navegável; histograma por error_type não gera patch), 2608.27454 t2 (memória de fracasso como arquivo consultável).

## Mapa de aplicação

### scripts
- ressalvas: falhas de pipeline registradas sem versão do artefato que as produziu.
### sisyphus-runtime
- ressalvas: constraints/princípios com drifts sem genótipo.
### agent-skills
- ressalvas: failures.jsonl sem versão do SKILL.md que falhou.
### papers-journal
- ressalvas: falha de render sem hash do template que a causou.
### llm-council
- ressalvas + não agora (2608.15242): incidentes registrados, sem chave de genótipo.

## Valor de negócio

Sem genótipo, a mesma falha é re-diagnosticada a cada ocorrência e a correção é cega (não sabe o que mudou desde a última vez que funcionou). Com memória de fracasso consultável, a intervenção falhada não se repete — e a interseção de falhas localiza a causa em vez de amostrar sintomas.
