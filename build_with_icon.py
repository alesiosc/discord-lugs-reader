#!/usr/bin/env python3
"""
PyInstaller build script with proper icon embedding and Windows cache handling.
This script creates a proper Windows icon and handles icon cache issues.
"""

import os
import sys
import subprocess
import shutil
from PIL import Image, ImageDraw

def create_proper_icon():
    """Create a professional Windows icon with multiple sizes"""
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Create RGBA image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw Discord-themed blue circle
        margin = size // 8
        draw.ellipse([margin, margin, size - margin, size - margin], 
                    fill='#5865F2', outline='#4752C4', width=max(1, size//64))
        
        # Draw white "D" for Discord
        if size >= 32:
            text_size = size // 2
            bbox = draw.textbbox((0, 0), "D", anchor="mm")
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            draw.text((x, y), "D", fill='white')
        
        images.append(img)
    
    # Save as multi-resolution ICO
    icon_path = 'app_icon.ico'
    images[0].save(icon_path, format='ICO', 
                   sizes=[(img.width, img.height) for img in images])
    
    return icon_path

def clear_windows_icon_cache():
    """Clear Windows icon cache to prevent display issues"""
    try:
        # Stop Explorer, clear cache, restart Explorer
        print("Clearing Windows icon cache...")
        subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], 
                      capture_output=True, check=False)
        
        cache_files = [
            os.path.expandvars(r'%LOCALAPPDATA%\IconCache.db'),
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Explorer\iconcache_*.db')
        ]
        
        for cache_pattern in cache_files:
            import glob
            for cache_file in glob.glob(cache_pattern):
                try:
                    if os.path.exists(cache_file):
                        os.remove(cache_file)
                        print(f"Removed: {cache_file}")
                except PermissionError:
                    print(f"Cannot remove (in use): {cache_file}")
        
        # Restart Explorer
        subprocess.Popen(['explorer.exe'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        print("Windows Explorer restarted")
        
    except Exception as e:
        print(f"Warning: Could not clear icon cache: {e}")

def build_executable():
    """Build the executable with PyInstaller"""
    spec_file = 'monitor.spec'
    
    if not os.path.exists(spec_file):
        print(f"Error: {spec_file} not found!")
        return False
    
    try:
        # Clean previous builds with error handling
        print("Cleaning previous builds...")
        for dir_name in ['dist', 'build']:
            if os.path.exists(dir_name):
                try:
                    shutil.rmtree(dir_name)
                    print(f"   Removed {dir_name}/")
                except PermissionError:
                    print(f"   Warning: Could not remove {dir_name}/ (may be in use)")
                except Exception as e:
                    print(f"   Warning: Error removing {dir_name}/: {e}")
        
        # Run PyInstaller
        print("Building executable with PyInstaller...")
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean', '--noconfirm', spec_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Build successful!")
            
            # Verify executable was created
            exe_path = os.path.join('dist', 'monitor.exe')
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path)
                print(f"Executable created: {exe_path} ({size:,} bytes)")
                return True
            else:
                print("Error: Executable not found after build")
                return False
        else:
            print("Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Build error: {e}")
        return False

def main():
    """Main build process"""
    print("=== Discord Lugs Reader - Icon-Enabled Build ===")
    print()
    
    # Step 1: Create proper icon
    print("1. Creating professional Windows icon...")
    icon_path = create_proper_icon()
    print(f"   Created: {icon_path}")
    
    # Step 2: Build full system executable
    print("\n2. Building full system executable...")
    if build_executable():
        print("\n3. Build completed successfully!")
        print("   Full system executable created with integrated browser detection and Discord messaging")
        print("   The executable should now display the correct icon.")
        print("   If icon doesn't appear immediately, try:")
        print("   - Refreshing the folder (F5)")
        print("   - Restarting Explorer")
        print("   - The script will attempt to clear the icon cache automatically")
        
        # Step 3: Clear icon cache (best effort)
        print("\n4. Attempting to clear Windows icon cache...")
        clear_windows_icon_cache()
        
        return True
    else:
        print("\nBuild failed! Check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)