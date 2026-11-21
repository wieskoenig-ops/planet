/* Laufzeit für die Hintergrundmotive: langsam, gedrosselt, pausiert wenn unsichtbar,
   bei prefers-reduced-motion nur ein ruhendes Standbild. Keine Bibliotheken. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)');
  var dark = matchMedia('(prefers-color-scheme: dark)');
  var FPS = 24;
  var P = window.PLANET = { ink: '' };
  function setInk() { P.ink = dark.matches ? '232,224,208' : '58,50,40'; }
  setInk();
  if (dark.addEventListener) dark.addEventListener('change', setInk);

  var pending = null, last = 0, raf = 0, onscreen = true, still = 0;

  function loop(t) {
    raf = 0;
    if (!pending) return;
    if (document.hidden || !onscreen) return;            // pausiert; wird bei Sichtbarkeit fortgesetzt
    if (t - last < 1000 / FPS) { raf = requestAnimationFrame(loop); return; }
    last = t;
    var fn = pending; pending = null;
    fn();
  }
  function wake() { if (pending && !raf && !document.hidden && onscreen) raf = requestAnimationFrame(loop); }

  P.next = function (fn) {
    if (reduce.matches) {                                 // Standbild: einige Schritte vorrechnen, dann stehen lassen
      if (still++ < 160) fn();
      return;
    }
    pending = fn;
    wake();
  };

  document.addEventListener('visibilitychange', wake);
  var c = document.getElementById('bg-canvas');
  if (c && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (e) { onscreen = e[0].isIntersecting; wake(); }).observe(c);
  }
})();
