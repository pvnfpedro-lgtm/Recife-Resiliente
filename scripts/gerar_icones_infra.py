"""Gera os ícones do grupo Infraestrutura crítica para o mapa (SVG + PNG 64 e 128 px).

Estilo C (docs/09-identidade-visual-mapa.md): octógono em grafite (#334155) com
contorno branco e desenho branco. Um ícone por camada de
dados/shapefiles/infra_critica/ (exceto metro_linhas, que é linha):

| Ícone                     | Camada            | Desenho                         |
|---------------------------|-------------------|---------------------------------|
| infra_hospital            | hospitais         | cruz (Maki "hospital")          |
| infra_subestacao          | subestacoes       | raio (Temaki "power")           |
| infra_metro_estacao       | metro_estacoes    | trem de metrô (Maki "rail-metro") |
| infra_terminal_onibus     | terminais_onibus  | ônibus (Maki "bus")             |
| infra_aeroporto           | aeroporto         | avião (Maki "airport")          |

Desenhos da Maki 8.2.0 e da Temaki 5.13.0, licença CC0 (domínio público),
numa grade de 15 px.

Uso: python3 scripts/gerar_icones_infra.py   (requer cairosvg)
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "mapa" / "icones"
TAMANHOS = (64, 128)

# Mesmo octógono do infra_aeroporto (16/10/2026).
FUNDO = ('<polygon points="30.04,21.82 21.82,30.04 10.18,30.04 1.96,21.82 1.96,10.18 '
         '10.18,1.96 21.82,1.96 30.04,10.18" fill="#334155" stroke="#fff" '
         'stroke-width="1.6" stroke-linejoin="round"/>')

# Desenhos na grade 15 x 15 (branco).
DESENHOS = {
    # Maki "hospital": cruz.
    "infra_hospital": (
        '<path d="M7,1C6.4,1,6,1.4,6,2v4H2C1.4,6,1,6.4,1,7v1c0,0.6,0.4,1,1,1h4v4c0,0.6,0.4,1,1,1h1'
        'c0.6,0,1-0.4,1-1V9h4c0.6,0,1-0.4,1-1V7c0-0.6-0.4-1-1-1H9V2c0-0.6-0.4-1-1-1H7z"/>'),
    # Temaki "power": raio.
    "infra_subestacao": (
        '<path d="M6 0L4 8L7 8L5 15L11 6L8 6L11 0Z"/>'),
    # Maki "rail-metro": trem de metrô de frente, sobre os trilhos.
    "infra_metro_estacao": (
        '<path d="M5.5,0c0,0-0.75,0-1,1L3,6.5V10c0,1,1,1,1,1h7c0,0,1,0,1-1V6.5L10.5,1c-0.2727-1-1-1-1-1H5.5z '
        'M6.5,1.5h2c0,0,0.5357,0,0.75,1L10,6c0.2146,1.0017-1,1-1,1H6c0,0-1.2146,0.0017-1-1l0.75-3.5'
        'C5.9643,1.5,6.5,1.5,6.5,1.5z M5,8c0.5523,0,1,0.4477,1,1s-0.4477,1-1,1S4,9.5523,4,9S4.4477,8,5,8z '
        'M6.75,8h1.5C8.3885,8,8.5,8.1115,8.5,8.25S8.3885,8.5,8.25,8.5h-1.5C6.6115,8.5,6.5,8.3885,6.5,8.25'
        'S6.6115,8,6.75,8z M10,8c0.5523,0,1,0.4477,1,1s-0.4477,1-1,1S9,9.5523,9,9S9.4477,8,10,8z '
        'M4.125,12L3,15h1.5l0.375-1h5.25l0.375,1H12l-1.125-3h-1.5l0.375,1h-4.5l0.375-1H4.125z"/>'),
    # Maki "bus": ônibus de frente.
    "infra_terminal_onibus": (
        '<path d="M2 3C2 1.9 2.9 1 4 1H11C12.1 1 13 1.9 13 3V11C13 12 12 12 12 12V13C12 13.55 11.55 14 '
        '11 14C10.45 14 10 13.55 10 13V12H5V13C5 13.55 4.55 14 4 14C3.45 14 3 13.55 3 13V12C2 12 2 11 2 '
        '11V3ZM3.5 4C3.22 4 3 4.22 3 4.5V7.5C3 7.78 3.22 8 3.5 8H11.5C11.78 8 12 7.78 12 7.5V4.5C12 4.22 '
        '11.78 4 11.5 4H3.5ZM4 9C3.45 9 3 9.45 3 10C3 10.55 3.45 11 4 11C4.55 11 5 10.55 5 10C5 9.45 4.55 '
        '9 4 9ZM11 9C10.45 9 10 9.45 10 10C10 10.55 10.45 11 11 11C11.55 11 12 10.55 12 10C12 9.45 11.55 9 '
        '11 9ZM4 2.5C4 2.78 4.22 3 4.5 3H10.5C10.78 3 11 2.78 11 2.5C11 2.22 10.78 2 10.5 2H4.5C4.22 2 4 '
        '2.22 4 2.5Z"/>'),
    # Maki "airport": avião (igual ao infra_aeroporto de 16/10/2026).
    "infra_aeroporto": (
        '<path d="M15 6.818V8.5l-6.5-1-.318 4.773L11 14v1l-3.5-.682L4 15v-1l2.818-1.727L6.5 7.5 0 8.5'
        'V6.818L6.5 4.5v-3s0-1.5 1-1.5 1 1.5 1 1.5v2.818l6.5 2.5z"/>'),
}


def svg(desenho):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            f'{FUNDO}<g transform="translate(7,7) scale(1.2)" fill="#fff">'
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
