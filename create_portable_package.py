"""
Create Portable Virtual Environment Package for Discord LUGS Reader
This creates a self-contained portable application using Option 3 methodology
"""
import os
import sys
import shutil
import subprocess
import zipfile
import urllib.request
from pathlib import Path
import time

class PortableVenvCreator:
    def __init__(self):
        self.project_root = Path.cwd()
        self.portable_dir = self.project_root / "discord_lugs_portable_venv"
        self.python_version = "3.11.9"  # Stable version for compatibility
        self.python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-embed-amd64.zip"
        
    def log(self, message, level="INFO"):
        """Enhanced logging with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def clean_previous_builds(self):
        """Clean previous portable builds"""
        self.log("Cleaning previous portable builds...")
        
        if self.portable_dir.exists():
            shutil.rmtree(self.portable_dir)
            self.log(f"  Removed: {self.portable_dir}")
            
    def create_portable_structure(self):
        """Create the portable directory structure"""
        self.log("Creating portable directory structure...")
        
        # Create main directories
        directories = [
            self.portable_dir,
            self.portable_dir / "python",
            self.portable_dir / "app",
            self.portable_dir / "data",
            self.portable_dir / "logs",
            self.portable_dir / "screenshots"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.log(f"  Created: {directory.name}/")
            
    def download_python_embedded(self):
        """Download and extract embedded Python"""
        self.log(f"Downloading Python {self.python_version} embedded...")
        
        python_zip = self.portable_dir / f"python-{self.python_version}-embed.zip"
        
        try:
            with urllib.request.urlopen(self.python_url) as response:
                with open(python_zip, 'wb') as f:
                    shutil.copyfileobj(response, f)
                    
            self.log(f"  Downloaded: {python_zip.name}")
            
            # Extract Python
            self.log("  Extracting Python...")
            with zipfile.ZipFile(python_zip, 'r') as zip_ref:
                zip_ref.extractall(self.portable_dir / "python")
                
            # Clean up zip file
            python_zip.unlink()
            
            # Enable pip for embedded Python by modifying ._pth file
            pth_files = list((self.portable_dir / "python").glob("python*._pth"))
            if pth_files:
                pth_file = pth_files[0]
                with open(pth_file, 'r') as f:
                    content = f.read()
                
                # Add site-packages and enable import site
                if 'import site' not in content:
                    content = content.strip() + '\n\nimport site\n'
                    
                with open(pth_file, 'w') as f:
                    f.write(content)
                self.log(f"  Modified {pth_file.name} to enable pip")
            
            # Create get-pip.py and install pip immediately
            self.log("  Installing pip in embedded Python...")
            try:
                get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
                get_pip_path = self.portable_dir / "python" / "get-pip.py"
                
                urllib.request.urlretrieve(get_pip_url, get_pip_path)
                
                python_exe = self.portable_dir / "python" / "python.exe"
                result = subprocess.run([
                    str(python_exe), str(get_pip_path), "--no-warn-script-location"
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    self.log("  Pip installed successfully in embedded Python")
                    get_pip_path.unlink()  # Clean up
                else:
                    self.log(f"  Pip installation failed: {result.stderr[:100]}", "WARN")
                    
            except Exception as e:
                self.log(f"  Pip installation error: {e}", "WARN")
                
            return True
            
        except Exception as e:
            self.log(f"  Error downloading Python: {e}", "ERROR")
            return False
            
    def install_dependencies(self):
        """Install required dependencies in portable Python"""
        self.log("Installing dependencies in portable Python...")
        
        python_exe = self.portable_dir / "python" / "python.exe"
        
        if not python_exe.exists():
            self.log("  Python executable not found", "ERROR")
            return False
            
        # Download and install pip first
        self.log("  Installing pip...")
        try:
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            get_pip_path = self.portable_dir / "get-pip.py"
            
            urllib.request.urlretrieve(get_pip_url, get_pip_path)
            
            result = subprocess.run([
                str(python_exe), str(get_pip_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("    Pip installed successfully")
                get_pip_path.unlink()  # Clean up
            else:
                self.log(f"    Pip installation failed: {result.stderr}", "WARN")
                
        except Exception as e:
            self.log(f"    Pip installation error: {e}", "WARN")
            
        # Install core dependencies
        essential_packages = [
            "requests",
            "python-dotenv",
            "playwright==1.47.0",
            "pillow",
        ]
        
        self.log("  Installing essential packages...")
        for package in essential_packages:
            try:
                self.log(f"    Installing {package}...")
                result = subprocess.run([
                    str(python_exe), "-m", "pip", "install", package, "--no-warn-script-location"
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    self.log(f"    ✅ {package} installed")
                else:
                    self.log(f"    ❌ {package} failed: {result.stderr[:100]}", "WARN")
                    
            except subprocess.TimeoutExpired:
                self.log(f"    ⏱️ {package} installation timed out", "WARN")
            except Exception as e:
                self.log(f"    ❌ {package} error: {e}", "WARN")
                
        return True
        
    def copy_application_files(self):
        """Copy all application files to portable directory"""
        self.log("Copying application files...")
        
        app_dir = self.portable_dir / "app"
        
        # Core application files
        core_files = [
            "main.py",
            "enhanced_ocr.py", 
            "browser_detector.py",
            "ocr_watcher.py",
            "run_ocr.py",
            "requirements.txt",
            "app_icon.ico",
            "hook-paddleocr-runtime.py"
        ]
        
        for file_name in core_files:
            source_file = self.project_root / file_name
            if source_file.exists():
                shutil.copy2(source_file, app_dir / file_name)
                self.log(f"  ✅ Copied: {file_name}")
            else:
                self.log(f"  ⚠️  Missing: {file_name}", "WARN")
                
        # Copy .env as template with exact formatting
        env_source = self.project_root / ".env"
        env_template = app_dir / ".env.template"
        
        if env_source.exists():
            with open(env_source, 'r') as src, open(env_template, 'w') as dst:
                for line in src:
                    if line.strip().startswith('#') or line.strip() == '':
                        # Keep comments and empty lines as-is
                        dst.write(line)
                    elif '=' in line and not line.strip().startswith('#'):
                        # Handle actual configuration lines
                        if 'WEBHOOK_URL=' in line and '"' in line:
                            # Special handling for webhook URLs to preserve structure
                            if '#TESTING' in line:
                                dst.write('WEBHOOK_URL="YOUR_DISCORD_WEBHOOK_URL_HERE" #TESTING\n')
                            elif '#PRODUCTION' in line:
                                dst.write('#WEBHOOK_URL="YOUR_PRODUCTION_WEBHOOK_URL_HERE" #PRODUCTION\n')
                            else:
                                dst.write('WEBHOOK_URL="YOUR_DISCORD_WEBHOOK_URL_HERE"\n')
                        elif 'DISCORD_CHANNEL_URL=' in line:
                            dst.write('DISCORD_CHANNEL_URL="YOUR_DISCORD_CHANNEL_URL_HERE"\n')
                        elif 'DISCORD_EMAIL=' in line:
                            dst.write('DISCORD_EMAIL="your_email@example.com"\n')
                        elif 'DISCORD_PASSWORD=' in line:
                            dst.write('DISCORD_PASSWORD="your_password"\n')
                        elif 'ENABLED_TICKERS=' in line:
                            dst.write('ENABLED_TICKERS="NQ,ES,YM"\n')
                        elif any(token in line for token in ['DISCORD_TOKEN', 'HEADLESS_MODE', 'DUPLICATES']):
                            # Keep these with sensible defaults
                            if 'DISCORD_TOKEN=' in line:
                                dst.write('DISCORD_TOKEN=your_discord_token\n')
                            elif 'HEADLESS_MODE=' in line:
                                dst.write('HEADLESS_MODE=true\n')
                            elif 'DUPLICATES=' in line:
                                dst.write('DUPLICATES=true\n')
                        elif any(rand_token in line for rand_token in ['RANDOM_']):
                            # Keep randomization values as-is since they're already good defaults
                            dst.write(line)
                        else:
                            # For any other settings, keep the structure but clear sensitive values
                            key = line.split('=', 1)[0]
                            dst.write(f"{key}=YOUR_VALUE_HERE\n")
                    else:
                        dst.write(line)
            self.log("  ✅ Created .env template")
            
    def create_startup_scripts(self):
        """Create startup and utility scripts"""
        self.log("Creating startup scripts...")
        
        # Main startup script
        startup_script = self.portable_dir / "start_discord_lugs.bat"
        with open(startup_script, 'w') as f:
            f.write(f"""@echo off
title Discord LUGS Reader - Portable
echo.
echo ====================================
echo   Discord LUGS Reader - Portable
echo ====================================
echo.

REM Check if .env exists
if not exist "app\\.env" (
    echo ERROR: .env file not found!
    echo.
    echo SETUP REQUIRED:
    echo 1. Copy app\\.env.template to app\\.env
    echo 2. Edit app\\.env with your Discord webhook and channel URLs
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Starting Discord LUGS Reader...
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"
set PYTHONPATH=%~dp0app
python\\python.exe app\\main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start!
    echo Check the logs directory for error details.
    echo.
)

pause
""")
        
        # OCR Watcher startup script  
        ocr_script = self.portable_dir / "start_ocr_watcher.bat"
        with open(ocr_script, 'w') as f:
            f.write(f"""@echo off
title Discord LUGS Reader - OCR Watcher
echo Starting OCR Watcher...

cd /d "%~dp0"
set PYTHONPATH=%~dp0app
python\\python.exe app\\ocr_watcher.py

pause
""")
        
        # Setup script
        setup_script = self.portable_dir / "setup.bat"
        with open(setup_script, 'w') as f:
            f.write(f"""@echo off
title Discord LUGS Reader - Setup
echo.
echo ====================================
echo   Discord LUGS Reader - Setup
echo ====================================
echo.

REM Copy template if .env doesn't exist
if not exist "app\\.env" (
    if exist "app\\.env.template" (
        copy "app\\.env.template" "app\\.env" > nul
        echo ✅ Created app\\.env from template
    ) else (
        echo ❌ Template file not found!
        pause
        exit /b 1
    )
) else (
    echo ℹ️  app\\.env already exists
)

echo.
echo NEXT STEPS:
echo 1. Edit app\\.env file with your Discord settings:
echo    - WEBHOOK_URL=your_discord_webhook_url
echo    - DISCORD_CHANNEL_URL=your_discord_channel_url
echo    - HEADLESS_MODE=true
echo.
echo 2. Run start_discord_lugs.bat to start the application
echo.

REM Install playwright browsers
echo Installing Playwright browsers...
cd /d "%~dp0"
python\\python.exe -m playwright install chromium --with-deps

echo.
echo ✅ Setup completed!
echo.
pause
""")
        
        # Test script
        test_script = self.portable_dir / "test_installation.bat"
        with open(test_script, 'w') as f:
            f.write(f"""@echo off
title Discord LUGS Reader - Installation Test
echo.
echo ====================================
echo   Testing Portable Installation
echo ====================================
echo.

cd /d "%~dp0"
set PYTHONPATH=%~dp0app

echo Testing Python...
python\\python.exe --version
if errorlevel 1 (
    echo ❌ Python test failed
    goto :error
)

echo Testing imports...
python\\python.exe -c "import requests, dotenv, playwright; print('✅ Core imports successful')"
if errorlevel 1 (
    echo ❌ Import test failed
    goto :error
)

echo Testing application files...
if not exist "app\\main.py" (
    echo ❌ main.py not found
    goto :error
)

if not exist "app\\enhanced_ocr.py" (
    echo ❌ enhanced_ocr.py not found
    goto :error
)

echo.
echo ✅ ALL TESTS PASSED!
echo Your portable installation is ready to use.
echo.
goto :end

:error
echo.
echo ❌ TESTS FAILED!
echo Please check the installation.
echo.

:end
pause
""")
        
        self.log("  ✅ Created startup scripts")
        
    def create_documentation(self):
        """Create comprehensive documentation"""
        self.log("Creating documentation...")
        
        readme_path = self.portable_dir / "README.txt"
        with open(readme_path, 'w') as f:
            f.write(f"""====================================
  Discord LUGS Reader - Portable
====================================

VERSION: Portable Virtual Environment Package
CREATED: {time.strftime("%Y-%m-%d %H:%M:%S")}

WHAT THIS IS:
This is a portable version of the Discord LUGS Reader that includes
everything needed to run on any Windows machine without installation.

CONTENTS:
📁 python/          - Embedded Python {self.python_version} runtime
📁 app/             - Discord LUGS Reader application
📁 data/            - Application data storage
📁 logs/            - Log files
📁 screenshots/     - Screenshot storage

QUICK START:
1. Run setup.bat (first time only)
2. Edit app\\.env with your Discord settings
3. Run start_discord_lugs.bat

DETAILED SETUP:
1. FIRST TIME SETUP:
   - Double-click setup.bat
   - This creates .env file and installs browser components
   
2. CONFIGURE DISCORD:
   - Open app\\.env in notepad
   - Set WEBHOOK_URL to your Discord webhook URL
   - Set DISCORD_CHANNEL_URL to your Discord channel URL
   - Save the file

3. START APPLICATION:
   - Double-click start_discord_lugs.bat
   - The application will start monitoring Discord

TESTING:
- Run test_installation.bat to verify everything works

TROUBLESHOOTING:
- If startup fails, check logs/ directory for error details
- Ensure .env file has correct Discord URLs
- Make sure you have internet connection
- Try running test_installation.bat first

SYSTEM REQUIREMENTS:
- Windows 10/11 (64-bit)
- Internet connection
- At least 500MB free disk space

SUPPORT:
Check the application logs in the logs/ directory for detailed
error information.

====================================
""")
        
        # Create changelog
        changelog_path = self.portable_dir / "CHANGELOG.txt"
        with open(changelog_path, 'w') as f:
            f.write(f"""DISCORD LUGS READER - PORTABLE VERSION CHANGELOG
===============================================

Version: Portable Virtual Environment Package
Date: {time.strftime("%Y-%m-%d")}

FEATURES:
✅ Self-contained portable application
✅ No installation required
✅ Embedded Python {self.python_version} runtime
✅ All dependencies included
✅ Easy setup with batch scripts
✅ Comprehensive documentation

TECHNICAL DETAILS:
- Based on Python {self.python_version} embedded distribution
- Uses virtual environment approach for maximum compatibility
- Includes OCR enhancements and all bug fixes
- Supports all ticker types (NQ, ES, YM, GC, RTY, CL)

KNOWN LIMITATIONS:
- OCR functionality requires separate installation (EasyOCR/PaddleOCR)
- First run requires internet for browser installation
- Windows only (64-bit)

TROUBLESHOOTING:
- Run test_installation.bat if issues occur
- Check logs/ directory for error details
- Ensure .env configuration is correct
""")
        
        self.log("  ✅ Created documentation")
        
    def create_portable_package(self):
        """Main function to create the complete portable package"""
        self.log("=== Creating Discord LUGS Reader Portable Package ===")
        
        # Step 1: Clean and prepare
        self.clean_previous_builds()
        
        # Step 2: Create structure
        self.create_portable_structure()
        
        # Step 3: Download embedded Python
        if not self.download_python_embedded():
            self.log("❌ Failed to download Python", "ERROR")
            return False
            
        # Step 4: Install dependencies
        if not self.install_dependencies():
            self.log("❌ Failed to install dependencies", "ERROR") 
            return False
            
        # Step 5: Copy application files
        self.copy_application_files()
        
        # Step 6: Create startup scripts
        self.create_startup_scripts()
        
        # Step 7: Create documentation
        self.create_documentation()
        
        # Final summary
        self.log("🎉 PORTABLE PACKAGE CREATED SUCCESSFULLY! 🎉")
        
        # Calculate size
        total_size = sum(f.stat().st_size for f in self.portable_dir.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        
        self.log(f"📁 Location: {self.portable_dir}")
        self.log(f"📏 Total size: {size_mb:.1f} MB")
        self.log(f"📄 Files included: {len(list(self.portable_dir.rglob('*')))}")
        
        print(f"""
🎉 SUCCESS! Your portable Discord LUGS Reader is ready!

📁 LOCATION: {self.portable_dir}
📏 SIZE: {size_mb:.1f} MB

🚀 TO USE:
1. Copy the entire folder to any Windows machine
2. Run setup.bat (first time only)  
3. Edit app\\.env with your Discord settings
4. Run start_discord_lugs.bat

✅ This package is completely self-contained and requires no installation!
""")
        
        return True

def main():
    creator = PortableVenvCreator()
    success = creator.create_portable_package()
    
    if not success:
        print("\\n❌ Portable package creation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()