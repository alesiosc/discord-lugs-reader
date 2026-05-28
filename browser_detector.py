import asyncio
import os
import sys
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from enhanced_ocr import EnhancedOCR
from dotenv import load_dotenv
import logging
from pathlib import Path
import re
import random

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('browser_detector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

class DiscordBrowserDetector:
    def __init__(self):
        self.discord_url = os.getenv('DISCORD_CHANNEL_URL')
        self.screenshot_dir = Path('./screenshots')
        self.screenshot_dir.mkdir(exist_ok=True)
        self.ocr = EnhancedOCR(timeout_seconds=30)  # Use enhanced OCR wrapper with timeout
        self.last_refresh_time = datetime.now()
        self.refresh_interval = 300  # Refresh every 5 minutes
        self.screenshot_counter = 0
        self.last_ticker_data = {}
        self.last_messages_hash = None  # To track if messages have changed
        
    async def setup_browser(self):
        """Initialize browser with proper Discord configuration"""
        self.playwright = await async_playwright().start()
        
        # Use persistent context to maintain Discord login
        user_data_dir = Path('./browser_data')
        user_data_dir.mkdir(exist_ok=True)
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,  # Set to True after debugging
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/Los_Angeles',
            permissions=['notifications'],
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # Get or create page
        pages = self.context.pages
        self.page = pages[0] if pages else await self.context.new_page()
        
        # Set user agent to avoid detection
        await self.page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        logger.info("Browser setup completed")
        
    async def navigate_to_discord(self):
        """Navigate to Discord channel with verification"""
        try:
            logger.info(f"Navigating to Discord URL: {self.discord_url}")
            
            # Navigate to Discord
            response = await self.page.goto(self.discord_url, wait_until='networkidle', timeout=60000)
            
            if not response.ok:
                logger.warning(f"Navigation response not OK: {response.status}")
            
            # Wait for Discord to fully load
            await self.page.wait_for_timeout(5000)
            
            # Check for Discord-specific elements
            try:
                # Wait for message container
                await self.page.wait_for_selector('[class*="messageContent"]', timeout=30000)
                logger.info("Discord message container loaded")
                
                # Scroll to bottom to get latest messages
                await self.scroll_to_latest_messages()
                
            except Exception as e:
                logger.error(f"Discord elements not found: {e}")
                # Try alternative selectors
                try:
                    await self.page.wait_for_selector('[class*="messages"]', timeout=15000)
                    logger.info("Alternative message container loaded")
                    await self.scroll_to_latest_messages()
                except Exception as e2:
                    logger.error(f"Alternative Discord elements not found: {e2}")
                    return False
                
        except Exception as e:
            logger.error(f"Error navigating to Discord: {e}")
            return False
            
        return True

    async def scroll_to_latest_messages(self):
        """Scroll to bottom of Discord chat to get latest messages"""
        try:
            logger.info("Performing enhanced scroll to latest messages (bottom of chat)...")
            
            # Discord loads messages in chunks, starting with the most recent
            # We need to make sure we're at the absolute bottom to see the latest messages
            for i in range(10):  # Multiple attempts to ensure we're at the bottom
                logger.info(f"Scroll to bottom attempt {i+1}/10")
                
                # Get current position
                old_scroll_pos = await self.page.evaluate("window.scrollY")
                old_doc_height = await self.page.evaluate("document.body.scrollHeight")
                
                # Scroll to bottom
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await self.page.wait_for_timeout(2000)
                
                # Check if we're at the bottom by seeing if scrollY is at the bottom
                new_scroll_pos = await self.page.evaluate("window.scrollY")
                new_doc_height = await self.page.evaluate("document.body.scrollHeight")
                window_height = await self.page.evaluate("window.innerHeight")
                scroll_bottom = new_scroll_pos + window_height
                
                # If we're close to the bottom, we might be at the latest messages
                is_at_bottom = (new_doc_height - scroll_bottom) < 100
                content_grew = new_doc_height > old_doc_height
                
                logger.info(f"  Position: scrollY={new_scroll_pos}, docHeight={new_doc_height}, winHeight={window_height}, at_bottom={is_at_bottom}, content_grew={content_grew}")
                
                # If content grew, that means more messages loaded, so scroll to bottom again
                if content_grew:
                    logger.info("  New content loaded, scrolling to bottom again")
                    await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await self.page.wait_for_timeout(1000)
                elif is_at_bottom:
                    logger.info("  Reached bottom of chat, latest messages should be visible")
                    break
                else:
                    logger.info("  Still more content to load, will try again")
            
            # Additional Discord-specific scrolling to ensure latest messages are loaded
            try:
                await self.page.evaluate("""
                    (function() {
                        // Look for Discord's specific chat containers and scroll to bottom
                        const selectors = [
                            '[data-list-id*="chat-messages"]',
                            '[class*="scrollerInner"]',
                            '[class*="messagesWrapper"]',
                            '[class*="scroller"]'
                        ];
                        
                        for (let selector of selectors) {
                            const elements = document.querySelectorAll(selector);
                            for (let element of elements) {
                                // Ensure we're at the bottom of the virtual list
                                element.scrollTop = element.scrollHeight;
                            }
                        }
                    })();
                """)
                logger.info("Discord-specific scrolling completed")
            except Exception as e:
                logger.info(f"Discord-specific scroll technique failed: {e}")
            
            # Wait a bit more for all messages to render
            logger.info("Waiting for messages to fully render...")
            await self.page.wait_for_timeout(5000)
            
            logger.info("Enhanced scrolling to latest messages completed")
                    
        except Exception as e:
            logger.error(f"Error scrolling to latest messages: {e}")

    async def take_screenshot(self):
        """Take a screenshot of the Discord channel"""
        try:
            self.screenshot_counter += 1
            timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%fZ')
            screenshot_path = self.screenshot_dir / f"page-{timestamp}.png"
            
            # Ensure the directory exists
            self.screenshot_dir.mkdir(exist_ok=True)
            
            # Take screenshot of the full page
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"Screenshot taken: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None

    def extract_ticker_data_with_ocr(self, image_path):
        """Extract ticker data from the screenshot using PaddleOCR"""
        try:
            # Perform OCR on the image
            # use enhanced OCR wrapper
            return self.ocr.extract_ticker_data(image_path)
        
        except Exception as e:
            logger.error(f"Error during PaddleOCR processing: {e}")
            import traceback
            traceback.print_exc()
            return []



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
            snapshot_content += f'          - generic: \u2014\n'
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

    async def run_detection_loop(self):
        """Main detection loop"""
        logger.info("Starting detection loop...")
        counter = 0
        
        while True:
            try:
                counter += 1
                logger.info(f"\n--- Detection Cycle #{counter} ---")
                
                # Check if we need to refresh the page
                if await self.needs_refresh():
                    await self.refresh_page()
                
                # Scroll to latest messages to ensure they're loaded
                await self.scroll_to_latest_messages()
                
                # Check if page content has changed (optional: to avoid unnecessary screenshots)
                current_hash = await self.get_page_content_hash()
                if self.last_messages_hash and current_hash == self.last_messages_hash:
                    logger.info("Page content hasn't changed, skipping screenshot")
                    # Still wait 60 seconds but with additional scrolling to trigger any lazy loading
                    await self.page.evaluate("window.scrollTo(0, window.scrollY - 100)")
                    await self.page.wait_for_timeout(1000)
                    await self.page.evaluate("window.scrollTo(0, window.scrollY + 100)")
                    await asyncio.sleep(60)
                    continue
                
                self.last_messages_hash = current_hash
                
                # Take screenshot
                screenshot_path = await self.take_screenshot()
                if not screenshot_path:
                    logger.error("Failed to take screenshot")
                    await asyncio.sleep(60)
                    continue
                
                # Extract ticker data
                ticker_data = self.extract_ticker_data_with_ocr(screenshot_path)
                
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

    async def close(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")

async def main():
    """Main function"""
    detector = DiscordBrowserDetector()
    
    try:
        # Setup browser
        await detector.setup_browser()
        
        # Navigate to Discord
        success = await detector.navigate_to_discord()
        if not success:
            logger.error("Failed to navigate to Discord")
            return
        
        # Run detection loop
        await detector.run_detection_loop()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await detector.close()

if __name__ == "__main__":
    asyncio.run(main())