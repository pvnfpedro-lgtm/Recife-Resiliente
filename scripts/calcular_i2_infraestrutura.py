"""I2 Infraestrutura crítica (aba "Notas dos pontos"; "I4" no checklist): distância do ponto até a
infraestrutura crítica mais próxima (17/11/2026, decisão de Pedro).

Fonte: camada do painel (appscript/DadosInfra.html, OpenStreetMap de 03/11/2026, não conferida):
estações de metrô, terminais de ônibus, subestações de energia e aeroporto. Hospitais ficam de fora
(o checklist põe hospital e UPA no E2, para não contar duas vezes). Distância em SIRGAS 2000 / UTM 25S;
o aeroporto conta pela borda do polígono.
Nota por quintis da distância (20% mais próximos = 5; 20% mais distantes = 1). A faixa fixa do checklist
(≤ 500 m = 5 ... > 2 km = 1) foi abandonada: dava 4 ou 5 aos 28 pontos (o mais distante fica a ~0,8 km).

Uso: python3 scripts/calcular_i2_infraestrutura.py
Saída: dados/processados/i2_infraestrutura_critica.csv
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
CAMADAS = ["metro_estacoes", "terminais_onibus", "subestacoes", "aeroporto"]
txt = open(os.path.join(RAIZ, "appscript", "DadosInfra.html"), encoding="utf-8").read()
camadas = json.loads(re.search(r"var INFRA_CAMADAS = (\[.*\]);", txt, re.S).group(1))
infra = []
for c in camadas:
    if c["id"] not in CAMADAS:
        continue
    for it in c["itens"]:
        if "pt" in it:
            g = Point(tr(*it["pt"]))
        elif "aneis" in it:
            g = transform(tr, Polygon(it["aneis"][0], it["aneis"][1:]))
        else:
            continue
        infra.append((g, c["tipo"], it.get("nome") or ""))

res = []
for pid, lat, lon in PONTOS:
    p = Point(tr(lon, lat))
    d, tipo, nome = min(((g.distance(p), t, n) for g, t, n in infra), key=lambda x: x[0])
    res.append((pid, round(d), tipo, nome))
nota = quintis([r[1] for r in res], maior_e_pior=False)   # mais perto = nota maior

saida = os.path.join(RAIZ, "dados", "processados", "i2_infraestrutura_critica.csv")
with open(saida, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ponto", "distancia_m", "tipo_mais_proximo", "nome", "nota_I2"])
    for pid, d, tipo, nome in res:
        w.writerow([pid, d, tipo, nome, nota(d)])
        print(f"{pid:>3}  {d:>5} m  {tipo:<22} nota {nota(d)}")
print("gravado:", os.path.normpath(saida))
