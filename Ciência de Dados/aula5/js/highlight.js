/* =========================================================
   Realce de sintaxe (Python)
   Expõe window.HL(texto) — recebe HTML já escapado e devolve
   o mesmo texto com <span class="tok-*"> em volta dos tokens.
   Usado por js/slides.js e por js/trace.js.

   Diferença para o realce das aulas de C: aqui o `#` é
   comentário (e não diretiva de pré-processador), e a lista de
   palavras-chave é a do Python — mais os nomes que aparecem o
   tempo todo nesta aula (np, array, dtype, shape…).
   ========================================================= */
(function () {
  'use strict';

  var KEYWORDS = [
    'import','from','as','def','return','lambda','if','elif','else','for','while','in','not',
    'and','or','is','None','True','False','class','with','try','except','finally','raise',
    'yield','pass','break','continue','global','del','assert','print','range','len','sum',
    'list','int','float','str','bool','abs','min','max','sorted','enumerate','zip','append'
  ];

  var RE = new RegExp(
    '(#[^\\n]*)' +                                   /* comentário */
    '|("""[\\s\\S]*?""")' +                          /* docstring */
    '|("(?:[^"\\\\\\n]|\\\\.)*")' +                  /* string com aspas duplas */
    "|('(?:[^'\\\\\\n]|\\\\.)*')" +                  /* string com aspas simples */
    '|\\b(' + KEYWORDS.join('|') + ')\\b' +
    '|\\b(\\d+\\.?\\d*(?:e[-+]?\\d+)?)\\b' +
    '|\\b([A-Za-z_]\\w*)(?=\\s*\\()',                /* chamada de função */
    'gm'
  );

  window.HL = function (raw) {
    return raw.replace(RE, function (m, com, doc, str1, str2, kw, num, fn) {
      if (com)          return '<span class="tok-com">' + m + '</span>';
      if (doc || str1 || str2) return '<span class="tok-str">' + m + '</span>';
      if (kw)           return '<span class="tok-key">' + m + '</span>';
      if (num)          return '<span class="tok-num">' + m + '</span>';
      if (fn)           return '<span class="tok-fn">'  + m + '</span>';
      return m;
    });
  };

  window.escapeHTML = function (s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  };
})();
