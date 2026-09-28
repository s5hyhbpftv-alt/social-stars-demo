// Скриншоты блоков в середине и в конце анимации — в tools/qa/out/
// Запуск: node shots.mjs '{"voice/":[".vo-hero","#loss"]}'  (VW=390 — мобильный, T1/T2 — задержки в мс)
import { launch, BASE, OUT, skipIntro } from './lib.mjs';
import fs from 'fs'; import path from 'path';
fs.mkdirSync(OUT, { recursive: true });
const jobs = JSON.parse(process.argv[2] || '{"":["#why"]}'), W = +(process.env.VW || 1440);
const b = await launch();
const ctx = await b.newContext({ viewport: { width: W, height: W < 600 ? 844 : 900 } }); await skipIntro(ctx);
for (const [pg, sels] of Object.entries(jobs)) {
  const p = await ctx.newPage();
  await p.goto(`${BASE}/ai/${pg}`, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: '.hdr,.subnav{position:relative!important}' });
  for (const s of sels) {
    const el = await p.$(s); if (!el) { console.log('нет элемента', pg, s); continue; }
    await p.evaluate(e => e.scrollIntoView({ block: 'start' }), el);
    const n = `${W}_${pg.replace(/\//g, '') || 'index'}_${s.replace(/[^a-z0-9]/gi, '')}`;
    await p.waitForTimeout(+(process.env.T1 || 500)); await el.screenshot({ path: path.join(OUT, n + '_a.png') });
    await p.waitForTimeout(+(process.env.T2 || 3500)); await el.screenshot({ path: path.join(OUT, n + '_b.png') });
    console.log(n);
  }
  await p.close();
}
await b.close();
