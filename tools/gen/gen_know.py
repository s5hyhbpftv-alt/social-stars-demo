import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import *

CHIP = 'ИИ-поиск по документам'


def qs(q, ans, srcs, acc='Доступно отделу закупок', label='Ответ по вашим документам'):
    sr = ''.join(f'<div><i>{i + 1}</i>{icon("doc")}<b>{a}</b><span>{b}</span></div>' for i, (a, b) in enumerate(srcs))
    accs = f'<span class="qs-acc">{icon("lock")}{acc}</span>' if acc else ''
    return (f'<div class="qs"><div class="qs-in"><div class="qs-bar">{icon("search")}<span class="qs-q">{q}</span></div>'
            f'<div class="qs-ans"><small>{icon("sparkle")}{label}</small><p>{ans}</p></div><div class="qs-src">{sr}</div>{accs}</div></div>')


HERO = ('Какая отсрочка платежа в договоре с «Вектором»?',
        '30 календарных дней с даты поставки<sup>1</sup>. Для заказов больше 1 млн ₽ — 45 дней по допсоглашению от 12 марта<sup>2</sup>.',
        [('Договор поставки № 14, Вектор.pdf', 'стр. 3, п. 5.1'), ('Допсоглашение № 2.docx', 'п. 1')])
hero_vis = f'<div class="kn-hero" data-kn>{qs(*HERO)}</div>'

src_nodes = [('s1', 'server', '1С и учётные системы'), ('s2', 'layout', 'Битрикс24 и CRM'), ('s3', 'doc', 'Договоры и сканы'),
             ('s4', 'mail', 'Почта'), ('s5', 'book', 'Регламенты и вики'), ('s6', 'chats', 'Рабочие чаты')]
sources = f'''<div class="srcmap" data-wires="{" ".join(f"{n}>hub:h" for n, _, _ in src_nodes)} hub>out:h:2.4">
        <div class="sm-col">{"".join(f'<div class="hnode sm" data-n="{n}">{icon(i)}<b>{t}</b></div>' for n, i, t in src_nodes)}</div>
        <div class="sm-mid"><div class="hnode hub" data-n="hub">{icon("lock")}<b>Индекс с правами доступа</b><span>каждый документ помнит, кому его можно показывать</span></div></div>
        <div class="sm-out" data-n="out">{qs("Сколько дней отпуска у новичка в первый год?", "28 календарных дней; первые 14 можно взять после шести месяцев работы<sup>1</sup>.", [("Положение об отпусках.pdf", "п. 2.3")], acc="Доступно всем сотрудникам", label="Ответ")}</div>
      </div>'''

rights = f'''<div class="rights">
        <div><p class="who">{icon("user")}Спрашивает бухгалтер</p>{qs("Какая премия у отдела продаж за квартал?", "Фонд премии — 12% от выручки сверх плана, выплата до 15‑го числа месяца после квартала<sup>1</sup>.", [("Положение о премировании.pdf", "п. 4")], acc="Доступно бухгалтерии")}</div>
        <div><p class="who">{icon("user")}Спрашивает менеджер</p>{qs("Какая премия у отдела продаж за квартал?", "Документа с ответом нет среди доступных вам. Уточните у руководителя отдела — могу отправить ему вопрос.", [], acc="Ответ с учётом ваших прав", label="Нет доступа")}</div>
      </div>
      <p class="note">Документы и цифры в примерах условные.</p>'''

DEPTS = {'Продажи': ('Какую скидку я могу дать без согласования?', 'До 7% для клиентов с оборотом от 500 тыс. ₽ в квартал; больше — через коммерческого директора<sup>1</sup>.', [('Регламент скидок 2026.docx', 'п. 3.2')]),
         'Кадры': ('Как оформить удалённую работу на неделю?', 'Заявление в «Кадрах» 1С за три рабочих дня, согласует руководитель; ноутбук выдаёт ИТ по заявке<sup>1</sup>.', [('Положение о дистанционной работе.pdf', 'п. 2.1')]),
         'Юристы': ('Какие договоры нужно согласовывать с юристом?', 'Все договоры от 300 тыс. ₽, любые с иностранными контрагентами и все с отсрочкой больше 60 дней<sup>1</sup>.', [('Порядок согласования договоров.docx', 'п. 1.4')]),
         'Поддержка': ('Клиент просит вернуть товар через 20 дней. Можно?', 'Да, если товар не был в использовании: срок возврата — 30 дней, возврат денег в течение 10 дней<sup>1</sup>.', [('Правила возврата.pdf', 'раздел 2')])}
tabs = ''.join(f'<button type="button" class="sc-tab" aria-pressed="{"true" if i == 0 else "false"}" data-i="{i}">{n}</button>' for i, n in enumerate(DEPTS))
first = list(DEPTS.values())[0]
depts = f'''<div class="scen">
        <div class="sc-tabs" role="group" aria-label="Отделы">{tabs}</div>
        <div class="dp-ans">{qs(*first, acc="Доступно отделу продаж")}</div>
      </div>
<script type="application/json" id="dp-data">{json.dumps([[k] + list(v) for k, v in DEPTS.items()], ensure_ascii=False)}</script>'''

main = '<main id="main">\n' + hero('ИИ‑поиск по документам', 'Спросите у компании',
    'ИИ‑ассистент отвечает на вопросы сотрудников по вашим документам, базам и регламентам — со ссылкой на источник и с учётом прав доступа.',
    [('btn-primary', '#lead', 'Демо на ваших документах', CHIP), ('btn-line', '#sources', 'Как это работает', '')], hero_vis,
    [('Ответ', 'за секунды, со ссылкой'), ('Права доступа', 'как в ваших системах'), ('Где работает', 'облако РФ или ваш контур')], 'kn-hero-s') + '\n\n' + \
    subnav([('sources', 'Источники'), ('rights', 'Права'), ('depts', 'Отделы'), ('contour', 'Контур'), ('week', 'Этапы'), ('pricing', 'Тарифы'), ('faq', 'Вопросы')], 'Демо', CHIP) + '\n\n' + \
    section('sources', sources, head='Все знания компании — в одном ответе', lead='Подключаем ваши системы, а не переносим документы в новую.', split=True) + '\n\n' + \
    section('rights', rights, cls='band', head='Каждый видит только своё') + '\n\n' + \
    section('depts', depts, head='Вопросы, которые задают каждый день', lead='Выберите отдел.', split=True) + '\n\n' + \
    section('contour', ethics([('server', 'Облако в России', 'Быстрый старт на серверах в РФ по 152‑ФЗ.'),
                               ('lock', 'Ваш контур', 'Модель и индекс на ваших серверах — данные не покидают компанию.'),
                               ('brain', 'Модель на выбор', 'GigaChat, YandexGPT или открытые модели — под задачу и бюджет.'),
                               ('audit', 'Журнал запросов', 'Кто, что и когда спрашивал — для службы безопасности.')]), cls='band', head='Где работает') + '\n\n' + \
    section('week', steps([('Неделя 1', 'Аудит источников', 'Какие системы, где права, что устарело.'),
                           ('Недели 2–3', 'Подключение и права', 'Индексируем документы, переносим права из ваших систем.'),
                           ('Неделя 4', 'Проверка на 100 вопросах', 'Сотрудники задают реальные вопросы, мы меряем точность.'),
                           ('Неделя 5', 'Запуск', 'Бот в Telegram, окно на портале или в Битрикс24.')]), head='Запуск за пять недель') + '\n\n' + \
    section('pricing', plans([
        dict(name='Отдел', price='290 000 ₽', small='запуск + 39 000 ₽ в месяц', text='До 50 сотрудников, 3 источника.', list=['Регламенты, договоры, вики', 'Права по отделам', 'Бот в Telegram', 'Отчёт о вопросах'], cta='Выбрать «Отдел»'),
        dict(name='Компания', price='690 000 ₽', small='запуск + от 90 000 ₽ в месяц', text='Все отделы и системы.', list=['1С, CRM, почта, сканы', 'Права из ваших систем', 'Портал и Битрикс24', 'Журнал запросов'], cta='Выбрать «Компанию»', main=True, badge='Чаще выбирают'),
        dict(name='Закрытый контур', price='от 1,5 млн ₽', small='проект', text='Для банков, промышленности и госсектора.', list=['Модель на ваших серверах', 'Без выхода в интернет', 'Интеграция со службой ИБ', 'Поддержка 24/7'], cta='Обсудить проект')], CHIP),
        cls='band', head='Тарифы', lead='Демо на 20–30 ваших документах — до договора.', split=True) + '\n\n' + \
    section('faq', faq([
        ('Не будет ли ИИ придумывать ответы?', 'Ассистент отвечает только по найденным документам и всегда даёт ссылку. Если ответа нет — так и говорит и предлагает, кому задать вопрос.'),
        ('Как соблюдаются права доступа?', 'Права переносим из ваших систем: 1С, Битрикс24, общих папок. Сотрудник получает ответ только из документов, которые ему и так доступны.'),
        ('Где сотрудники задают вопросы?', 'В Telegram, на корпоративном портале, в Битрикс24 или в окне на вашем сайте для клиентов.'),
        ('Подойдут ли сканы и старые PDF?', 'Да, распознаём сканы, таблицы и печати. Качество проверяем на ваших документах в демо.'),
        ('Как быстро появляются новые документы?', 'Через несколько минут после загрузки. Устаревшие версии помечаем и не используем в ответах.')])
        + '\n      ' + next_link('procurement', 'flow', 'ИИ‑ассистент закупок'), head='Вопросы') + '\n'

style = SERVICE_CSS + '''    .kn-hero{max-width:560px;justify-self:end;width:100%}
    .srcmap{display:grid;grid-template-columns:minmax(200px,260px) minmax(200px,260px) minmax(280px,1fr);gap:clamp(40px,6vw,100px);align-items:center}
    .sm-col{display:grid;gap:10px}
    .hnode{display:grid;gap:4px;padding:18px 20px;border-radius:var(--r-md);background:var(--white);border:1px solid var(--mist)}
    .hnode .ic{color:var(--bronze-2);margin-bottom:6px}
    .hnode b{font-weight:500;font-size:17px}
    .hnode span{color:var(--slate);font-size:14.5px}
    .hnode.sm{grid-template-columns:auto 1fr;align-items:center;gap:12px;padding:12px 16px}
    .hnode.sm .ic{margin:0}.hnode.sm b{font-size:15.5px}
    .hnode.hub{background:var(--ink);border-color:var(--ink);color:#fff}
    .hnode.hub span{color:#a9b1c0}.hnode.hub .ic{color:var(--bronze)}
    .rights{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,48px);align-items:start}
    .rights .who{display:flex;align-items:center;gap:10px;font-weight:500;margin-bottom:14px}
    .rights .who .ic{color:var(--bronze-2)}
    .rights>div:last-child .qs-ans small{color:var(--slate)}
    .scen{display:grid;grid-template-columns:minmax(200px,300px) minmax(300px,560px);gap:clamp(32px,6vw,96px);align-items:start}
    .sc-tabs{display:grid;gap:10px;align-content:start}
    .sc-tab{text-align:left;padding:18px 20px;border-radius:var(--r-md);border:1px solid var(--mist);background:var(--white);font:400 18px/1.3 var(--font);color:var(--ink);cursor:pointer;transition:border-color .2s,box-shadow .2s}
    .sc-tab[aria-pressed="true"]{border-color:var(--bronze);box-shadow:0 0 0 3px var(--bronze-soft)}
    @media (max-width:1024px){ .kn-hero{justify-self:start} .srcmap{grid-template-columns:1fr;gap:16px} .srcmap .wires{display:none} .sm-col{grid-template-columns:1fr 1fr} .rights,.scen{grid-template-columns:1fr} }
    @media (max-width:600px){ .sm-col{grid-template-columns:1fr} }
'''

script = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  const g = window.gsap, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // первый экран: вопрос печатается, ответ проявляется, источники появляются
  const hero = document.querySelector('[data-kn]');
  if (hero && g && !reduce) {
    const q = hero.querySelector('.qs-q'), full = q.textContent, ans = hero.querySelector('.qs-ans'), src = hero.querySelectorAll('.qs-src > div, .qs-acc'), o = { n: 0 };
    const tl = g.timeline({ repeat: -1, repeatDelay: 3.5 });
    tl.set([ans, ...src], { opacity: 0, y: 8 }).set(o, { n: 0 })
      .to(o, { n: full.length, duration: 1.6, ease: 'none', onUpdate: () => { q.textContent = full.slice(0, Math.round(o.n)); } })
      .to(ans, { opacity: 1, y: 0, duration: .6, ease: 'power2.out' }, '+=.35')
      .to(src, { opacity: 1, y: 0, duration: .45, stagger: .18, ease: 'power2.out' }, '+=.2');
  }
  // вопросы по отделам
  const data = JSON.parse(document.getElementById('dp-data').textContent), tabs = [...document.querySelectorAll('#depts .sc-tab')], box = document.querySelector('.dp-ans');
  tabs.forEach((b, i) => b.addEventListener('click', () => {
    tabs.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    const [dep, q, a, s] = data[i];
    box.querySelector('.qs-q').textContent = q;
    box.querySelector('.qs-ans p').innerHTML = a;
    box.querySelector('.qs-src').innerHTML = s.map(([t, p], k) => `<div><i>${k + 1}</i><svg class="ic"><use href="#i-doc"/></svg><b>${t}</b><span>${p}</span></div>`).join('');
    box.querySelector('.qs-acc').lastChild.textContent = 'Доступно: ' + dep.toLowerCase();
    if (g && !reduce) g.fromTo(box.querySelectorAll('.qs-ans, .qs-src > div'), { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: .45, stagger: .12 });
  }));
});
</script>'''

build('ai/ugc/index.html', 'ai/knowledge/index.html',
      title='ИИ-поиск по документам компании с учётом прав доступа — Social Stars AI',
      desc='ИИ-ассистент отвечает сотрудникам по договорам, регламентам, 1С и CRM со ссылкой на источник и с учётом прав доступа. Облако в России или ваш контур. Запуск от 290 000 ₽.',
      path='/ai/knowledge/', og_title='Спросите у компании — ИИ-поиск по документам', og_desc='Ответ по вашим документам за секунды — со ссылкой и с учётом прав.',
      ld=ld_service('ИИ-поиск по документам компании', '/ai/knowledge/', 290000), style=style, main=main, script=script, service=CHIP)

# ——— кампания
L = lambda: legal()
banners = [
 ('square-ask', 1080, 1080, 'Квадрат 1080×1080 — Telegram Ads, VK Реклама',
  f'''<div class="bn b-sq ink">{LOGO}<h3>Спросите<br>у компании</h3>
      <p class="bn-lead">ИИ отвечает по вашим документам — со ссылкой на источник.</p>
      <span class="bn-cta">Демо на ваших документах</span>
      <div class="kv">{qs(*HERO)}</div>{L()}</div>'''),
 ('square-link', 1080, 1080, 'Квадрат 1080×1080 — ИТ‑директора и операционные руководители',
  f'''<div class="bn b-sq2">{LOGO}<h3>Ответ за секунды —<br>со ссылкой на документ</h3>
      <div class="kv2">{qs(*list(DEPTS.values())[0], acc="Доступно отделу продаж")}</div>
      <span class="bn-cta">Демо</span>{L()}</div>'''),
 ('story-newbie', 1080, 1920, 'Вертикаль 1080×1920 — истории и клипы',
  f'''<div class="bn b-st ink">{LOGO}<h3>Новичку<br>не нужно<br>дёргать коллег</h3>
      <div class="kv3">{qs("Сколько дней отпуска у новичка в первый год?", "28 календарных дней; первые 14 можно взять после шести месяцев работы<sup>1</sup>.", [("Положение об отпусках.pdf", "п. 2.3")], acc="Доступно всем сотрудникам")}</div>
      <p class="bn-lead">Регламенты, договоры и базы — в одном ответе.</p>
      <span class="bn-cta">Демо на ваших документах</span>{L()}</div>'''),
 ('wide-rules', 1200, 628, 'Горизонталь 1200×628 — Яндекс РСЯ, VK Реклама',
  f'''<div class="bn b-wd">{LOGO}<h3>Регламенты,<br>которые читают</h3>
      <p class="bn-lead">Сотрудники спрашивают — ИИ отвечает по документам.</p>
      <span class="bn-cta">Демо</span>
      <div class="kv4">{qs(*list(DEPTS.values())[2], acc="")}</div>{L()}</div>'''),
]
banner_css = '''    .b-sq h3{font-size:124px}
    .b-sq .bn-lead{top:470px;width:420px}
    .b-sq .bn-cta{top:740px;font-size:26px}
    .b-sq .kv{position:absolute;right:44px;top:450px;width:520px}
    .b-sq2 h3{font-size:74px;width:980px}
    .b-sq2 .kv2{position:absolute;left:64px;top:380px;width:640px}
    .b-sq2 .bn-cta{left:760px;top:420px}
    .b-st h3{font-size:132px;top:250px}
    .b-st .kv3{position:absolute;left:80px;right:80px;top:760px}
    .b-st .bn-lead{top:1420px;width:900px;font-size:42px}
    .b-st .bn-cta{top:1680px}
    .b-wd h3{font-size:62px}
    .b-wd .bn-lead{top:320px;width:420px}
    .b-wd .kv4{position:absolute;right:44px;top:60px;width:540px}
    .bn .qs-q::after{display:none}
'''
campaign('knowledge', service_name='ИИ‑поиск по документам', camp_name='Спросите у компании',
  lead='Запуск ИИ‑поиска по документам для средних и крупных компаний: идея, креативы, сценарии роликов и медиаплан на 6 недель.',
  facts=[('Цель', '9 договоров за 6 недель'), ('Аудитория', 'ИТ‑директора, операционные и HR‑руководители'), ('Бюджет', '600 000 ₽ — пример')],
  brief=[('Инсайт', 'Ответы есть в документах, но их никто не может найти: новички дёргают коллег, а опытные сотрудники тратят часы на поиск в папках и чатах.'),
         ('Идея', 'Спросите у компании: у каждой компании появляется собеседник, который знает все её документы.'),
         ('Обещание', 'Ответ за секунды со ссылкой на документ и с учётом прав доступа.'),
         ('Почему верить', 'Демо на 20–30 ваших документах до договора; облако в РФ или ваш контур; журнал запросов для безопасности.'),
         ('Тон', 'Спокойно и точно, без магии: конкретные вопросы сотрудников и ссылки на пункты документов.')],
  msgs=[('Спросите у компании', 'главный — все каналы'), ('Ответ за секунды — со ссылкой на документ', 'ИТ‑директора'),
        ('Новичку не нужно дёргать коллег', 'HR, истории и клипы'), ('Регламенты, которые читают', 'РСЯ, операционные директора'),
        ('Каждый видит только свои документы', 'служба безопасности, ретаргетинг')],
  banners=banners, banner_css=banner_css,
  scripts=[('«Первый день» · 20 секунд', [('0–5 с', 'Новичок за столом, вокруг занятые коллеги.', '«Первый день. Вопросов — сорок, спросить — некого»'),
                                         ('5–15 с', 'Окно поиска: вопрос, ответ со ссылкой на пункт регламента.', '«Спросите у компании. Ответ — за секунды, со ссылкой на документ»'),
                                         ('15–20 с', 'Логотип и кнопка.', '«ИИ‑поиск по документам Social Stars AI»')]),
           ('«Права» · 15 секунд', [('0–5 с', 'Два сотрудника задают один и тот же вопрос.', '«Один вопрос — два сотрудника»'),
                                   ('5–11 с', 'Бухгалтер получает ответ, менеджер — «нет доступа, спросите руководителя».', '«Каждый видит только то, что ему положено»'),
                                   ('11–15 с', 'Логотип.', '«Демо на ваших документах — до договора»')])],
  media=[('Яндекс Директ', 'поиск: «корпоративный поиск ИИ», «база знаний с нейросетью», «RAG внедрение»; РСЯ', 'текст + горизонталь', 35, 'цена заявки'),
         ('Telegram Ads', 'каналы для ИТ‑директоров, HR и операционных руководителей', 'квадрат, текст', 20, 'цена клика'),
         ('Посевы и подкасты', 'отраслевые медиа и подкасты о цифровизации', 'статья‑кейс + ролик «Права»', 20, 'переходы, запросы бренда'),
         ('VK Реклама', 'руководители среднего и крупного бизнеса', 'квадрат, вертикальное видео', 15, 'цена заявки'),
         ('Ретаргетинг', 'посетители страницы и тарифов', 'квадрат «Ответ со ссылкой»', 10, 'возврат на демо')],
  budget=600000, funnel=[('Бюджет', '600 000 ₽', 100), ('Заявки', '150', 100), ('Демо', '60', 40), ('Пилоты', '18', 12), ('Договоры', '9', 6)],
  kpis=[('Цена заявки', 'до 4 000 ₽'), ('Заявка → демо', '40%'), ('Демо → пилот', '30%'), ('Пилот → договор', '50%')],
  cal=[('Подготовка: креативы, ролики, маркировка', 1, 1), ('Яндекс Директ: поиск и РСЯ', 2, 6), ('Telegram Ads и VK Реклама', 2, 6), ('Посевы и подкасты', 2, 4), ('Ретаргетинг', 3, 6), ('Демо и пилоты у первых клиентов', 3, 6), ('Итоги и решение о масштабе', 6, 6)],
  utm_sources='yandex, telegram, vk, seeding', utm_content=['knowledge_2026', 'ask', 'link', 'newbie', 'rules'])
