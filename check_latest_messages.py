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

async def check_latest_messages_with_auth():
    """Check latest messages with proper authentication handling"""
    load_dotenv(".env", override=True)
    discord_url = os.getenv('DISCORD_CHANNEL_URL')
    
    playwright = await async_playwright().start()
    
    try:
        # Launch browser in non-headless mode for sign-in
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to Discord
        logger.info(f"Navigating to: {discord_url}")
        await page.goto(discord_url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait for potential authentication
        current_url = page.url
        if 'login' in current_url or 'auth' in current_url:
            logger.info("Login required. Please sign in manually in the browser window.")
            logger.info("Waiting 120 seconds for manual sign-in...")
            for i in range(120):
                await page.wait_for_timeout(1000)
                # Check if we've moved past login
                new_url = page.url
                if 'login' not in new_url and 'auth' not in new_url:
                    logger.info("Login appears to be complete")
                    break
                if i % 10 == 0:  # Log every 10 seconds
                    logger.info(f"Waiting for sign-in... {120-i} seconds remaining")
        else:
            logger.info("Already authenticated or no login required")
        
        # Wait for Discord interface to load
        logger.info("Waiting for Discord chat interface to load...")
        await page.wait_for_timeout(5000)
        
        # Aggressive scroll to bottom to ensure latest messages are loaded
        logger.info("Scrolling to load latest messages...")
        for i in range(10):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            logger.info(f"Scroll pass {i+1}/10 completed")
            
            # Check if we're getting new content
            doc_height = await page.evaluate("document.body.scrollHeight")
            logger.info(f"Document height: {doc_height}")
        
        # Additional Discord-specific scrolling
        try:
            await page.evaluate("""
                (function() {
                    const selectors = [
                        '[data-list-id*="chat-messages"]',
                        '[class*="scrollerInner"]',
                        '[class*="messagesWrapper"]'
                    ];
                    
                    for (let selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            element.scrollTop = element.scrollHeight;
                        }
                    }
                })();
            """)
            logger.info("Discord-specific scrolling completed")
        except:
            logger.info("Discord-specific scrolling not needed or failed")
        
        # Wait for messages to render
        await page.wait_for_timeout(5000)
        
        # Take a screenshot for visual verification
        await page.screenshot(path="latest_messages_check.png", full_page=True)
        logger.info("Screenshot saved as latest_messages_check.png")
        
        # Get page content
        logger.info("Extracting page content...")
        content = await page.content()
        
        # Find all ticker messages with more flexible pattern
        ticker_pattern = r'\[([A-Z]+)\].*?[Pp]ublished.*?[Ll]evel.*?[Tt]imestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM))'
        tickers = re.findall(ticker_pattern, content, re.IGNORECASE | re.DOTALL)
        
        logger.info(f"Found {len(tickers)} potential ticker messages:")
        
        if tickers:
            # Group by date for easier analysis
            messages_by_date = {}
            for ticker_type, timestamp in tickers:
                date_part = timestamp.split()[0]  # Get the date part (e.g., "11/4/2025")
                if date_part not in messages_by_date:
                    messages_by_date[date_part] = []
                messages_by_date[date_part].append((ticker_type, timestamp))
            
            # Show messages by date, newest first
            for date in sorted(messages_by_date.keys(), reverse=True)[:5]:  # Show top 5 dates
                logger.info(f"Date {date}: {len(messages_by_date[date])} messages")
                for ticker_type, timestamp in messages_by_date[date][:10]:  # Show first 10 of each date
                    logger.info(f"  [{ticker_type}] at {timestamp}")
            
            # Check specifically for the target 11/5 messages
            target_messages = [
                ("NQ", "11/5/2025 10:00:00 AM"),
                ("ES", "11/5/2025 12:26:00 PM"),
                ("YM", "11/5/2025 12:36:00 PM")
            ]
            
            logger.info("Checking for target 11/5 messages:")
            for ticker_type, target_timestamp in target_messages:
                found = any(ts == target_timestamp and tt.upper() == ticker_type 
                           for tt, ts in tickers)
                logger.info(f"  [{ticker_type}] at {target_timestamp}: {'FOUND' if found else 'NOT FOUND'}")
        else:
            logger.info("No ticker messages found in the content")
            
            # Let's also check for any timestamp-like patterns to see what content is there
            timestamp_pattern = r'[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)'
            timestamps = re.findall(timestamp_pattern, content, re.IGNORECASE)
            if timestamps:
                logger.info(f"Found {len(timestamps)} timestamps in content:")
                # Show unique timestamps, newest first
                unique_timestamps = list(set(timestamps))
                unique_timestamps.sort(reverse=True)
                for i, ts in enumerate(unique_timestamps[:20]):  # Show 20 newest
                    logger.info(f"  {i+1}: {ts}")
            else:
                logger.info("No timestamps found in content")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(check_latest_messages_with_auth())