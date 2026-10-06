# 11. Metodologia de gestão de riscos de alagamento (proposta)

> **Proposta de 06/10/2026 (Claude), ainda não aprovada por Pedro nem pelo
> grupo.** Enquadra o trabalho no processo de gestão de riscos do TCU, sem
> mudar o cálculo decidido em 02/10 (`02-metodologia-hierarquizacao.md`).

## Referência
TRIBUNAL DE CONTAS DA UNIÃO. *Referencial básico de gestão de riscos*.
Brasília: TCU, Segecex, 2018. 154 p. O referencial segue o processo da
ABNT NBR ISO 31000:2009 (figura 6, p. 23).

Arquivo lido por Claude no Drive de Pedro em 06/10/2026
(`Referencial_basico_gestao_riscos.pdf`). Páginas conferidas no texto
extraído do PDF.

## O que o referencial diz e como usamos

| No TCU | Página | No Recife Resiliente |
|---|---|---|
| Risco é "a possibilidade de ocorrência de eventos que afetem a realização ou alcance dos objetivos, combinada com o impacto dessa ocorrência" | 8 | Evento = alagamento no ponto crítico; objetivo = proteger pessoas, serviços e mobilidade |
| "O risco é uma função tanto da probabilidade como da medida das consequências" | 25 | Probabilidade (P) e Consequência (C = Exposição, Vulnerabilidade e Impacto) |
| Em métodos semiquantitativos, "a função 'Risco' será essencialmente um produto dessas variáveis": **Risco = Probabilidade × Impacto** | 26 | **Risco = P × C**, de 1 a 25 (já decidido em 02/10) |
| Escalas de probabilidade e de impacto definidas antes da análise, "compatível com o contexto" | 24 e 27 | Notas de 1 a 5 por variável, com faixas próprias de cada uma |
| Classificação do nível de risco em faixas (baixo, médio, alto, extremo) | 28 | **Novo:** faixas de risco para os 21 pontos (a definir pelo grupo) |
| Risco inerente × residual: residual = inerente × (1 − confiança nos controles) | 29 a 31 | **Não aplicar no score** (ver "Cuidado" abaixo); usar no tratamento |
| Diretrizes de priorização por nível de risco | 32 | Matriz risco × tratabilidade e ações por faixa |
| Opções de tratamento: evitar, reduzir, compartilhar, aceitar | 33 | Prevenção pelos órgãos: reduzir P ou reduzir C |
| Monitoramento e análise crítica; registro de riscos atualizado | 35 | Recalcular após cada estação chuvosa |

## As 7 etapas aplicadas aos pontos críticos

### 1. Comunicação e consulta (todas as etapas)
- **Partes interessadas:** COP, EMLURB, Defesa Civil, URB, CTTU, Compesa,
  ProMorar, SEPLAN e SEPLAG; tutora na CGM.
- **Produto:** quem informa cada variável e quem age em cada ponto. O TCU
  sugere matriz RACI ou de responsabilidades (p. 24).
- **Já em curso:** reunião com a EMLURB (P1 a P3), SEPLAN (E1 a E3, V1 a V3),
  CTTU (I1).

### 2. Estabelecimento do contexto
- **Objetivo:** priorizar a prevenção de alagamentos pelo risco, na RPA 6.
- **Escopo:** 21 trechos da EMLURB; círculo de 300 m (E3: 1 km).
- **Critérios de risco**, que o TCU pede para fixar nesta etapa (p. 24):
  escalas de nota das variáveis, pesos, faixas de risco e regra de
  priorização. Hoje: escalas em `10-dimensoes-e-variaveis.md`; pesos e
  faixas pendentes.

### 3. Identificação dos riscos
- Cada ponto crítico é um risco registrado. O TCU pede, para cada risco,
  "fonte de risco, as causas, o evento e as consequências" (p. 25).
- **Produto:** ficha do ponto, com causa do alagamento (diagnóstico de
  causa, fora do score) e o que é atingido.

### 4. Análise dos riscos
- Método **semiquantitativo** (p. 25): notas de 1 a 5 → nota de cada
  dimensão → **Risco = P × C**.
- **Produto:** aba "Notas dos pontos" = registro de riscos com nível
  calculado (equivale ao quadro 5 do TCU, p. 28).

### 5. Avaliação dos riscos
- Comparar o risco de cada ponto com as faixas definidas no contexto e
  decidir quais pontos recebem tratamento e em que ordem (p. 32).
- **Produto:** ranking, faixa de risco e quadrante da matriz risco ×
  tratabilidade.

### 6. Tratamento dos riscos
Opções do TCU (p. 33) traduzidas para alagamento:

| Opção | Exemplo no ponto crítico |
|---|---|
| Reduzir a probabilidade | Limpeza e desobstrução da drenagem (EMLURB), obra de drenagem (URB) |
| Reduzir a consequência | Alerta antecipado (COP, Defesa Civil), desvio de tráfego (CTTU), rota de fuga |
| Compartilhar | Ação conjunta entre órgãos (ProMorar, Compesa) |
| Aceitar | Risco baixo: só monitorar |

- **Produto:** plano de tratamento por ponto, com órgão responsável e prazo.

### 7. Monitoramento e análise crítica
- Atualizar as notas e o ranking após cada estação chuvosa e quando uma obra
  for concluída (p. 35: manter o registro de riscos atualizado).
- **Produto:** painel com o histórico do ranking.

## Cuidado: risco inerente × residual
O TCU separa o risco antes dos controles (inerente) do risco depois deles
(residual = inerente × risco de controle, p. 31). No nosso modelo, a
Probabilidade vem do **histórico de alagamentos**, que já reflete a drenagem
e a manutenção existentes. Ou seja, o risco calculado já é, na prática, o
**residual atual**. Aplicar de novo o fator de controle contaria a drenagem
duas vezes.

Proposta: manter o score como está e usar a ideia de residual só no
tratamento, para estimar quanto o risco cairia com uma obra ou ação prevista.

## Diferenças em relação ao exemplo do TCU
O exemplo do TCU (quadros 1 e 2, p. 27) usa pesos **1, 2, 5, 8 e 10** nas
escalas, o que leva o risco a 1–100. O nosso modelo usa notas **1 a 5**
(risco 1–25). O próprio TCU diz que as escalas são exemplos e devem ser
"construídas de modo compatível com o contexto" (p. 27). Recomendo manter
1 a 5, porque as notas vêm de dados medidos, e não converter.

## Pendências desta proposta
1. Pedro aprovar o enquadramento nas 7 etapas.
2. Grupo definir as **faixas de risco** (baixo, médio, alto, extremo) na
   escala de 1 a 25 e a ação esperada em cada uma (TCU, quadros 3 e 8). Não
   há proposta de cortes: o único corte decidido é o da matriz (risco 9).
3. Montar a matriz de responsabilidades (quem informa e quem age).
