# papers.hf

Jornal diário sobre os [Daily Papers](https://huggingface.co/papers) do Hugging
Face. Um cron gera a edição do próprio dia às 22:00 (BRT) e, às 07:00 do dia
seguinte, reconcilia a janela dos três dias anteriores: busca o que a API
ainda mudou, tria contra um perfil de interesse declarado e reescreve a
edição em markdown e em HTML somente quando a mudança é material.

O que o distingue de um agregador: ele **julga**. Um dia sem nada relevante
produz uma edição que diz isso, em vez de encher espaço com resumos.

## Como funciona

```
API do Hugging Face  ──▶  triagem por LLM  ──▶  edicoes/*.md   (leitura local)
  ~30 papers/dia          contra interests.md      docs/*.html   (site)
                                  │
                                  └──▶  .cache/*.json  (re-render sem custo)
```

Uma execução consome cerca de 8k tokens de entrada e 2,5k de saída.

## Rotina em duas passadas

| Passada | Horário (BRT) | O que faz |
|---|---|---|
| Geração | 22:00 | Edição do dia corrente, com snapshot de IDs+upvotes no front-matter |
| Reconciliação | 07:00 | Varre D-1..D-3 e regenera só o que mudou materialmente |

Por que duas passadas: às 22:00 a lista do dia já está essencialmente
completa, o leitor lê no próprio dia (e não na manhã seguinte) e os upvotes
jovens — o público do HF vota no horário comercial das Américas do Norte e
Europa — já refletem a primeira leva de votos. A reconciliação das 07:00
recupera o que a curadoria tardia do HF adiciona 1-2 dias depois e os upvotes
que engatilharam de madrugada.

O front-matter de cada edição carrega o snapshot `papers:` com um
`  - <id> <upvotes>` por paper. É contra esse snapshot que a segunda passada
compara a API.

**Gatilhos de regeneração, e só eles:** (a) o conjunto de IDs mudou (entrou OU
saiu paper); (b) algum paper teve delta absoluto >= 5 upvotes **desde a última
versão publicada** — cada regeneração atualiza o snapshot, o delta nunca é
acumulado desde a edição original. Upvotes < 5 e comentários não disparam
nada. A regeneração é inteira, nunca emenda: o LLM reavalia os destaques com
o catálogo completo.

**Backfill como rede de segurança:** dia da janela com papers na API e sem
edição (a geração das 22:00 falhou) é gerado pela reconciliação, logado como
backfill. **Silêncio no dia comum:** sem mudança material, a passada das 07:00
não escreve, não publica e não notifica — "Nada mudado na janela." Resposta
vazia da API para dia com edição existente é WARN no log e nenhuma ação: uma
edição nunca é apagada nem regenerada por causa de resposta vazia.

## Estrutura

| Caminho | Papel |
|---|---|
| `src/journal.py` | Busca, triagem e escrita da edição do dia |
| `src/render_html.py` | Renderiza o HTML, no estilo de portal de notícias |
| `src/index.py` | Gera `docs/index.html`, a capa do arquivo |
| `src/deepdive.py` | Leitura profunda de um paper, sob demanda |
| `src/deep_html.py` | Publica os deep dives do papers-deep em HTML e reconcilia a seção nas edições |
| `src/paths.py` | Único lugar que conhece o layout de diretórios |
| `bin/papers-daily.sh` | Wrapper de cron: lock, log, notificação, fail-loud |
| `interests.md` | Perfil que decide o que é relevante. **Edite este arquivo.** |
| `edicoes/AAAA/MM/` | Edições em markdown |
| `edicoes/deep/AAAA/MM/` | Deep dives do pipeline papers-deep, agrupados por edição |
| `edicoes/repos-registry.md` | Catálogo dos repos confrontados pelo papers-deep; cada entrada carrega `last-verified` e `verified-head` |
| `docs/` | Site publicável: `index.html` mais as edições em HTML |
| `docs/deep/AAAA/MM/` | Deep dives publicados, derivados das notas em `edicoes/deep/` |
| `deep/` | Leituras profundas por paper, escritas por `src/deepdive.py` |
| `.cache/AAAA/MM/` | Veredito do modelo (ignorado pelo git) |

A seção `## Deep dives` de uma edição não nasce do `journal.py`: o pipeline
papers-deep anexa-a ao markdown depois do render. Quando a rotina regenera
uma edição, essa cauda é extraída do `.md` antigo e reanexada ao novo — a
seção não se perde. No site, cada deep dive vira uma página self-contained em
`docs/deep/AAAA/MM/` e a edição ganha a mesma seção no fim, com links para
elas. Ambos saem de `python3 src/deep_html.py`, que lê as notas como fonte
única e é idempotente: pode ser re-rodado a qualquer momento para regenerar
ou reconciliar.

## Uso

```bash
bin/papers-daily.sh                 # reconciliação da janela D-1..D-3 (cron 07:00)
bin/papers-daily.sh 2026-08-24      # geração de uma data (cron 22:00 e manual)
python3 src/journal.py --dry-run    # imprime sem gravar nada
python3 src/journal.py --date 2026-08-24 --render-only   # re-render sem chamar o LLM
python3 src/journal.py --reconcile --dry-run   # o que a reconciliação faria, sem gravar
python3 src/deepdive.py 2608.16425  # leitura profunda de um paper
python3 src/deep_html.py            # publica deep dives em HTML e reconcilia as edições
python3 src/index.py                # regenera só o índice
```

`--render-only` lê o veredito já em cache, o que permite mexer no template sem
pagar nenhuma chamada de modelo. Ele reescreve o markdown da edição inteira a
partir do cache; a cauda `## Deep dives` anexada depois do render é
preservada automaticamente, e `python3 src/deep_html.py` reconcilia a seção
no HTML.

## Configuração

Só a chave da OpenAI é obrigatória. O script a procura em `OPENAI_API_KEY` e,
não a encontrando, lê `~/.local/share/opencode/auth.json`.

| Variável | Default | Para quê |
|---|---|---|
| `PAPERS_HOME` | raiz do projeto | Onde o código vive |
| `PAPERS_DATA_DIR` | `PAPERS_HOME` | Onde as edições são escritas |
| `PAPERS_NTFY_TOPIC` | vazio (não notifica) | Notificação de conclusão e de falha |
| `OPENAI_API_KEY` | `auth.json` do opencode | Chamada de triagem |

O wrapper carrega um `.env` na raiz, se existir. Um tópico ntfy é protegido
apenas por ser difícil de adivinhar, então ele mora ali e fica fora do git:

```bash
echo 'PAPERS_NTFY_TOPIC=https://ntfy.sh/seu-topico-aleatorio' > .env
chmod 600 .env
```

Sem essa variável o jornal é gerado normalmente, apenas sem notificação.

Separar `PAPERS_DATA_DIR` de `PAPERS_HOME` permite manter o código público e as
edições em outro lugar.

## Cron

```cron
0 22 * * * bash ~/papers-journal/bin/papers-daily.sh "$(date +\%F)"
0 7 * * * bash ~/papers-journal/bin/papers-daily.sh
```

A passada da noite gera a edição do dia corrente (o `%` escapado é obrigatório
no crontab); a da manhã, sem argumento, reconcilia a janela D-1..D-3. São nove
horas entre as duas, e o `flock` do wrapper segue como segurança contra
sobreposição.

## Falhas

O silêncio é ambíguo por natureza: nenhuma edição pode significar "nada
relevante" ou "quebrou". Por isso o script falha alto e o veredito distingue os
casos por código de saída.

| Código | Significado |
|---|---|
| 0 | Edição escrita ou janela reconciliada, com ou sem mudanças |
| 1 | Configuração: chave ausente, `interests.md` sumiu |
| 2 | Rede ou API; na reconciliação, ao menos um dia da janela falhou (os demais foram processados) |
| 3 | Sanidade: feed vazio, schema mudou, resposta degenerada do modelo |
| 4 | Sem publicação no dia ou janela inteira vazia (fim de semana) |

Os códigos 1-3 disparam notificação de prioridade alta. O 4 não é falha e não
notifica. Na reconciliação, o ntfy também só toca quando houve regeneração ou
backfill, com o resumo dos dias afetados; dia sem mudança é silêncio total. A
asserção de sanidade existe para o caso em que a API responde 200 com lista
vazia, que de outro modo passaria por "dia tranquilo" indefinidamente.

## Dependências

Nenhuma. Python 3.10+ da biblioteca padrão, `curl` e `flock`.

## Publicar como site

`docs/` já é uma raiz servível. Para publicar no GitHub Pages, aponte Pages para
a pasta `docs/` do branch principal e faça o cron commitar após gerar a edição.
