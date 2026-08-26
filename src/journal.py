#!/usr/bin/env python3
"""Gera o jornal diario de papers do Hugging Face.

Fluxo: busca o feed do dia na API publica do HF, pede ao LLM a triagem e a
prosa dos destaques, e renderiza o markdown final. A listagem completa e
montada pelo proprio script, nao pelo modelo, para que nenhum paper suma por
esquecimento.

Exit codes:
  0  jornal escrito
  1  erro de configuracao ou uso
  2  falha de rede / API
  3  assercao de sanidade falhou (feed vazio, resposta degenerada)

Uso:
  python3 journal.py                      # dia anterior
  python3 journal.py --date 2026-08-24
  python3 journal.py --date 2026-08-24 --dry-run
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from index import escrever_indice  # noqa: E402
from render_html import render_html  # noqa: E402

HF_API = "https://huggingface.co/api/daily_papers"
OPENAI_API = "https://api.openai.com/v1/chat/completions"
AUTH_JSON = Path.home() / ".local/share/opencode/auth.json"
DEFAULT_MODEL = "gpt-5.5"

# Folga sobre os 160 chars que o render usa como fallback; o resto triplicaria o cache.
CACHE_ABSTRACT_CHARS = 200

MEMORIA_EDICOES = 10

# Nao e erro: o Hugging Face nao publica em fins de semana e feriados.
SEM_PUBLICACAO = 4


class Fatal(Exception):
    """Erro que deve derrubar o processo com codigo especifico."""

    def __init__(self, code: int, msg: str) -> None:
        super().__init__(msg)
        self.code = code


def log(level: str, msg: str) -> None:
    print(f"[{dt.datetime.now().isoformat(timespec='seconds')}] [{level}] {msg}",
          file=sys.stderr)


def load_api_key() -> str:
    """Le a key do auth.json do opencode; env var tem precedencia."""
    env = os.environ.get("OPENAI_API_KEY")
    if env:
        return env
    if not AUTH_JSON.is_file():
        raise Fatal(1, f"sem OPENAI_API_KEY no ambiente e {AUTH_JSON} nao existe")
    try:
        data = json.loads(AUTH_JSON.read_text(encoding="utf-8"))
        key = data["openai"]["key"]
    except (json.JSONDecodeError, KeyError) as exc:
        raise Fatal(1, f"nao consegui extrair openai.key de {AUTH_JSON}: {exc}") from exc
    if not key:
        raise Fatal(1, "openai.key vazia no auth.json")
    return key


def http_json(url: str, *, data: bytes | None = None,
              headers: dict[str, str] | None = None, timeout: int = 180) -> Any:
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:400]
        raise Fatal(2, f"HTTP {exc.code} em {url}: {body}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise Fatal(2, f"falha de rede em {url}: {exc}") from exc


def fetch_papers(date: str) -> tuple[list[dict[str, Any]], int]:
    """Retorna (papers utilizaveis, quantidade bruta devolvida pela API).

    A contagem bruta separa dois casos que a lista vazia confunde: fim de semana
    sem publicacao (bruto zero, normal) e mudanca de schema (bruto positivo, mas
    nada aproveitavel).
    """
    raw = http_json(f"{HF_API}?date={date}&limit=100", timeout=60)
    if not isinstance(raw, list):
        raise Fatal(3, f"resposta inesperada da API do HF: {type(raw).__name__}")

    papers = []
    for item in raw:
        p = item.get("paper") or {}
        pid = p.get("id")
        if not pid:
            continue
        papers.append({
            "id": pid,
            "title": (p.get("title") or "").strip(),
            "abstract": (p.get("summary") or "").strip(),
            "one_liner": (p.get("ai_summary") or "").strip(),
            "keywords": p.get("ai_keywords") or [],
            "upvotes": p.get("upvotes") or 0,
            "authors": [a.get("name", "") for a in (p.get("authors") or [])],
            "comments": item.get("numComments") or 0,
            "thumbnail": item.get("thumbnail") or "",
        })
    papers.sort(key=lambda x: -x["upvotes"])
    return papers, len(raw)


def bloco_memoria(date: str) -> str:
    anteriores = paths.vereditos_anteriores(date, MEMORIA_EDICOES)
    if not anteriores:
        return ("Nenhuma edicao anterior disponivel. Trate tudo como novo e nao "
                "invente relacoes com o passado.")
    linhas = []
    for data, v in anteriores:
        teses = [f"  - {d.get('tese') or d.get('aproveitavel', '')[:110]}"
                 for d in v.get("destaques") or []]
        if teses:
            linhas.append(f"{data}:\n" + "\n".join(teses))
    return "\n".join(linhas) if linhas else "Edicoes anteriores sem teses registradas."


def build_prompt(papers: list[dict[str, Any]], interests: str, date: str) -> list[dict[str, str]]:
    catalogo = "\n\n".join(
        f"[{p['id']}] {p['title']}\n"
        f"upvotes: {p['upvotes']} | keywords: {', '.join(p['keywords'][:8])}\n"
        f"{p['abstract'][:1400]}"
        for p in papers
    )
    memoria = bloco_memoria(date)

    system = (
        "Voce e o editor de um jornal diario de pesquisa em IA, escrito para um "
        "unico leitor. Seu trabalho e triar o que saiu hoje e escrever com "
        "honestidade sobre o que importa para ele. Voce nao e um resumidor: voce "
        "julga. Dizer que o dia foi fraco e uma resposta valida e util."
    )

    user = f"""# Perfil do leitor

{interests}

# O que ja foi coberto nas edicoes recentes

Use isto para dar continuidade, nao para evitar assuntos. Tema recorrente e
normal e esperado; o que nao se repete e a mesma tese.

{memoria}

# Papers publicados em {date} ({len(papers)} no total)

{catalogo}

# Sua tarefa

Responda com um unico objeto JSON, sem markdown ao redor, com estas chaves:

- "manchete": string. Uma frase que captura o tema dominante do dia. Se nao
  houver tema dominante, diga isso. Nao invente coesao onde nao ha.

- "abertura": string. Um ou dois paragrafos em prosa sobre o dia como um todo:
  o que predominou, o que chamou atencao, o que estava ausente. Escreva para
  quem vai ler isso no cafe da manha, nao para um comite. Nada de bullets.

- "destaques": array de objetos, cada um com:
    - "id": o id exato do paper, entre colchetes no catalogo acima
    - "tese": UMA frase de 10 a 15 palavras com a afirmacao central do paper.
      Esta frase alimenta a memoria das proximas edicoes, entao precisa ser
      autossuficiente: quem a ler daqui a duas semanas, sem o paper na frente,
      tem que entender o que foi afirmado.
    - "analise": 2 a 4 frases. Qual a afirmacao central e o que ha de novo em
      relacao ao que ja se fazia. Sem "os autores propoem".
    - "aproveitavel": 1 a 2 frases sobre o que o leitor pode tirar disso para o
      sistema dele. Se nao houver nada aproveitavel, escreva exatamente
      "Nada diretamente aproveitavel." e nao force uma ponte.
    - "relacao": objeto com a relacao deste paper com as edicoes recentes:
        - "tipo": "novo", "avanca" ou "contradiz"
        - "ref_data": a data da edicao citada (AAAA-MM-DD), ou "" se tipo=novo
        - "ref_tese": a tese citada, copiada da memoria, ou "" se tipo=novo
        - "delta": o que exatamente este paper muda em relacao a tese citada.
          Uma frase concreta comecando por um verbo: "estende para...",
          "quantifica...", "mostra que o inverso vale quando...". Vazio se
          tipo=novo.
      "avanca" e "contradiz" so valem quando a tese citada e a MESMA afirmacao,
      nao um tema vizinho, e quando existe delta articulavel. Se voce nao
      conseguir escrever o delta em uma frase concreta, o tipo e "novo" — dois
      papers sobre coordenacao de agentes nao se relacionam so por serem sobre
      coordenacao. Na duvida entre "novo" e "avanca", escolha "novo".

- "repetidos": array de objetos para papers que voce descartaria do destaque por
  repetirem tese ja coberta, cada um com "id", "ref_data" e "ref_tese". Eles vao
  para o rodape com a citacao visivel. So liste aqui quando conseguir citar a
  tese anterior especifica; na duvida, trate como destaque normal. Um paper com
  muitos upvotes que apenas repete tese conhecida entra aqui, nao no destaque.

  Inclua entre 0 e 6 destaques, aplicando as regras da secao "Como escolher os
  destaques" do perfil: acionabilidade decide, piso de popularizacao admite,
  benchmark vale pelo modo de falha que revela, e teses repetidas no mesmo dia
  rendem um destaque so. Um paper que contradiz tese ja coberta merece destaque
  mesmo sem acionabilidade, e tem prioridade na disputa pelas vagas. Dia fraco
  tem zero ou um destaque, e tudo bem. Nunca preencha por preencher.

- "tangenciais": array de ids dos papers que valem uma linha de atencao sem
  merecer destaque, conforme a secao "Tangencial" do perfil. Pode ser vazio.

- "resumos": objeto mapeando o id de CADA UM dos {len(papers)} papers do catalogo
  para uma frase em portugues que diga o que o paper faz. Uma frase, direta,
  sem "este trabalho". Inclua todos, inclusive os que estao fora de escopo.

Todo o texto em portugues do Brasil, seguindo o tom descrito no perfil. Use
apenas ids que aparecem no catalogo."""

    return [{"role": "system", "content": system},
            {"role": "user", "content": user}]


def call_llm(messages: list[dict[str, str]], model: str, key: str) -> dict[str, Any]:
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")

    raw = http_json(
        OPENAI_API,
        data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {key}"},
        timeout=600,
    )

    try:
        content = raw["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise Fatal(2, f"resposta da API sem content: {json.dumps(raw)[:300]}") from exc

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise Fatal(3, f"modelo devolveu JSON invalido: {content[:300]}") from exc

    for field in ("manchete", "abertura", "destaques"):
        if field not in parsed:
            raise Fatal(3, f"JSON do modelo sem o campo '{field}'")
    if not str(parsed.get("abertura", "")).strip():
        raise Fatal(3, "abertura vazia: resposta degenerada")

    usage = raw.get("usage") or {}
    log("INFO", f"tokens: in={usage.get('prompt_tokens')} out={usage.get('completion_tokens')}")
    return parsed


def resolve_id(raw: Any, by_id: dict[str, dict[str, Any]]) -> str | None:
    """Casa o id do modelo com o catalogo tolerando colchetes, espacos e prefixo arXiv."""
    if not isinstance(raw, str):
        return None
    cand = raw.strip().strip("[]").replace("arXiv:", "").replace("arxiv:", "").strip()
    if cand in by_id:
        return cand
    for known in by_id:
        if known in cand or cand in known:
            return known
    return None


def normalize_verdict(verdict: dict[str, Any],
                      papers: list[dict[str, Any]]) -> dict[str, Any]:
    """Resolve os ids do modelo contra o catalogo, uma vez, para todos os renderers."""
    by_id = {p["id"]: p for p in papers}

    destaques = []
    orfaos = []
    for d in verdict.get("destaques") or []:
        match = resolve_id(d.get("id"), by_id)
        if match:
            destaques.append({**d, "id": match})
        else:
            orfaos.append(d.get("id"))

    # Destaque que nao casa com o catalogo e desalinhamento, nao "dia fraco".
    # Renderizar zero destaques aqui produziria um jornal silenciosamente falso.
    if orfaos and not destaques:
        raise Fatal(3, f"nenhum dos {len(orfaos)} destaques casou com o catalogo "
                       f"(ids do modelo: {orfaos[:5]})")
    if orfaos:
        log("WARN", f"{len(orfaos)} destaque(s) descartado(s) por id desconhecido: {orfaos}")

    dest_ids = {d["id"] for d in destaques}

    repetidos = []
    for r in verdict.get("repetidos") or []:
        match = resolve_id(r.get("id"), by_id)
        if not match or match in dest_ids:
            continue
        if not (r.get("ref_data") and r.get("ref_tese")):
            log("WARN", f"repetido {match} sem citacao completa; tratado como tangencial")
        repetidos.append({**r, "id": match})
    rep_ids = {r["id"] for r in repetidos}

    tang_ids = []
    for i in verdict.get("tangenciais") or []:
        match = resolve_id(i, by_id)
        if match and match not in dest_ids and match not in rep_ids and match not in tang_ids:
            tang_ids.append(match)

    resumos = {}
    for raw_id, texto in (verdict.get("resumos") or {}).items():
        match = resolve_id(raw_id, by_id)
        if match and isinstance(texto, str) and texto.strip():
            resumos[match] = texto.strip()
    faltando = len(papers) - len(resumos)
    if faltando:
        log("WARN", f"{faltando} paper(s) sem resumo em portugues; usando o do HF (ingles)")

    return {**verdict, "destaques": destaques, "repetidos": repetidos,
            "tangenciais": tang_ids, "resumos": resumos}


def chapeu_md(dest: dict[str, Any]) -> list[str]:
    rel = dest.get("relacao") or {}
    tipo, ref = rel.get("tipo"), rel.get("ref_data")
    if tipo not in ("avanca", "contradiz") or not ref:
        return []
    rotulo = "Contradiz" if tipo == "contradiz" else "Avança"
    ano, mes, dia = ref.split("-")
    detalhe = rel.get("delta") or rel.get("ref_tese", "")
    return [f"**{rotulo} [{dia}/{mes}](../../{ano}/{mes}/{ref}.md)** — {detalhe}", ""]


def render(date: str, papers: list[dict[str, Any]], verdict: dict[str, Any]) -> str:
    by_id = {p["id"]: p for p in papers}
    destaques = verdict["destaques"]
    dest_ids = {d["id"] for d in destaques}
    tang_ids = verdict["tangenciais"]
    repetidos = verdict.get("repetidos") or []
    rep_ids = {r["id"] for r in repetidos}
    resumos = verdict["resumos"]
    resto = [p for p in papers if p["id"] not in dest_ids
             and p["id"] not in tang_ids and p["id"] not in rep_ids]

    def linha(p: dict[str, Any], nota: str = "") -> str:
        autores = ", ".join(p["authors"][:2])
        if len(p["authors"]) > 2:
            autores += f" +{len(p['authors']) - 2}"
        desc = resumos.get(p["id"]) or p["one_liner"] or p["abstract"][:160]
        extra = f"  \n  *{nota}*" if nota else ""
        return (f"- **[{p['title']}](https://huggingface.co/papers/{p['id']})** "
                f"({p['upvotes']} upvotes){f' — {autores}' if autores else ''}  \n"
                f"  {desc}{extra}")

    out = [
        "---",
        f"date: {date}",
        "tipo: jornal-papers",
        f"papers: {len(papers)}",
        f"destaques: {len(destaques)}",
        "tags: [papers, hugging-face, daily]",
        "---",
        "",
        f"# Papers de {date}",
        "",
        f"## {verdict['manchete']}",
        "",
        str(verdict["abertura"]).strip(),
        "",
    ]

    if destaques:
        out += ["## Destaques", ""]
        for d in destaques:
            p = by_id[d["id"]]
            autores = ", ".join(p["authors"][:3])
            if len(p["authors"]) > 3:
                autores += f" e mais {len(p['authors']) - 3}"
            out += [
                *chapeu_md(d),
                f"### [{p['title']}](https://huggingface.co/papers/{p['id']})",
                "",
                f"`{p['id']}` · {p['upvotes']} upvotes · {p['comments']} comentários"
                + (f" · {autores}" if autores else ""),
                "",
                str(d.get("analise", "")).strip(),
                "",
                f"**Para o nosso caso:** {str(d.get('aproveitavel', '')).strip()}",
                "",
                f"[abstract](https://arxiv.org/abs/{p['id']}) · "
                f"aprofundar: `python3 src/deepdive.py {p['id']}`",
                "",
            ]
    else:
        out += ["## Destaques", "",
                "Nenhum paper de hoje passou o critério de relevância direta.", ""]

    if repetidos:
        out += ["## Já coberto", ""]
        for r in repetidos:
            nota = (f"Ecoa a tese de {r['ref_data']}: {r['ref_tese']}"
                    if r.get("ref_data") and r.get("ref_tese") else "Repete tese já coberta")
            out += [linha(by_id[r["id"]], nota)]
        out += [""]

    if tang_ids:
        out += ["## Tangenciais", ""]
        out += [linha(by_id[i]) for i in tang_ids]
        out += [""]

    if resto:
        out += [f"## Também publicado ({len(resto)})", ""]
        out += [linha(p) for p in resto]
        out += [""]

    out += ["---", "",
            f"Fonte: [Daily Papers](https://huggingface.co/papers/date/{date}) · "
            f"{len(papers)} papers processados"]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Jornal diario de papers do Hugging Face")
    ap.add_argument("--date", help="YYYY-MM-DD (padrao: ontem)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true", help="imprime sem gravar")
    ap.add_argument("--render-only", action="store_true",
                    help="re-renderiza a partir do .verdict.json, sem chamar o LLM")
    args = ap.parse_args()

    date = args.date or (dt.date.today() - dt.timedelta(days=1)).isoformat()
    try:
        dt.date.fromisoformat(date)
    except ValueError:
        raise Fatal(1, f"data invalida: {date}")

    if not paths.INTERESTS.is_file():
        raise Fatal(1, f"perfil de interesse ausente: {paths.INTERESTS}")
    interests = paths.INTERESTS.read_text(encoding="utf-8")

    cache = paths.cache(date)

    if args.render_only:
        if not cache.is_file():
            raise Fatal(1, f"--render-only exige {cache}, que nao existe")
        snapshot = json.loads(cache.read_text(encoding="utf-8"))
        papers, verdict = snapshot["papers"], snapshot["verdict"]
        log("INFO", f"re-render a partir do cache: {len(papers)} papers, "
                    f"{len(verdict['destaques'])} destaques")
    else:
        log("INFO", f"buscando papers de {date}")
        papers, brutos = fetch_papers(date)
        log("INFO", f"{len(papers)} papers recebidos ({brutos} brutos)")
        if brutos == 0:
            raise Fatal(SEM_PUBLICACAO, f"nenhum paper publicado em {date} "
                                        "(tipicamente fim de semana)")
        if not papers:
            raise Fatal(3, f"API devolveu {brutos} itens mas nenhum utilizavel em {date}: "
                           "schema provavelmente mudou")

        key = load_api_key()
        log("INFO", f"gerando jornal com {args.model}")
        verdict = normalize_verdict(call_llm(build_prompt(papers, interests, date),
                                             args.model, key), papers)
        log("INFO", f"{len(verdict['destaques'])} destaques, "
                    f"{len(verdict['tangenciais'])} tangenciais")

    markdown = render(date, papers, verdict)

    if args.dry_run:
        print(markdown)
        return 0

    dest = paths.ensure_parent(paths.edicao_md(date))
    dest.write_text(markdown, encoding="utf-8")
    log("INFO", f"jornal escrito: {dest}")

    dest_html = paths.ensure_parent(paths.edicao_html(date))
    dest_html.write_text(render_html(date, papers, verdict), encoding="utf-8")
    log("INFO", f"edicao html escrita: {dest_html}")

    escrever_indice()
    log("INFO", f"indice atualizado: {paths.INDEX}")

    if not args.render_only:
        enxuto = [{**p, "abstract": (p.get("abstract") or "")[:CACHE_ABSTRACT_CHARS]}
                  for p in papers]
        paths.ensure_parent(cache).write_text(
            json.dumps({"papers": enxuto, "verdict": verdict}, ensure_ascii=False),
            encoding="utf-8")

    print(dest)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as err:
        log("ERROR", str(err))
        sys.exit(err.code)
    except KeyboardInterrupt:
        sys.exit(130)
