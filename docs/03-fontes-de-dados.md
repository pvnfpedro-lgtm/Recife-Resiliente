# 3. Fontes de dados

A lista detalhada por subcritério está na aba *Fontes de dados* da planilha de
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
| IPTU — contribuintes (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso IPTU](https://dados.recife.pe.gov.br/dataset/imposto-predial-e-territorial-urbano-iptu/resource/9a847338-92a6-4b74-b3e8-c8f8b57aff2d) | A confirmar | E2 Usos expostos (coluna de tipo de empreendimento); talvez impermeabilização (áreas de terreno e construída) | Localizada por Pedro em 03/10/2026; **não conferida** | Segundo Pedro, traz os imóveis georreferenciados. Conferir: nome das colunas de coordenada, sistema de coordenadas, ano de referência, categorias do tipo de empreendimento e se há dado pessoal |
| Limites e divisões territoriais: bairro, microrregião, RPA e logradouro (Prefeitura do Recife) | [dados.recife.pe.gov.br — mapas de limites e divisões territoriais](https://dados.recife.pe.gov.br/dataset/mapas-de-limites-e-divisoes-territoriais) | A confirmar | Recorte da RPA 6, bairro de cada ponto, base do mapa; logradouros ajudam a conferir as coordenadas aproximadas (pendência 4) | Localizada por Pedro em 03/10/2026; **não conferida** | Conferir formatos disponíveis (SHP/GeoJSON/KML), sistema de coordenadas e data de atualização |
| Faixas e corredores de ônibus (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso faixas e corredores de ônibus](https://dados.recife.pe.gov.br/dataset/faixas-e-corredores-de-onibus/resource/4cee8c9a-681f-4e88-a347-0142e449e3fc) | A confirmar | Impacto: Mobilidade afetada (corredor ou faixa de ônibus a até 300 m do ponto) | Localizada por Pedro em 03/10/2026; **não conferida** | Complementa, não substitui, a hierarquia viária e as linhas de ônibus pedidas à CTTU (Antônio). Conferir formato, sistema de coordenadas e data de atualização |
| Fluxo de veículos por hora (Prefeitura do Recife) | [dados.recife.pe.gov.br — recurso fluxo de veículos por hora](https://dados.recife.pe.gov.br/dataset/fluxo-de-veiculo-por-hora/resource/e019893b-c054-4c1b-819f-fdf9b56399d6) | A confirmar | Impacto: Mobilidade afetada (volume de tráfego na via do ponto ou próxima a ele) | Localizada por Pedro em 03/10/2026; **não conferida** | Conferir de onde vem a contagem (pontos de medição), se há pontos de medição na RPA 6 perto dos 21 trechos, se há coordenadas, o período coberto e a data de atualização |
| Imóveis Especiais de Preservação — IEPs (Prefeitura do Recife) | [dados.recife.pe.gov.br — IEPs](https://dados.recife.pe.gov.br/dataset/imoveis-especiais-de-preservacao-ieps) | A confirmar | **Uso a definir com o grupo.** Não corresponde a nenhum dos 13 subcritérios. Sugestão: coluna de contexto no painel (patrimônio exposto no raio de 300 m) | Localizada por Pedro em 03/10/2026; **não conferida** | Conferir formato, se há coordenadas ou polígonos, sistema de coordenadas e data de atualização |
| Relação das favelas, cortiços e loteamentos irregulares (Prefeitura do Recife) | [dados.recife.pe.gov.br — favelas, cortiços e loteamentos irregulares](https://dados.recife.pe.gov.br/dataset/relacao-das-favelas-corticos-e-loteamentos-irregulares) | A confirmar | V3 Favelas e comunidades: complemento ou alternativa municipal à malha IBGE 2022 | Localizada por Pedro em 03/10/2026; **não conferida** | Pelo nome, pode ser só uma lista (sem geometria). Conferir se há polígonos ou coordenadas, sistema de coordenadas, ano de referência e se bate com a malha de favelas e comunidades do IBGE 2022 |

### A procurar
- Equipamentos: escolas, creches, unidades de saúde, hospitais/UPA.
- Rede de drenagem, canais e bacias (pendência 3).
- Curvas de nível ou altimetria.
- ZEC do Plano Diretor: link e significado da sigla a confirmar com Pedro.
- ZEIS do Plano Diretor (possível apoio ao V3).
- Lotes e quadras do cadastro imobiliário (só se o IPTU não trouxer coordenadas).

## Regras
- O arquivo original vai para `dados/brutos/<fonte>/` e não é editado.
  Registre a data de download e o link.
- Toda base precisa estar em **EPSG:31985** antes do cruzamento com os
  buffers.
- Dados pessoais (por exemplo, endereço de quem fez um chamado) **não** entram
  no repositório.
