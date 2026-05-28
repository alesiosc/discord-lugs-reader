
import sys
import json
from enhanced_ocr import EnhancedOCR

def main():
    """
    Standalone script to run EasyOCR on an image file.
    Takes one command-line argument: the path to the image.
    Prints the extracted data as a JSON string to stdout.
    """
    if len(sys.argv) != 2:
        # Can't use logger here, so print to stderr
        print("Usage: python run_ocr.py <image_path>", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    
    try:
        # Initialize the extractor
        ocr_processor = EnhancedOCR()
        
        # Run the OCR and get raw result
        raw_ocr_result = ocr_processor._ocr_with_timeout(image_path)
        
        # Parse text from raw OCR result
        parsed_text = ocr_processor.parse_text(raw_ocr_result)
        print(f"--- RAW PARSED TEXT FROM EASYOCR: {parsed_text} ---", file=sys.stderr)
        
        # Run the OCR and data extraction
        data = ocr_processor.extract_ticker_data_from_text(parsed_text)
        
        # Print the result as a JSON string
        print(json.dumps(data, indent=4))
        
    except Exception as e:
        # Can't use logger here, so print to stderr
        print(f"An error occurred in run_ocr.py: {e}", file=sys.stderr)
        # Print an empty JSON array on error
        print(json.dumps([]))
        sys.exit(1)

if __name__ == "__main__":
    main()
