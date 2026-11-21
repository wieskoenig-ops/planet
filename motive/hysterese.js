/* Hintergrundmotiv „hysterese“, übernommen von emergenz.art/punkt/hysterese/ */
// Hintergrund: ein Punkt folgt der Gleichung dx/dt = p + x − x³,
// während p langsam hin und her läuft. Er bleibt auf seinem Zweig,
// bis die Falte erreicht ist, und springt dann – auf dem Rückweg an anderer Stelle.
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H;

function resize() {
  W = canvas.width  = canvas.clientWidth;
  H = canvas.height = canvas.clientHeight;
}
resize();
window.addEventListener('resize', resize);

const P_MAX = 0.75;
const X_MAX = 1.45;
let p = -P_MAX, dir = 1, x = -1.2;
const trail = [];
const TRAIL_LEN = 260;

function sx(pp) { return W * 0.5 + pp / P_MAX * W * 0.36; }
function sy(xx) { return H * 0.5 - xx / X_MAX * H * 0.34; }

function drawCurve() {
  // Gleichgewichte p = x³ − x; stabil, wo 3x² − 1 > 0
  const xs = 1 / Math.sqrt(3);
  const seg = (a, b, dashed, alpha) => {
    ctx.beginPath();
    for (let i = 0; i <= 120; i++) {
      const xx = a + (b - a) * i / 120;
      const pp = xx * xx * xx - xx;
      if (i === 0) ctx.moveTo(sx(pp), sy(xx)); else ctx.lineTo(sx(pp), sy(xx));
    }
    ctx.setLineDash(dashed ? [3, 6] : []);
    ctx.strokeStyle = `rgba(${PLANET.ink},${alpha})`;
    ctx.lineWidth = 0.6;
    ctx.stroke();
  };
  seg(-1.25, -xs, false, 0.09);
  seg(-xs, xs, true, 0.05);
  seg(xs, 1.25, false, 0.09);
  ctx.setLineDash([]);
}

function step() {
  p += dir * 0.0011;
  if (p > P_MAX)  { p = P_MAX;  dir = -1; }
  if (p < -P_MAX) { p = -P_MAX; dir = 1; }
  for (let k = 0; k < 6; k++) x += 0.03 * (p + x - x * x * x);
  trail.push({ x: sx(p), y: sy(x) });
  if (trail.length > TRAIL_LEN) trail.shift();
}

function draw() {
  ctx.clearRect(0, 0, W, H);
  drawCurve();
  step();
  for (let i = 1; i < trail.length; i++) {
    const age = i / trail.length;
    ctx.beginPath();
    ctx.moveTo(trail[i-1].x, trail[i-1].y);
    ctx.lineTo(trail[i].x, trail[i].y);
    ctx.strokeStyle = `rgba(176,96,58,${age * age * 0.45})`;
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }
  const last = trail[trail.length - 1];
  ctx.beginPath();
  ctx.arc(last.x, last.y, 2.6, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(176,96,58,0.7)';
  ctx.fill();
  PLANET.next(draw);
}

draw();
