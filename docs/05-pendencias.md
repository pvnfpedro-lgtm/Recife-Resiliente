# 5. Pendências e dados não verificados

## Decisões em aberto

| # | Pendência | Responsável | Prazo | Recomendação |
|---|---|---|---|---|
| 1 | Pesos de Exposição, Vulnerabilidade e Impacto na Consequência, e pesos das variáveis | Grupo | 14/10 | Comparar com o cenário de pesos iguais |
| 2 | Índice de vulnerabilidade social | Pedro | 14/10 | Usar o IVS/Ipea por UDH, que já é a malha prevista; registrar que ele usa base do Censo 2010 (**conferir**) |
| 3 | Bacia e sub-bacia de cada ponto | Pedro | 27/10 | Fazer interseção do ponto com a malha de bacias do Plano de Drenagem do Recife, se disponível (**confirmar a fonte**) |
| 4 | Conferência das coordenadas aproximadas | Pedro | 14/10 | Conferir os 21 pontos com a EMLURB e por imagem de satélite; marcar `coordenada_verificada = sim` |
| 5 | Quem faz as vistorias | Grupo | 27/10 | Definir antes da Etapa 4 |
| 6 | Escala da tratabilidade (5 = mais tratável) | Grupo | 14/10 | Confirmar a convenção adotada no script |
| 7 | Papel da SEPLAN e nome do contato | Pedro | 05/10 | Definir antes de enviar o convite |
| 8 | Probabilidade dos 21 pontos (sem ela não há risco) | Pedro | 08/10 | Ficha de 1 a 5 preenchida com Pedro Oliveira (EMLURB); confirmar com dados do COP |
| 9 | Variáveis de cada dimensão | Pedro | 05/10 | Lista de 13 em `07-revisao-variaveis.md`; confirmar dados no checklist `.xlsx` |
| 10 | Confirmar com a EMLURB: os 21 são todos os pontos da RPA 6? Que critério definiu os 6 prioritários? | Pedro | 08/10 | Perguntar na reunião com Pedro Oliveira |
| 11 | Pedir à URB a lista de obras de drenagem da RPA 6 | Pedro | 05/10 | Junto com os pedidos a COP e CTTU |
| 12 | Faixas de nota (1 a 5) de cada variável | Pedro | 05/10 | Começar pela Probabilidade (ficha da EMLURB) |
| 13 | Contagem dupla no documento de Hellis (hospitais/escolas, vias e comércio em duas dimensões) | Grupo | 14/10 | Exposição = o que está no círculo de 300 m; Impacto = efeito além do local. Ver `07-revisao-variaveis.md` |
| 14 | Score: matriz GUT (comentário no documento de Hellis) ou Probabilidade × Consequência (decidido em 02/10) | Grupo | 14/10 | Manter P × C |
| 15 | Variáveis novas do documento de Hellis: isolamento, dificuldade de evacuação, infraestrutura precária | Pedro e Hellis | 08/10 | Pedir a definição de cada uma a Hellis antes de procurar dado |
| 16 | Recorrência histórica × frequência: são diferentes? | Pedro e Hellis | 08/10 | Se forem a mesma coisa, ficam no P1 |
| 17 | I1: classe de corredor de cada via (metropolitano, urbano principal, urbano secundário) | Pedro | 13/10 | A classificação está no **Anexo 7 da LUOS (Lei 16.176/1996)**, segundo busca na web (anexo não aberto: site bloqueado no ambiente). Pedro envia a LUOS ou o anexo. Rascunho das notas em `dados/processados/notas_I1_tipo_de_via.csv`. Em 03/10 Pedro marcou na planilha: fonte de medição = Sistema viário (CTTU), fonte confirmada e dado existente |
| 18 | I4: montar a camada de infraestrutura crítica (metrô, delegacias, bombeiros, SAMU, aeroporto, subestações) e medir a distância dos 21 pontos | Pedro | 27/10 | Conferir se as notas se espalham; se quase todos ficarem acima de 2 km, I4 vira contexto. Decidir se entram terminais integrados, Compesa, Defesa Civil e abrigos |

## Dados não verificados
- I1 (Tipo de via): Av. Mascarenhas de Moraes e Av. Recife como corredores
  metropolitanos (nota 5) vêm de resumo de busca na web sobre o Anexo 7 da LUOS;
  o anexo não foi aberto. As outras 18 notas do I1 estão pendentes.
Tudo o que estiver aqui **não** pode ir para a apresentação sem conferência.

- Coordenadas dos 21 trechos da RPA 6: aproximadas.
- Papéis de cada órgão na prevenção (tabela em `01-contexto.md`): leitura
  preliminar.
- Ano-base do IVS/Ipea por UDH: a confirmar.
- Base do IPTU (portal de dados abertos): coordenadas, sistema de
  coordenadas, ano e categorias do tipo de empreendimento ainda não abertos
  nem conferidos.
- Limites territoriais (bairro, microrregião, RPA, logradouro): formatos,
  sistema de coordenadas e data de atualização ainda não conferidos.
- Faixas e corredores de ônibus: formato, sistema de coordenadas e data de
  atualização ainda não conferidos.
- Fluxo de veículos por hora: local dos pontos de medição, cobertura na
  RPA 6, coordenadas e período ainda não conferidos.
- Imóveis Especiais de Preservação (IEPs): formato, geometria e data de
  atualização ainda não conferidos; uso no modelo a decidir com o grupo.
- Favelas, cortiços e loteamentos irregulares: se há geometria, ano de
  referência e coerência com a malha IBGE 2022 ainda não conferidos.
- ZEC (zoneamento do Plano Diretor): significado da sigla, geometria e data
  ainda não conferidos; uso no modelo a definir.
- Bases localizadas na busca em 03/10/2026 (escolas municipais, UBS,
  hospitais, rede de saúde, ZEIS, bacias e sub-bacias, drenagem da EMLURB,
  curvas da Condepe/Fidem): formatos, datas e coberturas vêm só dos resumos
  da busca; nenhum arquivo foi aberto. A data de 2020 das escolas municipais
  precisa ser conferida.
- Produtos do IBGE 2022 (Grade Estatística, CNEFE, agregados por setor):
  existência confirmada na busca, arquivos ainda não abertos.
- Malha de favelas e comunidades 2022, tipo de domicílio por setor, curvas de
  nível no ESIG e MapBiomas: não verificados.
