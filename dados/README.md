# Dados

- `modelos/`: cabeçalhos dos CSVs que o script lê. Copie para `processados/`
  e preencha.
- `brutos/<fonte>/`: arquivos originais, sem edição, com data e link de origem.
- `processados/`: saídas do SIG (notas por ponto) e do script (ranking).
- `historico/`: arquivos antigos, guardados só para consulta; não atualizar.
- `shapefiles/`: shapefiles do projeto, uma subpasta por camada, com
  catálogo no `README.md` da pasta.

Arquivos grandes de SIG (`.gdb`, `.aprx`, shapefiles de malha completa) ficam
fora do Git (ver `.gitignore`). Versione só os recortes e as tabelas.

Sistema de referência: SIRGAS 2000 / UTM 25S (EPSG:31985).
