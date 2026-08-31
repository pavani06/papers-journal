"""Gate da relacao no chapeu: degrada com stderr, nunca afirma sem verificacao."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import paths  # noqa: E402
from journal import chapeu_md  # noqa: E402


class TestChapeuMd(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        paths.DATA = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _chapeu(self, rel: dict, date: str = "2026-08-11") -> tuple[list[str], str]:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            out = chapeu_md({"id": "2608.1", "relacao": rel}, date)
        return out, err.getvalue()

    def test_tipo_novo_sai_calado(self):
        out, err = self._chapeu({"tipo": "novo", "ref_data": "", "ref_tese": ""})
        self.assertEqual(out, [])
        self.assertEqual(err, "")

    def test_tipo_desconhecido_rejeita_com_aviso(self):
        out, err = self._chapeu({"tipo": "eco", "ref_data": "2026-08-10"})
        self.assertEqual(out, [])
        self.assertIn("[relacao rejeitada]", err)
        self.assertIn("tipo desconhecido", err)

    def test_sem_ref_data_rejeita(self):
        out, err = self._chapeu({"tipo": "avanca", "ref_data": ""})
        self.assertEqual(out, [])
        self.assertIn("sem ref_data", err)

    def test_ref_data_fora_do_formato_rejeita(self):
        out, err = self._chapeu({"tipo": "avanca", "ref_data": "10/08/2026"})
        self.assertEqual(out, [])
        self.assertIn("fora do formato", err)

    def test_edicao_inexistente_rejeita(self):
        out, err = self._chapeu({"tipo": "avanca", "ref_data": "2026-08-10",
                                 "delta": "estende"})
        self.assertEqual(out, [])
        self.assertIn("nao existe em disco", err)

    def test_valido_monta_chapeu(self):
        edicao = paths.edicao_md("2026-08-10")
        edicao.parent.mkdir(parents=True, exist_ok=True)
        edicao.write_text("# Papers de 2026-08-10\n", encoding="utf-8")
        out, err = self._chapeu({"tipo": "avanca", "ref_data": "2026-08-10",
                                 "delta": "estende para X"})
        self.assertEqual(len(out), 2)
        self.assertIn("**Avança [10/08](../../2026/08/2026-08-10.md)**", out[0])
        self.assertIn("estende para X", out[0])
        self.assertEqual(err, "")

    def test_contradiz_rotula_contradiz(self):
        edicao = paths.edicao_md("2026-08-10")
        edicao.parent.mkdir(parents=True, exist_ok=True)
        edicao.write_text("# Papers de 2026-08-10\n", encoding="utf-8")
        out, _ = self._chapeu({"tipo": "contradiz", "ref_data": "2026-08-10",
                               "ref_tese": "tese antiga"})
        self.assertIn("**Contradiz [10/08]", out[0])


if __name__ == "__main__":
    unittest.main()
