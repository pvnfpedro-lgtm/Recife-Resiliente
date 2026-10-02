#!/usr/bin/env python3
"""Gera dados/Recife_Resiliente_Checklist_Subcriterios.xlsx.

Uma linha por subcritério: como medir, escala de notas de 1 a 5, origem da
faixa, recomendação, fonte e checklist de confirmação dos dados. Editar a
lista SUBCRITERIOS abaixo e rodar de novo para atualizar a planilha.
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

SAIDA = Path(__file__).resolve().parent.parent / "dados" / "Recife_Resiliente_Checklist_Subcriterios.xlsx"
FONTE = "Arial"
Q = ("Quintil 1 (20% menores)", "Quintil 2", "Quintil 3", "Quintil 4", "Quintil 5 (20% maiores)")

# (critério, código, subcritério, como medir, tipo de nota, (nota 1..5), origem da faixa,
#  recomendação, fonte, observação, busca prévia)
SUBCRITERIOS = [
    ("Probabilidade", "P1", "Frequência de alagamento",
     "Média de eventos por ano nas 3 últimas estações chuvosas", "Faixa fixa",
     ("< 1", "1–2", "3–4", "5–6", "≥ 7"), "Planilha original (provisória)",
     "Manter — peso alto",
     "Ficha preenchida com a EMLURB (agora); ocorrências do COP e da Defesa Civil (confirmação)",
     "Pedido ao COP via tutora/CGM. 156 só para conferir. Calibrar faixas com a distribuição real.",
     "Não verificado: depende de pedido aos órgãos."),
    ("Probabilidade", "P2", "Severidade",
     "Altura máxima da água e tempo para baixar; nota = média das duas notas, arredondada para cima",
     "Faixa fixa",
     ("Altura < 10 cm / baixa em < 1 h", "10–30 cm (tornozelo) / 1–3 h",
      "30–50 cm (joelho) / 3–6 h", "50–100 cm (cintura) / 6–12 h", "> 100 cm / > 12 h"),
     "Planilha original (provisória); regra da média: proposta Claude",
     "Manter — peso alto", "Ficha EMLURB; escuta com Defesa Civil e moradores",
     "Extensão da mancha fica registrada como informação, sem nota própria.",
     "Não verificado: dado de campo."),
    ("Probabilidade", "P3", "Influência da maré",
     "O escoamento trava com a maré alta?", "Classe",
     ("Não influencia", "—", "Agrava ocasionalmente", "—",
      "Alaga dependendo da maré / escoamento bloqueado"),
     "Planilha original", "Manter", "Ficha EMLURB; APAC; tábua de marés",
     "Notas 2 e 4 ficam para casos intermediários, se a EMLURB indicar.",
     "APAC confirmada na busca; tábua de marés não verificada."),
    ("Probabilidade", "P4", "Proximidade de rio ou canal",
     "Distância do ponto ao curso d'água mais próximo (m); quanto mais perto, maior a nota",
     "Quintil (invertido)",
     ("Quintil mais distante", "Quintil 2", "Quintil 3", "Quintil 4", "Quintil mais próximo"),
     "Regra de quintis da planilha original",
     "Manter — peso menor (suscetibilidade)",
     "Shapefile próprio da rede hidrográfica; ESIG – recursos hídricos",
     "Reprojetar para EPSG:31985. Conferir se os canais estão no arquivo.",
     "ESIG com recursos hídricos confirmado na busca (não aberto)."),
    ("Probabilidade", "P5", "Impermeabilização",
     "% do círculo de 300 m com vegetação ou solo permeável; quanto menos verde, maior a nota",
     "Faixa fixa", ("> 40%", "30–40%", "20–30%", "10–20%", "< 10%"),
     "Planilha original (provisória)", "Manter — peso menor (suscetibilidade)",
     "MapBiomas (30 m); alternativa: edificações do ESIG",
     "Se quase todos os pontos ficarem em < 10%, trocar por quintis.", "Não verificado."),
    ("Probabilidade", "P6", "Baixio",
     "Cota do ponto menos a cota média do círculo (m); quanto mais baixo, maior a nota",
     "Quintil (invertido)",
     ("Quintil mais alto", "Quintil 2", "Quintil 3", "Quintil 4", "Quintil mais baixo"),
     "Proposta Claude (quintis)", "Condicional — só com curvas de nível ou modelo de terreno",
     "ESIG (curvas de nível, a verificar); topografia da Prefeitura",
     "Medida mais objetiva de acúmulo de água.",
     "Não encontrado modelo de terreno público na busca."),
    ("Exposição", "E1", "População",
     "Moradores no círculo de 300 m (soma de população × fração da célula dentro do círculo)",
     "Quintil", Q, "Planilha original", "Manter",
     "IBGE — Grade Estatística 2022 (células de 200 × 200 m)",
     "No painel, mostrar também o valor em 1 km.", "Confirmado na busca (não baixado)."),
    ("Exposição", "E2", "Equipamentos sensíveis",
     "Nº de escolas, creches e unidades de saúde no círculo", "Faixa fixa",
     ("Nenhum", "1", "2", "3–4", "≥ 5 ou hospital/UPA no círculo"),
     "Proposta Claude (provisória)", "Manter",
     "IBGE — CNEFE 2022 (ensino e saúde); CNES/DATASUS",
     "Calibrar com as contagens reais. Conferir se creches aparecem como 'ensino'.",
     "CNEFE confirmado na busca (não baixado)."),
    ("Exposição", "E3", "Atividade econômica",
     "Nº de comércios e serviços no círculo", "Quintil", Q, "Planilha original", "Manter",
     "IBGE — CNEFE 2022 (outras finalidades)",
     "'Outras finalidades' pode incluir templos e órgãos públicos.",
     "CNEFE confirmado na busca (não baixado)."),
    ("Vulnerabilidade", "V2", "Grupos sensíveis",
     "% de moradores com 60+ anos ou 0–4 anos nos setores do círculo (ponderado pela área)",
     "Quintil", Q, "Planilha original", "Manter",
     "IBGE — Agregados por setor 2022 (idade)", "",
     "Idade por setor confirmada na busca (não baixado)."),
    ("Vulnerabilidade", "V3", "Favelas e comunidades urbanas",
     "% da área do círculo em favelas e comunidades urbanas", "Faixa fixa",
     ("0%", "< 10%", "10–25%", "25–50%", "> 50%"), "Proposta Claude (provisória)",
     "Manter — substitui o V1 se a malha 2022 existir",
     "IBGE — Favelas e Comunidades Urbanas 2022 (malha)", "Mais atual que o IVS (2010).",
     "Não verificado."),
    ("Vulnerabilidade", "V4", "Tipo de moradia",
     "% de domicílios do tipo casa nos setores do círculo", "Quintil", Q,
     "Proposta Claude (quintis)", "Manter",
     "IBGE — Agregados por setor 2022 (tipo de domicílio)",
     "Casa térrea é mais atingida que apartamento.",
     "Não verificado se a variável está no arquivo por setor."),
    ("Vulnerabilidade", "V1", "Vulnerabilidade social (IVS)",
     "Maior IVS entre as UDHs que tocam o círculo", "Faixa fixa",
     ("Muito baixa (0–0,200)", "Baixa (0,201–0,300)", "Média (0,301–0,400)",
      "Alta (0,401–0,500)", "Muito alta (> 0,500)"),
     "Faixas do Ipea (conferir no Atlas)", "Plano B — só se o V3 não estiver disponível",
     "Ipea — Atlas da Vulnerabilidade Social (UDH)", "Base do Censo 2010.",
     "Site confirmado na busca; faixas e ano-base a confirmar."),
    ("Impacto", "I1", "Mobilidade",
     "Classe da via mais importante afetada pelo alagamento; +1 se houver interdição registrada pela CTTU (máximo 5)",
     "Classe",
     ("Via local ou de pedestres", "Coletora", "Arterial secundária", "Arterial principal",
      "Trânsito rápido ou corredor de ônibus"),
     "Proposta Claude, a partir da classificação viária usada na planilha original",
     "Manter",
     "Hierarquia viária (ESIG / CTTU); OSM; paradas (Grande Recife); interdições (CTTU)",
     "Pedir a Antônio (CTTU): hierarquia viária, linhas e registro de interdições.",
     "Vias no ESIG confirmadas na busca; ônibus e interdições não verificados."),
    ("Impacto", "I2", "Risco sanitário",
     "% de domicílios sem ligação à rede de esgoto nos setores do círculo", "Quintil", Q,
     "Proposta Claude (quintis)", "Manter",
     "IBGE — Agregados por setor 2022 (esgotamento); Compesa",
     "Quintis porque a cobertura de esgoto no Recife é baixa e faixas fixas podem saturar.",
     "Esgotamento por setor confirmado na busca (não baixado)."),
]

CABECALHO = ["Critério", "Código", "Subcritério", "Como medir", "Tipo de nota",
             "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Nota 5", "Origem da faixa",
             "Recomendação", "Fonte", "Fonte confirmada?", "Dado existe na fonte?",
             "Observação", "Busca prévia (Claude)"]
LARGURAS = (14, 7, 22, 34, 12, 15, 15, 15, 15, 17, 22, 24, 34, 12, 12, 34, 30)
COR_CRITERIO = {"Probabilidade": "DDEBF7", "Exposição": "E2EFDA",
                "Vulnerabilidade": "FCE4D6", "Impacto": "EDE2F6"}
COR_NOTA = ("E2EFDA", "F4F9EE", "FFF9E5", "FDE9D9", "F8CBAD")
COLS_PREENCHER = (14, 15, 16)  # N, O, P


def gerar(saida=SAIDA):
    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist subcritérios"

    ws["A1"] = "Recife Resiliente — Subcritérios, notas, fontes e checklist dos dados (RPA 6)"
    ws["A1"].font = Font(name=FONTE, bold=True, size=13)
    ws["A2"] = (
        "Proposta de 02/10/2026 (Pedro + Claude), não validada pelo grupo. Nota 5 = mais crítico. "
        "Faixa fixa = valor absoluto (provisória: calibrar com os dados reais). Quintil = nota relativa "
        "entre os 21 pontos (Quintil 1 = 20% com menor valor). Preencha as colunas amarelas (N, O e P): "
        "Sim / Não / Parcial / Pendente. 'Fonte confirmada' = a base existe e é acessível; 'Dado existe "
        "na fonte' = a variável está lá, na escala do círculo de 300 m, e cobre os 21 pontos."
    )
    ws["A2"].font = Font(name=FONTE, italic=True, size=9)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:Q2")
    ws.row_dimensions[2].height = 44

    h = 4
    for c, titulo in enumerate(CABECALHO, 1):
        cel = ws.cell(row=h, column=c, value=titulo)
        cel.font = Font(name=FONTE, bold=True, color="FFFFFF")
        cel.fill = PatternFill("solid", fgColor="1F4E78")
        cel.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

    fino = Side(style="thin", color="BFBFBF")
    borda = Border(left=fino, right=fino, top=fino, bottom=fino)
    amarelo = PatternFill("solid", fgColor="FFF2CC")
    r0 = h + 1
    for i, (crit, cod, sub, medir, tipo, notas, origem, rec, fonte, obs, busca) in enumerate(SUBCRITERIOS):
        r = r0 + i
        valores = [crit, cod, sub, medir, tipo, *notas, origem, rec, fonte,
                   "Pendente", "Pendente", obs, busca]
        for c, v in enumerate(valores, 1):
            cel = ws.cell(row=r, column=c, value=v)
            cel.border = borda
            cel.font = Font(name=FONTE, size=10, color="0000FF" if c in COLS_PREENCHER else "000000")
            centro = c in (2, 5, 14, 15) or 6 <= c <= 10
            cel.alignment = Alignment(wrap_text=True, vertical="top",
                                      horizontal="center" if centro else "left")
            if c in COLS_PREENCHER:
                cel.fill = amarelo
            elif c in (1, 2):
                cel.fill = PatternFill("solid", fgColor=COR_CRITERIO[crit])
            elif 6 <= c <= 10:
                cel.fill = PatternFill("solid", fgColor=COR_NOTA[c - 6])
    ultima = r0 + len(SUBCRITERIOS) - 1

    dv = DataValidation(type="list", formula1='"Sim,Não,Parcial,Pendente"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"N{r0}:O{ultima}")
    for valor, cor in (("Sim", "C6EFCE"), ("Não", "FFC7CE"), ("Parcial", "FFEB9C")):
        ws.conditional_formatting.add(
            f"N{r0}:O{ultima}",
            CellIsRule(operator="equal", formula=[f'"{valor}"'],
                       fill=PatternFill("solid", fgColor=cor)))

    s = ultima + 2
    ws.cell(row=s, column=1, value="Resumo").font = Font(name=FONTE, bold=True)
    ws.cell(row=s, column=14, value="Fonte confirmada").font = Font(name=FONTE, bold=True, size=9)
    ws.cell(row=s, column=15, value="Dado existe").font = Font(name=FONTE, bold=True, size=9)
    for k, rotulo in enumerate(("Sim", "Parcial", "Não", "Pendente")):
        rr = s + 1 + k
        cel = ws.cell(row=rr, column=13, value=rotulo)
        cel.font = Font(name=FONTE, size=10)
        cel.alignment = Alignment(horizontal="right")
        for col in ("N", "O"):
            ws[f"{col}{rr}"] = f"=COUNTIF({col}${r0}:{col}${ultima},$M{rr})"
            ws[f"{col}{rr}"].font = Font(name=FONTE, size=10)
            ws[f"{col}{rr}"].alignment = Alignment(horizontal="center")
    rr = s + 5
    cel = ws.cell(row=rr, column=13, value="Subcritérios com fonte e dado confirmados")
    cel.font = Font(name=FONTE, bold=True, size=10)
    cel.alignment = Alignment(horizontal="right", wrap_text=True)
    ws[f"O{rr}"] = (f'=COUNTIFS(N{r0}:N{ultima},"Sim",O{r0}:O{ultima},"Sim")'
                    f'&" de "&ROWS(N{r0}:N{ultima})')
    ws[f"O{rr}"].font = Font(name=FONTE, bold=True, size=10)
    ws[f"O{rr}"].alignment = Alignment(horizontal="center")

    for i, largura in enumerate(LARGURAS):
        ws.column_dimensions[chr(ord("A") + i)].width = largura
    ws.freeze_panes = f"D{r0}"
    ws.auto_filter.ref = f"A{h}:Q{ultima}"
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    wb.calculation.fullCalcOnLoad = True
    wb.save(saida)
    return r0, ultima


if __name__ == "__main__":
    print(gerar())
