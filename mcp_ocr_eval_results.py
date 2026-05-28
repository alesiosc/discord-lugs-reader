import argparse
import json
import re
from datetime import datetime

# Regex patterns adapted from main.py/enhanced_ocr.py
PATTERNS = [
    r'\[([A-Z]+)\].*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)).*?Mid:\s*([0-9.]+).*?Lower:\s*([0-9.]+).*?Upper:\s*([0-9.]+)',
    r'\[([A-Z]+)\].*?Published Level:.*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)).*?Mid:\s*([0-9.]+).*?Lower:\s*([0-9.]+).*?Upper:\s*([0-9.]+)',
    r'\[([A-Z]+)\].*?Timestamp[:\s]*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM)).*?Mid[:\s]*([0-9.]+).*?Lower[:\s]*([0-9.]+).*?Upper[:\s]*([0-9.]+)',
]

VALID_TYPES = {'NQ','ES','YM','RTY','CL'}

def parse_text(text: str):
    if not text:
        return []
    matches = []
    for pat in PATTERNS:
        try:
            m = re.findall(pat, text, re.IGNORECASE | re.DOTALL)
            if m:
                matches = m
                break
        except Exception:
            continue
    out = []
    for ticker_type, timestamp, mid, lower, upper in matches:
        try:
            out.append({
                'type': ticker_type.upper().strip(),
                'timestamp': timestamp.strip(),
                'mid': float(mid),
                'lower': float(lower),
                'upper': float(upper)
            })
        except ValueError:
            continue
    # keep latest per type
    latest = {}
    for item in out:
        t = item['type']
        if t not in VALID_TYPES:
            continue
        try:
            ts = datetime.strptime(item['timestamp'], '%m/%d/%Y %I:%M:%S %p')
        except Exception:
            ts = None
        prev = latest.get(t)
        if prev is None:
            latest[t] = {**item, '_ts': ts}
        else:
            if ts and (prev.get('_ts') is None or ts > prev.get('_ts')):
                latest[t] = {**item, '_ts': ts}
    for v in latest.values():
        v.pop('_ts', None)
    return list(latest.values())


def main():
    ap = argparse.ArgumentParser(description='Evaluate MCP OCR results JSON against ticker parsers')
    ap.add_argument('--results', required=True, help='Path to mcp_test_results.json produced after MCP OCR runs')
    args = ap.parse_args()

    with open(args.results, 'r', encoding='utf-8') as f:
        data = json.load(f)

    engines = data.get('engines', [])
    inputs = data.get('inputs', [])

    print('MCP OCR Evaluation Summary')
    print(f'- Engines: {", ".join(e.get("name","?") for e in engines)}')
    print(f'- Inputs:  {len(inputs)} images')

    # Per engine metrics
    for eng in engines:
        name = eng.get('name')
        print('\n--- Engine:', name, '---')
        per_type = {t: {'count': 0, 'latest': None} for t in VALID_TYPES}
        successes = 0

        for inp in inputs:
            entry = inp.get('results', {}).get(name, {})
            text = entry.get('text', '')
            parsed = parse_text(text)
            if parsed:
                successes += 1
            for item in parsed:
                t = item['type']
                per_type[t]['count'] += 1
                try:
                    ts = datetime.strptime(item['timestamp'], '%m/%d/%Y %I:%M:%S %p')
                except Exception:
                    ts = None
                if ts:
                    prev = per_type[t]['latest']
                    if (prev is None) or (datetime.strptime(prev['timestamp'], '%m/%d/%Y %I:%M:%S %p') < ts):
                        per_type[t]['latest'] = item

        print(f'Screens with any parsed results: {successes} / {len(inputs)}')
        for t in VALID_TYPES:
            c = per_type[t]['count']
            latest = per_type[t]['latest']
            latest_s = latest['timestamp'] if latest else '-'
            print(f'  {t}: count={c}, latest={latest_s}')

    print('\nDone.')


if __name__ == '__main__':
    main()
