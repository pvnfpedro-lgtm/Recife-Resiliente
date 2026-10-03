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


def por_id(resultado):
    return {r["ponto_id"]: r for r in resultado}


class TestHierarquizar(unittest.TestCase):
    def test_risco_probabilidade_vezes_consequencia(self):
        p01 = por_id(rodar())["P01"]
        # P = (5*2 + 2*1)/3 = 4; C = (4*2 + 2*1 + 2*1)/4 = 3; risco = 12
        self.assertAlmostEqual(p01["probabilidade"], 4.0)
        self.assertAlmostEqual(p01["consequencia"], 3.0)
        self.assertAlmostEqual(p01["risco"], 12.0)
        self.assertAlmostEqual(p01["indice"], 11 / 24)
        self.assertEqual(p01["cobertura"], "5/5")

    def test_nota_ausente_nao_imputada(self):
        p02 = por_id(rodar())["P02"]
        self.assertEqual(p02["cobertura"], "4/5")
        self.assertIsNone(p02["dim_Vulnerabilidade"])
        # C = (5*2 + 5*1)/3 = 5; P = 1; risco = 5
        self.assertAlmostEqual(p02["risco"], 5.0)

    def test_sem_probabilidade_sem_risco(self):
        p03 = por_id(rodar())["P03"]
        self.assertIsNone(p03["risco"])
        self.assertAlmostEqual(p03["consequencia"], 5.0)
        self.assertEqual(p03["posicao"], "")

    def test_ranking_e_matriz(self):
        r = rodar()
        self.assertEqual([x["ponto_id"] for x in r], ["P01", "P02", "P03"])
        self.assertEqual(r[0]["posicao"], 1)
        self.assertEqual(r[0]["quadrante"], "Agir já")       # risco 12, trat 3
        self.assertEqual(r[1]["quadrante"], "Oportunidade")  # risco 5, trat 5
        self.assertEqual(rodar(corte_trat=3.5)[0]["quadrante"], "Estruturar")
        self.assertEqual(rodar(corte_risco=13)[0]["quadrante"], "Oportunidade")

    def test_nota_fora_da_escala(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        with self.assertRaises(h.ErroDeDados):
            h.hierarquizar(crit, [{"ponto_id": "P", "codigo": "P1", "nota": "6"}])

    def test_codigo_desconhecido(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        with self.assertRaises(h.ErroDeDados):
            h.hierarquizar(crit, [{"ponto_id": "P", "codigo": "X9", "nota": "3"}])

    def test_peso_dimensao_inconsistente(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        crit.append({"codigo": "E2", "dimensao": "Exposição", "subcriterio": "x",
                     "peso_subcriterio": "1", "peso_dimensao": "9"})
        with self.assertRaises(h.ErroDeDados):
            h.hierarquizar(crit, [])

    def test_peso_vazio_so_na_probabilidade(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        crit[2]["peso_dimensao"] = ""
        with self.assertRaises(h.ErroDeDados):
            h.hierarquizar(crit, [])

    def test_virgula_decimal(self):
        crit = h.ler_csv(FIX / "criterios.csv")
        notas = [{"ponto_id": "P", "codigo": "P1", "nota": "2,5"},
                 {"ponto_id": "P", "codigo": "E1", "nota": "4"}]
        self.assertAlmostEqual(h.hierarquizar(crit, notas)[0]["risco"], 10.0)

    def test_escrever_csv(self):
        buf = io.StringIO()
        h.escrever(rodar(), buf)
        linhas = buf.getvalue().splitlines()
        self.assertTrue(linhas[0].startswith(
            "posicao,ponto_id,risco,indice,probabilidade,consequencia"))
        self.assertIn("1,P01,12.00,0.46,4.00,3.00,5/5,3.00,Agir já", linhas[1])


if __name__ == "__main__":
    unittest.main()
