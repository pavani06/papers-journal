---
tipo: perfil-de-interesse
consumido-por: scripts/papers/journal.py
atualizar: quando seu foco de trabalho mudar (esperado: 1-2x por ano)
---

# Perfil de interesse

Este arquivo diz ao gerador do jornal o que conta como relevante. Ele é lido
inteiro a cada execução e injetado no prompt de triagem. Edite livremente: o
formato é prosa, não há schema a respeitar.

## Quem lê o jornal

Engenheiro que constrói e opera sistemas de agentes de IA para trabalho de
software real. Não é pesquisador de ML: não treina modelos, não roda
experimentos de arquitetura neural, não publica papers. Consome pesquisa para
melhorar um sistema em produção que ele mesmo mantém.

O sistema em questão é um harness de agentes sobre modelos de terceiros, com
orquestração de subagentes, skills versionadas como artefatos de texto,
governança de dispatch e trilha de evidência. O trabalho diário é decidir como
agentes devem planejar, delegar, verificar e registrar o que fizeram.

## Diretamente aplicável

Estes temas mudam decisões de arquitetura do sistema dele. Um paper aqui merece
destaque mesmo com poucos upvotes.

- **Harness e loop engineering**: como estruturar o laço de execução de um
  agente, quando parar, como reagir a falha, self-improvement de harness.
- **Orquestração multi-agente**: delegação, decomposição de tarefa, coordenação
  entre agente primário e subagentes, roteamento, quando um agente deve chamar
  outro em vez de fazer.
- **Context engineering**: gestão de janela, compactação, o que manter e o que
  descartar, memória entre sessões, handoff de contexto, orçamento de tokens.
- **Planejamento por agentes**: transformar pedido vago em plano executável,
  granularidade de passo, quando perguntar em vez de assumir, gates de
  aprovação.
- **Verificação e confiabilidade**: como saber que um agente realmente fez o que
  disse, evidência versus asserção, avaliação de confiabilidade em execuções
  repetidas, detecção de falha silenciosa, reprodutibilidade de execução.
- **Prompt e skill engineering**: prompts como artefatos versionados,
  composição, sobreposição entre instruções, degradação com o tamanho.
- **Agentes de código**: benchmarks de engenharia de software real, uso de
  ferramentas, edição de repositório, execução de testes, worktrees.
- **Observabilidade de agentes**: telemetria, tracing de execução, análise de
  trajetória, custo por tarefa.

## Tangencial

Vale uma linha no rodapé, sem destaque, a menos que traga um resultado
surpreendente ou um método reaproveitável fora do domínio original.

- RAG e recuperação, quando o foco for confiabilidade ou contaminação de fonte
- Avaliação e benchmarks em geral, quando a metodologia for reaproveitável
- Eficiência de inferência (quantização, atenção, serving), pelo impacto
  indireto em custo e latência
- Modelos de mundo e agentes incorporados, quando a lição for sobre planejamento
  de longo horizonte e não sobre robótica

## Fora de escopo

Cita no rodapé em uma linha, sem análise. Não gaste espaço de destaque.

- Geração de imagem, vídeo, áudio e música
- Visão computacional aplicada (reconhecimento facial, detecção, segmentação)
- Domínios científicos específicos: biologia, astronomia, química, medicina
- Treinamento de modelos base, leis de escala, arquitetura neural nova
- Robótica e controle, salvo pela ressalva de planejamento acima
- Aplicações verticais sem método transferível: e-commerce, finanças, jurídico

## Tom do jornal

Português do Brasil. Prosa direta, sem entusiasmo de release. Termos técnicos em
inglês quando for o uso consagrado (harness, context window, benchmark). O leitor
é sênior: não explique o que é um LLM, não defina RAG, não abra parágrafo com
"neste trabalho os autores propõem".

O que ele quer de cada destaque: qual é a afirmação central, o que é novo em
relação ao que já se fazia, e se há algo diretamente aproveitável no sistema
dele. Quando não houver nada aproveitável, diga isso em vez de inventar uma
ponte forçada.
