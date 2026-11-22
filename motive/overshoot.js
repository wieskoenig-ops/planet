/* Hintergrundmotiv „overshoot“: Eine Temperaturkurve steigt über die gestrichelte Marke,
   erreicht einen Gipfel und sinkt wieder darunter. Darunter folgt eine zweite, kupferne Spur,
   der Zustand des Systems: Er folgt dem Anstieg, sinkt aber nach dem Gipfel kaum wieder. */
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H;
function resize() { W = canvas.width = canvas.clientWidth; H = canvas.height = canvas.clientHeight; }
resize();
window.addEventListener('resize', resize);

const N = 520;                       // Schritte pro Durchlauf
let t = 0, fade = 1;
function temp(u) {                   // 0..1 → Temperatur (0 = Ausgang, 1 = Marke)
  const rise = 1.35 / (1 + Math.exp(-11 * (u - 0.32)));
  const fall = 0.85 / (1 + Math.exp(-9 * (u - 0.66)));
  return rise - fall;
}
const tempPts = [], statePts = [];
let state = 0, crossed = false;
function reset() { t = 0; state = 0; crossed = false; tempPts.length = 0; statePts.length = 0; fade = 1; }
reset();

function X(u) { return W * (0.06 + 0.88 * u); }
function Y(v) { return H * (0.82 - v * 0.42); }

function step() {
  const u = t / N, T = temp(u);
  // Der Zustand folgt der Temperatur, bis sie die Marke überschreitet.
  // Danach bleibt er oben: Die Temperatur sinkt, der Zustand kaum.
  if (crossed) state = Math.max(state - 0.0004, T); else { state = T; if (T > 1) crossed = true; }
  tempPts.push([X(u), Y(T)]);
  statePts.push([X(u), Y(state) + 5]);
  t++;
}
function line(pts, style, w) {
  ctx.beginPath();
  pts.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
  ctx.strokeStyle = style; ctx.lineWidth = w; ctx.stroke();
}
function draw() {
  ctx.clearRect(0, 0, W, H);
  ctx.setLineDash([3, 7]);
  ctx.beginPath(); ctx.moveTo(0, Y(1)); ctx.lineTo(W, Y(1));
  ctx.strokeStyle = `rgba(${PLANET.ink},${0.2 * fade})`; ctx.lineWidth = 0.7; ctx.stroke();
  ctx.setLineDash([]);
  for (let k = 0; k < 2 && t <= N; k++) step();
  if (t > N) { fade -= 0.008; if (fade <= 0) reset(); }
  line(tempPts, `rgba(${PLANET.ink},${0.22 * fade})`, 1);
  line(statePts, `rgba(176,96,58,${0.45 * fade})`, 1.2);
  const p = tempPts[tempPts.length - 1];
  if (p) { ctx.beginPath(); ctx.arc(p[0], p[1], 2.4, 0, 7); ctx.fillStyle = `rgba(${PLANET.ink},${0.4 * fade})`; ctx.fill(); }
  PLANET.next(draw);
}
draw();
