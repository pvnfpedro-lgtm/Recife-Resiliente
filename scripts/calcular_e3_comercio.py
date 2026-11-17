"""E3 Comércio e serviços: densidade de comércio no círculo de 1 km de cada ponto (17/11/2026, decisão de Pedro).

Fonte: comércio e serviços do OpenStreetMap usados no mapa de calor do painel (appscript/DadosComercio.html,
04/11/2026; dado colaborativo, pode estar incompleto): varejo, alimentação, mercados e serviços.
Substitui a régua original do checklist (soma do IPTU não residencial em 1 km), por falta da base do IPTU.
Raio de 1 km (o mesmo da régua original). Nota por quintis entre os pontos (20% com menos = 1; 20% com mais = 5).

Uso: python3 scripts/calcular_e3_comercio.py
Saída: dados/processados/e3_comercio_1km.csv
"""
import csv, json, os, re
from shapely.geometry import Point, Polygon
from shapely.ops import transform
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
tr = Transformer.from_crs(4326, 31985, always_xy=True).transform


def quintis(valores, maior_e_pior=True):
    """Nota 1–5 por quintis entre os pontos; empates no mesmo grupo."""
    ordem = sorted(valores) if maior_e_pior else sorted(valores, reverse=True)
    return lambda v: min(5, 1 + (ordem.index(v) * 5) // len(ordem))
from shapely.strtree import STRtree

txt = open(os.path.join(RAIZ, "appscript", "DadosComercio.html"), encoding="utf-8").read()
dados = json.loads(re.search(r"var COMERCIO = (\{.*\});", txt, re.S).group(1))
pts = [Point(tr(p[0], p[1])) for p in dados["pontos"]]
cat = [dados["categorias"][p[2]] for p in dados["pontos"]]
arvore = STRtree(pts)

res = []
for pid, lat, lon in PONTOS:
    c = Point(tr(lon, lat))
    idx = [i for i in arvore.query(c.buffer(1000)) if pts[i].distance(c) <= 1000]
    res.append((pid, len(idx), [sum(1 for i in idx if cat[i] == k) for k in dados["categorias"]]))
nota = quintis([r[1] for r in res])

saida = os.path.join(RAIZ, "dados", "processados", "e3_comercio_1km.csv")
with open(saida, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ponto", "estabelecimentos_1km", *dados["categorias"], "nota_E3"])
    for pid, n, por_cat in res:
        w.writerow([pid, n, *por_cat, nota(n)])
        print(f"{pid:>3}  {n:>4} estabelecimentos  nota {nota(n)}")
print("gravado:", os.path.normpath(saida))
