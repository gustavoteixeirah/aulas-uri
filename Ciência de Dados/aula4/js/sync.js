/* =========================================================
   Aula 04 — sincronização de slides entre abas/janelas
   Mantém todas as abas do deck no mesmo slide: ao avançar em
   uma, as outras acompanham.

   Como funciona: cada aba publica o slide atual em localStorage
   e observa mudanças. O evento 'storage' não é confiável em
   páginas abertas via file://, então há também uma verificação
   periódica (polling) como rede de segurança.

   Tecla S liga/desliga a sincronização apenas nesta aba.
   ========================================================= */
(function () {
  'use strict';

  if (!window.Deck) return;

  var KEY  = 'cd-aula4-sync-slide';
  var POLL = 250;                                  // ms
  var TAB  = String(Math.random()).slice(2) + '-' + performance.now();

  /* localStorage indisponível (ex.: Safari em file://) → desiste em silêncio */
  try {
    localStorage.setItem(KEY + '-probe', '1');
    localStorage.removeItem(KEY + '-probe');
  } catch (e) { return; }

  var ativo    = sessionStorage.getItem(KEY + '-off') !== '1';
  var aplicando = false;   // evita eco: mudança recebida não é reenviada
  var ultimoTs = 0;        // último aviso já processado

  function ler() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null'); }
    catch (e) { return null; }
  }

  /* Estado inicial: registra o que já está lá, mas NÃO pula o slide.
     Assim a aba só se move quando alguém realmente navegar. */
  var inicial = ler();
  if (inicial && inicial.ts) ultimoTs = inicial.ts;

  /* --- publica --------------------------------------------------- */
  window.addEventListener('deck:change', function (e) {
    if (!ativo || aplicando) return;
    // ts estritamente crescente: dois avisos no mesmo milissegundo não se anulam
    var anterior = ler();
    var ts = Date.now();
    if (anterior && anterior.ts >= ts) ts = anterior.ts + 1;
    ultimoTs = ts;
    try {
      localStorage.setItem(KEY, JSON.stringify({ i: e.detail.index, ts: ts, tab: TAB }));
    } catch (err) {}
  });

  /* --- recebe ---------------------------------------------------- */
  function verificar() {
    if (!ativo) return;
    var d = ler();
    if (!d || d.tab === TAB || !d.ts || d.ts <= ultimoTs) return;
    ultimoTs = d.ts;
    if (d.i === window.Deck.current()) return;
    aplicando = true;
    window.Deck.go(d.i);
    aplicando = false;
  }

  window.addEventListener('storage', function (e) {
    if (!e.key || e.key === KEY) verificar();
  });
  setInterval(verificar, POLL);

  /* --- liga/desliga nesta aba (tecla S) -------------------------- */
  function aviso(texto) {
    var el = document.createElement('div');
    el.textContent = texto;
    el.style.cssText = 'position:fixed;left:50%;bottom:28px;transform:translateX(-50%);' +
      'z-index:9999;padding:10px 18px;border-radius:999px;font:600 14px/1 system-ui,sans-serif;' +
      'background:rgba(20,20,25,.92);color:#fff;box-shadow:0 6px 24px rgba(0,0,0,.28);' +
      'pointer-events:none;transition:opacity .25s';
    document.body.appendChild(el);
    setTimeout(function () { el.style.opacity = '0'; }, 1300);
    setTimeout(function () { el.remove(); }, 1600);
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 's' && e.key !== 'S') return;
    ativo = !ativo;
    try { sessionStorage.setItem(KEY + '-off', ativo ? '0' : '1'); } catch (err) {}
    if (ativo) {
      var d = ler();
      if (d && d.ts) ultimoTs = d.ts;   // reentra sem pular para trás
    }
    aviso(ativo ? 'Sincronização entre abas: ligada' : 'Sincronização entre abas: desligada');
  });
})();
