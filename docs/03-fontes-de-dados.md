# 3. Fontes de dados

A lista detalhada por variável está na aba *Fontes de dados* da planilha de
trabalho. Esta tabela é o resumo. A coluna *Situação* deve ser atualizada à
medida que cada base for obtida e conferida.

| Fonte | Uso previsto | Unidade espacial | Situação |
|---|---|---|---|
| IBGE — Censo 2022 | População, domicílios, densidade, características do entorno | Setor censitário | A obter |
| Ipea — IVS (Atlas da Vulnerabilidade Social) | Vulnerabilidade social | UDH | A obter; ver pendência sobre o índice |
| Prefeitura do Recife (dados abertos / ESIG) | Equipamentos públicos, uso do solo, limites de bairro e RPA | Diversas | A obter |
| EMLURB | Lista dos 21 trechos críticos da RPA 6; manutenção da drenagem | Ponto/trecho | Planilha recebida, coordenadas aproximadas |
| COP | Histórico de ocorrências de alagamento | Ponto | A obter |
| Cemaden | Pluviometria; áreas de risco | Estação / polígono | A obter |
| Compesa | Rede de esgoto; extravasamentos | Rede / ponto | A obter |

## Catálogo de bases localizadas
Onde encontrar cada base. Aqui ficam **só os links**: os arquivos destas
bases não são guardados no repositório (decisão de Pedro, 03/10/2026). Uma
linha por conjunto encontrado; a *Situação* só
passa a "Conferida" depois de abrir o arquivo e checar colunas e sistema de
coordenadas.

| Base | Onde encontrar | Formato | Uso no modelo | Situação | Observações |
|---|---|---|---|---|---|
| IPTU — contribuintes (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso IPTU](https://dados.recife.pe.gov.br/dataset/imposto-predial-e-territorial-urbano-iptu/resource/9a847338-92a6-4b74-b3e8-c8f8b57aff2d) | A confirmar | E3 Atividade econômica (coluna de tipo de empreendimento); talvez impermeabilização (áreas de terreno e construída) | Localizada por Pedro em 03/10/2026; **não conferida** | Segundo Pedro, traz os imóveis georreferenciados. Conferir: nome das colunas de coordenada, sistema de coordenadas, ano de referência, categorias do tipo de empreendimento e se há dado pessoal |
| Limites e divisões territoriais: bairro, microrregião, RPA e logradouro (Prefeitura do Recife) | [dados.recife.pe.gov.br — mapas de limites e divisões territoriais](https://dados.recife.pe.gov.br/dataset/mapas-de-limites-e-divisoes-territoriais) | A confirmar | Recorte da RPA 6, bairro de cada ponto, base do mapa; logradouros ajudam a conferir as coordenadas aproximadas (pendência 4) | Localizada por Pedro em 03/10/2026; **não conferida** | Conferir formatos disponíveis (SHP/GeoJSON/KML), sistema de coordenadas e data de atualização |
| Faixas e corredores de ônibus (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso faixas e corredores de ônibus](https://dados.recife.pe.gov.br/dataset/faixas-e-corredores-de-onibus/resource/4cee8c9a-681f-4e88-a347-0142e449e3fc) | A confirmar | Impacto: Mobilidade afetada (corredor ou faixa de ônibus a até 300 m do ponto) | Localizada por Pedro em 03/10/2026; **não conferida** | Complementa, não substitui, a hierarquia viária e as linhas de ônibus pedidas à CTTU (Antônio). Conferir formato, sistema de coordenadas e data de atualização |
| Fluxo de veículos por hora (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso fluxo de veículos por hora](https://dados.recife.pe.gov.br/dataset/fluxo-de-veiculo-por-hora/resource/e019893b-c054-4c1b-819f-fdf9b56399d6) | A confirmar | Impacto: Mobilidade afetada (volume de tráfego na via do ponto ou próxima a ele) | Localizada por Pedro em 03/10/2026; **não conferida** | Conferir de onde vem a contagem (pontos de medição), se há pontos de medição na RPA 6 perto dos 21 trechos, se há coordenadas, o período coberto e a data de atualização |
| Imóveis Especiais de Preservação — IEPs (Prefeitura do Recife) | [dados.recife.pe.gov.br — IEPs](https://dados.recife.pe.gov.br/dataset/imoveis-especiais-de-preservacao-ieps) | A confirmar | **Uso a definir com o grupo.** Não corresponde a nenhum das 13 variáveis. Sugestão: coluna de contexto no painel (patrimônio exposto no raio de 300 m) | Localizada por Pedro em 03/10/2026; **não conferida** | Conferir formato, se há coordenadas ou polígonos, sistema de coordenadas e data de atualização |
| Relação das favelas, cortiços e loteamentos irregulares (Prefeitura do Recife) | [dados.recife.pe.gov.br — favelas, cortiços e loteamentos irregulares](https://dados.recife.pe.gov.br/dataset/relacao-das-favelas-corticos-e-loteamentos-irregulares) | A confirmar | V3 Favelas e comunidades: complemento ou alternativa municipal à malha IBGE 2022 | Localizada por Pedro em 03/10/2026; **não conferida** | Pelo nome, pode ser só uma lista (sem geometria). Conferir se há polígonos ou coordenadas, sistema de coordenadas, ano de referência e se bate com a malha de favelas e comunidades do IBGE 2022 |
| Zoneamento do Plano Diretor — recurso ZEC (Prefeitura do Recife) | [dados.recife.pe.gov.br — zoneamento, recurso ZEC](https://dados.recife.pe.gov.br/dataset/zoneamento/resource/f3076b94-d226-4e07-baea-a97f58b67884) | A confirmar | **Uso a definir.** Se a ZEC for zona de centralidade (comércio e serviços), reforça o E3 Atividade econômica | Localizada por Pedro em 03/10/2026; **não conferida** | Significado da sigla ZEC a confirmar no Plano Diretor. O conjunto *zoneamento* tem outros recursos: ver se inclui ZEIS (apoio ao V3) |
| Rede de Educação Municipal — escolas municipais (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso escolas municipais](http://dados.recife.pe.gov.br/dataset/rede-de-educacao-municipal/resource/41f377fc-8b36-4115-acbc-0f4645f7a6ff) | GeoJSON (segundo a busca) | E2 Equipamentos sensíveis (escolas) | Localizada na busca (Claude) em 03/10/2026; **não conferida** | A busca indica última atualização em 19/02/2020 (**conferir**). Só rede municipal: escolas estaduais e privadas ficam pelo CNEFE. Ver se as creches estão incluídas; há também a [lista de conjuntos com a tag creche](https://dados.recife.pe.gov.br/dataset?tags=Localiza%C3%A7%C3%A3o&res_format=GeoJSON&tags=creche) |
| Unidades Básicas de Saúde — UBS (Prefeitura do Recife) | [dados.recife.pe.gov.br — UBS](https://dados.recife.pe.gov.br/dataset/unidades-basica-de-saude) | CSV (segundo a busca) | E2 Equipamentos sensíveis (unidades de saúde) | Localizada na busca (Claude) em 03/10/2026; **não conferida** | Conferir se o CSV tem coordenadas ou só endereço |
| Hospitais (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso hospitais](http://dados.recife.pe.gov.br/dataset/hospitais/resource/a2dab4d4-3a7b-4cce-b3a7-dd7f5ef22226) | A confirmar | E2 Equipamentos sensíveis (hospital/UPA leva à nota 5) | Localizada na busca (Claude) em 03/10/2026; **não conferida** | Conferir se inclui UPA, coordenadas e data de atualização |
| Rede de saúde municipal e rede de atenção à saúde (Prefeitura do Recife) | [dados.recife.pe.gov.br — conjuntos de Saúde em GeoJSON](https://dados.recife.pe.gov.br/dataset?res_format=GeoJSON&tags=Sa%C3%BAde); [rede de atenção à saúde](https://dados.recife.pe.gov.br/dataset/rede-de-atencao-a-saude-no-recife) | GeoJSON, JSON (segundo a busca) | E2 Equipamentos sensíveis (policlínicas, USF, maternidades, hospitais) | Localizada na busca (Claude) em 03/10/2026; **não conferida** | Pode reunir UBS, USF e hospitais num só arquivo; escolher uma base para não contar duas vezes |
| ZEIS — zoneamento do Plano Diretor (Prefeitura do Recife) | [dados.recife.pe.gov.br — zoneamento, recurso ZEIS](https://dados.recife.pe.gov.br/dataset/zoneamento/resource/cffaefb3-0b8d-4e56-81c4-4dbdefbbd876) | GeoJSON (segundo a busca) | V3 Favelas e comunidades: apoio (ZEIS 1 = assentamentos de baixa renda) | Localizada na busca (Claude) em 03/10/2026; **não conferida** | Plano Diretor de 2020 (Lei 18.770/2020). ZEIS 2 são terrenos vazios: separar as duas. Também no ESIG: [MA_PlanoDiretor, camada 3](https://esigportal2.recife.pe.gov.br/arcgis/rest/services/MeioAmbiente/MA_PlanoDiretor/FeatureServer/3) |
| Bacias e sub-bacias (ESIG, Prefeitura do Recife) | [esigportal2 — MeioAmbiente/PCR_BaciasESubBacias](https://esigportal2.recife.pe.gov.br/arcgis/rest/services/MeioAmbiente/PCR_BaciasESubBacias/MapServer) | Serviço ArcGIS (MapServer) | Pendência 3 (bacia e sub-bacia de cada ponto); ligação ponto–obra | Localizada na busca (Claude) em 03/10/2026; **não conferida** | Conferir se é a malha do Plano de Drenagem e se permite exportar |
| Bases de drenagem da EMLURB (ESIG) | [esigportal2 — Emlurb/BASES_DRENAGEM_RECIFE_MI](https://esigportal2.recife.pe.gov.br/arcgis/rest/services/Emlurb/BASES_DRENAGEM_RECIFE_MI/MapServer) | Serviço ArcGIS (MapServer) | P4 Proximidade de rio ou canal; diagnóstico de causa | Localizada na busca (Claude) em 03/10/2026; **não conferida** | Camada 0 "Elementos da Rede". Conferir se tem canais e galerias, e se dá para consultar e exportar. Perguntar à EMLURB sobre atualização |
| Curvas de nível — Acervo Cartográfico (Condepe/Fidem) | [Condepe/Fidem — Acervo Cartográfico Virtual](http://www.condepefidem.pe.gov.br/web/condepe-fidem/acervo-cartografico-virtual) | A confirmar | P6 Baixio (condicional) | Localizada na busca (Claude) em 03/10/2026; **não conferida** | Segundo a busca: 1:10.000 com curvas a cada 5 m na RMR e 1:2.000 com curvas a cada 1 m na área urbana. Conferir ano do levantamento, formato e se cobre a RPA 6 |

### A procurar
- Creches: confirmar se estão na rede de educação municipal ou em conjunto próprio.
- Unidades de saúde da rede estadual (UPA e hospitais estaduais): conferir se estão nas bases da Prefeitura; senão, CNES/DATASUS.
- Lotes e quadras do cadastro imobiliário (só se o IPTU não trouxer coordenadas).

## Regras
- O arquivo original vai para `dados/brutos/<fonte>/` e não é editado.
  Registre a data de download e o link.
- Toda base precisa estar em **EPSG:31985** antes do cruzamento com os
  buffers.
- Dados pessoais (por exemplo, endereço de quem fez um chamado) **não** entram
  no repositório.
