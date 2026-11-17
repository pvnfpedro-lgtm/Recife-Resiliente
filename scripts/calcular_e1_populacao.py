"""E1 População: moradores no círculo de 300 m de cada ponto crítico (17/11/2026, pedido de Pedro).

Rateio por área: cada setor censitário do Censo 2022 (appscript/DadosSetores.html, com a população) entra
com a fração da área dele que cai no círculo. Cálculo em SIRGAS 2000 / UTM 25S (EPSG:31985).
Nota: quintis entre os pontos (20% com menos moradores = 1; 20% com mais = 5; empates no mesmo grupo).
Coordenadas: aba "Notas dos pontos" da planilha em 17/11/2026 (aproximadas, não conferidas em campo).

Uso: python3 scripts/calcular_e1_populacao.py appscript/DadosSetores.html
Saída: dados/processados/e1_populacao_300m.csv
"""
import json, math, re, sys
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import transform, unary_union
from shapely.validation import make_valid
from pyproj import Transformer

SET = sys.argv[1]
pts = [  # id, lat, lon (planilha "Notas dos pontos", 17/11/2026)
 (5,-8.113732,-34.893163),(6,-8.111009,-34.891491),(7,-8.115380,-34.894176),(11,-8.111816,-34.894789),
 (12,-8.112935,-34.896796),(18,-8.138796,-34.913979),(26,-8.145055,-34.905114),(8,-8.101066,-34.886765),
 (24,-8.107611,-34.920256),(25,-8.114288,-34.921465),(29,-8.081768,-34.942253),(31,-8.083085,-34.941671),
 (37,-8.105179,-34.927549),(32,-8.082658,-34.932934),(45,-8.100538,-34.929092),(46,-8.087902,-34.937429),
 (48,-8.078672,-34.931815),(9,-8.103376,-34.910673),(22,-8.140505,-34.927358),(36,-8.111915,-34.912386),
 (41,-8.098066,-34.888129),(51,-8.089423,-34.882717),(47,-8.062548,-34.932170),(19,-8.089716,-34.888275),
 (33,-8.113526,-34.939007),(34,-8.107493,-34.929853),(35,-8.110391,-34.936870),(54,-8.113869,-34.940702)]
tr = Transformer.from_crs(4326, 31985, always_xy=True).transform
s = open(SET, encoding='utf-8').read()
dados = json.loads(re.search(r'var SETORES = (\{.*\});', s, re.S).group(1))
setores = []
for st in dados['setores']:
    aneis = st['g']
    g = Polygon(aneis[0], aneis[1:]) if aneis and isinstance(aneis[0][0], (list, tuple)) else None
    if g is None: continue
    g = make_valid(transform(tr, g))
    if g.area > 0: setores.append((st['c'], st['b'], st.get('p') or 0, g))
recife = unary_union([g for *_, g in setores])
print('setores:', len(setores), '| população total:', sum(p for _, _, p, _ in setores))
res = []
for pid, lat, lon in pts:
    c = Point(tr(lon, lat)).buffer(300, quad_segs=64)
    pop, n = 0.0, 0
    for cod, bai, p, g in setores:
        if not g.intersects(c): continue
        a = g.intersection(c).area
        if a > 0: pop += p * a / g.area; n += 1
    cob = recife.intersection(c).area / c.area
    res.append((pid, round(pop), n, cob))
# quintis entre os pontos: nota pelo grupo de 20% (empates no mesmo grupo)
vals = sorted(r[1] for r in res); N = len(vals)
def nota(v): return min(5, 1 + (vals.index(v) * 5) // N)
print('ponto  moradores_300m  setores  circulo_dentro_do_Recife  nota_E1')
for pid, pop, n, cob in sorted(res, key=lambda r: -r[1]):
    print(f'{pid:>5}  {pop:>14}  {n:>7}  {cob:>23.0%}  {nota(pop):>7}')
import csv, os
saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dados', 'processados', 'e1_populacao_300m.csv')
with open(saida, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['ponto', 'moradores_300m', 'setores_no_circulo', 'fracao_do_circulo_no_recife', 'nota_E1'])
    for pid, pop, n, cob in sorted(res, key=lambda r: r[0]):
        w.writerow([pid, pop, n, round(cob, 3), nota(pop)])
print('gravado:', os.path.normpath(saida))
