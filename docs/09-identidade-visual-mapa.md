# 9. Identidade visual do mapa (ícones)

## Decidido (02/10/2026)
- **Estilo C — forma por grupo.** Todos os ícones em grafite (#334155) com
  desenho branco e contorno branco; a **forma** indica o grupo:
  - **Círculo:** risco (ponto crítico). Única cor forte: segue o índice de
    risco, do verde ao vermelho, igual ao painel.
  - **Quadrado arredondado:** drenagem (canal, reservatório etc.).
  - **Losango:** equipamentos sensíveis (escola, hospital etc.).
- Motivo: o grupo é reconhecido pela forma, mesmo com o ícone pequeno ou por
  quem não distingue bem as cores, e mantém a regra do painel (só o risco
  tem cor).
- **Formato:** SVG (símbolo personalizado no ArcGIS), com PNG de reserva.

## Ponto crítico (decidido em 03/10/2026)
- Desenho: **gota com onda** (gota da Maki + onda), em círculo.
- Pedro vai usar **um único símbolo** no ArcGIS. Versão única em vermelho
  #e31a1c: `mapa/icones/ponto_critico.svg` e `png/ponto_critico_64/128.png`.
- Sugestão: mostrar o risco pelo **tamanho** do símbolo (índice de risco),
  já que a imagem tem uma cor só. Escala de cor por classe (amarelo → vinho)
  fica como alternativa, com 4 imagens.

## Drenagem (proposta de 06/10/2026, a aprovar)
- Quadrado arredondado em grafite, desenho branco. Desenhos próprios (não há
  na Maki/Temaki): canal (três ondas), galeria (terreno e tubo em corte com
  água), reservatório (bacia com água), estação de bombeamento (símbolo de
  bomba: círculo com triângulo), comporta (porta com barra de içamento, água
  alta de um lado e baixa do outro).
- Arquivos: `mapa/icones/drenagem_*.svg` e `png/drenagem_*_64/128.png`,
  gerados por `scripts/gerar_icones_drenagem.py`. Prévia:
  `mapa/icones/previa_drenagem.png`.
- Teste sobre o mapa base cinza (06/10): o grafite tem contraste de cerca
  de 9:1 com o fundo e o vermelho do ponto crítico se destaca. Manter as
  cores; não pintar a drenagem de azul (só o risco tem cor). Usar **no
  mínimo 32 px** no ArcGIS: em 28 px, galeria, comporta e bombeamento ficam
  difíceis de ler. Imagem: `mapa/icones/teste_fundo_cinza.png`.

## Obras (proposta de 06/10/2026, a aprovar)
- Forma do grupo: **hexágono**. Símbolo: cone de obra. Situações iguais às
  do painel (Em obra, Em licitação, Concluído), mostradas sem cor:
  - **Em obra:** hexágono grafite cheio, cone branco.
  - **Em licitação:** hexágono vazado (branco, borda grafite), cone grafite.
  - **Concluído:** hexágono grafite cheio, sinal de feito (✓) branco.
- Arquivos: `mapa/icones/obra_*.svg` e `png/obra_*_64/128.png`, gerados por
  `scripts/gerar_icones_obras.py`. Prévia sobre o mapa base cinza:
  `mapa/icones/previa_obras.png`.

## Obras por tipo (proposta de 07/10/2026, a aprovar)
- Pedido de Pedro: o ponto da obra muda de desenho conforme o tipo. O
  **hexágono** continua sendo a forma do grupo Obras; o **desenho de dentro**
  mostra o tipo. A situação aparece sem cor: **cheio** (grafite, desenho
  branco) para em obra, concluído ou sem informação; **vazado** (branco,
  borda e desenho grafite) para em licitação.
- Seis categorias, a partir da coluna `tipo` da aba "Obras":

| Categoria | Tipos da planilha | Desenho |
|---|---|---|
| canal | Canal; Perfilamento do Rio Tejipió | três ondas (igual à drenagem) |
| dragagem | Dragagem | braço e caçamba sobre o sedimento, água em cima |
| reservatorio | Reservatórios de detenção; microrreservatório | bacia com água (igual à drenagem) |
| dique | Diques e comportas | aterro em trapézio, água alta de um lado e baixa do outro |
| parque | Parques alagáveis | árvore com água no chão |
| rede | Requalificações na rede | galeria: terreno e tubo com água (igual à drenagem) |

- Arquivos: `mapa/icones/obra_<categoria>.svg` e
  `obra_<categoria>_licitacao.svg`, com PNG 64/128 em `mapa/icones/png/`,
  gerados por `scripts/gerar_icones_obras_tipo.py`. Prévia:
  `mapa/icones/previa_obras_tipo.png`.
- No ArcGIS: símbolo por "Valores únicos" do campo de categoria (o CSV dos
  pontos vai levar a coluna). Usar no mínimo 32 px.
- CSV dos pontos (07/10/2026): `dados/processados/arcgis/obras_pontos.csv`,
  gerado por `scripts/gerar_pontos_obras.py` a partir da aba "Obras" (campos
  obra_id, nome, tipo, categoria, status, icone, lat, lon, coord_precisao).
  No ArcGIS Pro: Tabela XY para Ponto (X = lon, Y = lat, WGS 1984) →
  Simbologia → Valores únicos no campo `icone` → em cada valor, símbolo de
  imagem com o SVG de mesmo nome em `mapa/icones/`, 32 px. Obra sem tipo fica
  com `icone` vazio (cai em "todos os outros valores").
- Pendente: obras 26, 32 e 33 sem `tipo` na planilha; status quase todo
  vazio (só 1, 2 e 6), então quase todas aparecem cheias.

## Origem dos desenhos
- **Maki** (Mapbox), versão 8.2.0, licença CC0 (domínio público).
- **Temaki** (Rapid), versão 5.13.0, licença CC0 (domínio público).
- Ícones que não existem nessas bibliotecas são desenhados no mesmo estilo
  (ex.: canal, com três ondas).

## Em aberto
- Creche: o desenho da criança não ficou claro para Pedro (03/10); rever depois.
- Desenho da escola: o da Maki (lápis e maçã) não se lê em tamanho pequeno.
  Alternativas: capelo, prédio escolar, livro.
- Lista final de ícones (proposta abaixo) e quais equipamentos aparecem no
  mapa como camada.
- Forma dos grupos ainda sem definição: resposta e apoio, mobilidade.

## Lista proposta (a confirmar)
| Grupo | Ícones |
|---|---|
| Risco | Ponto crítico; trecho crítico (linha) |
| Drenagem | Canal; galeria; reservatório; estação de bombeamento; comporta |
| Equipamentos sensíveis (E2) | Escola; creche; unidade de saúde; hospital; ILPI |
| Resposta e apoio | Abrigo / ponto de apoio da Defesa Civil; base do COP |
| Mobilidade (I1) | Terminal integrado; estação de BRT; corredor de ônibus |
| Obras | Em obra; em licitação; concluído (proposta acima) |
