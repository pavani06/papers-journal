---
id: principio-0015
title: "Protocolo de controle é contrato verificável — narrativa não governa a execução"
status: adotado
camada: a
sinais:
  - "recorrência: 4 papers independentes (2608.28281, 2608.31076, 2609.00621, 2609.03153)"
  - "transversalidade: 4 repos (agent-workloops, papers-journal, agent-skills, scripts)"
evidencias:
  - arxiv: 2608.28281
    data: 2026-08-31
    sinal: recorrência
    citacao: "agent-workloops/templates/diretiva.md:3-11"
  - arxiv: 2608.31076
    data: 2026-09-01
    sinal: recorrência
    citacao: "agent-skills/skills/issue-start/SKILL.md:220-267"
  - arxiv: 2609.00621
    data: 2026-09-02
    sinal: recorrência
    citacao: "scripts/dispatch/preflight.sh:5-11,41-69"
  - arxiv: 2609.03153
    data: 2026-09-04
    sinal: recorrência
    citacao: "papers-journal/src/deepdive.py:159-196; agent-workloops/playbooks/workloop.md:61-81,102-112"
contra_evidencias:
  - "2608.24777: pre-check em toda tool call é sobredefesa; o contrato é proporcional ao risco."
criado_em: 2026-09-06
revalidado_em: null
adotado_em: 2026-09-06
---

# Protocolo de controle é contrato verificável — narrativa não governa a execução

## Formulação

Antes de uma ação com efeito, o sistema declara num artefato preservado o
objetivo, escopo, ações permitidas, critérios de sucesso, evidência exigida,
aprovações e estados de falha ou retry. Conteúdo de terceiro e prosa de
orientação transitam no canal de dados: não ampliam o contrato. Campo ausente,
default e falha têm semântica explícita e auditável; prompt é orientação, não
protocolo.

## Evidência

- **2608.28281**: Loop Contract anterior à ação. A diretiva atual já é contrato
  de issue persistido antes de código e seção vazia denuncia escopo não pensado
  (agent-workloops/templates/diretiva.md:3-11).
- **2608.31076**: o execution brief atual fixa objetivo, critérios, escopo,
  regras, fontes pinadas e validação antes da implementação
  (agent-skills/skills/issue-start/SKILL.md:220-267).
- **2609.00621**: controle tipado exige slots e falha explícita. O preflight
  atual declara exit codes, efeitos e gramática antes de executar, mas segue
  contrato textual (scripts/dispatch/preflight.sh:5-11,41-69).
- **2609.03153**: obrigação, evidência e estado por claim. O deepdive pede
  cinco seções narrativas (papers-journal/src/deepdive.py:159-196); o workloop
  tem critérios, blockers, pré-voo e gate humano, mas não matriz única
  obrigação → evidência → estado
  (agent-workloops/playbooks/workloop.md:61-81,102-112).

## Mapa de aplicação

### agent-workloops

- o que mudaria: diretiva de trabalho verificável ganha matriz curta critério
  → evidência → estado (supported, contradicted, unknown).
- veredito original: aplicar agora como convenção leve.
- esforço estimado: baixo.

### papers-journal

- o que mudaria: deep dives operacionais usam schema versionado para claim,
  evidência e abstenção antes do modelo.
- veredito original: aplicar com ressalvas; sem validador runtime, seria prosa.
- esforço estimado: médio.

### agent-skills

- o que mudaria: brief preserva estados de requisito ausente, falha estrutural
  e aprovação necessária.
- veredito original: aplicar com ressalvas; nem toda skill possui runtime.
- esforço estimado: baixo a médio.

### scripts

- o que mudaria: onde o risco justificar, preflight evolui para contrato com
  semântica de falha e retry verificável.
- veredito original: aplicar com ressalvas; o parser atual é aproximado.
- esforço estimado: médio.
