#!/usr/bin/env python3
"""Leitura profunda de um paper especifico, sob demanda.

Busca o texto completo no arXiv (versao HTML, sem dependencia de parser de PDF),
le contra o perfil de interesse e escreve a analise em papers/deep/.

Quando o HTML nao existe — papers antigos ou submissoes so em PDF — cai para o
abstract e diz isso no cabecalho, em vez de fingir leitura completa.

Uso:
  python3 deepdive.py 2608.21156
  python3 deepdive.py 2608.21156 --dry-run
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from journal import Fatal, http_json, load_api_key, log  # noqa: E402

OPENAI_API = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-5.5"
MAX_CHARS = 160_000


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.chunks: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip and data.strip():
            self.chunks.append(data.strip())

    def text(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", "\n".join(self.chunks))


def fetch_fulltext(paper_id: str) -> tuple[str, bool]:
    for url in (f"https://arxiv.org/html/{paper_id}v2",
                f"https://arxiv.org/html/{paper_id}v1",
                f"https://arxiv.org/html/{paper_id}"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "papers-deepdive/1.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                if resp.status != 200:
                    continue
                html = resp.read().decode("utf-8", "replace")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            continue
        parser = TextExtractor()
        parser.feed(html)
        text = parser.text()
        if len(text) > 4000:
            log("INFO", f"texto completo obtido de {url} ({len(text)} chars)")
            return text[:MAX_CHARS], True
    return "", False


def fetch_meta(paper_id: str) -> dict[str, Any]:
    data = http_json(f"https://huggingface.co/api/papers/{paper_id}", timeout=60)
    if not isinstance(data, dict) or not data.get("title"):
        raise Fatal(3, f"metadados vazios para {paper_id}")
    return data


def call_llm(messages: list[dict[str, str]], model: str, key: str) -> str:
    payload = json.dumps({"model": model, "messages": messages}).encode("utf-8")
    raw = http_json(OPENAI_API, data=payload,
                    headers={"Content-Type": "application/json",
                             "Authorization": f"Bearer {key}"},
                    timeout=900)
    try:
        content = raw["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise Fatal(2, f"resposta sem content: {json.dumps(raw)[:300]}") from exc
    if not content.strip():
        raise Fatal(3, "modelo devolveu analise vazia")
    usage = raw.get("usage") or {}
    log("INFO", f"tokens: in={usage.get('prompt_tokens')} out={usage.get('completion_tokens')}")
    return content


def main() -> int:
    ap = argparse.ArgumentParser(description="Leitura profunda de um paper")
    ap.add_argument("paper_id", help="id do arXiv, ex: 2608.21156")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    paper_id = args.paper_id.strip().strip("[]")
    if not paths.INTERESTS.is_file():
        raise Fatal(1, f"perfil de interesse ausente: {paths.INTERESTS}")
    interests = paths.INTERESTS.read_text(encoding="utf-8")

    log("INFO", f"buscando metadados de {paper_id}")
    meta = fetch_meta(paper_id)
    title = meta.get("title", "").strip()

    body, full = fetch_fulltext(paper_id)
    if not full:
        log("WARN", "texto completo indisponivel no arXiv HTML; usando abstract")
        body = meta.get("summary", "")

    key = load_api_key()
    system = ("Voce le papers de IA para um engenheiro que opera sistemas de agentes "
              "em producao. Ele quer saber o que da para usar, o que nao presta e "
              "onde estao as armadilhas. Seja concreto e honesto: se o paper nao "
              "sustenta as proprias afirmacoes, diga.")
    user = f"""# Perfil do leitor

{interests}

# Paper: {title}

{"Texto completo abaixo." if full else "ATENCAO: apenas o abstract esta disponivel. Seja explicito sobre o que nao da para afirmar sem o texto completo."}

{body}

# Sua tarefa

Escreva uma analise em markdown, em portugues do Brasil, com estas secoes:

## O que o paper afirma
A tese central e o mecanismo, em prosa. Sem "os autores propoem".

## Como sustentam
Quais experimentos, baselines e metricas. Onde a evidencia e forte e onde e fraca.
Se a avaliacao for so em benchmark sintetico, diga.

## O que da para aproveitar
Concreto: qual ideia, tecnica ou regra o leitor pode transplantar para o sistema
dele, e como. Se nao houver nada, diga isso sem rodeio.

## Armadilhas
Premissas escondidas, custo de implementacao, o que quebra fora do setup do paper.

## Veredito
Duas ou tres frases: vale investir tempo nisso agora, deixar no radar, ou ignorar."""

    log("INFO", f"analisando com {args.model}")
    analysis = call_llm([{"role": "system", "content": system},
                         {"role": "user", "content": user}], args.model, key)

    header = "\n".join([
        "---",
        f"paper: {paper_id}",
        "tipo: deepdive",
        f"fonte: {'texto completo' if full else 'apenas abstract'}",
        f"lido_em: {dt.date.today().isoformat()}",
        "tags: [papers, deepdive]",
        "---",
        "",
        f"# {title}",
        "",
        f"[HF](https://huggingface.co/papers/{paper_id}) · "
        f"[arXiv](https://arxiv.org/abs/{paper_id}) · "
        f"{'texto completo' if full else 'ATENÇÃO: análise baseada apenas no abstract'}",
        "",
    ])
    content = header + analysis.strip() + "\n"

    if args.dry_run:
        print(content)
        return 0

    dest = paths.ensure_parent(paths.deepdive(paper_id))
    dest.write_text(content, encoding="utf-8")
    log("INFO", f"analise escrita: {dest}")
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
