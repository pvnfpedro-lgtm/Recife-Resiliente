"""Confere que o Index do painel monta com todos os arquivos que ele inclui."""

import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import montar_painel as m  # noqa: E402


class TestMontarPainel(unittest.TestCase):
    def setUp(self):
        self.html = m.montar()

    def test_nenhum_include_sobra(self):
        self.assertNotIn("<?", self.html)

    def test_um_style_e_um_script_proprios(self):
        # Tags no começo da linha (o texto da página de impressão do ranking também tem <style>).
        def conta(tag):
            return len(re.findall(r"^" + tag, self.html, re.M))
        self.assertEqual(conta("<style>"), 1)
        self.assertEqual(conta("</style>"), 1)
        # O único <script> sem src é o do painel (as 4 partes juntas).
        self.assertEqual(conta("<script>"), 1)
        self.assertEqual(conta("</script>"), 1)

    def test_partes_na_ordem(self):
        pos = [self.html.index(t) for t in (
            "window.onerror", "PONTOS CRÍTICOS — lidos da planilha",
            "GOOGLE STREET VIEW", "PÁGINA 1 — KPIs + lista", "buildFilterBar();")]
        self.assertEqual(pos, sorted(pos))


if __name__ == "__main__":
    unittest.main()
