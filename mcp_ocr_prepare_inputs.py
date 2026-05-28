import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import shutil

SEARCH_DIRS = [
    Path('screenshots'),
    Path('.playwright-mcp'),
    Path('debug_screenshots'),
]

OUTPUT_DIR = Path('mcp_test_inputs')
MANIFEST = Path('mcp_test_manifest.json')


def find_images(max_count: int):
    candidates = []
    for d in SEARCH_DIRS:
        if not d.exists():
            continue
        for p in d.glob('*.png'):
            try:
                ts = p.stat().st_mtime
            except Exception:
                ts = 0
            candidates.append((p, ts))
    # Sort by modified time desc
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in candidates[:max_count]]


def copy_images(images):
    OUTPUT_DIR.mkdir(exist_ok=True)
    copied = []
    for i, src in enumerate(images, 1):
        dst = OUTPUT_DIR / f'{i:02d}_{src.name}'
        shutil.copy2(src, dst)
        copied.append(dst)
    return copied


def write_manifest(files):
    data = []
    for f in files:
        try:
            ts = datetime.fromtimestamp(f.stat().st_mtime).isoformat()
        except Exception:
            ts = None
        data.append({
            'file': str(f),
            'basename': f.name,
            'modified_iso': ts,
        })
    MANIFEST.write_text(json.dumps({'inputs': data}, indent=2), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description='Prepare MCP OCR test inputs from recent screenshots')
    ap.add_argument('--max', type=int, default=12, help='Max number of images to collect')
    args = ap.parse_args()

    images = find_images(args.max)
    if not images:
        print('No images found in screenshots/.playwright-mcp/debug_screenshots')
        return
    copied = copy_images(images)
    write_manifest(copied)
    print(f'Prepared {len(copied)} images into {OUTPUT_DIR} and manifest {MANIFEST}')


if __name__ == '__main__':
    main()
