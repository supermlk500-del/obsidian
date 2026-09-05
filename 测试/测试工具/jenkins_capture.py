from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "http://localhost:8088"
IMAGE_DIR = Path(__file__).parent / "images"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(1000)
    page.screenshot(path=str(IMAGE_DIR / "jenkins-login-当前实景.png"), full_page=True)
    browser.close()
