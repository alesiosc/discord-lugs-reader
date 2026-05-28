#!/usr/bin/env python3
"""
Test script for Discord login module
Tests various login scenarios and session management
"""
import os
import sys
from pathlib import Path
from discord_login import DiscordLoginManager

def test_login_scenarios():
    """Test different login scenarios"""
    print("=== Discord Login Module Tests ===")
    
    # Create login manager
    login_manager = DiscordLoginManager()
    
    print("\nTest 1: Check existing session validity")
    if login_manager.is_session_valid():
        print("✅ Existing session is valid")
    else:
        print("❌ No valid existing session found")
    
    print("\nTest 2: Attempt login (headless)")
    result = login_manager.login(headless=True)
    print(f"Result: {result}")
    
    if result["status"] == "success":
        print("✅ Login successful!")
        print(f"Browser data location: {login_manager.get_browser_data_path()}")
        
        # Test copying to a mock target
        mock_target = Path(__file__).parent / "test_browser_data_copy"
        if login_manager.copy_session_to_main_project(mock_target):
            print(f"✅ Successfully copied session to: {mock_target}")
            # Clean up test copy
            import shutil
            if mock_target.exists():
                shutil.rmtree(mock_target)
                print("🧹 Cleaned up test copy")
        else:
            print("❌ Failed to copy session")
            
    else:
        print("❌ Login failed")
        if result.get("reason"):
            print(f"Reason: {result['reason']}")
            
    print("\nTest 3: Browser data directory status")
    browser_data_path = Path(login_manager.get_browser_data_path())
    if browser_data_path.exists():
        file_count = len(list(browser_data_path.rglob("*")))
        print(f"✅ Browser data exists with {file_count} files")
    else:
        print("❌ No browser data directory found")

def test_manual_login():
    """Test login with browser window visible for manual intervention"""
    print("\n=== Manual Login Test ===")
    print("This will open a browser window for manual testing...")
    
    login_manager = DiscordLoginManager()
    result = login_manager.login(headless=False, force_relogin=True)
    
    print(f"\nManual Login Result: {result}")

def main():
    """Run all tests"""
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        test_manual_login()
    else:
        test_login_scenarios()

if __name__ == "__main__":
    main()