"""Tira os elementos de uma planta em PDF (vetor do CAD) e põe no mapa.

Feito para a implantação do Canal do Sanbra (PDF do ZWCAD sem
georreferenciamento), mas serve para outras pranchas: a configuração em JSON
diz qual pedaço da folha ler, a escala e que cor do desenho vira qual camada.

Passos:
1. Lê os desenhos do PDF dentro do recorte (PyMuPDF) e separa por cor.
2. Junta os polígonos de cada camada e simplifica.
3. Converte para metros da planta (escala da prancha).
4. Se houver pontos de controle (pontos da folha com lat/lon conhecidos),
   ajusta a planta ao terreno com uma transformação de semelhança (escala,
   rotação e deslocamento) em SIRGAS 2000 / UTM 25S e informa o erro de cada
   ponto em metros. Sem pontos de controle, grava só a prévia em metros da
   planta (sem posição no mapa).

Uso:
  python3 scripts/planta_pdf_para_geojson.py CONFIG.json [--saida PASTA]

Requer: pymupdf, shapely, pyproj, matplotlib.
"""
import argparse
import csv
import json
import math
from pathlib import Path

import pymupdf
from shapely.geometry import LineString, MultiPolygon, Polygon, mapping
from shapely.ops import transform, unary_union

POL_POR_PT = 25.4 / 72  # milímetros de papel por ponto do PDF


def cor(c):
    return tuple(round(v, 2) for v in c) if c else None


def mesma_cor(a, b, tol=0.02):
    return a is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def pontos_do_desenho(d, passos_curva=6, minimo=3):
    """Pontos de cada subcaminho do desenho (curvas de Bézier amostradas)."""
    partes, atual = [], []

    def fecha():
        if len(atual) >= minimo:
            partes.append(list(atual))
        atual.clear()

    for it in d["items"]:
        tipo = it[0]
        if tipo == "l":
            a, b = it[1], it[2]
            if atual and (abs(atual[-1][0] - a.x) > 0.01 or abs(atual[-1][1] - a.y) > 0.01):
                fecha()
            if not atual:
                atual.append((a.x, a.y))
            atual.append((b.x, b.y))
        elif tipo == "c":
            p0, p1, p2, p3 = it[1:5]
            if atual and (abs(atual[-1][0] - p0.x) > 0.01 or abs(atual[-1][1] - p0.y) > 0.01):
                fecha()
            if not atual:
                atual.append((p0.x, p0.y))
            for i in range(1, passos_curva + 1):
                t = i / passos_curva
                u = 1 - t
                atual.append((u**3 * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t**3 * p3.x,
                              u**3 * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t**3 * p3.y))
        elif tipo == "re":
            fecha()
            r = it[1]
            partes.append([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)])
        elif tipo == "qu":
            fecha()
            q = it[1]
            partes.append([(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y)])
    fecha()
    return partes


def ler_camadas(cfg):
    doc = pymupdf.open(cfg["pdf"])
    pg = doc[cfg.get("pagina", 0)]
    recorte = pymupdf.Rect(*cfg["recorte_pt"])
    # Entra o que toca o recorte; depois cada camada é cortada nele (o rio passa da borda da planta).
    desenhos = [d for d in pg.get_drawings() if recorte.intersects(d["rect"])]
    caixa = Polygon([(recorte.x0, recorte.y0), (recorte.x1, recorte.y0), (recorte.x1, recorte.y1), (recorte.x0, recorte.y1)])
    camadas = {}
    for cam in cfg["camadas"]:
        cores = cam["cor_pdf"] if isinstance(cam["cor_pdf"][0], list) else [cam["cor_pdf"]]
        campo = "fill" if cam.get("tipo_pdf", "f") == "f" else "color"
        pols = []
        for d in desenhos:
            if not any(mesma_cor(cor(d.get(campo)), tuple(c)) for c in cores):
                continue
            for p in pontos_do_desenho(d, minimo=2):
                g = Polygon(p).buffer(0) if len(p) >= 3 else None
                if g is None or g.is_empty or g.area == 0:
                    # Traço sem área (linha do CAD): vira uma faixa fina, para entrar na união.
                    g = LineString(p).buffer(0.25)
                pols.append(g)
        geom = unary_union(pols) if pols else None
        f = cam.get("fechar_pt", 0)
        if geom is not None and cam.get("envoltoria"):
            # Linha fechada (ex.: limite tracejado) → a área que ela cerca. Engorda para emendar
            # os traços, pega o contorno de fora da maior peça e volta ao tamanho.
            g = geom.buffer(f) if f else geom
            partes = g.geoms if hasattr(g, "geoms") else [g]
            geom = Polygon(max(partes, key=lambda x: x.area).exterior)
            if f:
                geom = geom.buffer(-f)
        elif geom is not None and f:
            # Junta pedaços quase encostados (emendas do CAD).
            geom = geom.buffer(f).buffer(-f)
        if geom is not None:
            geom = geom.intersection(caixa).simplify(cfg.get("simplificar_pt", 0.15))
        camadas[cam["id"]] = geom
        print(f"  {cam['id']}: {len(pols)} pedaços → área {0 if geom is None else round(geom.area)} pt²")
    # Camadas marcadas com "so_no_limite" ficam só dentro da camada-limite (com folga): tira o que
    # é da base cadastral ou das caixas de rótulo em volta da intervenção.
    lim = camadas.get(cfg.get("camada_limite"))
    if lim is not None:
        # O limite vem como traços (pode ser aberto na beira do rio): engorda até fechar,
        # pega a área de dentro e desconta, deixando a folga.
        F = cfg.get("fechar_limite_pt", 12)
        g = lim.buffer(F)
        partes = g.geoms if hasattr(g, "geoms") else [g]
        area = Polygon(max(partes, key=lambda x: x.area).exterior).buffer(-F + cfg.get("folga_limite_pt", 3))
        for cam in cfg["camadas"]:
            if cam.get("so_no_limite") and camadas.get(cam["id"]) is not None:
                camadas[cam["id"]] = camadas[cam["id"]].intersection(area)
    return camadas


def para_metros_planta(geom, escala):
    """Pontos do PDF (y para baixo) → metros da planta (y para cima)."""
    k = POL_POR_PT / 1000 * escala
    return transform(lambda x, y, z=None: (x * k, -y * k), geom)


def ajustar_semelhanca(origem, destino):
    """Mínimos quadrados de x' = a·x − b·y + c, y' = b·x + a·y + d."""
    n = len(origem)
    mx = sum(p[0] for p in origem) / n
    my = sum(p[1] for p in origem) / n
    Mx = sum(p[0] for p in destino) / n
    My = sum(p[1] for p in destino) / n
    sxx = sum((p[0] - mx) ** 2 + (p[1] - my) ** 2 for p in origem)
    a = sum((p[0] - mx) * (q[0] - Mx) + (p[1] - my) * (q[1] - My) for p, q in zip(origem, destino)) / sxx
    b = sum((p[0] - mx) * (q[1] - My) - (p[1] - my) * (q[0] - Mx) for p, q in zip(origem, destino)) / sxx
    c = Mx - a * mx + b * my
    d = My - b * mx - a * my
    return a, b, c, d


def ler_controle(caminho):
    with open(caminho, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("lat") and r.get("lon")]


def georreferenciar(camadas_m, cfg, controle):
    from pyproj import Transformer
    para_utm = Transformer.from_crs(4326, 31985, always_xy=True)
    para_geo = Transformer.from_crs(31985, 4326, always_xy=True)
    k = POL_POR_PT / 1000 * cfg["escala"]
    origem = [(float(r["x_pt"]) * k, -float(r["y_pt"]) * k) for r in controle]
    destino = [para_utm.transform(float(r["lon"]), float(r["lat"])) for r in controle]
    a, b, c, d = ajustar_semelhanca(origem, destino)
    escala_ajuste = math.hypot(a, b)
    rotacao = math.degrees(math.atan2(b, a))
    print(f"Ajuste: fator de escala {escala_ajuste:.4f} (1 = escala da prancha), rotação {rotacao:.2f}°")
    erros = []
    for r, p, q in zip(controle, origem, destino):
        x, y = a * p[0] - b * p[1] + c, b * p[0] + a * p[1] + d
        e = math.hypot(x - q[0], y - q[1])
        erros.append(e)
        print(f"  ponto {r['n']}: erro {e:.1f} m  ({r.get('descricao', '')})")
    if len(controle) > 2:
        print(f"  erro médio quadrático: {math.sqrt(sum(e * e for e in erros) / len(erros)):.1f} m")

    def f(x, y, z=None):
        X, Y = a * x - b * y + c, b * x + a * y + d
        return para_geo.transform(X, Y)
    return {k2: (transform(f, g) if g is not None else None) for k2, g in camadas_m.items()}, {
        "fator_escala": escala_ajuste, "rotacao_graus": rotacao,
        "erros_m": {r["n"]: round(e, 2) for r, e in zip(controle, erros)}}


def gravar_geojson(camadas, cfg, caminho, ajuste=None):
    feats = []
    for cam in cfg["camadas"]:
        g = camadas.get(cam["id"])
        if g is None or g.is_empty:
            continue
        if isinstance(g, Polygon):
            g = MultiPolygon([g])
        props = {k: cam[k] for k in ("id", "nome", "cor", "contorno", "espessura", "opacidade", "tracejado") if k in cam}
        props["fonte"] = cfg.get("fonte", "")
        feats.append({"type": "Feature", "properties": props, "geometry": mapping(g)})
    fc = {"type": "FeatureCollection", "name": cfg["nome"], "features": feats}
    if ajuste:
        fc["georreferenciamento"] = ajuste
    Path(caminho).write_text(json.dumps(fc, ensure_ascii=False), encoding="utf-8")


def previa(camadas_m, cfg, caminho):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    fig, ax = plt.subplots(figsize=(7, 14))
    for cam in cfg["camadas"]:
        g = camadas_m.get(cam["id"])
        if g is None or g.is_empty:
            continue
        for p in (g.geoms if hasattr(g, "geoms") else [g]):
            xs, ys = p.exterior.xy
            ax.fill(xs, ys, facecolor=cam.get("cor", "none"), alpha=cam.get("opacidade", 1),
                    edgecolor=cam.get("contorno", "none"), linewidth=cam.get("espessura", 0) * 0.75,
                    linestyle="--" if cam.get("tracejado") else "-")
            for furo in p.interiors:
                xs, ys = furo.xy
                ax.fill(xs, ys, facecolor="white")
    ax.legend(handles=[Patch(facecolor=c.get("cor", "none"), edgecolor=c.get("contorno", "none"), label=c["nome"])
                       for c in cfg["camadas"]], loc="lower left", fontsize=8, frameon=True)
    ax.set_aspect("equal")
    ax.set_title(cfg["nome"] + " — prévia (metros da planta)", fontsize=10)
    ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(caminho, dpi=110)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("config")
    ap.add_argument("--saida", default=".")
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    base = Path(args.config).parent
    cfg["pdf"] = str((base / cfg["pdf"]).resolve()) if not Path(cfg["pdf"]).is_absolute() else cfg["pdf"]
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)

    print("Lendo o PDF…")
    camadas = ler_camadas(cfg)
    camadas_m = {k: (para_metros_planta(g, cfg["escala"]) if g is not None else None) for k, g in camadas.items()}
    previa(camadas_m, cfg, saida / f"{cfg['id']}_previa.png")
    gravar_geojson(camadas_m, cfg, saida / f"{cfg['id']}_metros_planta.geojson")

    ctrl = base / cfg.get("pontos_controle", "pontos_controle.csv")
    controle = ler_controle(ctrl) if ctrl.exists() else []
    if len(controle) >= 2:
        geo, ajuste = georreferenciar(camadas_m, cfg, controle)
        gravar_geojson(geo, cfg, saida / f"{cfg['id']}.geojson", ajuste)
        print(f"Georreferenciado: {saida / (cfg['id'] + '.geojson')}")
    else:
        print(f"Sem pontos de controle com lat/lon em {ctrl}: gravei só a prévia em metros da planta.")


if __name__ == "__main__":
    main()
