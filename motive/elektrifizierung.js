/* Hintergrundmotiv „elektrifizierung“: Viele Lichtpunkte strömen von links nach rechts
   über parallele Leitungen. In der Mitte laufen die Leitungen zu einem schmalen Abschnitt
   zusammen, dem Transformator. Dort stauen sich die Punkte, dahinter fließen sie spärlich weiter. */
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H;
function resize() { W = canvas.width = canvas.clientWidth; H = canvas.height = canvas.clientHeight; }
resize();
window.addEventListener('resize', resize);

const LANES = 9, GATE = 0.56, CAP = 2;   // Durchlass pro Schritt
let parts = [], tick = 0, queue = 0;
function laneY(l, x) {                   // Leitungen bündeln sich zur Mitte hin
  const spread = (l - (LANES - 1) / 2) / ((LANES - 1) / 2);
  const pinch = Math.exp(-Math.pow((x / W - GATE) / 0.09, 2));
  return H * 0.5 + spread * H * 0.36 * (1 - 0.9 * pinch);
}
function draw() {
  ctx.clearRect(0, 0, W, H);
  for (let l = 0; l < LANES; l++) {
    ctx.beginPath();
    for (let x = 0; x <= W; x += 8) { const y = laneY(l, x); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.strokeStyle = `rgba(${PLANET.ink},0.07)`; ctx.lineWidth = 0.7; ctx.stroke();
  }
  tick++;
  if (tick % 2 === 0) parts.push({ l: Math.floor(Math.random() * LANES), x: 0, v: 1.6 + Math.random() * 0.8 });
  const gx = W * GATE; let passed = 0;
  parts.sort((a, b) => b.x - a.x);
  for (const p of parts) {
    if (p.x < gx - 4 && p.x + p.v >= gx - 4) {
      if (passed < CAP && tick % 3 === 0) { passed++; p.x += p.v; } else { p.wait = (p.wait || 0) + 1; }
    } else p.x += p.v * (p.x > gx ? 1.3 : 1);
  }
  // Staubereich: wartende Punkte rücken nach hinten auf
  const waiting = parts.filter(p => p.x < gx - 4 && p.x + p.v >= gx - 4);
  waiting.forEach((p, i) => { p.x = Math.max(gx - 6 - i * 0.9, p.x - 0.6); });
  parts = parts.filter(p => p.x < W + 4).slice(-600);
  for (const p of parts) {
    const after = p.x > gx;
    ctx.beginPath(); ctx.arc(p.x, laneY(p.l, p.x), after ? 1.6 : 1.3, 0, 7);
    ctx.fillStyle = after ? 'rgba(176,96,58,0.55)' : `rgba(${PLANET.ink},0.22)`; ctx.fill();
  }
  PLANET.next(draw);
}
draw();
