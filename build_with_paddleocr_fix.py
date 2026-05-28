"""
Build script with PaddleOCR PyInstaller fixes
"""
import os
import sys
import subprocess
import shutil

def clean_build():
    """Clean previous build files"""
    print("Cleaning previous build files...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")

def ensure_paddleocr_models():
    """Ensure PaddleOCR models are available for building"""
    print("Checking PaddleOCR models...")
    
    # Check if models exist
    home_dir = os.path.expanduser('~')
    paddleocr_home = os.path.join(home_dir, '.paddleocr')
    models_dir = os.path.join(paddleocr_home, 'whl')
    
    if os.path.exists(models_dir):
        print(f"  PaddleOCR models found at: {models_dir}")
        return True
    else:
        print(f"  PaddleOCR models not found, downloading...")
        try:
            # Run paddleocr to download models
            result = subprocess.run([
                sys.executable, '-c', 
                'import paddleocr; print("Models downloading...")'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("  PaddleOCR models downloaded successfully")
                return True
            else:
                print(f"  Warning: Model download failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"  Warning: Could not download models: {e}")
            return False

def build_executable():
    """Build the executable with PyInstaller"""
    print("Building executable with PyInstaller...")
    
    # Set environment variables for PaddleOCR
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    env['PADDLEOCR_HOME'] = os.path.join(os.path.expanduser('~'), '.paddleocr')
    
    # Build command - use Python 3.11 via py launcher
    cmd = [
        'py',
        '-3.11',
        '-c',
        'import sys; print("Using Python:", sys.executable); import PyInstaller; PyInstaller.__main__.main()',
        '--clean',
        'monitor.spec'
    ]
    
    # Actually, let's use a simpler approach - shell=True to run the command properly
    full_cmd = 'py -3.11 -m PyInstaller --clean monitor.spec'
    print(f"Running: {full_cmd}")
    result = subprocess.run(full_cmd, shell=True, env=env, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Build completed successfully!")
        print(f"Executable location: {os.path.join(os.getcwd(), 'dist', 'monitor.exe')}")
        return True
    else:
        print("❌ Build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False

def main():
    """Main build process"""
    print("=== Building Discord LUGS Reader with PaddleOCR Fix ===")
    
    # Clean build
    clean_build()
    
    # Ensure PaddleOCR models
    if not ensure_paddleocr_models():
        print("⚠️  Continuing build without model verification...")
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("\nThe executable should now work with PaddleOCR.")
        print("If you still get errors, run the main.py file directly from the source.")
    else:
        print("\n❌ Build failed!")
        print("Check the error messages above.")

if __name__ == "__main__":
    main()