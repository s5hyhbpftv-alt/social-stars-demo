import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import *

CHIP = 'Карточки для маркетплейсов'
NAME = 'ИИ‑фотостудия для маркетплейсов'
M = lambda *a, **k: mcard(*a, **k)

shelf = ('<div class="shelf" role="img" aria-label="Карточки товаров с ИИ-моделями: платья и шуба в разных сценах">'
         + M('m65', ['Посадка по фигуре', 'Размеры 40–54'], '4 990 ₽', '6 490 ₽', 'Платье‑футляр, красное')
         + M('m80', ['Открытые плечи', 'Не мнётся'], '5 790 ₽', '', 'Платье вечернее, изумрудное')
         + M('m5', ['Контрастные вставки', 'Длина миди'], '6 290 ₽', '7 900 ₽', 'Платье офисное, синее')
         + M('m77', ['Натуральный мех', 'Чистка в подарок'], '48 900 ₽', '', 'Шуба из меха норки')
         + '</div>')

def scene(pair, labels, chips, price, name):
    a, b = pair
    return f'''<div class="scene" data-scene>
          <div class="mcard"><div class="mc-in"><div class="mc-ph"><img src="{IMG}{a}.webp" alt="" loading="lazy" class="on" /><img src="{IMG}{b}.webp" alt="" loading="lazy" />
          <div class="mc-chips">{"".join(f"<span>{c}</span>" for c in chips)}</div><span class="mc-tag">ИИ‑модель</span></div>
          <p class="mc-price">{price}</p><p class="mc-name">{name}</p></div></div>
          <div class="seg" role="group" aria-label="Сцена"><button type="button" aria-pressed="true">{labels[0]}</button><button type="button" aria-pressed="false">{labels[1]}</button></div>
        </div>'''

scenes = '<div class="scenes">' + scene(('m65', 'm35'), ('Ателье', 'Причал'), ['Посадка по фигуре'], '4 990 ₽', 'Платье‑футляр, красное') + scene(('m80', 'm37'), ('За столом', 'В мастерской'), ['Открытые плечи'], '5 790 ₽', 'Платье вечернее, изумрудное') + '</div>'

anatomy = f'''<div class="anat" data-wires="l1>c:h l2>c:h c>r1:h c>r2:h">
        <div class="anat-col">
          <div class="call-out" data-n="l1"><b>Товар крупно и в сцене</b><span>Покупатель за секунду понимает, что это и для какого случая.</span></div>
          <div class="call-out" data-n="l2"><b>Три выгоды на фото</b><span>Инфографика отвечает на главные вопросы до клика.</span></div>
        </div>
        <div class="anat-card" data-n="c">{M('m80', ['Открытые плечи', 'Не мнётся', 'Размеры 40–54'], '5 790 ₽', '7 200 ₽', 'Платье вечернее, изумрудное, миди')}</div>
        <div class="anat-col">
          <div class="call-out" data-n="r1"><b>Название с ключевыми словами</b><span>Так карточку находит поиск маркетплейса.</span></div>
          <div class="call-out" data-n="r2"><b>8–12 кадров</b><span>Посадка, детали, ткань и таблица размеров.</span></div>
        </div>
      </div>'''

ab = f'''<div class="ab" data-bars>
        <figure>{M('m65', ['Посадка по фигуре'], '4 990 ₽', '', 'Вариант А: ателье')}<figcaption><span>Кликабельность</span><span class="tr"><i data-bar style="width:62%"></i></span><b data-count>3,1%</b></figcaption></figure>
        <figure class="win">{M('m35', ['Посадка по фигуре'], '4 990 ₽', '', 'Вариант Б: причал')}<figcaption><span>Кликабельность</span><span class="tr"><i data-bar style="width:92%"></i></span><b data-count>4,6%</b></figcaption></figure>
        <div class="ab-t"><h3>Оставляем то фото, на которое кликают</h3><p>Каждую неделю меняем главное фото и сравниваем кликабельность в выдаче. Цифры на примере условные — реальные вы увидите в отчёте.</p></div>
      </div>'''

main = '<main id="main">\n' + hero('Фотостудия для маркетплейсов', 'Снято без съёмки',
    'Карточки для Wildberries, Ozon и Яндекс Маркета: товар на ИИ‑модели, в нужной сцене, с инфографикой и текстом. Без студии, фотографа и аренды.',
    [('btn-primary', '#lead', '3 тестовые карточки', CHIP), ('btn-line', '#pricing', 'Смотреть тарифы', '')], shelf,
    [('Карточка', 'от 2 900 ₽'), ('Тестовые карточки', 'за 48 часов'), ('Сцены и модели', 'под вашу аудиторию')], 'mk-hero') + '\n\n' + \
    subnav([('scene', 'Сцены'), ('anatomy', 'Карточка'), ('ab', 'A/B‑тест'), ('week', 'Этапы'), ('honest', 'Правила'), ('pricing', 'Тарифы'), ('faq', 'Вопросы')], '3 тестовые карточки', CHIP) + '\n\n' + \
    section('scene', scenes + '\n      <p class="note">Кадры сгенерированы ИИ для нашего проекта сети ателье «Пчёлка»: одно и то же платье в разных сценах.</p>', head='Одна вещь — любая сцена', lead='Фото товара с телефона превращаем в кадры на модели: ателье, улица, отпуск, вечер.', split=True) + '\n\n' + \
    section('anatomy', anatomy, cls='band', head='Из чего состоит карточка, которая продаёт') + '\n\n' + \
    section('ab', ab, head='Главное фото решает клик') + '\n\n' + \
    section('week', steps([('День 1', 'Бриф и фото товара', 'Хватит снимков на телефон на ровном фоне или манекене.'),
                           ('Дни 2–3', 'Модели и сцены', 'Подбираем типаж и локации под вашу аудиторию.'),
                           ('Дни 3–4', 'Инфографика и тексты', 'Выгоды, размеры, название и описание для поиска.'),
                           ('Каждую неделю', 'Загрузка и A/B', 'Меняем главное фото и оставляем лучшее.')]), cls='band', head='Как идёт работа') + '\n\n' + \
    section('honest', ethics([('eye', 'Товар как в жизни', 'Цвет, фасон и детали сверяем с фото товара — без приукрашивания.'),
                              ('user', 'Модели — ИИ‑персонажи', 'Лица не принадлежат реальным людям, права на образы — у нас.'),
                              ('shield', 'Правила площадок', 'Следим за требованиями Wildberries, Ozon и Яндекс Маркета к фото.'),
                              ('copyright', 'Права — ваши', 'Изображения и тексты передаём по договору.')]), head='Честно для покупателя') + '\n\n' + \
    section('pricing', plans([
        dict(name='Карточка', price='2 900 ₽', small='за товар', text='Чтобы проверить подход.', list=['До 8 кадров на модели', 'Инфографика', 'Название и описание', 'Готово за 48 часов'], cta='Заказать карточки'),
        dict(name='Подписка', price='89 000 ₽', small='в месяц', text='Для постоянного ассортимента.', list=['40 карточек в месяц', 'A/B главного фото', 'Сезонные сцены', 'Отчёт по кликабельности'], cta='Выбрать подписку', main=True, badge='Чаще выбирают'),
        dict(name='Бренд', price='от 190 000 ₽', small='в месяц', text='Для брендов одежды и крупных селлеров.', list=['От 100 карточек в месяц', 'Своя ИИ‑модель бренда', 'Лукбуки и баннеры', 'Выделенный арт‑директор'], cta='Обсудить «Бренд»')], CHIP),
        cls='band', head='Тарифы', lead='Первые 3 карточки — тестовые: покажем подход на ваших товарах.', split=True) + '\n\n' + \
    section('faq', faq([
        ('Маркетплейсы разрешают фото с ИИ-моделями?', 'Да, если изображение соответствует товару и не вводит покупателя в заблуждение. Мы сверяем каждый кадр с реальным товаром и следим за правилами площадок.'),
        ('Нужна ли профессиональная съёмка товара?', 'Нет. Достаточно фото на телефон при дневном свете: на ровном фоне, на вешалке или манекене. Для одежды — ещё фото деталей и бирки с составом.'),
        ('Как вы передаёте посадку одежды?', 'Опираемся на ваши фото и замеры. Если посадка на кадре отличается от реальной, переделываем кадр — это входит в работу.'),
        ('Можно ли одну модель на весь магазин?', 'Да. В тарифе «Бренд» создаём постоянную ИИ‑модель — узнаваемое лицо вашего магазина во всех карточках.'),
        ('Какие категории подходят?', 'Одежда, обувь, аксессуары, товары для дома, косметика, детские товары. Для техники и крупных товаров делаем сцены в интерьере.')])
        + '\n      ' + next_link('voice', 'network', 'Голосовой ИИ‑оператор'), head='Вопросы') + '\n'

style = SERVICE_CSS + '''    .shelf{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:520px;justify-self:end;width:100%}
    .shelf .mcard:nth-child(2){transform:translateY(34px)}
    .shelf .mcard:nth-child(4){transform:translateY(34px)}
    .mc-ph .scan{position:absolute;left:0;right:0;top:0;height:2px;background:var(--bronze);box-shadow:0 0 18px 4px rgba(176,138,99,.55);opacity:0;z-index:3}
    .scenes{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,56px);max-width:860px}
    .scene{display:grid;gap:16px;justify-items:start}
    .scene .mc-ph img{position:absolute;inset:0;opacity:0;transition:opacity .6s var(--ease)}
    .scene .mc-ph img.on{opacity:1}
    .scene .mc-chips,.scene .mc-tag{z-index:2}
    .seg{display:inline-flex;padding:4px;border-radius:999px;background:var(--porcelain-2)}
    .seg button{border:0;background:none;font:500 14.5px var(--font);padding:9px 16px;border-radius:999px;color:var(--slate);cursor:pointer}
    .seg button[aria-pressed="true"]{background:var(--white);color:var(--ink);box-shadow:0 2px 8px -4px rgba(17,21,31,.3)}
    .anat{display:grid;grid-template-columns:1fr minmax(240px,340px) 1fr;gap:clamp(40px,6vw,96px);align-items:center}
    .anat-col{display:grid;gap:clamp(48px,8vw,120px)}
    .anat-col:last-child .call-out{text-align:left}
    .anat-col:first-child .call-out{text-align:right}
    .call-out{display:grid;gap:6px;padding:18px 20px;border-radius:var(--r-md);background:var(--white);border:1px solid var(--mist)}
    .call-out b{font-weight:500;font-size:17px}
    .call-out span{color:var(--slate);font-size:15px}
    .ab{display:grid;grid-template-columns:260px 260px 1fr;gap:clamp(24px,4vw,48px);align-items:end}
    .ab figure{margin:0;display:grid;gap:14px}
    .ab figcaption{display:grid;grid-template-columns:1fr 60px;gap:6px 12px;align-items:center;font-size:14px;color:var(--slate)}
    .ab figcaption .tr{grid-column:1;height:8px;border-radius:4px;background:var(--porcelain-2);overflow:hidden}
    .ab figcaption .tr i{display:block;height:100%;background:var(--mist-2);border-radius:4px}
    .ab .win figcaption .tr i{background:var(--bronze)}
    .ab figcaption b{grid-row:1 / span 2;grid-column:2;font-size:22px;font-weight:400;color:var(--ink);text-align:right}
    .ab .win .mc-in{box-shadow:0 0 0 2px var(--bronze),0 30px 60px -40px rgba(17,21,31,.45)}
    .ab-t h3{font-size:clamp(22px,2.2vw,28px);font-weight:300;letter-spacing:-.02em;margin-bottom:12px}
    .ab-t p{color:var(--slate)}
    @media (max-width:1024px){ .shelf{justify-self:start;max-width:440px} .anat{grid-template-columns:1fr} .anat .wires{display:none} .anat-card{max-width:340px} .anat-col:first-child .call-out{text-align:left} .anat-col{gap:14px} .ab{grid-template-columns:1fr 1fr} .ab-t{grid-column:1 / -1} }
    @media (max-width:600px){ .scenes{grid-template-columns:1fr} .scene .mcard{max-width:320px} .shelf{gap:10px} .ab{gap:14px} .ab figcaption b{font-size:18px} }
'''

script = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  const g = window.gsap, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // одна вещь — любая сцена
  document.querySelectorAll('[data-scene]').forEach(sc => {
    const imgs = sc.querySelectorAll('.mc-ph img'), btns = sc.querySelectorAll('.seg button');
    btns.forEach((b, i) => b.addEventListener('click', () => {
      btns.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      imgs.forEach((im, j) => im.classList.toggle('on', i === j));
    }));
  });
  // витрина: кадры «проявляются», как при генерации
  const cards = [...document.querySelectorAll('.shelf .mc-ph')];
  if (!g || reduce || !cards.length) return;
  cards.forEach(c => { const s = document.createElement('i'); s.className = 'scan'; c.appendChild(s); });
  const gen = (c, delay = 0) => {
    const img = c.querySelector('img'), scan = c.querySelector('.scan'), chips = c.querySelectorAll('.mc-chips span, .mc-tag');
    const tl = g.timeline({ delay });
    tl.set(img, { filter: 'blur(14px) saturate(.2) brightness(1.08)' }).set(chips, { opacity: 0, y: 6 })
      .fromTo(scan, { top: '0%', opacity: 1 }, { top: '100%', duration: 1.3, ease: 'power2.inOut' })
      .to(img, { filter: 'blur(0px) saturate(1) brightness(1)', duration: 1.3, ease: 'power2.inOut' }, '<')
      .to(scan, { opacity: 0, duration: .25 }, '>-.1')
      .to(chips, { opacity: 1, y: 0, duration: .5, stagger: .08, ease: 'power2.out' }, '>-.2');
    return tl;
  };
  cards.forEach((c, i) => gen(c, .3 + i * .45));
  let k = 0;
  setInterval(() => { if (!document.hidden) gen(cards[k++ % cards.length]); }, 4200);
});
</script>'''

build('ai/ugc/index.html', 'ai/marketplace/index.html',
      title='ИИ-фотостудия для маркетплейсов: карточки с ИИ-моделями — Social Stars AI',
      desc='Карточки товаров для Wildberries, Ozon и Яндекс Маркета: товар на ИИ-модели в нужной сцене, инфографика, тексты и A/B главного фото. От 2 900 ₽ за карточку, подписка от 89 000 ₽ в месяц.',
      path='/ai/marketplace/', og_title='Снято без съёмки — ИИ-фотостудия для маркетплейсов', og_desc='Товар на ИИ-модели в любой сцене — без студии и фотографа.',
      ld=ld_service('ИИ-фотостудия для маркетплейсов', '/ai/marketplace/', 2900), style=style, main=main, script=script, service=CHIP)

# ——— кампания
L = lambda: legal('Изображения созданы с ИИ‑моделями.')
banners = [
 ('square-shot', 1080, 1080, 'Квадрат 1080×1080 — Telegram Ads, VK Реклама',
  f'''<div class="bn b-sq ink">{LOGO}<h3>Снято<br>без съёмки</h3>
      <p class="bn-lead">Карточки для Wildberries и Ozon: товар на ИИ‑модели в любой сцене.</p>
      <span class="bn-cta">3 тестовые карточки</span>
      <div class="cards2">{M("m65", ["Посадка по фигуре"], "4 990 ₽", "", "Платье‑футляр", lazy=False)}{M("m35", ["Посадка по фигуре"], "4 990 ₽", "", "То же платье, другая сцена", lazy=False)}</div>{L()}</div>'''),
 ('square-click', 1080, 1080, 'Квадрат 1080×1080 — вариант для селлеров, которые уже продают',
  f'''<div class="bn b-sq2">{LOGO}<h3>Главное фото<br>решает клик</h3>
      <div class="abv"><div>{M("m65", ["Посадка по фигуре"], "4 990 ₽", "", "Вариант А", lazy=False)}<span>Вариант А</span></div><div class="w">{M("m35", ["Посадка по фигуре"], "4 990 ₽", "", "Вариант Б", lazy=False)}<span>Вариант Б — оставляем</span></div></div>
      <p class="bn-lead">Меняем главное фото каждую неделю и оставляем то, на которое кликают.</p>
      <span class="bn-cta">Узнать подробнее</span>{L()}</div>'''),
 ('story-collection', 1080, 1920, 'Вертикаль 1080×1920 — истории и клипы',
  f'''<div class="bn b-st">{LOGO}<h3>Коллекция<br>на модели —<br>к утру</h3>
      <div class="grid4">{"".join(M(i, [c], p, "", n, lazy=False) for i, c, p, n in [("m80", "Не мнётся", "5 790 ₽", "Платье вечернее"), ("m5", "Длина миди", "6 290 ₽", "Платье офисное"), ("m77", "Натуральный мех", "48 900 ₽", "Шуба")])}</div>
      <p class="bn-lead">Фото товара с телефона — карточки на модели за 48 часов.</p>
      <span class="bn-cta">3 тестовые карточки за 48 часов</span>{L()}</div>'''),
 ('wide-scene', 1200, 628, 'Горизонталь 1200×628 — Яндекс РСЯ, VK Реклама',
  f'''<div class="bn b-wd ink">{LOGO}<h3>Одно платье —<br>любая сцена</h3>
      <p class="bn-lead">Фото товара с телефона превращаем в карточки на модели.</p>
      <span class="bn-cta">3 тестовые карточки</span>
      <div class="pair">{M("m65", [], "4 990 ₽", "", "Ателье", lazy=False)}{M("m35", [], "4 990 ₽", "", "Причал", lazy=False)}</div>{L()}</div>'''),
]
banner_css = '''    .b-sq h3{font-size:124px}
    .b-sq .cards2{position:absolute;right:40px;top:430px;width:520px;height:600px}
    .b-sq .cards2 .mcard{position:absolute;width:250px}
    .b-sq .cards2 .mcard:first-child{left:10px;top:40px;transform:rotate(-6deg)}
    .b-sq .cards2 .mcard:last-child{left:240px;top:0;transform:rotate(5deg)}
    .b-sq2 h3{font-size:84px}
    .b-sq2 .abv{position:absolute;left:64px;top:400px;display:flex;gap:36px}
    .b-sq2 .abv>div{width:250px;display:grid;gap:12px;font-size:24px;color:var(--slate)}
    .b-sq2 .abv .w span{color:var(--bronze-2);font-weight:500}
    .b-sq2 .abv .w .mc-in{box-shadow:0 0 0 4px var(--bronze),0 30px 60px -40px rgba(17,21,31,.45)}
    .b-sq2 .bn-lead{left:640px;top:440px;width:380px;font-size:32px}
    .b-sq2 .bn-cta{left:640px;top:720px}
    .b-st h3{font-size:128px;top:240px}
    .b-st .grid4{position:absolute;left:80px;right:80px;top:720px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
    .b-st .grid4 .mcard{width:100%}
    .b-st .bn-lead{top:1290px;width:900px;font-size:44px}
    .b-st .bn-cta{top:1560px}
    .b-wd .pair{position:absolute;right:48px;top:40px;display:flex;gap:22px}
    .b-wd .pair .mcard{width:210px}
    .b-wd .pair .mcard:first-child{transform:rotate(-4deg) translateY(20px)}
    .b-wd .pair .mcard:last-child{transform:rotate(4deg)}
'''
campaign('marketplace', service_name='Фотостудия для маркетплейсов', camp_name='Снято без съёмки',
  lead='Запуск ИИ‑фотостудии для селлеров Wildberries, Ozon и Яндекс Маркета: идея, креативы, сценарии роликов и медиаплан на 6 недель.',
  facts=[('Цель', '25 подписок за 6 недель'), ('Аудитория', 'селлеры одежды и товаров для дома'), ('Бюджет', '500 000 ₽ — пример')],
  brief=[('Инсайт', 'Селлер хочет выпускать новые товары быстрее конкурентов, а студийная съёмка — это неделя и бюджет на каждую партию.'),
         ('Идея', 'Снято без съёмки: товар на модели в любой сцене — к утру, без студии и фотографа.'),
         ('Обещание', 'Три тестовые карточки на ваших товарах за 48 часов.'),
         ('Почему верить', 'Собственные ИИ‑модели, 12 лет Social Stars в визуальном контенте, A/B главного фото в каждой подписке.'),
         ('Тон', 'Языком селлера: карточка, выдача, клик, выкуп. Без магии — показываем кадры.')],
  msgs=[('Снято без съёмки', 'главный — все каналы'), ('Главное фото решает клик', 'для селлеров с продажами: VK, РСЯ'),
        ('Коллекция на модели — к утру', 'истории и клипы'), ('Одно платье — любая сцена', 'РСЯ, ретаргетинг'),
        ('Фотограф в отпуске. Карточки готовы', 'посевы в чатах селлеров')],
  banners=banners, banner_css=banner_css,
  scripts=[('«Было — стало» · 15 секунд', [('0–3 с', 'Платье на вешалке, снято на телефон.', '«Это фото товара с телефона»'),
                                           ('3–9 с', 'Кадр «проявляется»: то же платье на модели в ателье, потом на причале.', '«А это — карточка для маркетплейса. Без студии и фотографа»'),
                                           ('9–15 с', 'Карточка с инфографикой в выдаче, логотип.', '«Три тестовые карточки за 48 часов. Ссылка ниже»')]),
           ('«Выдача» · 15 секунд', [('0–4 с', 'Экран поиска: ряд одинаковых серых карточек.', '«Покупатель листает выдачу. На чём он остановится?»'),
                                    ('4–11 с', 'Одна карточка оживает: модель, сцена, три выгоды.', '«Главное фото решает клик. Мы меняем его каждую неделю и оставляем лучшее»'),
                                    ('11–15 с', 'Логотип и кнопка.', '«ИИ‑фотостудия Social Stars AI»')])],
  media=[('Telegram Ads', 'каналы для селлеров Wildberries и Ozon', 'квадрат, текст 160 знаков', 30, 'цена клика'),
         ('Яндекс Директ', 'поиск: «фото для вайлдберриз», «карточки товаров заказать», «инфографика для озон»; РСЯ', 'текст + горизонталь', 25, 'цена заявки'),
         ('VK Реклама', 'сообщества селлеров, похожие аудитории', 'квадрат, вертикальное видео', 20, 'цена заявки'),
         ('Посевы', 'авторы и чаты о маркетплейсах', 'нативный пост + ролик «Было — стало»', 15, 'переходы'),
         ('Ретаргетинг', 'посетители страницы и тарифов', 'квадрат «Главное фото решает клик»', 10, 'возврат на тест')],
  budget=500000, funnel=[('Бюджет', '500 000 ₽', 100), ('Заявки', '250', 100), ('Тестовые карточки', '75', 30), ('Подписки', '25', 10)],
  kpis=[('Цена заявки', 'до 2 000 ₽'), ('Заявка → тест', '30%'), ('Тест → подписка', '33%')],
  cal=[('Подготовка: креативы, маркировка, UTM', 1, 1), ('Посевы в чатах и каналах селлеров', 2, 3), ('Telegram Ads и VK Реклама', 2, 6), ('Яндекс Директ: поиск и РСЯ', 2, 6), ('Ретаргетинг', 3, 6), ('Замена креативов по данным', 3, 6), ('Итоги и решение о масштабе', 6, 6)],
  utm_sources='telegram, vk, yandex, seeding', utm_content=['shot_2026', 'shot', 'click', 'collection', 'scene'])
