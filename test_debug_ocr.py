import cv2
from paddleocr import PaddleOCR
import os

def test_ocr_on_debug_screenshot():
    """Test OCR on debug screenshot to see what content is visible"""
    try:
        # Initialize PaddleOCR - using English model
        print("Initializing PaddleOCR...")
        ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        print("PaddleOCR initialized successfully")
        
        # Test on message area screenshot
        screenshot_path = "debug_screenshots/message_area_20251105_193343.png"
        if not os.path.exists(screenshot_path):
            print(f"Screenshot file not found: {screenshot_path}")
            return
            
        print(f"Testing with file: {screenshot_path}")
        
        # Perform OCR on the image
        print("Performing OCR...")
        result = ocr.ocr(screenshot_path)
        
        # Extract text from OCR results
        text_parts = []
        if result is not None:
            print(f"OCR result type: {type(result)}")
            if isinstance(result, list):
                # Handle list result (PaddleOCR typically returns a list of lists)
                print(f"OCR result has {len(result)} elements")
                for i, item in enumerate(result):
                    if item is not None:
                        print(f"Item {i} type: {type(item)}")
                        if isinstance(item, list):
                            # Each item is a list of [bbox, [text, confidence]]
                            for j, subitem in enumerate(item):
                                if isinstance(subitem, list) and len(subitem) > 1 and isinstance(subitem[1], list) and len(subitem[1]) > 0:
                                    text_parts.append(subitem[1][0])  # Extract the text part
                                    print(f"  Subitem {j}: {subitem[1][0]}")
                        elif isinstance(item, dict) and 'rec_texts' in item:
                            text_parts.extend(item['rec_texts'])
                            print(f"  Found {len(item['rec_texts'])} text parts in item {i}")
                        elif hasattr(item, 'rec_texts'):
                            # Handle object with rec_texts attribute
                            text_parts.extend(item.rec_texts)
                            print(f"  Found {len(item.rec_texts)} text parts in item {i}")
        
        # Join all text parts
        text = ' '.join(text_parts)
        print(f"Extracted text length: {len(text)} characters")
        print(f"Extracted text preview: {text[:1000]}...")
        
        # Look for timestamp patterns
        import re
        timestamp_pattern = r'\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+(?:AM|PM)'
        timestamps = re.findall(timestamp_pattern, text, re.IGNORECASE)
        
        if timestamps:
            print(f"Found {len(timestamps)} timestamps:")
            for i, ts in enumerate(timestamps[:10]):
                print(f"  {i+1}: {ts}")
        else:
            print("No timestamps found in OCR results")
            
        # Look for ticker patterns
        ticker_pattern = r'\[([A-Z]+)\].*?Timestamp:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s+[0-9]{1,2}:[0-9]{2}:[0-9]{2}\s+(?:AM|PM))'
        tickers = re.findall(ticker_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if tickers:
            print(f"Found {len(tickers)} ticker patterns:")
            for i, (ticker_type, timestamp) in enumerate(tickers[:10]):
                print(f"  {i+1}: [{ticker_type}] at {timestamp}")
        else:
            print("No ticker patterns found in OCR results")
        
    except Exception as e:
        print(f"Error during PaddleOCR test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ocr_on_debug_screenshot()