/* Hintergrundmotiv „planetare kognition“ */
// Hintergrund: verstreute Knoten, zwischen denen nach und nach Verbindungen entstehen.
// Über die Verbindungen laufen Signale; erreicht eines einen Knoten, leuchtet er kurz auf und
// gibt es manchmal weiter. Es gibt keinen Moment, in dem das Netz „fertig“ ist: Es verdichtet
// sich langsam, lockert sich wieder, und die Signale werden mit der Dichte häufiger.
const canvas = document.getElementById('bg-canvas');
const ctx    = canvas.getContext('2d');
let W, H, nodes, links, pulses;

const CYCLE = 4800;   // Bilder für ein Verdichten und Lockern (etwa 200 Sekunden bei 24 fps)
let frame = 0;

function resize() {
  W = canvas.width  = canvas.clientWidth;
  H = canvas.height = canvas.clientHeight;
  const n = Math.max(40, Math.min(110, Math.round(W * H / 14000)));
  nodes = [];
  for (let i = 0; i < n; i++) {
    nodes.push({ x: Math.random() * W, y: Math.random() * H, glow: 0 });
  }
  // mögliche Verbindungen: jeder Knoten zu seinen nächsten Nachbarn, in zufälliger Reihenfolge
  const cand = [];
  for (let i = 0; i < n; i++) {
    const near = nodes.map((b, j) => [j, Math.hypot(b.x - nodes[i].x, b.y - nodes[i].y)])
      .filter(([j]) => j !== i).sort((a, b) => a[1] - b[1]).slice(0, 4);
    for (const [j] of near) cand.push([Math.min(i, j), Math.max(i, j)]);
  }
  const seen = new Set();
  links = [];
  for (const [a, b] of cand) {
    const k = a + ',' + b;
    if (seen.has(k)) continue;
    seen.add(k);
    links.push({ a, b, t: Math.random() });   // t: ab welcher Dichte die Verbindung besteht
  }
  pulses = [];
}
resize();
window.addEventListener('resize', resize);

function draw() {
  frame++;
  const density = 0.15 + 0.8 * (0.5 - 0.5 * Math.cos(2 * Math.PI * frame / CYCLE));
  const live = links.filter(l => l.t < density);

  // neue Signale, häufiger je dichter das Netz
  if (live.length && Math.random() < 0.03 + density * 0.12) {
    const l = live[Math.floor(Math.random() * live.length)];
    pulses.push(Math.random() < 0.5 ? { from: l.a, to: l.b, p: 0 } : { from: l.b, to: l.a, p: 0 });
  }

  ctx.clearRect(0, 0, W, H);
  ctx.lineWidth = 1;
  for (const l of live) {
    const A = nodes[l.a], B = nodes[l.b];
    const fadeIn = Math.min(1, (density - l.t) * 12);
    ctx.beginPath();
    ctx.moveTo(A.x, A.y);
    ctx.lineTo(B.x, B.y);
    ctx.strokeStyle = `rgba(${PLANET.ink},${0.05 * fadeIn})`;
    ctx.stroke();
  }

  const next = [];
  for (const s of pulses) {
    s.p += 0.025;
    const A = nodes[s.from], B = nodes[s.to];
    if (s.p >= 1) {
      B.glow = 1;
      // weitergeben an eine bestehende Verbindung des erreichten Knotens
      if (Math.random() < 0.35 + density * 0.3) {
        const out = live.filter(l => (l.a === s.to || l.b === s.to) && l.a !== s.from && l.b !== s.from);
        if (out.length) {
          const l = out[Math.floor(Math.random() * out.length)];
          next.push({ from: s.to, to: l.a === s.to ? l.b : l.a, p: 0 });
        }
      }
      continue;
    }
    const x = A.x + (B.x - A.x) * s.p, y = A.y + (B.y - A.y) * s.p;
    ctx.beginPath();
    ctx.arc(x, y, 1.4, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(176,96,58,0.45)';
    ctx.fill();
    next.push(s);
  }
  pulses = next.slice(-120);

  for (const nd of nodes) {
    ctx.beginPath();
    ctx.arc(nd.x, nd.y, 1.5 + nd.glow * 1.5, 0, Math.PI * 2);
    ctx.fillStyle = nd.glow > 0.05
      ? `rgba(176,96,58,${0.12 + nd.glow * 0.35})`
      : `rgba(${PLANET.ink},0.12)`;
    ctx.fill();
    nd.glow *= 0.94;
  }

  PLANET.next(draw);
}

draw();
