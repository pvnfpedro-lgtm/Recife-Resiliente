#!/usr/bin/env python3
"""Área de CIS no círculo de 300 m de cada ponto crítico — Recife Resiliente.

Lê os limites das Comunidades de Interesse Social (ESIG, camada
ATLAS/Ser_Camada_CIS, id 1, exportada em 04/10/2026) e os 21 pontos da RPA 6,
e grava, para cada ponto, a área de CIS dentro do círculo de 300 m, a
porcentagem do círculo e as CIS que tocam o círculo.

Ainda não é variável do modelo (V6 ou plano B do V1: a decidir). As
coordenadas de 11 pontos são aproximadas.

Requer: pip install pyshp shapely
"""

import argparse
import csv

import shapefile
from shapely.geometry import Point, shape
from shapely.ops import unary_union
from shapely.validation import make_valid

RAIO_M = 300


def ler_cis(caminho):
    leitor = shapefile.Reader(caminho, encoding="utf-8")
    cis = []
    for item in leitor.iterShapeRecords():
        geom = shape(item.shape.__geo_interface__)
        if not geom.is_valid:
            geom = make_valid(geom)
        cis.append((item.record["INDICADORE"], geom))
    return cis


def calcular(cis, pontos):
    uniao = unary_union([g for _, g in cis])
    linhas = []
    for p in pontos:
        circulo = Point(float(p["x"]), float(p["y"])).buffer(RAIO_M, resolution=64)
        area = circulo.intersection(uniao).area
        nomes = sorted({n for n, g in cis if g.intersects(circulo)})
        linhas.append({
            "ponto_id": p["ponto_id"],
            "bairro": p["bairro"],
            "precisao_coordenada": p["precisao_coordenada"],
            "area_cis_m2": round(area),
            "pct_circulo": round(area / circulo.area * 100, 1),
            "n_cis": len(nomes),
            "cis": "; ".join(nomes),
        })
    return linhas


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cis", default="dados/shapefiles/CIS/shp_CIS")
    ap.add_argument("--pontos", default="dados/processados/pontos_rpa6.csv")
    ap.add_argument("--saida", default="dados/processados/cis_buffer_300m.csv")
    args = ap.parse_args()

    with open(args.pontos, encoding="utf-8") as f:
        pontos = list(csv.DictReader(f))
    linhas = calcular(ler_cis(args.cis), pontos)
    with open(args.saida, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(f"{len(linhas)} pontos gravados em {args.saida}")


if __name__ == "__main__":
    main()
