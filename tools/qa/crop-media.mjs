// Нарезка кадров для макетов: вертикаль 9:19 (телефоны UGC) или 3:4 (карточки маркетплейсов) с фокусом на лице, в WebP.
// Запуск: node crop-media.mjs <исходник> <результат.webp> <9x19|3x4|16x9> [фокус по горизонтали 0…1] [ширина]
// Пример: node crop-media.mjs ../../export/maria.jpg ../../ai/img/team-maria.webp 4x5 .5 520
import { launch } from './lib.mjs';
import fs from 'fs'; import path from 'path';
const [src, out, ratio = '9x19', fx = '.5', width = '420'] = process.argv.slice(2);
if (!src || !out) { console.log('node crop-media.mjs <src> <out.webp> <9x19|3x4|4x5|16x9> [fx] [width]'); process.exit(1); }
const [RW, RH] = ratio.split('x').map(Number);
const b = await launch(); const p = await b.newPage();
const data = 'data:image/' + (path.extname(src).slice(1).replace('jpg', 'jpeg') || 'jpeg') + ';base64,' + fs.readFileSync(src).toString('base64');
const res = await p.evaluate(async ([data, fx, w, RW, RH]) => {
  const img = new Image(); img.src = data; await img.decode();
  const W = img.naturalWidth, H = img.naturalHeight;
  let cw = Math.round(H * RW / RH), ch = H;
  if (cw > W) { cw = W; ch = Math.round(W * RH / RW); }
  const x = Math.max(0, Math.min(W - cw, Math.round(W * fx - cw / 2))), y = Math.max(0, Math.round((H - ch) * .2));
  const c = document.createElement('canvas'); c.width = w; c.height = Math.round(w * RH / RW);
  c.getContext('2d').drawImage(img, x, y, cw, ch, 0, 0, c.width, c.height);
  return [c.toDataURL('image/webp', .8), `${W}×${H} → ${c.width}×${c.height}`];
}, [data, +fx, +width, RW, RH]);
fs.writeFileSync(out, Buffer.from(res[0].split(',')[1], 'base64'));
console.log(out, res[1], Math.round(fs.statSync(out).size / 1024) + ' КБ');
await b.close();
