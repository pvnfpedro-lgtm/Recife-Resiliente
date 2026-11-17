"""E2 Equipamentos públicos: equipamentos no círculo de 300 m de cada ponto crítico (17/11/2026, pedido de Pedro).

Fonte: Base de Equipamentos do Farol (04/08/2026), já filtrada para o alagamento e usada no painel
(appscript/DadosEquipamentos.html): (1) pessoas que dependem de outros para sair, (2) saúde que faz falta
depois da chuva, (3) apoio à população atingida. Os 3 grupos contam. Distância em SIRGAS 2000 / UTM 25S.
Escala do checklist (faixa fixa): nenhum = 1; 1 = 2; 2 = 3; 3–4 = 4; 5 ou mais, ou hospital/UPA no círculo = 5.

Uso: python3 scripts/calcular_e2_equipamentos.py
Saída: dados/processados/e2_equipamentos_300m.csv
"""
import csv, json, os, re
from shapely.geometry import Point
from pyproj import Transformer

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PONTOS = [  # id, lat, lon (aba "Notas dos pontos", 17/11/2026; aproximadas)
 (5,-8.113732,-34.893163),(6,-8.111009,-34.891491),(7,-8.115380,-34.894176),(11,-8.111816,-34.894789),
 (12,-8.112935,-34.896796),(18,-8.138796,-34.913979),(26,-8.145055,-34.905114),(8,-8.101066,-34.886765),
 (24,-8.107611,-34.920256),(25,-8.114288,-34.921465),(29,-8.081768,-34.942253),(31,-8.083085,-34.941671),
 (37,-8.105179,-34.927549),(32,-8.082658,-34.932934),(45,-8.100538,-34.929092),(46,-8.087902,-34.937429),
 (48,-8.078672,-34.931815),(9,-8.103376,-34.910673),(22,-8.140505,-34.927358),(36,-8.111915,-34.912386),
 (41,-8.098066,-34.888129),(51,-8.089423,-34.882717),(47,-8.062548,-34.932170),(19,-8.089716,-34.888275),
 (33,-8.113526,-34.939007),(34,-8.107493,-34.929853),(35,-8.110391,-34.936870),(54,-8.113869,-34.940702)]
HOSP = re.compile(r"hospital|\bupa\b|pronto[- ]atendimento|maternidade", re.I)

tr = Transformer.from_crs(4326, 31985, always_xy=True).transform
txt = open(os.path.join(RAIZ, "appscript", "DadosEquipamentos.html"), encoding="utf-8").read()
dados = json.loads(re.search(r"var EQUIPAMENTOS = (\{.*\});", txt, re.S).group(1))
equip = [(Point(tr(i[0], i[1])), i[2], i[3], i[4]) for i in dados["itens"]]

def nota(n, hosp):
    if n >= 5 or hosp:
        return 5
    return {0: 1, 1: 2, 2: 3}.get(n, 4)

saida = os.path.join(RAIZ, "dados", "processados", "e2_equipamentos_300m.csv")
with open(saida, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ponto", "equipamentos_300m", "grupo1_dependem_de_outros", "grupo2_saude", "grupo3_apoio",
                "hospital_ou_upa", "nota_E2", "equipamentos"])
    for pid, lat, lon in PONTOS:
        c = Point(tr(lon, lat))
        dentro = [e for e in equip if e[0].distance(c) <= 300]
        hosp = any(HOSP.search(e[2] + " " + e[3]) for e in dentro)
        g = [sum(1 for e in dentro if e[1] == k) for k in (1, 2, 3)]
        w.writerow([pid, len(dentro), *g, "sim" if hosp else "não", nota(len(dentro), hosp),
                    "; ".join("%s (%s)" % (e[3], e[2]) for e in dentro)])
        print(f"{pid:>3}  {len(dentro):>2} equipamentos  {g}  {'hospital/UPA' if hosp else ''}  nota {nota(len(dentro), hosp)}")
print("gravado:", os.path.normpath(saida))
