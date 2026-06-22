"""
DLR Token Extractor
Opens Discord in your real Chrome, you log in, then saves the token.
"""
import subprocess
import os
import time
import json
import sys
import tempfile
import shutil

TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "discord_token.txt")
EXT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dlr_ext")
PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_data")

# Step 1: Get the token via CDP from user's Chrome
print("=" * 60)
print("DLR Token Extractor")
print("=" * 60)
print()
print("This will:")
print("1. Open Discord in YOUR Chrome browser")
print("2. You log in to the #lugs channel")
print("3. I'll grab the token from localStorage")
print()

# Kill existing Chrome
os.system("taskkill //F //IM chrome.exe 2>nul")
time.sleep(1)

# Launch Chrome with remote debugging and user's default profile
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")

print(f"Chrome: {chrome_path}")
print()

proc = subprocess.Popen([
    chrome_path,
    "--remote-debugging-port=9222",
    "--no-first-run",
    "--new-window",
    "https://discord.com/channels/1069289461667598376/1399516015070548091"
])

print("✓ Chrome opened. Log in to Discord and get to the #lugs channel.")
print("  Then press ENTER here to extract the token...")
input()

# Try to get token via CDP
import urllib.request
import json

try:
    # Get tabs
    req = urllib.request.urlopen("http://localhost:9222/json", timeout=5)
    tabs = json.loads(req.read())
    
    token = None
    for tab in tabs:
        url = tab.get("url", "")
        if "discord" in url:
            # Execute JS to get token
            payload = json.dumps({
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "localStorage.getItem('token')"
                }
            }).encode()
            req2 = urllib.request.urlopen(
                f"http://localhost:9222/json/{tab['id']}/execute",
                data=payload,
                timeout=5
            )
            result = json.loads(req2.read())
            token_val = result.get("result", {}).get("result", {}).get("value", "")
            if token_val and len(token_val) > 20:
                token = token_val
                break
    
    if token:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        print(f"\n✓ Token saved! ({len(token)} chars)")
        print(f"  Saved to: {TOKEN_FILE}")
        
        # Also inject into DLR profile via storage
        print("\n  Also injecting into DLR's browser_data profile via Playwright...")
        
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=True,
                args=["--no-sandbox"]
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto("https://discord.com/app", wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            page.evaluate(f"localStorage.setItem('token', '{token}')")
            ctx.close()
        
        print("  ✓ Injected into DLR profile!")
        print("\nDLR should now work with the saved token.")
    else:
        print("\n✗ Could not find Discord token.")
        print("  Make sure you're logged into Discord in Chrome and try again.")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("  Make sure Chrome is open with --remote-debugging-port=9222")

proc.terminate()
input("\nPress Enter to exit...")
