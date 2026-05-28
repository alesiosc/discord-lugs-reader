import os
import fnmatch

root = "D:/MyPythonProjects_2/discord_lugs_reader+Portable-WORKING"
exclude_dirs = {'node_modules', '__pycache__', '.git', '_MEI422482', '_MEI490602',
                'browser_data', 'browser_data_check', 'browser_data_stable',
                'debug_screenshots', 'screenshots', 'build', 'dist', 'tools',
                '.playwright-mcp', 'test_venv_311', 'tmp_rovodev_chrome_profile',
                'tmp_rovodev_chrome_profile_stable'}

for root_dir, dirs, files in os.walk(root):
    # Skip excluded directories
    dir_name = os.path.basename(root_dir)
    if dir_name in exclude_dirs:
        dirs.clear()
        continue
    
    # Skip if any parent is excluded
    rel = os.path.relpath(root_dir, root)
    if any(ex in rel.split(os.sep) for ex in exclude_dirs):
        dirs.clear()
        continue
    
    for f in files:
        if '.env' in f.lower() or f == '.env':
            full = os.path.join(root_dir, f)
            print(full)
