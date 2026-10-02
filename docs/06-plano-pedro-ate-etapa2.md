# 6. Plano de Pedro até a Etapa 2 (14/10/2026)

Frentes de Pedro: dados, território, causas de infraestrutura e cronograma.
Objetivo da semana: chegar a 14/10 com critérios, pesos e 21 pontos conferidos,
e com os pedidos de dados de outros órgãos já feitos.

> ⚠️ **12/10 (segunda) é feriado nacional.** Na prática, depois da semana de
> 05 a 09/10 sobra só 13/10 para fechar a entrega.

## Semana de 05 a 09/10

| Dia | Tarefa | Entregável | Depende de |
|---|---|---|---|
| **Seg 05** | Enviar pedidos de dados a COP (histórico de ocorrências), Compesa (rede de esgoto e extravasamentos) e EMLURB (coordenadas exatas dos 21 trechos) | E-mails enviados, registrados em `03-fontes-de-dados.md` | — |
| Seg 05 | Transcrever os 24 subcritérios da aba *Critérios* para `dados/modelos/criterios.csv` | CSV com código, dimensão e subcritério (pesos vazios) | Planilha .xlsx |
| Seg 05 | Marcar a reunião do grupo para fechar os pesos (qui 08 ou sex 09) | Convite enviado | — |
| **Ter 06** | Conferir as coordenadas dos 21 pontos (lista da EMLURB + imagem de satélite) | `pontos.csv` com `coordenada_verificada` preenchida | Resposta da EMLURB, se chegar |
| Ter 06 | Baixar a malha de setores e os agregados do Censo 2022 (IBGE) e a malha do IVS por UDH (Ipea); confirmar o ano-base do IVS | Arquivos em `dados/brutos/`, com data e link | — |
| **Qua 07** | No ArcGIS Pro: reprojetar tudo para EPSG:31985, gerar os buffers de 300 m e fazer o primeiro cruzamento com Censo e IVS | Tabela preliminar de população e IVS por ponto | Coordenadas conferidas |
| Qua 07 | Achar a fonte de bacia e sub-bacia (ESIG / Plano de Drenagem) | Fonte identificada ou registrada como pendente | — |
| **Qui 08** | Preparar a proposta de pesos e rodar a sensibilidade (pesos iguais × proposta) com as notas que já existirem | Uma página de apoio para a reunião | Critérios no CSV |
| Qui 08 | Levar à equipe a proposta de quem faz as vistorias | Proposta escrita | — |
| **Sex 09** | Reunião do grupo: fechar os pesos e a escala da tratabilidade | Pesos em `criterios.csv` | Reunião marcada |
| Sex 09 | Cobrar os pedidos de dados sem resposta; atualizar o cronograma da equipe | `04-cronograma.md` e `05-pendencias.md` atualizados | — |

## Fechamento

| Dia | Tarefa |
|---|---|
| Seg 12 | Feriado |
| **Ter 13** | Consolidar a entrega da Etapa 2: recorte, critérios e pesos, 21 pontos conferidos, fontes e pendências; revisar com a tutora, se possível |
| **Qua 14** | **Entrega da Etapa 2** |

## Riscos
- **Pedidos a COP e Compesa:** costumam demorar. Por isso saem na segunda. Se
  não chegarem até 27/10, os subcritérios dependentes ficam com cobertura
  incompleta no ranking (o script mostra isso) e entram como pendência.
- **Pesos:** se não fecharem na sexta, a Etapa 2 vai com a proposta de pesos
  e a análise de sensibilidade, e isso fica explícito.
