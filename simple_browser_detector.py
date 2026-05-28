import asyncio
import os
import sys
from datetime import datetime
from playwright.async_api import async_playwright
from paddleocr import PaddleOCR
from dotenv import load_dotenv
import logging
from pathlib import Path
import re
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def take_screenshot_and_extract_data():
    """Simple function to take screenshot and extract latest ticker data"""
    discord_url = os.getenv('DISCORD_CHANNEL_URL')
    if not discord_url:
        logger.error("DISCORD_CHANNEL_URL not set in .env")
        return
    
    playwright = await async_playwright().start()
    
    try:
        # Launch browser in non-headless mode for debugging
        logger.info("Launching browser...")
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # Navigate to Discord
        logger.info(f"Navigating to: {discord_url}")
        await page.goto(discord_url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(5000)
        
        # Check if login is required
        current_url = page.url
        if 'login' in current_url.lower() or 'auth' in current_url.lower():
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
        try:
            await page.wait_for_selector('[data-list-id*="chat-messages"]', timeout=30000)
            logger.info("Discord chat messages container loaded")
        except:
            logger.info("Using alternative selector for messages")
            await page.wait_for_selector('[class*="messages"]', timeout=30000)
        
        # Aggressive scroll to bottom to ensure latest messages are loaded
        logger.info("Scrolling to bottom to load latest messages...")
        for i in range(15):  # Many attempts to ensure we get to the bottom
            old_height = await page.evaluate("document.body.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)  # Wait for content to load
            
            new_height = await page.evaluate("document.body.scrollHeight")
            logger.info(f"Scroll {i+1}: height {old_height} -> {new_height}")
            
            # Also try Discord-specific scrolling
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
            except:
                pass
            
            if new_height == old_height:
                logger.info("Scroll height stable")
                # Additional wait to ensure messages are rendered
                await page.wait_for_timeout(3000)
                break
        
        # Take screenshot
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%fZ')
        screenshot_path = f".playwright-mcp/page-{timestamp}.png"
        logger.info(f"Taking screenshot: {screenshot_path}")
        await page.screenshot(path=screenshot_path, full_page=True)
        
        # Extract ticker data using OCR
        logger.info("Extracting ticker data using OCR...")
        ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        result = ocr.ocr(screenshot_path)
        
        # Extract text from OCR results
        text_parts = []
        if result and isinstance(result, list):
            for item in result:
                if item is not None and isinstance(item, list):
                    for subitem in item:
                        if isinstance(subitem, list) and len(subitem) > 1 and isinstance(subitem[1], list) and len(subitem[1]) > 0:
                            text_parts.append(subitem[1][0])  # Extract the text part
        
        # Join all text parts
        text = ' '.join(text_parts)
        logger.info(f"OCR extracted text length: {len(text)} characters")
        
        # Find ticker patterns
        pattern = r'\[([A-Z]+)\].*?Published Level:.*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM))\s*,\s*Mid:\s*([0-9.]+)\s*,\s*Lower:\s*([0-9.]+)\s*,\s*Upper:\s*([0-9.]+)'
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        logger.info(f"Found {len(matches)} ticker matches")
        
        if not matches:
            # Try alternative pattern
            alt_pattern = r'\[([A-Z]+)\].*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)).*?Mid:\s*([0-9.]+).*?Lower:\s*([0-9.]+).*?Upper:\s*([0-9.]+)'
            matches = re.findall(alt_pattern, text, re.IGNORECASE | re.DOTALL)
            logger.info(f"Found {len(matches)} ticker matches with alternative pattern")
        
        ticker_data = []
        for match in matches:
            if len(match) == 5:  # Full pattern match
                ticker_type, timestamp, mid, lower, upper = match
            else:  # Alternative pattern match
                ticker_type, timestamp, mid, lower, upper = match[0], match[1], match[2], match[3], match[4]
            
            logger.info(f"Found ticker: {ticker_type} at {timestamp}")
            ticker_data.append({
                'type': ticker_type.upper(),
                'timestamp': timestamp,
                'mid': float(mid),
                'lower': float(lower),
                'upper': float(upper)
            })
        
        # Get the latest for each type
        latest_by_type = {}
        for item in ticker_data:
            ticker_type = item['type']
            if ticker_type in ['NQ', 'ES', 'YM', 'RTY', 'CL']:
                # Parse timestamp for comparison
                try:
                    item_timestamp = datetime.strptime(item['timestamp'], '%m/%d/%Y %I:%M:%S %p')
                    
                    # If this is the first message of this type, or if it's newer than the current latest
                    if ticker_type not in latest_by_type or item_timestamp > latest_by_type[ticker_type]['parsed_timestamp']:
                        item['parsed_timestamp'] = item_timestamp  # Store parsed timestamp for comparison
                        latest_by_type[ticker_type] = item
                        logger.info(f"Selected latest {ticker_type}: {item['timestamp']}")
                except Exception as e:
                    logger.error(f"Error parsing timestamp for {ticker_type}: {e}")
        
        # Remove the parsed_timestamp from the returned data
        for item in latest_by_type.values():
            if 'parsed_timestamp' in item:
                del item['parsed_timestamp']
        
        # Save to snapshot.txt
        if latest_by_type:
            logger.info(f"Saving {len(latest_by_type)} ticker messages to snapshot:")
            for item in latest_by_type.values():
                logger.info(f"  - {item['type']}: {item['timestamp']}")
            
            snapshot_content = "### Page state\n"
            snapshot_content += "- Page URL: https://discord.com/channels/1069289461667598376/1399516015070548091\n"
            snapshot_content += "- Page Title: Discord | #lugs | PWTrades\n"
            snapshot_content += "- Page Snapshot:\n"
            
            for i, item in enumerate(latest_by_type.values()):
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
                snapshot_content += f"      - generic [ref=e{i}]: \"[{item['type']}] Published Level: Lug Timestamp: {item['timestamp']}, Mid: {item['mid']}, Lower: {item['lower']}, Upper: {item['upper']}\"\n\n"
            
            with open("snapshot.txt", "w", encoding="utf-8") as f:
                f.write(snapshot_content)
            
            logger.info(f"Snapshot saved with {len(latest_by_type)} ticker messages")
        else:
            logger.info("No ticker data found to save")
        
        return list(latest_by_type.values())
        
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()

async def main():
    """Main function"""
    logger.info("Starting simple browser detector...")
    ticker_data = await take_screenshot_and_extract_data()
    logger.info("Simple browser detector completed")
    
    if ticker_data:
        logger.info(f"Found {len(ticker_data)} ticker messages:")
        for item in ticker_data:
            logger.info(f"  [{item['type']}] at {item['timestamp']}")
    else:
        logger.info("No ticker messages found")

if __name__ == "__main__":
    asyncio.run(main())
