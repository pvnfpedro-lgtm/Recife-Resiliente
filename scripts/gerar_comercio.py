#!/usr/bin/env python3
"""Comércio e serviços do Recife (OpenStreetMap) para o mapa de calor — Recife Resiliente.

Lê o GeoJSON exportado do Overpass Turbo (consulta em docs/03-fontes-de-dados.md,
seção "Comércio e serviços"), limpa e grava:
- dados/shapefiles/comercio/comercio_osm.shp: um ponto por estabelecimento, em
  SIRGAS 2000 / UTM 25S (EPSG:31985), com nome, categoria e etiqueta do OSM;
- appscript/DadosComercio.html: os mesmos pontos (lon, lat, categoria) para o
  mapa de calor do painel (JsPontosCriticos.html).

Limpeza:
- sai o que não é comércio em funcionamento: loja vazia ou desativada
  (shop=vacant, disused:*, abandoned:*), hospital, nome com "abandonad", e
  prédio marcado só como building=commercial sem loja ou serviço (em geral
  escritórios);
- a mesma coisa mapeada duas vezes (mesmo nome a menos de 50 m, ou sem nome a
  menos de 5 m) vira uma só.

Categorias: varejo (lojas), alimentacao (restaurantes, bares, lanchonetes),
mercados (supermercados, mercados públicos, shoppings, lojas de departamento) e
servicos (bancos, farmácias, postos de combustível).

Dado colaborativo: não é cadastro oficial e pode estar incompleto,
principalmente nos bairros periféricos. Não substitui o IPTU não residencial do E3.

Requer: pip install shapely pyproj pyshp
Uso:    python3 scripts/gerar_comercio.py --geojson dados/brutos/osm/<arquivo>.geojson --data AAAA-MM-DD
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path

import shapefile
from pyproj import Transformer

RAIZ = Path(__file__).resolve().parent.parent
PARA_UTM = Transformer.from_crs("EPSG:4326", "EPSG:31985", always_xy=True)
PRJ_31985 = ('PROJCS["SIRGAS_2000_UTM_Zone_25S",GEOGCS["GCS_SIRGAS_2000",DATUM["D_SIRGAS_2000",'
             'SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],'
             'UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],'
             'PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],'
             'PARAMETER["Central_Meridian",-33.0],PARAMETER["Scale_Factor",0.9996],'
             'PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]')

CATEGORIAS = ["varejo", "alimentacao", "mercados", "servicos"]
ALIMENTACAO = {"restaurant", "cafe", "fast_food", "bar", "pub", "ice_cream", "food_court"}
SERVICOS = {"bank", "pharmacy", "fuel"}
MERCADOS_SHOP = {"supermarket", "mall", "department_store", "wholesale"}


def categoria(p):
    """Categoria do estabelecimento, ou None se não for comércio em funcionamento."""
    if p.get("shop") in ("vacant", "no", "disused", "none") or p.get("amenity") == "hospital":
        return None
    if any(k.startswith(("disused:", "abandoned:", "was:")) for k in p):
        return None
    if re.search(r"abandonad", p.get("name", ""), re.I):
        return None
    a, s = p.get("amenity"), p.get("shop")
    if a in ALIMENTACAO:
        return "alimentacao"
    if a in SERVICOS:
        return "servicos"
    if a == "marketplace" or s in MERCADOS_SHOP:
        return "mercados"
    if s:
        return "varejo"
    if p.get("building") == "retail":
        return "varejo"
    return None   # building=commercial sem loja: escritório


def etiqueta(p):
    for k in ("shop", "amenity", "building"):
        if k in p:
            return f"{k}={p[k]}"
    return ""


def chave(nome):
    s = unicodedata.normalize("NFD", nome or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def processar(feicoes):
    itens, fora = [], 0
    for f in feicoes:
        p = {k: v for k, v in f["properties"].items() if not k.startswith("@")}
        cat = categoria(p)
        if cat is None or f["geometry"]["type"] != "Point":
            fora += 1
            continue
        lon, lat = f["geometry"]["coordinates"][:2]
        x, y = PARA_UTM.transform(lon, lat)
        itens.append({"osm_id": f.get("id") or f["properties"].get("@id", ""), "nome": p.get("name", ""),
                      "categoria": cat, "etiqueta": etiqueta(p), "lon": lon, "lat": lat, "x": x, "y": y,
                      "n": len(p)})
    # Duplicatas: grade de 50 m para achar vizinhos rápido.
    itens.sort(key=lambda i: (not i["nome"], -i["n"]))
    grade, ficam = {}, []
    for it in itens:
        cx, cy, k = int(it["x"] // 50), int(it["y"] // 50), chave(it["nome"])
        viz = [o for dx in (-1, 0, 1) for dy in (-1, 0, 1) for o in grade.get((cx + dx, cy + dy), [])]
        d2 = lambda o: (o["x"] - it["x"]) ** 2 + (o["y"] - it["y"]) ** 2
        if any((k and k == chave(o["nome"]) and d2(o) < 50 ** 2) or (not k and d2(o) < 5 ** 2) for o in viz):
            continue
        grade.setdefault((cx, cy), []).append(it)
        ficam.append(it)
    return ficam, fora, len(itens) - len(ficam)


def gravar_shapefile(itens, pasta, data):
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / "comercio_osm"
    with shapefile.Writer(str(caminho), shapeType=shapefile.POINT, encoding="utf-8") as w:
        for nome, tam in (("osm_id", 20), ("nome", 120), ("categoria", 12), ("etiqueta", 60),
                          ("fonte", 32), ("data", 10)):
            w.field(nome, "C", size=tam)
        for it in itens:
            w.point(it["x"], it["y"])
            w.record(it["osm_id"], it["nome"], it["categoria"], it["etiqueta"], "OpenStreetMap (Overpass Turbo)", data)
    Path(str(caminho) + ".prj").write_text(PRJ_31985)
    Path(str(caminho) + ".cpg").write_text("UTF-8")


def gravar_painel(itens, saida, data):
    pts = [[round(it["lon"], 5), round(it["lat"], 5), CATEGORIAS.index(it["categoria"])] for it in itens]
    texto = ("/* Comércio e serviços (OpenStreetMap, " + data + ") para o mapa de calor do painel\n"
             "   (JsPontosCriticos.html). Dado colaborativo, não conferido; pode estar incompleto.\n"
             "   Arquivo gerado por scripts/gerar_comercio.py: não editar à mão. */\n"
             "var COMERCIO = " + json.dumps({"data": data, "categorias": CATEGORIAS, "pontos": pts},
                                            separators=(",", ":")) + ";\n")
    saida.write_text(texto, encoding="utf-8")
    return len(texto)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--geojson", required=True, help="GeoJSON exportado do Overpass Turbo")
    ap.add_argument("--data", required=True, help="data da extração (AAAA-MM-DD)")
    ap.add_argument("--saida-shp", default=str(RAIZ / "dados" / "shapefiles" / "comercio"))
    ap.add_argument("--saida-painel", default=str(RAIZ / "appscript" / "DadosComercio.html"))
    args = ap.parse_args()
    with open(args.geojson, encoding="utf-8") as f:
        feicoes = json.load(f)["features"]
    itens, fora, dup = processar(feicoes)
    gravar_shapefile(itens, Path(args.saida_shp), args.data)
    tam = gravar_painel(itens, Path(args.saida_painel), args.data)
    por_cat = {c: sum(1 for i in itens if i["categoria"] == c) for c in CATEGORIAS}
    print(f"{len(feicoes)} feições lidas; {fora} fora (não comércio); {dup} duplicatas; {len(itens)} pontos")
    print("por categoria:", por_cat, f"| DadosComercio.html: {tam // 1024} KB")


if __name__ == "__main__":
    main()
