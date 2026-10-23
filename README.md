# RC Property Development Ltd.

A Django-served frontend reproduced from the fourteen supplied design boards. Public pages use template inheritance, reusable partials, local photographs extracted from those boards, local fonts, shared CSS tokens and vanilla JavaScript. The custom staff workspace is separate from the public layout.

## Run locally

Python 3.10–3.14 and Django 5.2.18 LTS. Verified here with Python 3.14.7. Django 5.2 supports Python 3.14 from patch 5.2.8; 5.2.18 is the current 5.2 security patch checked for this work. [Django compatibility](https://docs.djangoproject.com/en/5.2/releases/5.2/), [supported releases](https://www.djangoproject.com/download/).

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. SQLite is local and ignored by Git. No Node server, external API key or frontend build step is needed.

## Staff access

```bash
python manage.py createsuperuser
```

Choose your own local username/password, then visit `/staff/sign-in/`. There are no committed credentials or seeded production accounts. Login validates the actual Django user and requires `is_staff`. The email label follows the reference; enter your Django **username** for local authentication.

In development (`DJANGO_DEBUG=1`, the default), the MFA demonstration accepts `123456`; recovery mode accepts `DEMO-RECOVERY`. These are deliberately documented local UI fixtures, **not a production second factor**. Forgot-password shows feedback and sends no email. With `DJANGO_DEBUG=0`, the fixed MFA codes are disabled. Production authentication, MFA and recovery must be integrated before deployment.

## Routes

| Public | Purpose |
| --- | --- |
| `/` | Home; compact mobile cards |
| `/projects/` | Projects listing |
| `/projects/1/`, `/projects/2/` | Distinct detail layouts |
| `/gallery/` | Gallery and keyboard-accessible lightbox |
| `/virtual-site-visit/?project=1&mode=video` | Video interface and fallback |
| `/virtual-site-visit/?project=2&mode=panorama` | 360° interface and fallback |
| `/assistant/` | Local demonstration conversation |
| `/inquiry/?project=1` | Separate inquiry form and confirmation |
| `/about/`, `/contact/` | Company pages; contact content remains pending |
| `/privacy/`, `/terms/` | Separate reference draft policies |

| Staff | Purpose |
| --- | --- |
| `/staff/` | Project table |
| `/staff/projects/add/` | Add local project draft |
| `/staff/projects/1/edit/` | EN/BN editor, media picker, upload, main image, alt text |
| `/staff/projects/1/review/` | Checklist and publication result |
| `/staff/inquiries/`, `/staff/inquiries/1/` | Synthetic inbox, phone reveal and status |
| `/staff/faqs/` | FAQ list and bilingual editor |
| `/staff/contacts/` | Contact editor, preview and checklist |
| `/staff/sign-in/`, `/staff/mfa/` | Sign-in and MFA demonstration |
| `/staff/mfa/?recovery=1` | Recovery code demonstration |
| `/staff/forgot-password/` | Recovery feedback, no delivery |
| `/staff/restricted/` | Access restriction state, HTTP 403 |

EN/বাংলা buttons POST through Django's `set_language` view. The current URL, selected project and query parameters are preserved. Bangla wording from board 13 is transcribed in the templates. Noto Sans Bengali provides local character shaping. Additional interface translations live in `static/js/language.js`; the draft legal body text remains the supplied English wording.

## Demonstration states

These URL fixtures are deterministic and only active with Django DEBUG enabled:

| URL | State |
| --- | --- |
| `/inquiry/?project=1&scenario=invalid-phone` | Invalid phone and matching errors |
| `/inquiry/?project=1&scenario=sending` | Frozen loading state with disabled submit |
| `/inquiry/?project=2&scenario=failure` | Failure with retained input; Retry succeeds; Edit restores editing |
| `/assistant/?scenario=ai-unavailable` | Assistant unavailable and contact/inquiry alternatives |
| `/virtual-site-visit/?scenario=media-failure` | Missing media with retry/photo actions |
| `/staff/mfa/?scenario=invalid-code` | MFA invalid-code state after sign-in |
| `/staff/restricted/` | Access restricted |

Remove `scenario` to return to the normal flow. Normal inquiry submission shows a short loading state before successful local confirmation. Phone validation accepts Bangladesh mobile numbers, optional country code, separators and Bangla digits. Name/message are optional, phone/project required, contact permission initially unchecked and optional. POST requests use Django CSRF protection. No personal inquiry data is persisted or delivered.

The assistant uses only `website/data.py` and a local deterministic adapter. It makes **no external AI calls**. The supplied AI-service disclosure and draft privacy wording are retained, with an explicit local-demo label added to the introduction.

Staff drafts, FAQ list changes and inquiry statuses use browser `sessionStorage`. Preview and publication actions operate only on demonstration state; they never change the public project fixture. Uploaded files stay in the browser. Browser storage can be cleared to reset the demo; closing the browser session also clears it. The staff inbox contains only labeled synthetic data, including synthetic revealed number `01700000123`.

## Assets and reproduction limits

The Drive folder contains only the fourteen composited PNG boards. It contains no standalone logo, original photographs, font identifiers, videos or equirectangular panoramas. Extracted image regions and logo crops are local; no stock or generated replacement photography is used. Source and extraction coordinates are committed. Run `python tools/extract_assets.py` with development dependencies to reproduce extraction.

Roboto and Noto Sans Bengali are licensed substitutions; their OFL licenses are included. The reference font cannot be positively identified from raster boards. Icons use lightweight local SVG/CSS and some Unicode symbols; these remain an area of visual difference. Hero and other photos have different crops where embedded UI obscures original pixels. Video/360° controls expose the intended interface and an honest fallback; photographs are not represented as real working tours. Approved company contacts, legal policies, location, ownership and project copy remain pending.

See [reference inventory](docs/reference-inventory.md), [visual review](docs/visual-review.md) and [verification report](docs/verification/browser-report.json). The implementation is **not certified as an exact visual match**.

## Verification

```bash
python -m pip install -r requirements-dev.txt
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
python manage.py runserver 127.0.0.1:8001 --noreload
```

In a second activated terminal:

```bash
python tools/verify_browser.py
python tools/review_contact_sheets.py
```

The browser script defaults to installed Microsoft Edge and `http://127.0.0.1:8001`. Override `VERIFY_URL` for another port. To use Playwright's Chromium, run `python -m playwright install chromium` and set `BROWSER_CHANNEL=chromium`. The script creates a randomly named temporary staff user, signs in through the actual UI and deletes that user at the end. It never prints its generated password.

Outputs:

- `docs/verification/screenshots/`: full-page browser captures and interaction states.
- `docs/verification/comparisons/`: extracted source frames, side-by-side images, overlays, absolute pixel diffs and review contact sheets.
- `docs/verification/browser-report.json`: actual run results, viewport/bounds and interaction checks.

Large screenshots/comparisons are generated locally and ignored by Git. The source frames always come from the supplied PNGs, never from implementation-generated golden images. Pixel differences are recorded as diagnostic values, not a visual acceptance threshold. See `docs/visual-review.md` for the checks actually run and remaining differences.

The default settings are for local development. For later integration set a real secret, hosts, deployment security, authentication/recovery and content delivery. No real publishing, contact delivery, payments, map service or AI integration is included.
