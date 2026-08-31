---
id: principio-0011
title: "Uma execução não é medida — pass^k, variância e nulos honestos"
status: candidato
camada: a
sinais:
  - "recorrencia: 6 papers independentes (2607.28609, 2608.13417, 2608.17271, 2608.19741, 2608.20438, 2608.22510)"
  - "transversalidade: 4 repos (llm-council, agent-skills, papers-journal, agent-workloops)"
evidencias:
  - arxiv: 2608.13417
    data: 2026-08-11
    sinal: recorrencia
    citacao: "tese 2 — exigir k execucoes e reportar avg@k e best@k; a distancia entre os dois e a confiabilidade"
  - arxiv: 2608.17271
    data: 2026-08-14
    sinal: recorrencia
    citacao: "tese 6 — queda de 2,48 com desvio ±2,35 e ruido publicado como 'sharp decline'"
  - arxiv: 2608.19741
    data: 2026-08-16
    sinal: recorrencia
    citacao: "teses 1,4,5 — pass@1 65,36% vs pass^20 25,25%; registrar quantas execucoes sustentam um passes:true"
  - arxiv: 2608.20438
    data: 2026-08-17
    sinal: recorrencia
    citacao: "teses 2-3 — nulo com IC largo e inconclusivo; N instancias do mesmo modelo e uma fonte so"
contra_evidencias: []
criado_em: 2026-08-30
revalidado_em: null
adotado_em: null
---

# Uma execução não é medida

## Formulação

Execução única mede descoberta, não confiabilidade: onde a decisão importa, k execuções isoladas com `avg@k`/`best@k` reportados juntos. Diferença menor que a variância entre runs não é achado; nulo com IC largo é "inconclusivo", não "neutro"; N realizações do mesmo prompt não são N fontes independentes.

## Evidência

- **Recorrência (6 papers)** — 2607.28609 t4 (estabilidade do juiz antes de comprar mais juízes; resample muda 6-9% dos vereditos), 2608.13417 t2, 2608.17271 t6 (ruído publicado como achado), 2608.19741 t1/4/5 (pass@1 vs pass^20; registrar N execuções), 2608.20438 t2-3 (nulo com IC largo; N realizações = 1 fonte), 2608.22510 t2 (score exploratório vs. pass estrito).

## Mapa de aplicação

### llm-council
- ressalvas: smoke de repetição; métrica de convergência entre rodadas.
### agent-skills
- ressalvas: harness roda cada gate 1×; `retry_count: 0` mentiroso.
### papers-journal
- agora (2608.19741) / ressalvas (medição antes de mudar janela em 2608.20438).
### agent-workloops
- veredito não extraído (2608.17271).

## Valor de negócio

Decisões baseadas em execução única (gate de skill que passou 1×, "melhoria" de um run) convertem ruído em política. Registrar k execuções e a distância avg/best é o mínimo que torna a decisão defensável — e custa só a coluna no relatório.
