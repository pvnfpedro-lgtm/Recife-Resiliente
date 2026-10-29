"""Monta a página do painel como o Apps Script entrega, fora do Apps Script.

O Index (appscript/Index.html.html) chama os outros arquivos com
<?!= include('Nome'); ?>. Este script troca cada chamada pelo conteúdo de
appscript/Nome.html, igual à função include() de Código.js. Serve para abrir
a página no navegador ou conferir que nenhum pedaço se perdeu.

Uso: python3 scripts/montar_painel.py [--saida painel.html]
"""
import argparse
import re
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "appscript"
INCLUDE = re.compile(r"<\?!=\s*include\('([^']+)'\);?\s*\?>")


def montar(pasta=PASTA):
    """Devolve o HTML do Index com os includes trocados pelo conteúdo dos arquivos."""
    index = (pasta / "Index.html.html").read_text(encoding="utf-8")

    def trocar(m):
        arquivo = pasta / (m.group(1) + ".html")
        if not arquivo.exists():
            raise FileNotFoundError(f"include('{m.group(1)}'): {arquivo} não existe")
        return arquivo.read_text(encoding="utf-8")

    return INCLUDE.sub(trocar, index)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--saida", default="painel_montado.html")
    args = ap.parse_args()
    Path(args.saida).write_text(montar(), encoding="utf-8")
    print(f"Página montada em {args.saida}")


if __name__ == "__main__":
    main()
