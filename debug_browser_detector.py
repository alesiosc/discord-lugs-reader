import asyncio
import os
import json
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from paddleocr import PaddleOCR
from dotenv import load_dotenv
import logging
from pathlib import Path
import re

# Enhanced logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DiscordBrowserDebugger:
    def __init__(self):
        self.discord_url = os.getenv('DISCORD_CHANNEL_URL')
        self.screenshot_dir = Path('./debug_screenshots')
        self.screenshot_dir.mkdir(exist_ok=True)
        self.ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        
    async def debug_discord_state(self):
        """Comprehensive Discord state debugging"""
        playwright = await async_playwright().start()
        
        try:
            # Launch browser in headed mode for debugging
            logger.info("Launching browser in headed mode for debugging...")
            browser = await playwright.chromium.launch(
                headless=False,  # IMPORTANT: Keep False for debugging
                args=['--start-maximized']
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
                # Note: Removed record_video_dir to avoid storage issues
            )
            
            page = await context.new_page()
            
            # Enable console logging
            page.on('console', lambda msg: logger.info(f'Browser console: {msg.text}'))
            page.on('pageerror', lambda err: logger.error(f'Page error: {err}'))
            
            # Step 1: Navigate and verify URL
            logger.info(f"Navigating to: {self.discord_url}")
            await page.goto(self.discord_url, wait_until='domcontentloaded', timeout=60000)
            await page.wait_for_timeout(5000)
            
            current_url = page.url
            logger.info(f"Current URL after navigation: {current_url}")
            
            # Step 2: Check for login/authentication
            if 'login' in current_url.lower() or 'auth' in current_url.lower():
                logger.error("AUTHENTICATION REQUIRED - Browser is at login page")
                # In debug mode, we'll wait for manual login
                logger.info("Please manually log in to Discord. Waiting 60 seconds...")
                for i in range(60):
                    await page.wait_for_timeout(1000)
                    logger.info(f"Waiting for login... {60-i} seconds remaining")
                    # Check if we've moved past login
                    new_url = page.url
                    if 'login' not in new_url.lower() and 'auth' not in new_url.lower():
                        logger.info("Login appears to be complete")
                        break
            
            # Step 3: Verify we're in the right channel
            await self._verify_channel_context(page)
            
            # Step 4: Force refresh and scroll to latest
            logger.info("Forcing page refresh...")
            await page.reload(wait_until='networkidle')
            await page.wait_for_timeout(3000)
            
            # Step 5: Scroll to absolute bottom multiple times
            await self._aggressive_scroll_to_latest(page)
            
            # Step 6: Take diagnostic screenshots
            await self._take_diagnostic_screenshots(page)
            
            # Step 7: Extract and analyze visible messages
            await self._analyze_visible_messages(page)
            
            logger.info("Debug session complete. Check debug log and screenshots for analysis.")
            
        except Exception as e:
            logger.error(f"Error in debug session: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await context.close()
            await browser.close()
            await playwright.stop()

    async def _verify_channel_context(self, page):
        """Verify we're in the correct Discord channel"""
        try:
            # Look for channel-specific elements
            channel_header = await page.query_selector('[class*="title"]')
            if channel_header:
                channel_text = await channel_header.inner_text()
                logger.info(f"Current channel header: {channel_text}")
            
            # Check for server name
            server_elements = await page.query_selector_all('[class*="guildName"]')
            for elem in server_elements:
                server_text = await elem.inner_text()
                logger.info(f"Server name found: {server_text}")
                
            # Check URL structure
            current_url = page.url
            logger.info(f"Current Discord URL: {current_url}")
            
            # Verify it's a Discord channels URL
            if 'discord.com/channels/' in current_url:
                logger.info("URL structure appears correct for Discord channels")
            else:
                logger.warning("URL may not be pointing to correct Discord channel")
                
        except Exception as e:
            logger.error(f"Error verifying channel context: {e}")

    async def _aggressive_scroll_to_latest(self, page):
        """Aggressively scroll to ensure latest content is visible"""
        try:
            logger.info("Performing aggressive scroll to latest messages...")
            
            # Multiple scroll attempts with different techniques
            for i in range(5):
                logger.info(f"Scroll attempt {i+1}/5")
                
                # Technique 1: Scroll to absolute bottom
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                
                # Technique 2: Scroll up slightly then back down (trigger lazy loading)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight - 500)")
                await page.wait_for_timeout(1000)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                
                # Technique 3: Use Discord-specific scroll behavior
                try:
                    await page.evaluate("""
                        const container = document.querySelector('[class*="scroller"]') || 
                                         document.querySelector('[class*="messages"]') ||
                                         document.querySelector('[class*="chat"]');
                        if (container) {
                            container.scrollTop = container.scrollHeight;
                        }
                    """)
                    await page.wait_for_timeout(2000)
                except:
                    logger.info("Discord-specific scroll technique failed, continuing with generic approach")
                
                logger.info("Scroll attempt completed")
            
            logger.info("Aggressive scrolling completed")
            
        except Exception as e:
            logger.error(f"Error during aggressive scrolling: {e}")

    async def _take_diagnostic_screenshots(self, page):
        """Take diagnostic screenshots for analysis"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Full page screenshot
            full_screenshot_path = self.screenshot_dir / f"full_page_{timestamp}.png"
            await page.screenshot(path=str(full_screenshot_path), full_page=True)
            logger.info(f"Full page screenshot saved: {full_screenshot_path}")
            
            # Viewport screenshot
            viewport_screenshot_path = self.screenshot_dir / f"viewport_{timestamp}.png"
            await page.screenshot(path=str(viewport_screenshot_path), full_page=False)
            logger.info(f"Viewport screenshot saved: {viewport_screenshot_path}")
            
            # Screenshot of message area specifically
            try:
                message_area = await page.query_selector('[class*="messages"]') or await page.query_selector('[class*="chat"]')
                if message_area:
                    area_screenshot_path = self.screenshot_dir / f"message_area_{timestamp}.png"
                    await message_area.screenshot(path=str(area_screenshot_path))
                    logger.info(f"Message area screenshot saved: {area_screenshot_path}")
            except:
                logger.info("Could not capture specific message area screenshot")
                
        except Exception as e:
            logger.error(f"Error taking diagnostic screenshots: {e}")

    async def _analyze_visible_messages(self, page):
        """Extract and analyze visible messages to check content freshness"""
        try:
            # Get page content
            content = await page.content()
            
            # Look for timestamp patterns in the content
            timestamp_pattern = r'\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+(?:AM|PM)'
            timestamps = re.findall(timestamp_pattern, content, re.IGNORECASE)
            
            if timestamps:
                logger.info(f"Found {len(timestamps)} timestamps in page content")
                # Show first few timestamps
                for i, ts in enumerate(timestamps[:10]):
                    logger.info(f"Timestamp {i+1}: {ts}")
            else:
                logger.info("No timestamps found in page content")
            
            # Look for ticker patterns specifically
            ticker_pattern = r'\[([A-Z]+)\].*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM))'
            tickers = re.findall(ticker_pattern, content, re.IGNORECASE | re.DOTALL)
            
            if tickers:
                logger.info(f"Found {len(tickers)} ticker patterns in page content")
                for i, (ticker_type, timestamp) in enumerate(tickers[:10]):
                    logger.info(f"Ticker {i+1}: [{ticker_type}] at {timestamp}")
            else:
                logger.info("No ticker patterns found in page content")
            
            # Save content for further analysis
            content_path = self.screenshot_dir / f"page_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Page content saved to: {content_path}")
            
        except Exception as e:
            logger.error(f"Error analyzing visible messages: {e}")

async def main():
    """Main debug function"""
    logger.info("Starting Discord Browser Debug Session")
    debugger = DiscordBrowserDebugger()
    await debugger.debug_discord_state()
    logger.info("Debug session ended")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv(".env", override=True)
    asyncio.run(main())