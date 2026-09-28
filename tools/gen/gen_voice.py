import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import *

CHIP = 'Голосовой оператор'
DEMO = [('cl', 'Здравствуйте, хочу записаться к стоматологу'),
        ('ai', 'Здравствуйте! Клиника «Улыбка», я ИИ‑ассистент. Есть время завтра в 10:30 или в 16:00 — как удобнее?'),
        ('cl', 'Давайте в 16:00. Меня зовут Анна'),
        ('ai', 'Записала вас, Анна, на завтра в 16:00. Напоминание придёт в СМС.')]
CRM_ROWS = [('Имя', 'Анна'), ('Услуга', 'Консультация стоматолога'), ('Время', 'Завтра, 16:00'), ('Источник', 'Входящий звонок')]

hero_vis = f'''<div class="vdemo" data-vdemo role="img" aria-label="Пример звонка: ИИ-оператор записывает клиентку на приём, данные сразу появляются в CRM">
        {call_ui(DEMO, t='00:00')}
        {crm(CRM_ROWS, 'Запись создана')}
      </div>'''

SC = {
  'Запись на приём': [('cl', 'Можно записаться на стрижку в субботу?'), ('ai', 'Да, в субботу свободно в 12:00 и в 15:30. Какое время удобно?'), ('cl', 'В 12'), ('ai', 'Готово: суббота, 12:00, мастер Ольга. Пришлю напоминание накануне.')],
  'Статус заказа': [('cl', 'Где мой заказ? Номер 48213'), ('ai', 'Заказ 48213 передан курьеру, доставка сегодня с 14 до 18. Прислать ссылку на отслеживание в СМС?'), ('cl', 'Да, пришлите'), ('ai', 'Отправила. Что‑нибудь ещё подсказать?')],
  'Квалификация заявки': [('cl', 'Нам нужна поставка упаковки, большой объём'), ('ai', 'Подскажите, какой объём в месяц и в какой город?'), ('cl', 'Около 20 тысяч коробок, Казань'), ('ai', 'Передаю менеджеру по крупным клиентам — он перезвонит в течение 15 минут с расчётом.')],
  'Подтверждение визита': [('ai', 'Здравствуйте, это ИИ‑ассистент автосервиса «Мотор». Вы записаны на завтра на 9:00 — подтверждаете?'), ('cl', 'Нет, давайте перенесём на пятницу'), ('ai', 'В пятницу свободно в 9:00 и в 13:00.'), ('cl', 'В 13'), ('ai', 'Перенесла на пятницу, 13:00. Спасибо!')],
}
tabs = ''.join(f'<button type="button" class="sc-tab" aria-pressed="{"true" if i == 0 else "false"}" data-i="{i}">{n}</button>' for i, n in enumerate(SC))
first = list(SC.values())[0]
scen = f'''<div class="scen">
        <div class="sc-tabs" role="group" aria-label="Сценарии">{tabs}<p class="note">Компании и диалоги условные. Исходящий звонок — только клиенту, который дал согласие.</p></div>
        <div class="sc-phone">{call_ui(first, title='Звонок', t='00:00')}</div>
      </div>
<script type="application/json" id="sc-data">{json.dumps(list(SC.values()), ensure_ascii=False)}</script>'''

handoff = f'''<div class="hand" data-wires="c>ai ai>o1:2 ai>o2 ai>o3">
        <div class="hcol"><div class="hnode" data-n="c">{icon("bell")}<b>Звонок клиента</b><span>днём, ночью, в выходные</span></div></div>
        <div class="hcol"><div class="hnode hub" data-n="ai">{icon("assistant")}<b>ИИ‑оператор</b><span>отвечает с первого гудка</span></div></div>
        <div class="hcol outs">
          <div class="hnode" data-n="o1">{icon("inbox")}<b>Решил сам</b><span>запись, ответ, статус — сразу в CRM</span></div>
          <div class="hnode" data-n="o2">{icon("people")}<b>Сложный вопрос</b><span>переводит на сотрудника с кратким пересказом</span></div>
          <div class="hnode" data-n="o3">{icon("alert")}<b>Недовольный клиент</b><span>сразу к руководителю смены</span></div>
        </div>
      </div>'''

calc = '''<div class="loss" data-loss>
        <div class="loss-in">
          <div class="rng"><label>Звонков в день <output>80</output></label><input type="range" min="10" max="500" step="10" value="80" data-k="calls" /></div>
          <div class="rng"><label>Пропущено или без ответа <output>15%</output></label><input type="range" min="2" max="40" step="1" value="15" data-k="miss" /></div>
          <div class="rng"><label>Звонок превращается в продажу <output>25%</output></label><input type="range" min="5" max="60" step="1" value="25" data-k="conv" /></div>
          <div class="rng"><label>Средний чек <output>6 000 ₽</output></label><input type="range" min="1000" max="100000" step="1000" value="6000" data-k="check" /></div>
        </div>
        <div class="loss-out">
          <small>Недополученная выручка в месяц</small>
          <div class="big" data-o="money">2 160 000 ₽</div>
          <div class="loss-bar"><i data-o="bar"></i></div>
          <p><b data-o="clients">90</b> клиентов в месяц звонили, но не дошли до покупки. Расчёт по вашим цифрам, 30 дней.</p>
        </div>
      </div>'''

main = '<main id="main">\n' + hero('Голосовой ИИ‑оператор', 'На звонок уже ответили',
    'Голосовой ИИ‑оператор принимает звонки круглосуточно: отвечает на вопросы, записывает, сообщает статус и передаёт заявку в CRM. Сложное — сразу человеку.',
    [('btn-primary', '#lead', 'Послушать демо‑звонок', CHIP), ('btn-line', '#loss', 'Посчитать потери', '')], hero_vis,
    [('Ответ', 'с первого гудка'), ('Работает', 'круглосуточно'), ('Минута разговора', 'от 14 ₽')], 'vo-hero') + '\n\n' + \
    subnav([('scenarios', 'Сценарии'), ('case', 'На практике'), ('handoff', 'Люди'), ('loss', 'Потери'), ('law', 'Закон'), ('week', 'Этапы'), ('pricing', 'Тарифы'), ('faq', 'Вопросы')], 'Демо‑звонок', CHIP) + '\n\n' + \
    section('scenarios', scen, head='Что оператор делает сам', lead='Выберите сценарий — звонок проиграется заново.', split=True) + '\n\n' + \
    demo('case', 'voice-roots.mp4', 'Звонок в салон после закрытия', 'Пример: салон красоты. Клиентка звонит в 21:40. ИИ‑оператор сразу говорит, что он ИИ, находит свободное окно у мастера и отправляет подтверждение сообщением.', ['Представляется как ИИ‑оператор', 'Видит расписание мастеров', 'Подтверждение приходит сообщением'], label='Клиентка салона после укладки') + '\n\n' + \
    section('handoff', handoff, cls='band', head='Когда подключается человек') + '\n\n' + \
    section('loss', calc, head='Сколько стоит пропущенный звонок') + '\n\n' + \
    section('law', ethics([('tag', 'Маркировка звонков', 'Исходящие звонки идут с маркировкой по 41‑ФЗ: клиент видит компанию и цель звонка.'),
                           ('sign', 'Исходящие — по согласию', 'Рекламный обзвон — только тем, кто явно согласился. Без согласия не звоним.'),
                           ('assistant', 'Честно представляется', 'Ассистент сразу говорит, что он ИИ, и переводит на человека по первой просьбе.'),
                           ('lock', 'Данные в России', 'Записи и расшифровки хранятся на серверах в РФ, по 152‑ФЗ.')]), cls='band', head='По закону') + '\n\n' + \
    section('week', steps([('Неделя 1', 'Слушаем 100 звонков', 'Находим частые вопросы и где теряются клиенты.'),
                           ('Неделя 2', 'Сценарии и голос', 'Пишем диалоги, выбираем голос, настраиваем паузы.'),
                           ('Неделя 3', 'Телефония и CRM', 'Подключаем ваши номера, CRM и расписание.'),
                           ('Недели 4–5', 'Пилот', 'Оператор работает на части звонков, сравниваем с людьми.')]), head='Запуск за месяц') + '\n\n' + \
    section('pricing', plans([
        dict(name='Старт', price='190 000 ₽', small='запуск, минута от 14 ₽', text='Один сценарий на входящих.', list=['Запись или ответы на вопросы', 'Телефония и CRM', 'Перевод на сотрудника', 'Отчёт раз в неделю'], cta='Выбрать «Старт»'),
        dict(name='Бизнес', price='390 000 ₽', small='запуск, минута от 12 ₽', text='Для компаний с потоком звонков.', list=['До 5 сценариев', 'Исходящие по согласию', 'Аналитика разговоров', 'Доработка каждую неделю'], cta='Выбрать «Бизнес»', main=True, badge='Чаще выбирают'),
        dict(name='Контакт‑центр', price='от 900 000 ₽', small='запуск', text='Для банков, сетей и госсектора.', list=['Голос бренда', 'Развёртывание в вашем контуре', 'Интеграция с 1С и АТС', 'Поддержка 24/7'], cta='Обсудить проект')], CHIP),
        cls='band', head='Тарифы', lead='Минуты считаем по факту разговора. Пилот на части звонков — до подписания основного договора.', split=True) + '\n\n' + \
    section('faq', faq([
        ('Клиенты поймут, что говорят с ИИ?', 'Да — ассистент представляется сразу. Это честно, и так спокойнее для клиента: он знает, что может попросить человека в любой момент.'),
        ('Что, если оператор не понял вопрос?', 'Переспросит один раз, а если не поможет — переведёт на сотрудника и передаст краткий пересказ разговора, чтобы клиенту не пришлось повторять.'),
        ('С какой телефонией и CRM работаете?', 'Облачные АТС (Манго, Мегафон, Билайн, Телфин и другие), Битрикс24, amoCRM, 1С, YCLIENTS и собственные системы через API.'),
        ('Можно ли продавать исходящими звонками?', 'Только клиентам, которые явно согласились на звонки, и с маркировкой по 41‑ФЗ. Холодный рекламный обзвон мы не делаем — это штрафы до 1 млн ₽ и потеря доверия.'),
        ('Где хранятся записи разговоров?', 'На серверах в России. Для банков и госсектора разворачиваем оператора в вашем контуре.')])
        + '\n      ' + next_link('trainer', 'stairs', 'ИИ‑тренажёр продаж'), head='Вопросы') + '\n'

style = SERVICE_CSS + '''    .vdemo{position:relative;display:grid;grid-template-columns:1fr .78fr;gap:18px;align-items:start;max-width:560px;justify-self:end;width:100%}
    .vdemo .crm{margin-top:120px}
    .scen{display:grid;grid-template-columns:1fr minmax(280px,380px);gap:clamp(32px,6vw,96px);align-items:start}
    .sc-tabs{display:grid;gap:10px;align-content:start}
    .sc-tab{text-align:left;padding:18px 20px;border-radius:var(--r-md);border:1px solid var(--mist);background:var(--white);font:400 18px/1.3 var(--font);color:var(--ink);cursor:pointer;transition:border-color .2s,box-shadow .2s}
    .sc-tab:hover{border-color:var(--mist-2)}
    .sc-tab[aria-pressed="true"]{border-color:var(--bronze);box-shadow:0 0 0 3px var(--bronze-soft)}
    .hand{display:grid;grid-template-columns:1fr 1fr 1.3fr;gap:clamp(40px,7vw,120px);align-items:center}
    .hcol{display:grid;gap:18px}
    .hnode{display:grid;gap:4px;padding:18px 20px;border-radius:var(--r-md);background:var(--white);border:1px solid var(--mist)}
    .hnode .ic{color:var(--bronze-2);margin-bottom:6px}
    .hnode b{font-weight:500;font-size:17px}
    .hnode span{color:var(--slate);font-size:14.5px}
    .hnode.hub{background:var(--ink);border-color:var(--ink);color:#fff}
    .hnode.hub span{color:#a9b1c0}.hnode.hub .ic{color:var(--bronze)}
    .loss{display:grid;grid-template-columns:6fr 5fr;gap:24px}
    .loss-in,.loss-out{background:var(--white);border:1px solid var(--mist);border-radius:var(--r-lg);padding:clamp(24px,3vw,36px)}
    .rng{display:grid;gap:10px;margin-bottom:26px}.rng:last-child{margin-bottom:0}
    .rng label{display:flex;justify-content:space-between;gap:12px;font-size:15.5px}
    .rng output{font-weight:500;font-variant-numeric:tabular-nums}
    .rng input{width:100%;accent-color:var(--ink);height:24px}
    .loss-out{display:grid;gap:18px;align-content:start}
    .loss-out small{font-size:14px;color:var(--slate)}
    .loss-out .big{font-size:clamp(40px,5vw,64px);font-weight:200;letter-spacing:-.05em;line-height:1;font-variant-numeric:tabular-nums}
    .loss-bar{height:10px;border-radius:5px;background:var(--porcelain-2);overflow:hidden}
    .loss-bar i{display:block;height:100%;width:30%;background:var(--bronze);border-radius:5px;transition:width .4s var(--ease)}
    .loss-out p{color:var(--slate)}
    .loss-out p b{color:var(--ink);font-weight:500}
    @media (max-width:1024px){ .vdemo{justify-self:start} .scen,.loss{grid-template-columns:1fr} .sc-phone{max-width:380px} .hand{grid-template-columns:1fr;gap:16px} .hand .wires{display:none} }
    @media (max-width:600px){ .vdemo{grid-template-columns:1fr} .vdemo .crm{margin-top:0;max-width:300px} }
'''

script = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  const g = window.gsap, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt = n => Math.round(n).toLocaleString('ru-RU').replace(/\\u202f/g, '\\u00a0');
  const mmss = s => String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(Math.floor(s % 60)).padStart(2, '0');
  // проигрыш звонка: реплики по очереди, волна говорит, таймер идёт, CRM заполняется
  const play = (call, crmEl, loop) => {
    const bubbles = [...call.querySelectorAll('.call-log .b')], bars = call.querySelectorAll('.call-wave i'), t = call.querySelector('.call-t');
    const dds = crmEl ? [...crmEl.querySelectorAll('dd')] : [], vals = dds.map(d => d.textContent), st = crmEl && crmEl.querySelector('.crm-st');
    if (!g || reduce) return null;
    const clock = { s: 0 };
    const tl = g.timeline({ repeat: loop ? -1 : 0, repeatDelay: 2.4, onRepeat: () => {} });
    tl.set(bubbles, { opacity: 0, y: 10 }).set(bars, { scaleY: .18 }).set(clock, { s: 0 });
    if (crmEl) { tl.add(() => dds.forEach(d => { d.textContent = '—'; })).set(st, { opacity: 0 }); }
    tl.to(clock, { s: 4 + bubbles.length * 6, duration: .8 + bubbles.length * 1.9, ease: 'none', onUpdate: () => { t.textContent = mmss(clock.s); } }, 0);
    bubbles.forEach((b, i) => {
      const at = .5 + i * 1.9;
      tl.to(b, { opacity: 1, y: 0, duration: .45, ease: 'power2.out' }, at)
        .to(bars, { scaleY: () => .2 + Math.random() * .8, duration: .14, ease: 'sine.inOut', stagger: { each: .015, repeat: 5, yoyo: true } }, at)
        .to(bars, { scaleY: .18, duration: .3 }, at + 1.4);
      if (crmEl && b.classList.contains('ai') && i > 1) tl.add(() => dds.forEach((d, j) => { d.textContent = vals[j]; g.fromTo(d, { opacity: 0 }, { opacity: 1, duration: .4, delay: j * .12 }); }), at + .4);
    });
    if (crmEl) tl.to(st, { opacity: 1, duration: .4 }, '>-.2');
    return tl;
  };
  const demo = document.querySelector('[data-vdemo]');
  if (demo) {
    const tl = play(demo.querySelector('.call'), demo.querySelector('.crm'), true);
    if (tl && window.ScrollTrigger) ScrollTrigger.create({ trigger: demo, start: 'top bottom', end: 'bottom top', onToggle: s => s.isActive ? tl.resume() : tl.pause() });
  }
  // сценарии
  const data = JSON.parse(document.getElementById('sc-data').textContent), phone = document.querySelector('.sc-phone .call'), tabs = [...document.querySelectorAll('.sc-tab')];
  let cur = null;
  const show = i => {
    tabs.forEach((b, j) => b.setAttribute('aria-pressed', String(i === j)));
    phone.querySelector('.call-log').innerHTML = data[i].map(([w, t]) => `<p class="b ${w}"><small>${w === 'ai' ? 'ИИ‑оператор' : 'Клиент'}</small>${t}</p>`).join('');
    phone.querySelector('.call-top b').textContent = data[i][0][0] === 'ai' ? 'Исходящий звонок' : 'Входящий звонок';
    if (cur) cur.kill(); cur = play(phone, null, false);
  };
  tabs.forEach((b, i) => b.addEventListener('click', () => show(i)));
  if (window.ScrollTrigger && g && !reduce) ScrollTrigger.create({ trigger: phone, start: 'top 80%', once: true, onEnter: () => show(0) });
  // калькулятор потерь
  const box = document.querySelector('[data-loss]');
  if (box) {
    const inp = [...box.querySelectorAll('input')], o = k => box.querySelector(`[data-o="${k}"]`);
    const upd = () => {
      const v = Object.fromEntries(inp.map(i => [i.dataset.k, +i.value]));
      inp.forEach(i => { const out = i.closest('.rng').querySelector('output'); out.textContent = i.dataset.k === 'check' ? fmt(+i.value) + '\\u00a0₽' : (i.dataset.k === 'calls' ? i.value : i.value + '%'); });
      const clients = v.calls * 30 * v.miss / 100 * v.conv / 100, money = clients * v.check;
      o('money').textContent = fmt(money) + '\\u00a0₽'; o('clients').textContent = fmt(clients);
      o('bar').style.width = Math.min(100, v.miss / 40 * 100) + '%';
    };
    inp.forEach(i => i.addEventListener('input', upd)); upd();
  }
});
</script>'''

build('ai/ugc/index.html', 'ai/voice/index.html',
      title='Голосовой ИИ-оператор: звонки 24/7 с записью в CRM — Social Stars AI',
      desc='Голосовой ИИ-оператор отвечает на звонки круглосуточно, записывает клиентов, сообщает статус заказа и передаёт заявки в CRM. Маркировка по 41-ФЗ, данные в РФ. Запуск от 190 000 ₽, минута от 12 ₽.',
      path='/ai/voice/', og_title='На звонок уже ответили — голосовой ИИ-оператор', og_desc='Ответ с первого гудка, днём и ночью, с записью в CRM.',
      ld=ld_service('Голосовой ИИ-оператор', '/ai/voice/', 190000), style=style, main=main, script=script, service=CHIP)

# ——— кампания
L = lambda: legal()
mini = [('cl', 'Здравствуйте, можно записаться на завтра?'), ('ai', 'Здравствуйте! Есть 10:30 и 16:00 — как удобнее?')]
banners = [
 ('square-important', 1080, 1080, 'Квадрат 1080×1080 — Telegram Ads, VK Реклама',
  f'''<div class="bn b-sq ink">{LOGO}<h3>Ваш звонок<br>очень важен</h3>
      <p class="bn-lead">Поэтому на него уже ответили. Голосовой ИИ‑оператор — круглосуточно.</p>
      <span class="bn-cta">Послушать демо‑звонок</span>
      <div class="vcall">{call_ui(mini, t='00:07', bars=28, static=True)}</div>{L()}</div>'''),
 ('square-missed', 1080, 1080, 'Квадрат 1080×1080 — владельцы клиник, салонов, сервисов',
  f'''<div class="bn b-sq2">{LOGO}<h3>Ни одного пропущенного звонка</h3>
      <div class="vpair">{call_ui(mini, t='00:07', bars=24, static=True)}{crm([("Имя", "Анна"), ("Услуга", "Консультация"), ("Время", "Завтра, 16:00")], "Запись создана")}</div>
      <p class="bn-lead">Ответ с первого гудка, запись сразу в CRM.</p>
      <span class="bn-cta">Посчитать потери</span>{L()}</div>'''),
 ('story-night', 1080, 1920, 'Вертикаль 1080×1920 — истории и клипы',
  f'''<div class="bn b-st ink">{LOGO}<h3 class="clock">03:14</h3>
      <p class="bn-lead">Клиент звонит ночью. Ему отвечают, записывают и присылают СМС.</p>
      <div class="vstack">{call_ui(mini, t='00:07', bars=30, static=True)}{crm([("Имя", "Анна"), ("Время", "Завтра, 10:30")], "Запись создана")}</div>
      <span class="bn-cta">Послушать демо‑звонок</span>{L()}</div>'''),
 ('wide-zero', 1200, 628, 'Горизонталь 1200×628 — Яндекс РСЯ, VK Реклама',
  f'''<div class="bn b-wd ink">{LOGO}<h3>00:00 ожидания</h3>
      <p class="bn-lead">Голосовой ИИ‑оператор отвечает с первого гудка.</p>
      <span class="bn-cta">Послушать демо‑звонок</span>
      <div class="vwave">{"".join(f'<i style="height:{h}%"></i>' for h in [18,26,40,62,80,54,36,70,92,66,40,28,52,84,100,72,46,30,58,88,64,38,24,44,76,96,68,42,26,18,34,56,78,50,32,20])}</div>{L()}</div>'''),
]
banner_css = '''    .b-sq h3{font-size:118px}
    .b-sq .vcall{position:absolute;right:48px;top:450px;width:440px}
    .b-sq .vcall .call-log{min-height:0}
    .b-sq2 h3{font-size:84px;width:900px}
    .b-sq2 .vpair{position:absolute;left:64px;top:400px;display:grid;grid-template-columns:430px 360px;gap:28px;align-items:start}
    .b-sq2 .vpair .call-log{min-height:0}
    .b-sq2 .vpair .crm{margin-top:90px}
    .b-sq2 .bn-lead{top:840px;width:600px;font-size:30px}
    .b-sq2 .bn-cta{left:700px;top:840px}
    .b-st h3.clock{font-size:260px;top:230px;font-weight:200;letter-spacing:-.06em;font-variant-numeric:tabular-nums}
    .b-st .bn-lead{top:560px}
    .b-st .vstack{position:absolute;left:80px;right:80px;top:780px;display:grid}
    .b-st .vstack .call{width:640px}
    .b-st .vstack .call-log{min-height:0}
    .b-st .vstack .crm{width:500px;justify-self:end;margin-top:-40px;position:relative}
    .b-st .bn-cta{top:1690px}
    .bn.ink .call-in{box-shadow:0 0 0 1px rgba(255,255,255,.1),0 40px 70px -40px rgba(0,0,0,.6);background:#1c2233}
    .b-wd .vwave{position:absolute;right:56px;top:170px;width:520px;height:260px;display:flex;align-items:center;gap:7px}
    .b-wd .vwave i{flex:1;border-radius:6px;background:var(--bronze)}
'''
campaign('voice', service_name='Голосовой ИИ‑оператор', camp_name='Ваш звонок очень важен',
  lead='Запуск голосового ИИ‑оператора для клиник, салонов, сервисов и доставки: идея, креативы, аудиоролик и медиаплан на 6 недель.',
  facts=[('Цель', '10 договоров за 6 недель'), ('Аудитория', 'владельцы и управляющие сервисного бизнеса'), ('Бюджет', '700 000 ₽ — пример')],
  brief=[('Инсайт', 'Клиент, который слышит «Ваш звонок очень важен, оставайтесь на линии», звонит конкуренту. Вечером и в выходные звонки теряются совсем.'),
         ('Идея', 'Разворачиваем самую надоевшую фразу: ваш звонок очень важен — поэтому на него уже ответили.'),
         ('Обещание', 'Ответ с первого гудка в любое время и запись сразу в CRM.'),
         ('Почему верить', 'Живой демо‑звонок на сайте, пилот на части звонков до основного договора, маркировка по 41‑ФЗ.'),
         ('Тон', 'С лёгкой иронией над колл‑центрами, но без насмешки над клиентами. Цифры — из калькулятора потерь, а не из воздуха.')],
  msgs=[('Ваш звонок очень важен. Поэтому на него уже ответили', 'главный — все каналы'), ('Ни одного пропущенного звонка', 'клиники, салоны, автосервисы'),
        ('03:14. Клиент звонит. Ему отвечают', 'истории и клипы'), ('00:00 ожидания', 'РСЯ, ретаргетинг'), ('Посчитайте, сколько стоит пропущенный звонок', 'поиск и ретаргетинг — ведёт на калькулятор')],
  banners=banners, banner_css=banner_css,
  scripts=[('Аудиоролик «Оставайтесь на линии» · 20 секунд', [('0–5 с', 'Мелодия ожидания, знакомый голос.', '«Ваш звонок очень важен для нас. Пожалуйста, оставайтесь на линии…»'),
                                                            ('5–7 с', 'Музыка обрывается.', '«Здравствуйте! Слушаю вас»'),
                                                            ('7–17 с', 'Голос диктора.', '«Голосовой ИИ‑оператор отвечает с первого гудка — днём, ночью и в выходные. Записывает клиентов и сразу передаёт заявку в CRM»'),
                                                            ('17–20 с', 'Звуковой логотип.', '«Social Stars AI. Послушайте демо‑звонок на сайте»')]),
           ('Видео «03:14» · 15 секунд', [('0–3 с', 'Тёмная клиника, на стойке звонит телефон, часы 03:14.', 'Титр: «03:14. Все ушли домой»'),
                                         ('3–10 с', 'Экран звонка: реплики появляются, в CRM заполняется запись.', '«Клиент звонит ночью. Ему отвечают и записывают на утро»'),
                                         ('10–15 с', 'Утро, администратор видит новую запись. Логотип.', '«Голосовой ИИ‑оператор. Ни одного пропущенного звонка»')])],
  media=[('Яндекс Директ', 'поиск: «голосовой робот для клиники», «ИИ‑оператор колл‑центра», «автоответчик для бизнеса»; РСЯ', 'текст + горизонталь', 35, 'цена заявки'),
         ('Аудиореклама', 'подкасты и музыкальные сервисы, деловая аудитория', 'аудиоролик 20 с', 20, 'охват, запросы бренда'),
         ('VK Реклама', 'владельцы клиник, салонов, автосервисов, служб доставки', 'квадрат, вертикальное видео', 20, 'цена заявки'),
         ('Telegram Ads', 'каналы о бизнесе, медицине и сервисе', 'квадрат, текст', 15, 'цена клика'),
         ('Ретаргетинг', 'посетители калькулятора и тарифов', 'горизонталь «00:00 ожидания»', 10, 'возврат на демо')],
  budget=700000, funnel=[('Бюджет', '700 000 ₽', 100), ('Заявки', '200', 100), ('Демо‑звонки', '80', 40), ('Пилоты', '20', 10), ('Договоры', '10', 5)],
  kpis=[('Цена заявки', 'до 3 500 ₽'), ('Заявка → демо', '40%'), ('Демо → пилот', '25%'), ('Пилот → договор', '50%')],
  cal=[('Подготовка: креативы, аудиоролик, маркировка', 1, 1), ('Яндекс Директ: поиск и РСЯ', 2, 6), ('VK Реклама и Telegram Ads', 2, 6), ('Аудиореклама', 3, 5), ('Ретаргетинг на калькулятор', 3, 6), ('Пилоты у первых клиентов', 4, 6), ('Итоги и решение о масштабе', 6, 6)],
  utm_sources='yandex, vk, telegram, audio', utm_content=['voice_2026', 'important', 'missed', 'night', 'zero'],
  extra_tech=['Каждый креатив регистрируем в ОРД и получаем erid', 'На макете — «Реклама», рекламодатель и erid', 'Наши собственные звонки клиентам — только с маркировкой по 41‑ФЗ', 'Отчёты в ЕРИР — ежемесячно'])
