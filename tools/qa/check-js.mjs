// Ошибки JS после прокрутки всей страницы — в обычном режиме и при «уменьшении движения»; интро не зависает.
import { launch, pages, BASE } from './lib.mjs';
const list = process.argv.slice(2).length ? process.argv.slice(2) : pages();
const b = await launch(); let bad = 0;
for (const rm of [false, true]) {
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: rm ? 'reduce' : 'no-preference' });
  for (const pg of list) {
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
    await p.goto(`${BASE}/ai/${pg}`, { waitUntil: 'networkidle' });
    await p.waitForTimeout(rm ? 1500 : 6000);
    for (let y = 0; y < 20000; y += 600) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(60); }
    await p.waitForTimeout(1500);
    const stuck = await p.evaluate(() => !!document.getElementById('intro') || document.documentElement.classList.contains('intro-on'));
    const ok = !errs.length && !stuck; if (!ok) bad++;
    console.log(rm ? 'reduce' : 'motion', (pg || 'index').padEnd(24), ok ? 'ok' : JSON.stringify({ errs: errs.slice(0, 3), stuck }));
    await p.close();
  }
  await ctx.close();
}
await b.close();
process.exit(bad ? 1 : 0);
