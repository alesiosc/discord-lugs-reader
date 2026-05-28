from pathlib import Path
from datetime import datetime
from enhanced_ocr import EnhancedOCR
from PIL import Image

LOG_PATH = Path('tmp_rovodev_offline_ocr.txt')
SEARCH_DIRS = [Path('screenshots'), Path('.playwright-mcp'), Path('debug_screenshots')]


def log(msg: str):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | {msg}\n")


def find_latest_image():
    candidates = []
    for d in SEARCH_DIRS:
        if not d.exists():
            continue
        for p in d.glob('*.png'):
            if p.name.endswith('_processed.png'):
                continue
            try:
                candidates.append((p, p.stat().st_mtime))
            except Exception:
                pass
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def main():
    try:
        LOG_PATH.write_text('', encoding='utf-8')
    except Exception:
        pass

    img = find_latest_image()
    if not img:
        log('No PNG screenshots found in screenshots/.playwright-mcp/debug_screenshots')
        log('DONE')
        return

    log(f'Offline OCR on latest screenshot: {img}')
    ocr = EnhancedOCR(timeout_seconds=45)

    # 1) RAW image
    data = ocr.extract_ticker_data(str(img))
    if data:
        log(f'RAW: Parsed {len(data)} entries')
        for item in data:
            log(f'RAW: {item}')
        log('DONE')
        return
    else:
        log('RAW: No parse, trying bottom-crop...')

    # 2) Bottom crop
    try:
        im = Image.open(img)
        w, h = im.size
        ch = max(100, min(700, h))
        crop = im.crop((0, max(0, h - ch), w, h))
        tmp = img.with_name(img.stem + '_offline_bottom700.png')
        crop.save(tmp)
        data2 = ocr.extract_ticker_data(str(tmp))
        if data2:
            log(f'BOTTOM: Parsed {len(data2)} entries')
            for item in data2:
                log(f'BOTTOM: {item}')
            log('DONE')
            return
        else:
            log('BOTTOM: No parse')
    except Exception as e:
        log(f'Bottom-crop attempt failed: {e}')

    log('No ticker data parsed from offline run.')
    log('DONE')

if __name__ == '__main__':
    main()
