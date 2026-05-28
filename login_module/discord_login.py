"""
Discord Login Module
Standalone authentication system for Discord login with session persistence.
Handles username/password login and "Continue with browser" scenarios.
"""
import os
import sys
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

class DiscordLoginManager:
    def __init__(self, config_file="login_config.json"):
        self.config_file = Path(__file__).parent / config_file
        self.browser_data_dir = Path(__file__).parent / "browser_data_login"
        self.config = self.load_config()
        
        # Load environment variables
        load_dotenv()
        self.discord_email = os.getenv("DISCORD_EMAIL")
        self.discord_password = os.getenv("DISCORD_PASSWORD") 
        self.discord_channel_url = os.getenv("DISCORD_CHANNEL_URL")
        
    def load_config(self):
        """Load login configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "last_login": None,
            "session_valid": False,
            "login_method": "browser",
            "browser_data_exists": False
        }
    
    def save_config(self):
        """Save login configuration"""
        self.config["last_login"] = time.time()
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def log(self, message, level="INFO"):
        """Enhanced logging"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def is_session_valid(self):
        """Check if existing session is still valid"""
        if not self.config.get("session_valid", False):
            return False
            
        last_login = self.config.get("last_login", 0)
        # Consider session valid for 24 hours
        if time.time() - last_login > 86400:
            self.log("Session expired (24+ hours old)")
            return False
            
        # Check if browser data directory exists
        if not self.browser_data_dir.exists():
            self.log("Browser data directory not found")
            return False
            
        return True
        
    def create_browser_context(self, headless=False):
        """Create browser context with persistent data"""
        self.log("Creating browser context...")
        
        # Ensure browser data directory exists
        self.browser_data_dir.mkdir(exist_ok=True)
        
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.browser_data_dir),
            headless=headless,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-first-run',
                '--disable-dev-shm-usage'
            ],
            java_script_enabled=True,  # Ensure JavaScript is enabled
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        
        return playwright, browser
        
    def handle_discord_login_page(self, page):
        """Handle Discord login page with multiple scenarios"""
        self.log("Analyzing Discord login page...")
        
        try:
            # Wait for page to load
            page.wait_for_load_state('networkidle', timeout=10000)
            
            # Check for different login scenarios
            
            # Scenario 1: Already logged in - redirected to channel
            if "channels" in page.url:
                self.log("Already logged in! Redirected to Discord channels")
                return "already_logged_in"
                
            # Scenario 2: "Continue with browser" button
            continue_button = page.locator('button:has-text("Continue in browser")')
            if continue_button.is_visible():
                self.log("Found 'Continue in browser' button, clicking...")
                continue_button.click()
                page.wait_for_load_state('networkidle', timeout=15000)
                
                # Check if redirected to channels after continue
                if "channels" in page.url:
                    self.log("Successfully continued in browser")
                    return "continued_in_browser"
            
            # Scenario 3: Login form present
            email_field = page.locator('input[name="email"], input[type="email"]')
            password_field = page.locator('input[name="password"], input[type="password"]')
            
            if email_field.is_visible() and password_field.is_visible():
                self.log("Login form found, attempting login...")
                return self.perform_login(page, email_field, password_field)
                
            # Scenario 4: Unknown state - get debug info
            self.log(f"Unknown Discord page state. Current URL: {page.url}", "WARN")
            self.log(f"Page title: {page.title()}", "INFO")
            
            # Take screenshot for debugging
            screenshot_path = Path(__file__).parent / "debug_screenshot.png"
            page.screenshot(path=str(screenshot_path))
            self.log(f"Debug screenshot saved: {screenshot_path}", "INFO")
            
            # Log some page content for debugging
            try:
                body_text = page.locator('body').text_content()[:500]  # First 500 chars
                self.log(f"Page content preview: {body_text}", "INFO")
            except:
                pass
                
            return "unknown_state"
            
        except Exception as e:
            self.log(f"Error analyzing login page: {e}", "ERROR")
            return "error"
            
    def perform_login(self, page, email_field, password_field):
        """Perform actual Discord login"""
        if not self.discord_email or not self.discord_password:
            self.log("Discord credentials not found in environment variables", "ERROR")
            return "missing_credentials"
            
        try:
            # Fill login form
            self.log("Filling email field...")
            email_field.fill(self.discord_email)
            
            self.log("Filling password field...")
            password_field.fill(self.discord_password)
            
            # Find and click login button
            login_button = page.locator('button[type="submit"], button:has-text("Log In")')
            if login_button.is_visible():
                self.log("Clicking login button...")
                login_button.click()
                
                # Wait for login to process
                page.wait_for_load_state('networkidle', timeout=15000)
                
                # Check for successful login
                if "channels" in page.url:
                    self.log("Login successful! Redirected to Discord channels")
                    return "login_success"
                    
                # Check for 2FA requirement
                if page.locator('input[placeholder*="6-digit"], input[placeholder*="code"]').is_visible():
                    self.log("2FA code required", "WARN")
                    return "requires_2fa"
                    
                # Check for other errors
                error_msg = page.locator('.error, [class*="error"]').first
                if error_msg.is_visible():
                    error_text = error_msg.text_content()
                    self.log(f"Login error: {error_text}", "ERROR")
                    return "login_error"
                    
            else:
                self.log("Login button not found", "ERROR")
                return "no_login_button"
                
        except Exception as e:
            self.log(f"Error during login: {e}", "ERROR")
            return "login_exception"
            
        return "login_unknown"
        
    def test_channel_access(self, page):
        """Test access to the specific Discord channel"""
        if not self.discord_channel_url:
            self.log("Discord channel URL not set", "ERROR")
            return False
            
        try:
            self.log(f"Testing channel access: {self.discord_channel_url}")
            page.goto(self.discord_channel_url, timeout=15000)
            page.wait_for_load_state('networkidle', timeout=10000)
            
            # Look for chat messages area
            chat_area = page.locator('[data-list-id="chat-messages"]')
            if chat_area.is_visible(timeout=5000):
                self.log("✅ Channel access successful - chat messages visible")
                return True
            else:
                # Try alternative selectors
                alternative_selectors = [
                    '[role="log"]',
                    '[class*="messages"]',
                    '[class*="chat"]'
                ]
                
                for selector in alternative_selectors:
                    if page.locator(selector).is_visible(timeout=2000):
                        self.log(f"✅ Channel access successful - found with selector: {selector}")
                        return True
                        
                self.log("❌ Channel access failed - chat messages not visible", "WARN")
                return False
                
        except Exception as e:
            self.log(f"Error testing channel access: {e}", "ERROR")
            return False
            
    def login(self, headless=False, force_relogin=False):
        """Main login function"""
        self.log("=== Discord Login Manager ===")
        
        # Check if session is still valid (unless forced relogin)
        if not force_relogin and self.is_session_valid():
            self.log("Existing session found, testing channel access...")
            
            # Quick test with existing session
            playwright, browser = self.create_browser_context(headless=True)
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            if self.test_channel_access(page):
                self.log("✅ Existing session is valid and working!")
                browser.close()
                playwright.stop()
                return {"status": "success", "method": "existing_session"}
            else:
                self.log("Existing session invalid, proceeding with fresh login...")
                browser.close()
                playwright.stop()
        
        # Perform fresh login
        self.log("Starting fresh Discord login process...")
        playwright, browser = self.create_browser_context(headless=headless)
        
        try:
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            # Navigate to Discord
            self.log("Navigating to Discord login...")
            page.goto("https://discord.com/login", timeout=30000)  # Increased timeout
            
            # Handle login page
            login_result = self.handle_discord_login_page(page)
            
            if login_result in ["already_logged_in", "continued_in_browser", "login_success"]:
                # Test channel access
                if self.test_channel_access(page):
                    # Save successful session
                    self.config["session_valid"] = True
                    self.config["login_method"] = login_result
                    self.config["browser_data_exists"] = True
                    self.save_config()
                    
                    self.log("✅ Discord login completed successfully!")
                    return {
                        "status": "success", 
                        "method": login_result,
                        "browser_data_dir": str(self.browser_data_dir),
                        "channel_access": True
                    }
                else:
                    self.log("❌ Login succeeded but channel access failed", "ERROR")
                    return {
                        "status": "partial_success",
                        "method": login_result, 
                        "channel_access": False
                    }
            else:
                self.log(f"❌ Login failed: {login_result}", "ERROR")
                return {"status": "failed", "reason": login_result}
                
        except Exception as e:
            self.log(f"❌ Login process failed: {e}", "ERROR")
            return {"status": "error", "error": str(e)}
            
        finally:
            if not headless:
                self.log("Browser will remain open for manual inspection...")
                input("Press Enter to close browser...")
            browser.close()
            playwright.stop()
            
    def get_browser_data_path(self):
        """Get the path to the browser data directory for integration"""
        return str(self.browser_data_dir)
        
    def copy_session_to_main_project(self, target_path):
        """Copy successful login session to main project"""
        target_path = Path(target_path)
        
        if not self.browser_data_dir.exists():
            self.log("No browser data to copy", "ERROR")
            return False
            
        try:
            if target_path.exists():
                import shutil
                shutil.rmtree(target_path)
                
            import shutil  
            shutil.copytree(self.browser_data_dir, target_path)
            self.log(f"✅ Browser data copied to: {target_path}")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to copy browser data: {e}", "ERROR")
            return False


def main():
    """Test the login module"""
    login_manager = DiscordLoginManager()
    
    # Test login
    result = login_manager.login(headless=False)
    
    print(f"\\nLogin Result: {result}")
    
    if result["status"] == "success":
        print(f"Browser data saved to: {login_manager.get_browser_data_path()}")
        print("Login session is ready for integration!")
    else:
        print("Login failed - check the logs above for details")


if __name__ == "__main__":
    main()