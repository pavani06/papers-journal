"""Casamento tolerante de ids: colchetes, prefixo arXiv, espacos, contenção."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from journal import resolve_id  # noqa: E402

BY_ID = {"2608.12345": {"id": "2608.12345"}, "2606.99999": {"id": "2606.99999"}}


class TestResolveId(unittest.TestCase):
    def test_id_exato(self):
        self.assertEqual(resolve_id("2608.12345", BY_ID), "2608.12345")

    def test_colchetes(self):
        self.assertEqual(resolve_id("[2608.12345]", BY_ID), "2608.12345")

    def test_prefixo_arxiv(self):
        self.assertEqual(resolve_id("arXiv:2608.12345", BY_ID), "2608.12345")
        self.assertEqual(resolve_id("arxiv:2608.12345", BY_ID), "2608.12345")

    def test_espacos(self):
        self.assertEqual(resolve_id("  2608.12345  ", BY_ID), "2608.12345")

    def test_contencao_bidirecional(self):
        # "2608.12" esta contido em "2608.12345"; "2608.12345" contem "12345".
        self.assertEqual(resolve_id("2608.12", BY_ID), "2608.12345")
        self.assertEqual(resolve_id("12345", BY_ID), "2608.12345")

    def test_nao_string(self):
        self.assertIsNone(resolve_id(None, BY_ID))
        self.assertIsNone(resolve_id(12345, BY_ID))

    def test_desconhecido(self):
        self.assertIsNone(resolve_id("9999.99999", BY_ID))


if __name__ == "__main__":
    unittest.main()
