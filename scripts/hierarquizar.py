#!/usr/bin/env python3
"""Hierarquização de pontos críticos de alagamento — Recife Resiliente.

Calcula o risco de cada ponto como Probabilidade x Consequência (1 a 25), em
que a Consequência é a média ponderada de Exposição, Vulnerabilidade e
Impacto, e classifica o ponto na matriz risco x tratabilidade.
Metodologia em docs/02-metodologia-hierarquizacao.md.

Nota ausente não é imputada: o subcritério sai do cálculo daquele ponto e a
cobertura (notas presentes / subcritérios) é informada na saída.
"""

import argparse
import csv
import sys
from collections import defaultdict

NOTA_MIN, NOTA_MAX = 1, 5
PROBABILIDADE = "Probabilidade"

QUADRANTES = {
    (True, True): "Agir já",
    (True, False): "Estruturar",
    (False, True): "Oportunidade",
    (False, False): "Monitorar",
}


class ErroDeDados(ValueError):
    pass


def _numero(valor, contexto):
    try:
        return float(str(valor).strip().replace(",", "."))
    except ValueError:
        raise ErroDeDados(f"{contexto}: valor não numérico {valor!r}")


def _nota(valor, contexto):
    nota = _numero(valor, contexto)
    if not NOTA_MIN <= nota <= NOTA_MAX:
        raise ErroDeDados(f"{contexto}: nota {nota} fora da escala {NOTA_MIN}-{NOTA_MAX}")
    return nota


def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def carregar_criterios(linhas):
    """Retorna ({codigo: (dimensao, peso_sub)}, {dimensao: peso_dim})."""
    criterios, pesos_dim = {}, {}
    for i, linha in enumerate(linhas, start=2):
        codigo = linha["codigo"].strip()
        dimensao = linha["dimensao"].strip()
        if codigo in criterios:
            raise ErroDeDados(f"criterios.csv linha {i}: código duplicado {codigo!r}")
        peso_sub = _numero(linha["peso_subcriterio"], f"criterios.csv linha {i}")
        # A Probabilidade multiplica a Consequência e não tem peso próprio.
        bruto = str(linha["peso_dimensao"]).strip()
        peso_dim = 0.0 if not bruto and dimensao == PROBABILIDADE else \
            _numero(bruto, f"criterios.csv linha {i}")
        if peso_sub < 0 or peso_dim < 0:
            raise ErroDeDados(f"criterios.csv linha {i}: peso negativo")
        if dimensao in pesos_dim and pesos_dim[dimensao] != peso_dim:
            raise ErroDeDados(
                f"criterios.csv linha {i}: peso_dimensao de {dimensao!r} diverge "
                f"({pesos_dim[dimensao]} x {peso_dim})"
            )
        pesos_dim[dimensao] = peso_dim
        criterios[codigo] = (dimensao, peso_sub)
    if not criterios:
        raise ErroDeDados("criterios.csv está vazio")
    return criterios, pesos_dim


def carregar_notas(linhas, criterios):
    """Retorna {ponto_id: {codigo: nota}}."""
    notas = defaultdict(dict)
    for i, linha in enumerate(linhas, start=2):
        ponto = linha["ponto_id"].strip()
        codigo = linha["codigo"].strip()
        if codigo not in criterios:
            raise ErroDeDados(f"notas.csv linha {i}: código desconhecido {codigo!r}")
        if not str(linha["nota"]).strip():
            continue  # nota ausente: não entra no cálculo
        if codigo in notas[ponto]:
            raise ErroDeDados(f"notas.csv linha {i}: nota duplicada para {ponto}/{codigo}")
        notas[ponto][codigo] = _nota(linha["nota"], f"notas.csv linha {i}")
    return notas


def carregar_tratabilidade(linhas):
    """Retorna {ponto_id: média das notas de tratabilidade}."""
    por_ponto = defaultdict(list)
    for i, linha in enumerate(linhas, start=2):
        if not str(linha["nota"]).strip():
            continue
        por_ponto[linha["ponto_id"].strip()].append(
            _nota(linha["nota"], f"tratabilidade.csv linha {i}")
        )
    return {p: sum(v) / len(v) for p, v in por_ponto.items()}


def _media_ponderada(pares):
    total_peso = sum(peso for _, peso in pares)
    if total_peso == 0:
        return None
    return sum(valor * peso for valor, peso in pares) / total_peso


def score_ponto(notas_ponto, criterios, pesos_dim):
    """Retorna (risco, probabilidade, consequencia, {dimensao: nota}).

    Sem nota de Probabilidade o risco fica indefinido (None): não há como
    estimar risco só pela consequência.
    """
    por_dim = defaultdict(list)
    for codigo, nota in notas_ponto.items():
        dimensao, peso_sub = criterios[codigo]
        por_dim[dimensao].append((nota, peso_sub))

    notas_dim = {}
    for dimensao, pares in por_dim.items():
        media = _media_ponderada(pares)
        if media is not None:
            notas_dim[dimensao] = media

    probabilidade = notas_dim.get(PROBABILIDADE)
    consequencia = _media_ponderada(
        [(n, pesos_dim[d]) for d, n in notas_dim.items() if d != PROBABILIDADE]
    )
    if probabilidade is None or consequencia is None:
        return None, probabilidade, consequencia, notas_dim
    return probabilidade * consequencia, probabilidade, consequencia, notas_dim


def quadrante(risco, tratabilidade, corte_risco, corte_trat):
    if risco is None or tratabilidade is None:
        return ""
    return QUADRANTES[(risco >= corte_risco, tratabilidade >= corte_trat)]


def hierarquizar(criterios_linhas, notas_linhas, trat_linhas=None,
                 corte_risco=9.0, corte_trat=3.0):
    criterios, pesos_dim = carregar_criterios(criterios_linhas)
    notas = carregar_notas(notas_linhas, criterios)
    tratabilidade = carregar_tratabilidade(trat_linhas or [])
    dimensoes = list(dict.fromkeys(d for d, _ in criterios.values()))

    resultado = []
    for ponto in sorted(set(notas) | set(tratabilidade)):
        risco, prob, cons, notas_dim = score_ponto(
            notas.get(ponto, {}), criterios, pesos_dim)
        trat = tratabilidade.get(ponto)
        resultado.append({
            "ponto_id": ponto,
            "risco": risco,
            "indice": None if risco is None else (risco - 1) / 24,
            "probabilidade": prob,
            "consequencia": cons,
            "cobertura": f"{len(notas.get(ponto, {}))}/{len(criterios)}",
            "tratabilidade": trat,
            "quadrante": quadrante(risco, trat, corte_risco, corte_trat),
            **{f"dim_{d}": notas_dim.get(d) for d in dimensoes},
        })

    # Ranking: maior risco primeiro; pontos sem risco vão para o fim.
    resultado.sort(key=lambda r: (r["risco"] is None, -(r["risco"] or 0), r["ponto_id"]))
    posicao = 0
    for r in resultado:
        if r["risco"] is not None:
            posicao += 1
            r["posicao"] = posicao
        else:
            r["posicao"] = ""
    return resultado


def _formatar(valor):
    if valor is None:
        return ""
    if isinstance(valor, float):
        return f"{valor:.2f}"
    return valor


def escrever(resultado, destino):
    if not resultado:
        return
    campos = ["posicao", "ponto_id", "risco", "indice", "probabilidade", "consequencia",
              "cobertura", "tratabilidade", "quadrante"]
    campos += [k for k in resultado[0] if k.startswith("dim_")]
    escritor = csv.DictWriter(destino, fieldnames=campos)
    escritor.writeheader()
    for r in resultado:
        escritor.writerow({k: _formatar(r[k]) for k in campos})


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--criterios", required=True)
    p.add_argument("--notas", required=True)
    p.add_argument("--tratabilidade")
    p.add_argument("--corte-risco", type=float, default=9.0,
                   help="corte do risco na matriz (padrão: 9 = 3 x 3)")
    p.add_argument("--corte-tratabilidade", type=float, default=3.0,
                   help="corte da tratabilidade na matriz (padrão: 3)")
    p.add_argument("--saida", help="CSV de saída (padrão: tela)")
    args = p.parse_args(argv)

    try:
        resultado = hierarquizar(
            ler_csv(args.criterios),
            ler_csv(args.notas),
            ler_csv(args.tratabilidade) if args.tratabilidade else None,
            args.corte_risco,
            args.corte_tratabilidade,
        )
    except (ErroDeDados, KeyError) as e:
        sys.exit(f"Erro nos dados: {e}")

    if args.saida:
        with open(args.saida, "w", newline="", encoding="utf-8") as f:
            escrever(resultado, f)
    else:
        escrever(resultado, sys.stdout)

    incompletos = [r["ponto_id"] for r in resultado
                   if r["cobertura"].split("/")[0] != r["cobertura"].split("/")[1]]
    if incompletos:
        print(f"Aviso: {len(incompletos)} ponto(s) com notas faltando: "
              f"{', '.join(incompletos)}", file=sys.stderr)


if __name__ == "__main__":
    main()
