"""Exercise publication snapshots, true panorama interaction and the full viewport matrix."""
import json
import os
import secrets
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth import get_user_model

BASE = os.environ.get('VERIFY_URL', 'http://127.0.0.1:8005')
OUT = ROOT / 'docs/verification'
SHOTS = OUT / 'screenshots/completion'
SHOTS.mkdir(parents=True, exist_ok=True)

def run():
    report = {'checks': [], 'matrix': [], 'errors': [], 'panoramas': []}
    password = secrets.token_urlsafe(24)
    user = get_user_model().objects.create_user(username='completion-'+secrets.token_hex(4), password=password, is_staff=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel='msedge', headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
            context = browser.new_context(viewport={'width': 1440, 'height': 1000})
            page = context.new_page()
            page.on('pageerror', lambda e: report['errors'].append(str(e)))
            def goto(route):
                response = page.goto(BASE + route)
                assert response.status < 400, (route, response.status)
                return response
            for project in (1, 2):
                goto(f'/virtual-site-visit/?project={project}&mode=panorama')
                page.wait_for_function('window.rcPanorama?.isLoaded()', timeout=30000)
                stage = page.locator('#panorama')
                stage.scroll_into_view_if_needed()
                bounds = stage.bounding_box()
                start = page.evaluate('rcPanorama.getYaw()')
                x, y = bounds['x'] + bounds['width']*.7, bounds['y'] + bounds['height']*.55
                page.mouse.move(x,y); page.mouse.down(); page.mouse.move(x-210,y+25, steps=15); page.mouse.up()
                page.wait_for_timeout(700)
                after = page.evaluate('rcPanorama.getYaw()')
                assert abs(after-start) > 10, (start, after)
                fov = page.evaluate('rcPanorama.getHfov()')
                page.locator('[data-zoom="-10"]').click(); page.wait_for_timeout(400)
                assert page.evaluate('rcPanorama.getHfov()') < fov
                page.locator('[data-reset]').click(); page.wait_for_timeout(400)
                assert abs(page.evaluate('rcPanorama.getYaw()')) < 1
                page.locator('.fullscreen-toggle').first.click()
                page.wait_for_function('!!document.fullscreenElement')
                page.screenshot(path=str(SHOTS / f'panorama-{project}-fullscreen.png'))
                page.locator('.fullscreen-toggle').first.click(); page.wait_for_function('!document.fullscreenElement')
                for yaw in (0, 90, 179, -179, -90):
                    page.evaluate('(yaw)=>rcPanorama.setYaw(yaw,false)', yaw); page.wait_for_timeout(150)
                    stage.screenshot(path=str(SHOTS / f'panorama-{project}-yaw-{yaw}.png'))
                before = page.evaluate('rcPanorama.getYaw()'); page.wait_for_timeout(800)
                assert abs(page.evaluate('rcPanorama.getYaw()') - before) < .1, 'Unexpected autorotation'
                page.evaluate("document.querySelector('#media-stage').dataset.panorama='/static/not-a-panorama.webp'")
                page.locator('.retry-media').evaluate('(b)=>b.click()')
                page.wait_for_selector('.media-fallback:not([hidden])')
                page.evaluate(f"document.querySelector('#media-stage').dataset.panorama='/static/images/media/panorama-0{project}-1774.webp'")
                page.locator('.retry-media').click(); page.wait_for_function('window.rcPanorama?.isLoaded()')
                report['panoramas'].append({'project':project, 'drag_yaw_before':start, 'drag_yaw_after':after, 'zoom_reset_fullscreen_retry':True, 'yaw_frames':[0,90,179,-179,-90]})
            # Touch input uses a mobile browser context and actual CDP touch events.
            mobile = browser.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
            touch = mobile.new_page(); touch.goto(BASE+'/virtual-site-visit/?mode=panorama')
            touch.wait_for_function('window.rcPanorama?.isLoaded()')
            touch.locator('#panorama').scroll_into_view_if_needed()
            bounds = touch.locator('#panorama').bounding_box(); x,y = bounds['x']+280,bounds['y']+180
            client = mobile.new_cdp_session(touch)
            start = touch.evaluate('rcPanorama.getYaw()')
            client.send('Input.dispatchTouchEvent', {'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
            for delta in range(10,160,10): client.send('Input.dispatchTouchEvent', {'type':'touchMove','touchPoints':[{'x':x-delta,'y':y}]})
            client.send('Input.dispatchTouchEvent', {'type':'touchEnd','touchPoints':[]})
            touch.wait_for_timeout(500)
            assert abs(touch.evaluate('rcPanorama.getYaw()')-start)>10
            mobile.close(); report['checks'].append('Mouse and touch drag, zoom, reset, fullscreen, yaw wrap, no autorotation, actual failed asset and retry')
            goto('/staff/projects/1/edit/')
            page.locator('[name=username]').fill(user.username); page.locator('[name=password]').fill(password); page.locator('button[type=submit]').click()
            page.wait_for_url('**/staff/mfa/'); page.locator('[data-code-digit]').first.fill('1')
            for i,digit in enumerate('123456'): page.locator('[data-code-digit]').nth(i).fill(digit)
            page.locator('button[type=submit]').click(); page.wait_for_url('**/staff/projects/1/edit/')
            page.locator('[name=title_en]').fill('Reviewed snapshot A'); page.locator('[data-save-draft]').click()
            page.locator('.demo-editor button[type=submit]').click(); page.wait_for_url('**/review/')
            page.locator('.publication-review input').check() if page.locator('.publication-review input').count()==1 else page.locator('.publication-review input').evaluate_all('(es)=>es.forEach(e=>e.click())')
            page.locator('.publication-review button').click()
            goto('/staff/projects/1/edit/'); page.locator('[name=title_en]').fill('Unpublished draft B'); page.locator('[data-save-draft]').click()
            goto('/staff/projects/1/preview/?version=published'); assert page.locator('.summary h1').inner_text()=='Reviewed snapshot A'
            goto('/staff/projects/1/preview/?version=draft'); assert page.locator('.summary h1').inner_text()=='Unpublished draft B'
            goto('/projects/1/'); assert page.locator('.summary h1').inner_text()=='Project 01'
            report['checks'].append('Protected deep link returns after MFA; draft and published snapshot remain separate; public fixture unchanged')
            goto('/staff/faqs/')
            page.locator('[data-tab=bn]').click()
            page.locator('#question-bn').fill('স্বতন্ত্র প্রথম প্রশ্ন')
            page.locator('[data-save-draft]').click(); page.locator('.faq-row').nth(1).click()
            assert page.locator('#question-bn').input_value() != 'স্বতন্ত্র প্রথম প্রশ্ন'
            page.locator('.faq-row').first.click(); assert page.locator('#question-bn').input_value()=='স্বতন্ত্র প্রথম প্রশ্ন'
            page.reload(); assert page.locator('#question-bn').input_value()=='স্বতন্ত্র প্রথম প্রশ্ন'
            report['checks'].append('FAQ English/Bangla fields persist per row without mixing languages between records')
            routes = ['/', '/projects/', '/projects/1/', '/projects/2/', '/gallery/', '/virtual-site-visit/', '/assistant/', '/inquiry/', '/about/', '/contact/', '/privacy/', '/terms/', '/staff/', '/staff/projects/1/edit/', '/staff/projects/1/review/', '/staff/inquiries/', '/staff/inquiries/1/', '/staff/faqs/', '/staff/contacts/']
            for width in (320,375,390,430,768,1024,1280,1440,1920):
                page.set_viewport_size({'width':width, 'height':900})
                for route in routes:
                    goto(route)
                    overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
                    report['matrix'].append({'width':width,'route':route,'overflow':overflow})
                    assert not overflow, (width,route)
                page.screenshot(path=str(SHOTS / f'contacts-{width}.png'),full_page=True)
            for width,height in ((844,390),(1024,600),(320,568)):
                page.set_viewport_size({'width':width,'height':height}); goto('/virtual-site-visit/')
                page.wait_for_function('window.rcPanorama?.isLoaded()')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.screenshot(path=str(SHOTS / f'panorama-{width}x{height}.png'),full_page=True)
            page.set_viewport_size({'width':1280,'height':800}); goto('/staff/projects/1/edit/')
            page.evaluate("document.documentElement.style.zoom='200%'")
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.screenshot(path=str(SHOTS/'staff-200-percent.png'), full_page=True)
            report['checks'].append('171 route/width checks; landscape and short screens; staff editor at 200% browser CSS zoom')
            browser.close()
    finally:
        user.delete()
        (OUT / 'completion-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    assert not report['errors'], report['errors']
    print(f"{len(report['matrix'])} matrix checks; {len(report['checks'])} interaction groups; {len(report['errors'])} script errors")

if __name__ == '__main__': run()
