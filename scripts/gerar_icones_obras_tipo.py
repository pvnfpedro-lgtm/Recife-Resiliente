"""Gera os ícones das obras por tipo para o mapa (SVG + PNG 64 e 128 px).

Estilo C (docs/09-identidade-visual-mapa.md): o hexágono é a forma do grupo
Obras; o desenho de dentro mostra o tipo de obra. A situação aparece sem cor:
hexágono cheio (grafite, desenho branco) para em obra, concluído ou sem
informação; hexágono vazado (branco, borda e desenho grafite) para em
licitação. Desenhos numa grade de 15 px; canal, reservatório e galeria são
os mesmos do grupo Drenagem (scripts/gerar_icones_drenagem.py).

Categorias (aba "Obras", coluna tipo):
  canal          Canal; Perfilamento do Rio Tejipió
  dragagem       Dragagem
  reservatorio   Reservatórios de detenção; microrreservatório
  dique          Diques e comportas
  parque         Parques alagáveis
  rede           Requalificações na rede

Uso: python3 scripts/gerar_icones_obras_tipo.py   (requer cairosvg)
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "mapa" / "icones"
TAMANHOS = (64, 128)

GRAFITE = "#334155"
BRANCO = "#fff"
HEXAGONO = "16,2 28.1,9 28.1,23 16,30 3.9,23 3.9,9"


def onda(y):
    """Onda de 2 a 13 na altura y (três cristas)."""
    return f"M2 {y} q1.375 -1.6 2.75 0 t2.75 0 t2.75 0 t2.75 0"


def desenhos(c):
    """Desenhos na grade 15 x 15, na cor c."""
    def traco(w=1.6):
        return (f'fill="none" stroke="{c}" stroke-width="{w}" '
                'stroke-linecap="round" stroke-linejoin="round"')
    return {
        # Canal: três ondas.
        "canal": f'<path d="{onda(4)} {onda(7.5)} {onda(11)}" {traco()}/>',
        # Dragagem: braço e caçamba tirando o sedimento do fundo do rio
        # (lâmina d'água em cima, à esquerda).
        "dragagem": (
            f'<path d="M0.8 2.4 q1.1 -1.2 2.2 0 t2.2 0" {traco()}/>'
            f'<path d="M14 1 L9.6 5.6" {traco(1.8)}/>'
            f'<path d="M5 4.6 H11 L9.8 9.4 H6.2 Z" fill="{c}"/>'
            f'<path d="M0.5 14.5 Q7.5 9.6 14.5 14.5 Z" fill="{c}"/>'
        ),
        # Reservatório: bacia em corte com água.
        "reservatorio": (
            f'<path d="M1 2.5 L3.2 13 H11.8 L14 2.5" {traco()}/>'
            '<path d="M2.4 7.2 q1.275 -1.4 2.55 0 t2.55 0 t2.55 0 t2.55 0 '
            f'L11.4 12 H3.6 Z" fill="{c}"/>'
        ),
        # Dique: aterro em trapézio; água alta de um lado e baixa do outro.
        "dique": (
            f'<path d="M3.6 13.5 L6.3 3.5 H8.7 L11.4 13.5 Z" fill="{c}"/>'
            f'<path d="M0.6 6.5 q0.75 -1 1.5 0 t1.5 0 M0.6 9.5 q0.75 -1 1.5 0 t1.5 0" {traco(1.3)}/>'
            f'<path d="M11.8 11 q0.7 -1 1.4 0 t1.4 0" {traco(1.3)}/>'
            f'<path d="M0.5 13.8 H14.5" {traco()}/>'
        ),
        # Parque alagável: árvore e água no chão.
        "parque": (
            f'<circle cx="7.5" cy="4.6" r="3.9" fill="{c}"/>'
            f'<path d="M7.5 7.5 V10.4" {traco(1.8)}/>'
            f'<path d="{onda(13.2)}" {traco()}/>'
        ),
        # Requalificação de rede: galeria (terreno e tubo em corte com água).
        "rede": (
            f'<path d="M0.5 1.5 H14.5" {traco()}/>'
            f'<circle cx="7.5" cy="9" r="5" {traco()}/>'
            f'<path d="M3.6 10 H11.4 A3.9 3.9 0 0 1 3.6 10 Z" fill="{c}"/>'
        ),
    }


def svg(cheio, desenho):
    if cheio:
        fundo = (f'<polygon points="{HEXAGONO}" fill="{GRAFITE}" stroke="{BRANCO}" '
                 'stroke-width="2" stroke-linejoin="round"/>')
    else:
        fundo = (f'<polygon points="{HEXAGONO}" fill="{BRANCO}" stroke="{GRAFITE}" '
                 'stroke-width="2" stroke-linejoin="round"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            f'{fundo}<g transform="translate(8.5,8.5)">{desenho}</g></svg>\n')


def icones():
    """{nome do arquivo: texto SVG} — cheio e vazado (em licitação) por tipo."""
    cheios, vazados = desenhos(BRANCO), desenhos(GRAFITE)
    saida = {}
    for tipo in cheios:
        saida[f"obra_{tipo}"] = svg(True, cheios[tipo])
        saida[f"obra_{tipo}_licitacao"] = svg(False, vazados[tipo])
    return saida


def main():
    import cairosvg

    (PASTA / "png").mkdir(parents=True, exist_ok=True)
    for nome, texto in icones().items():
        (PASTA / f"{nome}.svg").write_text(texto, encoding="utf-8")
        for t in TAMANHOS:
            cairosvg.svg2png(bytestring=texto.encode("utf-8"),
                             write_to=str(PASTA / "png" / f"{nome}_{t}.png"),
                             output_width=t, output_height=t)
        print(nome)


if __name__ == "__main__":
    main()
