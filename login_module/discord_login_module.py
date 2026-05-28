#!/usr/bin/env python3
"""
Test Discord Channel Access
Verifies we can navigate to the specific Discord channel after login
"""

import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

def test_channel_access():
    """Test accessing the Discord channel directly"""
    
    # Load environment variables
    load_dotenv()
    
    discord_channel_url = os.getenv('DISCORD_CHANNEL_URL')
    
    print("=== Discord Channel Access Test ===")
    print(f"Target Channel: {discord_channel_url}")
    
    with sync_playwright() as p:
        print("[INFO] Creating browser context...")
        
        # Launch browser with visible window
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        
        try:
            print("[INFO] Starting with Discord login page...")
            page.goto("https://discord.com/login", timeout=30000)
            
            # Wait for login page to load
            time.sleep(2)
            print(f"[INFO] Current URL after login page: {page.url}")
            
            # If we're already logged in, we'll be redirected
            if "discord.com/app" in page.url or "discord.com/channels" in page.url:
                print("[INFO] Already logged in!")
                print(f"[INFO] Target channel URL: {discord_channel_url}")
                print("[INFO] You can now manually navigate to the channel...")
                
            else:
                # Handle actual login process
                print("[INFO] Login page detected, performing automated login...")
                
                # Load login credentials
                email = os.getenv('DISCORD_EMAIL')
                password = os.getenv('DISCORD_PASSWORD')
                
                if email and password:
                    try:
                        # Wait for login form
                        print("[INFO] Waiting for login form...")
                        page.wait_for_selector('input[name="email"]', timeout=10000)
                        
                        # Fill in email
                        print("[INFO] Filling email field...")
                        page.fill('input[name="email"]', email)
                        time.sleep(1)
                        
                        # Fill in password
                        print("[INFO] Filling password field...")
                        page.fill('input[name="password"]', password)
                        time.sleep(1)
                        
                        # Click login button
                        print("[INFO] Clicking login button...")
                        page.click('button[type="submit"]')
                        
                        # Wait for login to complete
                        print("[INFO] Waiting for login to complete...")
                        page.wait_for_url("**/app**", timeout=30000)
                        print("[INFO] Login successful!")
                        
                        # NOW navigate directly to the channel 
                        time.sleep(2)  # Give Discord time to fully load
                        print(f"[INFO] Navigating directly to channel: {discord_channel_url}")
                        page.goto(discord_channel_url, timeout=30000)
                        time.sleep(3)  # Wait for channel to load
                        print(f"[INFO] Direct navigation completed! Current URL: {page.url}")
                        
                    except Exception as e:
                        print(f"[ERROR] Automated login failed: {e}")
                        print("[INFO] Please complete login manually...")
                        time.sleep(15)  # Give time for manual login
                else:
                    print("[INFO] No credentials found, please complete login manually...")
                    time.sleep(15)  # Give time for manual login
            
            current_url = page.url
            page_title = page.title()
            
            print(f"[INFO] Current URL: {current_url}")
            print(f"[INFO] Page Title: {page_title}")
            
            # Check if we're in the channel
            if "channels" in current_url:
                print("✅ Successfully navigated to Discord channel!")
                
                # Try to find channel content
                try:
                    # Look for common Discord channel elements
                    messages_area = page.locator('[data-list-id="chat-messages"]')
                    if messages_area.count() > 0:
                        print("✅ Channel messages area found!")
                    
                    channel_name = page.locator('[class*="title"]').first
                    if channel_name.count() > 0:
                        print(f"✅ Channel detected: {channel_name.inner_text()}")
                        
                except Exception as e:
                    print(f"[WARN] Could not detect channel elements: {e}")
                
                # Keep browser open for manual inspection
                print("\n🔍 Browser window is open for manual inspection...")
                print("You can now see the Discord channel in the browser!")
                print("Press Enter to close browser...")
                input()
                
            else:
                print(f"❌ Not in expected channel. Current URL: {current_url}")
                
        except Exception as e:
            print(f"[ERROR] Failed to navigate to channel: {e}")
            print("\n🔍 Browser window is open for debugging...")
            print("Press Enter to close browser...")
            input()
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_channel_access()