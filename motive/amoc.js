/* Hintergrundmotiv „amoc“, übernommen von emergenz.art/punkt/amoc/ */
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H;

function resize() {
  W = canvas.width  = canvas.clientWidth;
  H = canvas.height = canvas.clientHeight;
}
resize();
window.addEventListener('resize', resize);

const N_NODES = 48;
const nodes = [];
const MAX_DIST = 160;
const TENSION_CYCLE = 520;
let frame = 0;

for (let i = 0; i < N_NODES; i++) {
  nodes.push({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 0.2,
    vy: (Math.random() - 0.5) * 0.2,
    r: 1.2 + Math.random() * 1.4,
  });
}

const edges = [];

function buildEdges(threshold) {
  edges.length = 0;
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[i].x - nodes[j].x;
      const dy = nodes[i].y - nodes[j].y;
      const d = Math.sqrt(dx*dx + dy*dy);
      if (d < threshold) edges.push({ a: i, b: j, d });
    }
  }
}

function draw() {
  ctx.clearRect(0, 0, W, H);
  frame++;

  const t = (frame % TENSION_CYCLE) / TENSION_CYCLE;
  let threshold, globalAlpha;

  if (t < 0.45) {
    threshold = MAX_DIST * (0.3 + t / 0.45 * 0.7);
    globalAlpha = 1;
  } else if (t < 0.55) {
    threshold = MAX_DIST;
    globalAlpha = 1;
  } else if (t < 0.72) {
    const p = (t - 0.55) / 0.17;
    threshold = MAX_DIST * (1 - p * 0.92);
    globalAlpha = 1 - p * 0.65;
  } else {
    threshold = MAX_DIST * 0.08;
    globalAlpha = 0.35;
  }

  buildEdges(threshold);

  for (const n of nodes) {
    n.x += n.vx;
    n.y += n.vy;
    if (n.x < 0 || n.x > W) n.vx *= -1;
    if (n.y < 0 || n.y > H) n.vy *= -1;
    n.x = Math.max(0, Math.min(W, n.x));
    n.y = Math.max(0, Math.min(H, n.y));
  }

  for (const e of edges) {
    const a = nodes[e.a], b = nodes[e.b];
    const proximity = 1 - e.d / threshold;
    const alpha = globalAlpha * proximity * 0.15;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.strokeStyle = `rgba(${PLANET.ink},${alpha})`;
    ctx.lineWidth = 0.5;
    ctx.stroke();
  }

  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    let degree = 0;
    for (const e of edges) { if (e.a === i || e.b === i) degree++; }
    const brightness = Math.min(0.06 + degree * 0.022, 0.38) * globalAlpha;
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${PLANET.ink},${brightness})`;
    ctx.fill();
  }

  PLANET.next(draw);
}

draw();
