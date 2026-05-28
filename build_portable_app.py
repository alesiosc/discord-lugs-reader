"""
Optimized Portable Application Builder for Discord LUGS Reader
Following comprehensive portable application creation methodology from file 12
"""
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

class PortableAppBuilder:
    def __init__(self):
        self.project_root = Path.cwd()
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.portable_dir = self.project_root / "discord_lugs_portable"
        
    def log(self, message, level="INFO"):
        """Enhanced logging with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def clean_previous_builds(self):
        """Clean all previous build artifacts"""
        self.log("Cleaning previous build artifacts...")
        
        dirs_to_clean = [
            self.dist_dir,
            self.build_dir, 
            self.portable_dir,
            self.project_root / "__pycache__"
        ]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                self.log(f"  Removed: {dir_path}")
                
        # Clean .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            pyc_file.unlink()
            
        self.log("Build cleanup completed")
        
    def verify_environment(self):
        """Verify build environment and dependencies"""
        self.log("Verifying build environment...")
        
        # Check Python version
        python_version = sys.version_info
        self.log(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 11):
            self.log("WARNING: Python 3.11+ recommended for optimal compatibility", "WARN")
            
        # Check required files
        required_files = [
            ".env",
            "main.py", 
            "ocr_watcher.py",
            "enhanced_ocr.py",
            "browser_detector.py",
            "run_ocr.py",
            "hook-paddleocr-runtime.py",
            "app_icon.ico",
            "discord_lugs_portable.spec"
        ]
        
        missing_files = []
        for file_name in required_files:
            if not (self.project_root / file_name).exists():
                missing_files.append(file_name)
                
        if missing_files:
            self.log(f"ERROR: Missing required files: {missing_files}", "ERROR")
            return False
            
        # Check PyInstaller
        try:
            import PyInstaller
            self.log(f"PyInstaller version: {PyInstaller.__version__}")
        except ImportError:
            self.log("ERROR: PyInstaller not found", "ERROR")
            return False
            
        self.log("Environment verification completed successfully")
        return True
        
    def ensure_paddleocr_models(self):
        """Ensure PaddleOCR models are downloaded"""
        self.log("Verifying PaddleOCR models...")
        
        home_dir = Path.home()
        paddleocr_home = home_dir / ".paddleocr"
        models_dir = paddleocr_home / "whl"
        
        if models_dir.exists() and list(models_dir.glob("*")):
            self.log(f"  PaddleOCR models found at: {models_dir}")
            return True
        else:
            self.log("  PaddleOCR models not found, downloading...")
            try:
                # Import PaddleOCR to trigger model download
                result = subprocess.run([
                    sys.executable, "-c", 
                    "import paddleocr; ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en'); print('Models ready')"
                ], capture_output=True, text=True, timeout=600)
                
                if result.returncode == 0:
                    self.log("  PaddleOCR models downloaded successfully")
                    return True
                else:
                    self.log(f"  Model download failed: {result.stderr}", "WARN")
                    return False
                    
            except Exception as e:
                self.log(f"  Model download error: {e}", "WARN")
                return False
                
    def build_single_file_executable(self):
        """Build single-file executable using PyInstaller"""
        self.log("Building single-file executable...")
        
        # Set optimal environment variables
        env = os.environ.copy()
        env['PYTHONPATH'] = str(self.project_root)
        env['PADDLEOCR_HOME'] = str(Path.home() / ".paddleocr")
        env['PYTHONOPTIMIZE'] = '1'  # Enable optimizations
        
        # Build command for single file
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm", 
            "discord_lugs_portable.spec"
        ]
        
        self.log(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                env=env,
                capture_output=True, 
                text=True,
                timeout=3600  # 60 minute timeout
            )
            
            if result.returncode == 0:
                self.log("✅ Single-file executable built successfully!")
                
                # Check if executable exists
                exe_path = self.dist_dir / "discord_lugs_reader.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    self.log(f"  Executable size: {size_mb:.1f} MB")
                    self.log(f"  Location: {exe_path}")
                    return True
                else:
                    self.log("ERROR: Executable not found in expected location", "ERROR")
                    return False
                    
            else:
                self.log("❌ Build failed!", "ERROR")
                self.log(f"STDOUT: {result.stdout}", "ERROR")
                self.log(f"STDERR: {result.stderr}", "ERROR")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("❌ Build timed out after 10 minutes", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Build error: {e}", "ERROR")
            return False
            
    def create_portable_folder(self):
        """Create portable folder with all necessary files"""
        self.log("Creating portable folder distribution...")
        
        # Create portable directory
        self.portable_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_source = self.dist_dir / "discord_lugs_reader.exe"
        exe_dest = self.portable_dir / "discord_lugs_reader.exe"
        
        if exe_source.exists():
            shutil.copy2(exe_source, exe_dest)
            self.log(f"  Copied executable to: {exe_dest}")
        else:
            self.log("ERROR: Source executable not found", "ERROR")
            return False
            
        # Copy essential files
        essential_files = [
            ".env.example",  # Template env file
            "requirements.txt",
            "README.md" if (self.project_root / "README.md").exists() else None
        ]
        
        for file_name in essential_files:
            if file_name and (self.project_root / file_name).exists():
                shutil.copy2(self.project_root / file_name, self.portable_dir / file_name)
                self.log(f"  Copied: {file_name}")
                
        # Create .env.example from .env
        env_file = self.project_root / ".env"
        env_example = self.portable_dir / ".env.example"
        
        if env_file.exists():
            with open(env_file, 'r') as src, open(env_example, 'w') as dst:
                for line in src:
                    if '=' in line:
                        key, _ = line.split('=', 1)
                        dst.write(f"{key}=YOUR_VALUE_HERE\\n")
                    else:
                        dst.write(line)
            self.log("  Created .env.example template")
            
        # Create startup script
        startup_script = self.portable_dir / "start_discord_lugs.bat"
        with open(startup_script, 'w') as f:
            f.write("""@echo off
set "LNK_NAME=Discord Lugs Reader.lnk"
set "EXE_NAME=discord_lugs_reader.exe"

cd /d "%~dp0"

if not exist "%EXE_NAME%" (
    echo [ERROR] %EXE_NAME% not found!
    echo Please ensure this file is in the same folder as %EXE_NAME%
    pause
    exit /b
)

REM Create (or update) the shortcut to ensure it uses the EXE's icon
echo [SETUP] Creating taskbar-friendly launcher...
set "PS_CMD=$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%~dp0%LNK_NAME%'); $s.TargetPath = '%~dp0%EXE_NAME%'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0%EXE_NAME%,0'; $s.Save()"
powershell -Command "%PS_CMD%"

REM Launch the shortcut which spawns the window with the correct icon
echo [LAUNCH] Starting Application...
start "" "%LNK_NAME%"

REM Close this launcher script
exit
""")
        self.log("  Created startup batch file with icon support")
        
        # Create README for portable version
        readme_path = self.portable_dir / "PORTABLE_README.txt"
        with open(readme_path, 'w') as f:
            f.write("""Discord LUGS Reader - Portable Version

SETUP INSTRUCTIONS:
1. Copy .env.example to .env
2. Edit .env file with your Discord webhook and channel URLs
3. Run start_discord_lugs.bat

REQUIREMENTS:
- Windows 10/11 (64-bit)
- Internet connection for Discord integration
- Chrome/Chromium browser installed

TROUBLESHOOTING:
- If the app fails to start, run discord_lugs_reader.exe directly
- Check .env file configuration
- Ensure Discord URLs are correct

For support, check the project documentation.
""")
        self.log("  Created portable README")
        
        self.log("✅ Portable folder created successfully!")
        return True
        
    def run_tests(self):
        """Run basic tests on the built executable"""
        self.log("Running basic tests...")
        
        exe_path = self.dist_dir / "discord_lugs_reader.exe"
        if not exe_path.exists():
            self.log("ERROR: Executable not found for testing", "ERROR")
            return False
            
        # Test 1: Check if executable starts
        try:
            result = subprocess.run([str(exe_path), "--help"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 or "help" in result.stdout.lower():
                self.log("✅ Executable starts successfully")
            else:
                self.log("⚠️  Executable may have startup issues", "WARN")
                
        except subprocess.TimeoutExpired:
            self.log("⚠️  Executable test timed out", "WARN")
        except Exception as e:
            self.log(f"⚠️  Test error: {e}", "WARN")
            
        return True
        
    def build(self):
        """Main build process"""
        self.log("=== Discord LUGS Reader Portable Application Builder ===")
        self.log("Following comprehensive portable application methodology")
        
        # Step 1: Clean previous builds
        self.clean_previous_builds()
        
        # Step 2: Verify environment
        if not self.verify_environment():
            self.log("❌ Environment verification failed!", "ERROR")
            return False
            
        # Step 3: Ensure PaddleOCR models
        if not self.ensure_paddleocr_models():
            self.log("⚠️  Continuing without model verification...", "WARN")
            
        # Step 4: Build single-file executable
        if not self.build_single_file_executable():
            self.log("❌ Executable build failed!", "ERROR")
            return False
            
        # Step 5: Create portable folder
        if not self.create_portable_folder():
            self.log("❌ Portable folder creation failed!", "ERROR")
            return False
            
        # Step 6: Run tests
        self.run_tests()
        
        # Final summary
        self.log("🎉 PORTABLE APPLICATION BUILD COMPLETED SUCCESSFULLY! 🎉")
        self.log(f"Portable folder: {self.portable_dir}")
        self.log(f"Single executable: {self.dist_dir / 'discord_lugs_reader.exe'}")
        
        return True

def main():
    builder = PortableAppBuilder()
    success = builder.build()
    
    if success:
        print("\\n🎉 Build completed successfully!")
        print(f"✅ Portable folder: {builder.portable_dir}")
        print(f"✅ Single executable: {builder.dist_dir / 'discord_lugs_reader.exe'}")
    else:
        print("\\n❌ Build failed! Check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()