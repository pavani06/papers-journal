---
id: papers.principios.glossario-causas
title: "Papers — Glossário de Causas"
type: catalogo-principios
date: 2026-08-30
status: active
tags:
  - papers
  - principios
relates-to:
  - "[[papers/repos-registry]]"
---

# Glossário de Causas

Vocabulário fechado do padrão de segunda ordem (camada d) do papers-synth:
quando um veredito de confronto é "aplicar com ressalvas" ou "não aplicar", a
causa é nomeada em uma sentença canônica. Uma causa com 2+ ocorrências de
papers independentes contra repos diferentes vira padrão candidato. Causa
nova abre entrada; vocabulário inflando é sinal de calibração pelo operador.

Origem: primeira re-síntese total (2026-08-30), 100 notas — 21 causas nomeadas
(15 padrão, 6 nascentes). Nota de extração: o log da camada d terminou no meio
da C21; a próxima re-síntese re-valida o glossário.

## Causas padrão (2+ papers independentes, 2+ repos)

| Causa | Ocorrências | Notas (exemplos) |
|---|---|---|
| Portão sem caso de referência re-executável é teatro | 5 | 2607.28048→scripts/sisyphus-runtime/agent-skills; 2608.09819→agent-skills; 2608.07545→agent-skills |
| Sem execução real acumulada que alimente o mecanismo | 8 | 2608.16590→agent-skills; 2608.18852→agent-skills; 2608.19880→koda/agent-skills; 2608.23041; 2608.25593→agent-workloops; 2608.23200 |
| A tese já está implementada; confronto é confirmação, não correção | 23 | llm-council/koda/agent-workloops/ciot em 2606.00152, 2608.04574, 2608.05013, 2608.05784, 2608.06301, 2608.08160, 2608.08722, 2608.12307, 2608.12440, 2608.12571, 2608.12781, 2608.13558, 2608.15089, 2608.15242, 2608.19861, 2608.21500, 2608.23740, 2608.24358, 2608.24569, 2608.24979, 2608.26070, 2608.26530, 2608.27454 |
| Sem chamador de produção / caminho morto | 4 | 2608.03451→agent-skills; 2608.16425→scripts; 2608.07169/10692/11079/12307→papers-journal |
| Custo da sonda excede o ganho | 6 | 2608.06270→papers-journal; 2608.16425→scripts; 2608.19880/19741/18565→llm-council; 2608.19880→agent-skills; 2608.16391→papers-journal |
| Escala pequena demais para o método | 10 | 2608.05703, 2608.06301, 2608.11079, 2608.14036, 2608.18580, 2608.23670, 2608.25500, 2608.15242, 2608.27454, 2608.28609 |
| Regime do repo difere do regime em que o ganho foi medido | 11 | 2608.05102, 2608.05987, 2608.15008, 2608.16003, 2608.20202, 2608.20438, 2608.23740, 2608.24569, 2608.19861, 2608.06113, 2608.09867 |
| Depende de produtor externo / campo sem quem preencha | 11 | 2606.00152, 2608.05784, 2608.18852, 2608.15888, 2608.10692, 2608.21156, 2608.15008, 2608.11341, 2608.29211, 2608.23552, 2608.06352 |
| Implementação parcial é pior que nenhuma | 11 | 2608.05987, 2608.09867, 2608.12990, 2608.15008, 2608.17271, 2608.18565, 2608.18580, 2608.18852, 2608.08311, 2608.16590, 2608.00677 |
| Sem medição local prévia, aplicar é calibrar no escuro | 11 | 2608.12307, 2608.07645, 2608.29211, 2608.20202, 2608.05102, 2608.14036, 2608.11994, 2608.24189, 2608.06270, 2608.20438, 2608.16002 |
| A mudança exige decisão de política que é do operador | 17 | 2607.28609, 2608.12781, 2608.04569, 2608.09802, 2608.08311, 2608.10299, 2608.15242, 2608.16033, 2608.09867, 2608.19880, 2608.26005, 2608.25593, 2608.21156, 2608.26530, 2608.16391, 2608.12440, 2608.10875 |
| A mudança arrisca o ativo central do desenho | 15 | 2608.03836, 2608.04569, 2608.08389, 2608.08722, 2608.11924, 2608.16425, 2608.12781, 2608.19861, 2608.04574, 2608.23552, 2608.10875, 2608.10692, 2608.05013, 2608.23740, 2608.06867 |
| A aplicação exigiria redesenho, não emenda | 12 | 2608.16859, 2608.17310, 2608.18580, 2608.21156, 2608.13667, 2608.10450, 2608.23283, 2608.06301, 2608.06714, 2608.11341, 2608.15763, 2608.22510 |
| Ruído/falso positivo destrói o gate por desuso | 3 | 2608.05219→agent-skills; 2608.12571→llm-council; 2608.18565→papers-journal |
| A evidência do paper é fraca (nulo, N=1, correlacional) | 4 | 2608.20438→agent-skills; 2608.24569→agent-skills/llm-council; 2608.12440→agent-skills; 2608.24189→sisyphus-runtime |

## Causas nascentes (1 paper ou 1 repo — vocabulário, ainda não padrão)

| Causa | Ocorrências |
|---|---|
| Fonte de dados deliberadamente desligada | 2608.07645/13417/15242/23670 → agent-skills (1 repo) |
| Repo sem suíte de testes/CI: mudança no cron exige verificação manual | 2608.16002/17597/19799/21500/18580/23283/20634 → papers-journal (1 repo) |
| Mecanismo sob experimento selado; mudanças esperam o fechamento | 2608.07545/09802/23564/06352/06867/16859/19197/21500/22510/11994/19880 → llm-council (1 repo) |
| Auto-relato do agente não é evidência de gate | 2608.03744/16002 → agent-skills (1 repo) |
| Defesa em prompt não é gate | 2606.00152 → agent-skills/scripts (1 paper) |
| Selo/garantia sobre base não verificada dá garantia falsa | 2608.09819/15888 → papers-journal (extração interrompida) |
