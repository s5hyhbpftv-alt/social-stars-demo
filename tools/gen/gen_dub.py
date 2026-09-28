import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import *

CHIP = 'Перевод видео'
LANGS = [('RU', 'ru', 'Примерка — бесплатно до пятницы. Ждём вас в ателье.'),
         ('EN', 'en', 'Fittings are free until Friday. See you at the studio.'),
         ('TR', 'tr', 'Cumaya kadar prova ücretsiz. Sizi atölyede bekliyoruz.'),
         ('KZ', 'kk', 'Жұмаға дейін киіп көру тегін. Сізді ательеде күтеміз.'),
         ('UZ', 'uz', 'Juma kunigacha kiyib ko‘rish bepul. Sizni atelyeda kutamiz.'),
         ('AR', 'ar', 'القياس مجاني حتى يوم الجمعة. بانتظاركم في المشغل.'),
         ('ZH', 'zh', '周五前试衣免费。我们在工作室等您。'),
         ('ES', 'es', 'La prueba es gratis hasta el viernes. Te esperamos en el taller.')]


def player(active=1, video=True, lazy=True, langs=LANGS, t='0:12 / 0:31', interactive=False):
    code, lang, text = langs[active]
    media = ('<video class="media vpl-v" src="/social-stars-demo/ai/video/fitting.mp4" poster="/social-stars-demo/ai/img/ugc/v-fitting.webp" muted loop playsinline preload="none" style="--op:55% 40%"></video>'
             if video else f'<img src="/social-stars-demo/ai/img/ugc/v-fitting.webp" alt=""{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""} style="--op:55% 40%" />')
    tag = 'button type="button"' if interactive else 'span'
    close = 'button' if interactive else 'span'
    chips = ''.join(f'<{tag} class="{"on" if i == active else ""}"{(" aria-pressed=" + chr(34) + ("true" if i == active else "false") + chr(34)) if interactive else ""} data-i="{i}">{c}</{close}>' for i, (c, _, _) in enumerate(langs))
    return (f'<div class="vpl"><div class="vpl-in"><div class="vpl-scr">{media}<span class="vpl-badge">ИИ‑перевод</span>'
            f'<p class="vpl-sub" lang="{lang}" dir="auto"><span>{text}</span></p></div>'
            f'<div class="vpl-bar">{icon("video")}<span class="vpl-prog"><i></i></span><span>{t}</span></div>'
            f'<div class="vpl-langs"{" role=" + chr(34) + "group" + chr(34) + " aria-label=" + chr(34) + "Язык" + chr(34) if interactive else ""}>{chips}</div></div></div>')


hero_vis = f'<div class="dub-hero">{player(1, interactive=True)}<p class="note">Демонстрация интерфейса: субтитры меняются, звук в примере выключен.</p></div>'

sync = '''<div class="sync" data-cols>
        <div class="sy-row"><span>Оригинал, русский</span><span class="sy-w">''' + ''.join(f'<i data-col style="height:{h}%"></i>' for h in [30, 55, 80, 60, 35, 20, 45, 75, 95, 70, 40, 25, 50, 85, 65, 35, 20, 40, 70, 90, 60, 30, 15, 35, 60, 80, 55, 30]) + '''</span><b>0:31</b></div>
        <div class="sy-row en"><span>Перевод, английский</span><span class="sy-w">''' + ''.join(f'<i data-col style="height:{h}%"></i>' for h in [28, 50, 85, 62, 30, 22, 48, 72, 92, 66, 44, 22, 55, 80, 60, 38, 18, 45, 74, 88, 58, 26, 18, 38, 62, 78, 50, 28]) + '''</span><b>0:31</b></div>
        <div class="sy-marks"><span>Тот же тембр голоса</span><span>Паузы и темп сохранены</span><span>Губы совпадают с речью</span></div>
      </div>'''

cost = '''<div class="cost" data-bars>
        <div class="cst"><h3>Стоимость минуты</h3>
          <div class="cr"><span>Студийный дубляж</span><span class="tr"><i data-bar style="width:100%"></i></span><b>$500–2 000</b></div>
          <div class="cr ai"><span>ИИ‑перевод и озвучка</span><span class="tr"><i data-bar style="width:3%"></i></span><b>$2–20</b></div>
        </div>
        <div class="cst"><h3>Срок для часа видео</h3>
          <div class="cr"><span>Студийный дубляж</span><span class="tr"><i data-bar style="width:100%"></i></span><b>3–6 недель</b></div>
          <div class="cr ai"><span>ИИ‑перевод и озвучка</span><span class="tr"><i data-bar style="width:12%"></i></span><b>3–5 дней</b></div>
        </div>
      </div>
      <p class="note">Стоимость минуты — оценка рынка по обзору HeyGen, 2026. Сроки — наш опыт с проверкой носителем языка.</p>'''

main = '<main id="main">\n' + hero('Перевод и озвучка видео', 'Одно видео — на любом языке',
    'Переводим обучающие курсы, вебинары и рекламу с голосом вашего спикера: тот же тембр, синхронные губы, проверка носителем языка.',
    [('btn-primary', '#lead', 'Перевести пробную минуту', CHIP), ('btn-line', '#pricing', 'Смотреть тарифы', '')], hero_vis,
    [('Языки', 'более 30'), ('Час видео', 'за 3–5 дней'), ('Минута', 'от 3 000 ₽')], 'db-hero') + '\n\n' + \
    subnav([('sync', 'Голос'), ('cost', 'Сравнение'), ('uses', 'Задачи'), ('week', 'Этапы'), ('honest', 'Правила'), ('pricing', 'Тарифы'), ('faq', 'Вопросы')], 'Пробная минута', CHIP) + '\n\n' + \
    section('sync', sync, head='Голос тот же, язык другой', lead='Клонируем тембр спикера, сохраняем паузы и темп, подстраиваем движение губ.', split=True) + '\n\n' + \
    section('cost', cost, cls='band', head='В десятки раз дешевле студии') + '\n\n' + \
    section('uses', ethics([('cap', 'Обучение и онбординг', 'Курсы и инструкции для сотрудников в других странах.'),
                            ('megaphone', 'Реклама и соцсети', 'Один ролик — версии для каждого рынка.'),
                            ('video', 'Вебинары и YouTube', 'Архив выступлений работает на новую аудиторию.'),
                            ('globe', 'Выход на новые рынки', 'СНГ, Турция, Ближний Восток, Китай, Латинская Америка.')]), head='Что переводят чаще всего') + '\n\n' + \
    section('week', steps([('День 1', 'Расшифровка', 'Текст с таймкодами и глоссарий ваших терминов.'),
                           ('Дни 1–2', 'Перевод и редактура', 'Переводчик адаптирует смысл, а не слова.'),
                           ('Дни 2–4', 'Голос и губы', 'Клон голоса спикера и синхронизация губ.'),
                           ('День 5', 'Проверка носителем', 'Носитель языка слушает ролик целиком, правим мелочи.')]), cls='band', head='Как идёт работа') + '\n\n' + \
    section('honest', ethics([('sign', 'Согласие спикера', 'Голос клонируем только с письменного согласия человека.'),
                              ('tag', 'Пометка о переводе', 'В описании ролика указываем, что озвучка сделана с ИИ.'),
                              ('eye', 'Проверяет носитель', 'Каждый язык слушает живой человек, а не только модель.'),
                              ('copyright', 'Права — ваши', 'Переведённые ролики и клон голоса принадлежат вам.')]), head='Правила') + '\n\n' + \
    section('pricing', plans([
        dict(name='Ролик', price='от 9 000 ₽', small='до 3 минут, за язык', text='Для рекламы и соцсетей.', list=['Клон голоса', 'Синхронизация губ', 'Субтитры', 'Проверка носителем'], cta='Перевести ролик'),
        dict(name='Пакет', price='149 000 ₽', small='в месяц, 60 минут', text='Для вебинаров и контента.', list=['60 минут в любых языках', 'Глоссарий терминов', 'Приоритет в очереди', 'Выгрузка на площадки'], cta='Выбрать пакет', main=True, badge='Чаще выбирают'),
        dict(name='Курсы', price='от 390 000 ₽', small='проект', text='Для онлайн‑школ и корпоративного обучения.', list=['Библиотека курсов', 'Выгрузка в LMS', 'Тесты и материалы', 'Менеджер проекта'], cta='Обсудить проект')], CHIP),
        cls='band', head='Тарифы', lead='Пробная минута — бесплатно на вашем видео.', split=True) + '\n\n' + \
    section('faq', faq([
        ('Будет ли слышно, что это ИИ?', 'Современные модели передают тембр и интонации очень близко к оригиналу. Спорные места правим вручную, а носитель языка слушает ролик целиком.'),
        ('Что с движением губ?', 'Для роликов, где лицо крупно, делаем синхронизацию губ. Для вебинаров и экранных записей она не нужна — хватает голоса и субтитров.'),
        ('Какие языки доступны?', 'Более 30: английский, казахский, узбекский, турецкий, арабский, китайский, испанский, немецкий и другие. Редкие языки — по запросу.'),
        ('Можно ли перевести видео с несколькими спикерами?', 'Да, для каждого делаем отдельный голос. Нужно согласие всех, чей голос клонируем.'),
        ('Как вы работаете с терминами?', 'Собираем глоссарий до перевода и используем его во всех роликах, чтобы названия продуктов и термины звучали одинаково.')])
        + '\n      ' + next_link('knowledge', 'network', 'ИИ‑поиск по документам'), head='Вопросы') + '\n' + \
    f'<script type="application/json" id="dub-data">{json.dumps(LANGS, ensure_ascii=False)}</script>\n'

style = SERVICE_CSS + '''    .dub-hero{max-width:580px;justify-self:end;width:100%;display:grid;gap:10px}
    .dub-hero .note{margin-top:0}
    .sync{display:grid;gap:18px;padding:clamp(24px,3vw,40px);border-radius:var(--r-lg);background:#141925;color:#eef1f6}
    .sy-row{display:grid;grid-template-columns:190px 1fr 50px;gap:18px;align-items:center;font-size:15px}
    .sy-row>span:first-child{color:#a9b1c0}
    .sy-row b{font-weight:400;color:#a9b1c0;text-align:right;font-variant-numeric:tabular-nums}
    .sy-w{display:flex;align-items:center;gap:4px;height:64px}
    .sy-w i{flex:1;border-radius:3px;background:#5b6474}
    .sy-row.en .sy-w i{background:var(--bronze)}
    .sy-marks{display:flex;flex-wrap:wrap;gap:10px;padding-left:208px}
    .sy-marks span{font-size:14px;padding:8px 12px;border-radius:999px;border:1px solid rgba(255,255,255,.14);color:#dfe4ec}
    .cost{display:grid;grid-template-columns:1fr 1fr;gap:24px}
    .cst{background:var(--white);border:1px solid var(--mist);border-radius:var(--r-lg);padding:clamp(24px,3vw,36px);display:grid;gap:18px}
    .cst h3{font-size:21px;font-weight:400}
    .cr{display:grid;grid-template-columns:170px 1fr 120px;gap:14px;align-items:center;font-size:15px}
    .cr>span:first-child{color:var(--slate)}
    .cr .tr{height:12px;border-radius:6px;background:var(--porcelain-2);overflow:hidden}
    .cr .tr i{display:block;height:100%;border-radius:6px;background:var(--mist-2)}
    .cr.ai .tr i{background:var(--bronze)}
    .cr b{font-weight:500;text-align:right;white-space:nowrap}
    @media (max-width:1024px){ .dub-hero{justify-self:start} .cost{grid-template-columns:1fr} }
    @media (max-width:600px){ .sy-row{grid-template-columns:1fr;gap:6px} .sy-row b{text-align:left} .sy-marks{padding-left:0} .cr{grid-template-columns:1fr 70px;gap:6px 12px} .cr .tr{grid-column:1 / -1;grid-row:2} }
'''

script = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  const data = JSON.parse(document.getElementById('dub-data').textContent);
  const box = document.querySelector('.dub-hero'), sub = box.querySelector('.vpl-sub'), btns = [...box.querySelectorAll('.vpl-langs button')];
  const g = window.gsap, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let i = 1, auto = true;
  const set = k => {
    i = k; const [, lang, text] = data[k];
    btns.forEach((b, j) => { b.classList.toggle('on', j === k); b.setAttribute('aria-pressed', String(j === k)); });
    sub.lang = lang; sub.innerHTML = '<span></span>'; sub.firstChild.textContent = text;
    if (g && !reduce) g.fromTo(sub, { opacity: 0, y: 6 }, { opacity: 1, y: 0, duration: .45, ease: 'power2.out' });
  };
  btns.forEach((b, k) => b.addEventListener('click', () => { auto = false; set(k); }));
  if (!reduce) setInterval(() => { if (auto && !document.hidden) set((i + 1) % data.length); }, 2600);
});
</script>'''

build('ai/ugc/index.html', 'ai/dubbing/index.html',
      title='Перевод и озвучка видео голосом спикера — Social Stars AI',
      desc='Перевод обучающих курсов, вебинаров и рекламы на 30+ языков с клоном голоса спикера, синхронизацией губ и проверкой носителем языка. Час видео за 3–5 дней, минута от 3 000 ₽.',
      path='/ai/dubbing/', og_title='Одно видео — на любом языке', og_desc='Перевод и озвучка видео голосом вашего спикера.',
      ld=ld_service('Перевод и озвучка видео', '/ai/dubbing/', 9000), style=style, main=main, script=script, service=CHIP)

# ——— кампания
L = lambda: legal('Озвучка создана с ИИ.')
banners = [
 ('square-markets', 1080, 1080, 'Квадрат 1080×1080 — Telegram Ads, VK Реклама',
  f'''<div class="bn b-sq ink">{LOGO}<h3>Один ролик —<br>десять рынков</h3>
      <p class="bn-lead">Переводим видео голосом вашего спикера на 30+ языков.</p>
      <span class="bn-cta">Пробная минута</span>
      <div class="dv">{player(1, video=False, lazy=False)}</div>{L()}</div>'''),
 ('square-hello', 1080, 1080, 'Квадрат 1080×1080 — экспортёры и онлайн‑школы',
  f'''<div class="bn b-sq2">{LOGO}<h3>Hello. Merhaba.<br>Сәлем. 你好.</h3>
      <div class="dv2">{player(2, video=False, lazy=False)}</div>
      <p class="bn-lead">Тот же голос и тот же спикер — на языке ваших клиентов.</p>
      <span class="bn-cta">Смотреть тарифы</span>{L()}</div>'''),
 ('story-language', 1080, 1920, 'Вертикаль 1080×1920 — истории и клипы',
  f'''<div class="bn b-st ink">{LOGO}<h3>Говорите<br>с клиентами<br>на их языке</h3>
      <div class="dv3">{player(5, video=False, lazy=False)}</div>
      <p class="bn-lead">Курсы, вебинары и реклама — с голосом вашего спикера и проверкой носителем.</p>
      <span class="bn-cta">Перевести пробную минуту</span>{L()}</div>'''),
 ('wide-voice', 1200, 628, 'Горизонталь 1200×628 — Яндекс РСЯ, VK Реклама',
  f'''<div class="bn b-wd">{LOGO}<h3>Переведём видео<br>вашим голосом</h3>
      <p class="bn-lead">30+ языков, час видео за 3–5 дней.</p>
      <span class="bn-cta">Пробная минута</span>
      <div class="dv4">{player(6, video=False, lazy=False)}</div>{L()}</div>'''),
]
banner_css = '''    .b-sq h3{font-size:110px}
    .b-sq .bn-lead{top:470px;width:420px}
    .b-sq .bn-cta{top:700px}
    .b-sq .dv{position:absolute;right:48px;top:470px;width:520px}
    .b-sq2 h3{font-size:92px}
    .b-sq2 .dv2{position:absolute;left:64px;top:420px;width:600px}
    .b-sq2 .bn-lead{left:700px;top:430px;width:320px;font-size:30px}
    .b-sq2 .bn-cta{left:700px;top:700px}
    .b-st h3{font-size:128px;top:250px}
    .b-st .dv3{position:absolute;left:80px;right:80px;top:760px}
    .b-st .bn-lead{top:1500px;width:900px;font-size:40px}
    .b-st .bn-cta{top:1690px}
    .b-wd h3{font-size:56px}
    .b-wd .bn-lead{top:320px}
    .b-wd .dv4{position:absolute;right:44px;top:100px;width:500px}
'''
campaign('dubbing', service_name='Перевод и озвучка видео', camp_name='Один ролик — десять рынков',
  lead='Запуск перевода и озвучки видео для экспортёров, онлайн‑школ и брендов: идея, креативы, сценарии роликов и медиаплан на 6 недель.',
  facts=[('Цель', '18 договоров за 6 недель'), ('Аудитория', 'экспорт, онлайн‑образование, бренды'), ('Бюджет', '450 000 ₽ — пример')],
  brief=[('Инсайт', 'Компании выходят на рынки СНГ, Турции и Ближнего Востока, а весь видеоконтент — только на русском. Студийный дубляж стоит как новый ролик.'),
         ('Идея', 'Один ролик — десять рынков: снимаете один раз, говорите на всех языках своих клиентов.'),
         ('Обещание', 'Пробная минута бесплатно на вашем видео, час видео — за 3–5 дней.'),
         ('Почему верить', 'Клон голоса вашего спикера, синхронизация губ, проверка носителем каждого языка.'),
         ('Тон', 'Уверенно и конкретно: языки, сроки, рынки. Кампания сама звучит на нескольких языках.')],
  msgs=[('Один ролик — десять рынков', 'главный — все каналы'), ('Hello. Merhaba. Сәлем. 你好', 'экспортёры: Telegram, VK'),
        ('Говорите с клиентами на их языке', 'истории и клипы'), ('Переведём видео вашим голосом', 'РСЯ, ретаргетинг'),
        ('Ваш курс уже готов для Казахстана', 'онлайн‑школы, посевы')],
  banners=banners, banner_css=banner_css,
  scripts=[('«Один ролик» · 20 секунд', [('0–5 с', 'Спикер в кадре говорит по‑русски.', '«Примерка — бесплатно до пятницы»'),
                                        ('5–15 с', 'Та же фраза тем же голосом: английский, турецкий, казахский, арабский — быстрые склейки.', 'Титры языков сменяются по кругу'),
                                        ('15–20 с', 'Карта с отмеченными странами, логотип.', '«Один ролик — десять рынков. Social Stars AI»')]),
           ('«Курс» · 15 секунд', [('0–4 с', 'Экран онлайн‑курса, 40 уроков на русском.', '«40 уроков. Один язык»'),
                                  ('4–11 с', 'Переключатель языков, уроки меняют подписи и голос.', '«Переводим голосом вашего преподавателя за неделю»'),
                                  ('11–15 с', 'Логотип и кнопка.', '«Пробная минута — бесплатно»')])],
  media=[('Telegram Ads', 'каналы об экспорте, ВЭД и онлайн‑образовании', 'квадрат, текст', 25, 'цена клика'),
         ('Яндекс Директ', 'поиск: «перевод видео на английский», «озвучка видео ИИ», «локализация курса»; РСЯ', 'текст + горизонталь', 30, 'цена заявки'),
         ('VK Реклама', 'владельцы онлайн‑школ, экспортёры, маркетологи брендов', 'квадрат, вертикальное видео', 20, 'цена заявки'),
         ('Посевы', 'сообщества экспортёров и EdTech', 'пост + ролик «Один ролик»', 15, 'переходы'),
         ('Ретаргетинг', 'посетители страницы и тарифов', 'горизонталь «Вашим голосом»', 10, 'возврат на пробную минуту')],
  budget=450000, funnel=[('Бюджет', '450 000 ₽', 100), ('Заявки', '180', 100), ('Пробные минуты', '60', 33), ('Договоры', '18', 10)],
  kpis=[('Цена заявки', 'до 2 500 ₽'), ('Заявка → пробная минута', '33%'), ('Пробная минута → договор', '30%')],
  cal=[('Подготовка: креативы, ролики на 4 языках, маркировка', 1, 1), ('Посевы в сообществах экспортёров', 2, 3), ('Telegram Ads и VK Реклама', 2, 6), ('Яндекс Директ: поиск и РСЯ', 2, 6), ('Ретаргетинг', 3, 6), ('Замена креативов по данным', 3, 6), ('Итоги и решение о масштабе', 6, 6)],
  utm_sources='telegram, yandex, vk, seeding', utm_content=['dubbing_2026', 'markets', 'hello', 'language', 'voice'])
