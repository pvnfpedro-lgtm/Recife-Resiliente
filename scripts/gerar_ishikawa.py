"""Gera docs/img/ishikawa_painel.svg (Ishikawa: o que o painel de risco precisa).

Situação de cada item: d = decidido ou pronto, p = proposta/teste/parcial, f = falta.
Atualize a letra do item e rode de novo: python3 scripts/gerar_ishikawa.py
"""
from xml.sax.saxutils import escape as e
W, H, SY = 1720, 1000, 500
COR = {"d": ("#0869A6", "#0869A6", "#FFFFFF"), "p": ("#5496BF", "#5496BF", "#FFFFFF"), "f": ("#F2F2F2", "#5496BF", "#1F2A33")}
ESP = [
 ("Método (modelo)", True, 550, [("Critérios (4)", "d"), ("Fórmula P × C e índice 0–1", "d"), ("Subcritérios (13 + P6 e V1)", "p"), ("Escalas de nota 1–5", "p"), ("Pesos (de teste)", "p")]),
 ("Dados (fontes)", True, 960, [("Bases nacionais: IBGE, Ipea, MapBiomas", "f"), ("Bases municipais: portal e ESIG", "f"), ("7 links do portal localizados", "p"), ("Pedidos aos órgãos", "f")]),
 ("Território (base SIG)", True, 1370, [("EPSG:31985", "d"), ("Buffers de 300 m e 1 km", "p"), ("Coordenadas dos 21 pontos", "p"), ("Linha dos 12 trechos", "f")]),
 ("Pessoas e órgãos", False, 550, [("Equipe (6) e tutora", "d"), ("EMLURB: Pedro Oliveira", "f"), ("CTTU: Antônio", "f"), ("SEPLAN: contato em aberto", "f"), ("COP e Defesa Civil", "f")]),
 ("Ferramentas", False, 960, [("Script Python de cálculo", "d"), ("Planilha Google Sheets", "p"), ("Apps Script e clasp", "p"), ("ArcGIS Pro e ESIG", "f")]),
 ("Validação", False, 1370, [("Teste com pesos iguais", "f"), ("Conferência: EMLURB, Defesa Civil, COP", "f"), ("Vistoria de amostra", "f")]),
]
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Roboto, Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
     '<text x="40" y="52" font-size="26" font-weight="700" fill="#1F2A33">Recife Resiliente — o que o painel de risco precisa (RPA 6)</text>',
     '<text x="40" y="80" font-size="15" fill="#4A5763">Diagrama de Ishikawa · situação em 03/10/2026</text>',
     f'<line x1="40" y1="{SY}" x2="1410" y2="{SY}" stroke="#1F2A33" stroke-width="5"/>']
DX, DY = 190, 330
for nome, cima, ax, itens in ESP:
    s = -1 if cima else 1
    ty = SY + s * DY
    o.append(f'<line x1="{ax}" y1="{SY}" x2="{ax-DX}" y2="{ty}" stroke="#1F2A33" stroke-width="3"/>')
    ly = ty - 16 if cima else ty + 30
    o.append(f'<text x="{ax-DX}" y="{ly}" font-size="18" font-weight="700" fill="#0869A6" text-anchor="middle">{e(nome)}</text>')
    n = len(itens)
    for i, (txt, st) in enumerate(itens):
        d = 40 + i * (DY - 70) / max(n - 1, 1) if n > 1 else DY / 2
        d = DY - d  # primeiro item mais longe do eixo
        y = SY + s * (DY - d) if False else SY + s * d
        xr = ax - DX * d / DY
        bw, bh = 300, 34
        x0 = xr - 14 - bw
        f, b, t = COR[st]
        o.append(f'<line x1="{x0+bw}" y1="{y}" x2="{xr}" y2="{y}" stroke="#1F2A33" stroke-width="1.5"/>')
        o.append(f'<rect x="{x0}" y="{y-bh/2}" width="{bw}" height="{bh}" rx="6" fill="{f}" stroke="{b}" stroke-width="1.5"/>')
        o.append(f'<text x="{x0+bw/2}" y="{y+5}" font-size="14" fill="{t}" text-anchor="middle">{e(txt)}</text>')
# cabeça
o.append(f'<path d="M1410 {SY-80} L1660 {SY-80} Q1700 {SY} 1580 {SY+80} L1410 {SY+80} Z" fill="#0869A6"/>')
for k, l in enumerate(["Painel com a", "análise de risco"]):
    o.append(f'<text x="1540" y="{SY-6+k*28}" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle">{l}</text>')
o.append(f'<text x="1540" y="{SY+115}" font-size="13" fill="#4A5763" text-anchor="middle">No painel, fora do risco:</text>')
o.append(f'<text x="1540" y="{SY+133}" font-size="13" fill="#4A5763" text-anchor="middle">tratabilidade e obras</text>')
# legenda
lx = 40
for st, l in [("d", "Decidido ou pronto"), ("p", "Proposta, teste ou parcial"), ("f", "Falta")]:
    f, b, t = COR[st]
    o.append(f'<rect x="{lx}" y="{H-50}" width="22" height="18" rx="4" fill="{f}" stroke="{b}" stroke-width="1.5"/>')
    o.append(f'<text x="{lx+30}" y="{H-36}" font-size="14" fill="#1F2A33">{l}</text>')
    lx += 260
o.append(f'<text x="{W-40}" y="{H-36}" font-size="12" fill="#4A5763" text-anchor="end">Coordenadas e buffers: com pontos ainda aproximados. Pesos: só de teste; o grupo decide até 14/10.</text>')
o.append('</svg>')
open(__import__("pathlib").Path(__file__).resolve().parents[1] / "docs/img/ishikawa_painel.svg", "w", encoding="utf-8").write("\n".join(o))
