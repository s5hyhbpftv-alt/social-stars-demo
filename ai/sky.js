// Social Stars AI — «небо»: точки-упоминания собираются в созвездие-фигуру.
// Использование: <div data-sky="star"></div>. Фигуры: star, grid, network, wave, rank, cleanse, flow, stairs, orbit.
(() => {
  const TAU = Math.PI * 2;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // детерминированный генератор, чтобы созвездие было одинаковым при каждом открытии
  const rng = seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const ease = t => 1 - Math.pow(1 - t, 3);
  const lerp = (a, b, t) => a + (b - a) * t;

  // точки вдоль отрезка
  const seg = (out, x1, y1, x2, y2, n, o = {}) => {
    const start = out.length;
    for (let i = 0; i < n; i++) { const t = n === 1 ? 0 : i / (n - 1); out.push({ x: lerp(x1, x2, t), y: lerp(y1, y2, t), ...o }); }
    return start;
  };
  const chain = (edges, from, n) => { for (let i = from; i < from + n - 1; i++) edges.push([i, i + 1]); };

  // ---------- фигуры (координаты в квадрате -0.5…0.5)
  const SHAPES = {
    star(R) {
      const P = [], E = [];
      const verts = [];
      for (let i = 0; i < 10; i++) {
        const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? .165 : .42;
        verts.push([Math.cos(a) * r, Math.sin(a) * r]);
      }
      const k0 = P.length;
      verts.forEach((v, i) => {
        const w = verts[(i + 1) % 10];
        for (let j = 0; j < 4; j++) { const t = j / 4; P.push({ x: lerp(v[0], w[0], t), y: lerp(v[1], w[1], t), s: j ? 1.4 : 2.6, c: 'accent' }); }
      });
      for (let i = k0; i < P.length; i++) E.push([i, i + 1 < P.length ? i + 1 : k0, 'accent']);
      const core = P.push({ x: 0, y: 0, s: 4, c: 'accent', halo: 1 }) - 1;
      for (let i = 1; i < 10; i += 2) E.push([core, k0 + i * 4, 'faint']);
      // упоминания вокруг — часть из них «цитируется» звездой
      for (let i = 0; i < 70; i++) {
        const a = R() * TAU, r = .5 + R() * .55;
        const p = P.push({ x: Math.cos(a) * r * 1.15, y: Math.sin(a) * r * .9, s: .8 + R() * 1.6, c: 'ink' }) - 1;
        if (r < .72 && R() < .55) {
          let best = k0, bd = 9;
          for (let j = k0; j < k0 + 40; j += 4) { const d = Math.hypot(P[j].x - P[p].x, P[j].y - P[p].y); if (d < bd) { bd = d; best = j; } }
          E.push([p, best, 'faint']);
        }
      }
      return { P, E };
    },

    grid(R) { // макет сайта
      const P = [], E = [];
      const rect = (x, y, w, h, n, o) => { const s = P.length;
        seg(P, x, y, x + w, y, n, o); seg(P, x + w, y, x + w, y + h, Math.max(2, n * h / w | 0), o);
        seg(P, x + w, y + h, x, y + h, n, o); seg(P, x, y + h, x, y, Math.max(2, n * h / w | 0), o);
        for (let i = s; i < P.length - 1; i++) E.push([i, i + 1]); E.push([P.length - 1, s]); };
      rect(-.46, -.34, .92, .68, 16, { s: 1.2, c: 'ink' });            // окно браузера
      let s = seg(P, -.46, -.25, .46, -.25, 16, { s: .9, c: 'ink' }); chain(E, s, 16);
      s = seg(P, -.38, -.15, .08, -.15, 8, { s: 1.6, c: 'accent' }); chain(E, s, 8);   // заголовок
      s = seg(P, -.38, -.09, -.02, -.09, 6, { s: 1.2, c: 'accent' }); chain(E, s, 6);
      s = seg(P, -.38, -.02, -.2, -.02, 3, { s: 1.6, c: 'accent' }); chain(E, s, 3);   // кнопка
      rect(.14, -.18, .24, .2, 5, { s: 1, c: 'ink' });                 // изображение
      rect(-.38, .08, .22, .18, 4, { s: 1, c: 'ink' }); rect(-.11, .08, .22, .18, 4, { s: 1, c: 'ink' }); rect(.16, .08, .22, .18, 4, { s: 1, c: 'ink' });
      const ai = P.push({ x: .38, y: .3, s: 3.4, c: 'accent', halo: 1 }) - 1;    // ИИ-консультант
      E.push([ai, P.length - 3, 'faint']);
      for (let i = 0; i < 26; i++) { const a = R() * TAU, r = .55 + R() * .4; P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r * .8, s: .7 + R(), c: 'ink' }); }
      return { P, E };
    },

    network(R) { // агент и инструменты
      const P = [], E = [];
      const hub = P.push({ x: 0, y: 0, s: 5, c: 'accent', halo: 1 }) - 1;
      const n = 6;
      for (let i = 0; i < n; i++) {
        const a = -Math.PI / 2 + i * TAU / n + (R() - .5) * .2, r = .27 + R() * .04;
        const t = P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r, s: 3, c: 'ink' }) - 1;
        E.push([hub, t, 'pulse']);
        const leaves = 4 + (R() * 4 | 0);
        for (let j = 0; j < leaves; j++) {
          const b = a + (j - leaves / 2) * .28, q = .12 + R() * .07;
          const l = P.push({ x: P[t].x + Math.cos(b) * q, y: P[t].y + Math.sin(b) * q, s: 1.2, c: 'ink' }) - 1;
          E.push([t, l]);
        }
      }
      for (let i = 0; i < 24; i++) { const a = R() * TAU, r = .58 + R() * .35; P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r * .85, s: .7 + R(), c: 'ink' }); }
      return { P, E, pulses: true };
    },

    wave(R) { // голос
      const P = [], E = [], n = 90;
      for (let k = 0; k < 2; k++) {
        const s = P.length;
        for (let i = 0; i < n; i++) P.push({ x: -.48 + i * .96 / (n - 1), y: 0, s: 1.3, c: i > 22 && i < 68 ? 'accent' : 'ink', wave: k ? -1 : 1, u: i / (n - 1) });
        chain(E, s, n);
      }
      for (let i = 0; i < n; i += 3) E.push([i, i + n, 'faint']);
      for (let i = 0; i < 30; i++) { const a = R() * TAU, r = .55 + R() * .4; P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r * .8, s: .7 + R(), c: 'ink' }); }
      return { P, E, update(P, t) {
        for (const p of P) if (p.wave) {
          const env = Math.sin(p.u * Math.PI) ** 1.5;
          const talk = .55 + .45 * Math.sin(t * 1.9) * Math.sin(t * .7 + 1);
          const y = env * talk * (.3 * Math.sin(p.u * 17 + t * 4.2) + .12 * Math.sin(p.u * 39 - t * 6.3));
          p.ty = p.base + y * p.wave + p.wave * env * .035;
        }
      } };
    },

    rank(R) { // выдача и ответ
      const P = [], E = [];
      const rows = 6;
      for (let r = 0; r < rows; r++) {
        const y = -.3 + r * .12, len = r === 0 ? .62 : .5 - r * .04, n = r === 0 ? 11 : 8;
        const s = seg(P, -.42, y, -.42 + len, y, n, { s: r === 0 ? 2 : 1.1, c: r === 0 ? 'accent' : 'ink' });
        chain(E, s, n);
        if (r) E.push([s, 0, 'faint']);
      }
      const ans = P.push({ x: .36, y: -.3, s: 5, c: 'accent', halo: 1 }) - 1;
      E.push([10, ans, 'accent']);
      for (let i = 0; i < 30; i++) { const a = R() * TAU, r = .55 + R() * .4; P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r * .8, s: .7 + R(), c: 'ink' }); }
      return { P, E };
    },

    cleanse(R) { // негатив теряет вес, кольцо репутации светлеет
      const P = [], E = [], n = 44;
      const s = P.length;
      for (let i = 0; i < n; i++) { const a = i / n * TAU; P.push({ x: Math.cos(a) * .36, y: Math.sin(a) * .36, s: 1.5, c: 'ink', ring: 1 }); }
      for (let i = s; i < s + n; i++) E.push([i, i + 1 < s + n ? i + 1 : s]);
      for (let i = 0; i < 38; i++) {
        const a = R() * TAU, r = Math.sqrt(R()) * .28, bad = i < 11;
        const p = P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r, s: bad ? 2.4 : 1.2, c: bad ? 'bad' : 'ink', bad }) - 1;
        if (R() < .5) E.push([p, s + (Math.round((a / TAU) * n) % n), 'faint']);
      }
      for (let i = 0; i < 26; i++) { const a = R() * TAU, r = .58 + R() * .38; P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r * .85, s: .7 + R(), c: 'ink' }); }
      return { P, E, update(P, t) {
        const k = Math.min(1, Math.max(0, (t - 2.6) / 3));
        for (const p of P) {
          if (p.bad) { p.fade = 1 - k * .88; p.push = k; }
          if (p.ring) p.glow = k;
        }
      } };
    },

    flow(R) { // контент-поток
      const P = [], E = [];
      const curve = (u, lane) => {
        const x = -.5 + u;
        const spread = u < .45 ? (1 - u / .45) : (u > .6 ? (u - .6) / .4 : 0);
        return [x, lane * .22 * spread + Math.sin(u * 7 + lane) * .015];
      };
      for (let i = 0; i < 210; i++) {
        const lane = [-1.5, -.75, 0, .75, 1.5][i % 5] + (R() - .5) * .25;
        P.push({ x: 0, y: 0, s: 1 + R() * 1.4, c: R() < .35 ? 'accent' : 'ink', stream: 1, u: R(), lane, sp: .04 + R() * .035 });
      }
      const hub = P.push({ x: .03, y: 0, s: 4, c: 'accent', halo: 1 }) - 1;
      return { P, E, update(P, t, dt) {
        for (const p of P) if (p.stream) {
          p.u = (p.u + p.sp * dt) % 1;
          const [x, y] = curve(p.u, p.lane); p.tx = x; p.ty = y;
          p.fade = Math.min(1, p.u * 8, (1 - p.u) * 8);
        }
      } };
    },

    stairs(R) { // уровни зрелости
      const P = [], E = [];
      let x = -.44, y = .3;
      for (let k = 0; k < 5; k++) {
        const top = k === 4;
        let s = seg(P, x, y, x + .18, y, 6, { s: top ? 2 : 1.2, c: top ? 'accent' : 'ink' }); chain(E, s, 6);
        if (!top) { s = seg(P, x + .18, y, x + .18, y - .15, 4, { s: 1.2, c: 'ink' }); chain(E, s, 4); E.push([s - 1, s]); }
        E.push([P.length - 1 - (top ? 0 : 4), P.length - (top ? 1 : 4)]);
        x += .18; y -= .15;
      }
      const star = P.push({ x: .38, y: -.42, s: 5, c: 'accent', halo: 1 }) - 1;
      E.push([star - 1, star, 'accent']);
      for (let i = 0; i < 30; i++) { const a = R() * TAU, r = .55 + R() * .4; P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r * .8, s: .7 + R(), c: 'ink' }); }
      return { P, E };
    },

    orbit(R) { // система модулей
      const P = [], E = [];
      const core = P.push({ x: 0, y: 0, s: 6, c: 'accent', halo: 1 }) - 1;
      const orbits = [[.16, 8], [.28, 14], [.4, 20]];
      orbits.forEach(([r, n], k) => {
        const s = P.length;
        for (let i = 0; i < n; i++) P.push({ x: 0, y: 0, s: i === 0 ? 3 : 1, c: i === 0 ? 'accent' : 'ink', orb: r, ph: i / n * TAU + k, w: (.18 - k * .04) * (k % 2 ? -1 : 1) });
        for (let i = s; i < s + n; i++) E.push([i, i + 1 < s + n ? i + 1 : s, 'faint']);
        E.push([core, s, 'pulse']);
      });
      for (let i = 0; i < 22; i++) { const a = R() * TAU, r = .56 + R() * .38; P.push({ x: Math.cos(a) * r, y: Math.sin(a) * r * .85, s: .7 + R(), c: 'ink' }); }
      return { P, E, pulses: true, update(P, t) {
        for (const p of P) if (p.orb) { const a = p.ph + t * p.w; p.tx = Math.cos(a) * p.orb * 1.15; p.ty = Math.sin(a) * p.orb * .8; }
      } };
    },
  };

  // ---------- рендер
  class Sky {
    constructor(el) {
      this.el = el; this.kind = el.dataset.sky;
      this.cx = parseFloat(el.dataset.skyX || .5); this.cy = parseFloat(el.dataset.skyY || .5);
      this.scale = parseFloat(el.dataset.skyScale || .9);
      this.cv = document.createElement('canvas'); this.cv.setAttribute('aria-hidden', 'true');
      el.appendChild(this.cv); this.ctx = this.cv.getContext('2d');
      const R = rng(7919 + this.kind.length * 131);
      const sh = SHAPES[this.kind](R);
      this.P = sh.P; this.E = sh.E; this.update = sh.update; this.pulses = sh.pulses;
      this.P.forEach(p => { p.base = p.y; p.tx = p.x; p.ty = p.y; p.sx = (R() - .5) * 1.6; p.sy = (R() - .5) * 1.6; p.d = R() * .45; p.ph = p.ph ?? R() * TAU; p.fade = p.fade ?? 1; });
      this.pl = this.E.filter(e => e[2] === 'pulse').map((e, i) => ({ e, k: i * .37 % 1 }));
      this.mouse = { x: -1e4, y: -1e4 };
      this.t0 = performance.now(); this.last = this.t0; this.running = false;
      this.colors();
      new ResizeObserver(() => this.resize()).observe(el); this.resize();
      el.addEventListener('pointermove', e => { const r = this.cv.getBoundingClientRect(); this.mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
      el.addEventListener('pointerleave', () => this.mouse = { x: -1e4, y: -1e4 });
      if (reduce) { this.t0 -= 1e5; this.frame(performance.now()); return; }
      new IntersectionObserver(es => es.forEach(x => x.isIntersecting ? this.start() : this.stop())).observe(el);
    }
    colors() {
      const cs = getComputedStyle(document.documentElement);
      const v = (n, f) => (cs.getPropertyValue(n).trim() || f);
      this.C = { ink: v('--sky-ink', '#1b2130'), accent: v('--sky-accent', '#b08a63'), line: v('--sky-line', '#c9d0da'), bad: v('--sky-bad', '#c2574b') };
    }
    resize() {
      const r = this.el.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio || 1);
      this.W = r.width; this.H = r.height; this.dpr = dpr;
      this.cv.width = r.width * dpr; this.cv.height = r.height * dpr;
      this.cv.style.width = r.width + 'px'; this.cv.style.height = r.height + 'px';
      this.S = Math.min(this.W, this.H) * this.scale;
      if (!this.running) this.frame(performance.now());
    }
    start() { if (this.running) return; this.running = true; this.last = performance.now(); const loop = t => { if (!this.running) return; this.frame(t); requestAnimationFrame(loop); }; requestAnimationFrame(loop); }
    stop() { this.running = false; }
    map(x, y) { return [this.W * this.cx + x * this.S, this.H * this.cy + y * this.S]; }
    frame(now) {
      const { ctx, dpr, P, E, C } = this; const t = (now - this.t0) / 1000, dt = Math.min(.05, (now - this.last) / 1000); this.last = now;
      if (this.update) this.update(P, t, dt);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, this.W, this.H);
      // позиции
      for (const p of P) {
        const k = ease(Math.min(1, Math.max(0, (t - p.d) / 2.2)));
        const [tx, ty] = this.map(p.tx, p.ty);
        const [sx, sy] = this.map(p.sx, p.sy);
        let x = lerp(sx, tx, k), y = lerp(sy, ty, k);
        if (!p.stream && !p.orb) { x += Math.sin(t * .6 + p.ph) * 2.2 * k; y += Math.cos(t * .5 + p.ph * 1.3) * 2.2 * k; }
        if (p.push) { const dx = x - this.W * this.cx, dy = y - this.H * this.cy, m = Math.hypot(dx, dy) || 1; x += dx / m * p.push * this.S * .35; y += dy / m * p.push * this.S * .35; }
        const mx = x - this.mouse.x, my = y - this.mouse.y, md = Math.hypot(mx, my);
        if (md < 110) { const f = (1 - md / 110) * 14; x += mx / md * f; y += my / md * f; }
        p.px = x; p.py = y; p.k = k;
      }
      // рёбра
      ctx.lineCap = 'round';
      for (const [a, b, kind] of E) {
        const A = P[a], B = P[b], al = Math.min(A.k, B.k) ** 3 * Math.min(A.fade, B.fade);
        if (al < .02) continue;
        ctx.strokeStyle = kind === 'accent' ? C.accent : C.line;
        ctx.globalAlpha = al * (kind === 'faint' ? .45 : kind === 'accent' ? .7 : .9);
        ctx.lineWidth = kind === 'accent' ? 1.2 : 1;
        ctx.beginPath(); ctx.moveTo(A.px, A.py); ctx.lineTo(B.px, B.py); ctx.stroke();
      }
      // импульсы по рёбрам
      if (this.pulses && !reduce) for (const q of this.pl) {
        q.k = (q.k + dt * .45) % 1; const A = P[q.e[0]], B = P[q.e[1]];
        ctx.globalAlpha = Math.min(A.k, B.k) * Math.sin(q.k * Math.PI);
        ctx.fillStyle = C.accent; ctx.beginPath(); ctx.arc(lerp(A.px, B.px, q.k), lerp(A.py, B.py, q.k), 2.2, 0, TAU); ctx.fill();
      }
      // точки
      for (const p of P) {
        const tw = .85 + .15 * Math.sin(t * 1.3 + p.ph * 3);
        let col = C[p.c] || C.ink, a = (p.c === 'ink' ? .55 : .95) * tw * p.fade * Math.max(.15, p.k);
        if (p.glow) col = C.accent, a = lerp(.55, .95, p.glow) * tw;
        if (p.halo) { ctx.globalAlpha = .16 * p.k; ctx.fillStyle = C.accent; ctx.beginPath(); ctx.arc(p.px, p.py, p.s * 4.2, 0, TAU); ctx.fill(); }
        ctx.globalAlpha = a; ctx.fillStyle = col;
        ctx.beginPath(); ctx.arc(p.px, p.py, p.s * (p.glow ? 1 + p.glow * .4 : 1), 0, TAU); ctx.fill();
      }
      ctx.globalAlpha = 1;
    }
  }

  const init = () => document.querySelectorAll('[data-sky]').forEach(el => { if (!el.__sky) el.__sky = new Sky(el); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
