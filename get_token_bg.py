"""
DLR Token Extractor (background mode)
Launches Chrome with remote debugging, waits for signal, extracts token.
"""
import subprocess
import os
import time
import json
import sys
import urllib.request

TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "discord_token.txt")
STATUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token_status.json")
PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_data")
EXT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dlr_ext")

def main():
    # Kill existing Chrome
    os.system("taskkill //F //IM chrome.exe 2>nul")
    time.sleep(1)

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")

    # Launch with remote debugging
    subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",
        "--no-first-run",
        "--new-window",
        "https://discord.com/channels/1069289461667598376/1399516015070548091"
    ])

    json.dump({
        "status": "waiting",
        "msg": "Chrome open. Log into Discord #lugs, then I'll grab the token."
    }, open(STATUS_FILE, "w"))

    # Poll for token
    for attempt in range(120):  # 2 minutes
        time.sleep(1)
        try:
            req = urllib.request.urlopen("http://localhost:9222/json", timeout=3)
            tabs = json.loads(req.read())
            for tab in tabs:
                url = tab.get("url", "")
                if "discord.com/channels" in url:
                    # User is logged in! Grab token
                    payload = json.dumps({
                        "method": "Runtime.evaluate",
                        "params": {"expression": "localStorage.getItem('token')"}
                    }).encode()
                    req2 = urllib.request.urlopen(
                        f"http://localhost:9222/json/{tab['id']}/execute",
                        data=payload, timeout=5
                    )
                    result = json.loads(req2.read())
                    token = result.get("result", {}).get("result", {}).get("value", "")
                    if token and len(token) > 20:
                        with open(TOKEN_FILE, "w") as f:
                            f.write(token)
                        
                        # Also inject into DLR profile via Playwright
                        try:
                            from playwright.sync_api import sync_playwright
                            with sync_playwright() as p:
                                ctx = p.chromium.launch_persistent_context(
                                    user_data_dir=PROFILE_DIR, headless=True,
                                    args=["--no-sandbox"]
                                )
                                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                                page.goto("https://discord.com/app", wait_until="domcontentloaded", timeout=30000)
                                time.sleep(2)
                                page.evaluate(f"localStorage.setItem('token', '{token}')")
                                ctx.close()
                        except:
                            pass
                        
                        json.dump({
                            "status": "saved",
                            "token_len": len(token),
                            "msg": f"Token saved! ({len(token)} chars) and injected into DLR profile"
                        }, open(STATUS_FILE, "w"))
                        return
            
            if attempt % 10 == 0:
                json.dump({
                    "status": "checking",
                    "msg": "Waiting for you to reach #lugs channel..."
                }, open(STATUS_FILE, "w"))
                
        except:
            # CDP not ready yet
            if attempt == 5:
                json.dump({
                    "status": "waiting",
                    "msg": "Chrome launching..."
                }, open(STATUS_FILE, "w"))

    json.dump({
        "status": "timeout",
        "msg": "Timed out waiting. Log in and try again."
    }, open(STATUS_FILE, "w"))

if __name__ == "__main__":
    main()
    print("Done", file=sys.stderr)
