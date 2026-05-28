#!/usr/bin/env python3
"""
Setup script for Discord Login Module
Installs dependencies and prepares environment
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command with error handling"""
    print(f"[INFO] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed:")
        print(f"  Command: {command}")
        print(f"  Error: {e.stderr}")
        return False

def setup_login_module():
    """Set up the login module environment"""
    print("=== Discord Login Module Setup ===")
    
    # Change to login module directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Create virtual environment if it doesn't exist
    venv_dir = script_dir / "venv"
    if not venv_dir.exists():
        print("[INFO] Creating virtual environment...")
        if not run_command(f"python -m venv {venv_dir}", "Virtual environment creation"):
            return False
    else:
        print("[INFO] Virtual environment already exists")
    
    # Determine pip executable path
    if os.name == 'nt':  # Windows
        pip_exe = venv_dir / "Scripts" / "pip.exe"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        pip_exe = venv_dir / "bin" / "pip"
        python_exe = venv_dir / "bin" / "python"
    
    # Install requirements
    if not run_command(f'"{pip_exe}" install -r requirements.txt', "Installing requirements"):
        return False
    
    # Install Playwright browsers
    if not run_command(f'"{python_exe}" -m playwright install chromium', "Installing Playwright browsers"):
        return False
    
    # Create .env file if it doesn't exist
    env_file = script_dir / ".env"
    env_template = script_dir / ".env.template"
    
    if not env_file.exists() and env_template.exists():
        import shutil
        shutil.copy(env_template, env_file)
        print(f"[INFO] Created .env file from template")
        print(f"[ACTION REQUIRED] Edit {env_file} with your Discord credentials")
    else:
        print("[INFO] .env file already exists")
    
    print("\n=== Setup Complete ===")
    print(f"✅ Virtual environment: {venv_dir}")
    print(f"✅ Dependencies installed")
    print(f"✅ Playwright browsers installed")
    print(f"✅ Configuration file: {env_file}")
    
    print("\n=== Next Steps ===")
    print(f"1. Edit {env_file} with your Discord credentials")
    print(f"2. Run: {python_exe} test_login.py")
    print(f"3. Or run: {python_exe} discord_login.py")
    
    return True

if __name__ == "__main__":
    success = setup_login_module()
    if not success:
        print("\n❌ Setup failed! Check the errors above.")
        sys.exit(1)
    else:
        print("\n🎉 Setup completed successfully!")