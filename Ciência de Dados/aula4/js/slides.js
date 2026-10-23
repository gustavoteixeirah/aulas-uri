/* =========================================================
   Aula 04 — motor dos slides
   Navegação, animações de entrada, índice, tema e realce de sintaxe.
   Sem dependências externas: basta abrir o index.html.
   ========================================================= */
(function () {
  'use strict';

  var STAGE_W = 800;
  var STAGE_H = 600;

  var stage   = document.getElementById('stage');
  var deck    = document.getElementById('deck');
  var slides  = Array.prototype.slice.call(deck.querySelectorAll('.slide'));
  var elCur   = document.getElementById('cur');
  var elTotal = document.getElementById('total');
  var elFill  = document.getElementById('progressFill');
  var elTitle = document.getElementById('barTitle');
  var elBlock = document.getElementById('barBlock');
  var btnPrev = document.getElementById('btnPrev');
  var btnNext = document.getElementById('btnNext');
  var btnMenu = document.getElementById('btnMenu');
  var btnMenuClose = document.getElementById('btnMenuClose');
  var btnTheme = document.getElementById('btnTheme');
  var btnFull  = document.getElementById('btnFull');
  var menu     = document.getElementById('menu');
  var menuList = document.getElementById('menuList');

  var index = 0;

  /* ---------------------------------------------------------
     1. Escala o palco para preencher a janela mantendo 4:3
     --------------------------------------------------------- */
  function fit() {
    var margin = window.innerWidth < 700 ? 8 : 24;
    var scale = Math.min(
      (window.innerWidth  - margin * 2) / STAGE_W,
      (window.innerHeight - margin * 2) / STAGE_H
    );
    stage.style.transform = 'scale(' + scale + ')';
  }
  window.addEventListener('resize', fit);

  /* ---------------------------------------------------------
     2. Realce de sintaxe — a função vive em js/highlight.js
     --------------------------------------------------------- */
  document.querySelectorAll('pre.code > code').forEach(function (code) {
    if (code.classList.contains('no-hl')) return;
    code.innerHTML = window.HL(code.innerHTML);
  });

  /* ---------------------------------------------------------
     3. Animação escalonada dos elementos de cada slide
     --------------------------------------------------------- */
  var CONTAINERS = ['cards', 'compare', 'timeline', 'pipeline', 'roadmap',
                    'levels', 'steps', 'recap', 'chips', 'checks', 'qlist',
                    'stackbox', 'idcard', 'split', 'alts'];

  function isContainer(el) {
    return CONTAINERS.some(function (c) { return el.classList.contains(c); });
  }

  slides.forEach(function (slide) {
    var targets = [];
    Array.prototype.forEach.call(slide.children, function (el) {
      if (isContainer(el) && el.children.length) {
        Array.prototype.forEach.call(el.children, function (kid) { targets.push(kid); });
      } else {
        targets.push(el);
      }
    });
    targets.forEach(function (el, i) {
      el.classList.add('anim');
      el.style.setProperty('--i', i);
    });
  });

  /* ---------------------------------------------------------
     4. Índice lateral
     --------------------------------------------------------- */
  slides.forEach(function (slide, i) {
    var a = document.createElement('a');
    var isSec = slide.classList.contains('divider');
    a.className = isSec ? 'sec' : '';
    a.innerHTML = '<i>' + (i + 1) + '</i><span>' + (slide.dataset.title || 'Slide') + '</span>';
    a.addEventListener('click', function () { go(i); closeMenu(); });
    menuList.appendChild(a);
  });
  var menuLinks = Array.prototype.slice.call(menuList.children);

  function openMenu()  { menu.classList.add('open');  menu.setAttribute('aria-hidden', 'false'); }
  function closeMenu() { menu.classList.remove('open'); menu.setAttribute('aria-hidden', 'true'); }
  function toggleMenu(){ menu.classList.contains('open') ? closeMenu() : openMenu(); }

  /* ---------------------------------------------------------
     5. Navegação
     --------------------------------------------------------- */
  function go(n) {
    n = Math.max(0, Math.min(slides.length - 1, n));
    if (n === index && slides[n].classList.contains('is-active')) return;

    slides.forEach(function (s, i) {
      s.classList.toggle('is-active', i === n);
      s.classList.toggle('is-past', i < n);
      // reinicia as animações do slide que entra
      if (i === n) {
        s.querySelectorAll('.anim').forEach(function (el) {
          el.style.animation = 'none';
          void el.offsetWidth;
          el.style.animation = '';
        });
      }
    });

    index = n;
    update();
    if (location.hash !== '#' + (n + 1)) {
      history.replaceState(null, '', '#' + (n + 1));
    }
    // avisa quem estiver ouvindo (ex.: js/sync.js) que o slide mudou
    window.dispatchEvent(new CustomEvent('deck:change', { detail: { index: n } }));
  }

  function update() {
    var s = slides[index];
    elCur.textContent = index + 1;
    elTitle.textContent = s.dataset.title || '';
    elBlock.textContent = s.dataset.block || '';
    elFill.style.width = ((index) / (slides.length - 1) * 100) + '%';
    btnPrev.disabled = index === 0;
    btnNext.disabled = index === slides.length - 1;
    menuLinks.forEach(function (a, i) { a.classList.toggle('on', i === index); });
    var on = menuLinks[index];
    if (on && menu.classList.contains('open')) {
      on.scrollIntoView({ block: 'nearest' });
    }
  }

  function next() { go(index + 1); }
  function prev() { go(index - 1); }

  btnNext.addEventListener('click', next);
  btnPrev.addEventListener('click', prev);
  btnMenu.addEventListener('click', toggleMenu);
  btnMenuClose.addEventListener('click', closeMenu);

  /* ---------------------------------------------------------
     6. Tema e tela cheia
     --------------------------------------------------------- */
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem('cd-aula4-tema', t); } catch (e) {}
  }
  try {
    var saved = localStorage.getItem('cd-aula4-tema');
    if (saved) setTheme(saved);
    else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) setTheme('dark');
  } catch (e) {}

  btnTheme.addEventListener('click', function () {
    setTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  btnFull.addEventListener('click', function () {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen();
  });

  /* ---------------------------------------------------------
     6b. Exportar para PDF (impressão do navegador)
     --------------------------------------------------------- */
  var pdfModal = document.getElementById('pdfModal');
  var btnPdf   = document.getElementById('btnPdf');

  function abrirPdf()  { pdfModal.classList.add('open');   pdfModal.setAttribute('aria-hidden', 'false'); }
  function fecharPdf() { pdfModal.classList.remove('open'); pdfModal.setAttribute('aria-hidden', 'true'); }

  btnPdf.addEventListener('click', abrirPdf);
  document.getElementById('pdfCancel').addEventListener('click', fecharPdf);
  document.getElementById('pdfGo').addEventListener('click', function () {
    fecharPdf();
    closeMenu();
    // espera o modal sumir antes de abrir a janela de impressão
    setTimeout(function () { window.print(); }, 120);
  });
  pdfModal.addEventListener('click', function (e) { if (e.target === pdfModal) fecharPdf(); });

  /* ---------------------------------------------------------
     7. Teclado, toque e roda
     --------------------------------------------------------- */
  document.addEventListener('keydown', function (e) {
    switch (e.key) {
      case 'ArrowRight': case 'PageDown': case ' ': case 'Enter':
        e.preventDefault(); next(); break;
      case 'ArrowLeft': case 'PageUp': case 'Backspace':
        e.preventDefault(); prev(); break;
      case 'Home': e.preventDefault(); go(0); break;
      case 'End':  e.preventDefault(); go(slides.length - 1); break;
      case 'Escape': closeMenu(); fecharPdf(); break;
      case 'm': case 'M': toggleMenu(); break;
      case 't': case 'T': btnTheme.click(); break;
      case 'f': case 'F': btnFull.click(); break;
      case 'p': case 'P': e.preventDefault(); abrirPdf(); break;
    }
  });

  var tx = 0, ty = 0;
  stage.addEventListener('touchstart', function (e) {
    tx = e.changedTouches[0].clientX; ty = e.changedTouches[0].clientY;
  }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    var dx = e.changedTouches[0].clientX - tx;
    var dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy)) (dx < 0 ? next : prev)();
  }, { passive: true });

  /* ---------------------------------------------------------
     8. Início
     --------------------------------------------------------- */
  elTotal.textContent = slides.length;
  fit();
  var fromHash = parseInt((location.hash || '').replace('#', ''), 10);
  go(isNaN(fromHash) ? 0 : fromHash - 1);

  window.addEventListener('hashchange', function () {
    var n = parseInt((location.hash || '').replace('#', ''), 10);
    if (!isNaN(n) && n - 1 !== index) go(n - 1);
  });

  /* API pública mínima — usada por js/sync.js */
  window.Deck = {
    go: go,
    current: function () { return index; },
    total: slides.length
  };
})();
