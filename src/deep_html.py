#!/usr/bin/env python3
"""Publish papers-deep notes as static HTML pages and link them from the editions.

The note in edicoes/deep/YYYY/MM/<arxiv-id>.md is the single source of truth; the
page under docs/deep/ is pure derivation. For every edition with at least one note,
a "Deep dives" section (and its nav anchor) is reconciled into the edition page in
docs/. Idempotent: rerunning converges to the same bytes, and stale derivations
(pages, sections, anchors) of removed notes are dropped.

Usage: python3 src/deep_html.py
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from render_html import _CSS, _data_por_extenso  # noqa: E402

_E = html.escape

MARCA = "<!-- deep-dives -->"
_NAV_ANCORA = '<a class="c-vermelho" href="#deep-dives">Deep dives</a>'
_RODAPE_FAIXA = '<div class="faixa"></div><footer class="wrap rodape">'
_EDICAO_WIKILINK = re.compile(
    r"\[\[papers/(\d{4})/(\d{2})/(\d{4}-\d{2}-\d{2})(?:\|([^\]]+))?\]\]"
)
_DEEP_WIKILINK = re.compile(
    r"\[\[papers/deep/(\d{4})/(\d{2})/(\d{4}\.\d+)(?:\|([^\]]+))?\]\]"
)
_WIKILINK = re.compile(r"\[\[[^\]]+\]\]")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
_CODE = re.compile(r"`([^`]+)`")
_DATA = re.compile(r"\d{4}-\d{2}-\d{2}")
_ITEM = re.compile(r"^(?:\d+\.|-) ")
_SUMARIO = re.compile(r"\*\*Sumário de ação\*\*:\s*(.+?)(?=\n\n|\Z)", re.DOTALL)

Bloco = tuple[str, "str | list[str] | tuple[bool, list[str]]"]

_ARTIGO_CSS = """
.artigo p{font-size:17px;line-height:27px;margin:14px 0 0}
.artigo h2{font-size:22px;line-height:27px;font-weight:700;color:var(--cor,#C4170C);margin:28px 0 2px;padding-top:14px;border-top:1px solid #F0F0F0}
.artigo h3{font-size:18px;line-height:23px;font-weight:700;margin:20px 0 2px}
.artigo ul,.artigo ol{margin:12px 0 0 22px}
.artigo li{font-size:16px;line-height:24px;margin:8px 0}
.artigo code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px;background:#F5F5F5;border-radius:3px;padding:1px 5px}
.fonte{background:#F5F5F5;border-left:4px solid #0669DE;border-radius:0 8px 8px 0;padding:12px 14px;margin:16px 0 0}
.fonte b{display:block;font-size:13px;font-weight:700;color:#0669DE;margin-bottom:4px}
.fonte p{font-size:14px;line-height:21px;margin:0}
.crumb{font-size:13px;margin:18px 0 0}
.crumb a{color:#0669DE;text-decoration:none}
"""


# ---------------------------------------------------------------- frontmatter

def _escalar(valor: str) -> str:
    """Tira as aspas externas e desfaz o escape de aspas dentro delas.

    Sem isto, `title: "When \\"Must\\" ..."` chega ao <title>, ao <h1> e ao
    card com as barras literais.
    """
    valor = valor.strip()
    if len(valor) >= 2 and valor[0] == valor[-1] == '"':
        valor = valor[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return valor


def _parse_frontmatter(texto: str) -> tuple[dict, str]:
    """Split and parse the simple YAML frontmatter used by the pipeline notes."""
    if not texto.startswith("---\n"):
        return {}, texto
    fim = texto.find("\n---", 3)
    if fim < 0:
        raise ValueError("frontmatter sem fechamento")
    meta: dict = {}
    chave: str | None = None
    for linha in texto[4:fim].split("\n"):
        if linha.startswith("  - "):
            if chave is None:
                raise ValueError(f"item de lista sem chave: {linha!r}")
            meta[chave].append(_escalar(linha[4:]))
        elif linha.startswith((" ", "\t")):
            raise ValueError(f"linha de frontmatter nao suportada: {linha!r}")
        else:
            chave, sep, valor = linha.partition(":")
            if not sep:
                raise ValueError(f"linha de frontmatter sem ':': {linha!r}")
            chave = chave.strip()
            valor = valor.strip()
            if valor.startswith("[") and valor.endswith("]"):
                itens = valor[1:-1].strip()
                meta[chave] = [v.strip() for v in itens.split(",")] if itens else []
                chave = None
            elif valor == "":
                meta[chave] = []
            else:
                meta[chave] = _escalar(valor)
    return meta, texto[fim + 4:].lstrip("\n")


# --------------------------------------------------------------------- inline

_ESQUEMA = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")
_ESQUEMA_OK = ("http://", "https://", "mailto:")


def _href_ok(url: str) -> bool:
    """So vira <a> o que e http(s), mailto ou caminho sem esquema. As notas sao
    escritas por modelo a partir de texto de terceiro: esquema arbitrario nao
    deve virar href vivo na pagina publicada."""
    u = html.unescape(url).strip().lower()
    return u.startswith(_ESQUEMA_OK) or not _ESQUEMA.match(u)


def _inline(texto: str, prefixo: str = "../../../") -> str:
    """Markdown inline (subset das notas) -> HTML. Preserva code spans.

    `prefixo` e o caminho relativo ate `docs/` a partir da pagina que recebe o
    HTML: `../../../` de uma pagina deep, `../../` de uma pagina de edicao.
    """
    codigos: list[str] = []

    def _guarda(m: re.Match) -> str:
        codigos.append(m.group(1))
        return f"\x00{len(codigos) - 1}\x00"

    texto = _CODE.sub(_guarda, texto)
    texto = _E(texto, quote=False)
    texto = _LINK.sub(
        lambda m: (f'<a href="{_E(html.unescape(m.group(2)), quote=True)}">'
                   f"{m.group(1)}</a>")
        if _href_ok(m.group(2)) else m.group(1),
        texto,
    )
    texto = _EDICAO_WIKILINK.sub(
        lambda m: (f'<a href="{prefixo}{m.group(1)}/{m.group(2)}/{m.group(3)}.html">'
                   f"{_E(m.group(4) or m.group(3))}</a>"),
        texto,
    )
    texto = _DEEP_WIKILINK.sub(
        lambda m: (f'<a href="{prefixo}deep/{m.group(1)}/{m.group(2)}/{m.group(3)}.html">'
                   f"{_E(m.group(4) or m.group(3))}</a>"),
        texto,
    )
    texto = _WIKILINK.sub(lambda m: _E(m.group(0).strip("[]").split("|")[-1]), texto)
    texto = _BOLD.sub(r"<strong>\1</strong>", texto)
    texto = _ITALIC.sub(r"<em>\1</em>", texto)
    texto = re.sub(
        r"\x00(\d+)\x00",
        lambda m: f"<code>{_E(codigos[int(m.group(1))])}</code>",
        texto,
    )
    return texto


# --------------------------------------------------------------------- blocos

def _blocos(corpo: str) -> list[Bloco]:
    """Group the note body into typed blocks."""
    saida: list[Bloco] = []
    linhas = corpo.split("\n")
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        if not linha.strip():
            i += 1
        elif linha.startswith("# "):
            i += 1  # h1 da nota: o titulo vem do frontmatter
        elif linha.startswith("## "):
            saida.append(("h2", linha[3:].strip()))
            i += 1
        elif linha.startswith("### "):
            saida.append(("h3", linha[4:].strip()))
            i += 1
        elif linha.startswith(">"):
            bloco: list[str] = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(linhas[i].lstrip("> ").strip())
                i += 1
            saida.append(("callout", bloco))
        elif _ITEM.match(linha):
            ordenado = linha[0].isdigit()
            itens: list[str] = []
            while True:
                while i < len(linhas) and (m := _ITEM.match(linhas[i])):
                    if linhas[i][0].isdigit() != ordenado:
                        break
                    itens.append(linhas[i][m.end():].strip())
                    i += 1
                    while i < len(linhas) and linhas[i].startswith((" ", "\t")):
                        itens[-1] += " " + linhas[i].strip()
                        i += 1
                # itens separados por linha em branco continuam a mesma lista
                j = i
                while j < len(linhas) and not linhas[j].strip():
                    j += 1
                if (j < len(linhas) and _ITEM.match(linhas[j])
                        and linhas[j][0].isdigit() == ordenado):
                    i = j
                else:
                    break
            saida.append(("lista", (ordenado, itens)))
        else:
            paragrafo = [linha.strip()]
            i += 1
            while i < len(linhas) and linhas[i].strip() and not re.match(
                r"^(#{2,3} |>|\d+\. |- )", linhas[i]
            ):
                paragrafo.append(linhas[i].strip())
                i += 1
            saida.append(("p", " ".join(paragrafo)))
    return saida


def _render_corpo(blocos: list[Bloco]) -> str:
    partes: list[str] = []
    for tipo, conteudo in blocos:
        if tipo in ("h2", "h3") and isinstance(conteudo, str):
            partes.append(f"<{tipo}>{_inline(conteudo)}</{tipo}>")
        elif tipo == "callout" and isinstance(conteudo, list):
            rotulo = "Nota"
            if conteudo and (m := re.match(r"^\[!([^\]]+)\]\s*(.*)", conteudo[0])):
                rotulo = m.group(2).strip() or m.group(1).capitalize()
                conteudo = conteudo[1:]
            corpo = _inline(" ".join(l for l in conteudo if l))
            partes.append(
                f'<div class="fonte"><b>{_E(rotulo)}</b><p>{corpo}</p></div>'
            )
        elif tipo == "lista" and isinstance(conteudo, tuple):
            ordenado, itens = conteudo
            tag = "ol" if ordenado else "ul"
            vis = "".join(f"<li>{_inline(i)}</li>" for i in itens)
            partes.append(f"<{tag}>{vis}</{tag}>")
        elif isinstance(conteudo, str):
            partes.append(f"<p>{_inline(conteudo)}</p>")
    return "\n".join(partes)


# -------------------------------------------------------------------- paginas

def _pagina_deep(meta: dict, corpo: str, date: str, edicao_rel: str) -> str:
    titulo = str(meta.get("title") or meta.get("arxiv") or date)
    return (
        '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>papers.hf — {_E(titulo)}</title>\n"
        f"<style>{_CSS}{_ARTIGO_CSS}</style>\n</head>\n<body>\n"
        '<div class="topo-fixo"><header class="topo">'
        f'<a class="logo" href="{edicao_rel}">papers.hf</a>'
        f'<span class="data-topo">Deep dive · {_E(_data_por_extenso(date))}'
        "</span></header></div>\n"
        '<div class="wrap sec-vermelho artigo">\n'
        f'<p class="crumb"><a href="{edicao_rel}">&larr; Edição de {_E(date)}</a></p>\n'
        f'<h1 class="manchete">{_E(titulo)}</h1>\n'
        f"{corpo}\n</div>\n"
        f"{_RODAPE_FAIXA}Deep dive do pipeline papers-deep · "
        f'<a href="{edicao_rel}">edição de {_E(date)}</a></footer>\n'
        "</body>\n</html>\n"
    )


def _secao_edicao(refs: list[tuple[str, str, str]], date: str) -> str:
    itens = "".join(
        f'<article class="card"><a class="titulo" '
        f'href="../../deep/{date[:4]}/{date[5:7]}/{_E(paper_id)}.html">{_E(titulo)}</a>'
        f'<div class="chamada"><p>{_inline(sumario, "../../")}</p></div>'
        f"</article>"
        for paper_id, titulo, sumario in refs
    )
    return (
        f'{MARCA}<div class="faixa"></div><div class="wrap sec-vermelho">'
        f'<section id="deep-dives"><h2 class="kicker c-vermelho">Deep dives</h2>'
        f"{itens}</section></div>"
    )


def _reconcilia_edicao(texto: str, secao: str | None) -> str:
    """Swap the marked block for `secao` (or drop it) and keep the nav anchor true."""
    if MARCA in texto:
        inicio = texto.index(MARCA)
        fim = texto.index(_RODAPE_FAIXA, inicio)
        texto = texto[:inicio] + texto[fim:]
    if secao is None:
        return texto.replace(_NAV_ANCORA, "")
    fim = texto.index(_RODAPE_FAIXA)
    texto = texto[:fim] + secao + texto[fim:]
    if _NAV_ANCORA not in texto:
        texto = texto.replace("</nav>", _NAV_ANCORA + "</nav>", 1)
    return texto


# ------------------------------------------------------------------------ main

def main() -> int:
    notas = paths.deep_notas()
    por_edicao: dict[str, list[tuple[str, str, str]]] = {}
    for nota in notas:
        meta, corpo = _parse_frontmatter(nota.read_text(encoding="utf-8"))
        date = str(meta.get("date") or "")
        if not _DATA.fullmatch(date):
            raise SystemExit(f"{nota}: frontmatter 'date' ausente ou invalido")
        paper_id = str(meta.get("arxiv") or nota.stem)
        titulo = str(meta.get("title") or paper_id)
        sumario = _SUMARIO.search(corpo)
        chamada = (
            sumario.group(1).strip().replace("\n", " ")
            if sumario
            else "Deep dive do pipeline papers-deep: destilação do paper "
            "com confronto contra o estado atual dos nossos repos."
        )
        edicao_rel = f"../../../{date[:4]}/{date[5:7]}/{date}.html"
        pagina = _pagina_deep(meta, _render_corpo(_blocos(corpo)), date, edicao_rel)
        destino = paths.escrever(paths.deep_html(paper_id, date), pagina)
        por_edicao.setdefault(date, []).append((paper_id, titulo, chamada))

    for date, refs in sorted(por_edicao.items()):
        edicao = paths.edicao_html(date)
        if not edicao.is_file():
            print(f"aviso: edicao {edicao} inexistente; secao nao injetada",
                  file=sys.stderr)
            continue
        paths.escrever(
            edicao,
            _reconcilia_edicao(edicao.read_text(encoding="utf-8"),
                               _secao_edicao(sorted(refs), date)))

    for _, edicao in paths.edicoes_publicadas():
        texto = edicao.read_text(encoding="utf-8")
        if MARCA in texto and edicao.stem not in por_edicao:
            paths.escrever(edicao, _reconcilia_edicao(texto, None))

    if paths.DOCS_DEEP.is_dir():
        fontes = {
            str(n.relative_to(paths.DEEP_EDICOES).with_suffix(".md")) for n in notas
        }
        for pagina in sorted(paths.DOCS_DEEP.glob("*/*/*.html")):
            derivada = pagina.relative_to(paths.DOCS_DEEP).with_suffix(".md")
            if str(derivada) not in fontes:
                pagina.unlink()
                print(f"removida pagina sem nota de origem: {pagina}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
