// Social Stars AI — общее поведение: шапка, меню, под-навигация, вопросы, заявка
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const path = location.pathname.replace(/index\.html$/, '');

  // шапка получает границу после начала прокрутки
  const hdr = $('.hdr');
  const onScroll = () => hdr && hdr.classList.toggle('is-solid', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // текущая страница в меню
  $$('.mega a, .mnav a, .ftr a').forEach(a => { if (a.getAttribute('href') === path) a.setAttribute('aria-current', 'page'); });

  // меню «Услуги»
  const megaBtn = $('[data-mega-btn]'), mega = $('.mega');
  if (megaBtn && mega) {
    let t;
    const open = v => { clearTimeout(t); mega.classList.toggle('is-open', v); megaBtn.setAttribute('aria-expanded', v); };
    megaBtn.addEventListener('click', () => open(!mega.classList.contains('is-open')));
    if (matchMedia('(hover: hover)').matches) [megaBtn, mega].forEach(el => {
      el.addEventListener('mouseenter', () => { clearTimeout(t); t = setTimeout(() => open(true), 90); });
      el.addEventListener('mouseleave', () => { clearTimeout(t); t = setTimeout(() => open(false), 200); });
    });
    document.addEventListener('click', e => { if (!mega.contains(e.target) && !megaBtn.contains(e.target)) open(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && mega.classList.contains('is-open')) { open(false); megaBtn.focus(); } });
  }

  // мобильное меню
  const burger = $('.burger'), mnav = $('.mnav');
  if (burger && mnav) {
    const set = v => {
      burger.setAttribute('aria-expanded', v); burger.setAttribute('aria-label', v ? 'Закрыть меню' : 'Открыть меню');
      mnav.classList.toggle('is-open', v); mnav.inert = !v; document.body.classList.toggle('lock', v);
    };
    mnav.inert = true;
    burger.addEventListener('click', () => set(burger.getAttribute('aria-expanded') !== 'true'));
    $$('a', mnav).forEach(a => a.addEventListener('click', () => set(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && mnav.classList.contains('is-open')) { set(false); burger.focus(); } });
  }

  // под-навигация: активный раздел
  const subnav = $('.subnav');
  if (subnav && 'IntersectionObserver' in window) {
    const links = $$('a[href^="#"]:not(.btn)', subnav);
    const byId = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      links.forEach(a => a.classList.remove('is-active'));
      const a = byId.get(e.target.id);
      if (a) { a.classList.add('is-active'); subnav.querySelector('.wrap').scrollTo({ left: a.offsetLeft - 40, behavior: reduce ? 'auto' : 'smooth' }); }
    }), { rootMargin: '-35% 0px -60% 0px' });
    byId.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }

  // вопросы: плавное раскрытие
  $$('.faq details').forEach(d => {
    const s = $('summary', d), a = $('.a', d);
    if (!s || !a || reduce) return;
    s.addEventListener('click', e => {
      e.preventDefault();
      const opts = { duration: 300, easing: 'cubic-bezier(.2,.7,.2,1)' };
      if (d.open) a.animate([{ height: a.scrollHeight + 'px' }, { height: '0px' }], opts).onfinish = () => d.open = false;
      else { d.open = true; a.animate([{ height: '0px' }, { height: a.scrollHeight + 'px' }], opts); }
    });
  });

  // на странице услуги её интерес в заявке отмечен заранее
  const svc = document.body.dataset.service;
  if (svc) { const cb = $('.chips input[value="' + svc + '"]'); if (cb) cb.checked = true; }
  $$('[data-pick]').forEach(a => a.addEventListener('click', () => { const cb = $('.chips input[value="' + a.dataset.pick + '"]'); if (cb) cb.checked = true; }));

  // заявка → письмо (у статического хостинга нет сервера)
  $$('form[data-lead]').forEach(form => {
    const fields = $$('.field', form);
    const check = f => {
      const i = $('input,textarea', f), bad = i.required && !i.value.trim();
      f.classList.toggle('is-invalid', bad); i.setAttribute('aria-invalid', bad); return !bad;
    };
    fields.forEach(f => $('input,textarea', f).addEventListener('input', () => f.classList.contains('is-invalid') && check(f)));
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!fields.map(check).every(Boolean)) { $('.is-invalid input', form).focus(); return; }
      const v = n => (form.elements[n] && form.elements[n].value.trim()) || '—';
      const interests = $$('input[name="i"]:checked', form).map(x => x.value).join(', ') || 'не указано';
      const body = `Имя: ${v('name')}\nКонтакт: ${v('contact')}\nКомпания: ${v('company')}\nЗадача: ${v('task')}\nИнтересы: ${interests}\nСтраница: ${location.href}`;
      location.href = 'mailto:info@social-stars.ai?subject=' + encodeURIComponent('Заявка на AI-аудит') + '&body=' + encodeURIComponent(body);
      form.classList.add('is-done'); $('.form-done', form).focus();
    });
  });
})();

// ролики в макетах телефонов играют только на экране; при «уменьшении движения» — обложка
(() => {
  const vids = document.querySelectorAll('video.media');
  if (!vids.length || matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (e.isIntersecting) { v.preload = 'auto'; const p = v.play(); if (p) p.catch(() => {}); } else v.pause();
  }), { threshold: .25 });
  vids.forEach(v => io.observe(v));
})();
