# 7. Revisão das dimensões (rascunho de 01/10/2026)

> **Termos (03/10/2026):** "critério" passou a se chamar **dimensão** e
> "subcritério" passou a se chamar **variável**. O texto abaixo já usa os
> termos novos; a aba *Critérios* da planilha da equipe mantém o nome original.

> **Atualização 02/10/2026:** Pedro decidiu os **4 dimensões principais**
> (Probabilidade, Exposição, Vulnerabilidade e Impacto), o cálculo
> **Probabilidade × Consequência** e o raio de **300 m** no score, com 1 km no
> painel. Ver `02-metodologia-hierarquizacao.md`.
>
> **Lista atual de variáveis:** ver a seção *Lista proposta de 02/10*
> no fim deste documento e a planilha
> `dados/Recife_Resiliente_Checklist_Variaveis.xlsx`. A tabela de 12
> variáveis logo abaixo é a versão de 01/10, mantida como histórico.

Revisão da aba *Critérios* de `dados/Recife_Resiliente_RPA6_Criterios_Pontos_Criticos.xlsx`
(24 variáveis no score e 7 itens de tratabilidade). Esta é uma
**recomendação** para o grupo decidir, não uma decisão tomada.

Filtros usados em cada variável:
1. Mede risco (probabilidade, exposição, vulnerabilidade ou impacto)?
2. Diferencia os 21 pontos?
3. Tem dado viável até 27/10?
4. Conta o mesmo fenômeno que outra variável?
5. Mede a gravidade do ponto ou a facilidade de agir nele?

## Diagnóstico

**1. O núcleo do risco depende de dado que ainda não temos.**
As seis variáveis hidrológicas (1 a 6) medem a *probabilidade* e a
*magnitude* do alagamento. Todos dependem de registros do COP e da Defesa
Civil ou de escuta de campo. As variáveis que dá para calcular agora com
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
  diferença entre os pontos vai vir das dimensões de ponto (hidrológico e
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

**4. Alguns variáveis medem causa ou resposta, não risco.**
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

## Recomendação: de 24 para 12 variáveis, organizados pelos 4 componentes do risco

| Componente | Variável | Origem | Dado |
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

| Variável | Destino | Motivo |
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
- Se o agregado do Censo 2022 por setor traz faixa etária (para a variável
  9).
- Se existe camada de uso do solo ou de equipamentos georreferenciada no portal
  da Prefeitura.
- Qualidade do MapBiomas (30 m) num círculo de 300 m: são cerca de 300 pixels,
  o que deve bastar, mas é preciso conferir.
- O resultado da sobreposição muda depois da conferência das coordenadas.

## Lista proposta de 02/10/2026 (13 variáveis)

Pedro aprovou as variáveis recomendadas, incluiu favelas e comunidades
(V3) e pediu sugestões. A lista abaixo junta as duas coisas. **Ainda depende
da confirmação dos dados.** O checklist de cada fonte está em
`dados/Recife_Resiliente_Checklist_Variaveis.xlsx`.

| Dimensão | Código | Variável | Situação |
|---|---|---|---|
| Probabilidade | P1 | Frequência | Manter, peso alto |
| | P2 | Severidade (altura + tempo para baixar + extensão) | Manter, peso alto |
| | P3 | Influência da maré | Manter |
| | P4 | Proximidade de rio ou canal | Manter, peso menor |
| | P5 | Impermeabilização | Manter, peso menor |
| | P6 | Baixio (cota do terreno) | Condicional: só com curvas de nível |
| Exposição | E1 | População (grade de 200 m) | Manter |
| | E2 | Equipamentos sensíveis (CNEFE) | Manter |
| | E3 | Atividade econômica (CNEFE) | Manter |
| Vulnerabilidade | V2 | Grupos sensíveis (idade) | Manter |
| | V3 | Favelas e comunidades urbanas 2022 | Manter; substitui o V1 |
| | V4 | Tipo de moradia (% casas) | Manter |
| | V1 | IVS (2010) | Plano B, se o V3 não existir |
| Impacto | I1 | Mobilidade (classe da via + paradas + interdições) | Manter |
| | I2 | Risco sanitário (esgotamento por setor) | Manter |

Sugestões descartadas: chamados do 156 como variável (usar só para
conferir o P1), % de não alfabetizados (repete V3/IVS), leptospirose (dado
por bairro, grande demais para o círculo), rota até hospital (é resposta ao
evento, do COP). Exposição não ganhou variáveis novas.

Próximo passo: faixas de nota de 1 a 5 de cada variável, começando pela
Probabilidade (que vira a ficha da reunião com a EMLURB).

## Documento da equipe (Hellis, 03/10/2026)
Documento no Google Docs feito por Hellis, do grupo:
<https://docs.google.com/document/d/1fs88X9gkLE-rsSib_2g1YIOCM1FZn7Ul-PZSB3PMOos/edit>.
Seções: mapa institucional (órgão × competência × indicador ×
responsabilidade), modelo de risco com 4 dimensões e "exemplos de
variáveis", score, mapa de pontos prioritários, catálogo de controles
(preventivos, concomitantes, posteriores) e painel.

**Leitura (recomendação, não decisão do grupo):** as dimensões são as mesmas
4 do modelo. A tabela do documento é a moldura conceitual; a lista acima é a
versão operacional (fonte, medida no círculo de 300 m, nota de 1 a 5). Não
trocar as variáveis; mostrar ao grupo a correspondência abaixo.

| Dimensão | Exemplo do documento | Variável correspondente | Observação |
|---|---|---|---|
| Probabilidade | Recorrência histórica | P1 | Perguntar se é diferente de frequência |
| | Frequência | P1 | — |
| | Intensidade das chuvas | Nenhum | Diferencia pouco 21 pontos na mesma RPA; sugestão: contexto no painel |
| | Relevo | P6 | Curvas da Condepe/Fidem podem tirar o P6 da condição |
| | Proximidade de canais | P4 | — |
| Exposição | População | E1 | — |
| | Equipamentos públicos | E2 | — |
| | Comércio | E3 | — |
| | Vias principais | I1 | Contar só no Impacto, para não repetir |
| Impacto | Interrupção do trânsito | I1 | — |
| | Hospitais/escolas atingidos | E2 | Contagem dupla se ficar também no Impacto. "Rota até hospital" já tinha sido descartada (resposta ao evento, do COP) |
| | Perdas econômicas | E3 | Sem fonte para perda; contagem dupla com o comércio |
| | Isolamento | Nenhum | Nova: comunidade sem rota alternativa. Medida possível pela malha viária |
| Vulnerabilidade | ZEIS | V3 (apoio) | Fonte localizada: ZEIS do Plano Diretor |
| | População vulnerável | V2 / V1 | — |
| | Dificuldade de evacuação | Nenhum | Nova; definição a pedir a Hellis |
| | Infraestrutura precária | V4 / I2 | Nova; definição a pedir a Hellis |

As variáveis P2 (severidade), P3 (maré), P5 (impermeabilização) e I2
(risco sanitário) não aparecem nos exemplos do documento; a recomendação é
mantê-los.

O comentário do documento sugere uma **matriz GUT** para o score. O cálculo
decidido em 02/10 é **Probabilidade × Consequência**; a recomendação é
mantê-lo, porque usa as próprias 4 dimensões do documento. Fica para o grupo
confirmar (pendência 14).

## Lista adotada em 03/10/2026 (Pedro)
Pedro decidiu trabalhar com a lista que junta o documento da Hellis à lista
de 02/10. Os códigos antigos foram mantidos (o painel lê as colunas pelo
código); as variáveis novas ganharam códigos novos. Escalas de nota, pesos e
validação pelo grupo continuam em aberto.

| Dimensão | Código | Variável | Situação |
|---|---|---|---|
| Probabilidade | P1 | Frequência e recorrência histórica | Manter (pendência 16) |
| | P2 | Severidade | Manter |
| | P3 | Influência da maré | Manter |
| | P4 | Proximidade de rio ou canal | Manter |
| | P5 | Impermeabilização | Manter |
| | P6 | Relevo (baixio) | Condicional: curvas da Condepe/Fidem a conferir |
| Exposição | E1 | População | Manter |
| | E2 | Equipamentos públicos | Manter; inclui "hospitais/escolas atingidos" |
| | E3 | Comércio e serviços | Manter; inclui "perdas econômicas" |
| Vulnerabilidade | V2 | População vulnerável | Manter |
| | V3 | ZEIS, favelas e comunidades | Manter |
| | V4 | Tipo de moradia | Manter; pode ir para o V6 |
| | V5 | Dificuldade de evacuação | **Nova**, sem definição nem escala (pendência 15) |
| | V6 | Infraestrutura precária | **Nova**, sem definição nem escala (pendência 15) |
| | V1 | IVS | Plano B |
| Impacto | I1 | Tipo de via | Manter; inclui "vias principais"; escala definida (abaixo) |
| | I2 | Risco sanitário | Manter; pode ir para o V6 |
| | I3 | Isolamento | **Nova**, sem definição nem escala (pendência 15) |

Intensidade das chuvas: contexto no painel, fora da nota.

### I1 — Tipo de via (escala definida por Pedro, 03/10/2026)
| Nota | Classe |
|---|---|
| 5 | Corredor de transporte metropolitano |
| 4 | Corredor de transporte urbano principal |
| 3 | Corredor de transporte urbano secundário |
| 2 | Demais avenidas |
| 1 | Ruas |

- Vale a via mais importante afetada; nos trechos, a própria via do trecho.
- A interdição registrada pela CTTU não soma ponto: serve só para conferir.
- Falta confirmar qual base classifica os corredores nessas três classes
  (pendência 17).
