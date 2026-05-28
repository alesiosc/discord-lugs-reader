import os
import asyncio
from datetime import datetime
from pathlib import Path

import numpy as np
from enhanced_ocr import EnhancedOCR
from playwright.async_api import async_playwright

OUT_DIR = Path('screenshots')
STORAGE_PATH = Path('tmp_rovodev_simple_storage.json')
OUT_DIR.mkdir(exist_ok=True)
LOG = Path('tmp_rovodev_simple_live.log')

async def maybe_click_continue_in_browser(page):
    # Try multiple times to dismiss the prompt if visible
    for attempt in range(10):
        try:
            btn = page.get_by_role("button", name=lambda n: n and "continue in browser" in n.lower())
            if await btn.is_visible(timeout=1500):
                log('Clicking "Continue in browser" button')
                await btn.click()
                await page.wait_for_timeout(1200)
                return True
        except Exception:
            pass
        try:
            el = page.get_by_text("Continue in browser", exact=False)
            if await el.is_visible(timeout=1500):
                log('Clicking text "Continue in browser"')
                await el.click()
                await page.wait_for_timeout(1200)
                return True
        except Exception:
            pass
        await page.wait_for_timeout(500)
    return False

async def wait_for_messages_ready(page):
    # Wait for Discord messages list to be present
    try:
        await page.wait_for_selector('[data-list-id="chat-messages"]', timeout=15000)
        log('Channel messages list detected.')
        return True
    except Exception:
        log('Messages list not detected quickly; retrying shortly...')
        return False

def log(msg: str):
    print(msg, flush=True)
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | {msg}\n")
    except Exception:
        pass

DISCORD_URL = os.getenv('DISCORD_CHANNEL_URL', '').strip()
if not DISCORD_URL:
    log('ERROR: DISCORD_CHANNEL_URL not set in environment (.env).')
    raise SystemExit(1)

async def maybe_click_continue_in_browser(page):
    # Try the common Discord landing prompt
    try:
        btn = page.get_by_role("button", name=lambda n: n and "continue in browser" in n.lower())
        if await btn.is_visible(timeout=2000):
            log('Clicking "Continue in browser" button')
            await btn.click()
            await page.wait_for_timeout(1000)
            return
    except Exception:
        pass
    # Try text/link fallback
    try:
        el = page.get_by_text("Continue in browser", exact=False)
        if await el.is_visible(timeout=2000):
            log('Clicking text "Continue in browser"')
            await el.click()
            await page.wait_for_timeout(1000)
            return
    except Exception:
        pass

async def wait_for_channel_ready(page):
    # Best-effort wait for message list; fall back to a short delay
    try:
        await page.wait_for_selector('[data-list-id="chat-messages"]', timeout=8000)
        log('Channel messages list detected.')
    except Exception:
        log('Messages list not detected quickly; proceeding after short delay.')
        await page.wait_for_timeout(1500)

async def main():
    try:
        LOG.write_text('', encoding='utf-8')
    except Exception:
        pass

    log('Starting simple live run at ' + datetime.now().isoformat())

    # Prewarm OCR to avoid long wait after screenshots
    log('Prewarming EnhancedOCR models...')
    ocr = EnhancedOCR(timeout_seconds=60)
    try:
        dummy = (np.ones((32,32,3), dtype=np.uint8) * 255)
        _ = ocr._ocr_with_timeout(dummy)
    except Exception:
        pass
    log('EnhancedOCR ready.')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ctx_kwargs = {"viewport": {"width": 1280, "height": 900}}
        if STORAGE_PATH.exists():
            ctx_kwargs["storage_state"] = str(STORAGE_PATH)
            log('Using saved storage state to skip login.')
        context = await browser.new_context(**ctx_kwargs)
        page = await context.new_page()
        log('Navigating to: ' + DISCORD_URL)
        await page.goto(DISCORD_URL, wait_until='domcontentloaded')
        # Loop until channel content is ready; auto-click "Continue in browser" when present
        for _ in range(10):
            clicked = await maybe_click_continue_in_browser(page)
            ready = await wait_for_messages_ready(page)
            if ready:
                break
        # Save storage state after potential login/continue
        try:
            await context.storage_state(path=str(STORAGE_PATH))
            log('Saved storage state for next run: ' + str(STORAGE_PATH))
        except Exception as e:
            log('Failed to save storage state: ' + str(e))

        # Zoom for readability and capture messages container if possible
        try:
            await page.evaluate("document.body.style.zoom='1.5'")
        except Exception:
            pass

        try:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(400)
        except Exception:
            pass

        messages = page.locator('[data-list-id="chat-messages"]')
        ts1 = datetime.now().strftime('%H%M%S')
        img1 = OUT_DIR / f"simple_live_{ts1}_1.png"
        try:
            await messages.screenshot(path=str(img1))
            log('Screenshot 1 (messages only) saved: ' + str(img1))
        except Exception as e:
            await page.screenshot(path=str(img1), full_page=True)
            log('Fallback full-page Screenshot 1 saved: ' + str(img1) + ' error=' + str(e))

        try:
            await page.evaluate("window.scrollTo(0, Math.max(window.scrollY - 140, 0))")
            await page.wait_for_timeout(300)
        except Exception:
            pass

        ts2 = datetime.now().strftime('%H%M%S')
        img2 = OUT_DIR / f"simple_live_{ts2}_2.png"
        try:
            await messages.screenshot(path=str(img2))
            log('Screenshot 2 (messages only) saved: ' + str(img2))
        except Exception as e:
            await page.screenshot(path=str(img2), full_page=True)
            log('Fallback full-page Screenshot 2 saved: ' + str(img2) + ' error=' + str(e))

        await context.close()
        await browser.close()

    # OCR both screenshots and print results clearly
    def do_ocr(path: Path):
        log(f'=== OCR START {path.name} ===')
        data = ocr.extract_ticker_data(str(path))
        if not data:
            log(f'NO PARSE {path.name}')
        else:
            log(f'PARSED {len(data)} items for {path.name}:')
            for item in data:
                log('  ' + str(item))
        log(f'=== OCR END {path.name} ===')

    do_ocr(img1)
    do_ocr(img2)
    log('Run complete.')

if __name__ == '__main__':
    asyncio.run(main())
