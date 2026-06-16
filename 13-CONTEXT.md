=== STARTING DISCORD LUGS READER WITH DEBUGGING ===
Python executable: D:\MyPythonProjects_2\discord_lugs_reader+Portable-WORKING\venv311_new\Scripts\python.exe
Python version: 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]
Current working directory: D:\MyPythonProjects_2\discord_lugs_reader+Portable-WORKING
Environment variables: WEBHOOK_URL=not set, DISCORD_CHANNEL_URL=not set
2026-06-16 14:15:06,946 - __main__ - INFO - === DISCORD LUGS READER STARTING ===
2026-06-16 14:15:06,947 - __main__ - INFO - Python executable: D:\MyPythonProjects_2\discord_lugs_reader+Portable-WORKING\venv311_new\Scripts\python.exe
2026-06-16 14:15:06,947 - __main__ - INFO - Python version: 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]
2026-06-16 14:15:06,947 - __main__ - INFO - Current working directory: D:\MyPythonProjects_2\discord_lugs_reader+Portable-WORKING
2026-06-16 14:15:06,947 - __main__ - INFO - Arguments: ['D:\\MyPythonProjects_2\\discord_lugs_reader+Portable-WORKING\\main.py']
2026-06-16 14:15:06,947 - __main__ - INFO - Environment variables: WEBHOOK_URL=not set
2026-06-16 14:15:06,948 - __main__ - INFO - Environment variables: DISCORD_CHANNEL_URL=not set
2026-06-16 14:15:06,948 - __main__ - INFO - Environment variables: HEADLESS_MODE=not set
2026-06-16 14:15:06,948 - __main__ - INFO - Loading environment variables from .env file...
2026-06-16 14:15:06,948 - __main__ - DEBUG - Env file not found (not an error): .env
2026-06-16 14:15:06,975 - __main__ - INFO - Loaded env from: discord_lugs_portable_venv/app/login.env
2026-06-16 14:15:06,975 - __main__ - DEBUG - Env file not found (not an error): discord_lugs_portable_venv/app/.env
2026-06-16 14:15:06,975 - __main__ - INFO - Environment variables loaded successfully
=== STARTING MAIN APPLICATION ===
2026-06-16 14:15:06,984 - asyncio - DEBUG - Using proactor: IocpProactor
2026-06-16 14:15:06,985 - __main__ - INFO - === MAIN FUNCTION STARTING ===
2026-06-16 14:15:06,991 - __main__ - INFO - Removed existing snapshot.txt to ensure fresh data.
2026-06-16 14:15:06,991 - __main__ - INFO - Headless mode setting: True
2026-06-16 14:15:06,991 - __main__ - INFO - Creating DiscordBrowserDetector instance...
2026-06-16 14:15:06,991 - __main__ - INFO - === DISCORD BROWSER DETECTOR INIT START ===
2026-06-16 14:15:06,991 - __main__ - INFO - Discord URL from env: https://discord.com/channels/1069289461667598376/1399516015070548091
2026-06-16 14:15:06,993 - __main__ - INFO - Screenshot directory: screenshots
2026-06-16 14:15:06,993 - __main__ - INFO - === DISCORD BROWSER DETECTOR INIT COMPLETE ===
2026-06-16 14:15:06,994 - __main__ - INFO - DiscordBrowserDetector instance created
2026-06-16 14:15:06,996 - __main__ - INFO - === CALLING SETUP_BROWSER ===
2026-06-16 14:15:06,997 - __main__ - INFO - === SETTING UP BROWSER (STABLE) ===
2026-06-16 14:15:06,997 - __main__ - INFO - Starting Playwright...
2026-06-16 14:15:07,566 - __main__ - INFO - Playwright started successfully
2026-06-16 14:15:07,572 - __main__ - INFO - Browser data directory: browser_data
2026-06-16 14:15:07,572 - __main__ - INFO - Headless mode: True
2026-06-16 14:15:07,572 - __main__ - INFO - Launching persistent browser context with stable arguments...
2026-06-16 14:15:08,632 - __main__ - INFO - Browser context launched successfully
2026-06-16 14:15:08,632 - __main__ - INFO - Page created/retrieved successfully
2026-06-16 14:15:08,634 - __main__ - INFO - === BROWSER SETUP COMPLETED ===
2026-06-16 14:15:08,634 - __main__ - INFO - === SETUP_BROWSER COMPLETED ===
2026-06-16 14:15:08,635 - __main__ - INFO - === CALLING NAVIGATE_TO_DISCORD ===
2026-06-16 14:15:08,635 - __main__ - INFO - Navigating to Discord URL: https://discord.com/channels/1069289461667598376/1399516015070548091
2026-06-16 14:15:17,152 - __main__ - INFO - Page loaded.
2026-06-16 14:15:17,152 - __main__ - INFO - Waiting 5 seconds before debug screenshot...
2026-06-16 14:15:22,288 - __main__ - INFO - DEBUG: Startup screenshot saved to debug_startup_screenshot.png
2026-06-16 14:15:22,288 - __main__ - INFO - Attempting to close 'Restore pages' popup by clicking 'Close' button...
2026-06-16 14:15:27,296 - __main__ - WARNING - Did not find a 'Close' button, trying 'Escape' key as a fallback.
2026-06-16 14:15:28,526 - __main__ - INFO - 'Escape' key pressed successfully.
2026-06-16 14:15:28,526 - __main__ - INFO - Starting monitor thread...
2026-06-16 14:15:28,528 - __main__ - INFO - Monitor thread started
2026-06-16 14:15:28,529 - __main__ - INFO - === STARTING DETECTION LOOP ===
2026-06-16 14:15:28,529 - __main__ - INFO - Starting detection loop...
2026-06-16 14:15:28,529 - __main__ - INFO -
--- Detection Cycle #1 ---
2026-06-16 14:15:28,608 - __main__ - INFO - Loaded 731 previously processed messages
2026-06-16 14:15:28,608 - __main__ - INFO - Duplicates enabled: False
2026-06-16 14:15:28,610 - __main__ - INFO - Enabled tickers: {'ES', 'CL', 'NQ', 'GC', 'YM'}
2026-06-16 14:15:28,616 - __main__ - INFO - Loaded randomization settings: {}
2026-06-16 14:15:28,616 - __main__ - INFO -
--- Checking for new messages ---
2026-06-16 14:15:28,617 - __main__ - INFO - Getting latest messages from snapshot.txt...
2026-06-16 14:15:28,622 - __main__ - INFO - snapshot.txt not found. Please wait for it to be created.
2026-06-16 14:15:28,623 - __main__ - INFO - No messages found.
2026-06-16 14:15:28,624 - __main__ - INFO - No new messages.
2026-06-16 14:15:28,624 - __main__ - INFO - Waiting for 60 seconds...
2026-06-16 14:15:28,912 - __main__ - INFO - --- Scrolling to latest messages (aggressive) ---
2026-06-16 14:15:38,934 - __main__ - WARNING - Could not scroll to latest messages: Page.wait_for_selector: Timeout 10000ms exceeded.
Call log:
  - waiting for locator("[data-list-id=\"chat-messages\"]") to be visible

2026-06-16 14:15:38,934 - __main__ - INFO - Clicking in the chat messages area to remove focus...
2026-06-16 14:15:43,941 - __main__ - WARNING - Could not click in chat messages area: Page.click: Timeout 5000ms exceeded.
Call log:
  - waiting for locator("[data-list-id=\"chat-messages\"]")

2026-06-16 14:15:44,457 - __main__ - INFO - Taking clipped screenshot of messages area...
2026-06-16 14:15:44,458 - __main__ - INFO - Trying selector: [data-list-id="chat-messages"]
2026-06-16 14:15:44,608 - __main__ - INFO - Trying selector: [class*="messagesWrapper"]
2026-06-16 14:15:44,612 - __main__ - INFO - Trying selector: [class*="messages"]
2026-06-16 14:15:44,615 - __main__ - INFO - Trying selector: main
2026-06-16 14:15:44,619 - __main__ - INFO - Trying selector: [role="main"]
2026-06-16 14:15:44,622 - __main__ - WARNING - Could not find messages container with any selector, taking full page screenshot.
2026-06-16 14:15:45,138 - __main__ - INFO - Full page screenshot taken: screenshots\page-2026-06-16T14-15-44-457736Z.png
2026-06-16 14:15:45,138 - __main__ - INFO - Requesting OCR for screenshots\page-2026-06-16T14-15-44-457736Z.png via file system...
2026-06-16 14:15:45,228 - __main__ - INFO - OCR response file found.
2026-06-16 14:15:45,233 - __main__ - INFO - Successfully parsed 4 items from OCR response.
2026-06-16 14:15:45,236 - __main__ - INFO - After deduplication: 4 unique tickers
2026-06-16 14:15:45,236 - __main__ - INFO - Found 4 ticker messages
2026-06-16 14:15:45,237 - __main__ - INFO - New ticker data detected, updating snapshot
2026-06-16 14:15:45,238 - __main__ - INFO - Saving 4 ticker messages to snapshot:
2026-06-16 14:15:45,238 - __main__ - INFO -   - ES: 06/15/2026 11:51:00 AM
2026-06-16 14:15:45,239 - __main__ - INFO -   - YM: 06/15/2026 01:24:00 PM
2026-06-16 14:15:45,239 - __main__ - INFO -   - CL: 06/14/2026 10:26:00 PM
2026-06-16 14:15:45,239 - __main__ - INFO -   - GC: 06/14/2026 09:33:00 PM
2026-06-16 14:15:45,246 - __main__ - INFO - Snapshot saved with 4 ticker messages
2026-06-16 14:15:45,246 - __main__ - INFO - Waiting 60 seconds...
2026-06-16 14:16:28,626 - __main__ - INFO -
--- Checking for new messages ---
2026-06-16 14:16:28,626 - __main__ - INFO - Getting latest messages from snapshot.txt...
2026-06-16 14:16:28,627 - __main__ - INFO - Snapshot content:
### Page state
- Page URL: https://discord.com/channels/1069289461667598376/1399516015070548091
- Page Title: Discord | #lugs | PWTrades
- Page Snapshot:
  - article "LugsBot APP , [ES] Published Level: Lug Timestamp: 06/15/2026 11:51:00 AM, Mid: 7642.75, Lower: 7564.25, Upper: 7721.25 , 16/06/2026, 14:15" [ref=e0]:
    - generic [ref=e0]:
      - img [ref=e0]
      - heading "LugsBot APP 16/06/2026, 14:15" [level=3] [ref=e0]:
        - generic [ref=e0]:
          - button "LugsBot" [ref=e0]
          - generic [ref=e0]: APP
        - generic:
          - generic: â€”
          - text: 16/06/2026, 14:15
      - generic [ref=e0]: "[ES] Published Level: Lug Timestamp: 06/15/2026 11:51:00 AM, Mid: 7642.75, Lower: 7564.25, Upper: 7721.25"

  - article "LugsBot APP , [YM] Published Level: Lug Timestamp: 06/15/2026 01:24:00 PM, Mid: 52379.0, Lower: 52015.0, Upper: 52743.0 , 16/06/2026, 14:15" [ref=e1]:
    - generic [ref=e1]:
      - img [ref=e1]
      - heading "LugsBot APP 16/06/2026, 14:15" [level=3] [ref=e1]:
        - generic [ref=e1]:
          - button "LugsBot" [ref=e1]
          - generic [ref=e1]: APP
        - generic:
          - generic: â€”
          - text: 16/06/2026, 14:15
      - generic [ref=e1]: "[YM] Published Level: Lug Timestamp: 06/15/2026 01:24:00 PM, Mid: 52379.0, Lower: 52015.0, Upper: 52743.0"

  - article "LugsBot APP , [CL] Published Level: Lug Timestamp: 06/14/2026 10:26:00 PM, Mid: 80.48, Lower: 77.16, Upper: 83.81 , 16/06/2026, 14:15" [ref=e2]:
    - generic [ref=e2]:
      - img [ref=e2]
      - heading "LugsBot APP 16/06/2026, 14:15" [level=3] [ref=e2]:
        - generic [ref=e2]:
          - button "LugsBot" [ref=e2]
          - generic [ref=e2]: APP
        - generic:
          - generic: â€”
          - text: 16/06/2026, 14:15
      - generic [ref=e2]: "[CL] Published Level: Lug Timestamp: 06/14/2026 10:26:00 PM, Mid: 80.48, Lower: 77.16, Upper: 83.81"

  - article "LugsBot APP , [GC] Published Level: Lug Timestamp: 06/14/2026 09:33:00 PM, Mid: 4328.3, Lower: 4251.3, Upper: 4405.3 , 16/06/2026, 14:15" [ref=e3]:
    - generic [ref=e3]:
      - img [ref=e3]
      - heading "LugsBot APP 16/06/2026, 14:15" [level=3] [ref=e3]:
        - generic [ref=e3]:
          - button "LugsBot" [ref=e3]
          - generic [ref=e3]: APP
        - generic:
          - generic: â€”
          - text: 16/06/2026, 14:15
      - generic [ref=e3]: "[GC] Published Level: Lug Timestamp: 06/14/2026 09:33:00 PM, Mid: 4328.3, Lower: 4251.3, Upper: 4405.3"


2026-06-16 14:16:28,628 - __main__ - INFO - RAW MESSAGE: [YM] Timestamp: 06/15/2026 01:24:00 PM, Mid: 52379.0, Lower: 52015.0, Upper: 52743.0
2026-06-16 14:16:28,629 - __main__ - INFO - Extracted msg_type: YM
2026-06-16 14:16:28,629 - __main__ - INFO - ACCEPTED: Processing YM (Enabled)
2026-06-16 14:16:28,629 - __main__ - INFO - Extracted timestamp_str: 06/15/2026 01:24:00 PM
2026-06-16 14:16:28,630 - __main__ - INFO - Message already processed: [YM] Timestamp: 06/15/2026 01:24:00 PM, Mid: 52379.0, Lower: 52015.0, Upper: 52743.0
2026-06-16 14:16:28,630 - __main__ - INFO - RAW MESSAGE: [ES] Timestamp: 06/15/2026 11:51:00 AM, Mid: 7642.75, Lower: 7564.25, Upper: 7721.25
2026-06-16 14:16:28,630 - __main__ - INFO - Extracted msg_type: ES
2026-06-16 14:16:28,631 - __main__ - INFO - ACCEPTED: Processing ES (Enabled)
2026-06-16 14:16:28,631 - __main__ - INFO - Extracted timestamp_str: 06/15/2026 11:51:00 AM
2026-06-16 14:16:28,631 - __main__ - INFO - Message already processed: [ES] Timestamp: 06/15/2026 11:51:00 AM, Mid: 7642.75, Lower: 7564.25, Upper: 7721.25
2026-06-16 14:16:28,632 - __main__ - INFO - RAW MESSAGE: [CL] Timestamp: 06/14/2026 10:26:00 PM, Mid: 80.48, Lower: 77.16, Upper: 83.81
2026-06-16 14:16:28,632 - __main__ - INFO - Extracted msg_type: CL
2026-06-16 14:16:28,633 - __main__ - INFO - ACCEPTED: Processing CL (Enabled)
2026-06-16 14:16:28,633 - __main__ - INFO - Extracted timestamp_str: 06/14/2026 10:26:00 PM
2026-06-16 14:16:28,633 - __main__ - INFO - Message already processed: [CL] Timestamp: 06/14/2026 10:26:00 PM, Mid: 80.48, Lower: 77.16, Upper: 83.81
2026-06-16 14:16:28,634 - __main__ - INFO - RAW MESSAGE: [GC] Timestamp: 06/14/2026 09:33:00 PM, Mid: 4328.3, Lower: 4251.3, Upper: 4405.3
2026-06-16 14:16:28,634 - __main__ - INFO - Extracted msg_type: GC
2026-06-16 14:16:28,634 - __main__ - INFO - ACCEPTED: Processing GC (Enabled)
2026-06-16 14:16:28,635 - __main__ - INFO - Extracted timestamp_str: 06/14/2026 09:33:00 PM
2026-06-16 14:16:28,635 - __main__ - INFO - Message already processed: [GC] Timestamp: 06/14/2026 09:33:00 PM, Mid: 4328.3, Lower: 4251.3, Upper: 4405.3
2026-06-16 14:16:28,635 - __main__ - INFO - No new messages.
2026-06-16 14:16:28,636 - __main__ - INFO - Waiting for 60 seconds...