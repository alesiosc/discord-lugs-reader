import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Try system Chrome channel for stability
        browser = await p.chromium.launch(channel="chrome", headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://example.com", wait_until="domcontentloaded")
        print("Browser opened and navigated to example.com")
        await page.wait_for_timeout(20000)
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
