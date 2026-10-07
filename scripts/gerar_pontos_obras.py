"""Gera o CSV de pontos das obras para o ArcGIS Pro ("Tabela XY para Ponto").

Lê a aba "Obras" da planilha do painel (export CSV do Google Sheets) e
escreve `dados/processados/arcgis/obras_pontos.csv`, com lat e lon separados
(ponto decimal, WGS 1984), a categoria do tipo de obra e o nome do ícone
(mapa/icones/obra_<categoria>[_licitacao].svg; docs/09-identidade-visual-mapa.md).

Obra sem coordenada, com coordenada fora do Recife ou sem tipo reconhecido não
recebe valor inventado: sem coordenada ou fora do Recife fica fora do CSV; sem
tipo entra com categoria e ícone vazios. Todas aparecem na lista de pendências
que o script imprime.

Uso: python3 scripts/gerar_pontos_obras.py [arquivo.csv]
     (sem argumento, baixa a aba direto da planilha)
"""
import csv
import io
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "dados" / "processados" / "arcgis" / "obras_pontos.csv"
PLANILHA_ID = "1DN3abWIPk0dvOkh-28D2NGYBLgMI437Vx7Sk7TqpDc0"
GID_OBRAS = 900100
URL = f"https://docs.google.com/spreadsheets/d/{PLANILHA_ID}/export?format=csv&gid={GID_OBRAS}"

# Coluna "tipo" da aba "Obras" -> categoria do ícone (minúsculas, sem espaços extras).
CATEGORIAS = {
    "canal": "canal",
    "perfilamento do rio tejipió": "canal",
    "dragagem": "dragagem",
    "reservatórios de detenção": "reservatorio",
    "microrreservatório": "reservatorio",
    "diques e comportas": "dique",
    "parques alagáveis": "parque",
    "requalificações na rede": "rede",
}

# Caixa que contém o município do Recife, com folga (graus, WGS 1984).
LAT_MIN, LAT_MAX = -8.16, -7.92
LON_MIN, LON_MAX = -35.02, -34.85

CAMPOS = ["obra_id", "nome", "tipo", "categoria", "status", "icone",
          "lat", "lon", "coord_precisao"]


def categoria(tipo):
    return CATEGORIAS.get(" ".join(tipo.split()).lower(), "")


def situacao(status):
    """Situação padronizada: em_obra, licitacao, concluido ou vazio."""
    s = " ".join(status.split()).lower()
    if not s:
        return ""
    if "licita" in s:
        return "licitacao"
    if "conclu" in s:
        return "concluido"
    if "obra" in s:
        return "em_obra"
    return s


def icone(cat, sit):
    if not cat:
        return ""
    return f"obra_{cat}_licitacao" if sit == "licitacao" else f"obra_{cat}"


def coordenadas(texto):
    """'-8.08, -34.93' -> (-8.08, -34.93). Devolve None se vazio ou ilegível."""
    partes = [p.strip() for p in texto.split(",")]
    if len(partes) != 2:
        return None
    try:
        return float(partes[0]), float(partes[1])
    except ValueError:
        return None


def no_recife(lat, lon):
    return LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX


def montar(linhas):
    """Linhas da aba (dicionários) -> (pontos, pendências)."""
    pontos, pendencias = [], []
    for ln in linhas:
        oid = (ln.get("obra_id") or "").strip()
        if not oid:
            continue
        nome = (ln.get("nome") or "").strip()
        tipo = (ln.get("tipo") or "").strip()
        texto = (ln.get("coordenadas (lat, lon)") or "").strip()
        rotulo = f"{oid} {nome}"
        if not texto:
            pendencias.append(f"{rotulo}: sem coordenada (fora do CSV)")
            continue
        xy = coordenadas(texto)
        if xy is None:
            pendencias.append(f"{rotulo}: coordenada ilegível '{texto}' (fora do CSV)")
            continue
        if not no_recife(*xy):
            pendencias.append(f"{rotulo}: coordenada fora do Recife {xy} (fora do CSV)")
            continue
        cat = categoria(tipo)
        if not cat:
            pendencias.append(f"{rotulo}: tipo '{tipo}' sem categoria (ícone vazio)")
        sit = situacao(ln.get("status") or "")
        pontos.append({
            "obra_id": oid, "nome": nome, "tipo": tipo, "categoria": cat,
            "status": sit, "icone": icone(cat, sit),
            "lat": repr(xy[0]), "lon": repr(xy[1]),
            "coord_precisao": (ln.get("coord_precisao") or "").strip(),
        })
    return pontos, pendencias


def ler(origem=None):
    if origem:
        texto = Path(origem).read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(URL, timeout=60) as r:
            texto = r.read().decode("utf-8")
    return list(csv.DictReader(io.StringIO(texto)))


def main():
    pontos, pendencias = montar(ler(sys.argv[1] if len(sys.argv) > 1 else None))
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(pontos)
    print(f"{len(pontos)} pontos em {SAIDA.relative_to(RAIZ)}")
    for p in pendencias:
        print("pendente:", p)


if __name__ == "__main__":
    main()
