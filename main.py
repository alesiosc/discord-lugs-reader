# IMMEDIATE CRASH LOGGING AT TOP LEVEL
import sys
import os

def write_crash_log(message):
    """Write immediate crash log file"""
    try:
        with open("discord_crash_log.txt", "a", encoding='utf-8') as f:
            f.write(f"=== {datetime.now()} ===\n")
            f.write(f"Message: {message}\n")
            f.write(f"Python: {sys.version}\n")
            f.write(f"Executable: {sys.executable}\n")
            f.write(f"Working Dir: {os.getcwd()}\n")
            f.write(f"Args: {sys.argv}\n")
            f.write("="*50 + "\n")
            f.flush()
    except:
        pass  # Don't crash on crash logging

try:
    from datetime import datetime
    write_crash_log("Successfully imported datetime")
except Exception as e:
    write_crash_log(f"Failed to import datetime: {e}")
    sys.exit(1)

try:
    import asyncio
    write_crash_log("Successfully imported asyncio")
except Exception as e:
    write_crash_log(f"Failed to import asyncio: {e}")
    sys.exit(1)

try:
    import threading
    write_crash_log("Successfully imported threading")
except Exception as e:
    write_crash_log(f"Failed to import threading: {e}")
    sys.exit(1)

try:
    import time
    write_crash_log("Successfully imported time")
except Exception as e:
    write_crash_log(f"Failed to import time: {e}")
    sys.exit(1)

try:
    import json
    write_crash_log("Successfully imported json")
except Exception as e:
    write_crash_log(f"Failed to import json: {e}")
    sys.exit(1)

try:
    import random
    write_crash_log("Successfully imported random")
except Exception as e:
    write_crash_log(f"Failed to import random: {e}")
    sys.exit(1)

try:
    import re
    write_crash_log("Successfully imported re")
except Exception as e:
    write_crash_log(f"Failed to import re: {e}")
    sys.exit(1)

try:
    import subprocess
    write_crash_log("Successfully imported subprocess")
except Exception as e:
    write_crash_log(f"Failed to import subprocess: {e}")
    sys.exit(1)

try:
    from pathlib import Path
    write_crash_log("Successfully imported Path")
except Exception as e:
    write_crash_log(f"Failed to import Path: {e}")
    sys.exit(1)

try:
    from typing import List, Dict
    write_crash_log("Successfully imported List, Dict from typing")
except Exception as e:
    write_crash_log(f"Failed to import List, Dict from typing: {e}")
    sys.exit(1)

# Continue with other imports step by step
try:
    from dotenv import load_dotenv
    write_crash_log("Successfully imported dotenv")
except Exception as e:
    write_crash_log(f"Failed to import dotenv: {e}")
    sys.exit(1)

try:
    import requests
    write_crash_log("Successfully imported requests")
except Exception as e:
    write_crash_log(f"Failed to import requests: {e}")
    sys.exit(1)

try:
    import logging
    write_crash_log("Successfully imported logging")
except Exception as e:
    write_crash_log(f"Failed to import logging: {e}")
    sys.exit(1)

try:
    import traceback
    write_crash_log("Successfully imported traceback")
except Exception as e:
    write_crash_log(f"Failed to import traceback: {e}")
    sys.exit(1)

# CRITICAL IMPORTS - Test these last
try:
    from playwright.async_api import async_playwright
    write_crash_log("Successfully imported Playwright")
except Exception as e:
    write_crash_log(f"Failed to import Playwright: {e}")
    sys.exit(1)

write_crash_log("All basic imports successful, proceeding to main code...")



# ADD COMPREHENSIVE DEBUGGING AT START
print("=== STARTING DISCORD LUGS READER WITH DEBUGGING ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Environment variables: WEBHOOK_URL={'set' if os.getenv('WEBHOOK_URL') else 'not set'}, DISCORD_CHANNEL_URL={'set' if os.getenv('DISCORD_CHANNEL_URL') else 'not set'}")

# Set up comprehensive logging
try:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[
            logging.FileHandler('discord_lugs_reader_debug.log', mode='w'),  # Overwrite each time
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    write_crash_log("Logging system initialized successfully")
    
    # Log everything at the start
    logger.info("=== DISCORD LUGS READER STARTING ===")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Arguments: {sys.argv}")
    logger.info(f"Environment variables: WEBHOOK_URL={'set' if os.getenv('WEBHOOK_URL') else 'not set'}")
    logger.info(f"Environment variables: DISCORD_CHANNEL_URL={'set' if os.getenv('DISCORD_CHANNEL_URL') else 'not set'}")
    logger.info(f"Environment variables: HEADLESS_MODE={os.getenv('HEADLESS_MODE', 'not set')}")
    
    # Load environment variables
    try:
        logger.info("Loading environment variables from .env file...")
        # Try multiple .env locations for compatibility
        env_paths = [".env", "discord_lugs_portable_venv/app/login.env", "discord_lugs_portable_venv/app/.env"]
        for env_file in env_paths:
            if os.path.exists(env_file):
                load_dotenv(env_file, override=True)
                logger.info(f"Loaded env from: {env_file}")
            else:
                logger.debug(f"Env file not found (not an error): {env_file}")
        logger.info("Environment variables loaded successfully")
        write_crash_log("Environment variables loaded successfully")
    except Exception as e:
        error_msg = f"Failed to load environment variables: {e}"
        logger.error(error_msg)
        try:
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
        except:
            pass
        write_crash_log(error_msg)
        print("PAUSING - Copy the error above, then press Enter to exit...")
        input()
        sys.exit(1)
except Exception as e:
    error_msg = f"Failed to initialize logging system: {e}"
    write_crash_log(error_msg)
    print(error_msg)
    input("Press Enter to exit...")
    sys.exit(1)

class DiscordBrowserDetector:
    def __init__(self):
        logger.info("=== DISCORD BROWSER DETECTOR INIT START ===")
        try:
            self.discord_url = os.getenv('DISCORD_CHANNEL_URL')
            logger.info(f"Discord URL from env: {self.discord_url}")
            
            self.screenshot_dir = Path('./screenshots')
            self.screenshot_dir.mkdir(exist_ok=True)
            logger.info(f"Screenshot directory: {self.screenshot_dir}")
            
            self.last_refresh_time = datetime.now()
            self.refresh_interval = 300  # Refresh every 5 minutes
            self.screenshot_counter = 0
            self.last_ticker_data = {}
            self.last_messages_hash = None
            
            logger.info("=== DISCORD BROWSER DETECTOR INIT COMPLETE ===")
            
        except Exception as e:
            logger.error(f"ERROR in DiscordBrowserDetector.__init__: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise



    async def setup_browser(self):
        """Initialize browser with proven stable settings."""
        logger.info("=== SETTING UP BROWSER (STABLE) ===")
        try:
            logger.info("Starting Playwright...")
            self.playwright = await async_playwright().start()
            logger.info("Playwright started successfully")
            
            user_data_dir = Path('./browser_data') # Revert to original profile for session persistence
            user_data_dir.mkdir(exist_ok=True)
            logger.info(f"Browser data directory: {user_data_dir}")
            
            headless_mode = os.getenv("HEADLESS_MODE", "false").lower() == "true"
            logger.info(f"Headless mode: {headless_mode}")
            
            logger.info("Launching persistent browser context with stable arguments...")
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(user_data_dir),
                headless=headless_mode,
                viewport={'width': 1920, 'height': 1080},
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-session-crashed-bubble",
                ]
            )
            logger.info("Browser context launched successfully")
            
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            logger.info("Page created/retrieved successfully")
            
            logger.info("=== BROWSER SETUP COMPLETED ===")
            
        except Exception as e:
            logger.error(f"ERROR in setup_browser: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise
        
    async def navigate_to_discord(self):
        """Navigate to Discord channel."""
        try:
            logger.info(f"Navigating to Discord URL: {self.discord_url}")
            await self.page.goto(self.discord_url, wait_until='domcontentloaded', timeout=60000)
            logger.info("Page loaded.")

            # Take an immediate screenshot for debugging startup issues
            try:
                logger.info("Waiting 5 seconds before debug screenshot...")
                await asyncio.sleep(5)
                debug_screenshot_path = "debug_startup_screenshot.png"
                await self.page.screenshot(path=debug_screenshot_path)
                logger.info(f"DEBUG: Startup screenshot saved to {debug_screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take debug screenshot: {e}")

            # AGGRESSIVE POPUP HANDLING
            try:
                logger.info("Attempting to close 'Restore pages' popup by clicking 'Close' button...")
                # This is a guess for the selector. It might be a button with the text "Close".
                await self.page.click('button:has-text("Close")', timeout=5000)
                logger.info("Clicked 'Close' button successfully.")
            except Exception:
                logger.warning("Did not find a 'Close' button, trying 'Escape' key as a fallback.")
                try:
                    await self.page.press('body', 'Escape', timeout=5000)
                    logger.info("'Escape' key pressed successfully.")
                except Exception as e2:
                    logger.warning(f"Could not press 'Escape' as a fallback: {e2}")
            
            return True
                
        except Exception as e:
            logger.error(f"Error navigating to Discord: {e}")
            return False

    async def scroll_to_latest_messages(self):
        """
        More robustly scroll to the bottom of the page by repeatedly pressing 'End'.
        """
        logger.info("--- Scrolling to latest messages (aggressive) ---")
        messages_selector = '[data-list-id="chat-messages"]'
        try:
            await self.page.wait_for_selector(messages_selector, timeout=10000)
            logger.info("Pressing 'End' key 5 times to ensure we are at the bottom...")
            for i in range(5):
                await self.page.press(messages_selector, 'End')
                await self.page.wait_for_timeout(300)  # Wait for UI to settle
            logger.info("Finished aggressive scrolling.")
        except Exception as e:
            logger.warning(f"Could not scroll to latest messages: {e}")

    async def take_screenshot(self):
        """Take a clipped screenshot of the messages area."""
        try:
            self.screenshot_counter += 1
            timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%fZ')
            screenshot_path = self.screenshot_dir / f"page-{timestamp}.png"
            
            logger.info("Taking clipped screenshot of messages area...")
            
            # Try multiple selectors for Discord messages area
            selectors_to_try = [
                '[data-list-id="chat-messages"]',
                '[class*="messagesWrapper"]',
                '[class*="messages"]',
                'main',
                '[role="main"]'
            ]
            
            box = None
            successful_selector = None
            
            for selector in selectors_to_try:
                try:
                    logger.info(f"Trying selector: {selector}")
                    messages_locator = self.page.locator(selector)
                    if await messages_locator.count() > 0:
                        box = await messages_locator.first.bounding_box()
                        if box:
                            successful_selector = selector
                            logger.info(f"Successfully found messages area with selector: {selector}")
                            break
                except Exception as selector_error:
                    logger.debug(f"Selector {selector} failed: {selector_error}")
                    continue
            
            if box and successful_selector:
                await self.page.screenshot(path=str(screenshot_path), clip=box)
                logger.info(f"Clipped screenshot taken using {successful_selector}: {screenshot_path}")
                return str(screenshot_path)
            else:
                logger.warning("Could not find messages container with any selector, taking full page screenshot.")
                await self.page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"Full page screenshot taken: {screenshot_path}")
                return str(screenshot_path)

        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            # Try one final fallback - basic screenshot
            try:
                timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%fZ')
                fallback_path = self.screenshot_dir / f"fallback-{timestamp}.png"
                await self.page.screenshot(path=str(fallback_path))
                logger.info(f"Emergency fallback screenshot taken: {fallback_path}")
                return str(fallback_path)
            except Exception as fallback_error:
                logger.error(f"Even fallback screenshot failed: {fallback_error}")
                return None

    def extract_ticker_data_with_ocr(self, image_path: str) -> List[Dict]:
        """
        Extracts ticker data by communicating with the ocr_watcher.py script
        via the file system.
        """
        logger.info(f"Requesting OCR for {image_path} via file system...")
        request_file = Path("ocr.request")
        response_file = Path("ocr.response")
        
        try:
            # Create the request file
            with open(request_file, 'w') as f:
                f.write(image_path)
            
            # Wait for the response file to be created
            timeout = 300  # seconds (increased to match watcher timeout)
            start_time = time.time()
            while not response_file.exists():
                if time.time() - start_time > timeout:
                    logger.error("Timed out waiting for OCR response file.")
                    if request_file.exists():
                        request_file.unlink() # Clean up stale request
                    return []
                time.sleep(0.5)
            
            logger.info("OCR response file found.")
            
            # Read the response
            with open(response_file, 'r') as f:
                response_content = f.read()
            
            # Clean up the files
            response_file.unlink()
            
            # Parse the JSON data
            if not response_content:
                logger.warning("OCR response file was empty.")
                return []
            
            # Find the start of the JSON data
            json_start_index = response_content.find('[')
            if json_start_index == -1:
                logger.error(f"Could not find start of JSON in OCR response. Content: {response_content}")
                return []
            
            response_json = response_content[json_start_index:]
            
            data = json.loads(response_json)
            
            if data:
                logger.info(f"Successfully parsed {len(data)} items from OCR response.")
            else:
                logger.info("OCR response contained no data.")
                
            return data

        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from OCR response file. Content: {response_content}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred during file-based OCR communication: {e}")
            # Clean up files in case of error
            if request_file.exists():
                request_file.unlink()
            if response_file.exists():
                response_file.unlink()
            return []

    def format_and_randomize_data(self, ticker_data):
        """Format the extracted data and apply randomization"""
        formatted_messages = []
        
        for item in ticker_data:
            # Apply randomization based on ticker type
            randomized_mid = item['mid']
            randomized_lower = item['lower']
            randomized_upper = item['upper']
            
            if item['type'] in ['NQ', 'YM']:
                randomized_mid += random.uniform(-3, 3)
                randomized_lower += random.uniform(-3, 3)
                randomized_upper += random.uniform(-3, 3)
            elif item['type'] == 'ES':
                randomized_mid += random.uniform(-2, 2)
                randomized_lower += random.uniform(-2, 2)
                randomized_upper += random.uniform(-2, 2)
            elif item['type'] == 'CL':  # Added CL with ±0.5 range
                randomized_mid += random.uniform(-0.5, 0.5)
                randomized_lower += random.uniform(-0.5, 0.5)
                randomized_upper += random.uniform(-0.5, 0.5)
            elif item['type'] == 'GC':
                randomized_mid += random.uniform(-0.5, 0.5)
                randomized_lower += random.uniform(-0.5, 0.5)
                randomized_upper += random.uniform(-0.5, 0.5)
            
            # Format timestamp
            dt_object = datetime.strptime(item['timestamp'], '%m/%d/%Y %I:%M:%S %p')
            formatted_timestamp = dt_object.strftime("%Y-%m-%d %H:%M:%S EDT")
            
            formatted_message = f"[{item['type']}] Time: {formatted_timestamp} | Mid: {randomized_mid:.2f}, Lower: {randomized_lower:.2f}, Upper: {randomized_upper:.2f}"
            formatted_messages.append(formatted_message)
        
        return formatted_messages

    def save_to_snapshot(self, ticker_data):
        """Save the extracted ticker data to snapshot.txt in the expected format"""
        if not ticker_data:
            logger.info("No ticker data to save to snapshot")
            return
        
        logger.info(f"Saving {len(ticker_data)} ticker messages to snapshot:")
        for item in ticker_data:
            logger.info(f"  - {item['type']}: {item['timestamp']}")
        
        snapshot_content = "### Page state\n"
        snapshot_content += "- Page URL: https://discord.com/channels/1069289461667598376/1399516015070548091\n"
        snapshot_content += "- Page Title: Discord | #lugs | PWTrades\n"
        snapshot_content += "- Page Snapshot:\n"
        
        for i, item in enumerate(ticker_data):
            # Create a simulated article entry to match snapshot format
            snapshot_content += f'  - article "LugsBot APP , [{item["type"]}] Published Level: Lug Timestamp: {item["timestamp"]}, Mid: {item["mid"]}, Lower: {item["lower"]}, Upper: {item["upper"]} , {datetime.now().strftime("%d/%m/%Y, %H:%M")}" [ref=e{i}]:\n'
            snapshot_content += f'    - generic [ref=e{i}]:\n'
            snapshot_content += f'      - img [ref=e{i}]\n'
            snapshot_content += f'      - heading "LugsBot APP {datetime.now().strftime("%d/%m/%Y, %H:%M")}" [level=3] [ref=e{i}]:\n'
            snapshot_content += f'        - generic [ref=e{i}]:\n'
            snapshot_content += f'          - button "LugsBot" [ref=e{i}]\n'
            snapshot_content += f'          - generic [ref=e{i}]: APP\n'
            snapshot_content += f'        - generic:\n'
            snapshot_content += f'          - generic: —\n'
            snapshot_content += f'          - text: {datetime.now().strftime("%d/%m/%Y, %H:%M")}\n'
            snapshot_content += f'      - generic [ref=e{i}]: "[{item["type"]}] Published Level: Lug Timestamp: {item["timestamp"]}, Mid: {item["mid"]}, Lower: {item["lower"]}, Upper: {item["upper"]}"\n\n'
        
        try:
            with open("snapshot.txt", "w", encoding="utf-8") as f:
                f.write(snapshot_content)
            logger.info(f"Snapshot saved with {len(ticker_data)} ticker messages")
        except Exception as e:
            logger.error(f"Error saving snapshot: {e}")

    async def get_page_content_hash(self):
        """Get a hash of the current page content to detect changes"""
        try:
            # Get page text content to create a hash
            content = await self.page.content()
            import hashlib
            content_hash = hashlib.md5(content.encode()).hexdigest()
            return content_hash
        except Exception as e:
            logger.error(f"Error getting page content hash: {e}")
            return None

    async def needs_refresh(self):
        """Check if we need to refresh the page"""
        return (datetime.now() - self.last_refresh_time).seconds > self.refresh_interval

    async def refresh_page(self):
        """Refresh the Discord page to ensure fresh content"""
        try:
            logger.info("Refreshing Discord page to ensure fresh content...")
            await self.page.reload(wait_until='networkidle', timeout=30000)
            await self.page.wait_for_timeout(5000)  # Wait for reload
            await self.scroll_to_latest_messages()
            self.last_refresh_time = datetime.now()
            logger.info("Page refreshed successfully")
        except Exception as e:
            logger.error(f"Error refreshing page: {e}")

    async def is_browser_alive(self):
        """Check if browser and page are accessible"""
        try:
            if not self.page or self.page.is_closed():
                return False
            # Try a lightweight operation
            await self.page.evaluate("1+1")
            return True
        except:
            return False

    async def restart_browser(self):
        """Restart the browser session"""
        logger.warning("=== RESTARTING BROWSER SESSION ===")
        try:
            await self.close()
        except Exception as e:
            logger.error(f"Error closing during restart: {e}")
        
        await asyncio.sleep(10)
        
        # Retry setup up to 3 times
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self.setup_browser()
                if await self.navigate_to_discord():
                    self.last_refresh_time = datetime.now()
                    logger.info("Browser restarted successfully")
                    return
            except Exception as e:
                logger.error(f"Restart attempt {attempt+1} failed: {e}")
                await asyncio.sleep(10)
        
        logger.error("All browser restart attempts failed")
        raise RuntimeError("Failed to restart browser after multiple attempts")

    async def run_detection_loop(self):
        """Main detection loop"""
        logger.info("Starting detection loop...")
        counter = 0
        last_full_restart = datetime.now()
        restart_interval = 3600  # Restart browser every hour to clear memory leaks
        
        while True:
            try:
                counter += 1
                logger.info(f"\n--- Detection Cycle #{counter} ---")
                
                # 1. Periodic Forced Restart (Memory Leak Protection)
                if (datetime.now() - last_full_restart).seconds > restart_interval:
                    logger.info("PERFORMING SCHEDULED HOURLY BROWSER RESTART...")
                    await self.restart_browser()
                    last_full_restart = datetime.now()
                    continue

                # 2. Check if browser/page is still alive
                if not await self.is_browser_alive():
                    logger.warning("Browser connection lost! Attempting to restart...")
                    await self.restart_browser()
                    continue
                
                # Check if we need to refresh the page
                if await self.needs_refresh():
                    await self.refresh_page()
                
                # Scroll to latest messages to ensure they're loaded
                await self.scroll_to_latest_messages()

                # Click in the messages area to remove focus from any specific element
                try:
                    logger.info("Clicking in the chat messages area to remove focus...")
                    await self.page.click('[data-list-id="chat-messages"]', timeout=5000)
                    logger.info("Clicked successfully.")
                except Exception as e:
                    logger.warning(f"Could not click in chat messages area: {e}")
                
                # Always take a screenshot during testing
                # current_hash = await self.get_page_content_hash()
                # if self.last_messages_hash and current_hash == self.last_messages_hash:
                #     logger.info("Page content hasn't changed, skipping screenshot")
                #     # Still wait 60 seconds but with additional scrolling to trigger any lazy loading
                #     await self.page.evaluate("window.scrollTo(0, window.scrollY - 100)")
                #     await self.page.wait_for_timeout(1000)
                #     await self.page.evaluate("window.scrollTo(0, window.scrollY + 100)")
                #     await asyncio.sleep(60)
                #     continue
                
                # self.last_messages_hash = current_hash
                
                # Take first screenshot at absolute bottom
                # Ensure bottom and slight settle
                try:
                    await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await self.page.wait_for_timeout(500)
                except Exception as e:
                    logger.info(f"Ensure-bottom before shot failed: {e}")
                screenshot_path_1 = await self.take_screenshot()
                if not screenshot_path_1:
                    logger.error("Failed to take screenshot")
                    await asyncio.sleep(15)
                    continue

                # Extract ticker data from the screenshot  
                ticker_data = []
                data1 = self.extract_ticker_data_with_ocr(screenshot_path_1)
                if data1:
                    ticker_data.extend(data1)
                
                # Deduplicate across all screenshots: only keep the latest ticker for each type
                if ticker_data:
                    latest_tickers = {}
                    for ticker in ticker_data:
                        ticker_type = ticker['type']
                        timestamp = ticker['timestamp']
                        
                        # Parse the timestamp for comparison
                        try:
                            dt = datetime.strptime(timestamp, '%m/%d/%Y %I:%M:%S %p')
                        except ValueError:
                            try:
                                dt = datetime.strptime(timestamp, '%m/%d/%Y %I:%M %p')
                            except ValueError:
                                logger.warning(f"Could not parse timestamp for deduplication: {timestamp}")
                                continue
                        
                        # Keep only the latest ticker for each type
                        if ticker_type not in latest_tickers or dt > latest_tickers[ticker_type]['parsed_dt']:
                            latest_tickers[ticker_type] = {
                                'ticker': ticker,
                                'parsed_dt': dt
                            }
                    
                    # Replace ticker_data with only the latest of each type
                    ticker_data = [info['ticker'] for info in latest_tickers.values()]
                    logger.info(f"After deduplication: {len(ticker_data)} unique tickers")

                if ticker_data:
                    logger.info(f"Found {len(ticker_data)} ticker messages")
                    
                    # Check if we have new data compared to last run
                    has_new_data = False
                    for item in ticker_data:
                        key = item['type']
                        if key not in self.last_ticker_data or self.last_ticker_data[key] != item['timestamp']:
                            has_new_data = True
                            break
                    
                    if has_new_data:
                        logger.info("New ticker data detected, updating snapshot")
                        # Save to snapshot.txt for monitor.py to process
                        self.save_to_snapshot(ticker_data)
                        
                        # Update last ticker data
                        for item in ticker_data:
                            self.last_ticker_data[item['type']] = item['timestamp']
                    else:
                        logger.info("No new ticker data detected")
                else:
                    logger.info("No ticker data found")
                
                # Wait 60 seconds
                logger.info("Waiting 60 seconds...")
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in detection loop: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(60)

    def cleanup_processed_images(self):
        """Clean up any processed image files"""
        try:
            if hasattr(self, 'screenshot_dir') and self.screenshot_dir.exists():
                processed_files = list(self.screenshot_dir.glob('*_processed.png'))
                for file_path in processed_files:
                    try:
                        file_path.unlink()
                        logger.info(f"Cleaned up processed image: {file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to clean up {file_path}: {e}")
        except Exception as e:
            logger.warning(f"Error during processed image cleanup: {e}")

    async def close(self):
        """Clean up resources"""
        try:
            # Clean up any processed images
            self.cleanup_processed_images()
            
            # Clean up PaddleOCR if needed
            if hasattr(self, 'ocr') and self.ocr is not None:
                # PaddleOCR doesn't have a specific cleanup method, but we can clear references
                self.ocr = None
                logger.info("Cleared PaddleOCR reference")
            
            # Close browser
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
                logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def load_processed_messages():
    """Load processed messages from file to persist across restarts."""
    try:
        with open('processed_messages.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_processed_messages(processed_keys):
    """Save processed messages to file."""
    with open('processed_messages.json', 'w') as f:
        json.dump(list(processed_keys), f)

def _parse_timestamp_flexible(timestamp_str: str) -> datetime | None:
    """
    Attempts to parse a timestamp string using multiple flexible formats.
    """
    # First, try to clean the timestamp in a targeted way
    # Only replace dots that are part of the time (e.g., 2.42.00 -> 2:42:00)
    # Also handle missing space between date and time
    cleaned_str = re.sub(r'(\d{1,2})\.(\d{2})\.(\d{2})', r'\1:\2:\3', timestamp_str)
    cleaned_str = re.sub(r'(\d{4})\s*(\d{1,2})', r'\1 \2', cleaned_str)

    formats = [
        '%m/%d/%Y %I:%M:%S %p',  # Standard format
        '%m/%d/%Y %I.%M.%S %p',  # OCR reads : as .
        '%m/%d/%Y%I:%M:%S %p',   # Missing space after year
        '%m/%d/%Y.%I:%M:%S %p',  # Dot after year
    ]
    
    # Try parsing the cleaned string first
    for fmt in formats:
        try:
            return datetime.strptime(cleaned_str, fmt)
        except ValueError:
            continue
            
    # If cleaned string fails, try parsing the original string
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue

    logger.warning(f"Could not parse timestamp string: '{timestamp_str}' (or cleaned version '{cleaned_str}') with any known format.")
    return None

def get_latest_messages():
    """Fetches the latest messages from the snapshot file."""
    logger.info("Getting latest messages from snapshot.txt...")
    try:
        with open("snapshot.txt", 'r') as f:
            snapshot_content = f.read()
        logger.info(f"Snapshot content:\n{snapshot_content}")
        
        messages = []
        if snapshot_content:
            lines = snapshot_content.split('\n')
            for line in lines:
                if 'article' in line and 'LugsBot' in line:
                    try:
                        # Extract the message content between quotes
                        message_match = re.search(r'"([^"]*)"', line)
                        if message_match:
                            full_message = message_match.group(1)
                            # Extract the ticker info part from the message
                            ticker_match = re.search(r'\[([A-Z]+)\].*?Timestamp: ([^,]+), Mid: (None|[\d.]+), Lower: (None|[\d.]+), Upper: (None|[\d.]+)', full_message)
                            if ticker_match:
                                msg_type = ticker_match.group(1)
                                timestamp_str = ticker_match.group(2)
                                # Convert timestamp string to datetime object for proper sorting
                                dt_object = _parse_timestamp_flexible(timestamp_str)
                                if not dt_object:
                                    logger.error(f"Failed to parse timestamp from snapshot: {timestamp_str}")
                                    continue
                                
                                mid_str = ticker_match.group(3)
                                lower_str = ticker_match.group(4)
                                upper_str = ticker_match.group(5)

                                mid = float(mid_str) if mid_str != 'None' else 0.0
                                lower = float(lower_str) if lower_str != 'None' else 0.0
                                upper = float(upper_str) if upper_str != 'None' else 0.0
                                
                                # Reconstruct the message in the expected format
                                reconstructed_message = f"[{msg_type}] Timestamp: {timestamp_str}, Mid: {mid}, Lower: {lower}, Upper: {upper}"
                                messages.append({
                                    'message': reconstructed_message,
                                    'type': msg_type,
                                    'timestamp': dt_object
                                })
                    except Exception as e:
                        logger.error(f"Error processing line: {line}, Error: {e}")
                        pass
        
        # Sort messages by timestamp (most recent first) and keep only the latest for each type
        if messages:
            # Sort by timestamp, descending (most recent first)
            messages.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Return all messages
            return [msg['message'] for msg in messages]
        else:
            return []
    except FileNotFoundError:
        logger.info("snapshot.txt not found. Please wait for it to be created.")
        return []
    except Exception as e:
        logger.error(f"An error occurred while getting messages: {e}")
        return []

def format_message(message, randomization_settings):
    """Formats a message string into the desired format."""
    logger.info(f"Formatting message: {message}")
    try:
        parts = message.split(",")
        msg_type = parts[0].split("]")[0].strip("[")
        timestamp_str = parts[0].split("Timestamp:")[1].strip()
        mid = float(parts[1].split(":")[1].strip())
        lower = float(parts[2].split(":")[1].strip())
        upper = float(parts[3].split(":")[1].strip())

        # Apply randomization based on ticker type
        rand_min = randomization_settings.get(f'RANDOM_{msg_type}_MIN', 0)
        rand_max = randomization_settings.get(f'RANDOM_{msg_type}_MAX', 0)
        mid += random.uniform(rand_min, rand_max)
        lower += random.uniform(rand_min, rand_max)
        upper += random.uniform(rand_min, rand_max)

        # Convert timestamp (keep original time as requested)
        dt_object = _parse_timestamp_flexible(timestamp_str)
        if not dt_object:
            logger.error(f"Failed to parse timestamp for formatting: {timestamp_str}")
            return None
            
        formatted_timestamp = dt_object.strftime("%Y-%m-%d %H:%M:%S EDT")

        # Format with integers (no decimals) to match Layla format style
        return f"[{msg_type}] Time: {formatted_timestamp} | Mid: {int(mid)}, Lower: {int(lower)}, Upper: {int(upper)}"
    except Exception as e:
        logger.error(f"Error formatting message: {e}")
        return None

def send_to_discord(message):
    """Sends a message to the Discord webhook."""
    logger.info(f"Sending message to Discord: {message}")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL not set. Cannot send message.")
        return

    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status() # Raise an exception for bad status codes
        logger.info("Message sent successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message to Discord: {e}")

def run_monitor():
    """Run the monitor loop in a separate thread."""
    processed_message_keys = load_processed_messages()
    logger.info(f"Loaded {len(processed_message_keys)} previously processed messages")
    # Read DUPLICATES setting from .env
    duplicates_enabled = os.getenv("DUPLICATES", "false").lower() == "true"
    logger.info(f"Duplicates enabled: {duplicates_enabled}")

    # Read enabled tickers from .env
    enabled_tickers_str = os.getenv('ENABLED_TICKERS', 'NQ,ES,YM,CL,GC')
    enabled_tickers = {ticker.strip() for ticker in enabled_tickers_str.split(',')}
    logger.info(f"Enabled tickers: {enabled_tickers}")

    # Read randomization settings from .env
    randomization_settings = {}
    for key, value in os.environ.items():
        if key.startswith("RANDOM_"):
            try:
                randomization_settings[key] = float(value)
            except ValueError:
                logger.error(f"Invalid randomization value for {key}: {value}. Must be a number.")
    logger.info(f"Loaded randomization settings: {randomization_settings}")

    while True:
        logger.info("\n--- Checking for new messages ---")
        messages = get_latest_messages()
        new_messages_found = False

        if not messages:
            logger.info("No messages found.")
        else:
            for message in messages:
                logger.info(f"RAW MESSAGE: {message}")
                # Create a key based on message type and timestamp to avoid duplicates
                try:
                    # Extract ticker type and timestamp from message
                    msg_type_match = re.search(r'\[([A-Z]+)\]', message)
                    timestamp_match = re.search(r'Timestamp: ([^,]+)', message)
                    
                    if msg_type_match and timestamp_match:
                        msg_type = msg_type_match.group(1)
                        logger.info(f"Extracted msg_type: {msg_type}")
                        
                        # Only process tickers that are enabled in the .env file
                        if msg_type not in enabled_tickers:
                            logger.info(f"DROPPED: Skipping {msg_type} because it is not in ENABLED_TICKERS {enabled_tickers}")
                            continue
                        
                        logger.info(f"ACCEPTED: Processing {msg_type} (Enabled)")

                        timestamp_str = timestamp_match.group(1).strip()
                        logger.info(f"Extracted timestamp_str: {timestamp_str}")
                        message_key = f"{msg_type}_{timestamp_str}"
                        
                        if duplicates_enabled:
                            formatted_message = format_message(message, randomization_settings)
                            if formatted_message:
                                send_to_discord(formatted_message)
                                new_messages_found = True
                        elif message_key not in processed_message_keys:
                            new_messages_found = True
                            logger.info(f"New message found: {message}")
                            formatted_message = format_message(message, randomization_settings)
                            if formatted_message:
                                send_to_discord(formatted_message)
                                # Only add to processed if successfully sent
                                processed_message_keys.add(message_key)
                                save_processed_messages(processed_message_keys)
                        else:
                            logger.info(f"Message already processed: {message}")
                    else:
                        logger.warning(f"Could not extract msg_type and timestamp from message: {message}")
                        # Fallback to using the entire message as key
                        if duplicates_enabled:
                            # We still need to check the ticker type here
                            msg_type_match = re.search(r'\[([A-Z]+)\]', message)
                            if msg_type_match and msg_type_match.group(1) not in enabled_tickers:
                                logger.info(f"Skipping {msg_type_match.group(1)} because it is not in enabled_tickers.")
                                continue

                            formatted_message = format_message(message, randomization_settings)
                            if formatted_message:
                                send_to_discord(formatted_message)
                                new_messages_found = True
                        elif message not in processed_message_keys:
                            # And here as well
                            msg_type_match = re.search(r'\[([A-Z]+)\]', message)
                            if msg_type_match and msg_type_match.group(1) not in enabled_tickers:
                                logger.info(f"Skipping {msg_type_match.group(1)} because it is not in enabled_tickers.")
                                continue
                                
                            new_messages_found = True
                            logger.info(f"New message found: {message}")
                            formatted_message = format_message(message, randomization_settings)
                            if formatted_message:
                                send_to_discord(formatted_message)
                                # Only add to processed if successfully sent
                                processed_message_keys.add(message)
                                save_processed_messages(processed_message_keys)
                        else:
                            logger.info(f"Message already processed: {message}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        
        if not new_messages_found:
            logger.info("No new messages.")

        # Wait for 60 seconds before checking again
        logger.info("Waiting for 60 seconds...")
        time.sleep(60)

async def main():
    """Main function to run both browser detector and monitor."""
    logger.info("=== MAIN FUNCTION STARTING ===")
    try:
        # Ensure a clean slate for snapshot.txt at startup
        snapshot_file = Path("snapshot.txt")
        if snapshot_file.exists():
            snapshot_file.unlink()
            logger.info("Removed existing snapshot.txt to ensure fresh data.")

        # Check if we should run in headless mode
        headless_mode = os.getenv("HEADLESS_MODE", "false").lower() == "true"
        logger.info(f"Headless mode setting: {headless_mode}")
        
        # Create an instance of the detector
        logger.info("Creating DiscordBrowserDetector instance...")
        detector = DiscordBrowserDetector()
        logger.info("DiscordBrowserDetector instance created")
        
        # Setup browser
        logger.info("=== CALLING SETUP_BROWSER ===")
        await detector.setup_browser()
        logger.info("=== SETUP_BROWSER COMPLETED ===")
        
        # Navigate to Discord
        logger.info("=== CALLING NAVIGATE_TO_DISCORD ===")
        success = await detector.navigate_to_discord()
        if not success:
            logger.error("Failed to navigate to Discord")
            return
        
        # Run the monitor in a separate thread
        logger.info("Starting monitor thread...")
        monitor_thread = threading.Thread(target=run_monitor, daemon=True)
        monitor_thread.start()
        logger.info("Monitor thread started")
        
        # Run detection loop
        logger.info("=== STARTING DETECTION LOOP ===")
        await detector.run_detection_loop()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"=== FATAL ERROR IN MAIN ===")
        logger.error(f"Error in main: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        logger.error(f"Stack trace: {traceback.format_stack()}")
    finally:
        logger.info("=== CLEANING UP ===")
        if 'detector' in locals():
            await detector.close()
        logger.info("=== MAIN FUNCTION ENDED ===")

if __name__ == "__main__":
    try:
        print("=== STARTING MAIN APPLICATION ===")
        asyncio.run(main())
    except Exception as e:
        print(f"=== CRITICAL STARTUP ERROR ===")
        print(f"Error: {e}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        print("PAUSING - Copy the error above, then press Enter to exit...")
        input()
        sys.exit(1)
