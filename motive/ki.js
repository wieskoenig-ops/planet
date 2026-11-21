/* Hintergrundmotiv „ki“, übernommen von emergenz.art/punkt/ki/ */
// Hintergrund: gekoppelte Taktgeber (Kuramoto-Modell).
// Jeder Taktgeber hat sein eigenes Tempo und spürt schwach den gemeinsamen Takt aller anderen.
// Die Kopplung K wird langsam stärker und wieder schwächer. Unterhalb einer Schwelle bleibt es
// beim Durcheinander; oberhalb finden die Taktgeber in kurzer Zeit zu einem gemeinsamen Rhythmus.
const canvas = document.getElementById('bg-canvas');
const ctx    = canvas.getContext('2d');
let W, H, GW, GH, SP, phase, omega;

const SPREAD = 0.45;   // Streuung der Eigentempi
const K_MAX  = 1.6;    // die Schwelle liegt bei etwa 0,72
const CYCLE  = 5400;   // Bilder für einen Durchgang (etwa 90 Sekunden)
const DT     = 0.03;
let frame = 0;

function gauss() {
  return Math.sqrt(-2 * Math.log(Math.random() || 1e-9)) * Math.cos(2 * Math.PI * Math.random());
}

function resize() {
  W = canvas.width  = canvas.clientWidth;
  H = canvas.height = canvas.clientHeight;
  SP = Math.max(22, Math.min(34, Math.round(Math.min(W, H) / 22)));
  GW = Math.ceil(W / SP) + 1;
  GH = Math.ceil(H / SP) + 1;
  const n = GW * GH;
  phase = new Float32Array(n);
  omega = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    phase[i] = Math.random() * Math.PI * 2;
    omega[i] = 0.25 + gauss() * SPREAD;
  }
}
resize();
window.addEventListener('resize', resize);

function draw() {
  frame++;
  const K = K_MAX * (0.5 - 0.5 * Math.cos(2 * Math.PI * frame / CYCLE));

  // gemeinsamer Takt: Stärke r und Phase psi des Mittelwerts
  let cs = 0, sn = 0;
  for (let i = 0; i < phase.length; i++) { cs += Math.cos(phase[i]); sn += Math.sin(phase[i]); }
  const r = Math.hypot(cs, sn) / phase.length, psi = Math.atan2(sn, cs);
  for (let i = 0; i < phase.length; i++) {
    phase[i] += DT * (omega[i] + K * r * Math.sin(psi - phase[i]));
  }

  ctx.clearRect(0, 0, W, H);
  ctx.lineWidth = 1;
  const L = SP * 0.32;
  for (let y = 0; y < GH; y++) {
    for (let x = 0; x < GW; x++) {
      const p = phase[y * GW + x];
      // wie sehr dieser Taktgeber im gemeinsamen Rhythmus mitschwingt
      const inStep = r * Math.max(0, Math.cos(p - psi));
      const cx = x * SP, cy = y * SP;
      const dx = Math.cos(p) * L, dy = Math.sin(p) * L;
      ctx.beginPath();
      ctx.moveTo(cx - dx, cy - dy);
      ctx.lineTo(cx + dx, cy + dy);
      ctx.strokeStyle = inStep > 0.35
        ? `rgba(176,96,58,${0.08 + inStep * 0.4})`
        : `rgba(${PLANET.ink},0.07)`;
      ctx.stroke();
    }
  }

  PLANET.next(draw);
}

draw();
