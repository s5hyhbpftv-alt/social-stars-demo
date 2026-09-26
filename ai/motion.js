// Social Stars AI — анимации визуализаций на GSAP 3 (ScrollTrigger, DrawSVG, MotionPath).
// Правило: движение объясняет данные — график растёт, ответ печатается, данные идут по связям.
// Каждая визуализация играет один раз, когда появляется на экране. Без JS и при «уменьшении движения»
// всё видно сразу в конечном состоянии.
(() => {
  const g = window.gsap;
  if (!g || !window.ScrollTrigger) return;
  g.registerPlugin(ScrollTrigger, window.DrawSVGPlugin, window.MotionPathPlugin);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const NS = 'http://www.w3.org/2000/svg';

  // запустить таймлайн, когда элемент доходит до нижней трети экрана
  const onView = (el, build, start = 'clamp(top 86%)') => {
    if (reduce || !el) return;
    const tl = g.timeline({ paused: true });
    build(tl);
    ScrollTrigger.create({ trigger: el, start, once: true, onEnter: () => tl.play() });
  };

  // ——— числа: считаем от нуля, сохраняя формат («316 млрд ₽», «1,5 млн», «+21», «94%»)
  const countUp = (tl, els, at = 0, dur = 1.6) => els.forEach((el, i) => {
    const txt = el.textContent, m = txt.match(/(\d(?:[\d\s  ]*\d)?)(,(\d+))?/);
    if (!m) return;
    const dec = m[3] ? m[3].length : 0, val = parseFloat(m[1].replace(/\D/g, '') + (dec ? '.' + m[3] : ''));
    const pre = txt.slice(0, m.index), post = txt.slice(m.index + m[0].length), o = { v: 0 };
    const fmt = v => v.toLocaleString('ru-RU', { minimumFractionDigits: dec, maximumFractionDigits: dec }).replace(/ /g, ' ');
    el.style.fontVariantNumeric = 'tabular-nums';
    tl.fromTo(o, { v: 0 }, { v: val, duration: dur, ease: 'expo.out', onUpdate: () => { el.textContent = pre + fmt(o.v) + post; },
      onComplete: () => { el.textContent = txt; el.style.fontVariantNumeric = ''; } }, at + i * .08);
  });

  // ——— полосы: растут от левого края
  const grow = (tl, bars, at = 0, axis = 'x') => tl.fromTo(bars, { [axis === 'x' ? 'scaleX' : 'scaleY']: 0 },
    { [axis === 'x' ? 'scaleX' : 'scaleY']: 1, transformOrigin: axis === 'x' ? '0 50%' : '50% 100%', duration: 1.3, ease: 'expo.out', stagger: .07 }, at);

  // ——— текст ответа нейросети печатается по словам
  const words = el => {
    const out = [];
    [...el.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const f = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(w => {
          if (!w) return;
          if (/^\s+$/.test(w)) { f.appendChild(document.createTextNode(w)); return; }
          const s = document.createElement('span'); s.className = 'w'; s.textContent = w; f.appendChild(s); out.push(s);
        });
        n.replaceWith(f);
      } else if (n.nodeType === 1) out.push(n);
    });
    return out;
  };
  const type = (tl, el, at = 0) => { const w = words(el); tl.fromTo(w, { opacity: 0 }, { opacity: 1, duration: .25, stagger: .045, ease: 'none' }, at); return w.length * .045; };

  // ——— схемы связей: <div data-wires="a>b b>c"> и узлы [data-n]. Линии считаются по положению узлов,
  // по ним бегут импульсы. Модификаторы ребра: a>b:dash (пунктир, без импульсов), a>b:3 (толщина).
  const wires = box => {
    const svg = document.createElementNS(NS, 'svg'); svg.classList.add('wires'); svg.setAttribute('aria-hidden', 'true');
    box.prepend(svg); box.classList.add('has-wires');
    const edges = box.dataset.wires.trim().split(/\s+/).map(s => {
      const [ab, ...mods] = s.split(':'), [a, b] = ab.split('>');
      const p = document.createElementNS(NS, 'path'); p.classList.add('wire');
      mods.forEach(m => /^[\d.]+$/.test(m) ? (p.style.strokeWidth = m) : p.classList.add(m));
      svg.appendChild(p);
      return { a: box.querySelector(`[data-n="${a}"]`), b: box.querySelector(`[data-n="${b}"]`), p, mod: mods.includes('dash') ? 'dash' : '', bad: mods.includes('bad'), dir: mods.includes('v') ? 'v' : mods.includes('h') ? 'h' : '' };
    }).filter(e => e.a && e.b);
    const layout = () => {
      const R = box.getBoundingClientRect();
      svg.setAttribute('viewBox', `0 0 ${R.width} ${R.height}`);
      edges.forEach(e => {
        const a = e.a.getBoundingClientRect(), b = e.b.getBoundingClientRect();
        const ax = a.left - R.left, ay = a.top - R.top, bx = b.left - R.left, by = b.top - R.top;
        let d;
        const vert = e.dir === 'v' || (!e.dir && !(b.left >= a.right - 8) && !(b.right <= a.left + 8));
        if (vert && b.top >= a.bottom - 8) { // вниз
          const x1 = ax + a.width / 2, y1 = ay + a.height, x2 = bx + b.width / 2, y2 = by, k = Math.max(20, (y2 - y1) * .5);
          d = `M${x1} ${y1} C${x1} ${y1 + k} ${x2} ${y2 - k} ${x2} ${y2}`;
        } else if (vert && b.bottom <= a.top + 8) { // вверх
          const x1 = ax + a.width / 2, y1 = ay, x2 = bx + b.width / 2, y2 = by + b.height, k = Math.max(20, (y1 - y2) * .5);
          d = `M${x1} ${y1} C${x1} ${y1 - k} ${x2} ${y2 + k} ${x2} ${y2}`;
        } else if (b.left >= a.right - 8) { // вправо
          const x1 = ax + a.width, y1 = ay + a.height / 2, x2 = bx, y2 = by + b.height / 2, k = Math.max(24, (x2 - x1) * .5);
          d = `M${x1} ${y1} C${x1 + k} ${y1} ${x2 - k} ${y2} ${x2} ${y2}`;
        } else if (b.right <= a.left + 8) { // влево
          const x1 = ax, y1 = ay + a.height / 2, x2 = bx + b.width, y2 = by + b.height / 2, k = Math.max(24, (x1 - x2) * .5);
          d = `M${x1} ${y1} C${x1 - k} ${y1} ${x2 + k} ${y2} ${x2} ${y2}`;
        } else if (b.top >= a.bottom - 8) { // вниз
          const x1 = ax + a.width / 2, y1 = ay + a.height, x2 = bx + b.width / 2, y2 = by, k = Math.max(20, (y2 - y1) * .5);
          d = `M${x1} ${y1} C${x1} ${y1 + k} ${x2} ${y2 - k} ${x2} ${y2}`;
        } else { // вверх
          const x1 = ax + a.width / 2, y1 = ay, x2 = bx + b.width / 2, y2 = by + b.height, k = Math.max(20, (y1 - y2) * .5);
          d = `M${x1} ${y1} C${x1} ${y1 - k} ${x2} ${y2 + k} ${x2} ${y2}`;
        }
        e.p.setAttribute('d', d);
      });
    };
    layout();
    let pulses = [];
    const startPulses = () => {
      pulses.forEach(t => t.kill()); $$('.pulse', svg).forEach(c => c.remove()); pulses = [];
      if (reduce) return;
      edges.forEach((e, i) => {
        if (e.mod === 'dash') return;
        const c = document.createElementNS(NS, 'circle'); c.classList.add('pulse'); if (e.bad) c.classList.add('bad'); c.setAttribute('r', 3); svg.appendChild(c);
        const len = e.p.getTotalLength(), dur = .7 + len / 240;
        const t = g.timeline({ repeat: -1, repeatDelay: .6 + (i % 3) * .35, delay: i * .27 });
        t.set(c, { opacity: 0 })
          .to(c, { motionPath: { path: e.p, align: e.p, alignOrigin: [.5, .5] }, duration: dur, ease: 'power1.inOut' }, 0)
          .to(c, { opacity: 1, duration: .18 }, 0)
          .to(c, { opacity: 0, duration: .25 }, dur - .25);
        pulses.push(t);
      });
    };
    let drawn = false;
    new ResizeObserver(() => { layout(); if (drawn) startPulses(); }).observe(box);
    if (reduce) return;
    const tl = g.timeline({ paused: true, onComplete: () => { drawn = true; startPulses(); } });
    tl.fromTo(edges.map(e => e.p), { drawSVG: '0%' }, { drawSVG: '100%', duration: 1, ease: 'power2.inOut', stagger: .08 });
    ScrollTrigger.create({ trigger: box, start: 'clamp(top 82%)', once: true, onEnter: () => tl.play() });
    // импульсы идут только когда схема на экране
    ScrollTrigger.create({ trigger: box, start: 'top bottom', end: 'bottom top',
      onToggle: s => pulses.forEach(t => s.isActive ? t.resume() : t.pause()) });
  };

  // ——— этапы работы: линия времени соединяет шаги
  const steps = ol => {
    const line = document.createElement('span'); line.className = 'st-line'; line.setAttribute('aria-hidden', 'true'); ol.prepend(line);
    const dots = $$(':scope > li', ol).map(li => { const d = document.createElement('span'); d.className = 'st-dot'; d.setAttribute('aria-hidden', 'true'); li.prepend(d); return d; });
    const vertical = () => getComputedStyle(ol).gridTemplateColumns.split(' ').length === 1;
    onView(ol, tl => {
      const v = vertical();
      tl.fromTo(line, { [v ? 'scaleY' : 'scaleX']: 0 }, { [v ? 'scaleY' : 'scaleX']: 1, transformOrigin: '0 0', duration: 1.6, ease: 'power2.inOut' })
        .fromTo(dots, { scale: 0 }, { scale: 1, duration: .5, ease: 'back.out(3)', stagger: .32 }, .1)
        .fromTo($$(':scope > li > :not(.st-dot)', ol), { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: .7, ease: 'power2.out', stagger: .05 }, .15);
      if (ol.dataset.timeline === 'travel') tl.add(() => travel(ol, dots), '>-.2');
    });
  };
  // точка-клиент проходит путь от этапа к этапу
  const travel = (ol, dots) => {
    const r = document.createElement('span'); r.className = 'st-runner'; r.setAttribute('aria-hidden', 'true'); ol.appendChild(r);
    let loop;
    const build = () => {
      if (loop) loop.kill();
      const o = ol.getBoundingClientRect(), xs = dots.map(d => d.getBoundingClientRect().left - o.left);
      loop = g.timeline({ repeat: -1, repeatDelay: .8 });
      loop.set(r, { x: xs[0], opacity: 0 }).to(r, { opacity: 1, duration: .3 });
      xs.slice(1).forEach(x => loop.to(r, { x, duration: .75, ease: 'power2.inOut' }, '+=.45'));
      loop.to(r, { opacity: 0, duration: .4 }, '+=.5');
    };
    build(); new ResizeObserver(build).observe(ol);
    ScrollTrigger.create({ trigger: ol, start: 'top bottom', end: 'bottom top', onToggle: s => s.isActive ? loop.resume() : loop.pause() });
  };

  // ————————————————————————————————— подключение
  const init = () => {
    $$('.steps, [data-timeline]').forEach(steps);
    $$('[data-wires]').forEach(wires);

    // полосы весов и индексов
    $$('.srcs, .report .card, [data-bars]').forEach(box => {
      const bars = $$('.w i, .tr i, [data-bar]', box); if (!bars.length) return;
      onView(box, tl => { grow(tl, bars, 0); countUp(tl, $$('.p, .v, [data-count]', box), 0, 1.3); });
    });
    // вертикальные столбцы
    $$('[data-cols]').forEach(box => onView(box, tl => grow(tl, $$('[data-col]', box), 0, 'y')));
    // линия графика
    $$('svg.spark, svg[data-draw]').forEach(svg => onView(svg, tl => {
      tl.fromTo($$('.ln, [data-line]', svg), { drawSVG: '0%' }, { drawSVG: '100%', duration: 1.8, ease: 'power2.inOut' })
        .fromTo($$('.ar, [data-area]', svg), { opacity: 0 }, { opacity: 1, duration: 1.2, ease: 'power1.out' }, .6)
        .fromTo($$('[data-pop]', svg), { scale: 0, transformOrigin: '50% 50%' }, { scale: 1, duration: .5, ease: 'back.out(3)', stagger: .1 }, 1.2);
    }));
    // кольца-показатели
    $$('[data-ring]').forEach(el => onView(el, tl => {
      tl.fromTo($$('.ring-v', el), { drawSVG: '0%' }, { drawSVG: (i, t) => '0% ' + t.dataset.v + '%', duration: 1.8, ease: 'expo.out' });
      countUp(tl, $$('[data-count]', el), 0, 1.8);
    }));
    // крупные числа
    $$('.stats, .kp, [data-counts]').forEach(box => onView(box, tl => countUp(tl, $$('b, [data-count]', box).filter(b => !b.closest('[data-ring]')))));
    // ответ нейросети печатается
    $$('[data-type]').forEach(el => onView(el, tl => {
      const box = el.closest('[data-type-box]') || el;
      const d = type(tl, el, .2);
      tl.fromTo($$('[data-after]', box), { opacity: 0, y: 6 }, { opacity: 1, y: 0, duration: .5, stagger: .12, ease: 'power2.out' }, .3 + d);
    }));
    // матрица сравнения: точки проявляются по столбцам, наш столбец — последним и ярче
    $$('[data-matrix]').forEach(box => onView(box, tl => {
      const cols = [...new Set($$('[data-c]', box).map(d => d.dataset.c))];
      cols.forEach((c, i) => tl.fromTo($$(`[data-c="${c}"]`, box), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: 'back.out(2.4)', stagger: .05 }, i * .22));
    }));
    // уровни зрелости: ступени растут
    $$('[data-stairs]').forEach(box => onView(box, tl => {
      const bars = $$('[data-step]', box), wide = bars[0] && bars[0].offsetHeight < 60;
      tl.fromTo(bars, { [wide ? 'scaleX' : 'scaleY']: 0 }, { [wide ? 'scaleX' : 'scaleY']: 1, transformOrigin: wide ? '0 50%' : '50% 100%', duration: 1.1, ease: 'expo.out', stagger: .14 });
    }));
    // говорящий аватар: волна голоса и смена языков
    $$('[data-voice]').forEach(box => {
      const bars = $$('.vb', box), ws = $$('[data-say]', box), chips = $$('[data-chip]', box);
      if (!bars.length || !ws.length) return;
      let k = 0;
      const chip = i => chips.forEach((c, j) => c.classList.toggle('on', j === i));
      chip(0);
      if (reduce) return;
      g.set(ws, { opacity: 0 }); g.set(ws[0], { opacity: 1 });
      const wave = g.to(bars, { scaleY: () => .12 + Math.random() * .88, duration: .16, ease: 'sine.inOut', stagger: { each: .01, repeat: -1, yoyo: true, repeatRefresh: true }, paused: true });
      const cycle = g.timeline({ repeat: -1, paused: true });
      ws.forEach((w, i) => cycle.add(() => {
        const prev = ws[k]; k = i; chip(i);
        if (prev !== w) g.to(prev, { opacity: 0, y: -16, duration: .45, ease: 'power2.in' });
        g.fromTo(w, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .7, ease: 'expo.out', delay: prev !== w ? .25 : 0 });
      }, i * 1.9));
      cycle.add(() => {}, ws.length * 1.9);
      ScrollTrigger.create({ trigger: box, start: 'top bottom', end: 'bottom top', onToggle: s => { s.isActive ? (wave.play(), cycle.play()) : (wave.pause(), cycle.pause()); } });
    });
    // SERP превращается в один ответ
    $$('[data-shift]').forEach(box => onView(box, tl => {
      tl.fromTo($$('.serp li', box), { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: .5, stagger: .08, ease: 'power2.out' })
        .to($$('.serp li.fade', box), { opacity: .28, filter: 'blur(1.2px)', duration: .8, stagger: .06, ease: 'power2.inOut' }, '+=.3')
        .fromTo($$('.serp li:not(.fade)', box), { backgroundColor: 'rgba(176,138,99,0)' }, { backgroundColor: 'rgba(176,138,99,.1)', duration: .6 }, '<');
      const d = type(tl, box.querySelector('.answer'), '>-.2');
      tl.fromTo($$('.cites span', box), { opacity: 0, y: 6 }, { opacity: 1, y: 0, duration: .5, stagger: .12, ease: 'power2.out' }, `>-${Math.max(0, d - .6)}`);
    }, 'clamp(top 76%)'));
    // нейро-ORM: пометки в ответе подсвечиваются после печати
    $$('[data-marks]').forEach(box => onView(box, tl => {
      const p = box.querySelector('[data-marks-text]'); if (!p) return;
      const d = type(tl, p, 1.4);
      tl.fromTo($$('mark', p), { backgroundSize: '0% 100%' }, { backgroundSize: '100% 100%', duration: .6, stagger: .3, ease: 'power2.out' }, 1.4 + d);
    }, 'clamp(top 78%)'));
    ScrollTrigger.refresh();
  };
  // после интро — чтобы первые экраны не сыграли под заставкой
  const go = () => requestAnimationFrame(init);
  if (document.documentElement.classList.contains('intro-on')) addEventListener('ss-intro-done', go, { once: true });
  else if (document.readyState === 'loading') addEventListener('DOMContentLoaded', go, { once: true }); else go();
})();
