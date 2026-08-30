#!/usr/bin/env python3
"""Extrai os confrontos das notas papers-deep e agrupa por repo.

As notas sao a fonte da verdade; este script so deriva. Para cada bloco
"### [[papers/repos-registry|<repo>]]" dentro de "## Confronto com repos",
coleta a nota de origem, o veredito e as citacoes `file:line`.

Uso: python3 src/confrontos.py [dir-das-notas] [dir-de-saida]
Read-only sobre as notas; escreve so no dir-de-saida. O default de saida fica
fora deste repo, junto dos utilitarios do orquestrador em scripts/papers-deep/,
para a derivacao nao morar dentro do objeto inspecionado.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOTAS = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "edicoes/deep/2026/08"
SAIDA = (Path(sys.argv[2]) if len(sys.argv) > 2
         else Path.home() / "scripts/papers-deep/confrontos")
REGISTRO = RAIZ / "edicoes/repos-registry.md"
HOME = str(Path.home()) + "/"

CITACAO = re.compile(r"`([\w./-]+\.(?:py|sh|ts|toml|md|json|yml|yaml)):(\d+(?:-\d+)?)`")
# numero dentro ou fora do negrito, separador opcional
VEREDITO = re.compile(
    r"\*\*\s*(?:\d+\.\s*)?Veredito\s*\*\*\s*[:—–-]?\s*(.+?)(?=\n\n|\n###|\Z)", re.S)
CABECA = re.compile(r"\[\[papers/repos-registry\|([^\]]+)\]\]")


def repos_do_registro() -> dict[str, Path]:
    """nome -> raiz no disco, para a guarda de normalizacao."""
    out = {}
    for bloco in re.split(r"\n(?=## )", REGISTRO.read_text(encoding="utf-8")):
        m = re.match(r"^## (.+)", bloco)
        p = re.search(r"path:\s*`?([^\s`\n]+)", bloco)
        if m and p:
            out[m.group(1).strip()] = Path(p.group(1).replace("~", str(Path.home())))
    return out


def normaliza(citacoes: list[str], raiz: Path | None) -> list[str]:
    """Absoluto -> relativo ao repo; basename solto -> caminho longo, quando
    houver exatamente um candidato E o arquivo nao existir na raiz do repo."""
    rel = []
    for c in citacoes:
        arq, _, linha = c.rpartition(":")
        if arq.startswith(HOME):
            resto = arq[len(HOME):]
            arq = resto.split("/", 1)[1] if "/" in resto else resto
        rel.append(f"{arq}:{linha}")

    longos = {c.rpartition(":")[0] for c in rel if "/" in c.rpartition(":")[0]}
    saida = []
    for c in rel:
        arq, _, linha = c.rpartition(":")
        if "/" not in arq:
            cand = [L for L in longos if L.endswith("/" + arq)]
            if len(cand) == 1 and not (raiz and (raiz / arq).is_file()):
                arq = cand[0]
        saida.append(f"{arq}:{linha}")
    return sorted(set(saida))


def main() -> None:
    conhecidos = repos_do_registro()
    por_repo: dict[str, list] = collections.defaultdict(list)
    vazias: list[str] = []
    anomalias: list[tuple[str, str]] = []

    for nota in sorted(NOTAS.glob("*.md")):
        txt = nota.read_text(encoding="utf-8")
        m = re.search(r"^## Confronto com repos\s*$(.*)", txt, re.M | re.S)
        if not m:
            continue
        corpo = m.group(1)
        if "nenhum confronto aplicável" in corpo.lower():
            vazias.append(nota.stem)
            continue
        t = re.search(r"^title:\s*\"?(.+?)\"?\s*$", txt, re.M)
        titulo = t.group(1) if t else nota.stem
        for bloco in re.split(r"^### ", corpo, flags=re.M)[1:]:
            c = CABECA.match(bloco.strip())
            nome = c.group(1) if c else bloco.split("\n")[0].strip()
            if nome not in conhecidos:
                anomalias.append((nota.stem, nome))
                continue
            v = VEREDITO.search(bloco)
            ver = " ".join(v.group(1).split())[:400] if v else "(sem veredito)"
            cits = normaliza([f"{a}:{l}" for a, l in CITACAO.findall(bloco)],
                             conhecidos.get(nome))
            por_repo[nome].append((nota.stem, titulo, ver, cits))

    SAIDA.mkdir(parents=True, exist_ok=True)
    print(f"{'repo':20} {'confrontos':>10} {'citações':>9} {'arquivos':>9}")
    for repo, itens in sorted(por_repo.items(), key=lambda kv: -len(kv[1])):
        linhas = [f"# Confrontos do papers-deep — {repo}", "",
                  f"{len(itens)} confrontos, derivados das notas em `{NOTAS.relative_to(RAIZ)}`.",
                  "A nota de origem tem o raciocínio completo; as citações são pista a",
                  "verificar contra o código atual, nunca fato.", ""]
        arquivos = set()
        for stem, titulo, ver, cits in itens:
            linhas += [f"## {stem} — {titulo}", "", f"**Veredito:** {ver}", ""]
            if cits:
                linhas += ["Evidência: " + ", ".join(f"`{c}`" for c in cits), ""]
            arquivos.update(c.rpartition(":")[0] for c in cits)
        (SAIDA / f"{repo}.md").write_text("\n".join(linhas), encoding="utf-8")
        n_cit = sum(len(c) for *_, c in itens)
        print(f"{repo:20} {len(itens):>10} {n_cit:>9} {len(arquivos):>9}")

    print(f"\nnotas sem confronto aplicável: {len(vazias)}"
          + (f" ({', '.join(vazias)})" if vazias else ""))
    if anomalias:
        print(f"\nblocos que não nomeiam repo do registro: {len(anomalias)}")
        for stem, nome in anomalias:
            print(f"  {stem}: {nome!r}")


if __name__ == "__main__":
    main()
