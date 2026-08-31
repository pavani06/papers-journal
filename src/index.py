#!/usr/bin/env python3
"""Gera docs/index.html: a capa do arquivo, agrupando as edicoes por mes.

Le o disco, nao um banco de estado: a lista de edicoes e sempre o que existe em
docs/. Isso mantem o indice correto mesmo depois de apagar ou repopular edicoes
a mao.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from render_html import MONTHS, _CSS  # noqa: E402

_E = html.escape

_CSS_INDEX = """
.mes{font-size:20px;font-weight:700;color:#2F3134;margin:24px 0 4px}
.edicao{display:block;padding:14px 0;border-top:1px solid #F0F0F0;text-decoration:none}
.edicao .dia{font-size:13px;color:#757575;margin-bottom:3px}
.edicao .chamada-titulo{font-size:17px;line-height:22px;font-weight:700;color:#C4170C}
.edicao .n{font-size:13px;color:#757575;margin-top:4px}
.vazio{padding:24px 0;color:#757575}
"""


def _manchete_e_destaques(html_path: Path) -> tuple[str, int]:
    """Extrai manchete e contagem de destaques do html ja gerado."""
    try:
        texto = html_path.read_text(encoding="utf-8")
    except OSError:
        return "", 0
    m = re.search(r'<h1 class="manchete">(.*?)</h1>', texto, re.S)
    manchete = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
    return manchete, texto.count('class="destaque"')


def _cache_manchete(date: str) -> tuple[str, int]:
    c = paths.cache(date)
    if not c.is_file():
        return "", 0
    try:
        v = json.loads(c.read_text(encoding="utf-8"))["verdict"]
        return str(v.get("manchete", "")), len(v.get("destaques") or [])
    except (json.JSONDecodeError, KeyError, OSError):
        return "", 0


def construir_indice() -> str:
    edicoes = paths.edicoes_publicadas()

    corpo: list[str] = []
    mes_atual = ""
    for date, html_path in edicoes:
        manchete, n = _manchete_e_destaques(html_path)
        if not manchete:
            manchete, n = _cache_manchete(date)
        ano, mes, dia = date.split("-")
        rotulo = f"{MONTHS[int(mes) - 1].capitalize()} de {ano}"
        if rotulo != mes_atual:
            mes_atual = rotulo
            corpo.append(f'<h2 class="mes">{_E(rotulo)}</h2>')
        rel = f"{ano}/{mes}/{date}.html"
        plural = "destaques" if n != 1 else "destaque"
        corpo.append(
            f'<a class="edicao" href="{rel}">'
            f'<div class="dia">{dia}/{mes}</div>'
            f'<div class="chamada-titulo">{_E(manchete or "Edição sem manchete")}</div>'
            f'<div class="n">{n} {plural}</div></a>'
        )

    if not corpo:
        corpo.append('<p class="vazio">Nenhuma edição publicada ainda.</p>')

    return (
        '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>papers.hf — arquivo</title>\n"
        f"<style>{_CSS}{_CSS_INDEX}</style>\n</head>\n<body>\n"
        '<div class="topo-fixo"><header class="topo">'
        '<a class="logo" href="index.html">papers.hf</a>'
        f'<span class="data-topo">{len(edicoes)} edições</span></header></div>\n'
        f'<div class="wrap">{"".join(corpo)}</div>\n'
        '<div class="faixa"></div><footer class="wrap rodape">'
        'Jornal diário sobre <a href="https://huggingface.co/papers">Daily Papers</a>.'
        "</footer>\n</body>\n</html>\n"
    )


def escrever_indice() -> Path:
    destino = paths.ensure_parent(paths.INDEX)
    paths.escrever(destino, construir_indice())
    return destino


if __name__ == "__main__":
    print(escrever_indice())
