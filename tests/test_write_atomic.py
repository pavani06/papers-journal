"""Escrita atomica: ou o destino tem o conteudo anterior, ou o novo inteiro."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import paths  # noqa: E402


class TestEscrever(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_grava_conteudo_completo(self):
        alvo = self.dir / "sub" / "a.json"
        paths.escrever(alvo, '{"x": 1}')
        self.assertEqual(alvo.read_text(encoding="utf-8"), '{"x": 1}')

    def test_nao_sobra_temporario(self):
        alvo = self.dir / "b.json"
        paths.escrever(alvo, "conteudo")
        sobras = list(self.dir.glob("*.tmp")) + list(self.dir.glob(".*.tmp"))
        self.assertEqual(sobras, [])

    def test_substitui_conteudo_anterior(self):
        alvo = self.dir / "c.json"
        paths.escrever(alvo, "velho")
        paths.escrever(alvo, "novo")
        self.assertEqual(alvo.read_text(encoding="utf-8"), "novo")

    def test_diretorio_criado(self):
        alvo = self.dir / "x" / "y" / "z.json"
        paths.escrever(alvo, "conteudo")
        self.assertTrue(alvo.is_file())


if __name__ == "__main__":
    unittest.main()
