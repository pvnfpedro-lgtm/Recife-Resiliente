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

## Regras
- O arquivo original vai para `dados/brutos/<fonte>/` e não é editado.
  Registre a data de download e o link.
- Toda base precisa estar em **EPSG:31985** antes do cruzamento com os
  buffers.
- Dados pessoais (por exemplo, endereço de quem fez um chamado) **não** entram
  no repositório.
