"""Gera os ícones do grupo Drenagem para o mapa (SVG + PNG 64 e 128 px).

Estilo C (docs/09-identidade-visual-mapa.md): quadrado arredondado em
grafite (#334155) com contorno branco e desenho branco. Os desenhos foram
feitos para este projeto (não existem na Maki/Temaki), numa grade de 15 px.

Uso: python3 scripts/gerar_icones_drenagem.py   (requer cairosvg)
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "mapa" / "icones"
TAMANHOS = (64, 128)

FUNDO = ('<rect x="3" y="3" width="26" height="26" rx="6" fill="#334155" '
         'stroke="#fff" stroke-width="2"/>')
TRACO = 'fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'


def onda(y):
    """Onda de 2 a 13 na altura y (três cristas)."""
    return f"M2 {y} q1.375 -1.6 2.75 0 t2.75 0 t2.75 0 t2.75 0"


# Desenhos na grade 15 x 15 (branco).
DESENHOS = {
    # Canal: três ondas.
    "drenagem_canal": f'<path d="{onda(4)} {onda(7.5)} {onda(11)}" {TRACO}/>',
    # Galeria: linha do terreno e tubo em corte, com água no fundo.
    "drenagem_galeria": (
        f'<path d="M0.5 1.5 H14.5" {TRACO}/>'
        f'<circle cx="7.5" cy="9" r="5" {TRACO}/>'
        '<path d="M3.6 10 H11.4 A3.9 3.9 0 0 1 3.6 10 Z" fill="#fff"/>'
    ),
    # Reservatório: bacia em corte com água.
    "drenagem_reservatorio": (
        f'<path d="M1 2.5 L3.2 13 H11.8 L14 2.5" {TRACO}/>'
        '<path d="M2.4 7.2 q1.275 -1.4 2.55 0 t2.55 0 t2.55 0 t2.55 0 '
        'L11.4 12 H3.6 Z" fill="#fff"/>'
    ),
    # Estação de bombeamento: símbolo de bomba (círculo com triângulo).
    "drenagem_bombeamento": (
        f'<circle cx="7.5" cy="7.5" r="6" {TRACO}/>'
        '<path d="M7.5 1.9 L12 10.5 H3 Z" fill="#fff"/>'
    ),
    # Comporta: porta com barra de içamento; água alta de um lado e baixa
    # do outro.
    "drenagem_comporta": (
        f'<path d="M3.5 1.5 H11.5 M7.5 1.5 V4" {TRACO}/>'
        '<rect x="6.3" y="4" width="2.4" height="10" rx="0.5" fill="#fff"/>'
        '<path d="M0.8 6.8 q1.125 -1.2 2.25 0 t2.25 0 V14 H0.8 Z" fill="#fff"/>'
        '<path d="M9.7 10.8 q1.125 -1.2 2.25 0 t2.25 0 V14 H9.7 Z" fill="#fff"/>'
    ),
}


def svg(desenho):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            f'{FUNDO}<g transform="translate(8,8) scale(1.0666666666666667)">'
            f'{desenho}</g></svg>\n')


def main():
    import cairosvg

    (PASTA / "png").mkdir(parents=True, exist_ok=True)
    for nome, desenho in DESENHOS.items():
        texto = svg(desenho)
        (PASTA / f"{nome}.svg").write_text(texto, encoding="utf-8")
        for t in TAMANHOS:
            cairosvg.svg2png(bytestring=texto.encode("utf-8"),
                             write_to=str(PASTA / "png" / f"{nome}_{t}.png"),
                             output_width=t, output_height=t)
        print(nome)


if __name__ == "__main__":
    main()
