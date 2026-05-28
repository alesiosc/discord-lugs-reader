# Discord Login Module

Standalone authentication system for Discord login with session persistence.

## 🎯 Purpose

This module handles Discord authentication independently from the main project, allowing for:
- Username/password login
- "Continue with browser" scenarios  
- Session persistence and reuse
- Browser data management for integration

## 🚀 Quick Start

### 1. Setup
```bash
python setup.py
```

### 2. Configure
Edit `.env` file with your Discord credentials:
```env
DISCORD_EMAIL="your_email@example.com"
DISCORD_PASSWORD="your_password"
DISCORD_CHANNEL_URL="https://discord.com/channels/YOUR_SERVER_ID/YOUR_CHANNEL_ID"
```

### 3. Test Login
```bash
# Automated test (headless)
venv/Scripts/python test_login.py

# Manual test (with browser window)
venv/Scripts/python test_login.py --manual

# Direct login
venv/Scripts/python discord_login.py
```

## 📋 Features

### ✅ Login Scenarios Handled
- **Already logged in**: Detects existing session
- **Continue with browser**: Handles Discord's browser continuation
- **Username/password**: Full login form automation
- **Session validation**: Checks if existing sessions are still valid

### ✅ Session Management
- **Persistent browser data**: Saves login state between runs
- **24-hour session validity**: Automatically detects expired sessions
- **Force relogin option**: Override existing sessions when needed

### ✅ Integration Ready
- **Browser data export**: Copy session to main project
- **Configuration management**: JSON-based state tracking
- **Error handling**: Comprehensive logging and error reporting

## 📁 Files

- `discord_login.py` - Main login module class
- `test_login.py` - Test suite and validation
- `setup.py` - Environment setup and dependency installation
- `.env.template` - Configuration template
- `requirements.txt` - Python dependencies
- `login_config.json` - Session state (auto-generated)
- `browser_data_login/` - Browser session storage (auto-generated)

## 🔧 Integration with Main Project

### Method 1: Copy Browser Data
```python
from login_module.discord_login import DiscordLoginManager

# Perform login
login_manager = DiscordLoginManager()
result = login_manager.login()

if result["status"] == "success":
    # Copy session to main project
    login_manager.copy_session_to_main_project("../browser_data_stable")
```

### Method 2: Direct Path Usage
```python
# Get the browser data path for direct use
browser_data_path = login_manager.get_browser_data_path()
# Use this path in your Playwright browser context
```

## 🧪 Testing

### Automated Testing
```bash
venv/Scripts/python test_login.py
```
Tests:
- Existing session validation
- Headless login process
- Browser data copying
- File system checks

### Manual Testing  
```bash
venv/Scripts/python test_login.py --manual
```
- Opens browser window for manual inspection
- Allows manual intervention for 2FA or other issues
- Visual verification of login process

## 📊 Return Values

### Successful Login
```json
{
  "status": "success",
  "method": "login_success|continued_in_browser|already_logged_in",
  "browser_data_dir": "/path/to/browser_data_login",
  "channel_access": true
}
```

### Failed Login
```json
{
  "status": "failed",
  "reason": "missing_credentials|requires_2fa|login_error|etc"
}
```

## ⚠️ Known Limitations

- **2FA Support**: Requires manual intervention for two-factor authentication
- **Rate Limiting**: Discord may impose login rate limits
- **Browser Dependencies**: Requires Chromium browser installation

## 🔒 Security

- **Credential Storage**: Uses environment variables only
- **Session Isolation**: Separate browser data directory
- **No Credential Logging**: Passwords never appear in logs

## 🛠️ Troubleshooting

### Common Issues

**"Missing credentials"**
- Check `.env` file configuration
- Verify DISCORD_EMAIL and DISCORD_PASSWORD are set

**"Channel access failed"**  
- Verify DISCORD_CHANNEL_URL is correct
- Check if account has access to the specific channel
- Try manual login to verify credentials

**"Session expired"**
- Run with `force_relogin=True`
- Delete `browser_data_login/` folder for fresh start

### Debug Mode
Run with browser window visible for debugging:
```python
result = login_manager.login(headless=False)
```

## 📈 Future Integration

This module is designed to be integrated into the main project once tested and working. The integration points are:

1. **Environment Configuration**: Same .env structure as main project
2. **Browser Data Sharing**: Compatible browser data format
3. **Logging Interface**: Same logging patterns as main project
4. **Error Handling**: Consistent error reporting

The module can be moved into the main project as a submodule or its functionality can be merged into existing authentication systems.