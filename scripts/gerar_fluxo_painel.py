"""Desenha o fluxo de dados do painel (docs/img/fluxo_painel.svg/.png).

Uso: python3 scripts/gerar_fluxo_painel.py docs/img/fluxo_painel   (requer cairosvg)
"""
import cairosvg, sys
W,H=1260,560
A="#0869A6"; G="#334155"; F="#F2F2F2"; L="#5496BF"
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, sans-serif">',
'<defs><marker id="s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#334155"/></marker></defs>',
f'<rect width="{W}" height="{H}" fill="#fff"/>',
f'<text x="30" y="34" font-size="20" font-weight="bold" fill="{A}">Fluxo de dados do painel Recife Resiliente</text>']
def box(x,y,w,h,t,s="",fill=F,stroke=L,tc=G):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    ty=y+h/2-(8 if s else -5)
    o.append(f'<text x="{x+w/2}" y="{ty}" font-size="15" font-weight="bold" fill="{tc}" text-anchor="middle">{t}</text>')
    for i,l in enumerate(s.split("|") if s else []):
        o.append(f'<text x="{x+w/2}" y="{ty+20+i*17}" font-size="12.5" fill="{tc}" text-anchor="middle">{l}</text>')
def seta(pts,lab="",lx=0,ly=0,dash=False):
    d="M"+" L".join(f"{x} {y}" for x,y in pts)
    o.append(f'<path d="{d}" fill="none" stroke="{G}" stroke-width="1.6" {"stroke-dasharray=\"6 4\"" if dash else ""} marker-end="url(#s)"/>')
    for i,l in enumerate(lab.split("|") if lab else []):
        o.append(f'<text x="{lx}" y="{ly+i*15}" font-size="11.5" fill="{G}" text-anchor="middle" font-style="italic">{l}</text>')
# colunas
for x,t in ((30,"ONDE O DADO NASCE"),(350,"ONDE FICA"),(660,"O QUE O PAINEL LÊ"),(980,"PAINEL")):
    o.append(f'<text x="{x}" y="72" font-size="12" font-weight="bold" fill="{L}" letter-spacing="1">{t}</text>')
box(30,95,240,80,"ArcGIS Pro","camada 2. Obras|(você insere as obras)")
box(350,95,240,80,"Portal ESIG","camada de obras publicada")
box(660,85,240,72,"WebMap d19385…","seu mapa (edição)|não aparece no painel")
box(660,170,240,62,"WebMap df725…","mapa que o painel carrega")
box(30,285,240,80,"Google Sheets","aba Notas dos pontos|(notas de TESTE)")
box(30,420,240,80,"GitHub","código do painel|(pasta appscript/)")
box(350,420,240,80,"Apps Script","projeto do painel")
# painel
o.append(f'<rect x="980" y="85" width="250" height="415" rx="10" fill="#fff" stroke="{A}" stroke-width="2.5"/>')
o.append(f'<text x="1105" y="112" font-size="16" font-weight="bold" fill="{A}" text-anchor="middle">Painel</text>')
box(995,128,220,72,"Mapa","camadas do WebMap df725",fill="#fff")
box(995,215,220,72,"Pontos críticos","21 pontos + círculo 300 m",fill="#fff")
box(995,302,220,86,"Lista, KPIs, aba 02","8 obras FICTÍCIAS|escritas no código",fill="#fff",stroke="#e31a1c")
box(995,403,220,82,"Endereços","/dev: teste (editores)|/exec @9: versão publicada",fill="#fff")
seta([(270,135),(345,135)],"Compartilhar como|camada da Web",308,190,dash=True)
seta([(590,125),(655,116)],dash=True)
seta([(590,145),(655,200)],"adicionar|a camada",585,215,dash=True)
seta([(900,201),(990,164)])
seta([(270,325),(990,251)],"Código.js lê a planilha",630,278)
seta([(270,460),(345,460)],"clasp push (só com|sua aprovação)",308,400)
seta([(590,460),(990,444)],"/exec só muda ao publicar nova versão",790,440)
# legenda
o.append(f'<line x1="30" y1="540" x2="70" y2="540" stroke="{G}" stroke-width="1.6"/><text x="78" y="544" font-size="12" fill="{G}">funcionando</text>')
o.append(f'<line x1="180" y1="540" x2="220" y2="540" stroke="{G}" stroke-width="1.6" stroke-dasharray="6 4"/><text x="228" y="544" font-size="12" fill="{G}">a fazer / não conectado</text>')
o.append(f'<rect x="420" y="532" width="22" height="14" rx="3" fill="#fff" stroke="#e31a1c" stroke-width="1.5"/><text x="450" y="544" font-size="12" fill="{G}">dado de exemplo</text>')
o.append('</svg>')
s="\n".join(o)
open(sys.argv[1]+".svg","w").write(s)
cairosvg.svg2png(bytestring=s.encode(),write_to=sys.argv[1]+".png",output_width=W*2)
