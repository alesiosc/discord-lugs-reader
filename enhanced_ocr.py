import os
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import List, Dict
from dotenv import load_dotenv
import easyocr
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import re

logger = logging.getLogger(__name__)
load_dotenv()

class EnhancedOCR:
    """Crash-resistant OCR wrapper with preprocessing, timeout and parsing helpers."""

    def __init__(self, timeout_seconds: int = 30):
        self.reader = None
        self.timeout = timeout_seconds
        self._init_easy_ocr()

    def _init_easy_ocr(self):
        try:
            # Initialize EasyOCR reader with English language
            self.reader = easyocr.Reader(['en'])
            logger.info("EasyOCR initialized with English language.")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
            raise

    def _ocr_with_timeout(self, image_input):
        """Run OCR directly in the main thread with EasyOCR."""
        if self.reader is None:
            self._init_easy_ocr()
        try:
            logger.info(f"Calling EasyOCR reader.readtext() on {image_input}")
            result = self.reader.readtext(image_input)
            logger.info("EasyOCR reader.readtext() call completed.")
            return result
        except Exception as e:
            logger.error(f"EasyOCR op failed in main thread: {e}", exc_info=True)
            return None

    def extract_ticker_data(self, image_path: str) -> List[Dict]:
        """Extract ticker data using EasyOCR."""
        logger.info("--- RUNNING OCR VIA ENHANCED_OCR WRAPPER (EasyOCR) ---")
        
        result = self._ocr_with_timeout(image_path)
        
        logger.info(f"--- RAW EASYOCR RESULT (from wrapper) ---")
        logger.info(f"Raw EasyOCR result: {result}")
        
        text = self.parse_text(result)
        if text:
            logger.info(f"Parsed text: {text}")
            data = self.extract_ticker_data_from_text(text)
            if data:
                logger.info("Found data with new parsing.")
                return data
        
        return []

    def parse_text(self, result) -> str:
        """Parse text from EasyOCR's output structure."""
        if not result:
            return ""
        
        parts = []
        for (bbox, text, prob) in result:
            parts.append(text)
        
        return ' '.join(parts).strip()

    def extract_ticker_data_from_text(self, text: str) -> List[Dict]:
        """More flexible regex to find ticker data, even if incomplete."""
        if not text:
            return []
        
        # Debug: Log the raw text to see what we're working with
        logger.info(f"--- RAW PARSED TEXT FROM EASYOCR: {text}")
        
        # Pre-process text to fix common OCR errors
        # Fix "LLevel" to "Level" - handle OCR misreads (including with colon)
        text = re.sub(r'LLevel(?=\s*:)', 'Level', text, flags=re.IGNORECASE)
        text = re.sub(r'L\s*Level(?=\s*:)', 'Level', text, flags=re.IGNORECASE)
        # Replace "Level: Lug Timestamp" with "Level: Timestamp" to fix parsing
        text = re.sub(r'Level:\s*Lug\s+Timestamp', 'Level: Timestamp', text, flags=re.IGNORECASE)
        text = re.sub(r'evel\s*:', 'Level:', text, flags=re.IGNORECASE)
        
        # Fix character recognition issues
        # Fix "0O" (zero-O) to "00" (zero-zero) - handle all O that should be 0
        text = re.sub(r'(\d)O(\d)', r'\g<1>0\g<2>', text)  # digit-O-digit -> digit-0-digit
        text = re.sub(r'(\d)O(?=\.|:|$|\s)', r'\g<1>0', text)  # Handle trailing O after digit
        # Fix dots in time format to colons
        text = re.sub(r'(\d{1,2})\.(\d{2})\.(\d{2})', r'\1:\2:\3', text)  # HH.MM.SS -> HH:MM:SS
        
        # Fix timestamp format issues: "11/10/20252.28.00" → "11/10/2025 2:28:00"
        # Pattern: year concatenated with time, missing space and colons
        text = re.sub(r'(\d{4})(\d{1,2})\.(\d{2})\.(\d{2})', r'\1 \2:\3:\4', text)
        # Add space between year and time if concatenated: "20252:28" → "2025 2:28"  
        text = re.sub(r'(\d{4})(\d{1,2}:\d{2})', r'\1 \2', text)
        # General case: year concatenated with hours
        text = re.sub(r'(\d{4})(\d{1,2}:\d{2}:\d{2})', r'\1 \2', text)
        
        # Fix specific timestamp format issues from the logs
        # Fix "11/12/2025.2.02.00" → "11/12/2025 2:02:00" (date with concatenated time)
        text = re.sub(r'(\d{1,2}/\d{1,2}/\d{4})\.(\d{1,2})\.(\d{2})\.(\d{2})', r'\1 \2:\3:\4', text)
        # Fix "11/12/2025:2:02:00" → "11/12/2025 2:02:00" (colon after year)
        text = re.sub(r'(\d{1,2}/\d{1,2}/\d{4}):(\d{1,2}:\d{2}:\d{2})', r'\1 \2', text)
        # Additional fix for date.time format without year concatenation
        text = re.sub(r'(\d{1,2}/\d{1,2}/\d{4})\.(\d{1,2}:\d{2}:\d{2})', r'\1 \2', text)
        
        # Fix "140.00" → "1:40:00" or "1140.00" → "11:40:00" in timestamps using safe AM/PM context
        text = re.sub(r'\b(\d{1,2})(\d{2})\.(\d{2})\s*(AM|PM)', r'\1:\2:\3 \4', text)
        text = re.sub(r'\b(\d{1,2})(\d{2}):(\d{2})\s*(AM|PM)', r'\1:\2:\3 \4', text)
        
        # Original date-based fixes as backup
        text = re.sub(r'(\d{1,2}/\d{1,2}/\d{4}\s+)(\d{1,2})(\d{2})\.(\d{2})', r'\g<1>\g<2>:\g<3>:\g<4>', text)

        # Debug: Log the text after preprocessing to verify fixes
        logger.info(f"--- TEXT AFTER PREPROCESSING: {text}")

        # Search for each ticker type individually to avoid complex regex issues
        out = []
        
        # Find all ticker types in the text
        enabled_tickers = os.getenv('ENABLED_TICKERS', 'NQ,ES,YM,CL,GC')
        ticker_patterns = [ticker.strip() for ticker in enabled_tickers.split(',')]
        
        for ticker_type in ticker_patterns:
            # Look for this specific ticker type
            ticker_pattern = rf'\[{ticker_type}\][^[]*?Timestamp[^[]*?(?=\[|$)'
            
            ticker_matches = re.finditer(ticker_pattern, text, re.IGNORECASE | re.DOTALL)
            
            for match in ticker_matches:
                block_text = match.group(0)
                logger.info(f"Found {ticker_type} block: {block_text[:100]}...")
                
                # Extract timestamp from the block
                timestamp_match = re.search(r'Timestamp[^,]*?([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}[^,]*?(?:AM|PM))', block_text, re.IGNORECASE)
                if not timestamp_match:
                    logger.warning(f"Could not find timestamp in {ticker_type} block")
                    continue
                
                timestamp = timestamp_match.group(1).strip()
                
                # Now, find Mid, Lower, Upper within this block
                # Updated patterns to handle trailing commas and spaces better
                mid_match = re.search(r'Mid\s*[:,\.]*\s*([0-9][0-9,]*\.?[0-9]*)', block_text, re.IGNORECASE)
                lower_match = re.search(r'Lower\s*[:,\.]*\s*([0-9][0-9,]*\.?[0-9]*)', block_text, re.IGNORECASE)
                upper_match = re.search(r'Upper\s*[:,\.]*\s*([0-9][0-9,]*\.?[0-9]*)', block_text, re.IGNORECASE)

                def to_float(s):
                    # Clean up the string: remove commas and trailing punctuation
                    cleaned = str(s).replace(',', '').rstrip('.,;: ')
                    return float(cleaned)

                try:
                    # Normalize timestamp format for datetime parsing
                    timestamp_normalized = timestamp.replace('.', ':')
                    
                    # Clean up any remaining issues in timestamp
                    # Remove extra colons that might have been introduced
                    timestamp_normalized = re.sub(r':+', ':', timestamp_normalized)
                    # Fix any remaining "0O" patterns in time
                    timestamp_normalized = re.sub(r'(\d)O(\d)', r'\g<1>0\g<2>', timestamp_normalized)
                    timestamp_normalized = re.sub(r'(\d)O(?=\s|:|$)', r'\g<1>0', timestamp_normalized)
                    
                    logger.info(f"Normalized timestamp: '{timestamp_normalized}' from original: '{timestamp}'")
                    
                    # Attempt to parse with seconds, then without
                    try:
                        dt_object = datetime.strptime(timestamp_normalized, '%m/%d/%Y %I:%M:%S %p')
                    except ValueError:
                        try:
                            dt_object = datetime.strptime(timestamp_normalized, '%m/%d/%Y %I:%M %p')
                        except ValueError:
                            # Try without leading zero on hour
                            timestamp_alt = re.sub(r'(\d{1,2}/\d{1,2}/\d{4})\s+0(\d:\d{2})', r'\1 \2', timestamp_normalized)
                            dt_object = datetime.strptime(timestamp_alt, '%m/%d/%Y %I:%M %p')
                    
                    # Extract values
                    mid_val = to_float(mid_match.group(1)) if mid_match else None
                    lower_val = to_float(lower_match.group(1)) if lower_match else None
                    upper_val = to_float(upper_match.group(1)) if upper_match else None

                    # Perform Validation
                    is_valid = True
                    current_type = ticker_type.upper().strip()
                    if current_type == 'ES':
                        # Must be 4 digits (1000 <= val < 10000)
                        for val_name, val in [('Mid', mid_val), ('Lower', lower_val), ('Upper', upper_val)]:
                            if val is not None:
                                if not (1000 <= val < 10000):
                                    logger.warning(f"ES Validation Failed: {val_name} value {val} is not 4 digits.")
                                    is_valid = False
                    elif current_type == 'NQ':
                        # Must be 5 digits (10000 <= val < 100000)
                        for val_name, val in [('Mid', mid_val), ('Lower', lower_val), ('Upper', upper_val)]:
                            if val is not None:
                                if not (10000 <= val < 100000):
                                    logger.warning(f"NQ Validation Failed: {val_name} value {val} is not 5 digits.")
                                    is_valid = False
                    
                    if is_valid:
                        out.append({
                            'type': current_type,
                            'timestamp': dt_object.strftime('%m/%d/%Y %I:%M:%S %p'), # Store in consistent format
                            'mid': mid_val,
                            'lower': lower_val,
                            'upper': upper_val,
                        })
                except (ValueError, AttributeError) as e:
                    logger.warning(f"Failed to parse ticker data or timestamp for {ticker_type} block: {block_text}. Error: {e}")
                    continue

        # Deduplicate: only keep the latest ticker for each type
        latest_tickers = {}
        for ticker in out:
            ticker_type = ticker['type']
            timestamp = ticker['timestamp']
            
            # Parse the timestamp for comparison
            try:
                dt = datetime.strptime(timestamp, '%m/%d/%Y %I:%M:%S %p')
            except ValueError:
                try:
                    dt = datetime.strptime(timestamp, '%m/%d/%Y %I:%M %p')
                except ValueError:
                    logger.warning(f"Could not parse timestamp: {timestamp}")
                    continue
            
            # Keep only the latest ticker for each type
            if ticker_type not in latest_tickers or dt > latest_tickers[ticker_type]['parsed_dt']:
                latest_tickers[ticker_type] = {
                    'ticker': ticker,
                    'parsed_dt': dt
                }
        
        # Return only the latest ticker of each type
        return [info['ticker'] for info in latest_tickers.values()]
