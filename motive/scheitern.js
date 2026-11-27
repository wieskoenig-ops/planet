/* Hintergrundmotiv „scheitern“ */
// Hintergrund: ein Ring aus Segmenten, der Verhandlungstisch. Ein Segment fehlt: die offene Stelle.
// Im Ring kreisen Punkte. Wer an die Lücke kommt, kann hinaus und sammelt sich draußen mit anderen
// zu kleinen Gruppen. Mit der Zeit schließt sich die Lücke wieder, und ein anderes Segment fällt aus.
const canvas = document.getElementById('bg-canvas');
const ctx    = canvas.getContext('2d');
let W, H, cx, cy, R, dots, gap, gapAge;

const SEG = 36;          // Segmente im Ring
const LIFE = 1400;       // Bilder, die eine Lücke offen bleibt
let frame = 0;

function resize() {
  W = canvas.width  = canvas.clientWidth;
  H = canvas.height = canvas.clientHeight;
  cx = W * 0.5; cy = H * 0.5;
  R = Math.min(W, H) * 0.32;
  dots = [];
  for (let i = 0; i < 90; i++) {
    dots.push({ a: Math.random() * Math.PI * 2, r: R * (0.3 + Math.random() * 0.6),
                w: (0.002 + Math.random() * 0.004) * (Math.random() < 0.5 ? -1 : 1),
                out: false, x: 0, y: 0, vx: 0, vy: 0, home: null });
  }
  gap = Math.floor(Math.random() * SEG); gapAge = 0;
}
resize();
window.addEventListener('resize', resize);

function segAngle(i) { return (i + 0.5) * 2 * Math.PI / SEG; }

function draw() {
  frame++; gapAge++;
  if (gapAge > LIFE) {                       // Lücke schließt sich, eine andere öffnet sich
    gap = (gap + 7 + Math.floor(Math.random() * 20)) % SEG; gapAge = 0;
    for (const d of dots) if (d.out && Math.random() < 0.5) d.fade = 1;
  }
  const open = Math.min(1, gapAge / 120) * Math.min(1, (LIFE - gapAge) / 120);
  const ga = segAngle(gap);

  ctx.clearRect(0, 0, W, H);
  ctx.lineWidth = 1.2;
  for (let i = 0; i < SEG; i++) {
    const a0 = i * 2 * Math.PI / SEG + 0.02, a1 = (i + 1) * 2 * Math.PI / SEG - 0.02;
    const alpha = i === gap ? 0.08 * (1 - open) : 0.08;
    if (alpha < 0.005) continue;
    ctx.beginPath();
    ctx.arc(cx, cy, R, a0, a1);
    ctx.strokeStyle = `rgba(${PLANET.ink},${alpha})`;
    ctx.stroke();
  }

  for (const d of dots) {
    if (!d.out) {
      d.a += d.w;
      d.x = cx + Math.cos(d.a) * d.r; d.y = cy + Math.sin(d.a) * d.r;
      // nahe der Lücke: manche treiben hinaus
      let da = Math.atan2(Math.sin(d.a - ga), Math.cos(d.a - ga));
      if (open > 0.6 && Math.abs(da) < 0.06 && Math.random() < 0.08) {
        d.out = true;
        d.vx = Math.cos(d.a) * 0.6; d.vy = Math.sin(d.a) * 0.6;
        const ha = ga + (Math.random() - 0.5) * 1.6;
        const hr = R * (1.35 + Math.random() * 0.5);
        d.home = { x: cx + Math.cos(ha) * hr, y: cy + Math.sin(ha) * hr };
      }
    } else {
      // draußen: zu einem Sammelpunkt, in der Nähe anderer
      d.vx += (d.home.x - d.x) * 0.0006; d.vy += (d.home.y - d.y) * 0.0006;
      for (const e of dots) {
        if (e === d || !e.out) continue;
        const dx = e.x - d.x, dy = e.y - d.y, q = dx * dx + dy * dy;
        if (q < 3600 && q > 1) { d.vx += dx * 0.00004; d.vy += dy * 0.00004; }
      }
      d.vx *= 0.97; d.vy *= 0.97;
      d.x += d.vx; d.y += d.vy;
      if (d.fade !== undefined) {
        d.fade -= 0.01;
        if (d.fade <= 0) {                   // zurück in den Ring
          d.out = false; d.fade = undefined;
          d.a = Math.random() * Math.PI * 2; d.r = R * (0.3 + Math.random() * 0.6);
        }
      }
    }
    const f = d.fade === undefined ? 1 : Math.max(0, d.fade);
    ctx.beginPath();
    ctx.arc(d.x, d.y, 1.6, 0, Math.PI * 2);
    ctx.fillStyle = d.out ? `rgba(176,96,58,${0.4 * f})` : `rgba(${PLANET.ink},0.14)`;
    ctx.fill();
  }

  PLANET.next(draw);
}

draw();
