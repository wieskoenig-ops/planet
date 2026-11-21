/* Hintergrundmotiv „politik“, übernommen von emergenz.art/punkt/politik/ */
// Hintergrund: Unten wiederholen sich kurze Bögen, die Legislaturperioden.
// Darüber steigt eine kupferne Kurve stetig an und kreuzt irgendwann die gestrichelte Schwelle.
// Die Bögen beginnen immer wieder von vorn, die Kurve nicht.
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H;

function resize() {
  W = canvas.width  = canvas.clientWidth;
  H = canvas.height = canvas.clientHeight;
}
resize();
window.addEventListener('resize', resize);

const SPAN = 60;        // sichtbare Jahre
const END = 150;        // Länge eines Durchlaufs in Jahren
const PERIOD = 4;       // Legislaturperiode
const THRESH = 0.55;    // Schwelle (Anteil der Höhe)
let t = 0;

function level(T) {
  if (T < 0) return 0;
  return Math.pow(T / END, 1.7) + 0.006 * Math.sin(T * Math.PI * 2);
}
function sx(T) { return (T - (t - SPAN)) / SPAN * W; }
function sy(v) { return H * (0.8 - 0.62 * v); }

function draw() {
  ctx.clearRect(0, 0, W, H);
  t += 0.02;
  if (t > END + 20) t = 0;
  const fade = t < 4 ? t / 4 : (t > END + 12 ? Math.max(0, (END + 20 - t) / 8) : 1);
  ctx.globalAlpha = fade;

  // Schwelle
  ctx.setLineDash([3, 7]);
  ctx.strokeStyle = `rgba(${PLANET.ink},0.1)`;
  ctx.lineWidth = 0.6;
  ctx.beginPath();
  ctx.moveTo(0, sy(THRESH));
  ctx.lineTo(W, sy(THRESH));
  ctx.stroke();
  ctx.setLineDash([]);

  // Legislaturperioden
  const base = H * 0.9, hump = H * 0.045;
  for (let k = Math.floor((t - SPAN) / PERIOD); k * PERIOD <= t; k++) {
    const a = k * PERIOD, b = Math.min(a + PERIOD, t);
    if (b <= a) continue;
    ctx.beginPath();
    for (let i = 0; i <= 24; i++) {
      const T = a + (b - a) * i / 24;
      const u = (T - a) / PERIOD;
      const y = base - Math.sin(u * Math.PI) * hump;
      if (i === 0) ctx.moveTo(sx(T), y); else ctx.lineTo(sx(T), y);
    }
    ctx.strokeStyle = `rgba(${PLANET.ink},0.13)`;
    ctx.lineWidth = 0.7;
    ctx.stroke();
  }

  // Die andere Uhr
  ctx.beginPath();
  for (let i = 0; i <= 200; i++) {
    const T = t - SPAN + SPAN * i / 200;
    const x = sx(T), y = sy(level(T));
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  const over = level(t) > THRESH;
  ctx.strokeStyle = over ? 'rgba(176,96,58,0.55)' : 'rgba(176,96,58,0.38)';
  ctx.lineWidth = 1.2;
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(sx(t), sy(level(t)), 2.6, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(176,96,58,0.75)';
  ctx.fill();

  ctx.globalAlpha = 1;
  PLANET.next(draw);
}

draw();
