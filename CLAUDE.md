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

## Como trabalhar
- Seja direto, recomende em vez de listar opções.
- Avise sempre que um dado não estiver verificado. Registre-o em
  `docs/05-pendencias.md`.
- Não invente critérios, pesos, coordenadas nem números. Se faltar o dado,
  deixe o campo vazio e marque como pendente.
- Escreva em português.
- SIG: SIRGAS 2000 / UTM 25S (EPSG:31985); buffer de 300 m por ponto.
- Testes: `python3 -m unittest discover -s tests`.
