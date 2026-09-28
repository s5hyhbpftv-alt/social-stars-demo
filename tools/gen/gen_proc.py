import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import *

CHIP = 'Ассистент закупок'
# поставщик, цена за шт, доставка ₽, отсрочка дней, срок дней, итог, флаг
KP = [('А «Картон‑Плюс»', 41.20, 38000, 0, 5, 862000, ''),
      ('Б «ТараПром»', 42.50, 0, 30, 7, 850000, ''),
      ('В «ГофроЛайн»', 39.80, 64000, 15, 12, 860000, 'штраф 30% за отмену')]
f2 = lambda x: f'{x:.2f}'.replace('.', ',')
m = lambda x: money(x) if x else 'включена'


def kp(best=1, note=True, compact=False):
    rows = ''
    for i, (n, p, d, t, s, tot, fl) in enumerate(KP):
        tag = '<span class="tag">Рекомендую</span>' if i == best else ''
        sub = tag or (f'<span class="flag">{fl}</span>' if fl else '')
        rows += (f'<tr class="{"best" if i == best else ""}"><th scope="row">{n}{("<br>" + sub) if sub else ""}</th><td class="num">{f2(p)} ₽</td>'
                 + ('' if compact else f'<td class="num">{m(d)}</td>') + f'<td class="num">{t or "нет"}{" дн." if t else ""}</td>'
                 + ('' if compact else f'<td class="num">{s} дн.</td>') + f'<td class="num"><b>{money(tot)}</b></td></tr>')
    head = '<tr><th scope="col">Поставщик</th><th scope="col" class="num">Цена за шт.</th>' + ('' if compact else '<th scope="col" class="num">Доставка</th>') + '<th scope="col" class="num">Отсрочка</th>' + ('' if compact else '<th scope="col" class="num">Срок</th>') + '<th scope="col" class="num">Итог</th></tr>'
    nt = (f'<p class="offer-note">{icon("sparkle")}<span><b>Рекомендую Б:</b> итог на 12 000 ₽ ниже, чем у А, и отсрочка 30 дней. У В в договоре штраф 30% за отмену заказа, п. 7.2.</span></p>') if note else ''
    return (f'<div class="offer"><div class="offer-in"><h4>Сравнение КП<span>Гофрокороб 600×400×400, 20 000 шт.</span></h4>'
            f'<table class="offer-t"><thead>{head}</thead><tbody>{rows}</tbody></table>{nt}</div></div>')


hero_vis = f'<div class="pr-hero" data-kp>{kp()}</div>'

flow = f'''<div class="pflow" data-wires="r>ai:h ai>h:h h>c:h">
        <div class="hnode" data-n="r">{icon("inbox")}<b>Заявка отдела</b><span>«нужно 20 000 коробок к 1 июня»</span></div>
        <div class="hnode hub" data-n="ai">{icon("assistant")}<b>ИИ‑ассистент</b><span>запрашивает КП у 5 поставщиков, сравнивает, читает договоры</span></div>
        <div class="hnode" data-n="h">{icon("user")}<b>Закупщик</b><span>видит сравнение и риски, принимает решение</span></div>
        <div class="hnode" data-n="c">{icon("server")}<b>Заказ в 1С</b><span>документы и сроки — автоматически</span></div>
      </div>'''

weights = '''<div class="wts" data-wts>
        <div class="wts-in">
          <div class="rng"><label>Важность итоговой цены <output>60%</output></label><input type="range" min="0" max="100" value="60" data-k="cost" /></div>
          <div class="rng"><label>Важность отсрочки <output>25%</output></label><input type="range" min="0" max="100" value="25" data-k="terms" /></div>
          <div class="rng"><label>Важность срока поставки <output>15%</output></label><input type="range" min="0" max="100" value="15" data-k="speed" /></div>
        </div>
        <div class="wts-out">
          <small>Оценка предложений</small>
          <div class="ws"><span>А «Картон‑Плюс»</span><span class="tr"><i></i></span><b></b></div>
          <div class="ws"><span>Б «ТараПром»</span><span class="tr"><i></i></span><b></b></div>
          <div class="ws"><span>В «ГофроЛайн»</span><span class="tr"><i></i></span><b></b></div>
          <p class="win">Лучшее предложение: <b></b></p>
        </div>
      </div>
      <p class="note">Настройте, что важнее для вас, — ассистент пересчитает рейтинг. Цифры поставщиков условные.</p>'''

risks = f'''<div class="risk">
        <div class="doc">
          <p class="doc-h">{icon("doc")}Договор поставки, ГофроЛайн.pdf</p>
          <p><span class="n">3.4</span> Цена товара <mark class="md">может быть изменена поставщиком в одностороннем порядке</mark> при росте стоимости сырья.</p>
          <p><span class="n">4.1</span> Покупатель вносит <mark class="hi">предоплату в размере 100%</mark> стоимости партии.</p>
          <p><span class="n">7.2</span> При отмене заказа покупатель уплачивает <mark class="hi">штраф в размере 30%</mark> стоимости заказа.</p>
          <p><span class="n">9.1</span> Договор <mark class="md">продлевается на год автоматически</mark>, если стороны не заявили иное.</p>
        </div>
        <ol class="flags">
          <li class="hi"><b>Штраф 30% за отмену</b><span>п. 7.2 — предложить 5% или отменить без штрафа за 10 дней</span></li>
          <li class="hi"><b>Предоплата 100%</b><span>п. 4.1 — ваш стандарт: 30% предоплаты</span></li>
          <li class="md"><b>Цена меняется без согласования</b><span>п. 3.4 — зафиксировать цену на партию</span></li>
          <li class="md"><b>Автопролонгация</b><span>п. 9.1 — уведомление за 30 дней</span></li>
        </ol>
      </div>'''

world = '''<div class="world" data-counts>
        <div><b data-count>3%</b><span>средняя выгода на переговорах, которые провёл ИИ‑агент</span></div>
        <div><b data-count>+35</b><span>дней к отсрочке платежа в среднем</span></div>
        <div><b data-count>60%</b><span>поставщиков принимают предложение агента</span></div>
      </div>
      <p class="note">Walmart и Pactum AI — результаты мирового лидера, не наши. Источник: Pactum, 2026.</p>'''

main = '<main id="main">\n' + hero('ИИ‑ассистент закупок', 'Три КП к обеду',
    'ИИ‑ассистент запрашивает коммерческие предложения, сравнивает их с учётом доставки и отсрочки, читает договоры и находит риски. Решение — за закупщиком.',
    [('btn-primary', '#lead', 'Пилот на одной категории', CHIP), ('btn-line', '#weights', 'Сравнить КП самому', '')], hero_vis,
    [('Сравнение КП', 'за минуты, а не дни'), ('Договоры', 'проверка каждого пункта'), ('Данные', 'в 1С и в России')], 'pr-hero-s') + '\n\n' + \
    subnav([('flow', 'Процесс'), ('case', 'На практике'), ('weights', 'Сравнение'), ('risks', 'Договоры'), ('world', 'Мировой опыт'), ('week', 'Этапы'), ('pricing', 'Тарифы'), ('faq', 'Вопросы')], 'Пилот', CHIP) + '\n\n' + \
    section('flow', flow, head='Рутину — ассистенту, решение — человеку') + '\n\n' + \
    demo('case', 'proc-duo.mp4', 'Флаконы, дозаторы, сырьё — одна сводка', 'Пример: производство косметики. ИИ собирает предложения поставщиков флаконов и сырья, сравнивает цену, сроки и надёжность и готовит сводку. Решение принимает закупщик.', ['Предложения поставщиков в одной таблице', 'Проверка сроков и надёжности', 'Решение — за человеком'], label='Две ИИ‑модели в лофте') + '\n\n' + \
    section('weights', weights, cls='band', head='Самое выгодное — не всегда самое дешёвое', lead='Итог с доставкой, отсрочка и сроки — в одной оценке.', split=True) + '\n\n' + \
    section('risks', risks, head='Ассистент читает договор до конца', lead='И сравнивает каждый пункт с вашими правилами закупок.', split=True) + '\n\n' + \
    section('world', world, cls='band', head='Как это работает у лидеров') + '\n\n' + \
    section('week', steps([('Неделя 1', 'Аудит закупок', 'Категории, «хвост» мелких закупок, ваши правила и шаблоны.'),
                           ('Недели 2–3', 'Подключение', '1С, почта закупщиков, реестр поставщиков.'),
                           ('Недели 4–6', 'Пилот', 'Одна категория: сравниваем экономию и сроки с ручной работой.'),
                           ('Дальше', 'Масштаб', 'Новые категории и согласование в вашей системе.')]), head='Запуск за полтора месяца') + '\n\n' + \
    section('honest', ethics([('user', 'Решает человек', 'Ассистент готовит сравнение и черновики, договор подписывает закупщик.'),
                              ('mail', 'Прозрачно для поставщиков', 'Письма с запросами подписаны: поставщик знает, что пишет ассистент компании.'),
                              ('shield', 'Госзакупки', 'По 44‑ФЗ и 223‑ФЗ помогаем готовить документы, процедуру ведёт закупщик.'),
                              ('lock', 'Данные в России', 'Цены и договоры хранятся на серверах в РФ или в вашем контуре.')]), cls='band', head='Правила') + '\n\n' + \
    section('pricing', plans([
        dict(name='Старт', price='250 000 ₽', small='запуск + 29 000 ₽ в месяц', text='Одна категория закупок.', list=['Сравнение КП', 'Проверка договоров', 'Выгрузка в 1С', 'Отчёт об экономии'], cta='Выбрать «Старт»'),
        dict(name='Отдел', price='490 000 ₽', small='запуск + 59 000 ₽ в месяц', text='Все категории отдела.', list=['Запросы КП поставщикам', 'Ваши правила закупок', 'Согласование в 1С', 'Аналитика по поставщикам'], cta='Выбрать «Отдел»', main=True, badge='Чаще выбирают'),
        dict(name='Холдинг', price='от 1,2 млн ₽', small='проект', text='Несколько юрлиц и складов.', list=['Единый реестр поставщиков', 'Развёртывание в вашем контуре', 'Интеграция с ERP', 'Выделенная команда'], cta='Обсудить проект')], CHIP),
        head='Тарифы', lead='Пилот на одной категории — до основного договора.', split=True) + '\n\n' + \
    section('faq', faq([
        ('Ассистент сам заключает сделки?', 'Нет. Он собирает предложения, сравнивает их и готовит черновики писем и замечаний к договору. Решение и подпись — за закупщиком.'),
        ('Как ассистент запрашивает КП?', 'Отправляет письма поставщикам из вашего реестра по шаблону, собирает ответы и раскладывает их в сравнение. Поставщик видит, что пишет ассистент компании.'),
        ('Подходит ли для госзакупок?', 'Для 44‑ФЗ и 223‑ФЗ ассистент помогает готовить документацию и анализировать заявки, но процедуру ведёт закупщик — как требует закон.'),
        ('С какими системами работает?', '1С: Управление торговлей и ERP, почта, электронные площадки, ваши реестры поставщиков в таблицах.'),
        ('Сколько можно сэкономить?', 'Зависит от категорий и того, как закупки устроены сейчас. На пилоте сравниваем цены и сроки с ручной работой на одной категории — и считаем эффект в рублях.')])
        + '\n      ' + next_link('seo-geo', 'rank', 'SEO и GEO'), head='Вопросы') + '\n' + \
    f'<script type="application/json" id="kp-data">{json.dumps([[n, tot, t, s] for n, p, d, t, s, tot, fl in KP], ensure_ascii=False)}</script>\n'

style = SERVICE_CSS + '''    .pr-hero{max-width:600px;justify-self:end;width:100%}
    .pflow{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(28px,4vw,64px);align-items:center}
    .hnode{display:grid;gap:4px;padding:18px 20px;border-radius:var(--r-md);background:var(--white);border:1px solid var(--mist)}
    .hnode .ic{color:var(--bronze-2);margin-bottom:6px}
    .hnode b{font-weight:500;font-size:17px}
    .hnode span{color:var(--slate);font-size:14.5px}
    .hnode.hub{background:var(--ink);border-color:var(--ink);color:#fff}
    .hnode.hub span{color:#a9b1c0}.hnode.hub .ic{color:var(--bronze)}
    .wts{display:grid;grid-template-columns:6fr 5fr;gap:24px}
    .wts-in,.wts-out{background:var(--white);border:1px solid var(--mist);border-radius:var(--r-lg);padding:clamp(24px,3vw,36px)}
    .rng{display:grid;gap:10px;margin-bottom:26px}.rng:last-child{margin-bottom:0}
    .rng label{display:flex;justify-content:space-between;gap:12px;font-size:15.5px}
    .rng output{font-weight:500;font-variant-numeric:tabular-nums}
    .rng input{width:100%;accent-color:var(--ink);height:24px}
    .wts-out{display:grid;gap:16px;align-content:start}
    .wts-out small{font-size:14px;color:var(--slate)}
    .ws{display:grid;grid-template-columns:150px 1fr 40px;gap:12px;align-items:center;font-size:15px}
    .ws .tr{height:12px;border-radius:6px;background:var(--porcelain-2);overflow:hidden}
    .ws .tr i{display:block;height:100%;border-radius:6px;background:var(--mist-2);transition:width .4s var(--ease),background .3s}
    .ws.top .tr i{background:var(--bronze)}
    .ws b{font-weight:500;text-align:right;font-variant-numeric:tabular-nums}
    .win{padding-top:14px;border-top:1px solid var(--mist)}
    .win b{font-weight:500}
    .risk{display:grid;grid-template-columns:7fr 5fr;gap:clamp(24px,4vw,56px);align-items:start}
    .doc{background:var(--white);border:1px solid var(--mist);border-radius:var(--r-lg);padding:clamp(24px,3vw,36px);display:grid;gap:14px;font-size:15.5px;line-height:1.6}
    .doc-h{display:flex;align-items:center;gap:10px;font-weight:500;padding-bottom:12px;border-bottom:1px solid var(--mist)}
    .doc-h .ic{color:var(--slate)}
    .doc .n{display:inline-block;min-width:34px;color:var(--slate);font-variant-numeric:tabular-nums}
    .doc mark{color:inherit;padding:1px 3px;border-radius:3px}
    .doc mark.hi{background:rgba(194,87,75,.16)}
    .doc mark.md{background:rgba(176,138,99,.2)}
    .flags{list-style:none;display:grid;gap:12px}
    .flags li{display:grid;gap:4px;padding:16px 18px;border-radius:var(--r-md);background:var(--white);border:1px solid var(--mist);border-left:3px solid var(--bronze)}
    .flags li.hi{border-left-color:var(--sky-bad,#c2574b)}
    .flags b{font-weight:500}
    .flags span{color:var(--slate);font-size:14.5px}
    .world{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
    .world b{display:block;font-size:clamp(44px,5vw,72px);font-weight:200;letter-spacing:-.05em;line-height:1}
    .world span{display:block;margin-top:12px;color:var(--ink-2);max-width:22em}
    @media (max-width:1024px){ .pr-hero{justify-self:start} .pflow{grid-template-columns:1fr 1fr;gap:16px} .pflow .wires{display:none} .wts,.risk{grid-template-columns:1fr} }
    @media (max-width:600px){ .pflow{grid-template-columns:1fr} .world{grid-template-columns:1fr;gap:28px} .ws{grid-template-columns:1fr 40px;gap:6px 12px} .ws .tr{grid-column:1 / -1;grid-row:2} .pr-hero .offer-t{font-size:11px} }
'''

script = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  const g = window.gsap, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // первый экран: строки КП появляются, ассистент выбирает лучшее
  const hero = document.querySelector('[data-kp]');
  if (hero && g && !reduce) {
    const rows = hero.querySelectorAll('tbody tr'), best = hero.querySelector('tr.best'), tag = hero.querySelector('.tag'), flag = hero.querySelector('.flag'), note = hero.querySelector('.kp-note');
    const tl = g.timeline({ repeat: -1, repeatDelay: 4 });
    tl.set(rows, { opacity: 0, x: -8 }).set([tag, note, flag], { opacity: 0 }).add(() => best.classList.remove('best'))
      .to(rows, { opacity: 1, x: 0, duration: .45, stagger: .35, ease: 'power2.out' })
      .to(flag, { opacity: 1, duration: .4 }, '+=.3')
      .add(() => best.classList.add('best'), '+=.3').to(tag, { opacity: 1, duration: .3 })
      .fromTo(note, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: .5, ease: 'power2.out' }, '+=.2');
  }
  // веса критериев
  const data = JSON.parse(document.getElementById('kp-data').textContent), box = document.querySelector('[data-wts]');
  if (box) {
    const inp = [...box.querySelectorAll('input')], rows = [...box.querySelectorAll('.ws')], win = box.querySelector('.win b');
    const cost = data.map(d => d[1]), terms = data.map(d => d[2]), speed = data.map(d => d[3]);
    const norm = (arr, better) => { const mn = Math.min(...arr), mx = Math.max(...arr); return arr.map(v => mx === mn ? 1 : better === 'low' ? (mx - v) / (mx - mn) : (v - mn) / (mx - mn)); };
    const nc = norm(cost, 'low'), nt = norm(terms, 'high'), ns = norm(speed, 'low');
    const upd = () => {
      const w = Object.fromEntries(inp.map(i => [i.dataset.k, +i.value])), sum = (w.cost + w.terms + w.speed) || 1;
      inp.forEach(i => { i.closest('.rng').querySelector('output').textContent = Math.round(+i.value / sum * 100) + '%'; });
      const sc = data.map((_, k) => Math.round(100 * (w.cost * nc[k] + w.terms * nt[k] + w.speed * ns[k]) / sum));
      const top = sc.indexOf(Math.max(...sc));
      rows.forEach((r, k) => { r.querySelector('i').style.width = Math.max(4, sc[k]) + '%'; r.querySelector('b').textContent = sc[k]; r.classList.toggle('top', k === top); });
      win.textContent = data[top][0];
    };
    inp.forEach(i => i.addEventListener('input', upd)); upd();
  }
});
</script>'''

build('ai/ugc/index.html', 'ai/procurement/index.html',
      title='ИИ-ассистент закупок: сравнение КП и проверка договоров — Social Stars AI',
      desc='ИИ-ассистент запрашивает коммерческие предложения, сравнивает их с учётом доставки и отсрочки, проверяет договоры на риски и выгружает заказ в 1С. Решение за закупщиком. Запуск от 250 000 ₽.',
      path='/ai/procurement/', og_title='Три КП к обеду — ИИ-ассистент закупок', og_desc='Сравнение предложений и проверка договоров — за минуты.',
      ld=ld_service('ИИ-ассистент закупок', '/ai/procurement/', 250000), style=style, main=main, script=script, service=CHIP)

# ——— кампания
L = lambda: legal()
risk_card = '''<div class="rk"><p class="rk-h">Договор поставки, ГофроЛайн.pdf</p><p><span>7.2</span> При отмене заказа покупатель уплачивает <mark>штраф в размере 30%</mark> стоимости заказа.</p><p class="rk-ai">ИИ‑ассистент: риск высокий. Предложите 5% или отмену без штрафа за 10 дней.</p></div>'''
banners = [
 ('square-lunch', 1080, 1080, 'Квадрат 1080×1080 — Telegram Ads, VK Реклама',
  f'''<div class="bn b-sq ink">{LOGO}<h3>Три КП<br>к обеду</h3>
      <p class="bn-lead">ИИ‑ассистент соберёт и сравнит предложения поставщиков.</p>
      <span class="bn-cta">Пилот на одной категории</span>
      <div class="pv">{kp(note=False, compact=True)}</div>{L()}</div>'''),
 ('square-penalty', 1080, 1080, 'Квадрат 1080×1080 — финансовые директора и юристы',
  f'''<div class="bn b-sq2">{LOGO}<h3>Штраф 30% за отмену?<br>ИИ заметил</h3>
      <div class="pv2">{risk_card}</div>
      <p class="bn-lead">Ассистент читает каждый договор до конца и сверяет с вашими правилами.</p>
      <span class="bn-cta">Пилот</span>{L()}</div>'''),
 ('story-compare', 1080, 1920, 'Вертикаль 1080×1920 — истории и клипы',
  f'''<div class="bn b-st ink">{LOGO}<h3>ИИ сравнит КП.<br>Вы примете<br>решение</h3>
      <div class="pv3">{kp(compact=True)}</div>
      <span class="bn-cta">Пилот на одной категории</span>{L()}</div>'''),
 ('wide-tail', 1200, 628, 'Горизонталь 1200×628 — Яндекс РСЯ, VK Реклама',
  f'''<div class="bn b-wd">{LOGO}<h3>Экономия прячется<br>в мелких закупках</h3>
      <p class="bn-lead">ИИ‑ассистент сравнивает КП и находит риски в договорах.</p>
      <span class="bn-cta">Пилот</span>
      <div class="pv4">{kp(note=False, compact=True)}</div>{L()}</div>'''),
]
banner_css = '''    .b-sq h3{font-size:128px}
    .b-sq .bn-lead{top:520px;width:430px}
    .b-sq .bn-cta{top:740px;font-size:26px}
    .b-sq .pv{position:absolute;right:44px;top:250px;width:470px}
    .b-sq2 h3{font-size:74px;width:980px}
    .b-sq2 .pv2{position:absolute;left:64px;top:390px;width:600px}
    .b-sq2 .bn-lead{left:700px;top:400px;width:330px;font-size:30px}
    .b-sq2 .bn-cta{left:700px;top:720px}
    .rk{background:#fff;border:1px solid var(--mist);border-radius:28px;padding:36px;display:grid;gap:20px;font-size:28px;line-height:1.5;color:var(--ink);box-shadow:0 40px 70px -46px rgba(17,21,31,.45)}
    .rk-h{font-weight:500;font-size:24px;color:var(--slate);padding-bottom:16px;border-bottom:1px solid var(--mist)}
    .rk span{color:var(--slate);margin-right:10px}
    .rk mark{background:rgba(194,87,75,.18);color:inherit;padding:2px 6px;border-radius:6px}
    .rk-ai{background:#141925;color:#eef1f6;border-radius:18px;padding:20px 24px;font-size:24px}
    .b-st h3{font-size:124px;top:250px}
    .b-st .pv3{position:absolute;left:80px;right:80px;top:760px}
    .b-st .bn-cta{top:1660px}
    .b-wd h3{font-size:58px}
    .b-wd .bn-lead{top:300px;width:430px}
    .b-wd .pv4{position:absolute;right:44px;top:90px;width:560px}
'''
campaign('procurement', service_name='ИИ‑ассистент закупок', camp_name='Три КП к обеду',
  lead='Запуск ИИ‑ассистента закупок для производств, дистрибуции и розничных сетей: идея, креативы, сценарии роликов и медиаплан на 6 недель.',
  facts=[('Цель', '8 договоров за 6 недель'), ('Аудитория', 'директора по закупкам, финансовые директора'), ('Бюджет', '500 000 ₽ — пример')],
  brief=[('Инсайт', 'Закупщик тратит дни на сбор и сравнение КП, а риски в договорах замечает, когда уже поздно. Больше всего денег теряется в «хвосте» мелких закупок, до которых не доходят руки.'),
         ('Идея', 'Три КП к обеду: рутину сбора и сравнения берёт ИИ‑ассистент, закупщику остаётся решение.'),
         ('Обещание', 'Сравнение предложений за минуты и проверка каждого договора по вашим правилам.'),
         ('Почему верить', 'Пилот на одной категории до основного договора, выгрузка в 1С, мировой опыт: Walmart и Pactum — 3% выгоды и +35 дней отсрочки.'),
         ('Тон', 'Язык закупщика и финансиста: итог с доставкой, отсрочка, штрафы, пункты договора.')],
  msgs=[('Три КП к обеду', 'главный — все каналы'), ('ИИ сравнит КП. Вы примете решение', 'истории и клипы'),
        ('Штраф 30% за отмену? ИИ заметил', 'финансовые директора и юристы'), ('Экономия прячется в мелких закупках', 'РСЯ, собственники'),
        ('Закупщик, который читает договоры до конца', 'посевы в закупочных сообществах')],
  banners=banners, banner_css=banner_css,
  scripts=[('«К обеду» · 20 секунд', [('0–5 с', 'Утро, закупщик получает заявку «20 000 коробок к 1 июня».', '«9:00. Нужны коробки. Срочно»'),
                                     ('5–15 с', 'Письма поставщикам уходят сами, приходят три КП, таблица сравнения, отмечается лучшее.', '«ИИ‑ассистент запрашивает предложения и считает итог с доставкой и отсрочкой»'),
                                     ('15–20 с', '12:30, закупщик нажимает «Согласовать». Логотип.', '«Три КП к обеду. Решение — за вами»')]),
           ('«Пункт 7.2» · 15 секунд', [('0–5 с', 'Длинный договор прокручивается.', '«Сорок страниц. Кто дочитает до пункта 7.2?»'),
                                       ('5–11 с', 'Пункт подсвечивается: штраф 30% за отмену.', '«ИИ‑ассистент читает договор до конца и находит риски»'),
                                       ('11–15 с', 'Логотип и кнопка.', '«Пилот на одной категории — до договора»')])],
  media=[('Яндекс Директ', 'поиск: «автоматизация закупок», «сравнение коммерческих предложений», «ИИ для закупщика»; РСЯ', 'текст + горизонталь', 35, 'цена заявки'),
         ('Telegram Ads', 'каналы для закупщиков и финансовых директоров', 'квадрат, текст', 20, 'цена клика'),
         ('Отраслевые медиа', 'закупочные сообщества, конференции и издания о снабжении', 'статья‑кейс + ролик «Пункт 7.2»', 20, 'переходы, запросы бренда'),
         ('VK Реклама', 'руководители производств, дистрибуции и сетей', 'квадрат, вертикальное видео', 15, 'цена заявки'),
         ('Ретаргетинг', 'посетители страницы и тарифов', 'квадрат «Штраф 30%»', 10, 'возврат на пилот')],
  budget=500000, funnel=[('Бюджет', '500 000 ₽', 100), ('Заявки', '125', 100), ('Демо', '50', 40), ('Пилоты', '15', 12), ('Договоры', '8', 6)],
  kpis=[('Цена заявки', 'до 4 000 ₽'), ('Заявка → демо', '40%'), ('Демо → пилот', '30%'), ('Пилот → договор', '50%')],
  cal=[('Подготовка: креативы, ролики, маркировка', 1, 1), ('Яндекс Директ: поиск и РСЯ', 2, 6), ('Telegram Ads и VK Реклама', 2, 6), ('Отраслевые медиа', 2, 4), ('Ретаргетинг', 3, 6), ('Пилоты у первых клиентов', 3, 6), ('Итоги и решение о масштабе', 6, 6)],
  utm_sources='yandex, telegram, vk, media', utm_content=['procurement_2026', 'lunch', 'penalty', 'compare', 'tail'])
