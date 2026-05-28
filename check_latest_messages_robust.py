import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import logging
import re

# Enhanced logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_latest_messages_robust():
    """More robust check to see what the latest messages are in Discord"""
    load_dotenv(".env", override=True)
    discord_url = os.getenv('DISCORD_CHANNEL_URL')
    
    playwright = await async_playwright().start()
    
    try:
        # Launch browser with persistent context to maintain login
        user_data_dir = './browser_data_check'
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            permissions=['notifications']
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        logger.info(f"Navigating to: {discord_url}")
        await page.goto(discord_url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(5000)
        
        # Check if we need to sign in
        current_url = page.url
        if 'login' in current_url.lower() or 'auth' in current_url.lower():
            logger.info("Login required - please sign in manually. Waiting 2 minutes...")
            await page.wait_for_timeout(120000)  # Wait 2 minutes for manual sign-in
        
        logger.info("Waiting for Discord to fully load...")
        # Wait for Discord message container to load
        try:
            await page.wait_for_selector('[data-list-id*="chat-messages"]', timeout=30000)
            logger.info("Discord chat messages container loaded")
        except:
            logger.info("Using alternative selector for messages")
            await page.wait_for_selector('[class*="messages"]', timeout=30000)
        
        logger.info("Scrolling to bottom to load latest messages...")
        # Simple but effective scroll to bottom with multiple attempts
        for i in range(10):  # More attempts
            old_height = await page.evaluate("document.body.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            
            new_height = await page.evaluate("document.body.scrollHeight")
            logger.info(f"Scroll {i+1}: height {old_height} -> {new_height}")
            
            if new_height == old_height:
                logger.info("Scroll height stable - likely at bottom")
                break
        
        # Additional wait for messages to render
        await page.wait_for_timeout(5000)
        
        # Get page content
        content = await page.content()
        logger.info(f"Page content length: {len(content)} characters")
        
        # Try different patterns to find ticker messages
        patterns = [
            r'\[([A-Z]+)\].*?Published Level:.*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM))',  # Original
            r'\[([A-Z]+)\].*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)).*?Mid:\s*([0-9.]+)',  # Flexible
            r'\[([A-Z]+)\].*?([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)).*?Published Level',  # Different order
        ]
        
        tickers = []
        for i, pattern in enumerate(patterns):
            found = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            logger.info(f"Pattern {i+1} found {len(found)} matches")
            tickers.extend(found)
            if found:
                break  # If we found matches with this pattern, use them
        
        logger.info(f"Total ticker messages found: {len(tickers)}")
        if tickers:
            # Show all found tickers
            for i, ticker in enumerate(tickers[:20]):  # Limit to first 20 for readability
                if len(ticker) == 2:
                    logger.info(f"  {i+1}: [{ticker[0]}] at {ticker[1]}")
                elif len(ticker) == 3:
                    logger.info(f"  {i+1}: [{ticker[0]}] at {ticker[1]}, Mid: {ticker[2]}")
                else:
                    logger.info(f"  {i+1}: {ticker}")
        else:
            logger.info("No ticker messages found in content")
            # Look for any timestamps to see what dates are available
            timestamp_pattern = r'\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+(?:AM|PM)'
            timestamps = re.findall(timestamp_pattern, content, re.IGNORECASE)
            logger.info(f"Found {len(timestamps)} timestamps in content:")
            for ts in timestamps[:10]:  # Show first 10
                logger.info(f"  {ts}")
        
        # Check specifically for the target 11/5 messages
        target_messages = [
            ("NQ", "11/5/2025 10:00:00 AM"),
            ("ES", "11/5/2025 12:26:00 PM"),
            ("YM", "11/5/2025 12:36:00 PM")
        ]
        
        logger.info("Checking for target 11/5 messages:")
        for ticker_type, target_timestamp in target_messages:
            found = any(ts == target_timestamp and tt == ticker_type 
                       for tt, ts in tickers if len(ticker) >= 2)
            logger.info(f"  [{ticker_type}] at {target_timestamp}: {'FOUND' if found else 'NOT FOUND'}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await context.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(check_latest_messages_robust())