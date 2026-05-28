"""
Runtime hook for PaddleOCR to fix version file issues in PyInstaller executables
"""
import os
import sys

# Create paddleocr version file if it doesn't exist to prevent crashes
try:
    # Get the paddleocr module path
    import paddleocr
    paddleocr_path = os.path.dirname(paddleocr.__file__)
    paddlex_version_file = os.path.join(paddleocr_path, 'paddlex', '.version')
    
    # Create the version file with a default version if missing
    if not os.path.exists(paddlex_version_file):
        try:
            os.makedirs(os.path.dirname(paddlex_version_file), exist_ok=True)
            with open(paddlex_version_file, 'w') as f:
                f.write('2.8.0')  # Default PaddleOCR version
        except Exception:
            pass  # Ignore errors if we can't create the file
except Exception:
    pass  # Ignore any errors during initialization

# Ensure PaddleOCR can find its models
try:
    # Set PaddleOCR to use user home directory for models
    if 'PADDLEOCR_HOME' not in os.environ:
        os.environ['PADDLEOCR_HOME'] = os.path.join(os.path.expanduser('~'), '.paddleocr')
except Exception:
    pass  # Ignore errors