"""
PyInstaller hook for PaddleOCR to fix version file issues
"""
import os
import sys
from PyInstaller.utils.hooks import collect_data_files

# Collect PaddleOCR data files
datas = collect_data_files('paddleocr')

# Create a hidden import for the version file handling
hiddenimports = [
    'paddleocr',
    'paddleocr.paddleocr',
    'paddleocr.tools',
    'paddleocr.utility',
    'paddleocr.concurrency',
    'paddleocr.ppocr',
    'paddleocr.ppocr.data',
    'paddleocr.ppocr.data.imaug',
    'paddleocr.ppocr.modeling.architectures',
    'paddleocr.ppocr.modeling.necks',
    'paddleocr.ppocr.modeling.heads',
    'paddleocr.ppocr.postprocess',
    'paddleocr.ppocr.utils.logging',
    'paddleocr.ppocr.utils.utility',
    'paddleocr.ppocr.utils.matrix',
    'paddleocr.ppocr.utils.ocr_utils',
    'paddleocr.ppocr.utils.utility',
    'paddlex',
    'paddlex.deploy',
]

# Create runtime hook to handle version file creation
runtime_hook = """
import os
import sys

# Create paddleocr version file if it doesn't exist
def create_paddleocr_version():
    try:
        import paddleocr
        # Get the paddleocr module path
        paddleocr_path = os.path.dirname(paddleocr.__file__)
        version_file = os.path.join(paddleocr_path, 'paddlex', '.version')
        
        if not os.path.exists(version_file):
            os.makedirs(os.path.dirname(version_file), exist_ok=True)
            with open(version_file, 'w') as f:
                f.write('2.8.0')  # Default PaddleOCR version
    except Exception:
        pass  # Ignore errors during version file creation

# Call the function when the module loads
create_paddleocr_version()
"""

# Add runtime hook if creating the hook file
if not os.path.exists('hook-paddleocr.py'):
    # Write runtime hook
    runtime_hooks = [os.path.abspath('hook-paddleocr-runtime.py') if os.path.exists('hook-paddleocr-runtime.py') else None]
    
    if runtime_hooks[0] is None:
        # Create runtime hook file
        with open('hook-paddleocr-runtime.py', 'w') as f:
            f.write(runtime_hook)
        runtime_hooks = [os.path.abspath('hook-paddleocr-runtime.py')]

hiddenimports = [
    'paddleocr',
    'paddleocr.paddleocr',
    'paddleocr.tools',
    'paddleocr.utility',
    'paddleocr.concurrency',
    'paddleocr.ppocr',
    'paddleocr.ppocr.data',
    'paddleocr.ppocr.data.imaug',
    'paddleocr.ppocr.modeling.architectures',
    'paddleocr.ppocr.modeling.necks',
    'paddleocr.ppocr.modeling.heads',
    'paddleocr.ppocr.postprocess',
    'paddleocr.ppocr.utils.logging',
    'paddleocr.ppocr.utils.utility',
    'paddleocr.ppocr.utils.matrix',
    'paddleocr.ppocr.utils.ocr_utils',
    'paddleocr.ppocr.utils.utility',
    'paddlex',
    'paddlex.deploy',
    'shutil_which',
    'decorator',
    'tqdm.auto',
    'gmpy2',
    'rapidfuzz.utils',
    'rapidfuzz',
    'google.protobuf',
    'google.protobuf.internal',
    'onnxruntime',
    'paddlepaddle'
]

# Add PaddleOCR data files
datas = []
datas += collect_data_files('paddleocr')
datas += collect_data_files('paddlex')

# Create a runtime hook file
if not os.path.exists('hook-paddleocr-runtime.py'):
    with open('hook-paddleocr-runtime.py', 'w') as f:
        f.write(runtime_hook)

# Update hidden imports
hiddenimports = [
    'paddleocr',
    'paddleocr.paddleocr',
    'paddleocr.tools', 
    'paddleocr.utility',
    'paddleocr.concurrency',
    'paddleocr.ppocr',
    'paddleocr.ppocr.data',
    'paddleocr.ppocr.data.imaug',
    'paddleocr.ppocr.modeling.architectures',
    'paddleocr.ppocr.modeling.necks',
    'paddleocr.ppocr.modeling.heads',
    'paddleocr.ppocr.postprocess',
    'paddleocr.ppocr.utils.logging',
    'paddleocr.ppocr.utils.utility',
    'paddleocr.ppocr.utils.matrix',
    'paddleocr.ppocr.utils.ocr_utils',
    'paddleocr.ppocr.utils.utility',
    'paddlex',
    'paddlex.deploy'
]

datas = collect_data_files('paddleocr')
runtime_hooks = [os.path.abspath('hook-paddleocr-runtime.py')]

# This part would be needed if this is an actual PyInstaller hook file
hiddenimports = [
    'paddleocr',
    'paddleocr.paddleocr',
    'paddleocr.tools', 
    'paddleocr.utility',
    'paddleocr.concurrency',
    'paddleocr.ppocr',
    'paddleocr.ppocr.data',
    'paddleocr.ppocr.data.imaug',
    'paddleocr.ppocr.modeling.architectures',
    'paddleocr.ppocr.modeling.necks',
    'paddleocr.ppocr.modeling.heads',
    'paddleocr.ppocr.postprocess',
    'paddleocr.ppocr.utils.logging',
    'paddleocr.ppocr.utils.utility',
    'paddleocr.ppocr.utils.matrix',
    'paddleocr.ppocr.utils.ocr_utils',
    'paddlex',
    'paddlex.deploy'
]

datas = collect_data_files('paddleocr')
runtime_hooks = [os.path.abspath('hook-paddleocr-runtime.py')]