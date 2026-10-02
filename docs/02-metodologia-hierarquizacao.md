# 2. Metodologia de hierarquização de pontos críticos

## Referência
Os critérios de hierarquização de obras do Plano de Ações do Plano Diretor de
Drenagem de São Paulo (FCTH/SIURB), adaptados para avaliar **pontos
críticos** em vez de obras.

## Escopo do piloto
RPA 6, com os **21 trechos** da planilha da EMLURB.

## Critérios principais (decidido por Pedro em 02/10/2026)

As 7 dimensões de São Paulo foram reduzidas a **4 critérios**, que
correspondem aos componentes do risco do recorte. A regra é que **todo
critério precisa ser medível nos 21 pontos com dado obtenível**.

| Critério | Pergunta | Papel no cálculo |
|---|---|---|
| **Probabilidade** | Quanto e com que facilidade o ponto alaga? | Multiplica a Consequência |
| **Exposição** | Quem e o que está no caminho da água? | Parte da Consequência |
| **Vulnerabilidade** | Quem está ali consegue lidar com o alagamento? | Parte da Consequência |
| **Impacto** | Que consequência vai além do local (mobilidade, saúde)? | Parte da Consequência |

### De onde veio cada dimensão de São Paulo
| Dimensão original | Destino |
|---|---|
| Hidrológico | Probabilidade |
| Social | Exposição (população) e Vulnerabilidade (IVS, grupos sensíveis) |
| Econômico | Exposição (usos expostos) |
| Infraestrutura e mobilidade | Impacto (mobilidade); equipamentos vão para Exposição |
| Ambiental e sanitário | Impacto (sanitário); impermeabilização vai para Probabilidade; área sensível sai |
| Técnico | Diagnóstico de causa (fora do score); posição na bacia vai para Probabilidade |
| Político e institucional | Fora do score; aparece como contexto no painel |

### Fora do score
- **Tratabilidade:** mede se dá para agir rápido e forma o outro eixo da
  matriz.
- **Diagnóstico de causa:** explica por que o ponto alaga e indica qual órgão
  age.
- **Repercussão e pressão política:** aparecem como informação no painel,
  sem entrar no cálculo.

Os subcritérios de cada critério ainda serão definidos. A proposta inicial
está em [07-revisao-criterios.md](07-revisao-criterios.md).

## Cálculo (decidido: Probabilidade × Consequência)

Notas de 1 a 5 em cada subcritério; 5 é o mais crítico.

1. **Nota de cada critério** = média ponderada das notas dos subcritérios,
   com `peso_subcriterio`.
2. **Consequência** = média ponderada de Exposição, Vulnerabilidade e
   Impacto, com `peso_dimensao`. Os pesos são definidos pelo grupo.
3. **Risco = Probabilidade × Consequência**, numa escala de **1 a 25**.

| Probabilidade \ Consequência | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | 5 | 10 | 15 | 20 | 25 |
| **4** | 4 | 8 | 12 | 16 | 20 |
| **3** | 3 | 6 | **9** | 12 | 15 |
| **2** | 2 | 4 | 6 | 8 | 10 |
| **1** | 1 | 2 | 3 | 4 | 5 |

Como se lê: um ponto que quase não alaga (P = 1) fica com risco baixo, por
mais gente que more perto. O ranking segue o raciocínio de risco e não premia
apenas a exposição.

**Consequência direta:** **sem nota de Probabilidade não há risco.** O ponto
fica sem posição no ranking até receber essa nota. Por isso a Probabilidade
dos 21 pontos é o dado prioritário: ficha da EMLURB agora e dados do COP
quando chegarem.

**Nota ausente não vira zero nem média.** O subcritério sai do cálculo
daquele ponto e a cobertura aparece na saída (por exemplo, `10/12`).

**Sensibilidade:** mostrar também o ranking com pesos iguais na Consequência.
Se o top 5 mudar muito, o ranking depende mais dos pesos do que dos dados.

## Matriz risco × tratabilidade
Tratabilidade de 1 a 5, em que **5 = mais tratável**. A nota é a média dos
itens.

Cortes padrão: risco **9** (equivale a 3 × 3) e tratabilidade **3**. Os dois
podem ser ajustados com `--corte-risco` e `--corte-tratabilidade`.

| | Tratabilidade alta | Tratabilidade baixa |
|---|---|---|
| **Risco alto** | **Agir já**: prevenção rápida e de alto impacto | **Estruturar**: articulação entre órgãos, médio prazo |
| **Risco baixo** | **Oportunidade**: quando houver equipe ou recurso | **Monitorar** |

## Coleta por SIG (decidido: 300 m no score, 1 km no painel)
- **Score:** buffer de **300 m**. Com as coordenadas atuais, só 4 dos 21
  pontos dividem mais da metade do círculo com outro ponto. Com 1 km, seriam
  18.
- **Painel:** buffer de **1 km** como "área de influência", só como
  informação.
- Nos trechos do tipo *Linha* ou *Vários*, aplicar o buffer à linha do
  trecho, não a uma coordenada só.
- ArcGIS Pro, SIRGAS 2000 / UTM 25S (**EPSG:31985**).
- Dados por área (setor, UDH, grade): ponderar pela fração de área dentro do
  buffer.

Fontes de menor escala (IBGE, Censo 2022), confirmadas na busca e ainda não
baixadas:
- **Grade Estatística:** células de 200 × 200 m na área urbana, com
  população.
- **Agregados por setor:** idade e tipo de esgotamento sanitário.
- **CNEFE:** coordenada de cada endereço (domicílios, estabelecimentos de
  saúde e de ensino).

> ⚠️ As coordenadas dos pontos ainda são **aproximadas**. Conferir antes do
> cálculo final.

## Camada de obras (planejada)
As obras **não entram no score de risco**, porque o risco mede a situação
de hoje. Elas servem para responder à pergunta *onde o risco é alto e
ninguém está atuando?*.

- **Tratabilidade:** item *janela de oportunidade*.
- **Painel:** cada ponto fica *com obra em execução*, *com obra prevista* ou
  *sem obra*. Risco alto sem obra é a lacuna onde a prevenção faz mais
  diferença.
- **Obra conectada ao ponto:** mesma sub-bacia (hierarquia do PMDR: Bacia →
  Sub-bacia → Ponto crítico → Obra) **e** confirmação da URB ou da EMLURB de
  que a obra atua na drenagem do ponto. Distância sozinha não basta.
- **Dados previstos:** `obras.csv` (id, nome, órgão, tipo, situação,
  previsão de término, valor, sub-bacia) e `pontos_obras.csv` (ponto, obra,
  relação *resolve / mitiga / indireta*, quem confirmou).
- **Obra concluída recentemente:** sinalizar o ponto para revisar a nota de
  Probabilidade com a EMLURB, porque o histórico pode exagerar o risco atual.
- **Fontes:** URB (obras, prazos e custos; verificar o sistema Target),
  ProMorar, EMLURB.

## Pontos da RPA 6
Arquivo: `dados/processados/pontos_rpa6.geojson` (e `.csv`), gerado a
partir da aba *Pontos RPA 6*.

- **Nenhuma coordenada verificada:** 11 marcadas como *Aproximado* e 10
  como *Interseção* (localização automática pelo OpenStreetMap).
- **12 dos 21 são trechos** (*Linha* ou *Vários*): desenhar a linha no
  ArcGIS e aplicar o buffer à linha.
- **Grupos com círculos sobrepostos:** G1 (5, 6, 7, 11, 12), G2 (8, 41), G3
  (9, 36), G4 (33, 35, 54), G5 (34, 37). Manter os 21 pontos separados e
  mostrar os grupos no painel.
- **Prioridade da EMLURB:** 24, 33, 34, 35, 36 e 37, todos fora de Boa
  Viagem. Comparar com o ranking final.

## Arquivos de entrada do script
| Arquivo | Colunas |
|---|---|
| `criterios.csv` | `codigo, dimensao, subcriterio, peso_subcriterio, peso_dimensao` (`dimensao` ∈ Probabilidade, Exposição, Vulnerabilidade, Impacto; `peso_dimensao` vazio na Probabilidade) |
| `notas.csv` | `ponto_id, codigo, nota` (uma linha por ponto e subcritério) |
| `tratabilidade.csv` | `ponto_id, item, nota` |
| `pontos.csv` | `ponto_id, trecho, bairro, x, y, coordenada_verificada` |
