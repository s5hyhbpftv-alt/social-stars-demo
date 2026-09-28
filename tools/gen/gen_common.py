# Общие функции генераторов страниц направлений и их рекламных кампаний.
# Страница собирается на основе ai/ugc/index.html (шапка, партиалы, скрипты), содержимое <main> и стили — из генератора.
# Запуск из корня репозитория: python3 tools/gen/gen_voice.py — затем python3 tools/include.py и проверки.
import re, json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
BASE = 'https://s5hyhbpftv-alt.github.io/social-stars-demo'
IMG = '/social-stars-demo/ai/img/ugc/'
NB = ' '


def money(n):
    return f'{n:,}'.replace(',', NB) + NB + '₽'


def build(template, out, *, title, desc, path, og_title, og_desc, ld, style, main, script='', service=None, extra_css=None):
    s = open(R + template).read()
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{title}</title>', s)
    s = re.sub(r'<meta name="description" content="[^"]*" />', lambda m: f'<meta name="description" content="{desc}" />', s)
    s = re.sub(r'<link rel="canonical" href="[^"]*" />', lambda m: f'<link rel="canonical" href="{BASE}{path}" />', s)
    s = re.sub(r'<meta property="og:url" content="[^"]*" />', lambda m: f'<meta property="og:url" content="{BASE}{path}" />', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*" />', lambda m: f'<meta property="og:title" content="{og_title}" />', s)
    s = re.sub(r'<meta property="og:description" content="[^"]*" />', lambda m: f'<meta property="og:description" content="{og_desc}" />', s)
    s = re.sub(r'  <script type="application/ld\+json">.*?</script>\n', '', s, flags=re.S)
    if ld:
        s = s.replace('  <link rel="stylesheet" href="/social-stars-demo/ai/ai.css" />',
                      '  <script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n  <link rel="stylesheet" href="/social-stars-demo/ai/ai.css" />', 1)
    s = re.sub(r'  <style>.*?</style>', lambda m: '  <style>\n' + style.strip('\n') + '\n  </style>', s, count=1, flags=re.S)
    if service:
        s = re.sub(r'<body data-service="[^"]*">', f'<body data-service="{service}">', s)
    a = s.index('<main id="main">'); b = s.index('<!-- @cta -->')
    s = s[:a] + main.strip('\n') + '\n\n' + s[b:]
    a = s.index('<!-- /@scripts -->') + len('<!-- /@scripts -->'); b = s.index('</body>')
    s = s[:a] + ('\n' + script.strip('\n') + '\n' if script else '\n') + s[b:]
    os.makedirs(os.path.dirname(R + out), exist_ok=True)
    open(R + out, 'w').write(s)
    print('wrote', out, len(s))


def ld_service(name, path, price):
    return {"@context": "https://schema.org", "@graph": [{"@type": "Service", "name": name, "url": BASE + path, "areaServed": "RU",
            "provider": {"@type": "Organization", "name": "Social Stars", "url": BASE + '/'},
            "offers": {"@type": "Offer", "price": str(price), "priceCurrency": "RUB"}}]}


def icon(name):
    return f'<svg class="ic"><use href="#i-{name}"/></svg>'


# ——— компоненты
def mcard(img, chips, price, old, name, tag='ИИ‑модель', lazy=True):
    ch = ''.join(f'<span>{c}</span>' for c in chips)
    lz = ' loading="lazy"' if lazy else ''
    return (f'<div class="mcard"><div class="mc-in"><div class="mc-ph"><img src="{IMG}{img}.webp" alt=""{lz} decoding="async" />'
            f'<div class="mc-chips">{ch}</div><span class="mc-tag">{tag}</span></div>'
            f'<p class="mc-price">{price}{f"<s>{old}</s>" if old else ""}</p><p class="mc-name">{name}</p></div></div>')


def call_ui(bubbles, title='Входящий звонок', t='00:00', bars=36, static=False, names=('ИИ‑оператор', 'Клиент')):
    import math
    wave = ''.join(f'<i style="transform:scaleY({.25 + .7 * abs(math.sin(i * 1.7) * math.cos(i * .45)):.2f})"></i>' for i in range(bars)) if static else '<i></i>' * bars
    log = ''.join(f'<p class="b {w}"><small>{names[0] if w == "ai" else names[1]}</small>{txt}</p>' for w, txt in bubbles)
    return (f'<div class="call"><div class="call-in"><div class="call-top"><span class="call-dot"></span><b>{title}</b><span class="call-t">{t}</span></div>'
            f'<div class="call-wave" aria-hidden="true">{wave}</div><div class="call-log">{log}</div></div></div>')


def crm(rows, status='Заявка создана'):
    dl = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in rows)
    return f'<div class="crm"><div class="crm-in"><h4>{icon("inbox")}Карточка в CRM</h4><dl>{dl}</dl><span class="crm-st">{status}</span></div></div>'


def persona(img, name, role, tags, lazy=True):
    tg = ''.join(f'<span class="{"ai" if i == 0 else ""}">{t}</span>' for i, t in enumerate(tags))
    lz = ' loading="lazy"' if lazy else ''
    return (f'<div class="persona"><div class="ps-in"><div class="ps-head"><img src="{IMG}{img}.webp" alt=""{lz} decoding="async" />'
            f'<div><b>{name}</b><span>{role}</span></div></div><div class="ps-tags">{tg}</div></div></div>')


def skills(rows):
    return '<div class="skills" data-bars>' + ''.join(
        f'<div class="sk{" lo" if v < 70 else ""}"><span>{n}</span><span class="tr"><i style="width:{v}%"></i></span><b data-count>{v}</b></div>' for n, v in rows) + '</div>'


def plans(items, chip):
    out = []
    for p in items:
        badge = f'<span class="badge">{p["badge"]}</span>' if p.get('badge') else ''
        lis = ''.join(f'<li>{x}</li>' for x in p['list'])
        btn = 'btn-primary' if p.get('main') else 'btn-line'
        out.append(f'''        <article class="plan{' main' if p.get('main') else ''}">
          {badge}<h3>{p["name"]}</h3>
          <div class="price">{p["price"]}<small>{p["small"]}</small></div>
          <p>{p["text"]}</p>
          <ul>{lis}</ul>
          <a class="btn {btn}" href="#lead" data-pick="{chip}">{p["cta"]}</a>
        </article>''')
    return '<div class="plans">\n' + '\n'.join(out) + '\n      </div>'


def faq(items):
    return '<div class="faq">\n' + '\n'.join(f'        <details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in items) + '\n      </div>'


def steps(items):
    return '<ol class="steps">\n' + '\n'.join(f'        <li><span class="when">{w}</span><h3>{h}</h3><p>{p}</p></li>' for w, h, p in items) + '\n      </ol>'


def ethics(items):
    return '<div class="ethics">\n' + '\n'.join(f'        <div><span class="ic-box" aria-hidden="true">{icon(i)}</span><h3>{h}</h3><p>{p}</p></div>' for i, h, p in items) + '\n      </div>'


def next_link(href, sky, name):
    return (f'<a class="next" href="/social-stars-demo/ai/{href}/" style="margin-top:clamp(64px,8vw,112px)"><span class="mini" data-sky="{sky}" data-sky-mini data-sky-scale=".95" aria-hidden="true"></span>'
            f'<span>Следующее направление</span><strong>{name}</strong></a>')


def hero(crumb, h1, lead, actions, visual, facts, cls=''):
    acts = ''.join(f'<a class="btn {c}" href="{h}"{" data-pick=" + chr(34) + p + chr(34) if p else ""}>{t}</a>' for c, h, t, p in actions)
    fc = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in facts)
    return f'''  <section class="hero {cls}">
    <div class="wrap">
      <div class="hero-text">
        <nav class="crumbs" aria-label="Вы здесь"><a href="/social-stars-demo/ai/">Social Stars AI</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
        <h1 class="t-hero">{h1}</h1>
        <p class="t-lead">{lead}</p>
        <div class="hero-actions">{acts}</div>
      </div>
      {visual}
    </div>
    <div class="wrap hero-facts">
      <dl class="facts">{fc}</dl>
    </div>
  </section>'''


def subnav(links, cta, chip):
    a = ''.join(f'<a href="#{i}">{t}</a>' for i, t in links)
    return f'''  <nav class="subnav" aria-label="Разделы страницы">
    <div class="wrap">{a}<a class="btn btn-ink" href="#lead" data-pick="{chip}">{cta}</a></div>
  </nav>'''


def section(id_, inner, cls='', head=None, lead=None, split=False):
    h = ''
    if head:
        h = f'<div class="head{" split" if split else ""}"><h2 class="t-h2">{head}</h2>' + (f'<p class="t-lead">{lead}</p>' if lead else '') + '</div>'
    return f'''  <section class="section{(" " + cls) if cls else ""}" id="{id_}">
    <div class="wrap">
      {h}
      {inner}
    </div>
  </section>'''


def demo(id_, media, title, text, points, tag='ИИ‑модель', label='', cls=''):
    """Пример на практике: вертикальный кадр (видео .mp4 или картинка) + сценарий."""
    src = f'/social-stars-demo/ai/video/{media}' if media.endswith('.mp4') else f'{IMG}{media}'
    if media.endswith('.mp4'):
        m = (f'<video class="media" src="{src}" poster="{IMG}v-{media[:-4]}.webp" muted loop playsinline preload="none" aria-label="{label}"></video>')
    else:
        m = f'<img src="{src}" alt="{label}" loading="lazy" width="540" height="960" />'
    pts = ''.join(f'<li>{p}</li>' for p in points)
    inner = (f'<div class="demo"><div class="demo-m">{m}<span class="tag">{tag}</span></div>'
             f'<div class="demo-t"><h2 class="t-h2">{title}</h2><p class="t-lead">{text}</p><ul class="demo-pts">{pts}</ul>'
             f'<p class="demo-note">Пример на демонстрационной ИИ‑съёмке, сценарий условный.</p></div></div>')
    return section(id_, inner, cls=cls)


SERVICE_CSS = '''    .ethics{display:grid;grid-template-columns:repeat(4,1fr);gap:40px}
    .ethics .ic-box{margin-bottom:18px}
    .ethics h3{font-size:21px;font-weight:400;letter-spacing:-.015em;margin-bottom:10px}
    .ethics p{color:var(--slate);font-size:15.5px}
    .note{font-size:14px;color:var(--slate);margin-top:18px}
    @media (max-width:1024px){ .ethics{grid-template-columns:1fr 1fr} }
    @media (max-width:600px){ .ethics{grid-template-columns:1fr;gap:28px} }
'''

# ——— кампании
CAMP_SCRIPT = '''<script>
(() => {
  if (/[?&]export\\b/.test(location.search)) document.documentElement.classList.add('export');
  const fit = f => { const b = f.firstElementChild; if (b) b.style.setProperty('--s', f.clientWidth / +getComputedStyle(f).getPropertyValue('--w')); };
  const ro = new ResizeObserver(es => es.forEach(e => fit(e.target)));
  document.querySelectorAll('.bn-frame').forEach(f => { fit(f); ro.observe(f); });
})();
</script>'''

LOGO = ('<span class="bn-logo"><svg class="s" viewBox="0 0 100 91.2"><use href="#ss-star"/></svg>'
        '<span class="w"><svg viewBox="0 0 66.97 11.77"><use href="#ss-social"/></svg><svg viewBox="0 0 61.26 11.78"><use href="#ss-stars"/></svg></span>'
        '<i></i><svg class="ai" viewBox="0 0 15.95 11.78"><use href="#ss-ai"/></svg></span>')


def legal(extra=''):
    return f'<p class="bn-legal">Реклама. [Рекламодатель], ИНН [—]. erid: [—].{(" " + extra) if extra else ""}</p>'


def campaign(slug, *, service_name, camp_name, lead, facts, brief, msgs, banners, banner_css, scripts, media, budget, funnel, kpis, cal, utm_sources, utm_content, extra_tech=None):
    path = f'/ai/{slug}/campaign/'
    bn_html = ''.join(f'''
        <figure class="bn-card">
          <div class="bn-frame" style="--w:{w};--h:{h}" data-bn="{bid}">{inner}</div>
          <figcaption><b>{cap}</b><a class="link" href="creatives/{bid}.png" download>Скачать PNG</a></figcaption>
        </figure>''' for bid, w, h, cap, inner in banners)
    sc_html = ''.join('''
        <article class="script"><h3>''' + t + '''</h3><table><thead><tr><th scope="col">Время</th><th scope="col">В кадре</th><th scope="col">Текст</th></tr></thead><tbody>''' +
                      ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows) + '</tbody></table></article>' for t, rows in scripts)
    md_html = ''.join(f'<tr><th scope="row">{c}</th><td>{a}</td><td>{f}</td><td class="num"><span class="mbar"><i data-bar style="width:{min(100, p * 3)}%"></i></span>{p}%</td><td class="num">{money(budget * p // 100)}</td><td>{k}</td></tr>' for c, a, f, p, k in media)
    top = funnel[0][2]
    fn_html = ''.join(f'<div class="fn-row"><span>{a}</span><span class="fn-bar"><i data-bar style="width:{w}%"></i></span><b>{v}</b></div>' for a, v, w in funnel)
    kp_html = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in kpis)
    cal_html = ''.join(f'<div class="cl-row"><span>{t}</span><span class="cl-track">' + ''.join(f'<i class="{"on" if a <= w <= b else ""}"></i>' for w in range(1, 7)) + '</span></div>' for t, a, b in cal)
    br_html = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in brief)
    ms_html = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in msgs)
    fc = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in facts)
    tech = extra_tech or ['Каждый креатив регистрируем в ОРД и получаем erid', 'На макете — «Реклама», рекламодатель и erid', 'В роликах с ИИ — пометка об этом', 'Отчёты в ЕРИР — ежемесячно']
    main = f'''<main id="main">
  <section class="hero camp-hero">
    <div class="wrap">
      <div class="hero-text">
        <nav class="crumbs" aria-label="Вы здесь"><a href="/social-stars-demo/ai/">Social Stars AI</a><span aria-hidden="true">/</span><a href="/social-stars-demo/ai/{slug}/">{service_name}</a><span aria-hidden="true">/</span><span aria-current="page">Кампания</span></nav>
        <h1 class="t-hero">Кампания «{camp_name}»</h1>
        <p class="t-lead">{lead}</p>
        <div class="hero-actions"><a class="btn btn-primary" href="#creatives">Смотреть креативы</a><a class="btn btn-line" href="/social-stars-demo/ai/{slug}/?utm_source=campaign_kit&amp;utm_medium=internal&amp;utm_campaign={utm_content[0]}">Посадочная страница</a></div>
      </div>
      <div class="camp-key"><div class="bn-frame" style="--w:{banners[0][1]};--h:{banners[0][2]}">{banners[0][4]}</div></div>
    </div>
    <div class="wrap hero-facts"><dl class="facts">{fc}</dl></div>
  </section>

  <nav class="subnav" aria-label="Разделы страницы">
    <div class="wrap"><a href="#idea">Идея</a><a href="#messages">Заголовки</a><a href="#creatives">Креативы</a><a href="#scripts">Сценарии</a><a href="#media">Медиаплан</a><a href="#funnel">Воронка</a><a href="#calendar">Календарь</a><a href="#tech">Метки</a></div>
  </nav>

  <section class="section" id="idea"><div class="wrap"><div class="head"><h2 class="t-h2">Идея в пяти строках</h2></div><dl class="brief">{br_html}</dl></div></section>

  <section class="section band" id="messages"><div class="wrap"><div class="head"><h2 class="t-h2">Заголовки</h2></div><ol class="msgs">{ms_html}</ol></div></section>

  <section class="section" id="creatives">
    <div class="wrap">
      <div class="head split"><h2 class="t-h2">Креативы</h2><p class="t-lead">Готовые макеты в размерах площадок. Перед запуском впишите рекламодателя и erid.</p></div>
      <div class="bn-grid">{bn_html}
      </div>
    </div>
  </section>

  <section class="section band" id="scripts"><div class="wrap"><div class="head"><h2 class="t-h2">Сценарии роликов</h2></div><div class="scripts">{sc_html}
      </div></div></section>

  <section class="section" id="media">
    <div class="wrap">
      <div class="head split"><h2 class="t-h2">Медиаплан</h2><p class="t-lead">Пример распределения {money(budget)} на 6 недель. Доли пересматриваем после первой недели.</p></div>
      <div class="tbl" data-bars><table class="mp"><thead><tr><th scope="col">Канал</th><th scope="col">Кому показываем</th><th scope="col">Форматы</th><th scope="col">Доля</th><th scope="col">Бюджет</th><th scope="col">Главная метрика</th></tr></thead><tbody>{md_html}</tbody></table></div>
    </div>
  </section>

  <section class="section band" id="funnel">
    <div class="wrap fn">
      <div>
        <h2 class="t-h2">Воронка</h2>
        <p class="t-lead">Ориентиры для планирования, а не обещание. Уточняем после первой недели.</p>
        <dl class="fn-kpi">{kp_html}</dl>
      </div>
      <div class="fn-chart" data-bars>{fn_html}</div>
    </div>
  </section>

  <section class="section" id="calendar">
    <div class="wrap">
      <div class="head"><h2 class="t-h2">Календарь</h2></div>
      <div class="cal" data-bars>
        <div class="cl-row cl-head"><span></span><span class="cl-track">{"".join(f"<b>Неделя {w}</b>" for w in range(1, 7))}</span></div>
        {cal_html}
      </div>
    </div>
  </section>

  <section class="section band" id="tech">
    <div class="wrap">
      <div class="head"><h2 class="t-h2">Метки и маркировка</h2></div>
      <div class="tech">
        <div>
          <h3>UTM</h3>
          <ul class="utm"><li><code>utm_source</code> {utm_sources}</li><li><code>utm_medium</code> cpc, cpm, post</li><li><code>utm_campaign</code> {utm_content[0]}</li><li><code>utm_content</code> {", ".join(utm_content[1:])}</li></ul>
          <p class="ex"><code>…/ai/{slug}/?utm_source=yandex&amp;utm_medium=cpc&amp;utm_campaign={utm_content[0]}&amp;utm_content={utm_content[1]}</code></p>
        </div>
        <div>
          <h3>Маркировка</h3>
          <ul class="utm">{"".join(f"<li>{x}</li>" for x in tech)}</ul>
        </div>
      </div>
    </div>
  </section>
'''
    style = '    .camp-hero .camp-key{max-width:520px;justify-self:end;width:100%}\n' + banner_css
    build('ai/ugc/campaign/index.html', f'ai/{slug}/campaign/index.html',
          title=f'Кампания «{camp_name}» — {service_name} — Social Stars AI',
          desc=f'Рекламная кампания направления «{service_name}»: идея, заголовки, креативы, сценарии роликов, медиаплан, воронка и календарь на 6 недель.',
          path=path, og_title=f'Кампания «{camp_name}»', og_desc=lead, ld=None, style=style, main=main, script=CAMP_SCRIPT)
