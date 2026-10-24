# Completion review — 24 October 2026

The fourteen original Drive PNG boards were downloaded again and visually inspected before these corrections. The folder contains only composited boards: no standalone originals, walkthrough video, panorama, design file, or font specification was available. This implementation has been compared against the supplied frames; it is not certified pixel-identical.

## Local review

The current development server is **http://127.0.0.1:8000/**. Open **http://127.0.0.1:8000/dev/** for a separate review index with direct links to every staff screen and recovery state. It is absent from the public navigation and returns 404 when DEBUG is off or on Vercel.

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py setup_demo_staff --username reviewer --generate
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

The local `reviewer` account has already been created. Read its password locally from the ignored **`.env.demo`** file; no password is committed or uploaded. The setup command never replaces an existing account or credentials file. A normal Django staff user is sufficient; a superuser is not required. The local demonstration checkpoint accepts `123456`, or `DEMO-RECOVERY` in recovery mode. Both codes are disabled on Vercel even if DEBUG is accidentally enabled. Anonymous deep links return through sign-in and the checkpoint to the original staff screen. Non-staff users receive HTTP 403. Sign-out requires POST and CSRF.

## Screen checklist and direct paths

Prefix paths below with `http://127.0.0.1:8000`. All application routes have stable Django names in `website/urls.py`.

| Board | Implemented review targets |
| --- | --- |
| 01–09 | `/`, `/projects/`, `/projects/1/`, `/projects/2/`, `/gallery/`, `/virtual-site-visit/`, `/assistant/`, `/inquiry/`, `/about/`, `/contact/`, `/privacy/`, `/terms/` |
| 10 | `/staff/`, `/staff/projects/add/`, `/staff/projects/1/edit/`, `/staff/projects/2/edit/`, `/staff/projects/1/review/` |
| 10 previews | `/staff/projects/1/preview/?version=draft` and `?version=published`; both require staff access |
| 11 | `/staff/sign-in/`, `/staff/mfa/`, `/staff/mfa/?scenario=invalid-code`, `/staff/mfa/?recovery=1`, `/staff/forgot-password/`, `/staff/inquiries/`, `/staff/inquiries/1/`, `/staff/inquiries/2/` |
| 12 | `/staff/faqs/`, `/staff/contacts/` |
| 13 | EN/Bangla home, Project 01 and inquiry through the actual language buttons; page and query parameters persist |
| 14 validation | `/inquiry/?project=1&scenario=invalid-phone` |
| 14 sending | `/inquiry/?project=1&scenario=sending` |
| 14 failure/retry | `/inquiry/?project=2&scenario=failure` |
| 14 AI unavailable | `/assistant/?scenario=ai-unavailable` |
| 14 media failure | `/virtual-site-visit/?scenario=media-failure`; Retry opens the working panorama |
| 14 restricted | `/staff/restricted/` after local sign-in, HTTP 403 |

Staff project drafts, uploaded image data, inquiry statuses, FAQs and contacts persist in this browser's `sessionStorage`. Project publication saves a **separate reviewed snapshot**. Draft edits subsequently leave it unchanged; protected full-page previews allow comparing both versions. Newly published demo projects appear in the staff table and remain editable. FAQ EN/Bangla values are stored per record, including newly added FAQs. FAQ/contact publication also saves separate snapshots, accessible with “View published snapshot.”

This is a frontend demonstration: public visitor content stays the illustrative reference fixture, and browser snapshots do not publish globally. Vercel staff login remains unavailable until a persistent database and production authentication are configured. No submitted inquiry data is delivered or retained. Password reset sends no email; AI answers come from a deterministic local fixture. These limits are identified in the UI.

## Media audit

All extracted originals are preserved in `static/images/`; intrinsic sizes are recorded in `website/image_manifest.json`. The tiny originals caused blur when enlarged: Project 01 was 609×238, Project 02 750×257, hero 669×335, and the visit background 438×164. Aerials, narrow secondary photos, map and company image still use source-board crops because separate original assets do not exist.

The completion brief explicitly authorized generated faithful replacements. Five new illustrative assets were generated using the extracted images as visual references:

| Generated original | Actual native dimensions | Use |
| --- | --- | --- |
| `ground-01.png` | 2006×784 | Grass, white boundary posts, Project 01 cards and primary photos |
| `ground-02.png` | 2139×735 | Sandy walled plot, Project 02 cards and primary photos |
| `hero.png` | 1774×887 | Sunset home hero |
| `panorama-01.png` | 1774×887 | Full spherical illustrative green site |
| `panorama-02.png` | 1774×887 | Full spherical illustrative sandy walled site |

Native PNGs live in `docs/assets/generated/`. Full prompts, reference filenames and actual output dimensions are in `docs/generated-assets.json`. Requested generation dimensions were larger than the tool returned; the table reports the actual outputs. There is no claim that missing photographic detail was recovered, that generated scenes depict a surveyed property, or that the outputs are 4K.

`tools/build_responsive_assets.py` exports downscaled WebP variants at 320/640/960/1440/native width without upscaling. Primary image tags use `srcset`, `sizes`, intrinsic width/height and asynchronous decoding; below-fold images are lazy loaded. CSS crops preserve the reference compositions where possible. Source-only small alternate/aerial/map assets remain visibly soft when enlarged. Generated surroundings and fine features differ from the original board crops.

## Working panorama

Pannellum **2.5.6** is vendored with its license under `static/vendor/pannellum/`; runtime use requires no CDN or API key. Each project has a distinct 2:1 full equirectangular texture. The spherical camera provides all horizontal directions and vertical viewing, rather than translating a flat photograph.

- Mouse drag and CDP-emulated touch drag changed the actual viewer yaw.
- Zoom, reset, fullscreen entry/exit, project switching and photo/back navigation work. There is no autorotation.
- Loading, real image/network/graphics failure, Retry and photo fallback are implemented. Verification deliberately requests a missing panorama, restores the valid URL, and confirms successful retry.
- Screenshots at yaw 0°, 90°, +179°, −179° and −90° were captured for both projects. The ±179° rendered seam views were visually inspected; there is no black gap or abrupt exposure boundary. Synthesized foliage/wall geometry and polar stretching remain illustrative approximations. No claim of an exact photographic stitch is made.
- Native panorama width is only 1774 pixels: at a 100° field of view, roughly 493 horizontal source pixels fill the screen. Large fullscreen views therefore remain soft. Higher-resolution actual 360 captures would improve that limit.
- Walkthrough video and transcript were not supplied. Video mode gives an explicit unavailable state and real photo/panorama alternatives; it does not simulate playback.

## Verification and comparison artifacts

Run the development server, install `requirements-dev.txt`, then:

```powershell
$env:VERIFY_URL='http://127.0.0.1:8000'
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test
.venv\Scripts\python.exe manage.py collectstatic --noinput
.venv\Scripts\python.exe tools/verify_browser.py
.venv\Scripts\python.exe tools/verify_completion.py
.venv\Scripts\python.exe tools/review_contact_sheets.py
```

The Django suite has **14 passing tests**. The reference browser suite captures **45 routes/states**, executes **18 interaction groups**, and reports zero JavaScript exceptions. The completion suite checks **19 routes at all nine requested widths: 320, 375, 390, 430, 768, 1024, 1280, 1440 and 1920** (171 checks), plus 844×390 landscape, 1024×600 short screens, 320×568, and a staff editor at 200% CSS browser zoom. Staff tables deliberately scroll within their own wrapper. Emulation is not a physical-device or cross-browser certification.

The completion suite also checks actual panorama interaction/recovery, login return paths, published-versus-draft separation and FAQ row isolation. Temporary random staff accounts are deleted after each run. Secrets are never printed.

- `docs/verification/browser-report.json`: routes, actual viewport sizes, source frame bounds, diagnostic pixel differences and interactions.
- `docs/verification/completion-report.json`: the width matrix, panorama yaw measurements and additional checks.
- `docs/verification/screenshots/`: full-size source-screen captures; `completion/` contains yaw, fullscreen, responsive and zoom evidence.
- `docs/verification/comparisons/`: source on left/rendered page on right, overlays, pixel diffs and eight contact sheets.

Large screenshot artifacts are reproducible and ignored by Git. Their source frames come from the fourteen original Drive boards, not generated expected screenshots. Staff boards 10/11/12 and all six board-14 states are included. Reference pairs were visually inspected, including staff/editor/FAQ/inquiries, sign-in/MFA/restricted and virtual visit. Pixel scores are diagnostic, never a claim of exact visual acceptance.

## Remaining visible differences

Generated photos reproduce the composition approximately; exact photographic pixels, camera geometry and some vegetation/buildings differ. Small original alternate photos and aerials remain limited by source resolution. Local Roboto/Noto Sans Bengali are licensed substitutes for an unidentified reference font. Some small icons, header proportions, staff form spacing, legal-page vertical rhythm and mobile inquiry spacing still differ. The real panorama and explanatory demo labels add behavior/copy absent from static source frames. Approved company contact information, map coordinates, final policies, production publishing/authentication, actual video/transcript and actual site panoramas remain external content/integration needs.

Repository: https://github.com/meherabmehu/rcpdl-property-platform

Updated live deployment: https://rcpdl-property-platform.vercel.app/ . The production browser check passed all 13 routes and six interaction/asset groups with zero JavaScript exceptions. It also confirmed a real panorama yaw change from mouse drag, CDN asset delivery, and disabled development index/error fixtures. The saved result is `docs/verification/deployment-report.json`.

Implementation commits: `10ab895` responsive media; `4db70e1` staff access/snapshots; `db14e97` spherical viewer; `86fe0a3` staff icons/responsive controls. Final verification and documentation are recorded in a subsequent commit.
