"""Grava as pranchas de projeto georreferenciadas como dados do painel.

Lê dados/processados/projetos/*.geojson (os de scripts/planta_pdf_para_geojson.py,
menos os "_metros_planta", que não têm posição) e escreve
appscript/DadosProjetos.html com a variável PROJETOS_PRANCHAS, que o painel
desenha como um grupo de camadas por prancha (JsPontosCriticos.html).

Para o arquivo ficar leve, simplifica cada camada em metros (UTM 25S) e
arredonda as coordenadas em 6 casas (cerca de 10 cm). Os anéis saem no sentido
que o ArcGIS espera: contorno externo no sentido horário, furos no anti-horário.

Uso: python3 scripts/gerar_projetos_painel.py [--tolerancia 0.3]
Requer: shapely, pyproj.
"""
import argparse
import json
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import shape
from shapely.geometry.polygon import orient
from shapely.ops import transform

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "processados" / "projetos"
SAIDA = RAIZ / "appscript" / "DadosProjetos.html"


def aneis(geom):
    """Lista de polígonos; cada um é a lista de anéis [[lon, lat], ...]."""
    out = []
    for p in (geom.geoms if hasattr(geom, "geoms") else [geom]):
        if p.is_empty:
            continue
        p = orient(p, sign=-1.0)  # externo horário
        out.append([[[round(x, 6), round(y, 6)] for x, y in r.coords] for r in [p.exterior, *p.interiors]])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tolerancia", type=float, default=0.3, help="simplificação em metros")
    args = ap.parse_args()
    para_utm = Transformer.from_crs(4326, 31985, always_xy=True).transform
    para_geo = Transformer.from_crs(31985, 4326, always_xy=True).transform

    pranchas = []
    for arq in sorted(ENTRADA.glob("*.geojson")):
        if arq.stem.endswith("_metros_planta"):
            continue
        fc = json.loads(arq.read_text(encoding="utf-8"))
        camadas = []
        for f in fc["features"]:
            pr = f["properties"]
            g = transform(para_utm, shape(f["geometry"])).simplify(args.tolerancia)
            g = transform(para_geo, g)
            camadas.append({k: pr[k] for k in ("id", "nome", "cor", "contorno", "espessura", "opacidade") if k in pr}
                           | {"poligonos": aneis(g)})
        pranchas.append({"id": arq.stem, "nome": fc["name"], "fonte": camadas and fc["features"][0]["properties"].get("fonte", ""),
                         "camadas": camadas})
        print(f"{arq.name}: {len(camadas)} camadas")

    js = json.dumps(pranchas, ensure_ascii=False, separators=(",", ":"))
    SAIDA.write_text(
        "/* Pranchas de projeto georreferenciadas, desenhadas pelo painel (JsPontosCriticos.html).\n"
        "   Arquivo gerado por scripts/gerar_projetos_painel.py: não editar à mão. */\n"
        "var PROJETOS_PRANCHAS = " + js + ";\n", encoding="utf-8")
    print(f"{SAIDA.relative_to(RAIZ)}: {SAIDA.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
