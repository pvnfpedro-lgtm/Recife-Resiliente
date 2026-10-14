"""Testes do CSV de pontos das obras, com linhas fictícias."""

import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import gerar_pontos_obras as g  # noqa: E402


def linha(oid, tipo="Canal", status="", coord="-8.08, -34.93", nome="Obra teste"):
    return {"obra_id": oid, "nome": nome, "tipo": tipo, "status": status,
            "coordenadas (lat, lon)": coord, "coord_precisao": ""}


class TestPontosObras(unittest.TestCase):
    def test_categorias_dos_tipos(self):
        self.assertEqual(g.categoria("Perfilamento do Rio Tejipió"), "canal")
        self.assertEqual(g.categoria("microrreservatório"), "reservatorio")
        self.assertEqual(g.categoria(" Diques  e comportas "), "dique")
        self.assertEqual(g.categoria(""), "")

    def test_icone_pela_situacao(self):
        self.assertEqual(g.icone("dique", g.situacao("Em licitação")), "obra_dique_licitacao")
        self.assertEqual(g.icone("dique", g.situacao("Concluído")), "obra_dique")
        self.assertEqual(g.icone("dique", g.situacao("")), "obra_dique")
        self.assertEqual(g.icone("", "em_obra"), "")

    def test_coordenadas(self):
        self.assertEqual(g.coordenadas("-8.1, -34.9"), (-8.1, -34.9))
        self.assertIsNone(g.coordenadas("-8,1 -34,9"))
        self.assertIsNone(g.coordenadas(""))

    def test_montar_separa_pendencias(self):
        pontos, pend = g.montar([
            linha("1", status="obra"),
            linha("2", coord=""),                      # sem coordenada
            linha("3", coord="-34.93, -8.08"),         # lat e lon trocadas
            linha("4", tipo=""),                       # sem tipo
            {"obra_id": "", "nome": ""},               # linha vazia
        ])
        self.assertEqual([p["obra_id"] for p in pontos], ["1", "4"])
        self.assertEqual(pontos[0]["icone"], "obra_canal")
        self.assertEqual(pontos[0]["status"], "em_obra")
        self.assertEqual(pontos[1]["icone"], "")
        self.assertEqual(len(pend), 3)


if __name__ == "__main__":
    unittest.main()
