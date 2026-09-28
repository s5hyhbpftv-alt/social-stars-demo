// Выгрузка баннеров кампании в PNG нативного размера: ai/<направление>/campaign/creatives/<id>.png
// Запуск: node export-banners.mjs ugc marketplace voice …  (без аргументов — все кампании)
import { launch, BASE, ROOT, skipIntro } from './lib.mjs';
import fs from 'fs'; import path from 'path';
const all = fs.readdirSync(path.join(ROOT, 'ai')).filter(d => fs.existsSync(path.join(ROOT, 'ai', d, 'campaign/index.html')));
const slugs = process.argv.slice(2).length ? process.argv.slice(2) : all;
const b = await launch();
for (const slug of slugs) {
  const dir = path.join(ROOT, 'ai', slug, 'campaign/creatives'); fs.mkdirSync(dir, { recursive: true });
  const ctx = await b.newContext({ viewport: { width: 2000, height: 2200 }, deviceScaleFactor: 1 }); await skipIntro(ctx);
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`${BASE}/ai/${slug}/campaign/?export`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : i.decode().catch(() => 0))); });
  await p.waitForTimeout(800);
  for (const f of await p.$$('#creatives [data-bn]')) {
    const id = await f.getAttribute('data-bn'), bn = await f.$('.bn');
    await bn.screenshot({ path: path.join(dir, id + '.png') });
    console.log(slug.padEnd(12), id, await bn.evaluate(e => e.offsetWidth + '×' + e.offsetHeight));
  }
  if (errs.length) console.log('ошибки', slug, errs);
  await ctx.close();
}
await b.close();
