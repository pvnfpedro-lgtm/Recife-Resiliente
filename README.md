# Recife Resiliente

Desafio estratégico do Programa Primeira Liderança / Rede GGOV Recife
(consultoria Motriz). Equipe de 6 servidores municipais; tutoria da Unidade de
Governança / CGM.

**Problema:** alagamentos no Recife.
**Recorte:** gestão integrada de risco de alagamento. A ideia é priorizar
territórios críticos por **risco** (probabilidade + exposição + vulnerabilidade
+ impacto), e não só por recorrência, e articular a prevenção entre os órgãos.
A solução não é obra: é **prevenção priorizada por risco**. A resposta ao
evento já tem dono (COP).

**Etapa atual:** sistema de hierarquização de pontos críticos, com piloto na
RPA 6 (21 trechos da planilha da EMLURB).

## Estrutura

```
docs/            contexto, metodologia, fontes, cronograma e pendências
dados/modelos/   modelos de CSV (critérios, pontos, notas, tratabilidade)
dados/brutos/    dados de origem (IBGE, IVS, EMLURB, COP…), sem edição
dados/processados/ saídas do SIG e do script de hierarquização
scripts/         hierarquizar.py: risco (Probabilidade × Consequência) + matriz
tests/           testes do script, com dados fictícios
entregas/        slides, resumo executivo, plano de 90 dias
```

## Documentos

1. [Contexto e recorte](docs/01-contexto.md)
2. [Metodologia de hierarquização](docs/02-metodologia-hierarquizacao.md)
3. [Fontes de dados](docs/03-fontes-de-dados.md)
4. [Cronograma](docs/04-cronograma.md)
5. [Pendências e dados não verificados](docs/05-pendencias.md)
6. [Plano de Pedro até a Etapa 2](docs/06-plano-pedro-ate-etapa2.md)
7. [Revisão dos critérios](docs/07-revisao-criterios.md)

Checklist de subcritérios, escalas de nota (1 a 5) e fontes:
`dados/Recife_Resiliente_Checklist_Subcriterios.xlsx` (gerado por
`scripts/gerar_checklist_subcriterios.py`).

## Calcular a hierarquização

O script usa só a biblioteca padrão do Python 3.9+.

```bash
python3 scripts/hierarquizar.py \
  --criterios dados/modelos/criterios.csv \
  --notas dados/processados/notas.csv \
  --tratabilidade dados/processados/tratabilidade.csv \
  --saida dados/processados/ranking.csv
```

Para conferir o funcionamento com dados fictícios:

```bash
python3 -m unittest discover -s tests
```

## Prazos

| Etapa | Data |
|---|---|
| Etapa 2 — Escolher | 14/10/2026 |
| Etapa 3 | 27/10/2026 |
| Etapa 4 | 04/11/2026 |
| Etapa 5 / entrega final | 11/11/2026 |

Na entrega final: apresentação de até 8 slides, resumo executivo de 1 página,
protótipo/teste e plano de 90 dias.
