# 8. Painel

## Base (decidido por Pedro em 02/10/2026)
O painel em Google Apps Script já existente é a base. Muita coisa vai mudar.

- Código: pasta `appscript/` (cópia baixada com `clasp`, projeto
  `1Om9PIGQQrIXZ9cTFqbv_iLv9DIvyGW3AbJEDejtEU2SC9PbKDbUVuIFr`).
- Web app (`doGet`) com ArcGIS Maps SDK 4.29, que carrega um WebMap do portal
  ESIG (`esigportal2.recife.pe.gov.br`, item `df725ec964b840a1afbc348ae4555c20`).
- Abas atuais: 01 Panorama · 02 Físico-Financeiro · 03 Ficha do Ponto.
- Os dados atuais são ilustrativos (8 obras fictícias), escritos no código.

## Decisões
| Tema | Decisão |
|---|---|
| Obras fictícias | Ficam por enquanto |
| Notas pelo Google Sheets | Ainda não |
| Acesso ao painel | A definir |
| Pontos críticos | Pedro vai subir um mapa novo no ArcGIS com os pontos |
| Pontos críticos no painel | Teste: o painel lê a aba "Notas dos pontos" da planilha Google Sheets `1DN3abWIPk0dvOkh-28D2NGYBLgMI437Vx7Sk7TqpDc0` e mostra os pontos com popup |
| Rede hidrográfica | Removida do código (`HidroData.html`); virá das camadas do ArcGIS |

## Implantações
- **Teste (HEAD, sempre o código mais recente):**
  https://script.google.com/macros/s/AKfycbwHvKBxXuhdg200oKKwCvdF4uZPHBWsiEE9kTqK5TI/dev
  (só abre para quem é editor do projeto).
- Versões publicadas: 9 implantações; a mais recente é a @9 "Primeira versão
  que deu certo". O `clasp push` não altera nenhuma delas.
- 02/10/2026: primeiro `clasp push` (pontos críticos lidos da planilha,
  sem HidroData).
- 03/10/2026: `clasp push` com os subcritérios de 03/10 (nomes novos; I3, V5
  e V6) e a função única `atualizarSubcriterios0310`, executada por Pedro no
  editor. Aba "Notas dos pontos" conferida: 7 cabeçalhos renomeados, V5 e V6
  antes do V1, I3 antes do I2 (ordem I1, I3, I2), colunas novas sem nota e
  sem peso, "Notas preenchidas" = 15 nos 21 pontos, risco calculado nos 21.
  Fórmulas escritas por script não usam separador de argumentos (planilha em
  pt-BR usa `;`).

## Estado em 02/10/2026 (aprovado por Pedro)
- Paleta: #0869A6 · #2685BF · #5496BF · #FFFFFF · #F2F2F2 (painel inteiro).
- Pontos críticos lidos da planilha Google Sheets, cor pelo índice de risco.
- Cartão do ponto (no lugar do popup do ArcGIS): abre à direita do ponto,
  centralizado na altura dele, a 36 px; estilo da ficha do Plano de Ações
  de SP; sem número do ponto; nível de risco em palavras; tabela critério/
  subcritério × avaliação; botões Aproximar e Street View.

## Em aberto
- Cores do nível de risco: manter verde/amarelo/laranja/vermelho ou usar
  tons de azul.
- Liberar `*.arcgis.com` e `esigportal2.recife.pe.gov.br` na rede do
  ambiente para testar o painel antes de cada envio.

## Como trabalhar no código
1. Editar os arquivos em `appscript/`; cada mudança vira um commit.
2. Enviar ao Apps Script com `clasp push` **só depois da aprovação de Pedro**.
3. Testar pela URL de teste (Implantar → Testar implantações); o link
   publicado só muda quando Pedro publicar uma nova versão.

## Camadas para o ArcGIS (`dados/processados/arcgis/`)
- `pontos_criticos_rpa6.geojson` / `.csv`: os 21 pontos com atributos.
- `buffer_300m_rpa6.geojson` e `buffer_1000m_rpa6.geojson`: círculos.
- Coordenadas ainda aproximadas.

## Pontos de atenção do painel atual
- A "Matriz de risco" da aba 02 é atraso × severidade das obras, não
  Probabilidade × Consequência. Renomear ou separar quando o risco entrar.
- `access: ANYONE`: se o WebMap do ESIG exigir login, quem não tiver acesso
  pode ver o mapa vazio (não testado).
- `GOOGLE_MAPS_EMBED_KEY` vazio: Street View e modo Google Maps mostram aviso.
