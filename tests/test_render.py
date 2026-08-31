"""Render do jornal: secoes esperadas, chapeu de relacao, rodape honesto."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import paths  # noqa: E402
from journal import render  # noqa: E402

PAPERS = [
    {"id": "2608.10001", "title": "Paper Um", "upvotes": 40, "comments": 3,
     "authors": ["A", "B"], "abstract": "resumo 1", "one_liner": "", "keywords": []},
    {"id": "2608.10002", "title": "Paper Dois", "upvotes": 12, "comments": 0,
     "authors": ["C"], "abstract": "resumo 2", "one_liner": "", "keywords": []},
]

VERDICT_BASE = {
    "manchete": "Dia de destaque",
    "abertura": "O dia trouxe um paper relevante.",
    "destaques": [],
    "tangenciais": [],
    "repetidos": [],
    "resumos": {"2608.10001": "Faz X", "2608.10002": "Faz Y"},
}


class TestRender(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        paths.DATA = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_secoes_esperadas(self):
        v = {**VERDICT_BASE,
             "destaques": [{"id": "2608.10001", "tese": "t", "analise": "a",
                            "aproveitavel": "ap", "relacao": {"tipo": "novo"}}],
             "tangenciais": ["2608.10002"]}
        md = render("2026-08-11", PAPERS, v)
        self.assertIn("# Papers de 2026-08-11", md)
        self.assertIn("## Destaques", md)
        self.assertIn("## Tangenciais", md)
        self.assertIn("[Paper Um](https://huggingface.co/papers/2608.10001)", md)
        self.assertIn("Fonte: [Daily Papers]", md)

    def test_relacao_novo_nao_gera_chapeu(self):
        v = {**VERDICT_BASE,
             "destaques": [{"id": "2608.10001", "tese": "t", "analise": "a",
                            "aproveitavel": "ap", "relacao": {"tipo": "novo"}}]}
        md = render("2026-08-11", PAPERS, v)
        self.assertNotIn("Avança", md)
        self.assertNotIn("Contradiz", md)

    def test_relacao_avanca_gera_chapeu_quando_edicao_existe(self):
        edicao = paths.edicao_md("2026-08-10")
        edicao.parent.mkdir(parents=True, exist_ok=True)
        edicao.write_text("# Papers de 2026-08-10\n", encoding="utf-8")
        v = {**VERDICT_BASE,
             "destaques": [{"id": "2608.10001", "tese": "t", "analise": "a",
                            "aproveitavel": "ap",
                            "relacao": {"tipo": "avanca", "ref_data": "2026-08-10",
                                        "delta": "estende para X"}}]}
        md = render("2026-08-11", PAPERS, v)
        self.assertIn("**Avança [10/08]", md)

    def test_sem_destaques_diz_dia_fraco(self):
        v = {**VERDICT_BASE}
        md = render("2026-08-11", PAPERS, v)
        self.assertIn("Nenhum paper de hoje passou o critério", md)

    def test_repetidos_vai_para_ja_coberto(self):
        v = {**VERDICT_BASE,
             "repetidos": [{"id": "2608.10002", "ref_data": "2026-08-10",
                            "ref_tese": "tese antiga"}]}
        md = render("2026-08-11", PAPERS, v)
        self.assertIn("## Já coberto", md)
        self.assertIn("Ecoa a tese de 2026-08-10", md)


if __name__ == "__main__":
    unittest.main()
