# Recife Resiliente — instruções para o Claude

## Contexto
Desafio estratégico do Programa Primeira Liderança / Rede GGOV Recife
(consultoria Motriz). Equipe de 6 servidores municipais; tutora: Ana Paula
Silva de Barros Souza (Unidade de Governança / CGM). Pedro cuida de dados,
território, causas de infraestrutura e cronograma.

Problema: alagamentos no Recife. O recorte é a gestão integrada de risco de
alagamento: priorizar territórios críticos por risco (probabilidade +
exposição + vulnerabilidade + impacto) e articular a prevenção entre COP,
EMLURB, Defesa Civil, URB, CTTU, Compesa, ProMorar e SEPLAG. A solução não é
obra, é prevenção priorizada por risco. A resposta ao evento é do COP.

Etapa atual: hierarquização de pontos críticos na RPA 6 (21 trechos da
EMLURB), adaptando os critérios do Plano Diretor de Drenagem de São Paulo
(FCTH/SIURB). Decidido: 4 critérios (Probabilidade, Exposição,
Vulnerabilidade, Impacto), risco = Probabilidade × Consequência (1–25),
buffer de 300 m no score e 1 km no painel. Detalhes em
`docs/02-metodologia-hierarquizacao.md`.

Arquivo de trabalho da equipe:
`dados/Recife_Resiliente_RPA6_Criterios_Pontos_Criticos.xlsx`, com as abas Leia-me,
Critérios, Fontes de dados e Pontos RPA 6.

## Estado atual (02/10/2026)
- **Modelo:** 13 subcritérios + P6 (condicional) e V1 (plano B) + I3, V5 e
  V6 (novas, do documento da Hellis, sem definição: pendência 15), escalas de
  nota, pesos de teste e cálculo em
  `dados/Recife_Resiliente_Checklist_Subcriterios.xlsx` (gerado por
  `scripts/gerar_checklist_subcriterios.py`). Índice de risco 0–1 =
  (Risco − 1) ÷ 24.
- **Documento-chave dos critérios e subcritérios:**
  `docs/10-criterios-e-subcriterios.md`. Toda decisão sobre critério,
  subcritério ou escala é registrada nele primeiro. O Google Docs
  `12zj_bPx0u5ejNpUsbFNEPsy7WGpTRwuH6k23O0k8f2I` é cópia para a equipe
  ler e comentar; atualizar a partir do Markdown quando Pedro pedir.
- **Planilha oficial das notas (Google Sheets nativa):**
  `1DN3abWIPk0dvOkh-28D2NGYBLgMI437Vx7Sk7TqpDc0`, aba "Notas dos pontos".
  As notas atuais são de TESTE (`=RANDBETWEEN(1,5)`); mudam a cada recálculo.
- **Painel:** Google Apps Script em `appscript/` (projeto
  `1Om9PIGQQrIXZ9cTFqbv_iLv9DIvyGW3AbJEDejtEU2SC9PbKDbUVuIFr`), enviado com
  `clasp push` só após aprovação de Pedro. URL de teste e decisões em
  `docs/08-painel.md`. O painel lê a planilha e mostra os 21 pontos com um
  cartão próprio (à direita do ponto). Paleta: #0869A6 · #2685BF · #5496BF ·
  #FFFFFF · #F2F2F2. Obras fictícias mantidas por enquanto.
- **clasp:** a credencial fica só na sessão em que foi feito o login. Numa
  sessão nova é preciso `npm i -g @google/clasp` e `clasp login --no-localhost`
  (Pedro autoriza e cola a URL `http://localhost:8888/?...`).
- **Rede do ambiente:** `docs.google.com` e `*.googleusercontent.com`
  liberados (leitura da planilha por export). O ArcGIS (`*.arcgis.com`,
  `esigportal2.recife.pe.gov.br`) ainda está bloqueado: não dá para testar o
  mapa aqui.
- **PR aberto:** pvnfpedro-lgtm/Recife-Resiliente#1 (branch
  `claude/dreamy-pasteur-j7phpz`).

## Próximos passos (escolha de Pedro)
1. Indicadores e ranking dos pontos críticos na aba 01 do painel.
2. Lista de conferência das coordenadas (11 "Aproximado").
3. Ficha da reunião com a EMLURB (P1, P2, P3 dos 21 pontos).
4. Pendências gerais em `docs/05-pendencias.md`.

## Como trabalhar
- Seja direto, recomende em vez de listar opções. Vá com calma: uma etapa
  por vez, confirmando com Pedro antes de avançar.
- Avise sempre que um dado não estiver verificado. Registre-o em
  `docs/05-pendencias.md`.
- Não invente critérios, pesos, coordenadas nem números. Se faltar o dado,
  deixe o campo vazio e marque como pendente.
- Escreva em português.
- SIG: SIRGAS 2000 / UTM 25S (EPSG:31985); buffer de 300 m por ponto.
- Testes: `python3 -m unittest discover -s tests`.
