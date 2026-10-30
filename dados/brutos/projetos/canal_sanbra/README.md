# Canal do Sanbra: pranchas do projeto

| Arquivo | O que é |
|---|---|
| `P01.CSb_Implan.Rem.2_assinado.pdf` | Prancha 01/28, implantação geral (Rem. 2), escala 1:1500. PDF assinado, gerado no ZWCAD em 21/10/2024. **Sem georreferenciamento** e sem grade de coordenadas. Recebido de Pedro em 29/10/2026 |
| `planta_p01.json` | Configuração de `scripts/planta_pdf_para_geojson.py`: recorte da planta na folha, escala, cor do desenho → camada, e cor/espessura de cada camada no mapa |
| `pontos_controle.csv` / `.png` | 5 pontos do canal para encaixar a planta no terreno. Coordenadas da folha (`x_pt`, `y_pt`); lat/lon dos pontos 4 e 5 coladas por Pedro do Google Maps em 29/10/2026 (pendência 24) |

O DWG `SANBRA_P17.CSb_Guarda-Corpo` (detalhe do guarda-corpo, AutoCAD 2007) não foi
usado: é detalhe construtivo, sem posição no terreno, e o formato não abre aqui sem o
LibreDWG.

Saídas em `dados/processados/projetos/`: `canal_sanbra_implantacao_metros_planta.geojson`
(prévia, metros da planta, sem posição) e, depois dos pontos de controle,
`canal_sanbra_implantacao.geojson` (WGS 84, com o erro de cada ponto). Prévias:
`docs/img/canal_sanbra_previa.png` e `docs/img/canal_sanbra_georreferenciado.png`.

Camadas tiradas pelas cores do desenho (nomes a conferir com a legenda): áreas verdes,
calçadas e pisos, piso intertravado vermelho, vias do projeto, faixas marrons (vias
existentes?), bacia de detenção (contorno aproximado), canal, Rio Jiquiá e limite da
intervenção. Mobiliário, árvores, textos e base cadastral ficaram de fora.
