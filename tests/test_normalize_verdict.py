"""Normalizacao do veredito: ids casam com o catalogo; orfaos nunca viram jornal falso."""

import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from journal import Fatal, normalize_verdict  # noqa: E402

PAPERS = [
    {"id": "2608.10001", "title": "Paper Um"},
    {"id": "2608.10002", "title": "Paper Dois"},
]


class TestNormalizeVerdict(unittest.TestCase):
    def test_id_valido_mantido(self):
        v = {"destaques": [{"id": "2608.10001", "tese": "t"}]}
        out = normalize_verdict(v, PAPERS)
        self.assertEqual(out["destaques"][0]["id"], "2608.10001")

    def test_todos_orfaos_derruba(self):
        v = {"destaques": [{"id": "9999.1", "tese": "t"}]}
        with self.assertRaises(Fatal) as ctx:
            normalize_verdict(v, PAPERS)
        self.assertEqual(ctx.exception.code, 3)

    def test_orfaos_parciais_descartados_com_aviso(self):
        err = io.StringIO()
        v = {"destaques": [
            {"id": "2608.10001", "tese": "t1"},
            {"id": "9999.2", "tese": "t2"},
        ]}
        with contextlib.redirect_stderr(err):
            out = normalize_verdict(v, PAPERS)
        self.assertEqual([d["id"] for d in out["destaques"]], ["2608.10001"])
        self.assertIn("descartado(s) por id desconhecido", err.getvalue())

    def test_repetido_sem_citacao_vira_warn(self):
        err = io.StringIO()
        v = {"destaques": [], "repetidos": [{"id": "2608.10002"}]}
        with contextlib.redirect_stderr(err):
            out = normalize_verdict(v, PAPERS)
        self.assertEqual(len(out["repetidos"]), 1)
        self.assertIn("sem citacao completa", err.getvalue())

    def test_tangencial_nao_duplica_destaque(self):
        v = {"destaques": [{"id": "2608.10001", "tese": "t"}],
             "tangenciais": ["2608.10001", "2608.10002"]}
        out = normalize_verdict(v, PAPERS)
        self.assertEqual(out["tangenciais"], ["2608.10002"])

    def test_resumo_faltante_vira_warn(self):
        err = io.StringIO()
        v = {"destaques": [], "tangenciais": [], "repetidos": [],
             "resumos": {"2608.10001": "Resumo um"}}
        with contextlib.redirect_stderr(err):
            out = normalize_verdict(v, PAPERS)
        self.assertIn("sem resumo", err.getvalue())
        self.assertNotIn("2608.10002", out["resumos"])


if __name__ == "__main__":
    unittest.main()
