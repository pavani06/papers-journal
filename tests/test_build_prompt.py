"""Prompt de triagem: catalogo montado pelo script, sem rede e sem LLM."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import paths  # noqa: E402
from journal import build_prompt  # noqa: E402

PAPERS = [
    {"id": "2608.10001", "title": "Paper Um", "upvotes": 40,
     "keywords": ["agents", "verification"], "abstract": "resumo do paper um"},
    {"id": "2608.10002", "title": "Paper Dois", "upvotes": 12,
     "keywords": [], "abstract": "resumo do paper dois"},
]

INTERESTS = "# Perfil\nteste\n"


class TestBuildPrompt(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        paths.DATA = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_duas_mensagens(self):
        msgs = build_prompt(PAPERS, INTERESTS, "2026-08-11")
        self.assertEqual(len(msgs), 2)
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(msgs[1]["role"], "user")

    def test_catalogo_contem_ids_e_titulos(self):
        user = build_prompt(PAPERS, INTERESTS, "2026-08-11")[1]["content"]
        self.assertIn("[2608.10001] Paper Um", user)
        self.assertIn("[2608.10002] Paper Dois", user)
        self.assertIn("Papers publicados em 2026-08-11", user)

    def test_memoria_sem_edicoes_anteriores(self):
        user = build_prompt(PAPERS, INTERESTS, "2026-08-11")[1]["content"]
        self.assertIn("Nenhuma edicao anterior disponivel", user)

    def test_perfil_do_leitor_incluido(self):
        user = build_prompt(PAPERS, INTERESTS, "2026-08-11")[1]["content"]
        self.assertIn("# Perfil do leitor", user)
        self.assertIn("teste", user)

    def test_cerca_de_dado_nao_confiavel_presente(self):
        user = build_prompt(PAPERS, INTERESTS, "2026-08-11")[1]["content"]
        self.assertIn("<<<CONTEUDO_NAO_CONFIAVEL>>>", user)
        self.assertIn("<<<FIM_CONTEUDO_NAO_CONFIAVEL>>>", user)
        inicio_catalogo = user.rfind("<<<CONTEUDO_NAO_CONFIAVEL>>>")
        fim_catalogo = user.rfind("<<<FIM_CONTEUDO_NAO_CONFIAVEL>>>")
        self.assertGreater(user.find("[2608.10001] Paper Um"), inicio_catalogo)
        self.assertLess(user.find("[2608.10001] Paper Um"), fim_catalogo)
        self.assertGreater(user.find("# Sua tarefa"), fim_catalogo)


if __name__ == "__main__":
    unittest.main()
