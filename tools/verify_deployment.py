"""Smoke-test the anonymous Vercel production frontend using real browser requests."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get("DEPLOYMENT_URL", "https://rcpdl-property-platform.vercel.app").rstrip("/")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/verification"
(OUT / "screenshots").mkdir(parents=True, exist_ok=True)

def main():
    report = {"url": BASE, "checked_at_utc": datetime.now(timezone.utc).isoformat(), "routes": [], "checks": [], "javascript_errors": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.on("pageerror", lambda error: report["javascript_errors"].append(str(error)))
        routes = ["/", "/projects/", "/projects/1/", "/projects/2/", "/gallery/", "/virtual-site-visit/", "/assistant/", "/inquiry/", "/about/", "/contact/", "/privacy/", "/terms/", "/staff/sign-in/"]
        for route in routes:
            response = page.goto(BASE + route)
            page.evaluate("document.fonts.ready")
            page.locator('img').evaluate_all('(els)=>Promise.all(els.map(e=>{e.loading="eager";return e.decode().catch(()=>{});} ))')
            assert response.status == 200, (route, response.status)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), route
            broken = page.locator("img[src]").evaluate_all("els => els.filter(e => !e.hidden && (!e.complete || !e.naturalWidth)).map(e => e.src)")
            assert not broken, (route, broken)
            report["routes"].append({"route": route, "status": response.status, "broken_images": broken})
        for asset in ["css/site.css", "css/refinements.css", "js/site.js", "images/logo.png", "fonts/Roboto.ttf", "fonts/NotoSansBengali.ttf"]:
            response = page.request.get(BASE + "/static/" + asset)
            assert response.status == 200, (asset, response.status)
        report["checks"].append("CSS, JavaScript, logo and English/Bangla fonts served from the production CDN")
        assert page.request.get(BASE + '/dev/').status == 404
        page.goto(BASE + '/virtual-site-visit/?project=2&mode=panorama&scenario=media-failure')
        assert page.locator('#panorama').count() == 1, 'Development failure fixture must be disabled online'
        page.wait_for_function('window.rcPanorama?.isLoaded()', timeout=30000)
        page.locator('#panorama').scroll_into_view_if_needed()
        bounds = page.locator('#panorama').bounding_box()
        yaw = page.evaluate('rcPanorama.getYaw()')
        x, y = bounds['x'] + bounds['width']*.65, bounds['y'] + bounds['height']*.55
        page.mouse.move(x,y); page.mouse.down(); page.mouse.move(x-200,y,steps=15); page.mouse.up()
        page.wait_for_timeout(500)
        assert abs(page.evaluate('rcPanorama.getYaw()') - yaw) > 10
        report['checks'].append('Production panorama loads from CDN and mouse drag changes actual yaw; dev index and failure fixtures disabled')
        page.goto(BASE + "/")
        page.screenshot(path=str(OUT / "screenshots/vercel-home-desktop.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.reload()
        page.screenshot(path=str(OUT / "screenshots/vercel-home-mobile.png"), full_page=True)
        page.locator(".menu-toggle").click()
        assert page.locator("#navigation").is_visible()
        page.keyboard.press("Escape")
        page.locator(".language button[value=bn]").click()
        page.wait_for_function("document.documentElement.lang === 'bn'")
        assert "আপনার" in page.locator("h1").inner_text()
        page.locator(".language button[value=en]").click()
        page.wait_for_function("document.documentElement.lang === 'en'")
        report["checks"].append("Mobile menu and Django CSRF-protected English/Bangla switching")
        page.goto(BASE + "/inquiry/?project=2")
        page.locator("[name=phone]").fill("01700000123")
        page.locator(".inquiry-form button[type=submit]").click()
        page.wait_for_selector(".confirmation")
        assert "Project 02" in page.locator(".confirmation").inner_text()
        assert "01XXX XXX123" in page.locator(".confirmation").inner_text()
        report["checks"].append("CSRF-protected inquiry demonstration confirms the selected project and masks synthetic phone input")
        page.goto(BASE + "/assistant/")
        page.locator("#page-chat-message").fill("What is Project 01's area?")
        page.locator(".assistant-page .chat-form button").click()
        page.wait_for_function("document.querySelector('.assistant-page .chat-log').textContent.includes('45,00,000')")
        report["checks"].append("Deterministic assistant works online without an external AI service")
        page.goto(BASE + "/staff/sign-in/")
        page.locator("[name=username]").fill("deployment-check")
        page.locator("[name=password]").fill("not-a-real-account")
        page.locator("button[type=submit]").click()
        assert "persistent database" in page.locator(".notice.error").inner_text()
        report["checks"].append("Hosted staff sign-in shows its explicit database requirement rather than attempting local SQLite authentication")
        browser.close()
    assert not report["javascript_errors"], report["javascript_errors"]
    (OUT / "deployment-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Production verified: {len(report['routes'])} routes, {len(report['checks'])} interaction/asset groups, zero JavaScript errors.")

if __name__ == "__main__":
    main()
