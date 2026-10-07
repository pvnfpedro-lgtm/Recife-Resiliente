function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Recife Resiliente — Painel')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/* =====================================================================
   PONTOS CRÍTICOS — leitura da planilha de notas (TESTE)
   A planilha precisa ser nativa do Google Sheets (não .xlsx no Drive).
   O web app roda com a conta de quem implantou (executeAs USER_DEPLOYING),
   então quem só visualiza o painel não precisa de acesso à planilha.
   ===================================================================== */
var PLANILHA_NOTAS_ID = '1DN3abWIPk0dvOkh-28D2NGYBLgMI437Vx7Sk7TqpDc0';
var ABA_NOTAS = 'Notas dos pontos';
var LINHA_CABECALHO = 6;

/* Códigos das variáveis, na ordem das colunas da aba. */
var VARIAVEIS = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'E1', 'E2', 'E3',
                    'V2', 'V3', 'V4', 'V5', 'V6', 'V1', 'I1', 'I2', 'I3'];

function getPontosCriticos() {
  try {
    var aba = SpreadsheetApp.openById(PLANILHA_NOTAS_ID).getSheetByName(ABA_NOTAS);
    if (!aba) return { erro: 'Aba "' + ABA_NOTAS + '" não encontrada na planilha.' };

    var valores = aba.getDataRange().getValues();
    var cab = valores[LINHA_CABECALHO - 1].map(function (h) {
      return String(h).replace(/\s+/g, ' ').trim();
    });
    // Coluna cujo cabeçalho começa com o texto dado (os cabeçalhos têm 2 linhas).
    function col(inicio) {
      for (var i = 0; i < cab.length; i++) if (cab[i].indexOf(inicio) === 0) return i;
      return -1;
    }
    var c = {
      id: col('ID'), bairro: col('Bairro'), trecho: col('Trecho'), tipo: col('Tipo'),
      grupo: col('Grupo de'), lat: col('Latitude'), lon: col('Longitude'), precisao: col('Precisão'),
      notaP: col('Nota Probabilidade'), notaE: col('Nota Exposição'),
      notaV: col('Nota Vulnerabilidade'), notaI: col('Nota Impacto'),
      cons: col('Consequência'), risco: col('Risco'), indice: col('Índice de risco'),
      posicao: col('Posição'), preenchidas: col('Notas preenchidas')
    };
    var faltando = Object.keys(c).filter(function (k) { return c[k] < 0; });
    if (faltando.length) return { erro: 'Colunas não encontradas: ' + faltando.join(', ') };

    function num(v) { return (typeof v === 'number' && !isNaN(v)) ? v : null; }
    // Nome de cada variável = texto do cabeçalho depois do código ("P1 Frequência..." → "Frequência...").
    var nomes = {};
    VARIAVEIS.forEach(function (cod) {
      var k = col(cod + ' ');
      if (k >= 0) nomes[cod] = cab[k].slice(cod.length).trim();
    });
    var pontos = [];
    for (var r = LINHA_CABECALHO; r < valores.length; r++) {
      var linha = valores[r];
      if (typeof linha[c.id] !== 'number') break;  // fim da tabela
      var subs = {};
      VARIAVEIS.forEach(function (cod) { var k = col(cod + ' '); subs[cod] = k < 0 ? null : num(linha[k]); });
      pontos.push({
        id: linha[c.id], bairro: String(linha[c.bairro]), trecho: String(linha[c.trecho]),
        tipo: String(linha[c.tipo]), grupo: String(linha[c.grupo] || ''),
        lat: num(linha[c.lat]), lon: num(linha[c.lon]), precisao: String(linha[c.precisao]),
        P: num(linha[c.notaP]), E: num(linha[c.notaE]), V: num(linha[c.notaV]), I: num(linha[c.notaI]),
        C: num(linha[c.cons]), risco: num(linha[c.risco]), indice: num(linha[c.indice]),
        posicao: num(linha[c.posicao]), preenchidas: num(linha[c.preenchidas]), notas: subs
      });
    }
    return { pontos: pontos, nomes: nomes, lidoEm: new Date().toISOString() };
  } catch (e) {
    return { erro: String(e && e.message ? e.message : e) };
  }
}

/* =====================================================================
   OBRAS — abas "Obras" e "Cronograma das obras" da mesma planilha (05/10/2026)
   Cabeçalho na linha 1. O nome da coluna vale até o primeiro espaço
   ("investimento_total (R$)" -> "investimento_total"). Linha sem obra_id fica de fora.
   Datas voltam como texto aaaa-mm-dd (o google.script.run não envia objetos Date).
   ===================================================================== */
var ABA_OBRAS = 'Obras';
var ABA_CRONOGRAMA = 'Cronograma das obras';

function lerAbaComoObjetos_(planilha, nomeAba) {
  var aba = planilha.getSheetByName(nomeAba);
  if (!aba) return null;
  var valores = aba.getDataRange().getValues();
  if (valores.length < 2) return [];
  var cab = valores[0].map(function (h) { return String(h).trim().split(/\s+/)[0].toLowerCase(); });
  var fuso = planilha.getSpreadsheetTimeZone();  // mesmo fuso da planilha, para a data não mudar de dia
  var linhas = [];
  for (var r = 1; r < valores.length; r++) {
    var obj = {}, temAlgo = false;
    for (var c = 0; c < cab.length; c++) {
      if (!cab[c]) continue;
      var v = valores[r][c];
      if (v instanceof Date) v = Utilities.formatDate(v, fuso, 'yyyy-MM-dd');
      if (v === '') v = null;
      if (v !== null) temAlgo = true;
      obj[cab[c]] = v;
    }
    if (temAlgo && obj.obra_id !== null && obj.obra_id !== undefined) linhas.push(obj);
  }
  return linhas;
}

function getObras() {
  try {
    var planilha = SpreadsheetApp.openById(PLANILHA_NOTAS_ID);
    var obras = lerAbaComoObjetos_(planilha, ABA_OBRAS);
    if (obras === null) return { erro: 'Aba "' + ABA_OBRAS + '" não encontrada na planilha.' };
    var etapas = lerAbaComoObjetos_(planilha, ABA_CRONOGRAMA) || [];
    var porObra = {};
    etapas.forEach(function (e) {
      if (!e.macroetapa) return;  // linha guia ainda sem nome de tarefa
      var k = String(e.obra_id);
      (porObra[k] = porObra[k] || []).push(e);
    });
    Object.keys(porObra).forEach(function (k) {
      porObra[k].sort(function (a, b) { return (Number(a.ordem) || 0) - (Number(b.ordem) || 0); });
    });
    obras.forEach(function (o) { o.etapas = porObra[String(o.obra_id)] || []; });
    return { obras: obras, lidoEm: new Date().toISOString() };
  } catch (e) {
    return { erro: String(e && e.message ? e.message : e) };
  }
}
