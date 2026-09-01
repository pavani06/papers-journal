#!/usr/bin/env python3
"""Extrai os confrontos das notas papers-deep e agrupa por repo.

As notas sao a fonte da verdade; este script so deriva. Para cada bloco
"### [[papers/repos-registry|<repo>]]" dentro de "## Confronto com repos",
coleta a nota de origem, o veredito e as citacoes `file:line`.

Uso: python3 src/confrontos.py [dir-das-notas] [dir-de-saida]
     python3 src/confrontos.py --gate <dir-das-notas>
Read-only sobre as notas; escreve so no dir-de-saida. O default de saida fica
fora deste repo, junto dos utilitarios do orquestrador em scripts/papers-deep/,
para a derivacao nao morar dentro do objeto inspecionado.

Modo --gate: executor do gate mecanico de citacoes do fechamento
(commands/papers-deep.md, "Gate mecanico de citacoes"). Resolve cada citacao
RAW contra a raiz do repo nomeado no bloco: caminho relativo a raiz, arquivo
existe, faixa cabe. Sem reparo por heuristica, sem escrita em lugar nenhum;
sai nao-zero nomeando qualquer citacao nao resolvida.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

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


def relativa(cit: str) -> str:
    """Caminho absoluto vira relativo ao repo que o contem."""
    arq, _, linha = cit.rpartition(":")
    if arq.startswith(HOME):
        resto = arq[len(HOME):]
        arq = resto.split("/", 1)[1] if "/" in resto else resto
    return f"{arq}:{linha}"


IGNORA = {".git", ".worktrees", "worktrees", "__pycache__", ".venv"}
IGNORA_PADRAO = (".backup-", ".bak")   # copias datadas poluem os candidatos


def indexa(raiz: Path | None) -> list[str]:
    """Todos os arquivos do repo, relativos a raiz. Autoritativo para resolver
    caminho parcial (a nota cita `references/x.md`, o arquivo esta em
    `skills/issue-executor-master/references/x.md`)."""
    if raiz is None or not raiz.is_dir():
        return []
    saida = []
    for p in raiz.rglob("*"):
        if not p.is_file():
            continue
        partes = p.relative_to(raiz).parts
        if IGNORA & set(partes):
            continue
        if any(s in parte for parte in partes for s in IGNORA_PADRAO):
            continue
        saida.append(p.relative_to(raiz).as_posix())
    return saida


def normaliza(citacoes: list[str], indice: list[str], raiz: Path | None,
              repo: str = "") -> list[str]:
    """Caminho parcial ou basename solto -> caminho real, quando o repo tem
    exatamente um arquivo terminando naquele sufixo. Caminho que ja resolve
    fica intacto, entao README.md da raiz nunca vira examples/README.md."""
    locais = [c.rpartition(":")[0] for c in citacoes if "/" in c.rpartition(":")[0]]
    saida = []
    for c in citacoes:
        arq, _, linha = c.rpartition(":")
        if not (raiz and (raiz / arq).is_file()):
            # a nota as vezes prefixa com o nome do proprio repo
            if repo and arq.startswith(repo + "/") and raiz \
                    and (raiz / arq[len(repo) + 1:]).is_file():
                arq = arq[len(repo) + 1:]
            else:
                for fonte in (indice, locais):
                    cand = [p for p in fonte if p.endswith("/" + arq)]
                    if len(cand) == 1:
                        arq = cand[0]
                        break
        saida.append(f"{arq}:{linha}")
    return sorted(set(saida))


def resolve(cit: str, raiz: Path | None) -> bool:
    """A citacao aponta para arquivo existente, com a linha dentro dele?"""
    if raiz is None:
        return False
    arq, _, faixa = cit.rpartition(":")
    alvo = raiz / arq
    if not alvo.is_file():
        return False
    fim = faixa.split("-")[-1]
    if not fim.isdigit():
        return False
    try:
        n = len(alvo.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return False
    return int(fim) <= n


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
            cits = [relativa(f"{a}:{l}") for a, l in CITACAO.findall(bloco)]
            por_repo[nome].append((nota.stem, titulo, ver, cits))

    # 2a passada: resolve caminho contra o sistema de arquivos de cada repo
    indices = {repo: indexa(conhecidos.get(repo)) for repo in por_repo}

    SAIDA.mkdir(parents=True, exist_ok=True)
    print(f"{'repo':20} {'confrontos':>10} {'no repo':>8} {'outro':>6} {'sem alvo':>9}")
    for repo, itens in sorted(por_repo.items(), key=lambda kv: -len(kv[1])):
        linhas = [f"# Confrontos do papers-deep — {repo}", "",
                  f"{len(itens)} confrontos, derivados das notas em `{NOTAS.relative_to(RAIZ)}`.",
                  "A nota de origem tem o raciocínio completo; as citações são pista a",
                  "verificar contra o código atual, nunca fato.", ""]
        raiz = conhecidos.get(repo)
        indice = indices[repo]
        n_aqui = n_outro = n_sem = 0
        for stem, titulo, ver, cits in itens:
            linhas += [f"## {stem} — {titulo}", "", f"**Veredito:** {ver}", ""]
            aqui, outro, sem = [], [], []
            for c in normaliza(cits, indice, raiz, repo):
                if resolve(c, raiz):
                    aqui.append(c)
                    continue
                donos = [r for r, rz in conhecidos.items()
                         if r != repo and resolve(c, rz)]
                (outro.append(f"{donos[0]}/{c}") if len(donos) == 1
                 else sem.append(c))
            if aqui:
                linhas += ["Evidência: " + ", ".join(f"`{c}`" for c in aqui), ""]
            if outro:
                linhas += ["Evidência em outro repo: "
                           + ", ".join(f"`{c}`" for c in outro), ""]
            if sem:
                linhas += ["Citações não resolvidas (nome ambíguo ou linha fora do "
                           "arquivo): " + ", ".join(f"`{c}`" for c in sem), ""]
            n_aqui += len(aqui); n_outro += len(outro); n_sem += len(sem)
        paths.escrever(SAIDA / f"{repo}.md", "\n".join(linhas))
        print(f"{repo:20} {len(itens):>10} {n_aqui:>8} {n_outro:>6} {n_sem:>9}")

    print(f"\nnotas sem confronto aplicável: {len(vazias)}"
          + (f" ({', '.join(vazias)})" if vazias else ""))
    if anomalias:
        print(f"\nblocos que não nomeiam repo do registro: {len(anomalias)}")
        for stem, nome in anomalias:
            print(f"  {stem}: {nome!r}")


def gate(argv: list[str]) -> int:
    """Executor estrito do gate mecanico: resolve RAW, nao grava, falha alto."""
    if not argv:
        print("uso: confrontos.py --gate <dir-das-notas> (diretorio obrigatorio)",
              file=sys.stderr)
        return 2
    notas_dir = Path(argv[0])
    if not notas_dir.is_dir():
        print(f"gate: diretorio de notas inexistente: {notas_dir}", file=sys.stderr)
        return 2
    conhecidos = repos_do_registro()
    notas = sorted(notas_dir.glob("*.md"))
    total = resolvidas = 0
    pendentes: list[tuple[str, str, str]] = []
    for nota in notas:
        txt = nota.read_text(encoding="utf-8")
        m = re.search(r"^## Confronto com repos\s*$(.*)", txt, re.M | re.S)
        if not m or "nenhum confronto aplicável" in m.group(1).lower():
            continue
        for bloco in re.split(r"^### ", m.group(1), flags=re.M)[1:]:
            c = CABECA.match(bloco.strip())
            nome = c.group(1) if c else "(bloco sem repo do registro)"
            raiz = conhecidos.get(c.group(1)) if c else None
            citacoes = sorted(set(f"{a}:{l}" for a, l in CITACAO.findall(bloco)))
            for cita in citacoes:
                total += 1
                arq, _, faixa = cita.rpartition(":")
                if (raiz is not None and arq and not Path(arq).is_absolute()
                        and faixa.split("-")[-1].isdigit() and resolve(cita, raiz)):
                    resolvidas += 1
                else:
                    pendentes.append((nota.name, nome, cita))
    print(f"gate: {len(notas)} notas, {total} citacoes, "
          f"{resolvidas} resolvidas, {len(pendentes)} nao resolvidas")
    for nota, repo, cita in pendentes:
        print(f"  nao resolvida: {nota} [{repo}] {cita}")
    return 1 if pendentes else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gate":
        sys.exit(gate(sys.argv[2:]))
    main()
