import asyncio
import sys
from datetime import datetime
from pathlib import Path

from main import DiscordBrowserDetector, logger

LOG_PATH = Path('tmp_rovodev_live_run_log.txt')
STORAGE_PATH = Path('tmp_rovodev_storage_state.json')

def log_print(*args):
    msg = ' '.join(str(a) for a in args)
    print(msg, flush=True)
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | {msg}\n")
    except Exception:
        pass

async def run_once_live():
    LOG_PATH.write_text('', encoding='utf-8')
    log_print("[RUN] Starting live one-off capture at", datetime.now().isoformat())
    det = DiscordBrowserDetector()
    try:
        log_print("[RUN] Forcing non-persistent Chromium with hardened launch args...")
        # Always use non-persistent for stability in this run
        try:
            from playwright.async_api import async_playwright
            det.playwright = await async_playwright().start()
            det.browser = await det.playwright.chromium.launch(
                headless=False,
                args=[
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-extensions",
                    "--disable-background-networking",
                    "--disable-renderer-backgrounding",
                    "--disable-breakpad",
                    "--no-first-run",
                    "--disable-features=Translate",
                ]
            )
            storage = None
            if STORAGE_PATH.exists():
                try:
                    storage = STORAGE_PATH.read_text(encoding='utf-8')
                    log_print("[RUN] Using existing storage state file.")
                except Exception:
                    storage = None
            ctx_kwargs = {"viewport": {"width": 1280, "height": 900}}
            if STORAGE_PATH.exists():
                ctx_kwargs["storage_state"] = str(STORAGE_PATH)
            det.context = await det.browser.new_context(**ctx_kwargs)
            det.page = await det.context.new_page()
            log_print("[RUN] Browser ready (non-persistent hardened). Login may be required.")
        except Exception as e2:
            log_print(f"[FATAL] Hardened non-persistent launch failed: {e2}")
            return

        # Attach Playwright event listeners and start tracing
        try:
            det.page.on("console", lambda msg: log_print(f"[PW-CONSOLE] {msg.type}: {msg.text}"))
            det.page.on("pageerror", lambda err: log_print(f"[PW-ERROR] {err}"))
            if det.context:
                await det.context.tracing.start(screenshots=True, snapshots=True, sources=True)
                log_print("[RUN] Tracing started.")
        except Exception as e:
            log_print(f"[WARN] Failed to attach listeners/start tracing: {e}")

        log_print("[RUN] Navigating to Discord source channel...")
        ok = await det.navigate_to_discord()
        if not ok:
            log_print("[FAIL] Navigation to Discord failed. Check DISCORD_CHANNEL_URL / login.")
            return

        # Wait for channel view to be ready (messages loaded)
        try:
            await det.page.wait_for_selector('[data-list-id="chat-messages"]', timeout=20000)
            log_print("[RUN] Channel messages list is present.")
        except Exception as e:
            log_print(f"[WARN] Messages list not detected quickly: {e}")

        log_print("[RUN] Scrolling to latest messages...")
        await det.scroll_to_latest_messages()

        log_print("[RUN] Taking first screenshot (bottom)...")
        img1 = await det.take_screenshot()
        log_print(f"[RUN] First screenshot: {img1}")

        log_print("[RUN] Nudging up and taking second screenshot...")
        try:
            await det.page.evaluate("window.scrollTo(0, Math.max(window.scrollY - 140, 0))")
            await det.page.wait_for_timeout(300)
        except Exception:
            pass
        img2 = await det.take_screenshot()
        log_print(f"[RUN] Second screenshot: {img2}")

        results = []
        if img1:
            log_print("[RUN] OCR on first screenshot...")
            r1 = det.extract_ticker_data_with_ocr(img1)
            log_print("[RUN] OCR1 results:", r1)
            results.extend(r1 or [])
        if img2:
            log_print("[RUN] OCR on second screenshot...")
            r2 = det.extract_ticker_data_with_ocr(img2)
            log_print("[RUN] OCR2 results:", r2)
            results.extend(r2 or [])

        if results:
            # Deduplicate by type, keep latest timestamp
            latest = {}
            from datetime import datetime as _dt
            for item in results:
                t = item.get('type')
                ts = item.get('timestamp')
                if t not in ['NQ','ES','YM','RTY','CL']:
                    continue
                try:
                    dt = _dt.strptime(ts, '%m/%d/%Y %I:%M:%S %p') if ts else None
                except Exception:
                    dt = None
                prev = latest.get(t)
                if prev is None or (dt and _dt.strptime(prev['timestamp'], '%m/%d/%Y %I:%M:%S %p') < dt):
                    latest[t] = item
            log_print(f"[OK] Parsed {len(latest)} unique entries:")
            for v in latest.values():
                log_print("  ", v)
        else:
            log_print("[INFO] No ticker data parsed from live screenshots.")

    finally:
        # Export Playwright trace for post-mortem
        try:
            if getattr(det, 'context', None):
                await det.context.tracing.stop(path="tmp_rovodev_live_trace.zip")
                log_print("[RUN] Trace saved to tmp_rovodev_live_trace.zip")
        except Exception as e:
            log_print(f"[WARN] Failed to save trace: {e}")

        # Save storage state for future runs to avoid repeated login
        try:
            if getattr(det, 'context', None):
                await det.context.storage_state(path=str(STORAGE_PATH))
                log_print(f"[RUN] Storage state saved to {STORAGE_PATH}")
        except Exception as e:
            log_print(f"[WARN] Failed to save storage state: {e}")

        log_print("[RUN] Cleaning up browser context...")
        try:
            if getattr(det, 'context', None):
                await det.context.close()
            if getattr(det, 'browser', None):
                await det.browser.close()
            if getattr(det, 'playwright', None):
                await det.playwright.stop()
        except Exception as e:
            logger.info(f'Cleanup error: {e}')
        log_print("[RUN] Done.")

if __name__ == '__main__':
    asyncio.run(run_once_live())
