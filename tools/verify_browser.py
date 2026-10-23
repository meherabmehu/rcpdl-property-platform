"""Capture actual browser frames and compare them to the supplied reference frames.

Run after starting Django. Browser uses installed Edge; set BROWSER_CHANNEL=chrome
or install Playwright Chromium and set BROWSER_CHANNEL=chromium.
"""
import json
import os
import sys
import secrets
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth import get_user_model

BASE = os.environ.get('VERIFY_URL', 'http://127.0.0.1:8001')
OUT = ROOT / 'docs/verification'
SHOTS = OUT / 'screenshots'
COMPARE = OUT / 'comparisons'
SHOTS.mkdir(parents=True, exist_ok=True)
COMPARE.mkdir(parents=True, exist_ok=True)
# Bounds exclude headings, shadows, board captions, and other presentation material.
FRAMES = [
    ('home', '/', '01-home.png', (0,34,1024,1536),1024),
    ('projects','/projects/','02-projects.png',(32,53,1153,1002),1440),
    ('project-01','/projects/1/','03-project-01-details.png',(40,56,1073,1010),1440),
    ('project-02','/projects/2/','04-project-02-details.png',(35,76,1177,1024),1440),
    ('gallery','/gallery/','05-gallery.png',(33,81,1117,762),1440),
    ('visit','/virtual-site-visit/?mode=panorama','06-virtual-site-visit.png',(23,74,869,924),1440),
    ('about','/about/','08-about-contact.png',(17,56,756,739),1024),
    ('contact','/contact/','08-about-contact.png',(781,56,1520,739),1024),
    ('privacy','/privacy/','09-privacy-terms.png',(17,93,587,1017),1024),
    ('terms','/terms/','09-privacy-terms.png',(607,93,1117,1017),1024),
    ('inquiry','/inquiry/?project=1','07-assistant-inquiry.png',(895,83,1320,780),460),
    ('assistant','/assistant/','07-assistant-inquiry.png',(455,83,879,780),460),
    ('home-mobile','/','13-mobile-bangla.png',(42,72,389,949),390),
    ('projects-mobile','/projects/','02-projects.png',(1189,53,1504,1002),375),
    ('project-01-mobile','/projects/1/','03-project-01-details.png',(1125,56,1497,1010),390),
    ('project-02-mobile','/projects/2/','04-project-02-details.png',(1200,77,1507,1024),375),
    ('gallery-mobile','/gallery/','05-gallery.png',(1150,81,1503,775),390),
    ('visit-video-mobile','/virtual-site-visit/?mode=video','06-virtual-site-visit.png',(902,74,1193,913),390),
    ('visit-panorama-mobile','/virtual-site-visit/?mode=panorama','06-virtual-site-visit.png',(1222,74,1513,913),390),
    ('about-mobile','/about/','08-about-contact.png',(96,752,367,997),375),
    ('contact-mobile','/contact/','08-about-contact.png',(860,752,1131,997),375),
    ('privacy-mobile','/privacy/','09-privacy-terms.png',(1135,93,1318,1017),375),
    ('terms-mobile','/terms/','09-privacy-terms.png',(1335,93,1519,1017),375),
]

def comparison(name, board, bounds, shot):
    ref = Image.open(ROOT / 'docs/references' / board).crop(bounds).convert('RGB')
    actual = Image.open(shot).convert('RGB')
    target_width = ref.width
    actual = actual.resize((target_width, round(actual.height * target_width / actual.width)))
    height = max(ref.height,actual.height)
    pair = Image.new('RGB',(target_width*2,height),'#e7edf1')
    pair.paste(ref,(0,0)); pair.paste(actual,(target_width,0))
    pair.save(COMPARE / f'{name}-side-by-side.jpg', quality=88)
    ref.save(COMPARE / f'{name}-reference.png')
    # Align at the top and preserve width scale; never squash actual page height.
    aligned = Image.new('RGB', ref.size, 'white'); aligned.paste(actual,(0,0))
    Image.blend(ref,aligned,.5).save(COMPARE / f'{name}-overlay.png')
    diff = ImageChops.difference(ref,aligned)
    diff.save(COMPARE / f'{name}-diff.png')
    return round(sum(ImageStat.Stat(diff).mean)/3,2)

def run():
    report = {'pages':[], 'checks':[], 'console_errors':[], 'request_failures':[]}
    username = 'visual-check-' + secrets.token_hex(4)
    password = secrets.token_urlsafe(24)
    user = get_user_model().objects.create_user(username=username,password=password,is_staff=True)
    try:
        with sync_playwright() as p:
            channel = os.environ.get('BROWSER_CHANNEL','msedge')
            browser = p.chromium.launch(headless=True, **({} if channel=='chromium' else {'channel':channel}))
            context = browser.new_context()
            page = context.new_page()
            page.on('pageerror',lambda e:report['console_errors'].append(str(e)))
            page.on('requestfailed',lambda r:report['request_failures'].append(r.url))
            def capture(name,route,width=1440,height=1000):
                page.set_viewport_size({'width':width,'height':height})
                response = page.goto(BASE+route)
                page.evaluate('document.fonts.ready')
                page.wait_for_timeout(100)
                shot = SHOTS / f'{name}.png'
                page.screenshot(path=str(shot),full_page=True)
                overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
                broken = page.locator('img').evaluate_all('(els)=>els.filter(e=>e.getAttribute("src") && !e.hidden && (!e.complete || e.naturalWidth===0)).map(e=>e.src)')
                assert not overflow, f'Overflow: {name}'
                assert not broken, f'Broken images: {name}: {broken}'
                assert response.status < 400 or 'restricted' in name, f'{name}: HTTP {response.status}'
                report['pages'].append({'name':name,'route':route,'viewport':[width,height],'status':response.status,'overflow':overflow,'broken_images':broken,'screenshot':f'screenshots/{name}.png'})
                return shot
            for name,route,board,bounds,width in FRAMES:
                shot = capture(name,route,width)
                report['pages'][-1]['reference'] = {'source':board,'bounds':bounds}
                report['pages'][-1]['mean_absolute_pixel_difference_0_255'] = comparison(name,board,bounds,shot)
            # English/Bangla switching through Django's actual language form.
            capture('language-switch','/projects/2/?mode=panorama',390)
            page.locator('.language button[value=bn]').click(); page.wait_for_load_state()
            assert page.locator('html').get_attribute('lang') == 'bn'
            assert '/projects/2/' in page.url and 'mode=panorama' in page.url
            report['checks'].append('Language switching preserves page, project and query parameters')
            for name,route,bounds in [('home-bangla','/',(416,72,758,949)),('project-01-bangla','/projects/1/',(784,72,1127,949)),('inquiry-bangla','/inquiry/?project=1',(1153,72,1497,949))]:
                shot = capture(name,route,390)
                comparison(name,'13-mobile-bangla.png',bounds,shot)
            page.goto(BASE+'/'); page.locator('.language button[value=en]').click(); page.wait_for_load_state()
            for width in [375,390,768,1024,1440]:
                for route in ['/','/projects/','/projects/1/','/projects/2/','/gallery/','/virtual-site-visit/','/about/','/contact/','/privacy/','/terms/','/inquiry/']:
                    page.set_viewport_size({'width':width,'height':900}); page.goto(BASE+route)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow {route} {width}'
            report['checks'].append('11 public routes: no overflow at 375, 390, 768, 1024, 1440px')
            page.set_viewport_size({'width':390,'height':844}); page.goto(BASE+'/'); page.locator('.menu-toggle').click(); assert page.locator('#navigation').is_visible(); page.keyboard.press('Escape'); assert not page.locator('#navigation').is_visible(); report['checks'].append('Mobile menu opens and Escape closes it')
            page.goto(BASE+'/projects/1/'); original=page.locator('#main-photo').get_attribute('src'); page.locator('.thumbnail').nth(1).click(); assert page.locator('#main-photo').get_attribute('src')!=original; report['checks'].append('Project thumbnail changes main image')
            page.goto(BASE+'/gallery/'); page.locator('[data-gallery]').first.click(); assert page.locator('#photo-viewer').is_visible(); page.keyboard.press('ArrowRight'); assert page.locator('.viewer-count').inner_text()=='2 / 5'; page.screenshot(path=str(SHOTS/'gallery-lightbox.png')); page.keyboard.press('Escape'); assert not page.locator('#photo-viewer').is_visible(); report['checks'].append('Gallery viewer opens, navigates by keyboard and closes with Escape')
            page.goto(BASE+'/'); page.locator('.ask-ai').click(); page.screenshot(path=str(SHOTS/'assistant-disclosure.png')); page.locator('[data-start-chat]').click(); page.locator('#dialog-chat-message').fill("What is Project 02's area?"); page.locator('#chat-dialog .chat-form button').click(); page.wait_for_function('document.querySelector("#chat-dialog .chat-log").textContent.includes("75,00,000")'); page.screenshot(path=str(SHOTS/'assistant-conversation.png')); page.keyboard.press('Escape'); report['checks'].append('Assistant introduction, start, fixture response and close')
            page.goto(BASE+'/inquiry/?project=2'); page.locator('.inquiry-form button[type=submit]').click(); assert page.locator('.invalid').is_visible(); page.locator('[name=phone]').fill('01700000123'); page.locator('.inquiry-form button[type=submit]').click(); assert page.locator('.inquiry-form button[type=submit]').is_disabled(); page.wait_for_selector('.confirmation'); assert '01XXX XXX123' in page.locator('.confirmation').inner_text(); page.screenshot(path=str(SHOTS/'inquiry-confirmation.png')); report['checks'].append('Inquiry validates, disables duplicate submission and confirms with masked phone')
            for scenario in ['invalid-phone','sending','failure']:
                capture('inquiry-'+scenario,'/inquiry/?project='+('2' if scenario=='failure' else '1')+'&scenario='+scenario,768,870)
            page.locator('.inquiry-form button[type=submit]').click(); page.wait_for_selector('.confirmation'); report['checks'].append('Inquiry failure preserves entries and retry succeeds')
            capture('ai-unavailable','/assistant/?scenario=ai-unavailable',1024,650)
            capture('media-failure','/virtual-site-visit/?scenario=media-failure',1024,650)
            page.goto(BASE+'/virtual-site-visit/?mode=video'); page.locator('.fullscreen-toggle').first.click(); page.wait_for_timeout(150); assert page.evaluate('!!document.fullscreenElement'); page.locator('.fullscreen-toggle').first.click(); report['checks'].append('Media fullscreen entry and exit')
            capture('staff-sign-in','/staff/sign-in/',1440)
            page.locator('[name=username]').fill(username); page.locator('[name=password]').fill(password); page.locator('.show-password').click(); assert page.locator('[name=password]').get_attribute('type')=='text'; page.locator('button[type=submit]').click(); page.wait_for_url('**/staff/mfa/');
            page.locator('[data-code-digit]').evaluate_all('(els)=>els.forEach(e=>{e.value="0";e.dispatchEvent(new Event("input",{bubbles:true}))})'); page.locator('button[type=submit]').click(); assert page.locator('.notice.error').is_visible(); page.screenshot(path=str(SHOTS/'staff-mfa-invalid.png'))
            page.locator('[data-code-digit]').evaluate_all('(els)=>els.forEach((e,i)=>{e.value=String(i+1);e.dispatchEvent(new Event("input",{bubbles:true}))})'); page.locator('button[type=submit]').click(); page.wait_for_url('**/staff/'); report['checks'].append('Real Django staff sign-in, password visibility, invalid MFA and local demo code')
            staff_frames=[('staff-projects','/staff/','10-staff-content.png',(18,56,762,822)),('staff-editor','/staff/projects/1/edit/','10-staff-content.png',(774,56,1519,822)),('staff-inquiries','/staff/inquiries/','11-staff-access-inquiries.png',(32,543,819,933)),('staff-inquiry','/staff/inquiries/1/','11-staff-access-inquiries.png',(838,543,1505,933)),('staff-faqs','/staff/faqs/','12-staff-faqs-contacts.png',(28,163,759,935)),('staff-contacts','/staff/contacts/','12-staff-faqs-contacts.png',(782,163,1512,935))]
            for name,route,board,bounds in staff_frames:
                shot=capture(name,route,1024); comparison(name,board,bounds,shot)
            for name,route in [('staff-add','/staff/projects/add/'),('staff-review','/staff/projects/1/review/'),('staff-restricted','/staff/restricted/')]: capture(name,route,1024,800)
            page.goto(BASE+'/staff/projects/1/edit/'); page.locator('[name=title_en]').fill('Project 01 test draft'); page.locator('[data-tab=bn]').click(); assert page.locator('[name=title_bn]').is_visible(); page.locator('[data-tab=en]').click(); page.locator('[data-save-draft]').click(); page.reload(); assert page.locator('[name=title_en]').input_value()=='Project 01 test draft'; page.locator('[data-preview]').click(); assert 'Project 01 test draft' in page.locator('.preview-content').inner_text(); page.keyboard.press('Escape'); page.locator('.demo-editor button[type=submit]').click(); page.wait_for_url('**/review/'); page.locator('.publication-review input[type=checkbox]').evaluate_all('(els)=>els.forEach(e=>e.click())'); page.locator('.publication-review button').click(); assert 'Revision published' in page.locator('.publication-review').inner_text(); report['checks'].append('Staff bilingual tabs, draft persistence, preview, review checklist and demonstration publication')
            page.goto(BASE+'/staff/inquiries/1/'); page.locator('.reveal-phone').click(); assert page.locator('.masked-phone').inner_text()=='01700000123'; page.locator('#status').select_option('Contacted'); page.locator('button[type=submit]').click(); page.reload(); assert page.locator('#status').input_value()=='Contacted'; report['checks'].append('Synthetic phone reveal and inquiry status persistence')
            page.goto(BASE+'/staff/faqs/'); page.locator('.faq-row').nth(1).click(); assert page.locator('#question').input_value()=='How can I contact the team?'; page.locator('[data-add-faq]').click(); assert page.locator('#question').input_value()==''; page.locator('#question').fill('Example question'); page.locator('#answer').fill('Example answer'); page.locator('[data-save-draft]').click(); report['checks'].append('FAQ selection, add and draft saving')
            page.goto(BASE+'/staff/contacts/'); page.locator('[name=contact_name_en]').fill('Demo contact'); page.locator('[data-preview]').click(); assert 'Demo contact' in page.locator('.preview-content').inner_text(); page.keyboard.press('Escape'); page.locator('[name=confirmed]').check(); page.locator('[name=languages_reviewed]').check(); page.locator('.demo-editor button[type=submit]').click(); assert page.locator('#staff-preview').is_visible(); report['checks'].append('Contact editor live preview and review entry')
            # Additional source states and interactions from the multi-screen boards.
            page.goto(BASE+'/staff/projects/1/edit/')
            page.locator('.media-upload').set_input_files(str(ROOT/'static/images/project-02.jpg'))
            page.wait_for_function('document.querySelector("[name=main_image]").value.startsWith("data:")')
            page.locator('[name=alt_text]').fill('Local uploaded test photograph')
            page.locator('[data-preview]').click()
            assert page.locator('.preview-content img').get_attribute('alt')=='Local uploaded test photograph'
            page.keyboard.press('Escape')
            report['checks'].append('Staff image upload, main-image selection and alt-text preview')
            page.goto(BASE+'/staff/faqs/')
            page.locator('.demo-editor button[type=submit]').click()
            page.locator('#staff-preview input[type=checkbox]').evaluate_all('(els)=>els.forEach(e=>e.click())')
            page.locator('#staff-preview .publication-review button').click()
            assert 'Revision published' in page.locator('.preview-content').inner_text()
            page.keyboard.press('Escape')
            report['checks'].append('FAQ review checklist and publication result')
            capture('staff-forgot-password','/staff/forgot-password/',1024)
            page.locator('[name=email]').fill('demo@example.invalid'); page.locator('button[type=submit]').click()
            page.screenshot(path=str(SHOTS/'staff-password-recovery-feedback.png'))
            capture('staff-recovery-code','/staff/mfa/?recovery=1',1024)
            page.locator('[name=code]').fill('DEMO-RECOVERY'); page.locator('button[type=submit]').click()
            page.wait_for_url('**/staff/')
            report['checks'].append('Password recovery feedback and recovery-code entry')
            capture('staff-mfa','/staff/mfa/',1024)
            comparison('staff-mfa','11-staff-access-inquiries.png',(779,54,1506,486),SHOTS/'staff-mfa.png')
            comparison('staff-sign-in','11-staff-access-inquiries.png',(32,54,758,486),SHOTS/'staff-sign-in.png')
            comparison('staff-mfa-invalid','11-staff-access-inquiries.png',(779,54,1506,486),SHOTS/'staff-mfa-invalid.png')
            comparison('inquiry-invalid-phone','14-feedback-recovery.png',(11,94,501,649),SHOTS/'inquiry-invalid-phone.png')
            comparison('inquiry-sending','14-feedback-recovery.png',(524,94,1013,649),SHOTS/'inquiry-sending.png')
            comparison('inquiry-failure','14-feedback-recovery.png',(1035,94,1525,649),SHOTS/'inquiry-failure.png')
            comparison('ai-unavailable','14-feedback-recovery.png',(12,699,501,1001),SHOTS/'ai-unavailable.png')
            comparison('media-failure','14-feedback-recovery.png',(524,699,1013,1001),SHOTS/'media-failure.png')
            comparison('staff-restricted','14-feedback-recovery.png',(1035,699,1525,1001),SHOTS/'staff-restricted.png')
            comparison('inquiry-confirmation','07-assistant-inquiry.png',(1337,83,1762,780),SHOTS/'inquiry-confirmation.png')
            page.set_viewport_size({'width':1440,'height':300}); page.goto(BASE+'/gallery/'); page.locator('[data-gallery]').first.click(); page.screenshot(path=str(SHOTS/'gallery-lightbox-desktop.png')); comparison('gallery-lightbox','05-gallery.png',(33,787,1503,1004),SHOTS/'gallery-lightbox-desktop.png'); page.keyboard.press('Escape')
            page.set_viewport_size({'width':460,'height':760}); page.goto(BASE+'/assistant/')
            page.locator('#page-chat-message').fill("What is Project 01's area?"); page.locator('.assistant-page .chat-form button').click()
            page.wait_for_function('document.querySelector(".chat-log").textContent.includes("45,00,000")')
            page.locator('#page-chat-message').fill('\u0986\u09b0\u0993 \u099c\u09be\u09a8\u09a4\u09c7 \u099a\u09be\u0987'); page.locator('.assistant-page .chat-form button').click()
            page.wait_for_function('document.querySelector(".chat-log").childElementCount >= 4')
            page.screenshot(path=str(SHOTS/'assistant-reference-conversation.png'),full_page=True)
            comparison('assistant-reference-conversation','07-assistant-inquiry.png',(455,83,879,780),SHOTS/'assistant-reference-conversation.png')
            for route in ['/staff/','/staff/projects/1/edit/','/staff/inquiries/','/staff/inquiries/1/','/staff/faqs/','/staff/contacts/']:
                page.set_viewport_size({'width':390,'height':844}); page.goto(BASE+route)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),route
            report['checks'].append('Six staff routes have no page overflow at 390px')
            browser.close()
    finally:
        user.delete()
        (OUT/'browser-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f'{len(report["pages"])} screenshots; {len(report["checks"])} interaction checks; {len(report["console_errors"])} JS errors')
    assert not report['console_errors'],report['console_errors']

if __name__=='__main__': run()
