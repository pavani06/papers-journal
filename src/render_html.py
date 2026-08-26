"""Render the daily papers verdict as a self-contained globo.com-style HTML page."""
from __future__ import annotations

import datetime
import html

_E = html.escape

WEEKDAYS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
            "sexta-feira", "sábado", "domingo"]
MONTHS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
          "agosto", "setembro", "outubro", "novembro", "dezembro"]

_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:"Globotipo UI",Inter,-apple-system,BlinkMacSystemFont,"Avenir Next",Avenir,"Helvetica Neue",Helvetica,Ubuntu,Roboto,Noto,"Segoe UI",Arial,sans-serif;color:#2F3134;background:#fff}
a{color:inherit}
img{display:block;width:100%;height:100%;object-fit:cover}
.wrap{max-width:680px;margin:0 auto;padding:0 16px}
.faixa{height:6px;background:#F5F5F5}
.topo-fixo{position:sticky;top:0;z-index:20;background:#fff}
.topo{display:flex;align-items:center;justify-content:space-between;height:56px;padding:0 16px;border-bottom:1px solid #F0F0F0}
.logo{color:#0669DE;font-weight:700;font-size:24px;letter-spacing:-.5px;text-decoration:none}
.data-topo{font-size:12px;color:#757575}
.marcas{display:flex;gap:28px;align-items:center;height:44px;padding:0 16px;overflow-x:auto;white-space:nowrap;border-bottom:1px solid #F0F0F0;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.marcas::-webkit-scrollbar{display:none}
.marcas a{font-size:16px;font-weight:700;text-decoration:none}
.c-vermelho{color:#C4170C}.c-verde{color:#06AA48}.c-laranja{color:#FF6700}
.sec-vermelho{--cor:#C4170C}.sec-verde{--cor:#06AA48}.sec-laranja{--cor:#FF6700}
section{scroll-margin-top:112px}
.manchete{font-size:32px;line-height:38px;font-weight:700;color:#C4170C;letter-spacing:-.3px;overflow-wrap:break-word;margin:20px 0 18px}
.foto{background:#EDEDED;border-radius:10px;overflow:hidden}
.foto--lead{aspect-ratio:16/9;border-radius:11px;margin-bottom:4px}
.foto--card{width:132px;aspect-ratio:1/1;flex-shrink:0}
.abertura p,.analise p{font-size:16px;line-height:24px;margin:16px 0 0}
.kicker{font-size:24px;font-weight:700;margin:18px 0 2px}
.destaque{padding:16px 0 20px}
.linha{display:flex;gap:12px;align-items:flex-start}
.titulo{display:block;font-size:18px;line-height:22px;font-weight:700;text-decoration:none;overflow-wrap:break-word;color:var(--cor,#2F3134)}
.analise .titulo{margin-bottom:2px}
.pull{background:#F5F5F5;border-left:4px solid var(--cor);border-radius:0 8px 8px 0;padding:12px 14px;margin-top:14px}
.pull b{display:block;font-size:13px;font-weight:700;color:var(--cor);margin-bottom:4px}
.pull span{font-size:15px;line-height:22px}
.meta{font-size:13px;line-height:18px;color:#757575;margin-top:12px}
.card{padding:17px 0 19px}
.card + .card{border-top:1px solid #F0F0F0}
.card .titulo{margin-top:1px}
.chamada{display:flex;gap:10px;margin-top:16px}
.chamada::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--cor);flex-shrink:0;margin-top:7px}
.chamada p{font-size:16px;line-height:22px}
.sem-destaques{font-size:16px;line-height:24px;color:#757575;padding:8px 0 20px}
.chapeu{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;color:#fff;background:var(--cor);padding:3px 8px;border-radius:3px;text-decoration:none;margin-bottom:8px}
.chapeu-tese{font-size:13px;line-height:19px;color:#757575;margin:0 0 10px}
.eco{font-size:13px;line-height:19px;color:#757575;font-style:italic;margin-top:5px}
.rodape{padding:20px 0 36px;font-size:13px;line-height:20px;color:#757575}
.rodape a{color:#0669DE}
"""


def _data_por_extenso(iso: str) -> str:
    d = datetime.date.fromisoformat(iso)
    return f"{WEEKDAYS[d.weekday()]}, {d.day} de {MONTHS[d.month - 1]} de {d.year}"


def _autores(authors: list[str]) -> str:
    if not authors:
        return ""
    if len(authors) <= 3:
        return ", ".join(authors)
    return f"{', '.join(authors[:3])} e mais {len(authors) - 3}"


def _resumo(paper: dict, resumos: dict[str, str]) -> str:
    texto = resumos.get(paper["id"]) or paper.get("one_liner") or ""
    if not texto:
        abstract = paper.get("abstract") or ""
        if len(abstract) > 160:
            texto = abstract[:160].rsplit(" ", 1)[0].rstrip(",;:.") + "…"
        else:
            texto = abstract
    return texto


def _foto(url: str, extra: str = "") -> str:
    if url:
        src = html.escape(url, quote=True)
        return f'<div class="foto {extra}"><img src="{src}" alt="" loading="lazy"></div>'
    return f'<div class="foto {extra}"></div>'


def _meta(paper: dict) -> str:
    up = paper["upvotes"]
    com = paper["comments"]
    partes = [
        _E(paper["id"]),
        f"{up} upvote{'s' if up != 1 else ''}",
        f"{com} comentário{'s' if com != 1 else ''}",
    ]
    autores = _autores(paper["authors"])
    if autores:
        partes.append(_E(autores))
    return f'<p class="meta">{" · ".join(partes)}</p>'


def _chapeu(dest: dict) -> str:
    rel = dest.get("relacao") or {}
    tipo, ref = rel.get("tipo"), rel.get("ref_data")
    if tipo not in ("avanca", "contradiz") or not ref:
        return ""
    rotulo = "Contradiz" if tipo == "contradiz" else "Avança"
    ano, mes, dia = ref.split("-")
    detalhe = rel.get("delta") or rel.get("ref_tese") or ""
    return (f'<a class="chapeu" href="../../{ano}/{mes}/{ref}.html">{rotulo} {dia}/{mes}</a>'
            + (f'<p class="chapeu-tese">{_E(detalhe)}</p>' if detalhe else ""))


def _bloco_destaque(paper: dict, dest: dict) -> str:
    url = f"https://huggingface.co/papers/{paper['id']}"
    paragrafos = "".join(
        f"<p>{_E(p.strip())}</p>" for p in dest["analise"].split("\n\n") if p.strip()
    )
    return (
        '<article class="destaque">'
        f"{_chapeu(dest)}"
        f'<div class="linha">{_foto(paper.get("thumbnail") or "", "foto--card")}'
        f'<a class="titulo" href="{url}">{_E(paper["title"])}</a></div>'
        f'<div class="analise">{paragrafos}</div>'
        f'<div class="pull"><b>Para o nosso caso</b><span>{_E(dest["aproveitavel"])}</span></div>'
        f"{_meta(paper)}"
        "</article>"
    )


def _card(paper: dict, resumos: dict[str, str], eco: str = "") -> str:
    url = f"https://huggingface.co/papers/{paper['id']}"
    return (
        '<article class="card">'
        f'<div class="linha">{_foto(paper.get("thumbnail") or "", "foto--card")}'
        f'<a class="titulo" href="{url}">{_E(paper["title"])}</a></div>'
        f'<div class="chamada"><p>{_E(_resumo(paper, resumos))}'
        + (f'<span class="eco">{_E(eco)}</span>' if eco else "")
        + "</p></div></article>"
    )


def render_html(date: str, papers: list[dict], verdict: dict) -> str:
    """Render the daily journal as one offline, mobile-first HTML document."""
    by_id = {p["id"]: p for p in papers}
    destaques = [(by_id[d["id"]], d) for d in verdict.get("destaques", []) if d["id"] in by_id]
    usados = {d["id"] for d, _ in destaques}
    repetidos = [r for r in verdict.get("repetidos", []) if r.get("id") in by_id
                 and r["id"] not in usados]
    usados.update(r["id"] for r in repetidos)
    tang_ids = [i for i in verdict.get("tangenciais", []) if i in by_id and i not in usados]
    usados.update(tang_ids)
    restantes = [p for p in papers if p["id"] not in usados]
    resumos = verdict.get("resumos", {})

    nav = '<a class="c-vermelho" href="#destaques">Destaques</a>'
    partes: list[str] = []

    lead_foto = ""
    if destaques:
        lead_foto = _foto(destaques[0][0].get("thumbnail") or "", "foto--lead")
    if tang_ids:
        nav += '<a class="c-verde" href="#tangenciais">Tangenciais</a>'
    if restantes:
        nav += '<a class="c-laranja" href="#tambem">Também publicado</a>'

    abertura = "".join(
        f"<p>{_E(p.strip())}</p>" for p in verdict["abertura"].split("\n\n") if p.strip()
    )
    partes.append(
        f'<div class="wrap"><h1 class="manchete">{_E(verdict["manchete"])}</h1>'
        f"{lead_foto}<div class=\"abertura\">{abertura}</div></div><div class=\"faixa\"></div>"
    )

    corpo_d = (
        '<p class="sem-destaques">Nenhum destaque hoje: nenhum paper teve '
        "aderência forte o suficiente aos nossos interesses.</p>"
        if not destaques
        else "".join(_bloco_destaque(p, d) for p, d in destaques)
    )
    partes.append(
        f'<div class="wrap sec-vermelho"><section id="destaques">'
        f'<h2 class="kicker c-vermelho">Destaques</h2>{corpo_d}</section></div>'
    )

    if repetidos:
        cards_j = "".join(
            _card(by_id[r["id"]], resumos,
                  f"Ecoa a tese de {r['ref_data']}: {r['ref_tese']}"
                  if r.get("ref_data") and r.get("ref_tese") else "Repete tese já coberta")
            for r in repetidos)
        partes.append(
            f'<div class="faixa"></div><div class="wrap sec-vermelho">'
            f'<section id="jacoberto"><h2 class="kicker c-vermelho">Já coberto</h2>'
            f"{cards_j}</section></div>"
        )

    if tang_ids:
        cards_t = "".join(_card(by_id[i], resumos) for i in tang_ids)
        partes.append(
            f'<div class="faixa"></div><div class="wrap sec-verde">'
            f'<section id="tangenciais"><h2 class="kicker c-verde">Tangenciais</h2>'
            f"{cards_t}</section></div>"
        )
    if restantes:
        cards_r = "".join(_card(p, resumos) for p in restantes)
        partes.append(
            f'<div class="faixa"></div><div class="wrap sec-laranja">'
            f'<section id="tambem"><h2 class="kicker c-laranja">Também publicado ({len(restantes)})</h2>'
            f"{cards_r}</section></div>"
        )

    fonte = f"https://huggingface.co/papers/date/{_E(date)}"
    doc = (
        "<!DOCTYPE html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>papers.hf — {_E(date)}</title>\n<style>{_CSS}</style>\n</head>\n<body>\n"
        '<div class="topo-fixo"><header class="topo"><a class="logo" href="#">papers.hf</a>'
        f'<span class="data-topo">{_E(_data_por_extenso(date))}</span></header>'
        f'<nav class="marcas">{nav}</nav></div>\n'
        f"{''.join(partes)}\n"
        f'<div class="faixa"></div><footer class="wrap rodape">Fonte: '
        f'<a href="{fonte}">Daily Papers</a> · {len(papers)} papers processados</footer>\n'
        "</body>\n</html>\n"
    )
    return doc
