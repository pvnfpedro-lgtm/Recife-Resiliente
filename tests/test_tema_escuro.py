"""O bloco do tema escuro em Estilos.html está em dia com o gerador e não vaza para o tema claro."""
import importlib.util
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("gerar_tema_escuro", RAIZ / "scripts" / "gerar_tema_escuro.py")
gte = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gte)


def _bloco(txt):
    return txt[txt.index(gte.INICIO):txt.index(gte.FIM) + len(gte.FIM)]


def test_bloco_em_dia_com_o_gerador():
    txt = gte.ARQ.read_text(encoding="utf-8")
    css = txt[txt.index("<style>") + len("<style>"):txt.index(gte.INICIO)]
    assert gte.gerar(css) == _bloco(txt), "rode: python3 scripts/gerar_tema_escuro.py"


def test_toda_regra_gerada_so_vale_no_escuro():
    bloco = _bloco(gte.ARQ.read_text(encoding="utf-8"))
    for linha in bloco.splitlines():
        m = re.match(r"\s*(.+?)\{.*;\}$", linha)
        if m:
            for sel in m.group(1).split(","):
                assert sel.strip().startswith(gte.PREFIXO), sel


def test_conversoes_basicas():
    assert gte.converter("#ffffff", "fundo") != "#ffffff"          # fundo branco escurece
    assert gte.converter("#1e2430", "fundo") == "#1e2430"          # fundo já escuro fica
    assert gte.converter("#ffffff", "texto") == "#ffffff"          # texto branco (sobre botão) fica
    assert gte.converter("#0869A6", "fundo") == "#0869A6"          # cor de botão fica
