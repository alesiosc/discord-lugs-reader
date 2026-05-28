import os
from pathlib import Path
from enhanced_ocr import EnhancedOCR

from PIL import Image

SEARCH_DIRS = [Path('screenshots'), Path('.playwright-mcp'), Path('debug_screenshots')]


def find_latest_image():
    candidates = []
    for d in SEARCH_DIRS:
        if not d.exists():
            continue
        for p in d.glob('*.png'):
            if p.name.endswith('_processed.png'):
                # Skip already-processed files
                continue
            try:
                candidates.append((p, p.stat().st_mtime))
            except Exception:
                pass
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def crop_bottom(image_path: Path, crop_height=700) -> Path | None:
    try:
        img = Image.open(image_path)
        w, h = img.size
        ch = max(100, min(crop_height, h))
        box = (0, max(0, h - ch), w, h)
        cropped = img.crop(box)
        out_path = image_path.with_name(image_path.stem + f'_bottom{ch}.png')
        cropped.save(out_path)
        return out_path
    except Exception as e:
        print(f'crop_bottom failed: {e}')
        return None


def main():
    img = find_latest_image()
    if not img:
        print('No suitable PNG screenshots found in screenshots/.playwright-mcp/debug_screenshots')
        return
    print(f'Testing EnhancedOCR on: {img}')
    ocr = EnhancedOCR(timeout_seconds=30)

    # 1) Raw image
    data = ocr.extract_ticker_data(str(img))
    if data:
        print(f'Parsed {len(data)} entries from RAW image:')
        for item in data:
            print(item)
        return
    print('No data from RAW image, trying bottom-crop...')

    # 2) Bottom crop
    bottom = crop_bottom(img, crop_height=700)
    if bottom is not None:
        data2 = ocr.extract_ticker_data(str(bottom))
        if data2:
            print(f'Parsed {len(data2)} entries from BOTTOM-CROP:')
            for item in data2:
                print(item)
            return
    print('No ticker data parsed from EnhancedOCR (raw or bottom-crop).')

if __name__ == '__main__':
    main()
