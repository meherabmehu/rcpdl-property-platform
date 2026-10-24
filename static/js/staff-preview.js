(() => {
    const box = document.querySelector('#staff-snapshot');
    if (!box) return;
    let data;
    try { data = JSON.parse(sessionStorage.getItem('rc-demo-' + (box.dataset.version === 'published' ? 'public-' : '') + box.dataset.key) || '{}'); }
    catch { data = {}; }
    if (!data.title_en) { box.querySelector('.snapshot-status').textContent = 'No saved snapshot yet. Showing the reference fixture.'; return; }
    const bn = document.documentElement.lang === 'bn';
    const set = (selector, value) => document.querySelectorAll(selector).forEach(el => el.textContent = value);
    set('.detail-hero h1,.summary-heading h1', data[bn ? 'title_bn' : 'title_en'] || data.title_en);
    set('.detail-hero .container>p:last-child,.summary .location', data.location);
    set('.summary .price', data.price);
    set('.summary .area', `${data.katha} katha · ${data.sqft} sq ft`);
    set('.summary .badge', data.availability);
    set('.about-project p', data[bn ? 'description_bn' : 'description_en']);
    const photo = document.querySelector('#main-photo');
    if (photo && data.main_image) { photo.removeAttribute('srcset'); photo.src = data.main_image; photo.alt = data.alt_text || data.title_en; }
    box.querySelector('.snapshot-status').textContent = box.dataset.version === 'published' ? 'Reviewed published snapshot; subsequent drafts are separate.' : 'Saved draft; publication has not changed.';
})();
