# 2. Metodologia de hierarquização de pontos críticos

## Referência
Os critérios de hierarquização de obras do Plano de Ações do Plano Diretor de
Drenagem de São Paulo (FCTH/SIURB), adaptados para avaliar **pontos
críticos** em vez de obras.

## Escopo do piloto
- RPA 6, com os **21 trechos** da planilha da EMLURB.
- A lista oficial de subcritérios está na aba *Critérios* de
  `Recife_Resiliente_RPA6_Criterios_Pontos_Criticos.xlsx`. Ela deve ser
  transcrita para `dados/modelos/criterios.csv`.

## Estrutura do score de criticidade
**24 subcritérios agrupados em 7 dimensões:**

| # | Dimensão | Código |
|---|---|---|
| 1 | Hidrológico | HID |
| 2 | Social | SOC |
| 3 | Econômico | ECO |
| 4 | Infraestrutura e mobilidade | INF |
| 5 | Ambiental e sanitário | AMB |
| 6 | Técnico | TEC |
| 7 | Político e institucional | POL |

- Cada subcritério recebe uma **nota de 1 a 5**; 5 é o mais crítico.
- Os **pesos são definidos pelo grupo** e ainda estão em aberto (ver
  [pendências](05-pendencias.md)).

### Cálculo (implementado em `scripts/hierarquizar.py`)

1. **Nota da dimensão** = média ponderada das notas dos subcritérios da
   dimensão, usando `peso_subcriterio`.
2. **Score de criticidade** = média ponderada das notas das dimensões,
   usando `peso_dimensao`.

Como os pesos são normalizados, o score fica sempre entre 1 e 5 e os pesos
podem ser informados em qualquer escala (percentual, 1–10 etc.).

**Nota ausente não vira zero nem média.** Se faltar nota, o subcritério sai
do cálculo daquele ponto e o ponto é marcado com a cobertura (por exemplo,
`22/24`). Assim o dado faltante aparece em vez de distorcer o ranking em
silêncio.

**Recomendação:** antes de fechar os pesos, rodar uma análise de
sensibilidade com pesos iguais e com os pesos do grupo. Se o top 5 mudar
muito, o ranking depende mais dos pesos do que dos dados, e isso precisa ser
dito à alta gestão.

## Tratabilidade (fora do score)
Prazo, custo, necessidade de desapropriação e itens parecidos **não entram**
no score. Eles medem se é fácil agir, não se o ponto é crítico. Por isso
compõem um eixo separado:

- Cada item de tratabilidade tem nota de 1 a 5, em que **5 = mais tratável**
  (mais rápido, mais barato, sem desapropriação).
- A tratabilidade do ponto é a média dos itens.

> ⚠️ A orientação da escala (5 = mais tratável) foi definida aqui por
> convenção e precisa ser confirmada pelo grupo.

### Matriz criticidade × tratabilidade
O corte padrão é 3,0 nos dois eixos e pode ser ajustado com `--corte`.

| | Tratabilidade alta | Tratabilidade baixa |
|---|---|---|
| **Criticidade alta** | **Agir já**: prevenção rápida e de alto impacto | **Estruturar**: articulação entre órgãos e planejamento de médio prazo |
| **Criticidade baixa** | **Oportunidade**: resolver quando houver equipe ou recurso | **Monitorar** |

## Coleta de dados por SIG
- **Unidade de análise:** círculo (buffer) de **300 m** em torno de cada
  ponto.
- **Software:** ArcGIS Pro.
- **Sistema de referência:** SIRGAS 2000 / UTM zona 25S, **EPSG:31985**.
- **Agregação:** para dados por setor censitário ou por UDH que cortam o
  buffer, recomendo ponderar pela área de interseção (*areal weighting*) e
  registrar o método usado em cada variável.
- As fontes estão em [03-fontes-de-dados.md](03-fontes-de-dados.md).

> ⚠️ As coordenadas dos pontos ainda são **aproximadas**. Como o buffer é de
> 300 m, um erro de algumas dezenas de metros pode mudar quais setores
> entram no cálculo. Conferir antes de rodar o SIG.

## Arquivos de entrada do script
| Arquivo | Colunas |
|---|---|
| `criterios.csv` | `codigo, dimensao, subcriterio, peso_subcriterio, peso_dimensao` |
| `notas.csv` | `ponto_id, codigo, nota` (formato longo, uma linha por ponto e subcritério) |
| `tratabilidade.csv` | `ponto_id, item, nota` |
| `pontos.csv` | `ponto_id, trecho, bairro, x, y, coordenada_verificada` |

Os modelos estão em `dados/modelos/`.
