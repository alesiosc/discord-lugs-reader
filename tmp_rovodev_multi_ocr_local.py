import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

import numpy as np
import cv2
from PIL import Image, ImageEnhance

# PaddleOCR (from venv311)
from paddleocr import PaddleOCR

SEARCH_DIRS = [Path('screenshots'), Path('.playwright-mcp'), Path('debug_screenshots')]

@dataclass
class OCRResult:
    engine: str
    prep: str
    file: str
    text: str

# ---------- Preprocessing pipelines ----------

def prep_inverted_otsu(img: Image.Image) -> np.ndarray:
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img = ImageEnhance.Sharpness(img).enhance(1.1)
    arr = np.array(img)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    inv = cv2.bitwise_not(gray)
    _, th = cv2.threshold(inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2RGB)


def prep_adaptive(img: Image.Image) -> np.ndarray:
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = ImageEnhance.Contrast(img).enhance(1.15)
    arr = np.array(img)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 8)
    kernel = np.ones((2,2), np.uint8)
    th = cv2.dilate(th, kernel, iterations=1)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2RGB)

PREPS: List[Tuple[str, callable]] = [
    ('inverted_otsu', prep_inverted_otsu),
    ('adaptive', prep_adaptive),
]

# ---------- Discovery ----------

def find_latest_images(max_count: int = 8) -> List[Path]:
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
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [p for p,_ in candidates[:max_count]]

# ---------- PaddleOCR ----------

def paddleocr_instance():
    # Use a minimal, robust config (no deprecated use_gpu)
    return PaddleOCR(use_angle_cls=True, lang='en')


def paddleocr_ocr(ocr: PaddleOCR, image_rgb: np.ndarray) -> str:
    try:
        res = ocr.ocr(image_rgb)
    except Exception as e:
        return ''
    if not res:
        return ''
    lines = []
    try:
        for line in res[0]:
            if isinstance(line, list) and len(line) >= 2 and isinstance(line[1], (list, tuple)):
                lines.append(str(line[1][0]))
            elif isinstance(line, (list, tuple)) and len(line) == 2 and isinstance(line[1], (list, tuple)):
                lines.append(str(line[1][0]))
    except Exception:
        pass
    return '\n'.join(lines)

# ---------- Tesseract (CLI) ----------

def tesseract_available() -> bool:
    return shutil.which('tesseract') is not None


def tesseract_ocr(image_rgb: np.ndarray) -> str:
    # Write to a temp PNG, call tesseract, read txt, then clean up
    tmp_png = Path('tmp_rovodev_tess_input.png')
    tmp_txt = Path('tmp_rovodev_tess_output')  # tesseract adds .txt
    try:
        Image.fromarray(image_rgb).save(tmp_png)
        # --psm 6: assume a single uniform block of text; you can try 3 or 4
        cmd = ['tesseract', str(tmp_png), str(tmp_txt), '--dpi', '300', '--psm', '6']
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_path = Path(str(tmp_txt) + '.txt')
        if out_path.exists():
            text = out_path.read_text(encoding='utf-8', errors='ignore')
        else:
            text = ''
        return text
    except Exception:
        return ''
    finally:
        try:
            if tmp_png.exists(): tmp_png.unlink()
            out_path = Path(str(tmp_txt) + '.txt')
            if out_path.exists(): out_path.unlink()
        except Exception:
            pass

# ---------- Ticker parsing ----------
import re
MATCHERS = [
    r'\[([A-Z]+)\].*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)).*?Mid:\s*([0-9.]+).*?Lower:\s*([0-9.]+).*?Upper:\s*([0-9.]+)'
]
VALID_TYPES = {'NQ','ES','YM','RTY','CL'}

def extract_ticker_data(text: str):
    out = []
    for pat in MATCHERS:
        m = re.findall(pat, text, re.IGNORECASE | re.DOTALL)
        for t, ts, mid, low, up in m:
            t = t.upper()
            if t in VALID_TYPES:
                try:
                    out.append({'type': t, 'timestamp': ts, 'mid': float(mid), 'lower': float(low), 'upper': float(up)})
                except ValueError:
                    continue
    return out

# ---------- Runner ----------

def run():
    imgs = find_latest_images(8)
    if not imgs:
        print('No images found to test')
        return

    print('Initializing PaddleOCR...')
    try:
        paddle = paddleocr_instance()
    except Exception as e:
        print(f'PaddleOCR init failed: {e}')
        paddle = None

    tess_ok = tesseract_available()
    if tess_ok:
        print('Tesseract CLI found on PATH.')
    else:
        print('Tesseract CLI not found; skipping Tesseract tests.')

    successes = []

    for img_path in imgs:
        print(f"\nIMAGE: {img_path}")
        try:
            base = Image.open(img_path)
        except Exception as e:
            print(f'  open failed: {e}')
            continue

        for prep_name, prep_fn in PREPS:
            try:
                rgb = prep_fn(base.copy())
            except Exception as e:
                print(f'  prep {prep_name} failed: {e}')
                continue

            # PaddleOCR
            if paddle is not None:
                text = paddleocr_ocr(paddle, rgb)
                data = extract_ticker_data(text)
                if data:
                    print(f'  OK Paddle ({prep_name}) entries={len(data)}')
                    successes.append(('Paddle', prep_name, str(img_path), len(data)))
                else:
                    print(f'  .. Paddle ({prep_name}) no parse')

            # Tesseract CLI
            if tess_ok:
                text = tesseract_ocr(rgb)
                data = extract_ticker_data(text)
                if data:
                    print(f'  OK Tesseract ({prep_name}) entries={len(data)}')
                    successes.append(('Tesseract', prep_name, str(img_path), len(data)))
                else:
                    print(f'  .. Tesseract ({prep_name}) no parse')

    print('\nSUMMARY:')
    if not successes:
        print('  No engine/prep combination parsed ticker data on tested images.')
    else:
        for s in successes:
            print(' ', s)

if __name__ == '__main__':
    run()
