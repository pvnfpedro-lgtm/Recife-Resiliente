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
- Forma dos grupos ainda sem definição: resposta e apoio, mobilidade, obras.

## Lista proposta (a confirmar)
| Grupo | Ícones |
|---|---|
| Risco | Ponto crítico; trecho crítico (linha) |
| Drenagem | Canal; galeria; reservatório; estação de bombeamento; comporta |
| Equipamentos sensíveis (E2) | Escola; creche; unidade de saúde; hospital; ILPI |
| Resposta e apoio | Abrigo / ponto de apoio da Defesa Civil; base do COP |
| Mobilidade (I1) | Terminal integrado; estação de BRT; corredor de ônibus |
| Obras | Em execução; prevista; concluída |
