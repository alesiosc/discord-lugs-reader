import os
import asyncio
from datetime import datetime
from pathlib import Path

import numpy as np
from enhanced_ocr import EnhancedOCR
from playwright.async_api import async_playwright

OUT_DIR = Path('screenshots')
OUT_DIR.mkdir(exist_ok=True)
LOG = Path('tmp_rovodev_race_capture.log')
STORAGE_PATH = Path('tmp_rovodev_simple_storage.json')
DISCORD_URL = os.getenv('DISCORD_CHANNEL_URL', '').strip()

def log(msg: str):
    print(msg, flush=True)
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | {msg}\n")
    except Exception:
        pass

async def maybe_click_continue_in_browser(page):
    for _ in range(8):
        try:
            btn = page.get_by_role("button", name=lambda n: n and "continue in browser" in n.lower())
            if await btn.is_visible(timeout=1000):
                log('Clicking "Continue in browser" button')
                await btn.click()
                await page.wait_for_timeout(500)
                return True
        except Exception:
            pass
        try:
            el = page.get_by_text("Continue in browser", exact=False)
            if await el.is_visible(timeout=1000):
                log('Clicking text "Continue in browser"')
                await el.click()
                await page.wait_for_timeout(500)
                return True
        except Exception:
            pass
        await page.wait_for_timeout(250)
    return False

async def race_once(ocr: EnhancedOCR, use_storage: bool) -> bool:
    async with async_playwright() as p:
        ctx_kwargs = {"viewport": {"width": 1280, "height": 900}}
        if use_storage and STORAGE_PATH.exists():
            ctx_kwargs["storage_state"] = str(STORAGE_PATH)
            log('Using saved storage_state to skip login')
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(**ctx_kwargs)
        page = await context.new_page()
        log('Going to: ' + DISCORD_URL)
        await page.goto(DISCORD_URL, wait_until='domcontentloaded')

        # Try to dismiss prompt quickly
        await maybe_click_continue_in_browser(page)

        # Immediately attempt screenshots (messages container and fallback full page)
        try:
            await page.evaluate("document.body.style.zoom='1.5'")
        except Exception:
            pass

        ts = datetime.now().strftime('%H%M%S')
        img_msg = OUT_DIR / f"race_{ts}_msg.png"
        img_full = OUT_DIR / f"race_{ts}_full.png"
        try:
            messages = page.locator('[data-list-id="chat-messages"]')
            await messages.screenshot(path=str(img_msg))
            log('Saved messages-only screenshot: ' + str(img_msg))
        except Exception as e:
            log('Messages-only screenshot failed: ' + str(e))
        try:
            await page.screenshot(path=str(img_full), full_page=True)
            log('Saved full-page screenshot: ' + str(img_full))
        except Exception as e:
            log('Full-page screenshot failed: ' + str(e))

        # Save storage_state for next attempts
        try:
            await context.storage_state(path=str(STORAGE_PATH))
            log('Saved storage_state: ' + str(STORAGE_PATH))
        except Exception as e:
            log('Failed to save storage_state: ' + str(e))

        await context.close()
        await browser.close()

    # OCR both quickly
    parsed_any = False
    for path in [img_msg, img_full]:
        if not path.exists():
            continue
        log(f'=== OCR START {path.name} ===')
        data = ocr.extract_ticker_data(str(path))
        if data:
            parsed_any = True
            log(f'PARSED {len(data)} items for {path.name}:')
            for item in data:
                log('  ' + str(item))
        else:
            log(f'NO PARSE {path.name}')
        log(f'=== OCR END {path.name} ===')
    return parsed_any

async def main():
    LOG.write_text('', encoding='utf-8')
    if not DISCORD_URL:
        log('ERROR: DISCORD_CHANNEL_URL not set in environment (.env).')
        return

    log('Starting race-capture at ' + datetime.now().isoformat())
    log('Prewarming EnhancedOCR models...')
    ocr = EnhancedOCR(timeout_seconds=60)
    try:
        dummy = (np.ones((32,32,3), dtype=np.uint8) * 255)
        _ = ocr._ocr_with_timeout(dummy)
    except Exception:
        pass
    log('EnhancedOCR ready.')

    # First attempt: with storage_state if available
    ok = await race_once(ocr, use_storage=True)
    if ok:
        log('Race-capture success on first attempt.')
        return

    # Second attempt: without storage_state (force fresh), in case storage caused redirect
    log('Retrying race-capture without storage_state...')
    ok = await race_once(ocr, use_storage=False)
    if ok:
        log('Race-capture success on second attempt.')
    else:
        log('Race-capture completed with no parse. Check screenshots in screenshots/ and log at ' + str(LOG))

if __name__ == '__main__':
    asyncio.run(main())
