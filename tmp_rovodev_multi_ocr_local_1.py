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

from paddleocr import PaddleOCR

SEARCH_DIRS = [Path('screenshots'), Path('.playwright-mcp'), Path('debug_screenshots')]

@dataclass
class OCRResult:
    engine: str
    prep: str
    file: str
    text: str

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

def prep_scale2_inverted(img: Image.Image) -> np.ndarray:
    img = img.resize((img.width*2, img.height*2), Image.LANCZOS)
    return prep_inverted_otsu(img)

def prep_scale2_adaptive(img: Image.Image) -> np.ndarray:
    img = img.resize((img.width*2, img.height*2), Image.LANCZOS)
    return prep_adaptive(img)

def prep_clahe_otsu(img: Image.Image) -> np.ndarray:
    if img.mode != 'RGB':
        img = img.convert('RGB')
    arr = np.array(img)
    lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    rgb = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2RGB)

PREPS: List[Tuple[str, callable]] = [
    ('inverted_otsu', prep_inverted_otsu),
    ('adaptive', prep_adaptive),
    ('scale2_inverted', prep_scale2_inverted),
    ('scale2_adaptive', prep_scale2_adaptive),
    ('clahe_otsu', prep_clahe_otsu),
]

def find_latest_images(max_count: int = 1) -> List[Path]:
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


def paddleocr_instance():
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


def run():
    log_path = Path('tmp_rovodev_local_ocr_results.txt')
    with open(log_path, 'w', encoding='utf-8') as LOG:
        imgs = find_latest_images(1)
        if not imgs:
            LOG.write('No images found to test\nDONE\n')
            return

        LOG.write('Initializing PaddleOCR...\n')
        try:
            paddle = paddleocr_instance()
            # Prewarm with a tiny dummy image to load models fully
            import numpy as _np
            _dummy = _np.ones((32, 32, 3), dtype=_np.uint8) * 255
            try:
                _ = paddle.ocr(_dummy)
            except Exception:
                pass
        except Exception as e:
            LOG.write(f'PaddleOCR init failed: {e}\n')
            paddle = None

        for img_path in imgs:
            LOG.write(f"\nIMAGE: {img_path}\n")
            try:
                base = Image.open(img_path)
            except Exception as e:
                LOG.write(f'  open failed: {e}\n')
                continue

            for prep_name, prep_fn in PREPS:
                try:
                    rgb = prep_fn(base.copy())
                except Exception as e:
                    LOG.write(f'  prep {prep_name} failed: {e}\n')
                    continue

                if paddle is not None:
                    text = paddleocr_ocr(paddle, rgb)
                    data = extract_ticker_data(text)
                    if data:
                        LOG.write(f'  OK Paddle ({prep_name}) entries={len(data)}\n')
                        for item in data:
                            LOG.write('    ' + json.dumps(item) + '\n')
                    else:
                        LOG.write(f'  .. Paddle ({prep_name}) no parse\n')
        LOG.write('\nDONE\n')

if __name__ == '__main__':
    run()
