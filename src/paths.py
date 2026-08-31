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
  edicoes/deep/YYYY/MM/*.md  deep dives do pipeline papers-deep, por edicao
  docs/YYYY/MM/*.html        jornal em html, raiz publicavel do site
  docs/deep/YYYY/MM/*.html   deep dives publicados, derivados das notas
  docs/index.html            indice das edicoes
  deep/*.md                  leituras profundas por paper
  .cache/YYYY/MM/*.json      veredito do modelo, para re-render sem custo
  papers.log                 log de execucao
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path

HOME = Path(os.environ.get("PAPERS_HOME") or Path(__file__).resolve().parent.parent)
DATA = Path(os.environ.get("PAPERS_DATA_DIR") or HOME)

INTERESTS = DATA / "interests.md"
LOG = DATA / "papers.log"
DOCS = DATA / "docs"
INDEX = DOCS / "index.html"
DEEP = DATA / "deep"
DEEP_EDICOES = DATA / "edicoes" / "deep"
DOCS_DEEP = DOCS / "deep"


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


def deep_html(paper_id: str, date: str) -> Path:
    """Pagina publicada do deep dive, derivada da nota, sob docs/deep/."""
    return DOCS_DEEP / date[:4] / date[5:7] / f"{paper_id}.html"


def deep_notas() -> list[Path]:
    """Lista todas as notas de deep dive do pipeline papers-deep."""
    if not DEEP_EDICOES.is_dir():
        return []
    return sorted(DEEP_EDICOES.glob("*/*/*.md"))


def escrever(path: Path, texto: str) -> Path:
    """Escreve `texto` em `path` atomicamente, criando o diretorio se preciso.

    Grava num temporario no MESMO diretorio e faz os.replace, que e atomico
    dentro do mesmo filesystem. Temporario no mesmo diretorio nao e detalhe:
    /tmp costuma ser outro filesystem, e ai o replace vira copia e perde a
    atomicidade justamente onde ela importa.

    O motivo nao e higiene. O guard de idempotencia do cron
    (bin/papers-daily.sh:84) e a verificacao pos-execucao (:107) testam
    EXISTENCIA do arquivo. Com escrita direta, uma interrupcao no meio deixa
    arquivo parcial e o guard marca o dia como feito. Com replace, o destino
    ou tem o conteudo anterior ou tem o novo inteiro — nunca um pedaco — e o
    guard passa a estar correto sem precisar mudar.
    """
    ensure_parent(path)
    tmp = path.with_name(f".{path.name}.tmp")
    try:
        tmp.write_text(texto, encoding="utf-8")
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return path


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def edicoes_publicadas() -> list[tuple[str, Path]]:
    """Lista (data, caminho html) de todas as edicoes, da mais recente para a mais antiga."""
    if not DOCS.is_dir():
        return []
    achadas = [(p.stem, p) for p in DOCS.glob("*/*/*.html") if p.name != "index.html"]
    return sorted(achadas, key=lambda x: x[0], reverse=True)


def digest_conteudo(conteudo: dict) -> str:
    """sha256 estavel (sort_keys) do conteudo serializado — para selar o cache.

    Determinismo importa: o digest e conferido na releitura (--render-only e
    memoria de edicoes), entao a serializacao tem que ser estavel entre
    execucoes, independente da ordem das chaves.
    """
    return hashlib.sha256(
        json.dumps(conteudo, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def vereditos_anteriores(date: str, limite: int) -> list[tuple[str, dict]]:
    """Le ate `limite` vereditos de edicoes anteriores a `date`, da mais recente para tras.

    Filtrar por data em vez de pegar os ultimos do disco importa ao regerar
    edicoes antigas: uma edicao de 12/08 nao pode enxergar a memoria de 25/08.
    """
    base = DATA / ".cache"
    if not base.is_dir():
        return []
    achados = []
    ilegiveis = 0
    for p in sorted(base.glob("*/*/*.json"), key=lambda x: x.stem, reverse=True):
        if p.stem >= date:
            continue
        try:
            dados = json.loads(p.read_text(encoding="utf-8"))
            digest = dados.get("digest")
            if digest:
                conferido = digest_conteudo(
                    {"papers": dados["papers"], "verdict": dados["verdict"]})
                if conferido != digest:
                    ilegiveis += 1
                    continue  # adulterado/corrompido: nao entra como memoria
            achados.append((p.stem, dados["verdict"]))
        except (json.JSONDecodeError, KeyError, OSError):
            ilegiveis += 1
            continue
        if len(achados) >= limite:
            break
    if ilegiveis:
        # Blind spot (molde NOT_FOUND do agent-skills): "nao havia" e "nao
        # consegui ler" sao estados diferentes — o segundo precisa aparecer.
        print(f"[{dt.datetime.now().isoformat(timespec='seconds')}] [WARN] "
              f"memoria: {len(achados)} lida(s), {ilegiveis} ilegiveis em {base}",
              file=sys.stderr)
    return achados
