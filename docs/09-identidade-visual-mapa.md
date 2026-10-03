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

## Origem dos desenhos
- **Maki** (Mapbox), versão 8.2.0, licença CC0 (domínio público).
- **Temaki** (Rapid), versão 5.13.0, licença CC0 (domínio público).
- Ícones que não existem nessas bibliotecas são desenhados no mesmo estilo
  (ex.: canal, com três ondas).

## Em aberto
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
