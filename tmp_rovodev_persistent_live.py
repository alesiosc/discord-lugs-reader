import os
import asyncio
from datetime import datetime
from pathlib import Path

import numpy as np
from enhanced_ocr import EnhancedOCR
from playwright.async_api import async_playwright

OUT_DIR = Path('screenshots')
OUT_DIR.mkdir(exist_ok=True)
PROFILE_DIR = Path('tmp_rovodev_chrome_profile')
PROFILE_DIR.mkdir(exist_ok=True)
LOG = Path('tmp_rovodev_persistent_live.log')

DISCORD_URL = os.getenv('DISCORD_CHANNEL_URL', '').strip()
if not DISCORD_URL:
    print('ERROR: DISCORD_CHANNEL_URL not set in environment (.env).')
    raise SystemExit(1)

def log(msg: str):
    print(msg, flush=True)
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | {msg}\n")
    except Exception:
        pass

async def maybe_click_continue_in_browser(page):
    # Try multiple strategies to dismiss the landing prompt
    for attempt in range(6):
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

async def wait_for_channel_ready(page):
    try:
        await page.wait_for_selector('[data-list-id="chat-messages"]', timeout=20000)
        log('Channel messages list detected.')
    except Exception:
        log('Messages list not detected quickly; proceeding after delay.')
        await page.wait_for_timeout(3000)

async def scroll_messages_to_bottom(page):
    """Scroll the messages container itself to absolute bottom, robustly."""
    # Try the known messages list container
    messages = page.locator('[data-list-id="chat-messages"]')
    try:
        # Ensure it exists
        await messages.wait_for(timeout=10000)
        # Scroll the element repeatedly until stable
        for _ in range(40):
            changed = await page.evaluate(
                "(sel) => { const el=document.querySelector(sel); if(!el) return false; const y=el.scrollTop; el.scrollTop = el.scrollHeight; return el.scrollTop !== y; }",
                '[data-list-id="chat-messages"]'
            )
            await page.wait_for_timeout(250)
            if not changed:
                break
        log('Scrolled messages container to bottom.')
        return True
    except Exception as e:
        log('Failed messages-container scroll, falling back to page scroll: ' + str(e))
        # Fallback to page scroll if container not found
        for _ in range(30):
            h = await page.evaluate("document.body.scrollHeight")
            y = await page.evaluate("window.scrollY")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(300)
            h2 = await page.evaluate("document.body.scrollHeight")
            y2 = await page.evaluate("window.scrollY")
            if h2 == h and y2 == y:
                break
        log('Scrolled page to bottom (fallback).')
        return False

async def main():
    try:
        LOG.write_text('', encoding='utf-8')
    except Exception:
        pass

    log('Starting persistent live run at ' + datetime.now().isoformat())

    # Prewarm OCR so model load happens before screenshots
    log('Prewarming EnhancedOCR models...')
    ocr = EnhancedOCR(timeout_seconds=60)
    try:
        dummy = (np.ones((32,32,3), dtype=np.uint8) * 255)
        _ = ocr._ocr_with_timeout(dummy)
    except Exception:
        pass
    log('EnhancedOCR ready.')

    async with async_playwright() as p:
        log('Launching persistent Chromium...')
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            viewport=None,  # we'll set viewport on the page explicitly
            args=[
                "--start-maximized",
                "--window-position=0,0",
                "--window-size=1920,1080",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-renderer-backgrounding",
                "--disable-breakpad",
                "--no-first-run",
                "--disable-features=Translate",
            ],
        )
        # Make timeouts more forgiving
        try:
            ctx.set_default_timeout(30000)
        except Exception:
            pass
        page = await ctx.new_page()
        # Force viewport to 1920x1080 for full window content
        try:
            await page.set_viewport_size({"width": 1920, "height": 1080})
            log('Viewport set to 1920x1080')
        except Exception as e:
            log('Failed to set viewport: ' + str(e))
        # Log close events to understand crashes
        try:
            page.on("close", lambda: log("[EVENT] Page closed"))
            ctx.on("close", lambda: log("[EVENT] Context closed"))
        except Exception:
            pass
        target_url = DISCORD_URL + ("?noapp=1" if "?" not in DISCORD_URL else "&noapp=1")
        log('Navigating to: ' + target_url)
        await page.goto(target_url, wait_until='domcontentloaded')

        # Reduce motion to lower CPU/GPU load
        try:
            await page.add_style_tag(content="* { scroll-behavior: auto !important; } @media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }")
        except Exception:
            pass

        # Dismiss the "Continue in browser" prompt if present
        clicked = await maybe_click_continue_in_browser(page)
        if clicked:
            log('Dismissed "Continue in browser" prompt.')
        else:
            log('Did not detect "Continue in browser" prompt (may not be present).')

        # Wait for messages container, then IMMEDIATE Screenshot A
        await wait_for_channel_ready(page)
        messages = page.locator('[data-list-id="chat-messages"]')
        tsA = datetime.now().strftime('%H%M%S')
        imgA = OUT_DIR / f"persistent_live_{tsA}_A.png"
        try:
            await messages.screenshot(path=str(imgA))
            log('Screenshot A (messages only) saved: ' + str(imgA))
        except Exception as e:
            await page.screenshot(path=str(imgA), full_page=True)
            log('Fallback full-page Screenshot A saved: ' + str(imgA) + ' error=' + str(e))

        # Scroll messages container to absolute bottom, Screenshot B
        await scroll_messages_to_bottom(page)
        tsB = datetime.now().strftime('%H%M%S')
        imgB = OUT_DIR / f"persistent_live_{tsB}_B.png"
        try:
            await messages.screenshot(path=str(imgB))
            log('Screenshot B (messages only, bottom) saved: ' + str(imgB))
        except Exception as e:
            await page.screenshot(path=str(imgB), full_page=True)
            log('Fallback full-page Screenshot B saved: ' + str(imgB) + ' error=' + str(e))

        # Nudge up slightly, Screenshot C
        try:
            await page.evaluate("window.scrollTo(0, Math.max(window.scrollY - 220, 0))")
            await page.wait_for_timeout(250)
        except Exception:
            pass
        tsC = datetime.now().strftime('%H%M%S')
        imgC = OUT_DIR / f"persistent_live_{tsC}_C.png"
        try:
            await messages.screenshot(path=str(imgC))
            log('Screenshot C (messages only, nudge-up) saved: ' + str(imgC))
        except Exception as e:
            await page.screenshot(path=str(imgC), full_page=True)
            log('Fallback full-page Screenshot C saved: ' + str(imgC) + ' error=' + str(e))

        # Do not close the browser; keep it open on the source page
        log('Keeping browser open for inspection. Press Ctrl+C to stop script when done.')
        await asyncio.sleep(3600)

    # OCR A/B/C screenshots and print results clearly
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

    for img in [imgA, imgB, imgC]:
        do_ocr(img)

    log('Run complete.')

if __name__ == '__main__':
    asyncio.run(main())
