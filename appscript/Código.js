function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Recife Resiliente — Painel')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/* Usado pelo Index.html para injetar HidroData.html no lugar certo
   (scriptlet <?!= include('HidroData'); ?>). */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}
