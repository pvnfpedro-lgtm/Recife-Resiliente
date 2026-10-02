# 7. Revisão dos critérios (rascunho de 01/10/2026)

> **Atualização 02/10/2026:** Pedro decidiu os **4 critérios principais**
> (Probabilidade, Exposição, Vulnerabilidade e Impacto), o cálculo
> **Probabilidade × Consequência** e o raio de **300 m** no score, com 1 km no
> painel. Ver `02-metodologia-hierarquizacao.md`. **Os subcritérios abaixo
> ainda são proposta.**

Revisão da aba *Critérios* de `dados/Recife_Resiliente_RPA6_Criterios_Pontos_Criticos.xlsx`
(24 subcritérios no score e 7 itens de tratabilidade). Esta é uma
**recomendação** para o grupo decidir, não uma decisão tomada.

Filtros usados em cada subcritério:
1. Mede risco (probabilidade, exposição, vulnerabilidade ou impacto)?
2. Diferencia os 21 pontos?
3. Tem dado viável até 27/10?
4. Conta o mesmo fenômeno que outro subcritério?
5. Mede a gravidade do ponto ou a facilidade de agir nele?

## Diagnóstico

**1. O núcleo do risco depende de dado que ainda não temos.**
Os seis subcritérios hidrológicos (1 a 6) medem a *probabilidade* e a
*magnitude* do alagamento. Todos dependem de registros do COP e da Defesa
Civil ou de escuta de campo. Os subcritérios que dá para calcular agora com
dado público são quase todos de **exposição e vulnerabilidade**. Se os dados
do COP não chegarem, o score vira um índice de quem mora perto, não de risco.
Por isso o pedido ao COP é o item mais importante do cronograma.

**2. Os círculos de 300 m se sobrepõem.**
Cálculo feito com as coordenadas atuais, que ainda são aproximadas:
- **14 dos 21 pontos** têm o círculo sobreposto ao de outro ponto.
- **Conselheiro Aguiar (5, 6, 7, 11 e 12):** 5 pontos a até 410 m uns dos
  outros.
- **Dois Rios, no Ibura (33, 35 e 54):** os círculos de 33 e 54 têm 60% de
  área em comum.
- Nesses grupos, população, IVS, usos e vias darão notas quase iguais. A
  diferença entre os pontos vai vir dos critérios de ponto (hidrológico e
  sanitário).

Daí sai mais uma recomendação: para os 12 trechos do tipo *Linha* ou *Vários*,
o círculo em volta de uma coordenada só não representa o trecho. Recomendo
desenhar a linha do trecho e aplicar um buffer de 300 m em volta dela.

**3. Há contagem dupla.**
- *Repercussão pública* (23) inclui recorrência, que já está em *Frequência*
  (1).
- *Importância das edificações* (11) e *Equipamentos de emergência expostos*
  (15) contam as unidades de saúde duas vezes.
- *Custo recorrente* (12) acompanha a frequência dos eventos.

**4. Alguns subcritérios medem causa ou resposta, não risco.**
- *Fragilidade da drenagem* (20) e *Dependência de equipamento* (21) explicam
  **por que** o ponto alaga. Se a frequência já está no score, eles contam o
  mesmo efeito outra vez. O lugar deles é o **diagnóstico de causa**, que diz
  qual órgão age e com que tipo de ação.
- *Acessibilidade de resposta* (16) mede a resposta ao evento, que é do COP e
  está fora do recorte.

**5. A tratabilidade está pensada para obra.**
Prazo de 0 a 60 meses, desapropriação, licenciamento e custo de intervenção
são critérios de obra, e a solução do projeto não é obra. Além disso, sem saber
qual intervenção cada ponto exige, esses itens não têm como ser medidos agora.

## Recomendação: de 24 para 12 subcritérios, organizados pelos 4 componentes do risco

| Componente | Subcritério | Origem | Dado |
|---|---|---|---|
| **Probabilidade** | Frequência de eventos | 1 | COP / Defesa Civil: **crítico** |
| | Gatilho de chuva | 2 | Depende do 1 + Cemaden/APAC |
| | Influência da maré | 3 | Escuta + APAC |
| | Severidade do evento (altura, extensão e duração juntas) | 4+5+6 | Escuta com EMLURB, Defesa Civil e moradores |
| | Posição na bacia | 22 | Shapefile próprio + PMDR |
| | Impermeabilização do entorno | 18 | MapBiomas / Prefeitura (não verificado) |
| **Exposição** | População exposta | 7 | IBGE 2022 |
| | Usos expostos (escola, creche, saúde, comércio) | 11+15+10 | Prefeitura / CNES |
| **Vulnerabilidade** | Vulnerabilidade social | 8 | IVS/Ipea (base 2010) |
| | Grupos sensíveis | 9 | IBGE 2022 (confirmar faixa etária por setor) |
| **Impacto** | Mobilidade afetada | 13 | Hierarquia viária e linhas de ônibus: **CTTU (Antônio)** |
| | Risco sanitário | 19 | Compesa + vistoria |

Pesos: como o risco é Probabilidade × Consequência, a Probabilidade não tem
peso. O grupo define só os pesos de Exposição, Vulnerabilidade e Impacto
dentro da Consequência.

### O que sai do score e para onde vai

| Subcritério | Destino | Motivo |
|---|---|---|
| 23 Repercussão pública, 24 Pressão institucional | Coluna de contexto no painel | Contagem dupla e risco de viés; difícil de defender na alta gestão |
| 20 Fragilidade da drenagem, 21 Dependência de equipamento | **Diagnóstico de causa** (frente de Pedro) | Explicam a causa, não a gravidade; definem quem age |
| 16 Acessibilidade de resposta | Sai | Resposta é do COP; exigiria análise de rede |
| 17 Área ambientalmente sensível | Tratabilidade (licenciamento), se houver intervenção | Mede impacto de obra, não risco de alagamento |
| 12 Custo recorrente, 14 Infraestrutura crítica | Sai; volta se o dado aparecer | Dado improvável até 27/10 |

### Nova tratabilidade, voltada para prevenção
| Item | Nota 5 (mais fácil) | Nota 1 (mais difícil) |
|---|---|---|
| Natureza da causa (vem do diagnóstico) | Manutenção ou limpeza | Obra estrutural |
| Governança do ponto (item 30 atual) | Dono e protocolo definidos | Sem dono / conflito de competência |
| Janela de oportunidade (item 31 atual) | Obra ou orçamento em andamento | Nada previsto |

## A confirmar
- Se o agregado do Censo 2022 por setor traz faixa etária (para o subcritério
  9).
- Se existe camada de uso do solo ou de equipamentos georreferenciada no portal
  da Prefeitura.
- Qualidade do MapBiomas (30 m) num círculo de 300 m: são cerca de 300 pixels,
  o que deve bastar, mas é preciso conferir.
- O resultado da sobreposição muda depois da conferência das coordenadas.
