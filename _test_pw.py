import asyncio, time, sys
from playwright.async_api import async_playwright

t0 = time.time()
print(f'[{t0:.1f}] Starting playwright async init...', flush=True)

async def main():
    p = await async_playwright().start()
    t1 = time.time()
    print(f'[{t1:.1f}] Playwright started in {t1-t0:.1f}s', flush=True)
    print(f'Chromium path: {p.chromium.executable_path}', flush=True)
    await p.stop()
    print('Done', flush=True)

asyncio.run(main())
