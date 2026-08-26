#!/usr/bin/env python3
"""Resolucao de caminhos do projeto.

Todo path de escrita nasce aqui. Nenhum outro modulo conhece a estrutura de
diretorios, o que permite publicar o codigo sem carregar junto os caminhos
pessoais de quem o roda.

Variaveis de ambiente:
  PAPERS_HOME       raiz do projeto (default: o diretorio acima de src/)
  PAPERS_DATA_DIR   raiz dos dados  (default: PAPERS_HOME)

Layout sob PAPERS_DATA_DIR:
  interests.md               perfil de interesse, editado a mao
  edicoes/YYYY/MM/*.md       jornal em markdown
  docs/YYYY/MM/*.html        jornal em html, raiz publicavel do site
  docs/index.html            indice das edicoes
  deep/*.md                  leituras profundas por paper
  .cache/YYYY/MM/*.json      veredito do modelo, para re-render sem custo
  papers.log                 log de execucao
"""

from __future__ import annotations

import os
from pathlib import Path

HOME = Path(os.environ.get("PAPERS_HOME") or Path(__file__).resolve().parent.parent)
DATA = Path(os.environ.get("PAPERS_DATA_DIR") or HOME)

INTERESTS = DATA / "interests.md"
LOG = DATA / "papers.log"
DOCS = DATA / "docs"
INDEX = DOCS / "index.html"
DEEP = DATA / "deep"


def _particionado(base: Path, date: str, suffix: str) -> Path:
    ano, mes = date[:4], date[5:7]
    return base / ano / mes / f"{date}{suffix}"


def edicao_md(date: str) -> Path:
    return _particionado(DATA / "edicoes", date, ".md")


def edicao_html(date: str) -> Path:
    return _particionado(DOCS, date, ".html")


def cache(date: str) -> Path:
    return _particionado(DATA / ".cache", date, ".json")


def deepdive(paper_id: str) -> Path:
    return DEEP / f"{paper_id}.md"


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def edicoes_publicadas() -> list[tuple[str, Path]]:
    """Lista (data, caminho html) de todas as edicoes, da mais recente para a mais antiga."""
    if not DOCS.is_dir():
        return []
    achadas = [(p.stem, p) for p in DOCS.glob("*/*/*.html") if p.name != "index.html"]
    return sorted(achadas, key=lambda x: x[0], reverse=True)
