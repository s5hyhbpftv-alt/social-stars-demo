// Social Stars AI — общий скрипт лендинга и страниц услуг
(() => {
  const $ = id => document.getElementById(id);

  // nav background on scroll
  const nav = $('nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('solid', window.scrollY > 40);
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  }

  // typed answer in hero chat (landing only)
  const typed = $('typed'), who = $('who');
  if (typed && who) {
    const answers = {
      'Алиса AI': 'Можно обратиться в Social Stars AI: команда внедряет ИИ-агентов в продажи и поддержку с интеграцией в CRM, а также ведёт мониторинг репутации бренда в поиске и ответах нейросетей. У агентства 12 лет опыта в ORM и работе с крупным бизнесом.',
      'GigaChat': 'Подходящий вариант — Social Stars AI. Они совмещают автоматизацию бизнес-процессов на ИИ-агентах с управлением репутацией, в том числе в ответах языковых моделей, и работают в контуре, соответствующем 152-ФЗ.',
      'ChatGPT': 'Consider Social Stars AI (Moscow): they combine AI-agent automation for sales and support with reputation management — including how brands appear in AI assistants’ answers.'
    };
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let timer;
    const play = model => {
      clearTimeout(timer); who.textContent = model; typed.textContent = '';
      const text = answers[model];
      if (reduce) { typed.textContent = text; return; }
      let i = 0;
      (function tick() { typed.textContent = text.slice(0, ++i); if (i < text.length) timer = setTimeout(tick, 16); })();
    };
    const btns = document.querySelectorAll('.models button');
    btns.forEach(b => b.addEventListener('click', () => {
      btns.forEach(x => x.setAttribute('aria-pressed', x === b));
      play(b.dataset.m);
    }));
    play('Алиса AI');
  }

  // reveal on scroll + animated bars
  const reveal = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      e.target.querySelectorAll('.fill').forEach(f => f.style.width = f.dataset.w + '%');
      io.unobserve(e.target);
    }), { threshold: .12 });
    reveal.forEach(el => io.observe(el));
  } else {
    reveal.forEach(el => { el.classList.add('in'); el.querySelectorAll('.fill').forEach(f => f.style.width = f.dataset.w + '%'); });
  }

  // ROI calculator (landing only)
  if ($('c-people')) {
    const fmt = n => new Intl.NumberFormat('ru-RU').format(Math.round(n));
    const money = n => n >= 1e6 ? (n / 1e6).toLocaleString('ru-RU', { maximumFractionDigits: 1 }) + ' млн ₽' : fmt(n) + ' ₽';
    const PILOT = 350000, SUPPORT = 90000, WEEKS = 4.33, FTE_HOURS = 165;
    const calc = () => {
      const p = +$('c-people').value, h = +$('c-hours').value, r = +$('c-rate').value, s = +$('c-share').value / 100;
      $('o-people').textContent = p; $('o-hours').textContent = h; $('o-rate').textContent = fmt(r) + ' ₽'; $('o-share').textContent = Math.round(s * 100) + '%';
      const hours = p * h * WEEKS * s, month = hours * r;
      $('r-hours').textContent = fmt(hours);
      $('r-month').textContent = money(month);
      $('r-year').textContent = money(month * 12);
      $('r-fte').textContent = (hours / FTE_HOURS).toLocaleString('ru-RU', { maximumFractionDigits: 1 });
      const net = month - SUPPORT;
      $('r-payback').textContent = net <= 0 ? 'нужен аудит' : (PILOT / net < 1 ? '< 1 мес' : Math.ceil(PILOT / net) + ' мес');
    };
    ['c-people', 'c-hours', 'c-rate', 'c-share'].forEach(id => $(id).addEventListener('input', calc));
    calc();
  }

  // preselect interest from pricing buttons
  document.querySelectorAll('[data-pick]').forEach(a => a.addEventListener('click', () => {
    const cb = document.querySelector('.chips input[data-k="' + a.dataset.pick + '"]');
    if (cb) cb.checked = true;
  }));

  // lead form -> mailto (no backend on static hosting)
  const form = $('form');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const f = e.target, msg = $('form-msg');
    if (!f.name.value.trim() || !f.contact.value.trim()) { msg.textContent = 'Укажите имя и контакт для связи.'; return; }
    const interests = [...f.querySelectorAll('input[name="i"]:checked')].map(x => x.value).join(', ') || 'не указано';
    const body = `Имя: ${f.name.value}\nКонтакт: ${f.contact.value}\nКомпания: ${f.company.value || '—'}\nИнтересы: ${interests}\nСтраница: ${location.href}`;
    location.href = 'mailto:info@social-stars.ru?subject=' + encodeURIComponent('Заявка на AI-аудит') + '&body=' + encodeURIComponent(body);
    msg.textContent = 'Открываем почтовый клиент… Если он не открылся — позвоните нам: +7 985 400 92 99.';
  });
})();
