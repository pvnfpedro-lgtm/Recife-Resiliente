# Shapefiles

Pasta para ir juntando os shapefiles do projeto. Uma subpasta por camada.

## Como subir
1. No GitHub, abra esta pasta no branch de trabalho e use
   **Add file → Upload files**.
2. No nome do arquivo, escreva antes o nome da subpasta, por exemplo
   `canais/` (o GitHub cria a pasta). Ou zipe a camada e mande na conversa
   com o Claude.
3. Suba **todos** os arquivos da camada juntos: `.shp`, `.shx`, `.dbf`,
   `.prj` e, se tiver, `.cpg`. Sem o `.prj` não dá para saber o sistema de
   referência.

## Regras
- Nome da subpasta e dos arquivos: minúsculas, sem acento e sem espaço
  (ex.: `canais/canais.shp`).
- Pelo site, o GitHub aceita até 25 MB por arquivo, e no máximo 100 MB por
  outros meios. Camada maior (malha da cidade inteira): não suba; anote o
  link abaixo e recortamos para a RPA 6.
- Sistema de referência do projeto: SIRGAS 2000 / UTM 25S (EPSG:31985).
  Camada em outro sistema pode subir como veio; a conversão fica registrada.

## Catálogo
Preencha uma linha por camada ao subir (fonte e data são obrigatórias).

| Subpasta | O que é | Fonte (órgão / link) | Data | Variável | Observação |
|---|---|---|---|---|---|
| `CIS/` | Limites das Comunidades de Interesse Social (545 polígonos; shapefile `shp_CIS` + `.pitemx` do serviço) | ESIG Recife, `ATLAS/Ser_Camada_CIS/MapServer/1` | exportado em 04/10/2026 (data dos dados: não conferida) | V6 ou plano B do V1 (a decidir) | SIRGAS 2000 / UTM 25S. Nomes dos campos cortados na exportação (`INDICADORE`, `INDICADO_1`…): significado pendente |
| `pontos_criticos/` | Os 21 pontos críticos da RPA 6 (shapefile `pontos_criticos_rpa6`; `pontos_criticos_kit.zip` traz também o ícone da gota) | Gerado de `dados/processados/pontos_rpa6.csv` (planilha da EMLURB de 02/10/2026) | 05/10/2026 | Todas (local dos pontos) | SIRGAS 2000 / UTM 25S. 11 coordenadas aproximadas; nenhuma verificada (pendência 4) |
