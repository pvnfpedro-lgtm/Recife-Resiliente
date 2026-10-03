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

/* Códigos dos subcritérios, na ordem das colunas da aba. */
var SUBCRITERIOS = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'E1', 'E2', 'E3',
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
    var pontos = [];
    for (var r = LINHA_CABECALHO; r < valores.length; r++) {
      var linha = valores[r];
      if (typeof linha[c.id] !== 'number') break;  // fim da tabela
      var subs = {};
      SUBCRITERIOS.forEach(function (cod) { var k = col(cod + ' '); subs[cod] = k < 0 ? null : num(linha[k]); });
      pontos.push({
        id: linha[c.id], bairro: String(linha[c.bairro]), trecho: String(linha[c.trecho]),
        tipo: String(linha[c.tipo]), grupo: String(linha[c.grupo] || ''),
        lat: num(linha[c.lat]), lon: num(linha[c.lon]), precisao: String(linha[c.precisao]),
        P: num(linha[c.notaP]), E: num(linha[c.notaE]), V: num(linha[c.notaV]), I: num(linha[c.notaI]),
        C: num(linha[c.cons]), risco: num(linha[c.risco]), indice: num(linha[c.indice]),
        posicao: num(linha[c.posicao]), preenchidas: num(linha[c.preenchidas]), notas: subs
      });
    }
    return { pontos: pontos, lidoEm: new Date().toISOString() };
  } catch (e) {
    return { erro: String(e && e.message ? e.message : e) };
  }
}

/* =====================================================================
   AJUSTE ÚNICO DA PLANILHA — subcritérios de 03/10/2026
   Renomeia cabeçalhos, insere V5 e V6 (antes do V1) e I3 (antes do I2),
   sem nota e sem peso, e refaz a fórmula de "Notas preenchidas".
   Pode ser executada mais de uma vez: o que já foi feito é pulado.
   Executar pelo editor do Apps Script (Executar → atualizarSubcriterios0310).
   ===================================================================== */
function atualizarSubcriterios0310() {
  var aba = SpreadsheetApp.openById(PLANILHA_NOTAS_ID).getSheetByName(ABA_NOTAS);
  var L = LINHA_CABECALHO;
  var log = [];
  function cab() {
    return aba.getRange(L, 1, 1, aba.getLastColumn()).getValues()[0].map(function (h) {
      return String(h).replace(/\s+/g, ' ').trim();
    });
  }
  function col(inicio) {  // número da coluna (1 = A) cujo cabeçalho começa com o texto
    var c = cab();
    for (var i = 0; i < c.length; i++) if (c[i].indexOf(inicio) === 0) return i + 1;
    return -1;
  }
  var ultimaLinha = L;
  var ids = aba.getRange(L + 1, 1, aba.getLastRow() - L, 1).getValues();
  for (var k = 0; k < ids.length && typeof ids[k][0] === 'number'; k++) ultimaLinha = L + 1 + k;
  var nLinhas = ultimaLinha - L;

  var nomes = { P1: 'Frequência e recorrência histórica', P6: 'Relevo (baixio)',
                E2: 'Equipamentos públicos', E3: 'Comércio e serviços',
                V2: 'População vulnerável', V3: 'ZEIS, favelas e comunidades',
                I1: 'Interrupção do trânsito' };
  Object.keys(nomes).forEach(function (cod) {
    var c = col(cod + ' ');
    if (c < 0) { log.push('Não achei ' + cod); return; }
    aba.getRange(L, c).setValue(cod + '\n' + nomes[cod]);
  });
  log.push('Cabeçalhos renomeados');

  function inserir(antesDe, novos) {
    if (col(novos[0][0] + ' ') > 0) { log.push(novos[0][0] + ' já existe'); return; }
    var c = col(antesDe + ' ');
    if (c < 0) throw new Error('Coluna ' + antesDe + ' não encontrada');
    aba.insertColumnsBefore(c, novos.length);
    var modelo = c + novos.length;  // a coluna que foi empurrada
    novos.forEach(function (n, i) {
      aba.getRange(L - 1, modelo, nLinhas + 2, 1).copyFormatToRange(aba, c + i, c + i, L - 1, ultimaLinha);
      aba.getRange(L - 1, c + i, nLinhas + 2, 1).clearContent();  // sem peso e sem nota
      aba.getRange(L, c + i).setValue(n[0] + '\n' + n[1]);
    });
    log.push('Inseridas: ' + novos.map(function (n) { return n[0]; }).join(', '));
  }
  inserir('V1', [['V5', 'Dificuldade de evacuação'], ['V6', 'Infraestrutura precária']]);
  inserir('I2', [['I3', 'Isolamento']]);

  var cNotas = col('Notas preenchidas');
  var cods = SUBCRITERIOS.map(function (cod) { return col(cod + ' '); }).filter(function (c) { return c > 0; });
  var formulas = [];
  for (var r = L + 1; r <= ultimaLinha; r++) {
    // Soma de COUNT de uma célula cada: sem separador de argumentos, funciona em qualquer idioma.
    formulas.push(['=' + cods.map(function (c) {
      return 'COUNT(' + aba.getRange(r, c).getA1Notation() + ')';
    }).join('+')]);
  }
  aba.getRange(L + 1, cNotas, formulas.length, 1).setFormulas(formulas);
  log.push('Notas preenchidas: ' + cods.length + ' colunas');

  var a2 = aba.getRange('A2');
  a2.setValue(String(a2.getValue()).replace('P6 e V1 são condicionais:',
    'P6 e V1 são condicionais e I3, V5 e V6 ainda não têm definição:'));
  Logger.log(log.join('\n'));
  return log;
}
