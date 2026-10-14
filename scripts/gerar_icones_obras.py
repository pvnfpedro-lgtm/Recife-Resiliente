"""Gera os ícones do grupo Obras para o mapa (SVG + PNG 64 e 128 px).

Estilo C (docs/09-identidade-visual-mapa.md): o grupo é reconhecido pela
forma (hexágono) e a situação da obra sem usar cor, para não competir com o
risco. Situações iguais às do painel: Em obra, Em licitação, Concluído.
Desenhos próprios, numa grade de 15 px.

Uso: python3 scripts/gerar_icones_obras.py   (requer cairosvg)
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "mapa" / "icones"
TAMANHOS = (64, 128)

GRAFITE = "#334155"
BRANCO = "#fff"
HEXAGONO = "16,2 28.1,9 28.1,23 16,30 3.9,23 3.9,9"


def fundo(cheio):
    if cheio:
        return (f'<polygon points="{HEXAGONO}" fill="{GRAFITE}" stroke="{BRANCO}" '
                'stroke-width="2" stroke-linejoin="round"/>')
    return (f'<polygon points="{HEXAGONO}" fill="{BRANCO}" stroke="{GRAFITE}" '
            'stroke-width="2" stroke-linejoin="round"/>')


def cone(cor):
    """Cone de obra em três faixas, com base."""
    def x(y):  # borda esquerda do cone na altura y (topo 6.5, base 3)
        return 6.5 - (y - 1.5) * 3.5 / 11

    faixas = ((1.5, 4.3), (5.8, 8.5), (10, 12.5))
    partes = []
    for y0, y1 in faixas:
        a, b = x(y0), x(y1)
        partes.append(f'<path d="M{a:.2f} {y0} H{15 - a:.2f} L{15 - b:.2f} {y1} '
                      f'H{b:.2f} Z" fill="{cor}"/>')
    partes.append(f'<rect x="1" y="12.5" width="13" height="1.8" rx="0.6" fill="{cor}"/>')
    return "".join(partes)


VISTO = (f'<path d="M2 8 L5.8 11.8 L13 3.6" fill="none" stroke="{BRANCO}" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')

ICONES = {
    "obra_em_obra": (True, cone(BRANCO)),
    "obra_em_licitacao": (False, cone(GRAFITE)),
    "obra_concluida": (True, VISTO),
}


def svg(cheio, desenho):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            f'{fundo(cheio)}<g transform="translate(8.5,8.5)">{desenho}</g></svg>\n')


def main():
    import cairosvg

    (PASTA / "png").mkdir(parents=True, exist_ok=True)
    for nome, (cheio, desenho) in ICONES.items():
        texto = svg(cheio, desenho)
        (PASTA / f"{nome}.svg").write_text(texto, encoding="utf-8")
        for t in TAMANHOS:
            cairosvg.svg2png(bytestring=texto.encode("utf-8"),
                             write_to=str(PASTA / "png" / f"{nome}_{t}.png"),
                             output_width=t, output_height=t)
        print(nome)


if __name__ == "__main__":
    main()
