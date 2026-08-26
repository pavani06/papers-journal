# papers.hf

Jornal diário sobre os [Daily Papers](https://huggingface.co/papers) do Hugging
Face. Todo dia de manhã, um cron busca o que foi publicado, tria contra um
perfil de interesse declarado e escreve uma edição em markdown e em HTML.

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

## Estrutura

| Caminho | Papel |
|---|---|
| `src/journal.py` | Busca, triagem e escrita da edição do dia |
| `src/render_html.py` | Renderiza o HTML, no estilo de portal de notícias |
| `src/index.py` | Gera `docs/index.html`, a capa do arquivo |
| `src/deepdive.py` | Leitura profunda de um paper, sob demanda |
| `src/paths.py` | Único lugar que conhece o layout de diretórios |
| `bin/papers-daily.sh` | Wrapper de cron: lock, log, notificação, fail-loud |
| `interests.md` | Perfil que decide o que é relevante. **Edite este arquivo.** |
| `edicoes/AAAA/MM/` | Edições em markdown |
| `docs/` | Site publicável: `index.html` mais as edições em HTML |
| `deep/` | Leituras profundas, uma por paper |
| `.cache/AAAA/MM/` | Veredito do modelo (ignorado pelo git) |

## Uso

```bash
bin/papers-daily.sh                 # edição de ontem (o que o cron roda)
bin/papers-daily.sh 2026-08-24      # uma data específica
python3 src/journal.py --dry-run    # imprime sem gravar nada
python3 src/journal.py --date 2026-08-24 --render-only   # re-render sem chamar o LLM
python3 src/deepdive.py 2608.16425  # leitura profunda de um paper
python3 src/index.py                # regenera só o índice
```

`--render-only` lê o veredito já em cache, o que permite mexer no template sem
pagar nenhuma chamada de modelo.

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
0 7 * * * bash ~/papers-journal/bin/papers-daily.sh
```

Roda antes do expediente e processa o dia anterior, já fechado.

## Falhas

O silêncio é ambíguo por natureza: nenhuma edição pode significar "nada
relevante" ou "quebrou". Por isso o script falha alto e o veredito distingue os
casos por código de saída.

| Código | Significado |
|---|---|
| 0 | Edição escrita |
| 1 | Configuração: chave ausente, `interests.md` sumiu |
| 2 | Rede ou API |
| 3 | Sanidade: feed vazio, schema mudou, resposta degenerada do modelo |

Qualquer código diferente de zero dispara notificação de prioridade alta. A
asserção de sanidade existe para o caso em que a API responde 200 com lista
vazia, que de outro modo passaria por "dia tranquilo" indefinidamente.

## Dependências

Nenhuma. Python 3.10+ da biblioteca padrão, `curl` e `flock`.

## Publicar como site

`docs/` já é uma raiz servível. Para publicar no GitHub Pages, aponte Pages para
a pasta `docs/` do branch principal e faça o cron commitar após gerar a edição.
