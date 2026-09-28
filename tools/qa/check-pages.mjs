// Вёрстка на десктопе и телефоне: горизонтальная прокрутка, один h1, дубли id, ошибки JS и 404, битые внутренние ссылки.
// Запуск: node check-pages.mjs [страница/ …]
import { launch, pages, BASE, ORIGIN, skipIntro } from './lib.mjs';
const list = process.argv.slice(2).length ? process.argv.slice(2) : pages();
const b = await launch();
const links = new Set(); let bad = 0;
for (const pg of list) for (const [n, w, h] of [['d', 1440, 900], ['m', 390, 844]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h } }); await skipIntro(ctx);
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await p.goto(`${BASE}/ai/${pg}`, { waitUntil: 'networkidle' });
  await p.waitForTimeout(600);
  const r = await p.evaluate(() => {
    const W = document.documentElement.clientWidth, o = [];
    document.querySelectorAll('body *').forEach(e => {
      const rc = e.getBoundingClientRect();
      if (rc.right > W + 1 && rc.width > 0) {
        let a = e.parentElement, clipped = false;
        while (a && a !== document.body) { if (getComputedStyle(a).overflowX !== 'visible' && a.getBoundingClientRect().right <= W + 1) { clipped = true; break; } a = a.parentElement; }
        if (!clipped) o.push(e.tagName + '.' + (e.className.baseVal ?? e.className));
      }
    });
    return { sw: document.documentElement.scrollWidth, o: o.slice(0, 5), h1: document.querySelectorAll('h1').length, ids: [...document.querySelectorAll('[id]')].map(e => e.id).filter((v, i, a) => a.indexOf(v) !== i) };
  });
  (await p.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')))).forEach(x => links.add(x));
  const ok = !errs.length && !r.o.length && r.h1 === 1 && !r.ids.length;
  if (!ok) bad++;
  console.log((pg || 'index').padEnd(24), n, ok ? 'ok' : JSON.stringify({ errs, overflow: r.o, h1: r.h1, dupIds: r.ids }));
  await ctx.close();
}
const p = await b.newPage(); const broken = [];
for (const h of links) { if (!h.startsWith('/social-stars-demo/')) continue; const r = await p.request.get(ORIGIN + h.split('#')[0]); if (r.status() >= 400) broken.push(r.status() + ' ' + h); }
console.log('внутренних ссылок', [...links].filter(h => h.startsWith('/')).length, '| битых', broken.length ? broken : 0, '| страниц с проблемами', bad);
await b.close();
process.exit(bad || broken.length ? 1 : 0);
