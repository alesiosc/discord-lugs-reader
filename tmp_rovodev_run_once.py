import asyncio
import sys

# Import the detector and logger from main.py
from main import DiscordBrowserDetector, logger

async def run_once():
    det = DiscordBrowserDetector()
    try:
        await det.setup_browser()
        ok = await det.navigate_to_discord()
        if not ok:
            print('Navigation to Discord failed. Check DISCORD_CHANNEL_URL and login state.')
            return

        # Ensure bottom and small settle, then screenshot
        await det.scroll_to_latest_messages()
        path1 = await det.take_screenshot()

        # Slight nudge up and take second screenshot
        try:
            await det.page.evaluate("window.scrollTo(0, Math.max(window.scrollY - 140, 0))")
            await det.page.wait_for_timeout(300)
        except Exception:
            pass
        path2 = await det.take_screenshot()

        all_data = []
        if path1:
            data1 = det.extract_ticker_data_with_ocr(path1)
            if data1:
                all_data.extend(data1)
        if path2:
            data2 = det.extract_ticker_data_with_ocr(path2)
            if data2:
                all_data.extend(data2)

        if all_data:
            # Deduplicate by type, keep latest timestamp
            latest = {}
            for item in all_data:
                t = item.get('type')
                ts = item.get('timestamp')
                if t not in ['NQ','ES','YM','RTY','CL']:
                    continue
                try:
                    from datetime import datetime
                    dt = datetime.strptime(ts, '%m/%d/%Y %I:%M:%S %p') if ts else None
                except Exception:
                    dt = None
                prev = latest.get(t)
                if prev is None or (dt and datetime.strptime(prev['timestamp'], '%m/%d/%Y %I:%M:%S %p') < dt):
                    latest[t] = item

            print(f'Parsed {len(latest)} entries:')
            for k,v in latest.items():
                print(v)
        else:
            print('No ticker data parsed in this one-off run.')

    finally:
        try:
            if getattr(det, 'context', None):
                await det.context.close()
            if getattr(det, 'playwright', None):
                await det.playwright.stop()
        except Exception as e:
            logger.info(f'Cleanup error: {e}')

if __name__ == '__main__':
    asyncio.run(run_once())
