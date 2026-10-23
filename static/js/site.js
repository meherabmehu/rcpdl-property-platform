/* Local, deterministic frontend demonstrations. No external messaging or AI calls. */
(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const scenario = document.body.dataset.scenario;
  const project = document.body.dataset.project || '1';
  const bn = document.documentElement.lang === 'bn';
  const toast = message => { const el = $('.toast'); if (!el) return; el.textContent = message; el.hidden = false; clearTimeout(el.timer); el.timer = setTimeout(() => el.hidden = true, 4500); };
  const open = id => { const dialog = document.getElementById(id); if (!dialog) return; if (dialog.open) return; dialog.showModal(); };
  $$('[data-open]').forEach(b => b.addEventListener('click', () => open(b.dataset.open)));
  $$('[data-close]').forEach(b => b.addEventListener('click', () => b.closest('dialog').close()));
  $$('dialog').forEach(d => d.addEventListener('click', e => { if (e.target === d && !d.classList.contains('lightbox')) { const r = d.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) d.close(); } }));
  $$('[data-notice]').forEach(b => b.addEventListener('click', () => { $('.notice-copy').textContent = b.dataset.notice; open('notice-dialog'); }));
  $('[data-start-chat]')?.addEventListener('click', () => { $('#ai-intro').close(); open('chat-dialog'); });
  const menu = $('.menu-toggle');
  const closeMenu = () => { $('#navigation')?.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); };
  menu?.addEventListener('click', () => { const shown = menu.getAttribute('aria-expanded') !== 'true'; $('#navigation').classList.toggle('open', shown); menu.setAttribute('aria-expanded', String(shown)); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });
  document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(); });
  $$('.thumbnail').forEach((b, i) => b.addEventListener('click', () => { const main = $('#main-photo') || $('.feedback-layout .main-photo img'); if (!main) return; main.src = b.dataset.image; main.alt = b.getAttribute('aria-label'); $$('.thumbnail').forEach(t => { t.classList.remove('selected'); t.setAttribute('aria-pressed', 'false'); }); b.classList.add('selected'); b.setAttribute('aria-pressed', 'true'); if ($('.image-count')) $('.image-count').textContent = `${i + 1} / ${$$('.thumbnail').length}`; }));
  let photos = []; try { photos = JSON.parse($('#gallery-data')?.textContent || '[]'); } catch { /* no gallery on staff pages */ }
  let index = 0; let activePhotos = photos;
  const showPhoto = () => { const p = activePhotos[index]; if (!p) return; $('.viewer-image').src = p.src; $('.viewer-image').alt = p.caption; $('.viewer-caption').textContent = p.caption; $('.viewer-count').textContent = `${index + 1} / ${activePhotos.length}`; };
  $$('[data-gallery]').forEach(b => b.addEventListener('click', () => { activePhotos = photos; index = Number(b.dataset.gallery); showPhoto(); open('photo-viewer'); }));
  $$('[data-photo-src]').forEach(b => b.addEventListener('click', () => { activePhotos = $$('[data-photo-src]').map(el => ({src: el.dataset.photoSrc, caption: el.dataset.caption})); index = $$('[data-photo-src]').indexOf(b); showPhoto(); open('photo-viewer'); }));
  const changePhoto = delta => { index = (index + delta + activePhotos.length) % activePhotos.length; showPhoto(); };
  $('.viewer-prev')?.addEventListener('click', () => changePhoto(-1)); $('.viewer-next')?.addEventListener('click', () => changePhoto(1));
  $('#photo-viewer')?.addEventListener('keydown', e => { if (e.key === 'ArrowRight') changePhoto(1); if (e.key === 'ArrowLeft') changePhoto(-1); });
  async function postForm(form, extra = {}) { const data = new FormData(form); Object.entries(extra).forEach(([k,v]) => data.set(k,v)); const res = await fetch(form.action, {method: 'POST', body: data, credentials: 'same-origin'}); const result = await res.json(); return {res, result}; }
  const success = (form, result) => {
    const parent = form.closest('.inquiry-card');
    parent.replaceChildren(); parent.classList.add('confirmation');
    const heading = document.createElement('div'); heading.className = 'dialog-heading';
    heading.innerHTML = '<div class="success-mark">✓</div><div><h2>Inquiry received</h2><p>Thank you for your inquiry.<br>We have received your message.</p></div>';
    const facts = document.createElement('div'); facts.className = 'confirmation-data';
    [['Project', result.project], ['Your submitted number', result.phone], ['Company contact', 'Pending confirmation']].forEach(([label, value]) => { const p = document.createElement('p'); p.textContent = label; const b = document.createElement('strong'); b.textContent = value; p.append(b); facts.append(p); });
    const a = document.createElement('a'); a.className = 'button'; a.href = `/projects/${result.project_id}/`; a.textContent = 'Back to project →'; parent.append(heading, facts, a); parent.tabIndex = -1; parent.focus();
  };
  $$('.inquiry-form').forEach(form => {
    const submit = $('button[type=submit]', form), error = $('.form-error', form), edit = $('.edit-details', form);
    const initial = submit.innerHTML; let busy = false; let failedOnce = false;
    const fail = message => { error.textContent = message; error.hidden = false; submit.textContent = 'Retry →'; edit.hidden = false; };
    const clear = () => { error.hidden = true; $$('.error-message', form).forEach(x => x.textContent = ''); $$('.invalid', form).forEach(x => {x.classList.remove('invalid'); x.removeAttribute('aria-invalid');}); };
    edit.addEventListener('click', () => { clear(); submit.innerHTML = initial; edit.hidden = true; $('[name=phone]', form).focus(); });
    if (['invalid-phone', 'sending', 'failure'].includes(scenario)) {
      $('[name=name]', form).value = 'Tanvir Ahmed'; $('[name=phone]', form).value = scenario === 'invalid-phone' ? '01XXX 12' : '01700000123'; $('[name=message]', form).value = 'I would like to know more about this project.';
      if (scenario === 'invalid-phone') { const phone = $('[name=phone]', form); phone.classList.add('invalid'); phone.setAttribute('aria-invalid', 'true'); $('.error-message', form).textContent = 'Enter a valid phone number.'; error.textContent = 'Check your phone number.'; error.hidden = false; }
      if (scenario === 'failure') { failedOnce = true; fail('Your inquiry was not sent. Your entries are kept on this screen.'); }
      if (scenario === 'sending') { submit.disabled = true; submit.textContent = '◯ Sending...'; busy = true; }
    }
    form.addEventListener('submit', async e => {
      e.preventDefault(); if (busy) return; clear();
      const phone = $('[name=phone]', form), selected = $('[name=project]', form);
      const digits = phone.value.replace(/[০-৯]/g, x => String('০১২৩৪৫৬৭৮৯'.indexOf(x))).replace(/[\s()-]/g, '');
      if (!/^(?:\+?88)?01[3-9]\d{8}$/.test(digits)) { error.hidden = false; error.textContent = 'Check your phone number.'; phone.classList.add('invalid'); phone.setAttribute('aria-invalid', 'true'); $('.error-message', form).textContent = 'Enter a valid phone number.'; phone.focus(); return; }
      if (!selected.value) { error.hidden = false; error.textContent = 'Select a project.'; selected.classList.add('invalid'); selected.setAttribute('aria-invalid','true'); selected.focus(); return; }
      busy = true; submit.disabled = true; submit.textContent = bn ? 'পাঠানো হচ্ছে...' : '◯ Sending...';
      try {
        await new Promise(r => setTimeout(r, 650));
        // First submit under failure scenario fails; an explicit Retry succeeds.
        const forceFailure = scenario === 'failure' && !failedOnce;
        const {res, result} = await postForm(form, {scenario: forceFailure ? 'failure' : ''});
        if (res.ok && result.ok) success(form, result); else { failedOnce = true; fail(result.error || 'Check your phone number and selected project.'); }
      } catch { failedOnce = true; fail('Your inquiry was not sent. Your entries are kept on this screen.'); }
      finally { busy = false; submit.disabled = false; if (submit.textContent.includes('Sending') || submit.textContent.includes('পাঠানো')) submit.innerHTML = initial; }
    });
  });
  $$('.chat-form').forEach(form => form.addEventListener('submit', async e => {
    e.preventDefault(); const input = $('[name=message]', form), button = $('button', form), log = $('.chat-log', form.parentElement); const message = input.value.trim(); if (!message || button.disabled) return;
    const add = (text, user = false) => { const b = document.createElement('div'); b.className = `chat-bubble${user ? ' user' : ''}`; b.textContent = text; log.append(b); log.scrollTop = log.scrollHeight; };
    add(message, true); button.disabled = true;
    try { const {res,result} = await postForm(form, {project, scenario}); if (!res.ok) throw Error();
      if (result.project && !/[\u0980-\u09ff]/.test(message)) {
        const p = result.project, bubble = document.createElement('div'); bubble.className = 'chat-bubble project-answer';
        const title = document.createElement('p'); title.textContent = `${p.name} details:`;
        const area = document.createElement('p'); area.textContent = `${p.katha} katha · ${p.sqft} sq ft`;
        const price = document.createElement('p'); price.className = 'price'; price.textContent = `৳${p.price}`;
        const total = document.createElement('small'); total.textContent = 'Total price';
        const badge = document.createElement('span'); badge.className = 'badge'; badge.textContent = 'Available';
        bubble.append(title,area,price,total,badge); log.append(bubble); log.scrollTop = log.scrollHeight;
      } else add(result.answer);
      input.value = ''; }
    catch { add('AI assistant is unavailable right now. Please try again later.'); const a = document.createElement('a'); a.href = `/inquiry/?project=${project}`; a.textContent = 'Send an inquiry →'; log.append(a); }
    finally {button.disabled = false; input.focus();}
  }));
  const stage = $('#media-stage');
  if (stage) {
    const params = new URLSearchParams(location.search);
    const mode = params.get('mode') || 'panorama';
    const setMode = m => { const panorama = m === 'panorama'; $$('.panorama-controls,.panorama-hint').forEach(x => x.hidden = !panorama); $$('.stage-play,.video-controls,.video-description').forEach(x => x.hidden = panorama); $('.photo-alternative').hidden = !panorama; $$('[data-mode]').forEach(b => { b.classList.toggle('outline', b.dataset.mode !== m); b.setAttribute('aria-pressed', String(b.dataset.mode === m)); }); const url = new URL(location.href); url.searchParams.set('mode',m); history.replaceState({},'',url); };
    setMode(mode); $$('[data-mode]').forEach(b => b.addEventListener('click', () => { setMode(b.dataset.mode); $('.media-fallback').hidden = false; }));
    $('#visit-project').addEventListener('change', e => { const url = new URL(location.href); url.searchParams.set('project', e.target.value); location.href = url; });
    const fallback = () => { $('.media-fallback').hidden = false; };
    $$('.stage-play,[data-media-fallback],.retry-media').forEach(b => b.addEventListener('click', fallback));
    $('.video-controls input')?.addEventListener('input', fallback);
    if (scenario === 'media-failure') fallback();
    $$('.fullscreen-toggle').forEach(b => b.addEventListener('click', async () => { try { if (document.fullscreenElement) await document.exitFullscreen(); else await stage.requestFullscreen(); } catch { toast('Fullscreen is unavailable in this browser.'); } }));
    document.addEventListener('fullscreenchange', () => { $('.stage-top .fullscreen-toggle').textContent = document.fullscreenElement ? '⛶ Exit fullscreen' : '⛶ Fullscreen'; });
  }
  // Any actual network image error receives the same recoverable fallback.
  $$('main img').forEach(img => img.addEventListener('error', () => { if (img.dataset.failed) return; img.dataset.failed = '1'; const box = document.createElement('div'); box.className = 'media-fallback'; const message = document.createElement('p'); message.textContent = 'This media could not load.'; const retry = document.createElement('button'); retry.className = 'button'; retry.textContent = 'Retry media →'; retry.addEventListener('click', () => { img.dataset.failed = ''; img.hidden = false; box.remove(); const u = new URL(img.src); u.searchParams.set('retry',Date.now()); img.src = u.href; }); box.append(message,retry); img.hidden = true; img.after(box); }));
  window.rcDemo = {toast, open};
})();
