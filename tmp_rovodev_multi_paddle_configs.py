import os
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
import traceback

import numpy as np
import cv2
from PIL import Image, ImageEnhance
from paddleocr import PaddleOCR

SEARCH_DIRS = [Path('screenshots'), Path('.playwright-mcp'), Path('debug_screenshots')]

@dataclass
class OCRConfig:
    name: str
    kwargs: dict

# Define several PaddleOCR configuration variants
OCR_CONFIGS = [
    OCRConfig('SVTR_LCNet_angle_cls', dict(use_angle_cls=True, lang='en', det_algorithm='DB', rec_algorithm='SVTR_LCNet', use_gpu=False, enable_mkldnn=True, cpu_threads=2)),
    OCRConfig('Basic_angle_cls', dict(use_angle_cls=True, lang='en', use_gpu=False)),
    OCRConfig('Minimal', dict(lang='en', use_gpu=False)),
]

# Preprocessing pipelines

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

def prep_clahe(img: Image.Image) -> np.ndarray:
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

def prep_none(img: Image.Image) -> np.ndarray:
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return np.array(img)

PREPS: List[Tuple[str, callable]] = [
    ('inverted_otsu', prep_inverted_otsu),
    ('adaptive', prep_adaptive),
    ('clahe_otsu', prep_clahe),
    ('raw', prep_none),
]


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


def parse_text_from_result(result) -> str:
    # PaddleOCR returns list of [[box], (text, prob)] per image; we join lines
    if not result:
        return ''
    lines = []
    try:
        for line in result[0]:
            if isinstance(line, list) and len(line) >= 2 and isinstance(line[1], (list, tuple)):
                lines.append(str(line[1][0]))
            elif isinstance(line, (list, tuple)) and len(line) == 2 and isinstance(line[1], (list, tuple)):
                lines.append(str(line[1][0]))
    except Exception:
        pass
    return '\n'.join(lines)

# Simple ticker parser copied from project regex (loose)
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
    images = find_latest_images(8)
    if not images:
        print('No images found to test')
        return

    # Build OCR instances per config (lazy init)
    ocr_instances = {}

    successes = []

    for img_path in images:
        print(f"\nIMAGE: {img_path}")
        try:
            base_img = Image.open(img_path)
        except Exception as e:
            print(f"  Failed to open image: {e}")
            continue

        for prep_name, prep_fn in PREPS:
            try:
                prepped = prep_fn(base_img.copy())
            except Exception as e:
                print(f"  Prep {prep_name} failed: {e}")
                continue

            for cfg in OCR_CONFIGS:
                key = cfg.name
                if key not in ocr_instances:
                    try:
                        ocr_instances[key] = PaddleOCR(**cfg.kwargs)
                    except Exception as e:
                        print(f"    Init OCR {key} failed: {e}")
                        continue
                ocr = ocr_instances[key]
                try:
                    res = ocr.ocr(prepped)
                    text = parse_text_from_result(res)
                    data = extract_ticker_data(text)
                    if data:
                        print(f"  OK: prep={prep_name}, ocr={key}, entries={len(data)}")
                        for item in data[:2]:
                            print(f"     - {item}")
                        successes.append((str(img_path), prep_name, key, len(data)))
                        # don't break; collect all
                    else:
                        print(f"  ..: prep={prep_name}, ocr={key}, no parse")
                except Exception as e:
                    print(f"  ERR: prep={prep_name}, ocr={key} -> {e}")
                    # print(traceback.format_exc())

    print("\nSUMMARY of successes:")
    if not successes:
        print("  No combinations produced parsed data.")
    else:
        for s in successes:
            print("  ", s)

if __name__ == '__main__':
    run()
