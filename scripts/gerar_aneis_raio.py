#!/usr/bin/env python3
"""Anéis concêntricos de 1 a 5 km em volta de pontos críticos escolhidos — Recife Resiliente.

Lê os pontos escolhidos por Pedro em 03/11/2026 (12, 36, 37, 32 e 47; lat/lon
da aba "Notas dos pontos"), projeta para SIRGAS 2000 / UTM 25S (EPSG:31985), desenha os círculos em metros nessa projeção e grava em WGS 84
(lon/lat), no mesmo formato de `buffer_1000m_rpa6.geojson`.

Saídas (em dados/processados/arcgis/):
- aneis_1a5km_selecao.geojson: anéis (0–1, 1–2, 2–3, 3–4 e 4–5 km), sem
  sobreposição dentro de um mesmo ponto; bom para simbolizar por faixa.
- circulos_1a5km_selecao.geojson: círculos completos de 1, 2, 3, 4 e 5 km
  (cada um contém os menores); bom para filtrar "até X km".

Para outra lista de pontos: --pontos <csv> --nome <sufixo>. O CSV precisa de
ponto_id, lat, lon (x e y em UTM são opcionais) e das colunas de atributos.
Para mudar os pontos, edite dados/processados/pontos_aneis_selecao.csv.

As 5 coordenadas são aproximadas e não foram conferidas em campo.

Requer: pip install shapely pyproj numpy
"""

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import shapely
from pyproj import Transformer
from shapely.geometry import Point, mapping

RAIOS_M = (1000, 2000, 3000, 4000, 5000)
_TRANSF = Transformer.from_crs("EPSG:31985", "EPSG:4326", always_xy=True)
_PARA_UTM = Transformer.from_crs("EPSG:4326", "EPSG:31985", always_xy=True)


def para_wgs84(geom):
    return shapely.transform(geom, lambda c: np.column_stack(_TRANSF.transform(c[:, 0], c[:, 1])))


def atributos(p):
    return {
        "ponto_id": int(p["ponto_id"]),
        "bairro": p["bairro"],
        "trecho": p["trecho"],
        "tipo": p["tipo"],
        "precisao": p["precisao_coordenada"],
        "verificada": p["coordenada_verificada"],
        "prior_emlurb": p["prioridade_emlurb"],
        "grupo": p["grupo_sobreposicao"],
        "lat": float(p["lat"]),
        "lon": float(p["lon"]),
    }


def arredondar(geom):
    return json.loads(json.dumps(mapping(geom)), parse_float=lambda v: round(float(v), 7))


def gerar(pontos, raios=RAIOS_M):
    aneis, circulos = [], []
    for p in pontos:
        if p.get("x") and p.get("y"):
            centro = Point(float(p["x"]), float(p["y"]))
        else:  # só lat/lon: projeta para UTM 25S
            centro = Point(*_PARA_UTM.transform(float(p["lon"]), float(p["lat"])))
        anterior = None
        for raio in raios:
            circulo = centro.buffer(raio, resolution=64)
            anel = circulo if anterior is None else circulo.difference(anterior)
            base = atributos(p)
            interno = 0 if anterior is None else raios[raios.index(raio) - 1]
            aneis.append({
                "type": "Feature",
                "properties": {**base, "raio_ini_m": interno, "raio_fim_m": raio,
                               "faixa": f"{interno // 1000}–{raio // 1000} km"},
                "geometry": arredondar(para_wgs84(anel)),
            })
            circulos.append({
                "type": "Feature",
                "properties": {**base, "raio_m": raio, "raio_km": raio // 1000},
                "geometry": arredondar(para_wgs84(circulo)),
            })
            anterior = circulo
    return aneis, circulos


def gravar(caminho, feicoes):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": feicoes}, f, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pontos", default="dados/processados/pontos_aneis_selecao.csv")
    ap.add_argument("--saida", default="dados/processados/arcgis")
    ap.add_argument("--nome", default="selecao", help="sufixo dos arquivos de saída")
    args = ap.parse_args()

    with open(args.pontos, encoding="utf-8") as f:
        pontos = list(csv.DictReader(f))
    aneis, circulos = gerar(pontos)
    saida = Path(args.saida)
    gravar(saida / f"aneis_1a5km_{args.nome}.geojson", aneis)
    gravar(saida / f"circulos_1a5km_{args.nome}.geojson", circulos)
    print(f"{len(pontos)} pontos × {len(RAIOS_M)} raios = {len(aneis)} feições em cada arquivo ({saida})")


if __name__ == "__main__":
    main()
