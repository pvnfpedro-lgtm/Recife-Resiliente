"""Grava a infraestrutura crítica como dados do painel.

Lê os shapefiles de dados/shapefiles/infra_critica/ (gerados por
scripts/gerar_infra_critica.py, em UTM 25S), passa para WGS 84 e escreve
appscript/DadosInfra.html com a variável INFRA_CAMADAS, que o painel desenha
como o grupo "Infraestrutura crítica" (JsPontosCriticos.html). Os ícones vão
junto, em base64, a partir de mapa/icones/infra_*.svg.

A linha do metrô é simplificada em 5 m e as coordenadas são arredondadas em 6
casas (cerca de 10 cm), para o arquivo ficar leve.

Uso: python3 scripts/gerar_infra_painel.py
Requer: pyshp, shapely, pyproj.
"""
import base64
import json
from pathlib import Path

import shapefile
from pyproj import Transformer
from shapely.geometry import shape
from shapely.geometry.polygon import orient
from shapely.ops import transform

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "shapefiles" / "infra_critica"
ICONES = RAIZ / "mapa" / "icones"
SAIDA = RAIZ / "appscript" / "DadosInfra.html"
PARA_WGS84 = Transformer.from_crs("EPSG:31985", "EPSG:4326", always_xy=True).transform

# Ordem de desenho: a primeira fica por baixo. (camada, título no painel, ícone)
CAMADAS = [
    ("aeroporto", "Aeroporto", "infra_aeroporto"),
    ("metro_linhas", "Metrô", None),
    ("metro_estacoes", "Estações de metrô", "infra_metro_estacao"),
    ("terminais_onibus", "Terminais de ônibus", "infra_terminal_onibus"),
    ("subestacoes", "Subestações de energia", "infra_subestacao"),
    ("hospitais", "Hospitais", "infra_hospital"),
]


def r6(c):
    return [round(c[0], 6), round(c[1], 6)]


def ler(nome):
    leitor = shapefile.Reader(str(ENTRADA / nome), encoding="utf-8")
    for item in leitor.iterShapeRecords():
        yield shape(item.shape.__geo_interface__), item.record.as_dict()


def camada(nome, titulo, icone):
    itens = []
    for geom, rec in ler(nome):
        g = transform(PARA_WGS84, geom.simplify(5) if geom.geom_type != "Point" else geom)
        if g.geom_type == "Point":
            dado = {"pt": r6(g.coords[0])}
        elif "LineString" in g.geom_type:
            partes = [g] if g.geom_type == "LineString" else list(g.geoms)
            dado = {"linhas": [[r6(c) for c in p.coords] for p in partes]}
        else:
            pols = [g] if g.geom_type == "Polygon" else list(g.geoms)
            dado = {"aneis": [[r6(c) for c in orient(p, sign=-1.0).exterior.coords] for p in pols]}
        dado.update({"nome": rec["nome"], "operador": rec["operador"]})
        itens.append(dado)
    out = {"id": nome, "titulo": titulo, "itens": itens}
    if icone:
        svg = (ICONES / f"{icone}.svg").read_bytes()
        out["icone"] = "data:image/svg+xml;base64," + base64.b64encode(svg).decode()
    return out


def main():
    dados = [camada(*c) for c in CAMADAS]
    fonte = next(ler("hospitais"))[1]
    texto = ("/* Infraestrutura crítica (OpenStreetMap, " + fonte["data"] + "), desenhada pelo painel\n"
             "   (JsPontosCriticos.html). Dado colaborativo, não conferido.\n"
             "   Arquivo gerado por scripts/gerar_infra_painel.py: não editar à mão. */\n"
             "var INFRA_CAMADAS = " + json.dumps(dados, ensure_ascii=False, separators=(",", ":")) + ";\n")
    SAIDA.write_text(texto, encoding="utf-8")
    print(f"{SAIDA.relative_to(RAIZ)}: {len(texto) // 1024} KB, " +
          ", ".join(f"{d['id']} {len(d['itens'])}" for d in dados))


if __name__ == "__main__":
    main()
