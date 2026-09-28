// Общие настройки для скриптов проверки.
// Сайт открывается по адресу http://localhost:8123/social-stars-demo/ — запустите tools/serve.sh.
// Переменные окружения: SS_BASE — другой адрес сайта, PW_CHROMIUM — свой путь к Chromium.
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export const BASE = (process.env.SS_BASE || 'http://localhost:8123/social-stars-demo').replace(/\/$/, '');
export const ORIGIN = new URL(BASE).origin;
export const OUT = path.join(ROOT, 'tools/qa/out');

// свой Chromium: PW_CHROMIUM, иначе предустановленный в облаке Claude Code, иначе браузер Playwright
const chromiumPath = () => {
  if (process.env.PW_CHROMIUM) return process.env.PW_CHROMIUM;
  const base = '/opt/pw-browsers';
  if (!fs.existsSync(base)) return undefined;
  const dir = fs.readdirSync(base).filter(d => /^chromium-\d+$/.test(d)).sort().pop();
  const exe = dir && path.join(base, dir, 'chrome-linux/chrome');
  return exe && fs.existsSync(exe) ? exe : undefined;
};
export const launch = () => { const p = chromiumPath(); return chromium.launch(p ? { executablePath: p } : {}); };

// все страницы направления: ai/**/index.html → 'sites/', 'ugc/campaign/' …
export const pages = () => {
  const out = [];
  const walk = d => fs.readdirSync(d, { withFileTypes: true }).forEach(e => {
    const p = path.join(d, e.name);
    if (e.isDirectory() && !['img', 'video', 'vendor', 'creatives'].includes(e.name)) walk(p);
    else if (e.name === 'index.html') out.push(path.relative(path.join(ROOT, 'ai'), d).replace(/\\/g, '/'));
  });
  walk(path.join(ROOT, 'ai'));
  return out.map(p => (p ? p + '/' : '')).sort();
};

// пропустить интро в браузерном контексте
export const skipIntro = ctx => ctx.addInitScript(() => { try { sessionStorage.setItem('ss-intro', '1'); } catch (e) {} });
