
====================================
  Discord LUGS Reader - Portable
====================================
[CONFIG] Show CMD Window: true

[INFO] Launching in VISIBLE mode...
[INFO] Command output will be shown below
[INFO] To hide: Set SHOW_CMD_WINDOW=false in app\.env

[INFO] Starting OCR Watcher in background...
[INFO] Starting Discord LUGS Reader...
[INFO] Both OCR Watcher and Main App are running
[INFO] Check logs\ directory for detailed logs
[INFO] Press Ctrl+C to stop both applications

=== STARTING DISCORD LUGS READER WITH DEBUGGING ===
Python executable: D:\MyPythonProjects_2\TESTING\discord_lugs_reader-ES-YM-NQ WORKING-REDUCE SIZE - Copy\discord_lugs_portable_venv\python\python.exe
Python version: 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]
Current working directory: D:\MyPythonProjects_2\TESTING\discord_lugs_reader-ES-YM-NQ WORKING-REDUCE SIZE - Copy\discord_lugs_portable_venv\app
Environment variables: WEBHOOK_URL=not set, DISCORD_CHANNEL_URL=not set
2025-11-15 13:53:37,547 - __main__ - INFO - === DISCORD LUGS READER STARTING ===
2025-11-15 13:53:37,555 - __main__ - INFO - Python executable: D:\MyPythonProjects_2\TESTING\discord_lugs_reader-ES-YM-NQ WORKING-REDUCE SIZE - Copy\discord_lugs_portable_venv\python\python.exe
2025-11-15 13:53:37,555 - __main__ - INFO - Python version: 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]
2025-11-15 13:53:37,555 - __main__ - INFO - Current working directory: D:\MyPythonProjects_2\TESTING\discord_lugs_reader-ES-YM-NQ WORKING-REDUCE SIZE - Copy\discord_lugs_portable_venv\app
2025-11-15 13:53:37,555 - __main__ - INFO - Arguments: ['main.py']
2025-11-15 13:53:37,556 - __main__ - INFO - Environment variables: WEBHOOK_URL=not set
2025-11-15 13:53:37,556 - __main__ - INFO - Environment variables: DISCORD_CHANNEL_URL=not set
2025-11-15 13:53:37,556 - __main__ - INFO - Environment variables: HEADLESS_MODE=not set
2025-11-15 13:53:37,557 - __main__ - INFO - Loading environment variables from .env file...
2025-11-15 13:53:37,557 - __main__ - INFO - Environment variables loaded successfully
=== STARTING MAIN APPLICATION ===
2025-11-15 13:53:37,564 - asyncio - DEBUG - Using proactor: IocpProactor
2025-11-15 13:53:37,564 - __main__ - INFO - === MAIN FUNCTION STARTING ===
2025-11-15 13:53:37,564 - __main__ - INFO - Headless mode setting: False
2025-11-15 13:53:37,564 - __main__ - INFO - Creating DiscordBrowserDetector instance...
2025-11-15 13:53:37,564 - __main__ - INFO - === DISCORD BROWSER DETECTOR INIT START ===
2025-11-15 13:53:37,564 - __main__ - INFO - Discord URL from env: https://discord.com/channels/1069289461667598376/1399516015070548091
2025-11-15 13:53:37,564 - __main__ - INFO - Screenshot directory: screenshots
2025-11-15 13:53:37,574 - __main__ - INFO - === DISCORD BROWSER DETECTOR INIT COMPLETE ===
2025-11-15 13:53:37,574 - __main__ - INFO - DiscordBrowserDetector instance created
2025-11-15 13:53:37,574 - __main__ - INFO - === CALLING SETUP_BROWSER ===
2025-11-15 13:53:37,574 - __main__ - INFO - === SETTING UP BROWSER (STABLE) ===
2025-11-15 13:53:37,574 - __main__ - INFO - Starting Playwright...
2025-11-15 13:53:42,102 - __main__ - INFO - Playwright started successfully
2025-11-15 13:53:42,102 - __main__ - INFO - Browser data directory: browser_data_stable
2025-11-15 13:53:42,103 - __main__ - INFO - Headless mode: False
2025-11-15 13:53:42,104 - __main__ - INFO - Launching persistent browser context with stable arguments...
2025-11-15 13:53:44,380 - __main__ - INFO - Browser context launched successfully
2025-11-15 13:53:44,380 - __main__ - INFO - Page created/retrieved successfully
2025-11-15 13:53:44,380 - __main__ - INFO - === BROWSER SETUP COMPLETED ===
2025-11-15 13:53:44,380 - __main__ - INFO - === SETUP_BROWSER COMPLETED ===
2025-11-15 13:53:44,380 - __main__ - INFO - === CALLING NAVIGATE_TO_DISCORD ===
2025-11-15 13:53:44,380 - __main__ - INFO - === STARTING DISCORD NAVIGATION WITH LOGIN ===
2025-11-15 13:53:44,380 - __main__ - INFO - Attempting direct navigation to Discord channel: https://discord.com/channels/1069289461667598376/1399516015070548091
2025-11-15 13:53:48,512 - __main__ - INFO - Current URL after direct navigation: https://discord.com/channels/1069289461667598376/1399516015070548091
--- Logging error ---
Traceback (most recent call last):
  File "logging\__init__.py", line 1113, in emit
  File "encodings\cp1252.py", line 19, in encode
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 44: character maps to <undefined>
Call stack:
  File "D:\MyPythonProjects_2\TESTING\discord_lugs_reader-ES-YM-NQ WORKING-REDUCE SIZE - Copy\discord_lugs_portable_venv\app\main.py", line 1259, in <module>
    asyncio.run(main())
  File "asyncio\runners.py", line 190, in run
  File "asyncio\runners.py", line 118, in run
  File "asyncio\base_events.py", line 641, in run_until_complete
  File "asyncio\windows_events.py", line 321, in run_forever
  File "asyncio\base_events.py", line 608, in run_forever
  File "asyncio\base_events.py", line 1936, in _run_once
  File "asyncio\events.py", line 84, in _run
  File "D:\MyPythonProjects_2\TESTING\discord_lugs_reader-ES-YM-NQ WORKING-REDUCE SIZE - Copy\discord_lugs_portable_venv\app\main.py", line 1227, in main
    success = await detector.navigate_to_discord()
  File "D:\MyPythonProjects_2\TESTING\discord_lugs_reader-ES-YM-NQ WORKING-REDUCE SIZE - Copy\discord_lugs_portable_venv\app\main.py", line 334, in navigate_to_discord
    logger.info("✅ Already logged in - direct channel access successful!")
  File "logging\__init__.py", line 1489, in info
  File "logging\__init__.py", line 1634, in _log
  File "logging\__init__.py", line 1644, in handle
  File "logging\__init__.py", line 1706, in callHandlers
  File "logging\__init__.py", line 978, in handle
  File "logging\__init__.py", line 1230, in emit
  File "logging\__init__.py", line 1118, in emit
Message: '✅ Already logged in - direct channel access successful!'
Arguments: ()
2025-11-15 13:53:48,512 - __main__ - INFO - ✅ Already logged in - direct channel access successful!
2025-11-15 13:53:50,235 - __main__ - INFO - Taking debug screenshot...
2025-11-15 13:53:52,482 - __main__ - INFO - DEBUG: Startup screenshot saved to debug_startup_screenshot.png
2025-11-15 13:53:52,483 - __main__ - INFO - Checking for popups...
2025-11-15 13:53:55,493 - __main__ - INFO - No popups found to close.
2025-11-15 13:53:55,629 - __main__ - INFO - Pressed Escape as precaution.
2025-11-15 13:53:55,630 - __main__ - INFO - === DISCORD NAVIGATION COMPLETED ===
2025-11-15 13:53:55,631 - __main__ - INFO - Starting monitor thread...
2025-11-15 13:53:55,631 - __main__ - INFO - Monitor thread started
2025-11-15 13:53:55,632 - __main__ - INFO - Loaded 0 previously processed messages
2025-11-15 13:53:55,632 - __main__ - INFO - === STARTING DETECTION LOOP ===
2025-11-15 13:53:55,632 - __main__ - INFO - Duplicates enabled: True
2025-11-15 13:53:55,633 - __main__ - INFO - Starting detection loop...
2025-11-15 13:53:55,633 - __main__ - INFO - Enabled tickers: {'ES', 'NQ', 'YM'}
2025-11-15 13:53:55,634 - __main__ - INFO -
--- Detection Cycle #1 ---
2025-11-15 13:53:55,634 - __main__ - INFO - Loaded randomization settings: {'RANDOM_NQ_POSITIVE_MIN': 1.0, 'RANDOM_NQ_POSITIVE_MAX': 3.0, 'RANDOM_NQ_NEGATIVE_MIN': -3.0, 'RANDOM_NQ_NEGATIVE_MAX': -1.0, 'RANDOM_ES_POSITIVE_MIN': 1.0, 'RANDOM_ES_POSITIVE_MAX': 2.0, 'RANDOM_ES_NEGATIVE_MIN': -2.0, 'RANDOM_ES_NEGATIVE_MAX': -1.0, 'RANDOM_YM_POSITIVE_MIN': 1.0, 'RANDOM_YM_POSITIVE_MAX': 4.0, 'RANDOM_YM_NEGATIVE_MIN': -4.0, 'RANDOM_YM_NEGATIVE_MAX': -1.0, 'RANDOM_RTY_POSITIVE_MIN': 0.3, 'RANDOM_RTY_POSITIVE_MAX': 1.0, 'RANDOM_RTY_NEGATIVE_MIN': -1.0, 'RANDOM_RTY_NEGATIVE_MAX': -0.3, 'RANDOM_CL_POSITIVE_MIN': 0.02, 'RANDOM_CL_POSITIVE_MAX': 0.08, 'RANDOM_CL_NEGATIVE_MIN': -0.08, 'RANDOM_CL_NEGATIVE_MAX': -0.02, 'RANDOM_GC_POSITIVE_MIN': 0.5, 'RANDOM_GC_POSITIVE_MAX': 2.0, 'RANDOM_GC_NEGATIVE_MIN': -2.0, 'RANDOM_GC_NEGATIVE_MAX': -0.5}
2025-11-15 13:53:55,636 - __main__ - INFO -
--- Checking for new messages ---
2025-11-15 13:53:55,636 - __main__ - INFO - Getting latest messages from snapshot.txt...
2025-11-15 13:53:55,637 - __main__ - INFO - snapshot.txt not found. Please wait for it to be created.
2025-11-15 13:53:55,637 - __main__ - INFO - No messages found.
2025-11-15 13:53:55,638 - __main__ - INFO - No new messages.
2025-11-15 13:53:55,638 - __main__ - INFO - Waiting for 60 seconds...
2025-11-15 13:53:55,640 - __main__ - INFO - --- Scrolling to latest messages (aggressive) ---
2025-11-15 13:53:55,657 - __main__ - INFO - Pressing 'End' key 5 times to ensure we are at the bottom...
2025-11-15 13:53:57,401 - __main__ - INFO - Finished aggressive scrolling.
2025-11-15 13:53:57,401 - __main__ - INFO - Clicking in the chat messages area to remove focus...
2025-11-15 13:53:57,601 - __main__ - INFO - Clicked successfully.
2025-11-15 13:53:58,122 - __main__ - INFO - Taking clipped screenshot of messages area...
2025-11-15 13:53:58,122 - __main__ - INFO - Trying selector: [data-list-id="chat-messages"]
2025-11-15 13:53:58,191 - __main__ - INFO - Successfully found messages area with selector: [data-list-id="chat-messages"]
2025-11-15 13:53:58,330 - __main__ - INFO - Clipped screenshot taken using [data-list-id="chat-messages"]: screenshots\page-2025-11-15T13-53-58-122029Z.png
2025-11-15 13:53:58,330 - __main__ - INFO - Requesting OCR for screenshots\page-2025-11-15T13-53-58-122029Z.png via file system...
2025-11-15 13:53:59,338 - __main__ - INFO - OCR response file found.
2025-11-15 13:53:59,338 - __main__ - INFO - OCR response contained no data.
2025-11-15 13:53:59,338 - __main__ - INFO - No ticker data found
2025-11-15 13:53:59,338 - __main__ - INFO - Waiting 60 seconds...
2025-11-15 13:54:55,639 - __main__ - INFO -
--- Checking for new messages ---
2025-11-15 13:54:55,639 - __main__ - INFO - Getting latest messages from snapshot.txt...
2025-11-15 13:54:55,640 - __main__ - INFO - snapshot.txt not found. Please wait for it to be created.
2025-11-15 13:54:55,640 - __main__ - INFO - No messages found.
2025-11-15 13:54:55,641 - __main__ - INFO - No new messages.
2025-11-15 13:54:55,641 - __main__ - INFO - Waiting for 60 seconds...
2025-11-15 13:54:59,357 - __main__ - INFO -
--- Detection Cycle #2 ---
2025-11-15 13:54:59,365 - __main__ - INFO - --- Scrolling to latest messages (aggressive) ---
2025-11-15 13:54:59,375 - __main__ - INFO - Pressing 'End' key 5 times to ensure we are at the bottom...
2025-11-15 13:55:01,106 - __main__ - INFO - Finished aggressive scrolling.
2025-11-15 13:55:01,106 - __main__ - INFO - Clicking in the chat messages area to remove focus...
2025-11-15 13:55:01,230 - __main__ - INFO - Clicked successfully.
2025-11-15 13:55:01,748 - __main__ - INFO - Taking clipped screenshot of messages area...
2025-11-15 13:55:01,748 - __main__ - INFO - Trying selector: [data-list-id="chat-messages"]
2025-11-15 13:55:01,764 - __main__ - INFO - Successfully found messages area with selector: [data-list-id="chat-messages"]
2025-11-15 13:55:01,904 - __main__ - INFO - Clipped screenshot taken using [data-list-id="chat-messages"]: screenshots\page-2025-11-15T13-55-01-748014Z.png
2025-11-15 13:55:01,904 - __main__ - INFO - Requesting OCR for screenshots\page-2025-11-15T13-55-01-748014Z.png via file system...
2025-11-15 13:55:02,411 - __main__ - INFO - OCR response file found.
2025-11-15 13:55:02,416 - __main__ - INFO - OCR response contained no data.
2025-11-15 13:55:02,416 - __main__ - INFO - No ticker data found
2025-11-15 13:55:02,416 - __main__ - INFO - Waiting 60 seconds...
2025-11-15 13:55:55,643 - __main__ - INFO -
--- Checking for new messages ---
2025-11-15 13:55:55,643 - __main__ - INFO - Getting latest messages from snapshot.txt...
2025-11-15 13:55:55,644 - __main__ - INFO - snapshot.txt not found. Please wait for it to be created.
2025-11-15 13:55:55,644 - __main__ - INFO - No messages found.
2025-11-15 13:55:55,645 - __main__ - INFO - No new messages.
2025-11-15 13:55:55,645 - __main__ - INFO - Waiting for 60 seconds...
2025-11-15 13:56:02,447 - __main__ - INFO -
--- Detection Cycle #3 ---
2025-11-15 13:56:02,447 - __main__ - INFO - --- Scrolling to latest messages (aggressive) ---
2025-11-15 13:56:02,457 - __main__ - INFO - Pressing 'End' key 5 times to ensure we are at the bottom...
2025-11-15 13:56:04,195 - __main__ - INFO - Finished aggressive scrolling.
2025-11-15 13:56:04,195 - __main__ - INFO - Clicking in the chat messages area to remove focus...
2025-11-15 13:56:04,324 - __main__ - INFO - Clicked successfully.
2025-11-15 13:56:04,837 - __main__ - INFO - Taking clipped screenshot of messages area...
2025-11-15 13:56:04,837 - __main__ - INFO - Trying selector: [data-list-id="chat-messages"]
2025-11-15 13:56:04,852 - __main__ - INFO - Successfully found messages area with selector: [data-list-id="chat-messages"]
2025-11-15 13:56:04,998 - __main__ - INFO - Clipped screenshot taken using [data-list-id="chat-messages"]: screenshots\page-2025-11-15T13-56-04-837364Z.png
2025-11-15 13:56:04,998 - __main__ - INFO - Requesting OCR for screenshots\page-2025-11-15T13-56-04-837364Z.png via file system...
2025-11-15 13:56:05,505 - __main__ - INFO - OCR response file found.
2025-11-15 13:56:05,508 - __main__ - INFO - OCR response contained no data.
2025-11-15 13:56:05,508 - __main__ - INFO - No ticker data found
2025-11-15 13:56:05,510 - __main__ - INFO - Waiting 60 seconds...