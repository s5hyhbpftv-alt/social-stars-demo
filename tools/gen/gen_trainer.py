import sys, json, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import *

CHIP = 'Тренажёр продаж'
NAMES = ('ИИ‑клиент', 'Менеджер')
SK = [('Контакт', 86), ('Выявление потребности', 72), ('Работа с возражением', 58), ('Следующий шаг', 90)]
DEMO = [('cl', 'Ирина, добрый день! Видел, что вы открываете два новых магазина — удобно обсудить поставки?'),
        ('ai', 'У нас уже есть поставщик, и он дешевле. Что вы можете предложить?'),
        ('cl', 'Понимаю. А что для вас сейчас важнее — цена или сроки поставки к открытию?')]

hero_vis = f'''<div class="tdemo" role="img" aria-label="Тренировка: менеджер разговаривает с ИИ-клиенткой, после звонка появляется оценка по навыкам">
        {persona('m15', 'Ирина', 'Закупщик сети магазинов', ['ИИ‑клиент', 'Торопится', 'Давит на цену'])}
        {call_ui(DEMO, title='Тренировка: холодный звонок', t='01:12', names=NAMES)}
        <div class="score"><div class="score-in"><h4>Оценка звонка</h4>{skills(SK)}</div></div>
      </div>'''

P = [('m15', 'Ирина', 'Закупщик сети магазинов', ['ИИ‑клиент', 'Торопится', 'Давит на цену'],
      [('ai', 'У нас уже есть поставщик, и он дешевле.'), ('cl', 'Понимаю. Если сравнить не цену, а стоимость за год — с доставкой и возвратами?'), ('ai', 'Хорошо, пришлите расчёт. Но у меня пять минут.')]),
     ('m50', 'Дарья', 'Владелица шоурума', ['ИИ‑клиент', 'Сомневается', 'Долго думает'],
      [('ai', 'Мне надо подумать, давайте я вам сама напишу.'), ('cl', 'Конечно. Подскажите, что именно хотите обдумать — бюджет или сроки?'), ('ai', 'Честно? Боюсь, что не окупится.')]),
     ('mb-salon', 'Марина', 'Директор салона', ['ИИ‑клиент', 'Работает с конкурентом', 'Скептик'],
      [('ai', 'Мы уже три года работаем с другой компанией, всё устраивает.'), ('cl', 'Отлично, что есть надёжный партнёр. Что бы вы в их работе улучшили, если бы могли?'), ('ai', 'Ну… отчёты они присылают с опозданием.')])]
pcards = ''.join(f'<div class="pc" role="button" tabindex="0" aria-pressed="{"true" if i == 0 else "false"}" data-i="{i}">{persona(img, n, r, t)}</div>' for i, (img, n, r, t, _) in enumerate(P))
pers = f'''<div class="pers">
        <div class="pc-list" role="group" aria-label="ИИ‑клиенты">{pcards}</div>
        <div class="pc-call">{call_ui(P[0][4], title='Тренировка', t='00:00', names=NAMES)}</div>
      </div>
      <p class="note">ИИ‑клиенты — вымышленные персонажи. Характеры и возражения собираем из ваших реальных звонков.</p>
<script type="application/json" id="pc-data">{json.dumps([p[4] for p in P], ensure_ascii=False)}</script>'''

report = f'''<div class="rep">
        <div class="rep-card">{skills([('Контакт', 86), ('Выявление потребности', 72), ('Презентация', 81), ('Работа с возражением', 58), ('Следующий шаг', 90)])}</div>
        <div class="rep-notes">
          <div><b>Получилось</b><p>Сразу назвали повод звонка и задали открытый вопрос о приоритетах.</p></div>
          <div class="lo"><b>Улучшить</b><p>На «у нас дешевле» перешли к скидке. Сначала стоило сравнить стоимость за год.</p></div>
          <div><b>Следующая тренировка</b><p>«Дорого» — три варианта клиента с разным бюджетом.</p></div>
        </div>
      </div>'''

W = [54, 58, 63, 67, 72, 78]
X0, X1, Y0, Y1 = 50, 620, 20, 220
xs = [X0 + (X1 - X0) * i / 5 for i in range(6)]
ys = [Y1 - (v - 40) / 50 * (Y1 - Y0) for v in W]
line = ' '.join(f'{"M" if i == 0 else "L"}{x:.0f} {y:.0f}' for i, (x, y) in enumerate(zip(xs, ys)))
area = line + f' L{xs[-1]:.0f} {Y1} L{xs[0]:.0f} {Y1} Z'
chart = f'''<svg class="prog" viewBox="0 0 660 260" data-draw role="img" aria-label="Средняя оценка команды выросла с 54 до 78 баллов за шесть недель — пример отчёта">
          {''.join(f'<line x1="{X0}" y1="{Y1 - (v - 40) / 50 * (Y1 - Y0):.0f}" x2="{X1}" y2="{Y1 - (v - 40) / 50 * (Y1 - Y0):.0f}"/><text x="{X0 - 10}" y="{Y1 - (v - 40) / 50 * (Y1 - Y0) + 4:.0f}" text-anchor="end">{v}</text>' for v in (50, 70, 90))}
          <path class="ar" d="{area}" data-area/><path class="ln" d="{line}" data-line/>
          {''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" data-pop/>' for x, y in zip(xs, ys))}
          {''.join(f'<text x="{x:.0f}" y="{Y1 + 26}" text-anchor="middle">Нед. {i + 1}</text>' for i, x in enumerate(xs))}
        </svg>'''
progress = f'''<div class="progw">{chart}<div class="prog-kp"><div><b data-count>78</b><span>средняя оценка команды</span></div><div><b data-count>+24</b><span>за шесть недель</span></div><div><b data-count>312</b><span>тренировок</span></div></div></div>
      <p class="note">Пример отчёта для руководителя отдела продаж — цифры условные.</p>'''

loop = f'''<div class="loopd" data-wires="a>b b>c c>d d>a:dash">
        <div class="ln1"><div class="hnode" data-n="a">{icon("chats")}<b>Реальный звонок</b><span>из телефонии</span></div><div class="hnode" data-n="b">{icon("audit")}<b>Разбор по чек‑листу</b><span>каждый звонок, а не выборка</span></div></div>
        <div class="ln2"><div class="hnode hub" data-n="d">{icon("people")}<b>Менеджер</b><span>выходит на следующий звонок сильнее</span></div><div class="hnode" data-n="c">{icon("target")}<b>Тренировка на ИИ‑клиенте</b><span>ровно по слабому месту</span></div></div>
      </div>'''

main = '<main id="main">\n' + hero('ИИ‑тренажёр продаж', 'Тренируйтесь на ИИ, а не на клиентах',
    'Менеджеры отрабатывают звонки с ИИ‑клиентами, собранными из ваших реальных разговоров. После каждой тренировки — оценка по чек‑листу и разбор ошибок.',
    [('btn-primary', '#lead', 'Попробовать тренажёр', CHIP), ('btn-line', '#personas', 'Посмотреть ИИ‑клиентов', '')], hero_vis,
    [('Тренировка', 'в любое время, 5–10 минут'), ('Оценка', 'сразу после звонка'), ('Менеджер', 'от 2 400 ₽ в месяц')], 'tr-hero') + '\n\n' + \
    subnav([('personas', 'ИИ‑клиенты'), ('report', 'Оценка'), ('progress', 'Отчёт'), ('loop', 'Разбор звонков'), ('week', 'Этапы'), ('pricing', 'Тарифы'), ('faq', 'Вопросы')], 'Попробовать', CHIP) + '\n\n' + \
    section('personas', pers, head='Клиенты, которые спорят как настоящие', lead='Выберите собеседника — и посмотрите, с чем придётся работать.', split=True) + '\n\n' + \
    section('report', report, cls='band', head='Оценка после каждого звонка') + '\n\n' + \
    section('progress', progress, head='Руководитель видит рост команды') + '\n\n' + \
    section('loop', loop, cls='band', head='Реальные звонки становятся тренировками', lead='Слабое место в живом разговоре превращается в упражнение на завтра.', split=True) + '\n\n' + \
    section('week', steps([('Неделя 1', 'Слушаем 50 звонков', 'Находим типичные возражения и сильные приёмы лучших менеджеров.'),
                           ('Неделя 2', 'ИИ‑клиенты и чек‑лист', 'Собираем персонажей и критерии оценки под ваш процесс продаж.'),
                           ('Неделя 3', 'Запуск на команду', 'Короткие тренировки каждый день — с телефона или компьютера.'),
                           ('Каждую неделю', 'Отчёт руководителю', 'Кто вырос, где провалы, какие тренировки добавить.')]), head='Запуск за три недели') + '\n\n' + \
    section('pricing', plans([
        dict(name='Команда', price='150 000 ₽', small='запуск + 2 900 ₽ за менеджера в месяц', text='До 10 менеджеров.', list=['5 ИИ‑клиентов', 'Чек‑лист оценки', 'Голос и текст', 'Отчёт раз в неделю'], cta='Выбрать «Команду»'),
        dict(name='Отдел', price='290 000 ₽', small='запуск + 2 400 ₽ за менеджера в месяц', text='До 50 менеджеров.', list=['15 ИИ‑клиентов', 'Разбор реальных звонков', 'Интеграция с телефонией', 'Новые сценарии каждый месяц'], cta='Выбрать «Отдел»', main=True, badge='Чаще выбирают'),
        dict(name='Компания', price='от 600 000 ₽', small='запуск', text='Несколько отделов и регионов.', list=['Разбор всех звонков', 'CRM и корпоративное обучение', 'Свои методики продаж', 'Развёртывание в вашем контуре'], cta='Обсудить проект')], CHIP),
        cls='band', head='Тарифы', lead='Первую неделю тренажёр работает на 3–5 менеджерах — до основного договора.', split=True) + '\n\n' + \
    section('faq', faq([
        ('Чем это лучше обычного тренинга?', 'Тренинг бывает раз в квартал, а навык нужен каждый день. Тренажёр даёт короткие повторения на ваших реальных возражениях и сразу показывает, что улучшить.'),
        ('Нужны ли записи наших звонков?', 'Желательно 50 и больше — так ИИ‑клиенты будут похожи на ваших покупателей. Если записей нет, собираем персонажей по интервью с лучшими менеджерами.'),
        ('Тренировки голосом или текстом?', 'И так, и так. Голос — как настоящий звонок, текст — для переписки в мессенджерах и почте.'),
        ('Как защищены записи звонков?', 'Храним на серверах в России, персональные данные обезличиваем до разбора. Для крупных компаний — развёртывание в вашем контуре.'),
        ('Заменит ли тренажёр руководителя отдела продаж?', 'Нет. Он забирает рутину — прослушку и разбор типовых ошибок — и даёт руководителю данные, на ком сфокусироваться.')])
        + '\n      ' + next_link('dubbing', 'wave', 'Перевод и озвучка видео'), head='Вопросы') + '\n'

style = SERVICE_CSS + '''    .tdemo{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:580px;justify-self:end;width:100%;align-items:start}
    .tdemo .persona{grid-column:1}
    .tdemo .call{grid-column:1 / -1;grid-row:2}
    .tdemo .call-log{min-height:0}
    .tdemo .score{grid-column:2;grid-row:1}
    .score-in{background:#fff;border:1px solid var(--mist);border-radius:18px;padding:18px 20px}
    .score-in h4{font-weight:500;font-size:15px;margin-bottom:12px}
    .score .sk{grid-template-columns:1fr 52px 26px;gap:8px;font-size:12.5px}
    .score .skills{gap:9px}
    .pers{display:grid;grid-template-columns:minmax(260px,380px) minmax(280px,420px);gap:clamp(32px,6vw,96px);align-items:start}
    .pc-list{display:grid;gap:12px}
    .pc{cursor:pointer;border-radius:18px;outline-offset:4px}
    .pc .ps-in{transition:border-color .2s,box-shadow .2s}
    .pc[aria-pressed="true"] .ps-in{border-color:var(--bronze);box-shadow:0 0 0 3px var(--bronze-soft)}
    .rep{display:grid;grid-template-columns:6fr 5fr;gap:clamp(24px,4vw,64px);align-items:start}
    .rep-card{background:var(--white);border:1px solid var(--mist);border-radius:var(--r-lg);padding:clamp(24px,3vw,36px)}
    .rep-notes{display:grid;gap:14px}
    .rep-notes div{padding:18px 20px;border-radius:var(--r-md);background:var(--white);border:1px solid var(--mist);border-left:3px solid var(--ink)}
    .rep-notes div.lo{border-left-color:var(--bronze)}
    .rep-notes b{font-weight:500}
    .rep-notes p{color:var(--slate);font-size:15px;margin-top:4px}
    .progw{display:grid;grid-template-columns:7fr 3fr;gap:clamp(24px,4vw,64px);align-items:center}
    .prog{width:100%;height:auto;overflow:visible}
    .prog line{stroke:var(--mist);stroke-width:1}
    .prog text{font:13px var(--font);fill:var(--slate)}
    .prog .ln{fill:none;stroke:var(--bronze);stroke-width:3;stroke-linejoin:round}
    .prog .ar{fill:var(--bronze-soft);opacity:.7}
    .prog circle{fill:var(--white);stroke:var(--bronze);stroke-width:2.5}
    .prog-kp{display:grid;gap:22px}
    .prog-kp b{display:block;font-size:clamp(36px,4vw,52px);font-weight:200;letter-spacing:-.04em;line-height:1}
    .prog-kp span{color:var(--slate);font-size:14.5px}
    .loopd{display:grid;gap:clamp(40px,6vw,80px)}
    .loopd .ln1,.loopd .ln2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(80px,14vw,220px);max-width:820px}
    .hnode{display:grid;gap:4px;padding:18px 20px;border-radius:var(--r-md);background:var(--white);border:1px solid var(--mist)}
    .hnode .ic{color:var(--bronze-2);margin-bottom:6px}
    .hnode b{font-weight:500;font-size:17px}
    .hnode span{color:var(--slate);font-size:14.5px}
    .hnode.hub{background:var(--ink);border-color:var(--ink);color:#fff}
    .hnode.hub span{color:#a9b1c0}.hnode.hub .ic{color:var(--bronze)}
    @media (max-width:1024px){ .tdemo{justify-self:start} .pers,.rep,.progw{grid-template-columns:1fr} .pc-call{max-width:420px} }
    @media (max-width:600px){ .tdemo{grid-template-columns:1fr} .tdemo .score{grid-column:1;grid-row:auto} .loopd .ln1,.loopd .ln2{grid-template-columns:1fr;gap:14px} .loopd .wires{display:none} .prog text{font-size:16px} }
'''

script = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  const g = window.gsap, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const data = JSON.parse(document.getElementById('pc-data').textContent), call = document.querySelector('.pc-call .call'), btns = [...document.querySelectorAll('.pc')];
  const show = i => {
    btns.forEach((b, j) => b.setAttribute('aria-pressed', String(i === j)));
    call.querySelector('.call-log').innerHTML = data[i].map(([w, t]) => `<p class="b ${w}"><small>${w === 'ai' ? 'ИИ‑клиент' : 'Менеджер'}</small>${t}</p>`).join('');
    if (g && !reduce) g.fromTo(call.querySelectorAll('.call-log .b'), { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: .45, stagger: .7, ease: 'power2.out' });
  };
  btns.forEach((b, i) => { b.addEventListener('click', () => show(i)); b.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(i); } }); });
  // первый экран: реплики тренировки по очереди, волна «говорит»
  const hc = document.querySelector('.tdemo .call');
  if (hc && g && !reduce) {
    const bs = hc.querySelectorAll('.call-log .b'), bars = hc.querySelectorAll('.call-wave i');
    const tl = g.timeline({ repeat: -1, repeatDelay: 3 });
    tl.set(bs, { opacity: 0, y: 10 });
    bs.forEach((b, i) => tl.to(b, { opacity: 1, y: 0, duration: .45 }, .4 + i * 1.8).to(bars, { scaleY: () => .2 + Math.random() * .8, duration: .14, stagger: { each: .015, repeat: 5, yoyo: true } }, .4 + i * 1.8).to(bars, { scaleY: .18, duration: .3 }, 1.8 + i * 1.8));
  }
});
</script>'''

build('ai/ugc/index.html', 'ai/trainer/index.html',
      title='ИИ-тренажёр продаж: тренировки с ИИ-клиентами — Social Stars AI',
      desc='Менеджеры отрабатывают звонки с ИИ-клиентами, собранными из ваших реальных разговоров, и получают оценку по чек-листу после каждой тренировки. Разбор реальных звонков и отчёт руководителю. Запуск от 150 000 ₽.',
      path='/ai/trainer/', og_title='Тренируйтесь на ИИ, а не на клиентах — ИИ-тренажёр продаж', og_desc='Короткие тренировки с ИИ-клиентами и оценка после каждого звонка.',
      ld=ld_service('ИИ-тренажёр продаж', '/ai/trainer/', 150000), style=style, main=main, script=script, service=CHIP)

# ——— кампания
L = lambda: legal()
bub = [('ai', 'Дорого. У конкурентов дешевле.'), ('cl', 'Давайте сравним не цену, а стоимость за год?')]
sk_static = lambda rows: '<div class="skills">' + ''.join(f'<div class="sk{" lo" if v < 70 else ""}"><span>{n}</span><span class="tr"><i style="width:{v}%"></i></span><b>{v}</b></div>' for n, v in rows) + '</div>'
banners = [
 ('square-hundred', 1080, 1080, 'Квадрат 1080×1080 — Telegram Ads, VK Реклама',
  f'''<div class="bn b-sq ink">{LOGO}<h3>Первая сотня<br>отказов —<br>в тренажёре</h3>
      <span class="bn-cta">Попробовать тренажёр</span>
      <div class="tv">{call_ui(bub, title="Тренировка с ИИ‑клиентом", t="00:41", bars=26, static=True, names=NAMES)}</div>{L()}</div>'''),
 ('square-expensive', 1080, 1080, 'Квадрат 1080×1080 — руководители отделов продаж',
  f'''<div class="bn b-sq2">{LOGO}<h3>«Дорого» — отработано<br>40 раз до обеда</h3>
      <div class="tv2">{persona("m50", "Дарья", "Владелица шоурума", ["ИИ‑клиент", "Сомневается"], lazy=False)}<div class="score"><div class="score-in"><h4>Оценка звонка</h4>{sk_static(SK)}</div></div></div>
      <span class="bn-cta">Попробовать тренажёр</span>{L()}</div>'''),
 ('story-train', 1080, 1920, 'Вертикаль 1080×1920 — истории и клипы',
  f'''<div class="bn b-st ink">{LOGO}<h3>Тренируйтесь<br>на ИИ, а не<br>на клиентах</h3>
      <div class="tv3">{persona("mb-salon", "Марина", "Директор салона", ["ИИ‑клиент", "Работает с конкурентом"], lazy=False)}{call_ui([("ai", "Мы уже три года работаем с другой компанией."), ("cl", "Что бы вы в их работе улучшили, если бы могли?")], title="Тренировка", t="01:05", bars=30, static=True, names=NAMES)}</div>
      <span class="bn-cta">Попробовать тренажёр</span>{L()}</div>'''),
 ('wide-rop', 1200, 628, 'Горизонталь 1200×628 — Яндекс РСЯ, VK Реклама',
  f'''<div class="bn b-wd">{LOGO}<h3>РОП не слушает<br>все звонки. ИИ — да</h3>
      <p class="bn-lead">Разбор каждого звонка и тренировка по слабому месту.</p>
      <span class="bn-cta">Попробовать тренажёр</span>
      <div class="tv4"><div class="score"><div class="score-in"><h4>Оценка звонка</h4>{sk_static(SK)}</div></div></div>{L()}</div>'''),
]
banner_css = '''    .bn .score-in{color:var(--ink)}
    .b-sq h3{font-size:112px}
    .b-sq .bn-cta{top:640px}
    .b-sq .tv{position:absolute;right:48px;top:560px;width:470px;display:grid;gap:18px}
    .b-sq .tv .persona{width:340px}
    .b-sq .tv .call-log{min-height:0}
    .b-sq .tv .call{margin-top:-6px}
    .b-sq2 h3{font-size:76px;width:980px}
    .b-sq2 .tv2{position:absolute;left:64px;right:64px;top:400px;display:grid;grid-template-columns:400px 1fr;gap:32px;align-items:start}
    .b-sq2 .tv2 .score-in{padding:34px 36px;border-radius:30px}
    .b-sq2 .tv2 .score-in h4{font-size:28px;margin-bottom:22px}
    .b-sq2 .tv2 .sk{grid-template-columns:1fr 150px 50px;font-size:22px;gap:14px}
    .b-sq2 .tv2 .skills{gap:18px}
    .b-sq2 .tv2 .sk .tr{height:12px}
    .b-sq2 .bn-cta{top:840px}
    .b-st h3{font-size:132px;top:250px}
    .b-st .tv3{position:absolute;left:80px;right:80px;top:720px;display:grid;gap:24px}
    .b-st .tv3 .persona{width:540px}
    .b-st .tv3 .call{width:700px;justify-self:end}
    .b-st .tv3 .call-log{min-height:0}
    .b-st .bn-cta{top:1700px}
    .b-wd h3{font-size:64px}
    .b-wd .bn-lead{top:320px}
    .b-wd .tv4{position:absolute;right:48px;top:110px;width:500px}
    .b-wd .tv4 .score-in{padding:28px 30px;border-radius:24px}
    .b-wd .tv4 .score-in h4{font-size:22px;margin-bottom:16px}
    .b-wd .tv4 .sk{grid-template-columns:1fr 150px 40px;font-size:18px;gap:12px}
    .b-wd .tv4 .skills{gap:14px}
'''
campaign('trainer', service_name='ИИ‑тренажёр продаж', camp_name='Первая сотня отказов',
  lead='Запуск ИИ‑тренажёра для отделов продаж: идея, креативы, сценарии роликов и медиаплан на 6 недель.',
  facts=[('Цель', '8 договоров за 6 недель'), ('Аудитория', 'РОПы, коммерческие директора, собственники'), ('Бюджет', '500 000 ₽ — пример')],
  brief=[('Инсайт', 'Новички учатся на живых клиентах и сливают первые заявки. Руководитель отдела продаж физически не успевает слушать звонки.'),
         ('Идея', 'Первая сотня отказов — в тренажёре: менеджер слышит «дорого» и «мы подумаем» от ИИ‑клиентов, а не от ваших покупателей.'),
         ('Обещание', 'Короткие тренировки каждый день и оценка после каждого звонка.'),
         ('Почему верить', 'ИИ‑клиенты собраны из ваших реальных звонков; пилот на 3–5 менеджерах до основного договора.'),
         ('Тон', 'Язык отдела продаж: возражения, скрипты, конверсия. Уважительно к менеджерам — тренажёр помогает, а не контролирует.')],
  msgs=[('Первая сотня отказов — в тренажёре', 'главный — все каналы'), ('Тренируйтесь на ИИ, а не на клиентах', 'истории и клипы'),
        ('«Дорого» — отработано 40 раз до обеда', 'руководители отделов продаж'), ('РОП не слушает все звонки. ИИ — да', 'РСЯ, собственники'),
        ('Новичок выходит на линию подготовленным', 'посевы у бизнес‑тренеров')],
  banners=banners, banner_css=banner_css,
  scripts=[('«Сотый звонок» · 20 секунд', [('0–6 с', 'Быстрая нарезка: менеджер снова и снова слышит «дорого», «нам не нужно», «мы подумаем».', 'Титр: «Отказ № 1… № 37… № 99»'),
                                          ('6–14 с', 'Оценка на экране растёт, менеджер спокойнее и увереннее.', '«Все отказы — от ИИ‑клиентов в тренажёре»'),
                                          ('14–20 с', 'Настоящий звонок, клиент соглашается на встречу. Логотип.', '«А сотый звонок — уже настоящий. ИИ‑тренажёр продаж Social Stars AI»')]),
           ('«РОП» · 15 секунд', [('0–4 с', 'Руководитель отдела продаж с наушниками и горой записей.', '«200 звонков в день. Вы слушаете пять»'),
                                 ('4–11 с', 'Экран отчёта: оценки по каждому менеджеру и слабые места.', '«ИИ разбирает все и собирает тренировку по слабому месту»'),
                                 ('11–15 с', 'Логотип и кнопка.', '«Попробуйте на своей команде»')])],
  media=[('Telegram Ads', 'каналы о продажах и управлении отделом продаж', 'квадрат, текст', 30, 'цена клика'),
         ('Яндекс Директ', 'поиск: «обучение менеджеров по продажам», «тренажёр продаж», «контроль качества звонков»; РСЯ', 'текст + горизонталь', 25, 'цена заявки'),
         ('Посевы', 'бизнес‑тренеры, подкасты и сообщества о продажах', 'нативный пост + ролик «Сотый звонок»', 20, 'переходы'),
         ('VK Реклама', 'руководители отделов продаж, собственники малого и среднего бизнеса', 'квадрат, вертикальное видео', 15, 'цена заявки'),
         ('Ретаргетинг', 'посетители страницы и тарифов', 'квадрат «Дорого»', 10, 'возврат на пилот')],
  budget=500000, funnel=[('Бюджет', '500 000 ₽', 100), ('Заявки', '125', 100), ('Демо', '50', 40), ('Пилоты', '15', 12), ('Договоры', '8', 6)],
  kpis=[('Цена заявки', 'до 4 000 ₽'), ('Заявка → демо', '40%'), ('Демо → пилот', '30%'), ('Пилот → договор', '50%')],
  cal=[('Подготовка: креативы, ролики, маркировка', 1, 1), ('Посевы у бизнес‑тренеров', 2, 4), ('Telegram Ads и VK Реклама', 2, 6), ('Яндекс Директ: поиск и РСЯ', 2, 6), ('Ретаргетинг', 3, 6), ('Пилоты у первых клиентов', 4, 6), ('Итоги и решение о масштабе', 6, 6)],
  utm_sources='telegram, yandex, vk, seeding', utm_content=['trainer_2026', 'hundred', 'expensive', 'train', 'rop'])
