---
tipo: perfil-de-interesse
consumido-por: src/journal.py
atualizar: quando seu foco de trabalho mudar (esperado: 1-2x por ano)
---

# Perfil de interesse

Este arquivo é lido inteiro a cada execução e colado no prompt de triagem. Não
há schema nem parser: o que está escrito aqui é literalmente o que decide o
jornal do dia. Edite em prosa.

## Quem lê o jornal

Engenheiro que constrói e opera sistemas de agentes de IA para trabalho de
software real. Não é pesquisador de ML: não treina modelos, não roda
experimentos de arquitetura neural, não publica papers. Consome pesquisa para
melhorar um sistema em produção que ele mesmo mantém.

O sistema é um harness de agentes sobre modelos de terceiros, com orquestração
de subagentes, skills versionadas como artefatos de texto, governança de
dispatch e trilha de evidência. O trabalho diário é decidir como agentes devem
planejar, delegar, verificar e registrar o que fizeram.

**É ferramental de um operador só.** Ninguém mais dispara execuções. Por isso
não interessam multi-tenancy, isolamento entre usuários, quotas, SLA, custo por
tenant ou degradação sob carga: o gargalo é a atenção de uma pessoa, não
throughput.

## Como escolher os destaques

O critério é **acionabilidade**, não pertencimento temático. A lista de temas
abaixo define quem concorre; o que decide é se o paper muda alguma decisão de
arquitetura, de gate, de prompt ou de verificação. Um paper impecável sobre um
tema da lista que não muda nada é rodapé, não destaque.

Três regras que refinam isso:

**Piso de popularização.** Um paper de um dos temas com 50 ou mais upvotes entra
como destaque mesmo sem ação clara. Acima desse patamar, virar referência comum
da área já é motivo suficiente para você saber que existe.

**Benchmarks valem pelo que revelam.** Benchmark que expõe um modo de falha é
destaque, porque diz o que temer e o que testar no próprio sistema. Benchmark
que apenas ranqueia modelos é rodapé. A diferença entre "descobrimos que agentes
falham assim" e "o modelo X ficou à frente do Y".

**Sem eco.** Quando dois papers do mesmo dia sustentam essencialmente a mesma
tese, só o mais forte vira destaque; o outro desce para o rodapé com uma linha
dizendo que ecoa o primeiro. Não vale gastar duas leituras na mesma ideia.

## Continuidade entre edições

O jornal enxerga as teses das últimas dez edições. Isso existe para dar
continuidade, não para evitar assuntos: **tema recorrente é normal e esperado**.
Verificação de agentes aparece quase todo dia porque é o eixo principal do
leitor, e isso não é defeito. O que não se repete é a mesma afirmação.

Cada destaque declara sua relação com o já coberto:

- **novo**: nada equivalente nas edições recentes. É o caso comum.
- **avança**: aprofunda ou estende uma tese já coberta. Continua destaque, e a
  análise diz o que mudou em relação ao que se sabia. Exige um delta concreto,
  escrito em uma frase: o que este paper faz que a tese anterior não fazia. Dois
  papers sobre coordenação de agentes não se relacionam apenas por serem sobre
  coordenação — sem delta articulável, a relação é "novo".
- **contradiz**: o resultado conflita com uma tese já coberta. Isso é o mais
  valioso que o jornal pode entregar, porque pode invalidar algo que o leitor já
  incorporou ao sistema. Contradição merece destaque mesmo sem nada aproveitável
  e tem prioridade quando houver disputa por vaga.
- **repete**: mesma tese, sem avanço. Vai para o rodapé, na seção "Já coberto".

Rebaixar por repetição exige citar a tese anterior e a data. Sem citação
específica, o paper concorre normalmente: a dúvida favorece o destaque, porque
um falso positivo custa uma leitura a mais e um falso negativo custa um achado
perdido em silêncio.

Repetição vence o piso de popularização. Um paper muito votado que apenas repete
tese conhecida vai para "Já coberto" com os upvotes visíveis: você fica sabendo
que existe sem gastar um destaque com algo que já leu.

## Temas que concorrem a destaque

- **Harness e loop engineering**: como estruturar o laço de execução de um
  agente, quando parar, como reagir a falha, self-improvement de harness.
- **Orquestração multi-agente**: delegação, decomposição de tarefa, coordenação
  entre agente primário e subagentes, roteamento, quando um agente deve chamar
  outro em vez de fazer.
- **Context engineering**: gestão de janela, compactação, o que manter e o que
  descartar, handoff de contexto, orçamento de tokens, memória entre sessões,
  arquitetura de estado persistente e seleção de memória.
- **Planejamento por agentes**: transformar pedido vago em plano executável,
  granularidade de passo, quando perguntar em vez de assumir.
- **Governança e gates humanos**: aprovação antes de ações irreversíveis,
  autoridade do operador sobre canais de decisão, revisão humana em workflow
  automatizado, sycophancy e revisão adversarial, calibrar quando o humano
  precisa estar no laço.
- **Verificação e confiabilidade**: como saber que um agente realmente fez o que
  disse, evidência versus asserção, avaliação de confiabilidade em execuções
  repetidas, detecção de falha silenciosa, reprodutibilidade de execução,
  metodologia de eval: desenho de rubricas, tiers de avaliação, gates de eval e
  correlação entre eval e produção.
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
- Avaliação e benchmarks que ranqueiam sem revelar modo de falha
- Eficiência de inferência (quantização, atenção, serving): não muda nada em
  quem consome modelos por API, mas serve de radar sobre para onde vai o custo
  por token, que mais cedo ou mais tarde chega via preço
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

O jornal é público, mas escrito para um leitor específico. Fale com ele em
segunda pessoa e cite o sistema dele sem cerimônia. Um texto que tenta servir a
qualquer engenheiro acaba não servindo a ninguém; a especificidade é o que
produz frases como "a ressalva é que isso exige um espaço de resposta
sondável".

O que ele quer de cada destaque: qual é a afirmação central, o que é novo em
relação ao que já se fazia, e se há algo diretamente aproveitável no sistema
dele. Quando não houver nada aproveitável, diga isso em vez de inventar uma
ponte forçada.
