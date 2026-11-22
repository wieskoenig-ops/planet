/* Hintergrundmotiv „wasser“: Schichten eines Grundwasserleiters, darin ein Wasserspiegel.
   Jedes Jahr (ein Durchlauf) wird ein wenig mehr entnommen, als nachfließt: Der Spiegel
   schwingt mit den Jahreszeiten, sinkt aber im Mittel. Die alten Höchststände bleiben als Spur. */
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H;
function resize() { W = canvas.width = canvas.clientWidth; H = canvas.height = canvas.clientHeight; }
resize();
window.addEventListener('resize', resize);

let t = 0, level = 0.28;
const marks = [];
function draw() {
  ctx.clearRect(0, 0, W, H);
  // Gesteinsschichten
  for (let k = 1; k < 7; k++) {
    ctx.beginPath();
    for (let x = 0; x <= W; x += 10) {
      const y = H * (k / 7) + Math.sin(x / W * 5 + k * 1.7) * H * 0.025;
      x ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.strokeStyle = `rgba(${PLANET.ink},0.06)`; ctx.lineWidth = 0.7; ctx.stroke();
  }
  t++;
  const season = Math.sin(t / 60) * 0.05;
  level += 0.00022;                                   // Entnahme > Neubildung
  if (level > 0.86) { level = 0.28; marks.length = 0; }
  if (t % 377 === 0) marks.push(level + season);
  for (const m of marks) {                            // frühere Stände
    ctx.setLineDash([2, 6]);
    ctx.beginPath(); ctx.moveTo(0, H * m); ctx.lineTo(W, H * m);
    ctx.strokeStyle = `rgba(${PLANET.ink},0.09)`; ctx.stroke();
  }
  ctx.setLineDash([]);
  const y0 = H * (level + season);
  ctx.beginPath();
  for (let x = 0; x <= W; x += 6) {
    const y = y0 + Math.sin(x / 37 + t / 18) * 1.6 + Math.sin(x / 91 - t / 31) * 2.2;
    x ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
  }
  ctx.strokeStyle = 'rgba(176,96,58,0.5)'; ctx.lineWidth = 1.2; ctx.stroke();
  ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.closePath();
  ctx.fillStyle = 'rgba(176,96,58,0.05)'; ctx.fill();
  PLANET.next(draw);
}
draw();
