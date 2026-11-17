"""Gera as regras do tema escuro do painel a partir do CSS claro (appscript/Estilos.html).

O painel tem centenas de cores escritas direto no CSS. Em vez de reescrever cada uma à mão, este script lê
cada declaração com cor e gera a mesma regra prefixada com :root[data-tema="escuro"], com a cor convertida:

- neutros (cinzas): fundos claros viram fundos escuros; textos escuros viram claros; bordas claras viram
  bordas escuras e bordas pretas viram cinza-claro. Fundos escuros (barra do topo) e textos claros ficam.
- cores (azul, verde, roxo...): textos escuros clareiam; fundos muito claros (pílulas) viram tons escuros
  da mesma cor; cores médias (botões, selos) ficam.
- branco translúcido dos painéis de vidro sobre o mapa vira grafite translúcido, um pouco mais opaco.

O resultado vai entre os marcadores TEMA-ESCURO-INICIO/FIM no fim do <style> de Estilos.html (substitui o
bloco anterior). Ajustes finos à mão ficam em appscript/Estilos.html, no bloco "Tema escuro: ajustes".

Uso: python3 scripts/gerar_tema_escuro.py
"""
import colorsys
import re
from pathlib import Path

ARQ = Path(__file__).resolve().parent.parent / "appscript" / "Estilos.html"
INICIO = "/* TEMA-ESCURO-INICIO (gerado por scripts/gerar_tema_escuro.py; não editar à mão) */"
FIM = "/* TEMA-ESCURO-FIM */"
AJUSTES = "/* TEMA-ESCURO-AJUSTES */"
PREFIXO = ':root[data-tema="escuro"]'

COR = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)")
VIDRO = (22, 27, 36)   # grafite dos painéis translúcidos no escuro


def ler_cor(t):
    if t.startswith("#"):
        h = t[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else None
        return r, g, b, a
    nums = [x.strip() for x in t[t.index("(") + 1:-1].replace("/", ",").split(",")]
    if len(nums) < 3 or not all(re.fullmatch(r"[\d.]+%?", n) for n in nums[:3]):
        return None   # rgb(var(--x)) e afins: não mexe
    r, g, b = (float(n[:-1]) * 2.55 if n.endswith("%") else float(n) for n in nums[:3])
    a = None
    if len(nums) > 3:
        a = float(nums[3][:-1]) / 100 if nums[3].endswith("%") else float(nums[3])
    return r, g, b, a


def escrever(r, g, b, a):
    r, g, b = (max(0, min(255, round(v))) for v in (r, g, b))
    if a is None:
        return "#%02x%02x%02x" % (r, g, b)
    return "rgba(%d,%d,%d,%s)" % (r, g, b, ("%.3f" % a).rstrip("0").rstrip("."))


def converter(t, papel):
    c = ler_cor(t)
    if c is None:
        return t
    r, g, b, a = c
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    # Cinza = pouca diferença entre os canais (os cinzas-ardósia do painel têm até ~0,17).
    croma = (max(r, g, b) - min(r, g, b)) / 255
    # Cinza = pouca diferença entre os canais; tons pastel (pílulas) têm croma maior e não entram.
    neutro = croma < 0.05 or (croma < 0.18 and s < 0.4)

    if papel == "sombra":
        if l > 0.8:   # brilho branco em sombra: vira sombra escura
            return escrever(0, 0, 0, (a if a is not None else 1) * 0.6)
        return escrever(r, g, b, min(1, (a if a is not None else 1) * 1.6)) if a is not None else t

    # Branco translúcido (painéis de vidro sobre o mapa)
    if a is not None and l > 0.9 and papel == "fundo":
        return escrever(*VIDRO, min(0.92, a + 0.35))
    if a is not None and l > 0.9 and papel == "linha":
        return escrever(255, 255, 255, a * 0.25)

    if neutro:
        if papel == "fundo":
            if l < 0.4:
                return t                      # fundos já escuros (barra do topo, dicas)
            # Branco (cartões, painéis) → 0,16; cinzas-claros de fundo ficam um pouco mais escuros que o
            # cartão, como no claro ficam um pouco mais escuros que o branco.
            nl = max(0.07, 0.16 - (1 - l) * 0.6)
        elif papel == "linha":
            nl = 0.6 if l < 0.35 else 0.12 + (1 - l) * 1.1
        else:   # texto
            if l >= 0.75:
                return t                      # texto claro (sobre botões e barras escuras)
            nl = 0.95 - l * 0.75
        # Cinzas com o mesmo leve tom azulado do painel claro (ardósia), seja qual for o cinza de origem.
        nr, ng, nb = colorsys.hls_to_rgb(0.6, nl, 0.16)
        return escrever(nr * 255, ng * 255, nb * 255, a)

    # Cores
    if papel == "texto":
        if l >= 0.55:
            return t
        nl, ns = max(0.68, l), min(s, 0.8)
    elif papel in ("fundo", "linha"):
        if l < 0.82:
            return t
        nl, ns = 0.2 if papel == "fundo" else 0.32, s * 0.55
    else:
        return t
    nr, ng, nb = colorsys.hls_to_rgb(h, nl, ns)
    return escrever(nr * 255, ng * 255, nb * 255, a)


def papel_de(prop):
    p = prop.strip().lower()
    if p.startswith("--"):
        return None   # variáveis: decididas pelo nome abaixo
    if "shadow" in p:
        return "sombra"
    if p.startswith("background") or p in ("fill",):
        return "fundo"
    if p.startswith("border") or p.startswith("outline") or p in ("stroke", "column-rule", "text-decoration-color"):
        return "linha"
    if p in ("color", "caret-color", "-webkit-text-fill-color", "accent-color"):
        return "texto"
    return None


def papel_da_variavel(nome):
    n = nome.lower()
    if any(k in n for k in ("shadow",)):
        return "sombra"
    if any(k in n for k in ("text", "dim", "faint", "-txt", "ink", "fg")):
        return "texto"
    if any(k in n for k in ("border", "line", "rule")):
        return "linha"
    if any(k in n for k in ("bg", "panel", "soft", "surface", "fundo")):
        return "fundo"
    if n in ("--bg",):
        return "fundo"
    return None   # cores de categoria (etapas, bacias, risco): não mudam


def converter_valor(valor, papel):
    return COR.sub(lambda m: converter(m.group(0), papel), valor)


def prefixar(seletores):
    saida = []
    for s in seletores.split(","):
        s = s.strip()
        if not s:
            continue
        if s.startswith(":root"):
            saida.append(PREFIXO + s[len(":root"):])
        elif s in ("html", "body") or s.startswith(("html ", "body ", "body.", "html.")):
            saida.append(PREFIXO + " " + s if not s.startswith("html") else PREFIXO + s[4:])
        else:
            saida.append(PREFIXO + " " + s)
    return ", ".join(saida)


def regras(css):
    """Percorre o CSS e devolve (contexto @media, seletores, corpo) para cada regra comum."""
    i, pilha, n = 0, [], len(css)
    css = re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.S)
    while i < n:
        j = css.find("{", i)
        k = css.find("}", i)
        if k != -1 and (j == -1 or k < j):
            if pilha:
                pilha.pop()
            i = k + 1
            continue
        if j == -1:
            break
        cab = css[i:j].strip()
        if cab.startswith("@media") or cab.startswith("@supports"):
            pilha.append(cab)
            i = j + 1
            continue
        if cab.startswith("@"):   # @keyframes, @font-face: pula o bloco inteiro
            prof, m = 1, j + 1
            while prof and m < n:
                prof += {"{": 1, "}": -1}.get(css[m], 0)
                m += 1
            i = m
            continue
        fim = css.find("}", j)
        yield tuple(pilha), cab, css[j + 1:fim]
        i = fim + 1


def gerar(css):
    blocos = {}
    for ctx, sel, corpo in regras(css):
        novas = []
        for decl in corpo.split(";"):
            if ":" not in decl:
                continue
            prop, valor = decl.split(":", 1)
            prop = prop.strip()
            if not COR.search(valor):
                continue
            papel = papel_da_variavel(prop) if prop.startswith("--") else papel_de(prop)
            if not papel:
                continue
            novo = converter_valor(valor.strip(), papel)
            if novo != valor.strip():
                novas.append("%s:%s" % (prop, novo))
        if novas:
            blocos.setdefault(ctx, []).append("%s{%s;}" % (prefixar(sel), ";".join(novas)))
    linhas = [INICIO]
    for ctx, rs in blocos.items():
        if ctx:
            linhas.append(" ".join(c + "{" for c in ctx))
        linhas.extend("  " + r for r in rs)
        if ctx:
            linhas.append("}" * len(ctx))
    linhas.append(FIM)
    return "\n".join(linhas)


def main():
    """Estilos.html: [CSS do painel] [bloco gerado] [ajustes à mão, após TEMA-ESCURO-AJUSTES] </style>."""
    txt = ARQ.read_text(encoding="utf-8")
    abre = txt.index("<style>") + len("<style>")
    fecha = txt.rindex("</style>")
    css = txt[abre:fecha]
    corte = [p for p in (css.find(INICIO), css.find(AJUSTES)) if p != -1]
    base = css[:min(corte)] if corte else css
    ajustes = css[css.index(AJUSTES):] if AJUSTES in css else ""
    bloco = gerar(base)
    novo_css = base.rstrip() + "\n\n" + bloco + "\n" + (ajustes.rstrip() + "\n" if ajustes else "")
    ARQ.write_text(txt[:abre] + novo_css + txt[fecha:], encoding="utf-8")
    print("regras geradas:", sum(1 for l in bloco.splitlines() if l.strip().startswith(PREFIXO)))


if __name__ == "__main__":
    main()
