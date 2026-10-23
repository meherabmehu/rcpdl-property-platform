(() => {
    'use strict';
    const $ = (s, root = document) => root.querySelector(s);
    const $$ = (s, root = document) => [...root.querySelectorAll(s)];
    const toast = text => window.rcDemo.toast(text);
    const read = key => {
        try {
            return JSON.parse(sessionStorage.getItem(`rc-demo-${key}`) || '{}');
        } catch {
            return {};
        }
    };
    const write = (key, data) => {
        try {
            sessionStorage.setItem(`rc-demo-${key}`, JSON.stringify(data));
            return true;
        } catch {
            toast('Draft storage is unavailable in this browser.');
            return false;
        }
    };
    // Six visible OTP fields feed the same Django form field used by the demo view.
    const codeInput = $('#code[maxlength="6"]');
    if (codeInput) {
        codeInput.type = 'hidden';
        codeInput.required = false;
        const group = document.createElement('div');
        group.className = 'mfa-digits';
        group.setAttribute('role', 'group');
        group.setAttribute('aria-label', '6-digit verification code');
        const digits = Array.from({length: 6}, (_, i) => {
            const field = document.createElement('input');
            field.type = 'text'; field.inputMode = 'numeric'; field.maxLength = 1;
            field.required = true; field.pattern = '[0-9]'; field.dataset.codeDigit = i;
            field.setAttribute('aria-label', `Digit ${i + 1} of 6`);
            field.autocomplete = i === 0 ? 'one-time-code' : 'off';
            group.append(field); return field;
        });
        const sync = () => {codeInput.value = digits.map(field => field.value).join('');};
        digits.forEach((field, i) => {
            field.addEventListener('input', () => {field.value = field.value.replace(/\D/g, '').slice(-1); sync(); if (field.value) digits[i+1]?.focus();});
            field.addEventListener('keydown', e => {if (e.key === 'Backspace' && !field.value) digits[i-1]?.focus(); if (e.key === 'ArrowLeft') digits[i-1]?.focus(); if (e.key === 'ArrowRight') digits[i+1]?.focus();});
            field.addEventListener('paste', e => {const text = e.clipboardData.getData('text').replace(/\D/g, '').slice(0,6); if (!text) return; e.preventDefault(); [...text].forEach((digit,j) => {if (digits[i+j]) digits[i+j].value = digit;}); sync(); digits[Math.min(i+text.length,5)].focus();});
        });
        codeInput.after(group); digits[0].focus();
    }
    $('.show-password')?.addEventListener('click', e => {
        const input = $('#password');
        const show = input.type === 'password';
        input.type = show ? 'text' : 'password';
        e.currentTarget.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    });
    $$('.editor-tabs').forEach(tabs => {
        const form = tabs.closest('form');
        const activate = button => {
            $$('[data-tab]', tabs).forEach(b => {
                b.setAttribute('aria-selected', String(b === button));
                b.tabIndex = b === button ? 0 : -1;
            });
            $$('[data-language]', form).forEach(p => p.hidden = p.dataset.language !== button.dataset.tab);
        };
        $$('[data-tab]', tabs).forEach(b => {
            b.addEventListener('click', () => activate(b));
            b.addEventListener('keydown', e => {
                if (!['ArrowLeft', 'ArrowRight'].includes(e.key)) return;
                e.preventDefault();
                const buttons = $$('[data-tab]', tabs);
                const next = buttons[(buttons.indexOf(b) + 1) % buttons.length];
                activate(next);
                next.focus();
            });
        });
    });
    const serialize = form => {
        const data = {};
        new FormData(form).forEach((value, key) => {
            if (typeof value === 'string') data[key] = value;
        });
        return data;
    };
    const preview = form => {
        const data = serialize(form);
        const box = $('.preview-content');
        box.replaceChildren();
        const title = document.createElement('h3');
        title.textContent = data.title_en || data.question_en || data.contact_name_en || 'Contact our team';
        box.append(title);
        if (data.main_image) {
            const img = document.createElement('img');
            img.src = data.main_image;
            img.alt = data.alt_text || 'Illustrative project image';
            box.append(img);
        }
        const body = document.createElement('p');
        body.textContent = data.description_en || data.answer_en || [data.contact_name_en, data.role_en, data.business_phone, data.address, data.hours].filter(Boolean).join('\n') || 'Company contact pending. Contact details will be shown here after confirmation.';
        box.append(body);
        if (data.katha) {
            const facts = document.createElement('p');
            facts.textContent = `${data.katha} katha · ${data.sqft} sq ft\n${data.price}\n${data.location}\n${data.availability}`;
            box.append(facts);
        }
        window.rcDemo.open('staff-preview');
    };
    const bindMedia = (button, form) => button.addEventListener('click', () => {
        $$('.media-option', form).forEach(b => {
            const selected = b === button;
            b.classList.toggle('selected', selected);
            b.setAttribute('aria-pressed', String(selected));
            $('span', b).textContent = selected ? 'Main image' : 'Set main';
        });
        $('[name=main_image]', form).value = button.dataset.media;
        $('.draft-status', form).textContent = 'Unsaved';
    });
    $$('.demo-editor').forEach(form => {
        const key = form.dataset.draftKey;
        const saved = read(key);
        Object.entries(saved).forEach(([name, value]) => {
            const el = form.elements.namedItem(name);
            if (!el || el.type === 'file') return;
            if (el.type === 'checkbox') el.checked = Boolean(value);
            else el.value = value;
        });
        if (Object.keys(saved).length && $('.draft-status', form)) $('.draft-status', form).textContent = 'Draft saved';
        form.addEventListener('input', () => {
            if ($('.draft-status', form)) $('.draft-status', form).textContent = 'Unsaved';
            if ($('.preview-contact-name')) $('.preview-contact-name').textContent = $('[name=contact_name_en]', form)?.value || 'Company contact pending.';
        });
        const save = () => {
            const saved = write(key, serialize(form));
            if (saved) {
                if (key === 'faqs') {
                    const list = $('.faq-list'),
                        question = $('#question').value,
                        answer = $('#answer').value;
                    let row = $('.faq-row.selected', list);
                    if (!row && question.trim()) {
                        row = document.createElement('button');
                        row.type = 'button';
                        row.className = 'faq-row selected';
                        list.append(row);
                        row.addEventListener('click', () => selectFAQ(row));
                    }
                    if (row && question.trim()) {
                        row.dataset.question = question;
                        row.dataset.answer = answer;
                        row.replaceChildren(document.createTextNode(question));
                        const span = document.createElement('span');
                        span.textContent = '›';
                        row.append(span);
                    }
                    write('faq-list', $$('.faq-row', list).map(b => ({
                        question: b.dataset.question,
                        answer: b.dataset.answer
                    })));
                }
                if ($('.draft-status', form)) $('.draft-status', form).textContent = 'Draft saved';
                toast('Draft saved in this browser session.');
            }
            return saved;
        };
        $('[data-save-draft]', form)?.addEventListener('click', save);
        $('[data-preview]', form)?.addEventListener('click', () => preview(form));
        $$('.media-option', form).forEach(b => bindMedia(b, form));
        $('.media-upload', form)?.addEventListener('change', e => {
            const file = e.target.files[0];
            if (!file) return;
            if (!file.type.startsWith('image/') || file.size > 5 * 1024 * 1024) {
                toast('Choose an image smaller than 5 MB.');
                return;
            }
            const reader = new FileReader();
            reader.onload = () => {
                const b = document.createElement('button');
                b.type = 'button';
                b.className = 'media-option';
                b.dataset.media = reader.result;
                b.setAttribute('aria-label', 'Set uploaded image as main');
                const img = document.createElement('img');
                img.src = reader.result;
                img.alt = file.name;
                const span = document.createElement('span');
                span.textContent = 'Set main';
                b.append(img, span);
                $('.upload-button', form).before(b);
                bindMedia(b, form);
                b.click();
                toast('Image added to local demonstration.');
            };
            reader.readAsDataURL(file);
        });
        form.addEventListener('submit', e => {
            e.preventDefault();
            // Reveal hidden language panels when native validation would target them.
            if (!save()) return;
            if (form.dataset.reviewUrl) {
                location.href = form.dataset.reviewUrl;
                return;
            }
            if (key === 'contacts' && (!form.elements.confirmed.checked || !form.elements.languages_reviewed.checked)) {
                toast('Complete both review checklist items before publishing.');
                return;
            }
            const box = $('.preview-content');
            box.replaceChildren();
            const intro = document.createElement('p');
            intro.textContent = 'Confirm before publishing the draft revision. The current public version remains unchanged until you publish.';
            box.append(intro);
            const review = document.createElement('form');
            review.className = 'publication-review';
            ['Facts approved', 'Both languages reviewed', ...(key === 'contacts' ? [] : ['Content approved'])].forEach(text => {
                const label = document.createElement('label');
                label.className = 'check-label';
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.required = true;
                label.append(checkbox, document.createTextNode(text));
                review.append(label);
            });
            const publish = document.createElement('button');
            publish.className = 'button';
            publish.textContent = 'Publish revision →';
            review.append(publish);
            review.addEventListener('submit', event => {
                event.preventDefault();
                box.replaceChildren();
                const result = document.createElement('div');
                result.className = 'notice success';
                result.textContent = 'Revision published in demonstration state. No public website content was changed.';
                box.append(result);
                write(`${key}-publication`, {
                    published: true
                });
            });
            box.append(review);
            window.rcDemo.open('staff-preview');
        });
    });
    const renderReview = () => {
        const el = $('[data-review-key]');
        if (!el) return;
        const saved = read(el.dataset.reviewKey);
        if (!saved.title_en) return;
        $('h2', el).textContent = saved.title_en;
        $('p', el).textContent = `${saved.katha} katha · ${saved.sqft} sq ft`;
        $('.price', el).textContent = saved.price;
    };
    renderReview();
    $('form.publication-review')?.addEventListener('submit', e => {
        e.preventDefault();
        const form = e.currentTarget;
        form.replaceChildren();
        const result = document.createElement('div');
        result.className = 'notice success';
        result.setAttribute('role', 'status');
        result.innerHTML = '<h2>Revision published</h2><p>Publication completed in local demonstration state. No public website content was changed.</p>';
        const a = document.createElement('a');
        a.className = 'button';
        a.href = '/staff/';
        a.textContent = 'Back to projects →';
        form.append(result, a);
    });
    const selectFAQ = b => {
        $$('.faq-row').forEach(r => r.classList.toggle('selected', r === b));
        $('#question').value = b.dataset.question;
        $('#answer').value = b.dataset.answer;
        $('.faq-editor .draft-status').textContent = 'Draft changes';
    };
    $$('.faq-row').forEach(b => b.addEventListener('click', () => selectFAQ(b)));
    const savedFAQList = read('faq-list');
    if (Array.isArray(savedFAQList) && $('.faq-list')) {
        $$('.faq-row').forEach(b => b.remove());
        savedFAQList.forEach((faq, i) => {
            const row = document.createElement('button');
            row.type = 'button';
            row.className = 'faq-row' + (i === 0 ? ' selected' : '');
            row.dataset.question = faq.question;
            row.dataset.answer = faq.answer;
            row.textContent = faq.question;
            const span = document.createElement('span');
            span.textContent = '›';
            row.append(span);
            $('.faq-list').append(row);
            row.addEventListener('click', () => selectFAQ(row));
        });
    }
    $('[data-add-faq]')?.addEventListener('click', () => {
        $$('.faq-row').forEach(b => b.classList.remove('selected'));
        $('#question').value = '';
        $('#answer').value = '';
        $('#question-bn').value = '';
        $('#answer-bn').value = '';
        $('#question').focus();
        $('.faq-editor h2').textContent = 'Add FAQ';
    });
    $('.reveal-phone')?.addEventListener('click', e => {
        const masked = $('.masked-phone');
        const revealed = masked.textContent === '01700000123';
        masked.textContent = revealed ? '01XXX XXX123' : '01700000123';
        e.currentTarget.textContent = revealed ? 'Reveal phone' : 'Hide phone';
    });
    const detail = $('.inquiry-detail');
    if (detail) {
        const key = `inquiry-${detail.dataset.inquiryId}`;
        const saved = read(key);
        if (saved.status) $('#status').value = saved.status;
        detail.addEventListener('submit', e => {
            e.preventDefault();
            if (write(key, {
                    status: $('#status').value
                })) toast('Inquiry status saved.');
        });
    }
    $$('[data-inquiry-status]').forEach(b => {
        const saved = read(`inquiry-${b.dataset.inquiryStatus}`);
        if (saved.status) b.textContent = saved.status;
    });
})();
