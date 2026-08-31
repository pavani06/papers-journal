"""Memoria de edicoes anteriores: filtro por data, tolerancia a cache invalido."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import paths  # noqa: E402
from journal import bloco_memoria  # noqa: E402


def _grava_cache(date: str, conteudo: str) -> None:
    p = paths.cache(date)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(conteudo, encoding="utf-8")


class TestVereditosAnteriores(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        paths.DATA = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_sem_cache_retorna_vazio(self):
        self.assertEqual(paths.vereditos_anteriores("2026-08-11", 10), [])

    def test_le_veredito_valido(self):
        _grava_cache("2026-08-10", json.dumps({"papers": [], "verdict": {"manchete": "m"}}))
        out = paths.vereditos_anteriores("2026-08-11", 10)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0][0], "2026-08-10")

    def test_cache_corrompido_e_pulado_sem_derruba(self):
        _grava_cache("2026-08-10", '{"papers": [], "verdict": {"manchete": "m"}}')
        _grava_cache("2026-08-09", "isso nao e json")
        out = paths.vereditos_anteriores("2026-08-11", 10)
        self.assertEqual([d for d, _ in out], ["2026-08-10"])

    def test_cache_sem_verdict_e_pulado(self):
        _grava_cache("2026-08-10", '{"papers": []}')
        out = paths.vereditos_anteriores("2026-08-11", 10)
        self.assertEqual(out, [])

    def test_filtro_por_data(self):
        _grava_cache("2026-08-10", json.dumps({"papers": [], "verdict": {}}))
        _grava_cache("2026-08-11", json.dumps({"papers": [], "verdict": {}}))
        # Para a edicao de 11/08, o cache de 11/08 (o proprio dia) nao conta.
        out = paths.vereditos_anteriores("2026-08-11", 10)
        self.assertEqual([d for d, _ in out], ["2026-08-10"])

    def test_limite_respeitado(self):
        _grava_cache("2026-08-10", json.dumps({"papers": [], "verdict": {}}))
        _grava_cache("2026-08-09", json.dumps({"papers": [], "verdict": {}}))
        out = paths.vereditos_anteriores("2026-08-11", 1)
        self.assertEqual([d for d, _ in out], ["2026-08-10"])

    def test_bloco_memoria_sem_anteriores(self):
        msg = bloco_memoria("2026-08-11")
        self.assertIn("Nenhuma edicao anterior disponivel", msg)


if __name__ == "__main__":
    unittest.main()
