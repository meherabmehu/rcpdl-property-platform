# Reference inventory

Source: connected Drive folder `1YPmIPFA-5njBWUdlAMh_cMTX-UxhfLwu`, listed and downloaded on 2026-10-23. The actual folder contains exactly the fourteen PNGs below, with no original media or font files. All fourteen boards were visually inspected before implementation. Originals are in `docs/references/`; exact asset extraction bounds are in `tools/extract_assets.py`.

Presentation titles, canvas backgrounds, viewport labels, numbered flow descriptions, and captions outside website frames are excluded from the application.

Status key: **B** = built and browser-captured; **I** = exercised through an interaction; **V** = source frame compared visually. V records a comparison, not approval or pixel equivalence. Known differences remain in `visual-review.md`.

| Source PNG | Screen or state | Reference | Route / interaction | Status |
| --- | --- | --- | --- | --- |
| 01-home | Complete home, header, hero, projects, gallery, visit, contact CTA, footer | Desktop | `/` | B / V |
| 02-projects | Two project cards and visit banner | Desktop | `/projects/` | B / V |
| 02-projects | Stacked project cards, compact banner and footer | Mobile | `/projects/` at 375 | B / V |
| 03-project-01-details | Hero, gallery, summary, location, details to confirm | Desktop | `/projects/1/` | B / V |
| 03-project-01-details | Selected thumbnail | Both | Thumbnail buttons | I |
| 03-project-01-details | Gallery, summary and media cards | Mobile | `/projects/1/` at 390 | B / V |
| 04-project-02-details | Main photo and controls, four thumbnails, summary, sample details, supporting media | Desktop 1440 | `/projects/2/` | B / V |
| 04-project-02-details | Main photo and controls, summary and sample details | Mobile 375 | `/projects/2/` | B / V |
| 05-gallery | Five-image arrangement | Desktop | `/gallery/` | B / V |
| 05-gallery | Four-image vertical arrangement | Mobile | `/gallery/` at 390 | B / V |
| 05-gallery | Selected photo lightbox, previous/next, counter, return and close | Desktop | Photo button; arrows; Escape | B / I / V |
| 06-virtual-site-visit | Selector, panorama mode and large stage | Desktop | `/virtual-site-visit/?project=1&mode=panorama` | B / V |
| 06-virtual-site-visit | Fullscreen stage and exit | Desktop | Fullscreen controls | I |
| 06-virtual-site-visit | Video mode with transcript entry | Mobile | `/virtual-site-visit/?mode=video` | B / V |
| 06-virtual-site-visit | Panorama controls and photo alternative | Mobile | `/virtual-site-visit/?mode=panorama` | B / V |
| 06-virtual-site-visit | Project selection | Both | Project select preserves media mode | I |
| 07-assistant-inquiry | Intro/disclosure dialog over home | Desktop | Ask AI button | B / I / V |
| 07-assistant-inquiry | Chat with project facts and Bangla response | Desktop | Start chat; local message adapter | B / I / V |
| 07-assistant-inquiry | Separate inquiry form | Desktop | `/inquiry/?project=1` | B / I / V |
| 07-assistant-inquiry | Confirmation with project, masked phone and back link | Desktop | Successful local submission | B / I / V |
| 08-about-contact | About hero, copy, CTAs and three images | Desktop | `/about/` | B / V |
| 08-about-contact | About top | Mobile | `/about/` at 375 | B / V |
| 08-about-contact | About supporting images continuation | Mobile | Scroll on `/about/` | B / V |
| 08-about-contact | Contact hero, pending contact cards, photo and form | Desktop | `/contact/` | B / V |
| 08-about-contact | Contact hero and pending contact cards | Mobile | `/contact/` at 375 | B / V |
| 08-about-contact | Contact form continuation | Mobile | Scroll on `/contact/` | B / V |
| 09-privacy-terms | Privacy draft, navigation, six sections and footer | Desktop | `/privacy/` | B / V |
| 09-privacy-terms | Terms draft, navigation, four sections and footer | Desktop | `/terms/` | B / V |
| 09-privacy-terms | Privacy stacked navigation/content | Mobile | `/privacy/` at 375 | B / V |
| 09-privacy-terms | Terms stacked navigation/content | Mobile | `/terms/` at 375 | B / V |
| 10-staff-content | Staff projects table, publication and availability | Desktop | `/staff/` | B / V |
| 10-staff-content | Add project | Desktop | `/staff/projects/add/` | B |
| 10-staff-content | Edit project, EN/BN tabs and fields | Desktop | `/staff/projects/1/edit/` | B / I / V |
| 10-staff-content | Media picker, upload, main image and alt text | Desktop | Editor media controls | I |
| 10-staff-content | Save draft and draft feedback | Desktop | Save draft button, session storage | I |
| 10-staff-content | Preview | Desktop | Editor Preview dialog | I |
| 10-staff-content | Review checklist and publication note | Desktop | `/staff/projects/1/review/` | B / I / V |
| 10-staff-content | Publication confirmation/result | Desktop | Complete all checkboxes; Publish revision | I |
| 11-staff-access-inquiries | Staff sign-in and password visibility | Desktop | `/staff/sign-in/` | B / I / V |
| 11-staff-access-inquiries | Forgot-password entry | Desktop | `/staff/forgot-password/` | B / I |
| 11-staff-access-inquiries | MFA challenge | Desktop | `/staff/mfa/` after sign-in | B / I / V |
| 11-staff-access-inquiries | MFA invalid code | Desktop | Incorrect code; `?scenario=invalid-code` | B / I / V |
| 11-staff-access-inquiries | Recovery-code entry | Desktop | `/staff/mfa/?recovery=1` | B / I |
| 11-staff-access-inquiries | Inquiry inbox | Desktop | `/staff/inquiries/` | B / V |
| 11-staff-access-inquiries | Inquiry detail and masked phone | Desktop | `/staff/inquiries/1/` | B / V |
| 11-staff-access-inquiries | Phone reveal/hide | Desktop | Reveal phone button; synthetic data | I |
| 11-staff-access-inquiries | Status selection and save feedback | Desktop | Save status | I |
| 12-staff-faqs-contacts | FAQ list and selected FAQ | Desktop | `/staff/faqs/` | B / I / V |
| 12-staff-faqs-contacts | Add/edit FAQ, EN/BN and draft | Desktop | FAQ editor; Add new FAQ | I |
| 12-staff-faqs-contacts | FAQ preview, review and publish | Desktop | Editor actions and checklist dialog | I |
| 12-staff-faqs-contacts | Public contact editor and preview | Desktop | `/staff/contacts/` | B / I / V |
| 12-staff-faqs-contacts | Contact checklist and save feedback | Desktop | Save draft / Review and publish | I |
| 13-mobile-bangla | English compact home | Mobile | `/` at 390 | B / V |
| 13-mobile-bangla | Bangla compact home | Mobile | Set language `bn`, `/` | B / I / V |
| 13-mobile-bangla | Bangla Project 01, media and gallery | Mobile | Set language `bn`, `/projects/1/` | B / V |
| 13-mobile-bangla | Bangla inquiry | Mobile | Set language `bn`, `/inquiry/?project=1` | B / V |
| 14-feedback-recovery | Invalid phone | Desktop | `/inquiry/?scenario=invalid-phone` | B / I / V |
| 14-feedback-recovery | Sending/disabled submit | Desktop | `/inquiry/?scenario=sending` | B / I / V |
| 14-feedback-recovery | Failure, retained inputs, retry and edit | Desktop | `/inquiry/?project=2&scenario=failure` | B / I / V |
| 14-feedback-recovery | AI unavailable | Desktop | `/assistant/?scenario=ai-unavailable` | B / I / V |
| 14-feedback-recovery | Media failed, retry and photos | Desktop | `/virtual-site-visit/?scenario=media-failure` | B / I / V |
| 14-feedback-recovery | Staff access restricted | Desktop | `/staff/restricted/` | B / I / V |

Only board 04 supplies explicit 1440/375 dimensions. Other frame viewports are inferred: home desktop 1024 (the original frame width), most public desktop 1440; About/Contact/legal desktop 1024, compact assistant flow 460, mobile 375 or 390, staff desktop 1024. Bounds and actual capture viewports are recorded in `tools/verify_browser.py` and `verification/browser-report.json`. The generated boards have inconsistent relative typography and some contradictory compositions, so these are documented choices, not original design-file measurements.

The correction pass adds distinct generated full equirectangular textures and a working spherical viewer; missing video still uses a visible fallback. See [completion review](completion-review.md) for local review links, protected draft/published previews, actual asset dimensions, panorama measurements and the complete responsive matrix. No external AI, contact delivery, global publication, map or recovery service is connected.
