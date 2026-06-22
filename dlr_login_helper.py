"""
DLR One-Time Login Helper
Loads the session-saver extension and opens Discord for manual login.
Once you log in, the extension saves the token. All future DLR runs
will auto-restore it — even after Discord logs you out.
"""
import asyncio
import sys
import os
from pathlib import Path
from playwright.async_api import async_playwright

EXT_PATH = Path(__file__).parent / "dlr_ext"
PROFILE_DIR = Path(__file__).parent / "browser_data"

async def main():
    print("=" * 60)
    print("DLR Discord Login Helper")
    print("=" * 60)
    print()
    print(f"Extension: {EXT_PATH}")
    print(f"Profile:   {PROFILE_DIR}")
    print()
    print("This will open a Chrome browser with the DLR session-saver extension.")
    print("Log in to Discord manually. The extension will automatically save")
    print("your auth token so DLR never asks again.")
    print()
    print("Close the browser when done.")
    print()

    PROFILE_DIR.mkdir(exist_ok=True)

    p = await async_playwright().start()
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        viewport={'width': 1920, 'height': 1080},
        args=[
            f'--disable-extensions-except={EXT_PATH}',
            f'--load-extension={EXT_PATH}',
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-web-security',
        ]
    )

    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    print("Navigating to Discord...")
    await page.goto("https://discord.com/login", wait_until="domcontentloaded", timeout=120000)
    print()
    print("✓ Browser is open. Log in to Discord.")
    print("  The extension at dlr_ext/ will save your token automatically.")
    print()

    # Wait for browser to close
    await page.wait_for_event("close", timeout=600000)

    # Check if extension saved a token
    print()
    print("Browser closed. Checking if token was saved...")

    # Verify by trying to inject and read from storage
    token = None
    try:
        token = await page.evaluate("localStorage.getItem('token')")
    except:
        pass

    if token and len(token) > 20:
        print(f"✓ Token saved! ({len(token)} chars)")
        print("  All future DLR runs will use the session-saver extension.")
        print("  If Discord logs you out, the extension restores the token automatically.")
    else:
        print("⚠ No token detected in localStorage.")
        print("  The extension needs a valid Discord login session.")
        print("  You may need to log in and try again.")

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(main())
