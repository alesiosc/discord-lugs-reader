"""
Screenshot cleanup for DLR.
Keeps only screenshots from the last 2 hours to prevent disk bloat.
Run manually or via Task Scheduler.
"""
import os, time, shutil

SCREENSHOTS_DIR = r"D:\MyPythonProjects_2\discord_lugs_reader+Portable-WORKING\screenshots"
KEEP_MINUTES = 120  # keep last 2 hours

def cleanup():
    if not os.path.isdir(SCREENSHOTS_DIR):
        print(f"Directory not found: {SCREENSHOTS_DIR}")
        return
    
    now = time.time()
    cutoff = now - (KEEP_MINUTES * 60)
    deleted = 0
    kept = 0
    errors = 0
    
    # Use scandir instead of listdir for performance with huge directories
    with os.scandir(SCREENSHOTS_DIR) as entries:
        for entry in entries:
            if not entry.is_file():
                continue
            name = entry.name
            # Only delete page-*.png files (the bulk screenshot files)
            if name.startswith("page-") and name.endswith(".png"):
                try:
                    mtime = os.path.getmtime(entry.path)
                    if mtime < cutoff:
                        os.remove(entry.path)
                        deleted += 1
                    else:
                        kept += 1
                except Exception as e:
                    errors += 1
                    if errors == 1:
                        print(f"First error: {e}")
    
    print(f"Deleted {deleted} old screenshots, kept {kept}, errors {errors}")

if __name__ == "__main__":
    cleanup()
