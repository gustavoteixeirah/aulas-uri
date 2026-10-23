/* =========================================================
   Aula 03 — gerador dos slides de questão
   Lê window.QUESTOES e insere, em cada âncora <div data-quiz="...">,
   dois slides por questão: o enunciado e a resposta comentada.
   Precisa rodar ANTES de js/slides.js.
   ========================================================= */
(function () {
  'use strict';

  var LETRAS = ['A', 'B', 'C', 'D', 'E', 'F'];
  var questoes = window.QUESTOES || [];

  function alternativas(q, revelar) {
    return q.alts.map(function (texto, i) {
      var certa = i === q.correta;
      var cls = revelar ? (certa ? ' class="is-right"' : ' class="is-off"') : '';
      var marca = revelar && certa ? '<span class="alt-ok">✓</span>' : '';
      return '<li' + cls + '><span class="alt-l">' + LETRAS[i] + '</span><span class="alt-t">' +
             texto + '</span>' + marca + '</li>';
    }).join('');
  }

  function slide(q, num, total, revelar) {
    var s = document.createElement('section');
    s.className = 'slide quiz' + (revelar ? ' quiz-resp' : '');
    s.dataset.title = 'Q' + num + (revelar ? ' · Resposta' : ' · ' + q.tema);
    s.dataset.block = 'Questão ' + num + ' de ' + total;

    var kicker = revelar
      ? '<span class="kicker kicker-ok">Resposta · ' + q.tema + '</span>'
      : '<span class="kicker">Questão ' + num + ' de ' + total + ' · ' + q.tema + '</span>';

    var why = revelar
      ? '<div class="callout ok q-why"><b>Letra ' + LETRAS[q.correta] + '.</b> ' + q.porque + '</div>'
      : '';

    var codigo = q.codigo
      ? '<pre class="code q-code"><code data-lang="python">' + q.codigo + '</code></pre>'
      : '';

    s.innerHTML =
      kicker +
      '<h2 class="q-txt">' + q.texto + '</h2>' +
      codigo +
      '<ul class="alts' + (q.codigo ? ' alts-curtas' : '') + '">' + alternativas(q, revelar) + '</ul>' +
      why;

    return s;
  }

  var total = questoes.length;
  var num = 0;

  document.querySelectorAll('[data-quiz]').forEach(function (ancora) {
    var grupo = ancora.getAttribute('data-quiz');
    var frag = document.createDocumentFragment();

    questoes.forEach(function (q) {
      if (q.grupo !== grupo) return;
      q._num = ++num;
      frag.appendChild(slide(q, q._num, total, false));
      frag.appendChild(slide(q, q._num, total, true));
    });

    ancora.parentNode.replaceChild(frag, ancora);
  });
})();
