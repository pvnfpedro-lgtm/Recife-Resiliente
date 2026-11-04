#!/usr/bin/env python3
"""Infraestrutura crítica do Recife em shapefile, a partir do OpenStreetMap — Recife Resiliente.

Duas entradas possíveis:
- --geojson <arquivo>: GeoJSON exportado do Overpass Turbo (consulta em
  docs/03-fontes-de-dados.md, seção "Infraestrutura crítica");
- sem --geojson: baixa direto da API Overpass (precisa de overpass-api.de
  liberado na rede).

Cada feição é classificada numa camada (CAMADAS, por ordem de prioridade: a
primeira regra que bate vence), limpa e gravada em
dados/shapefiles/infra_critica/<camada>.shp, em SIRGAS 2000 / UTM 25S
(EPSG:31985). Campos: osm_id, nome, camada, grupo, subtipo, operador, fonte, data.

Limpeza:
- fica de fora o que veio junto sem ter sido pedido: estacionamentos, escolas,
  paradas de ônibus (stop_position, platform), terminais de barco, bicicletários
  e polígonos sem nenhuma etiqueta;
- nas camadas de pontos, prédios (polígonos) viram um ponto dentro do prédio, e
  a mesma coisa mapeada duas vezes (mesmo nome a menos de 200 m, ou sem nome a
  menos de 30 m) vira uma só, ficando a que tem mais etiquetas;
- metrô: as linhas e os dois sentidos viram uma feição só ("Metrô do Recife").

Camadas (escolha de Pedro, 03/11/2026): hospitais, subestações de energia, metrô
(a rede inteira numa feição só, sem separar as linhas) e estações de metrô, aeroporto
e terminais de ônibus. O VLT (linha e estações) fica de fora. Em "hospitais" não entram
UPA, UPAE nem policlínica, mesmo quando o OSM os marca como hospital; maternidades
marcadas como hospital entram.

Dado colaborativo: não é cadastro oficial e pode estar incompleto. Conferir com
as fontes oficiais antes de usar no I4 (pendência 18).

Requer: pip install shapely pyproj pyshp requests
Uso:    python3 scripts/gerar_infra_critica.py --geojson dados/brutos/osm/infra_critica_overpass.geojson
"""

import argparse
import datetime as dt
import json
import re
import unicodedata
from pathlib import Path

import shapefile
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, Point, Polygon, mapping, shape
from shapely.ops import linemerge, unary_union
import shapely
import numpy as np

OVERPASS = "https://overpass-api.de/api/interpreter"
_UTM = Transformer.from_crs("EPSG:4326", "EPSG:31985", always_xy=True)


def para_utm(geom):
    return shapely.transform(geom, lambda c: np.column_stack(_UTM.transform(c[:, 0], c[:, 1])))
PRJ_31985 = ('PROJCS["SIRGAS_2000_UTM_Zone_25S",GEOGCS["GCS_SIRGAS_2000",DATUM["D_SIRGAS_2000",'
             'SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],'
             'UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],'
             'PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],'
             'PARAMETER["Central_Meridian",-33.0],PARAMETER["Scale_Factor",0.9996],'
             'PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]')

# Mesma consulta do Overpass Turbo (docs/03-fontes-de-dados.md).
CONSULTA = """[out:json][timeout:180];
area["boundary"="administrative"]["admin_level"="8"]["name"="Recife"]->.recife;
(
  nwr["amenity"="hospital"](area.recife);
  nwr["healthcare"="hospital"](area.recife);
  nwr["power"="substation"](area.recife);
  relation["route"~"^(subway|light_rail|train)$"](area.recife);
  nwr["railway"="station"](area.recife);
  nwr["public_transport"="station"](area.recife);
  nwr["aeroway"="aerodrome"](area.recife);
  nwr["amenity"="bus_station"](area.recife);
);
out tags geom;"""


def t(tags, k):
    return str(tags.get(k, "")).lower()


def nome_tem(tags, padrao):
    return re.search(padrao, tags.get("name", ""), re.I) is not None


# (camada, grupo, geometria, regra) — a primeira regra que bate vence.
# Camadas escolhidas por Pedro em 03/11/2026 (as outras 9 saíram: SAMU, UPAs, bombeiros, polícia,
# Defesa Civil/COP, policlínicas e maternidades, ILPIs, água e esgoto, comportas).
NAO_HOSPITAL = r"^UPAE?\b|Unidade de Pronto Atendimento|Pronto[- ]Atendimento|Policl[ií]nica"
CAMADAS = [
    ("hospitais", "Saúde", "ponto",
     lambda g: (t(g, "amenity") == "hospital" or t(g, "healthcare") == "hospital")
     and not nome_tem(g, NAO_HOSPITAL)),   # UPA, UPAE e policlínica não são hospital
    ("subestacoes", "Energia", "ponto", lambda g: t(g, "power") == "substation"),
    # Só metrô (Pedro, 03/11/2026: não há estações de VLT a considerar). A linha e as estações do VLT saem.
    ("metro_linhas", "Mobilidade", "linha", lambda g: t(g, "route") == "subway"),
    ("metro_estacoes", "Mobilidade", "ponto",
     lambda g: (t(g, "railway") == "station" or (t(g, "public_transport") == "station" and any(
         t(g, m) == "yes" for m in ("train", "subway"))))
     and t(g, "station") != "light_rail" and t(g, "light_rail") != "yes"),
    ("aeroporto", "Mobilidade", "poligono", lambda g: t(g, "aeroway") == "aerodrome"),
    ("terminais_onibus", "Mobilidade", "ponto",
     lambda g: t(g, "amenity") == "bus_station"
     or (t(g, "public_transport") == "station" and t(g, "bus") == "yes")),
]


def fora(tags):
    """O que veio junto na consulta sem ter sido pedido."""
    return (t(tags, "amenity") in ("parking", "school", "bicycle_rental", "ferry_terminal")
            or t(tags, "public_transport") in ("stop_position", "platform")
            or not any(k for k in tags if not k.startswith("@") and k not in ("name", "type")))


def feicoes_do_geojson(caminho):
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    for ft in dados["features"]:
        tags = {k: v for k, v in ft["properties"].items() if not k.startswith("@")}
        yield ft.get("id") or ft["properties"].get("@id"), tags, shape(ft["geometry"])


def feicoes_da_api():
    import requests
    r = requests.post(OVERPASS, data={"data": CONSULTA}, timeout=240,
                      headers={"User-Agent": "recife-resiliente/1.0"})
    r.raise_for_status()
    for el in r.json()["elements"]:
        if el["type"] == "node":
            geom = Point(el["lon"], el["lat"])
        elif el["type"] == "way":
            pts = [(g["lon"], g["lat"]) for g in el["geometry"]]
            geom = Polygon(pts) if len(pts) > 3 and pts[0] == pts[-1] else LineString(pts)
        else:
            linhas = [LineString([(g["lon"], g["lat"]) for g in m["geometry"]])
                      for m in el.get("members", []) if m["type"] == "way" and m.get("geometry")]
            if not linhas:
                continue
            geom = linemerge(MultiLineString(linhas))
            if el.get("tags", {}).get("aeroway"):
                geom = geom.convex_hull
        yield f"{el['type']}/{el['id']}", el.get("tags", {}), geom


def subtipo(tags):
    for k in ("emergency", "amenity", "healthcare", "social_facility", "power", "man_made",
              "waterway", "route", "railway", "public_transport", "aeroway"):
        if k in tags:
            return f"{k}={tags[k]}"
    return ""


def chave_nome(nome):
    s = unicodedata.normalize("NFD", nome or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def limpar_pontos(lista):
    """Junta a mesma coisa mapeada duas vezes; fica a que tem mais etiquetas."""
    lista = sorted(lista, key=lambda f: (not f["nome"], -f["n_tags"]))   # com nome primeiro
    ficam = []
    for f in lista:
        k = chave_nome(f["nome"])
        dup = any((k and k == chave_nome(o["nome"]) and f["geom"].distance(o["geom"]) < 200)
                  or (not k and not o["nome"] and f["geom"].distance(o["geom"]) < 30)
                  # sem nome a menos de 150 m de um com nome: anexo do mesmo equipamento
                  or (not k and o["nome"] and f["geom"].distance(o["geom"]) < 150) for o in ficam)
        if not dup:
            ficam.append(f)
    return ficam


def limpar_linhas(lista):
    """Uma feição só para todo o metrô (Pedro, 03/11/2026: não precisa diferenciar as linhas).
    O OSM tem uma relação por linha e por sentido; os trechos são unidos."""
    if not lista:
        return []
    partes = []
    for f in lista:
        g = f["geom"]
        partes += [g] if g.geom_type == "LineString" else list(g.geoms)
    rede = unary_union(partes)
    rede = linemerge(rede) if rede.geom_type == "MultiLineString" else rede
    base = max(lista, key=lambda f: f["n_tags"])
    return [dict(base, geom=rede, nome="Metrô do Recife", osm_id=";".join(sorted(f["osm_id"] for f in lista))[:20],
                 subtipo="route=subway", operador=base["operador"] or "CBTU")]


def gravar(caminho, forma, feicoes, data, fonte):
    tipo = {"ponto": shapefile.POINT, "linha": shapefile.POLYLINE, "poligono": shapefile.POLYGON}[forma]
    with shapefile.Writer(str(caminho), shapeType=tipo, encoding="utf-8") as w:
        for nome, tam in (("osm_id", 20), ("nome", 120), ("camada", 30), ("grupo", 20),
                          ("subtipo", 40), ("operador", 80), ("fonte", 40), ("data", 10)):
            w.field(nome, "C", size=tam)
        for f in feicoes:
            g = mapping(f["geom"])
            if forma == "ponto":
                w.point(*f["geom"].coords[0])
            elif forma == "linha":
                partes = [g["coordinates"]] if g["type"] == "LineString" else list(g["coordinates"])
                w.line([[list(c) for c in p] for p in partes])
            else:
                poligonos = [g["coordinates"]] if g["type"] == "Polygon" else list(g["coordinates"])
                w.poly([[list(c) for c in anel] for pol in poligonos for anel in pol])
            w.record(f["osm_id"], f["nome"], f["camada"], f["grupo"], f["subtipo"], f["operador"],
                     fonte, data)
    Path(str(caminho) + ".prj").write_text(PRJ_31985)
    Path(str(caminho) + ".cpg").write_text("UTF-8")


def processar(feicoes):
    """Classifica e limpa. Devolve {camada: [feições]} e a lista do que ficou de fora."""
    por_camada = {c[0]: [] for c in CAMADAS}
    descartes = []
    for osm_id, tags, geom in feicoes:
        if geom is None or geom.is_empty or fora(tags):
            descartes.append((osm_id, tags.get("name", ""), subtipo(tags) or "sem etiqueta"))
            continue
        regra = next((c for c in CAMADAS if c[3](tags)), None)
        if regra is None:
            descartes.append((osm_id, tags.get("name", ""), subtipo(tags) or "sem camada"))
            continue
        camada, grupo, forma, _ = regra
        if forma == "ponto" and geom.geom_type != "Point":
            geom = geom.representative_point() if "Polygon" in geom.geom_type else geom.centroid
        if forma == "linha" and geom.geom_type not in ("LineString", "MultiLineString"):
            continue
        if forma == "poligono" and "Polygon" not in geom.geom_type:
            continue
        por_camada[camada].append({
            "geom": para_utm(geom), "osm_id": osm_id, "nome": tags.get("name", ""),
            "camada": camada, "grupo": grupo, "subtipo": subtipo(tags),
            "operador": tags.get("operator", ""), "n_tags": len(tags)})
    for camada, _, forma, _ in CAMADAS:
        if forma == "ponto":
            por_camada[camada] = limpar_pontos(por_camada[camada])
        elif forma == "linha":
            por_camada[camada] = limpar_linhas(por_camada[camada])
    return por_camada, descartes


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--geojson", help="GeoJSON exportado do Overpass Turbo")
    ap.add_argument("--data", help="data da extração (AAAA-MM-DD); padrão: hoje")
    ap.add_argument("--saida", default="dados/shapefiles/infra_critica")
    args = ap.parse_args()
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    data = args.data or dt.date.today().isoformat()
    fonte = "OpenStreetMap (Overpass Turbo)" if args.geojson else "OpenStreetMap (API Overpass)"

    entrada = feicoes_do_geojson(args.geojson) if args.geojson else feicoes_da_api()
    por_camada, descartes = processar(entrada)
    for camada, grupo, forma, _ in CAMADAS:
        gravar(saida / camada, forma, por_camada[camada], data, fonte)
        print(f"{grupo:13} {camada:27} {len(por_camada[camada]):4}")
    print(f"Fora das camadas: {len(descartes)}")


if __name__ == "__main__":
    main()
