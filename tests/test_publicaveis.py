"""publicaveis(): o cron stagea so a edicao e o indice, nunca trabalho de outro produtor."""

import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import paths  # noqa: E402


class TestPublicaveis(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.data = Path(self._tmp.name)
        self._env_anterior = {
            chave: os.environ.get(chave)
            for chave in ("PAPERS_HOME", "PAPERS_DATA_DIR")
        }
        os.environ["PAPERS_HOME"] = str(self.data)
        os.environ["PAPERS_DATA_DIR"] = str(self.data)
        importlib.reload(paths)

    def tearDown(self):
        # paths resolve DATA no import; sem restaurar e recarregar, o tmpdir
        # deletado vaza para os outros testes da mesma execucao.
        for chave, valor in self._env_anterior.items():
            if valor is None:
                os.environ.pop(chave, None)
            else:
                os.environ[chave] = valor
        importlib.reload(paths)
        self._tmp.cleanup()

    def _criar(self, relativo: str) -> Path:
        alvo = self.data / relativo
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text("x", encoding="utf-8")
        return alvo

    def _relativos(self, obtidos: list[Path]) -> list[str]:
        return [p.relative_to(self.data).as_posix() for p in obtidos]

    def test_nota_deep_nao_commitada_fica_fora(self):
        edicao_md = self._criar("edicoes/2026/08/2026-08-31.md")
        edicao_html = self._criar("docs/2026/08/2026-08-31.html")
        indice = self._criar("docs/index.html")
        nota = self._criar("edicoes/deep/2026/08/2608.18524.md")
        pagina = self._criar("docs/deep/2026/08/2608.18524.html")

        obtidos = paths.publicaveis(["2026-08-31"])

        self.assertIn(edicao_md, obtidos)
        self.assertIn(edicao_html, obtidos)
        self.assertIn(indice, obtidos)
        self.assertNotIn(nota, obtidos)
        self.assertNotIn(pagina, obtidos)
        vazados = [
            r for r in self._relativos(obtidos)
            if r.startswith(("edicoes/deep/", "docs/deep/"))
        ]
        self.assertEqual(vazados, [], "path de outro produtor entrou no staging")

    def test_registro_moc_e_principios_ficam_fora(self):
        self._criar("edicoes/2026/08/2026-08-31.md")
        registro = self._criar("edicoes/repos-registry.md")
        moc = self._criar("edicoes/papers-moc.md")
        principio = self._criar("edicoes/principios/0002-auto-relato.md")

        obtidos = paths.publicaveis(["2026-08-31"])

        self.assertNotIn(registro, obtidos)
        self.assertNotIn(moc, obtidos)
        self.assertNotIn(principio, obtidos)

    def test_data_sem_edicao_nao_aparece(self):
        self.assertEqual(paths.publicaveis(["2026-08-31"]), [])

    def test_multiplas_datas_todas_as_existentes(self):
        trinta = self._criar("edicoes/2026/08/2026-08-30.md")
        trinta_um = self._criar("edicoes/2026/08/2026-08-31.md")

        obtidos = paths.publicaveis(["2026-08-30", "2026-08-31", "2026-08-29"])

        self.assertIn(trinta, obtidos)
        self.assertIn(trinta_um, obtidos)
        self.assertEqual(len(obtidos), 2)

    def test_indice_entra_quando_existe(self):
        self._criar("edicoes/2026/08/2026-08-31.md")
        indice = self._criar("docs/index.html")

        self.assertIn(indice, paths.publicaveis(["2026-08-31"]))


if __name__ == "__main__":
    unittest.main()
