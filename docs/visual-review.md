# Current completion audit

See [24 October correction and verification handoff](completion-review.md) for the current image replacements, working spherical viewer, staff snapshots and full nine-width matrix. The historical observations below describe the initial reproduction; missing panorama and no-generated-photo observations have since been addressed. Remaining font, small source-crop and spacing limitations still apply.

# Visual review and verification

Reviewed on 2026-10-23. The fourteen supplied PNG boards are the source of truth. All were opened visually before implementation. See [screen/state inventory](reference-inventory.md) and `tools/verify_browser.py` for individual frame bounds and viewport choices.

Latest successful browser run: **45 route/viewport captures, 18 interaction check groups, 44 source comparison pairs, zero JavaScript errors, zero failed requests**. Additional interaction screenshots are saved alongside route captures.

## Checks performed

- Django 5.2.18 on Python 3.14.7: `manage.py check` passed with no issues.
- `manage.py test`: nine tests passed. Includes public rendering, correct project facts, phone validation, Bangla digits, optional fields, inquiry failure/success, CSRF enforcement, local assistant facts, explicit development scenarios, locale preservation, real Django authentication, staff permissions, invalid MFA and local recovery.
- Migrations and `collectstatic --noinput` succeeded.
- Fresh `.venv-smoke` installed **only** `requirements.txt`. All migrations succeeded against a new SQLite file in ignored `test-results/`. Django checks passed; both Django's test client and a separate development server returned HTTP 200 for `/`.
- Headless Microsoft Edge via Playwright captured public desktop/mobile pages, Bangla screens, staff screens and feedback states. Route, viewport, source-frame bounds, HTTP status, overflow, broken-image findings and comparison metrics are in [browser-report.json](verification/browser-report.json).
- Eleven public routes were checked at 375, 390, 768, 1024 and 1440 pixels for horizontal overflow. Six staff routes were additionally checked at 390 pixels. These checks pass.
- Interaction checks cover mobile navigation/Escape, selected thumbnails, lightbox/arrow keys/Escape, assistant disclosure/chat/close, deterministic project responses, inquiry validation/loading/confirmation/retry, fullscreen entry/exit, real local sign-in/password visibility, invalid MFA and recovery, EN/BN editor tabs, draft persistence, preview/checklist/publication, synthetic phone reveal/status, FAQ add/edit/save/review, public contact preview, image upload/main-image selection/alt text.
- Browser report records zero JavaScript exceptions and zero failed network requests in the successful run. Expected recovery screens are explicit scenarios, not network failures introduced randomly.

## Comparison artifacts

Generated locally, intentionally excluded from Git because they are reproducible and large:

- `docs/verification/screenshots/`: actual browser screenshots.
- `docs/verification/comparisons/*-reference.png`: website frame extracted from the supplied board.
- `*-side-by-side.jpg`: source on the left, rendered page on the right.
- `*-overlay.png`: 50% overlay, aligned to the top and scaled by width.
- `*-diff.png`: absolute pixel difference.
- `review-sheet-*.jpg`: contact sheets for reviewing multiple comparisons.

The visual review used the supplied frames, not implementation-generated golden images. Source boards contain no design-file measurements. Only board 04 explicitly labels 1440/375px. Other dimensions are inferred and documented; About/Contact and staff use 1024px desktop captures, the compact assistant flow uses 460px, most other public desktop captures use 1440px. Home uses its actual 1024px source-frame width. A large pixel difference is not treated as a passing visual score.

The screenshot script prints the route-capture and interaction-group counts after a successful run. It also saves additional screenshots during interactions (for example disclosure, conversation, confirmation and invalid MFA), so the screenshot file count exceeds the route-capture count. Prior-run captures can remain in the ignored directory.

## Corrections from comparison

The review corrected home card images, gallery content/order, home spacing, the mobile media/gallery section on Project 01, the distinct Project 02 summary and supporting-media layout, responsive header/footer behavior, Bangla project/inquiry composition, mobile current-language labels, About hero sizing, virtual-visit proportions, gallery lightbox proportions, the staff inquiry header/sidebar variant, and standalone media-recovery composition. Interface code was formatted for review.

## Remaining differences and unavailable materials

This is a functioning frontend demonstration with known visual differences. It is **not a completed exact-match certification**.

1. **Original photography is unavailable.** Only raster boards were supplied. Extracted clean photo regions omit pixels obscured by headings, buttons, labels or gradients. Full hero and panoramic crops cannot be recovered exactly from those regions. Some page photos have noticeably different crops/sharpness, particularly the home/visit backgrounds, tall contact photograph, gallery aerials and narrow thumbnail regions.
2. **Font identity is unverified.** Roboto and Noto Sans Bengali are licensed local substitutes. Glyph widths, heading weight, line breaks, currency glyphs and Bangla shaping/spacing therefore differ from the raster samples.
3. **Icon artwork is incomplete.** The exact supplied raster logo is reused. Robot, envelope and chat glyphs are local SVG approximations; several other controls use Unicode/CSS. Their shapes differ from the reference. MFA reproduces six input boxes with paste, arrow-key and backspace support.
4. **Spacing and proportions still differ.** Header/logo scale, gallery row heights, legal-page vertical rhythm, some staff form/table spacing, assistant-dialog placement and mobile inquiry spacing are not pixel-equivalent. Source boards themselves use different header compositions; page-specific variants reproduce their broad structure.
5. **Media/integration exceptions are intentional and visible.** No video, transcript or equirectangular panorama was supplied. Media controls lead to fallback/information/photo alternatives; they do not fabricate a real tour. A short local-demonstration label was added to the AI disclosure to avoid implying an existing external integration. Staff publication/recovery messages also identify local demonstration behavior.
6. **Some reference states are composited illustrations.** Chat timestamps and sample phone text in the board are not a live service. The demo uses valid synthetic phone input, a masked confirmation, deterministic project data and dynamic messages. The lightbox navigates all five gallery assets even though the illustrated desktop counter says `1 / 3`. Contact permission remains initially unchecked on normal forms.
7. **Bangla coverage.** Supplied home/detail/inquiry wording is transcribed. Other UI labels have consistent translations. The reference draft legal body and pending company introduction remain English; no approved Bangla legal/company text was supplied.

Approved company contacts, map coordinates, ownership/land-use details, final legal policies and production authentication/MFA/recovery remain unprovided. The application keeps these pending. No real messages or public content were sent/published.
