// Превью ссылок (og:image) 1200×630 для каждой страницы направления → ai/og/<страница>.jpg
// Заголовок и раздел берутся со страницы, справа — кадр героини этой страницы.
// Запуск (сайт должен быть открыт локально): node og.mjs            — все страницы
//                                              node og.mjs agents ugc — выборочно
import { launch, BASE, ORIGIN, ROOT } from './lib.mjs';
import fs from 'fs'; import path from 'path';

const IMG = `${BASE}/ai/img/`;
// страница → кадры справа (один — крупно; три — веером) и метка на кадре
const MEDIA = {
  index: [['ugc/type-brunette.webp', 'ugc/cast-front.webp', 'ugc/type-dark.webp'], 'ИИ‑модели'],
  agents: [['ugc/v-agents-walk.webp'], 'ИИ‑модель'],
  avatars: [['ugc/cast-front.webp'], 'ИИ‑модель'],
  cases: [['forum-stage.webp'], ''],
  content: [['ugc/v-reel-pink.webp'], 'ИИ‑модель'],
  dubbing: [['../og/src-bee.webp'], 'ИИ‑модели'],
  'growth-os': [['ugc/v-salon-flip.webp', 'ugc/type-brunette.webp', 'ugc/type-platinum.webp'], 'ИИ‑модели'],
  knowledge: [['ugc/know-curls.webp'], 'ИИ‑модели'],
  marketplace: [['ugc/look-red.webp'], 'ИИ‑модель'],
  'neuro-orm': [['ugc/v-orm-loft.webp'], 'ИИ‑модель'],
  procurement: [['ugc/v-proc-duo.webp'], 'ИИ‑модели'],
  'seo-geo': [['ugc/seo-brunette.webp'], 'ИИ‑модель'],
  sites: [['ugc/type-noir.webp'], 'ИИ‑модель'],
  trainer: [['ugc/mb-salon.webp'], 'ИИ‑клиент'],
  transformation: [['mniid-talk.webp'], ''],
  ugc: [['ugc/gb-twirl.webp'], 'ИИ‑аватар'],
  voice: [['ugc/v-voice-roots.webp'], 'ИИ‑модель'],
};

const sprite = fs.readFileSync(path.join(ROOT, 'tools/partials/brand-sprite.html'), 'utf8');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const tpl = ({ eyebrow, title, imgs, tag }) => `<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="${BASE}/ai/ai.css">
<style>
  html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:#f3f5f8}
  .og{position:relative;width:1200px;height:630px;font-family:var(--font);color:var(--ink)}
  .sky{position:absolute;inset:0}
  .txt{position:absolute;left:72px;top:64px;bottom:60px;width:${imgs.length > 1 ? 500 : 640}px;display:flex;flex-direction:column}
  .brand{pointer-events:none;transform:scale(1.4);transform-origin:left top}
  .brand-star{width:48px;height:44px}
  .eb{margin-top:auto;font-size:24px;color:var(--bronze-2);letter-spacing:-.005em}
  h1{margin:14px 0 0;font-weight:300;font-size:${imgs.length > 1 ? (title.length > 40 ? 46 : 58) : title.length > 60 ? 50 : title.length > 40 ? 58 : 66}px;line-height:1.04;letter-spacing:-.035em}
  .foot{margin-top:30px;font-size:19px;color:var(--slate)}
  .ph{position:absolute;top:44px;width:330px;height:542px;border-radius:30px;overflow:hidden;background:#e9edf2;box-shadow:0 40px 80px -40px rgba(27,33,48,.55)}
  .ph img{width:100%;height:100%;object-fit:cover;display:block}
  .ph .tag{position:absolute;left:14px;top:14px;padding:6px 12px;border-radius:999px;background:rgba(27,33,48,.72);color:#fff;font-size:15px}
  .one .ph{right:72px}
  .fan .ph{width:260px;height:430px;top:100px}
  .fan .ph:nth-child(1){right:330px;transform:rotate(-7deg)}
  .fan .ph:nth-child(2){right:190px;top:70px;z-index:2}
  .fan .ph:nth-child(3){right:52px;transform:rotate(7deg)}
</style></head><body>${sprite}
<div class="og">
  <svg class="sky" viewBox="0 0 1200 630" aria-hidden="true"><g fill="none" stroke="#d9dee6" stroke-width="1.2">
    <path d="M700 40 L760 120 L720 210"/></g>
    <g fill="#c9d0da"><circle cx="700" cy="40" r="2.5"/><circle cx="760" cy="120" r="3.5"/><circle cx="720" cy="210" r="2.5"/></g></svg>
  <div class="txt">
    <span class="brand"><svg class="brand-star" viewBox="0 0 100 91.2"><use href="#ss-star"/></svg><span class="brand-word"><svg class="bw-social" viewBox="0 0 66.97 11.77"><use href="#ss-social"/></svg><svg class="bw-stars" viewBox="0 0 61.26 11.78"><use href="#ss-stars"/></svg></span><span class="brand-sep"></span><svg class="brand-ai" viewBox="0 0 15.95 11.78"><use href="#ss-ai"/></svg></span>
    <div class="eb">${esc(eyebrow)}</div>
    <h1>${esc(title)}</h1>
    <div class="foot">Бесплатный AI‑аудит за 48 часов</div>
  </div>
  <div class="${imgs.length > 1 ? 'fan' : 'one'}">${imgs.map(i => `<div class="ph"><img src="${IMG}${i}">${tag && imgs.length === 1 ? `<span class="tag">${tag}</span>` : ''}</div>`).join('')}</div>
</div></body></html>`;

const only = process.argv.slice(2);
const slugs = Object.keys(MEDIA).filter(s => !only.length || only.includes(s));
fs.mkdirSync(path.join(ROOT, 'ai/og'), { recursive: true });
const b = await launch();
const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const slug of slugs) {
  const html = fs.readFileSync(path.join(ROOT, 'ai', slug === 'index' ? '' : slug, 'index.html'), 'utf8');
  const txt = s => s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const title = txt((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [, ''])[1]);
  const crumb = txt((html.match(/<span aria-current="page">([\s\S]*?)<\/span>/) || [, 'Social Stars AI'])[1]);
  const [imgs, tag] = MEDIA[slug];
  await p.goto(`${ORIGIN}/social-stars-demo/ai/`, { waitUntil: 'domcontentloaded' });
  await p.setContent(tpl({ eyebrow: slug === 'index' ? 'Social Stars AI' : crumb, title, imgs, tag }), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const out = path.join(ROOT, 'ai/og', `${slug}.jpg`);
  await p.screenshot({ path: out, type: 'jpeg', quality: 86 });
  console.log(slug.padEnd(16), Math.round(fs.statSync(out).size / 1024) + ' КБ', '—', title);
}
await b.close();
