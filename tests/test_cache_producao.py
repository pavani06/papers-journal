"""Selo de producao e digest do cache: atribuivel, verificavel, retrocompativel."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import paths  # noqa: E402
from journal import montar_cache  # noqa: E402

PAPERS = [
    {"id": "2608.10001", "title": "Paper Um", "upvotes": 40, "keywords": [],
     "abstract": "x" * 500},
]
VERDICT = {"manchete": "m", "abertura": "a", "destaques": [], "tangenciais": [],
           "repetidos": [], "resumos": {}}


class TestMontarCache(unittest.TestCase):
    def test_selo_de_producao_presente(self):
        payload = montar_cache(PAPERS, VERDICT, "perfil", "gpt-5.5", "2026-08-11")
        prod = payload["producao"]
        self.assertEqual(prod["modelo"], "gpt-5.5")
        self.assertIn("criado_em", prod)
        self.assertEqual(len(prod["interests_sha256"]), 64)
        self.assertEqual(len(prod["prompt_sha256"]), 64)

    def test_abstract_truncado_no_cache(self):
        payload = montar_cache(PAPERS, VERDICT, "perfil", "gpt-5.5", "2026-08-11")
        self.assertLessEqual(len(payload["papers"][0]["abstract"]), 200)

    def test_digest_cobre_papers_e_verdict(self):
        payload = montar_cache(PAPERS, VERDICT, "perfil", "gpt-5.5", "2026-08-11")
        esperado = paths.digest_conteudo(
            {"papers": payload["papers"], "verdict": payload["verdict"]})
        self.assertEqual(payload["digest"], esperado)

    def test_digest_detecciona_adulteracao(self):
        payload = montar_cache(PAPERS, VERDICT, "perfil", "gpt-5.5", "2026-08-11")
        payload["verdict"] = {**payload["verdict"], "manchete": "adulterado"}
        conferido = paths.digest_conteudo(
            {"papers": payload["papers"], "verdict": payload["verdict"]})
        self.assertNotEqual(conferido, payload["digest"])


class TestMemoriaComDigest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        paths.DATA = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _grava(self, date: str, payload: dict) -> None:
        p = paths.cache(date)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def test_cache_com_digest_integro_e_lido(self):
        payload = montar_cache(PAPERS, VERDICT, "perfil", "gpt-5.5", "2026-08-11")
        self._grava("2026-08-10", payload)
        out = paths.vereditos_anteriores("2026-08-11", 10)
        self.assertEqual([d for d, _ in out], ["2026-08-10"])

    def test_cache_adulterado_nao_entra_como_memoria(self):
        payload = montar_cache(PAPERS, VERDICT, "perfil", "gpt-5.5", "2026-08-11")
        payload["verdict"] = {**payload["verdict"], "manchete": "adulterado"}
        self._grava("2026-08-10", payload)
        out = paths.vereditos_anteriores("2026-08-11", 10)
        self.assertEqual(out, [])

    def test_cache_antigo_sem_digest_continua_compativel(self):
        self._grava("2026-08-10",
                    {"papers": [], "verdict": {"manchete": "m"}})
        out = paths.vereditos_anteriores("2026-08-11", 10)
        self.assertEqual([d for d, _ in out], ["2026-08-10"])


if __name__ == "__main__":
    unittest.main()
