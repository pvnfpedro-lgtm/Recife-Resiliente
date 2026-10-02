"""Testes com dados fictícios (tests/fixtures) — não são dados da RPA 6."""

import io
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import hierarquizar as h  # noqa: E402

FIX = RAIZ / "tests" / "fixtures"


def rodar(**kw):
    return h.hierarquizar(
        h.ler_csv(FIX / "criterios.csv"),
        h.ler_csv(FIX / "notas.csv"),
        h.ler_csv(FIX / "tratabilidade.csv"),
        **kw,
    )


class TestHierarquizar(unittest.TestCase):
    def test_score_ponderado(self):
        p01 = {r["ponto_id"]: r for r in rodar()}["P01"]
        # HID = (5*2 + 2*1)/3 = 4; SOC = 4; score = (4*3 + 4*1)/4 = 4
        self.assertAlmostEqual(p01["dim_HID"], 4.0)
        self.assertAlmostEqual(p01["score"], 4.0)
        self.assertEqual(p01["cobertura"], "3/3")

    def test_nota_ausente_nao_imputada(self):
        p02 = {r["ponto_id"]: r for r in rodar()}["P02"]
        self.assertEqual(p02["cobertura"], "2/3")
        self.assertIsNone(p02["dim_SOC"])
        self.assertAlmostEqual(p02["score"], 1.0)

    def test_ranking_e_matriz(self):
        r = rodar()
        self.assertEqual([x["ponto_id"] for x in r], ["P01", "P02"])
        self.assertEqual(r[0]["posicao"], 1)
        self.assertEqual(r[0]["quadrante"], "Agir já")       # crit 4, trat 3
        self.assertEqual(r[1]["quadrante"], "Oportunidade")  # crit 1, trat 5
        self.assertEqual(rodar(corte=3.5)[0]["quadrante"], "Estruturar")

    def test_nota_fora_da_escala(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        with self.assertRaises(h.ErroDeDados):
            h.hierarquizar(crit, [{"ponto_id": "P", "codigo": "H1", "nota": "6"}])

    def test_codigo_desconhecido(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        with self.assertRaises(h.ErroDeDados):
            h.hierarquizar(crit, [{"ponto_id": "P", "codigo": "X9", "nota": "3"}])

    def test_peso_dimensao_inconsistente(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        crit[1]["peso_dimensao"] = "9"
        with self.assertRaises(h.ErroDeDados):
            h.hierarquizar(crit, [])

    def test_virgula_decimal(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        r = h.hierarquizar(crit, [{"ponto_id": "P", "codigo": "S1", "nota": "3,5"}])
        self.assertAlmostEqual(r[0]["score"], 3.5)

    def test_escrever_csv(self):
        buf = io.StringIO()
        h.escrever(rodar(), buf)
        linhas = buf.getvalue().splitlines()
        self.assertTrue(linhas[0].startswith("posicao,ponto_id,score"))
        self.assertIn("P01,4.00,3/3,3.00,Agir já", linhas[1])


if __name__ == "__main__":
    unittest.main()
