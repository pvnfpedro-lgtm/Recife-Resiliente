#!/usr/bin/env python3
"""Infraestrutura crítica do Recife em shapefile, a partir do OpenStreetMap — Recife Resiliente.

Baixa do OpenStreetMap (API Overpass), dentro do limite do município do Recife, um
shapefile por camada (lista em CAMADAS, abaixo), em SIRGAS 2000 / UTM 25S
(EPSG:31985), em dados/shapefiles/infra_critica/. Campos: osm_id, nome, tipo,
grupo, subtipo, operador, fonte, data. Polígonos de prédios viram um ponto
dentro do prédio nas camadas de pontos.

Grupos (lista aprovada por Pedro em 03/11/2026):
1. Resposta à emergência: bombeiros, SAMU, UPAs, Defesa Civil e COP, delegacias e PM.
2. Saúde e pessoas vulneráveis: hospitais, policlínicas e maternidades, ILPIs.
   Abrigos temporários NÃO estão aqui: quase não existem no OSM; virão da Defesa Civil.
3. Serviços essenciais: subestações, água e esgoto (Compesa), bombeamento da
   drenagem e comportas.
4. Mobilidade: metrô/VLT (linhas e estações), aeroporto, terminais de ônibus.

Dado colaborativo: não é cadastro oficial e pode estar incompleto. Conferir com
as fontes oficiais (CBMPE, SAMU, Defesa Civil, Compesa, Neoenergia, EMLURB, ESIG)
antes de usar no I4 (pendência 18).

Requer: pip install shapely pyproj pyshp requests
Uso:    python3 scripts/gerar_infra_critica.py [--saida dados/shapefiles/infra_critica]
"""

import argparse
import datetime as dt
import time
from pathlib import Path

import requests
import shapefile
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, Point, Polygon, mapping
from shapely.ops import linemerge, transform

OVERPASS = "https://overpass-api.de/api/interpreter"
AREA_RECIFE = 'area["boundary"="administrative"]["admin_level"="8"]["name"="Recife"]->.recife;'
PARA_UTM = Transformer.from_crs("EPSG:4326", "EPSG:31985", always_xy=True).transform
PRJ_31985 = ('PROJCS["SIRGAS_2000_UTM_Zone_25S",GEOGCS["GCS_SIRGAS_2000",DATUM["D_SIRGAS_2000",'
             'SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],'
             'UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],'
             'PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],'
             'PARAMETER["Central_Meridian",-33.0],PARAMETER["Scale_Factor",0.9996],'
             'PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]')

# nome do shapefile: (grupo, geometria, consulta Overpass)
CAMADAS = {
    # 1. Resposta à emergência
    "bombeiros": ("1 Emergência", "ponto", """
        nwr["amenity"="fire_station"](area.recife);"""),
    "samu": ("1 Emergência", "ponto", """
        nwr["emergency"="ambulance_station"](area.recife);
        nwr["name"~"SAMU",i](area.recife);"""),
    "upas": ("1 Emergência", "ponto", """
        nwr["name"~"(^UPA)|(Unidade de Pronto Atendimento)|(Pronto[- ]Atendimento)",i](area.recife);"""),
    "defesa_civil_cop": ("1 Emergência", "ponto", """
        nwr["name"~"Defesa Civil|COMDEC|Centro de Opera[çc][õo]es",i](area.recife);"""),
    "policia": ("1 Emergência", "ponto", """
        nwr["amenity"="police"](area.recife);"""),
    # 2. Saúde e pessoas vulneráveis
    "hospitais": ("2 Saúde", "ponto", """
        nwr["amenity"="hospital"](area.recife);
        nwr["healthcare"="hospital"](area.recife);"""),
    "policlinicas_maternidades": ("2 Saúde", "ponto", """
        nwr["amenity"~"^(clinic|hospital|doctors)$"]["name"~"Policl[ií]nica|Maternidade",i](area.recife);
        nwr["healthcare"~"^(clinic|hospital|centre)$"]["name"~"Policl[ií]nica|Maternidade",i](area.recife);"""),
    "ilpis": ("2 Saúde", "ponto", """
        nwr["social_facility"~"^(nursing_home|assisted_living|group_home)$"](area.recife);
        nwr["amenity"="nursing_home"](area.recife);
        nwr["social_facility:for"~"senior"](area.recife);"""),
    # 3. Serviços essenciais
    "subestacoes": ("3 Serviços", "ponto", """
        nwr["power"="substation"](area.recife);"""),
    "agua_esgoto": ("3 Serviços", "ponto", """
        nwr["man_made"~"^(water_works|wastewater_plant|water_tower|reservoir_covered)$"](area.recife);
        nwr["man_made"="pumping_station"]["substance"!~"rainwater|stormwater"](area.recife);"""),
    "drenagem_bombas_comportas": ("3 Serviços", "ponto", """
        nwr["man_made"="pumping_station"]["substance"~"rainwater|stormwater"](area.recife);
        nwr["waterway"~"^(sluice_gate|floodgate|lock_gate)$"](area.recife);
        nwr["flood_prone"]["man_made"="pumping_station"](area.recife);"""),
    # 4. Mobilidade
    "metro_linhas": ("4 Mobilidade", "linha", """
        relation["route"~"^(subway|light_rail|train)$"](area.recife);"""),
    "metro_estacoes": ("4 Mobilidade", "ponto", """
        nwr["railway"="station"](area.recife);
        nwr["public_transport"="station"]["train"="yes"](area.recife);
        nwr["public_transport"="station"]["subway"="yes"](area.recife);
        nwr["public_transport"="station"]["light_rail"="yes"](area.recife);"""),
    "aeroporto": ("4 Mobilidade", "poligono", """
        nwr["aeroway"="aerodrome"](area.recife);"""),
    "terminais_onibus": ("4 Mobilidade", "ponto", """
        nwr["amenity"="bus_station"](area.recife);
        nwr["public_transport"="station"]["bus"="yes"](area.recife);"""),
}


def baixar(corpo):
    q = f"[out:json][timeout:120];{AREA_RECIFE}({corpo});out tags geom;"
    r = requests.post(OVERPASS, data={"data": q}, timeout=180,
                      headers={"User-Agent": "recife-resiliente/1.0"})
    r.raise_for_status()
    return r.json()["elements"]


def geometria(el):
    if el["type"] == "node":
        return Point(el["lon"], el["lat"])
    if el["type"] == "way":
        pts = [(g["lon"], g["lat"]) for g in el["geometry"]]
        return Polygon(pts) if len(pts) > 3 and pts[0] == pts[-1] else LineString(pts)
    # relation: junta os trechos (ways) membros
    linhas = [LineString([(g["lon"], g["lat"]) for g in m["geometry"]])
              for m in el.get("members", []) if m["type"] == "way" and m.get("geometry")]
    if not linhas:
        return None
    juntas = linemerge(MultiLineString(linhas))
    if el.get("tags", {}).get("type") == "multipolygon" or el.get("tags", {}).get("aeroway"):
        return juntas.convex_hull if juntas.geom_type != "Polygon" else juntas
    return juntas


def subtipo(tags):
    for k in ("amenity", "healthcare", "emergency", "social_facility", "office", "power", "man_made",
              "waterway", "route", "railway", "public_transport", "aeroway"):
        if k in tags:
            return f"{k}={tags[k]}"
    return ""


def gravar(caminho, forma, feicoes, data):
    tipo = {"ponto": shapefile.POINT, "linha": shapefile.POLYLINE, "poligono": shapefile.POLYGON}[forma]
    with shapefile.Writer(str(caminho), shapeType=tipo, encoding="utf-8") as w:
        for nome, tam in (("osm_id", 20), ("nome", 120), ("tipo", 30), ("grupo", 20), ("subtipo", 40),
                          ("operador", 60), ("fonte", 40), ("data", 10)):
            w.field(nome, "C", size=tam)
        for f in feicoes:
            g = mapping(f["geom"])
            if forma == "ponto":
                w.point(*f["geom"].coords[0])
            elif forma == "linha":
                partes = [g["coordinates"]] if g["type"] == "LineString" else list(g["coordinates"])
                w.line([[list(c) for c in p] for p in partes])
            else:
                w.poly([[list(c) for c in anel] for anel in g["coordinates"]])
            w.record(f["osm_id"], f["nome"], f["tipo"], f["grupo"], f["subtipo"], f["operador"],
                     "OpenStreetMap (Overpass)", data)
    Path(str(caminho) + ".prj").write_text(PRJ_31985)
    Path(str(caminho) + ".cpg").write_text("UTF-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--saida", default="dados/shapefiles/infra_critica")
    args = ap.parse_args()
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    data = dt.date.today().isoformat()

    for nome, (grupo, forma, corpo) in CAMADAS.items():
        vistos, feicoes = set(), []
        for el in baixar(corpo):
            chave = f"{el['type']}/{el['id']}"
            if chave in vistos:
                continue
            vistos.add(chave)
            geom = geometria(el)
            if geom is None or geom.is_empty:
                continue
            if forma == "ponto" and geom.geom_type != "Point":
                geom = geom.representative_point() if geom.geom_type == "Polygon" else geom.centroid
            if forma == "linha" and geom.geom_type not in ("LineString", "MultiLineString"):
                continue
            if forma == "poligono" and geom.geom_type != "Polygon":
                continue
            tags = el.get("tags", {})
            feicoes.append({"geom": transform(PARA_UTM, geom), "osm_id": chave,
                            "nome": tags.get("name", ""), "tipo": nome, "grupo": grupo, "subtipo": subtipo(tags),
                            "operador": tags.get("operator", "")})
        gravar(saida / nome, forma, feicoes, data)
        print(f"{grupo} · {nome}: {len(feicoes)} feições")
        time.sleep(2)   # intervalo entre consultas, para não sobrecarregar a API pública


if __name__ == "__main__":
    main()
