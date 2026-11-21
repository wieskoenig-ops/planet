/* Hintergrundmotiv „kippt-hier-etwas“, übernommen von emergenz.art/punkt/kippt-hier-etwas/ */
// Hintergrund: ein Sandhaufen nach Bak, Tang und Wiesenfeld.
// Körner fallen einzeln; eine Zelle mit vier Körnern kippt und gibt je eins an die Nachbarn ab.
// Meist passiert wenig, gelegentlich läuft eine Lawine über das Feld. Kippende Zellen glühen kupfern.
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H, C, R, h, glow, cell;

function resize() {
  W = canvas.width  = canvas.clientWidth;
  H = canvas.height = canvas.clientHeight;
  cell = W < 760 ? 16 : 20;
  C = Math.ceil(W / cell); R = Math.ceil(H / cell);
  h = new Uint8Array(C * R);
  glow = new Float32Array(C * R);
  for (let i = 0; i < h.length; i++) h[i] = Math.random() < 0.7 ? 2 + (Math.random() < 0.5 ? 1 : 0) : Math.floor(Math.random() * 2);
}
resize();
window.addEventListener('resize', resize);

let unstable = [];
let frame = 0;
const DROP_EVERY = 9;   // Frames zwischen zwei Körnern

function step() {
  // eine Welle der Lawine pro Frame, damit man sie wandern sieht
  const next = [];
  for (const i of unstable) {
    if (h[i] < 4) continue;
    h[i] -= 4; glow[i] = 1;
    const x = i % C, y = (i / C) | 0;
    if (x > 0)     { h[i - 1]++; if (h[i - 1] === 4) next.push(i - 1); }
    if (x < C - 1) { h[i + 1]++; if (h[i + 1] === 4) next.push(i + 1); }
    if (y > 0)     { h[i - C]++; if (h[i - C] === 4) next.push(i - C); }
    if (y < R - 1) { h[i + C]++; if (h[i + C] === 4) next.push(i + C); }
    if (h[i] >= 4) next.push(i);
  }
  unstable = next;
}

function draw() {
  frame++;
  if (unstable.length) step();
  else if (frame % DROP_EVERY === 0) {
    const i = (Math.random() * C * R) | 0;
    h[i]++;
    if (h[i] >= 4) unstable.push(i);
  }

  ctx.clearRect(0, 0, W, H);
  const r = cell * 0.09;
  for (let y = 0; y < R; y++) {
    for (let x = 0; x < C; x++) {
      const i = y * C + x;
      const cx = x * cell + cell / 2, cy = y * cell + cell / 2;
      const g = glow[i];
      if (g > 0.02) {
        ctx.fillStyle = `rgba(176,96,58,${0.42 * g})`;
        ctx.fillRect(cx - cell * 0.32, cy - cell * 0.32, cell * 0.64, cell * 0.64);
        glow[i] = g * 0.94;
      }
      const a = [0.025, 0.05, 0.085, 0.13][Math.min(h[i], 3)];
      ctx.fillStyle = `rgba(${PLANET.ink},${a})`;
      ctx.fillRect(cx - r, cy - r, r * 2, r * 2);
    }
  }
  PLANET.next(draw);
}

draw();
