/* Hintergrundmotiv „kreislauf“: Material fällt über vier Stufen nach unten.
   Auf jeder Stufe bleibt ein Teil zurück und verblasst; was weiterläuft, wird blasser und kleiner.
   Ein Kreis, in dem nichts verloren geht, ist nur als feine Linie im Hintergrund angedeutet. */
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H;
function resize() { W = canvas.width = canvas.clientWidth; H = canvas.height = canvas.clientHeight; }
resize();
window.addEventListener('resize', resize);

const STEPS = 4;
let parts = [], tick = 0;
function stepX(i) { return W * (0.12 + i * 0.22); }
function stepY(i) { return H * (0.18 + i * 0.2); }
function draw() {
  ctx.clearRect(0, 0, W, H);
  // angedeuteter Kreis
  ctx.beginPath(); ctx.arc(W * 0.5, H * 0.5, Math.min(W, H) * 0.42, 0, 7);
  ctx.setLineDash([2, 8]); ctx.strokeStyle = `rgba(${PLANET.ink},0.07)`; ctx.lineWidth = 0.7; ctx.stroke();
  ctx.setLineDash([]);
  for (let i = 0; i < STEPS; i++) {                 // Stufen
    ctx.beginPath(); ctx.moveTo(stepX(i) - W * 0.08, stepY(i)); ctx.lineTo(stepX(i) + W * 0.1, stepY(i));
    ctx.strokeStyle = `rgba(${PLANET.ink},0.12)`; ctx.lineWidth = 1; ctx.stroke();
  }
  tick++;
  if (tick % 3 === 0) parts.push({ x: stepX(0) - W * 0.08 * Math.random(), y: stepY(0), vx: 0.9, vy: 0, s: 0, q: 1, stuck: false });
  for (const p of parts) {
    if (p.stuck) { p.q -= 0.006; continue; }
    p.x += p.vx; p.vy += 0.05; p.y += p.vy;
    const s = p.s;
    if (s < STEPS && p.y >= stepY(s) && p.x <= stepX(s) + W * 0.1) { p.y = stepY(s); p.vy = 0; }
    else if (s < STEPS && p.y > stepY(s) + 2) {
      p.s++;                                         // fällt auf die nächste Stufe
      if (Math.random() < 0.3) { p.stuck = true; p.y = stepY(p.s - 1); }   // Verlust im Prozess
      p.q *= 0.8;
    }
  }
  parts = parts.filter(p => p.q > 0.02 && p.y < H + 10);
  for (const p of parts) {
    ctx.beginPath(); ctx.arc(p.x, p.y, 0.8 + 1.4 * p.q, 0, 7);
    ctx.fillStyle = p.stuck ? `rgba(${PLANET.ink},${0.18 * p.q})` : `rgba(176,96,58,${0.55 * p.q})`;
    ctx.fill();
  }
  PLANET.next(draw);
}
draw();
