import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import logging
import re

# Enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def deep_discord_debug():
    """Deep debug to understand Discord message loading"""
    load_dotenv(".env", override=True)
    discord_url = os.getenv('DISCORD_CHANNEL_URL')
    
    playwright = await async_playwright().start()
    
    try:
        # Launch browser in headed mode for debugging
        logger.info("Launching browser in headed mode for deep debugging...")
        browser = await playwright.chromium.launch(
            headless=False,  # Keep False for debugging
            args=['--start-maximized']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        # Enable console logging
        page.on('console', lambda msg: logger.info(f'Browser console: {msg.text}'))
        page.on('pageerror', lambda err: logger.error(f'Page error: {err}'))
        
        # Navigate to Discord
        logger.info(f"Navigating to: {discord_url}")
        await page.goto(discord_url, wait_until='domcontentloaded', timeout=60000)
        await page.wait_for_timeout(5000)
        
        # Check authentication
        current_url = page.url
        logger.info(f"Current URL: {current_url}")
        
        if 'login' in current_url.lower() or 'auth' in current_url.lower():
            logger.info("On login page, waiting for manual login...")
            await page.wait_for_timeout(60000)  # Wait 60 seconds for manual login
        
        # Wait for Discord to load
        logger.info("Waiting for Discord chat interface to load...")
        try:
            await page.wait_for_selector('[class*="messages"]', timeout=30000)
            logger.info("Messages container found")
        except:
            logger.warning("Messages container not found, trying alternative selectors")
            await page.wait_for_selector('[data-list-id]', timeout=30000)
            logger.info("Alternative selector found")
        
        # Check current scroll position and total content
        initial_scroll_height = await page.evaluate("document.body.scrollHeight")
        initial_scroll_pos = await page.evaluate("window.scrollY")
        logger.info(f"Initial scrollHeight: {initial_scroll_height}, scrollY: {initial_scroll_pos}")
        
        # Perform very aggressive scrolling with multiple techniques
        for i in range(10):
            logger.info(f"Aggressive scroll iteration {i+1}/10")
            
            # Technique 1: Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            
            # Technique 2: Use Discord-specific scrolling
            scrolled = await page.evaluate("""
                (function() {
                    let scrolled = false;
                    
                    // Try to find Discord's custom scroll containers
                    const selectors = [
                        '[data-list-id*="chat-messages"]',
                        '[class*="scrollerInner"]',
                        '[class*="messagesWrapper"]',
                        '[class*="scroller"]',
                        '[class*="chat"]'
                    ];
                    
                    for (let selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            if (element.scrollHeight > element.clientHeight) {
                                const oldScrollTop = element.scrollTop;
                                element.scrollTop = element.scrollHeight;
                                if (element.scrollTop !== oldScrollTop) {
                                    scrolled = true;
                                }
                            }
                        }
                    }
                    
                    return scrolled;
                })();
            """)
            
            logger.info(f"Discord-specific scroll result: {scrolled}")
            
            # Technique 3: Wait for lazy loading
            await page.wait_for_timeout(3000)
            
            # Check for new content
            new_scroll_height = await page.evaluate("document.body.scrollHeight")
            logger.info(f"ScrollHeight after iteration {i+1}: {new_scroll_height}")
            
            if new_scroll_height > initial_scroll_height:
                logger.info(f"New content loaded! ScrollHeight increased from {initial_scroll_height} to {new_scroll_height}")
                initial_scroll_height = new_scroll_height
        
        # Final scroll to bottom
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(5000)
        
        # Capture page content
        content = await page.content()
        
        # Look for all timestamps in the content
        timestamp_pattern = r'\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+(?:AM|PM)'
        timestamps = re.findall(timestamp_pattern, content, re.IGNORECASE)
        
        logger.info(f"Found {len(timestamps)} timestamps in page content:")
        unique_timestamps = list(set(timestamps))  # Remove duplicates
        unique_timestamps.sort()
        
        for i, ts in enumerate(unique_timestamps[-20:], 1):  # Show last 20 (newest)
            logger.info(f"  {i}: {ts}")
        
        # Look for ticker patterns
        ticker_pattern = r'\[([A-Z]+)\].*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM))'
        tickers = re.findall(ticker_pattern, content, re.IGNORECASE | re.DOTALL)
        
        logger.info(f"Found {len(tickers)} ticker patterns in page content:")
        unique_tickers = list(set(tickers))  # Remove duplicates
        unique_tickers.sort(key=lambda x: x[1])  # Sort by timestamp
        
        for i, (ticker_type, timestamp) in enumerate(unique_tickers[-20:], 1):  # Show last 20 (newest)
            logger.info(f"  {i}: [{ticker_type}] at {timestamp}")
        
        # Check if we have the target timestamps from 11/5
        target_timestamps = [
            "11/5/2025 10:00:00 AM",  # NQ from source
            "11/5/2025 12:26:00 PM", # ES from source
            "11/5/2025 12:36:00 PM"  # YM from source
        ]
        
        logger.info("Checking for target timestamps from 11/5:")
        for target in target_timestamps:
            found = any(target in ts for ts in unique_timestamps)
            logger.info(f"  {target}: {'FOUND' if found else 'NOT FOUND'}")
        
        logger.info("Deep debug session complete.")
        
    except Exception as e:
        logger.error(f"Error in deep debug session: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(deep_discord_debug())