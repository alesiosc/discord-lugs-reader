import cv2
from paddleocr import PaddleOCR

def test_paddleocr():
    """Test PaddleOCR with a sample image"""
    try:
                # Initialize PaddleOCR - using English model
        print("Initializing PaddleOCR...")
        ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        print("PaddleOCR initialized successfully")
        
        # List all PNG files in the .playwright-mcp directory
        import os
        import glob
        png_files = glob.glob(".playwright-mcp/*.png")
        if not png_files:
            print("No PNG files found in .playwright-mcp directory")
            return
            
        # Use the most recent PNG file
        latest_file = max(png_files, key=os.path.getctime)
        print(f"Testing with file: {latest_file}")
        
        # Perform OCR on the image
        print("Performing OCR...")
        result = ocr.ocr(latest_file)
        
        # Extract text from OCR results
        text_parts = []
        if result is not None:
            print(f"OCR result type: {type(result)}")
            if isinstance(result, dict):
                # Handle dictionary result
                if 'rec_texts' in result:
                    text_parts = result['rec_texts']
                    print(f"Found {len(text_parts)} text parts in rec_texts")
            elif isinstance(result, list):
                # Handle list result
                print(f"OCR result has {len(result)} elements")
                for i, item in enumerate(result):
                    if item is not None:
                        print(f"Item {i} type: {type(item)}")
                        if isinstance(item, dict) and 'rec_texts' in item:
                            text_parts.extend(item['rec_texts'])
                            print(f"  Found {len(item['rec_texts'])} text parts in item {i}")
                        elif isinstance(item, list):
                            for j, subitem in enumerate(item):
                                if isinstance(subitem, list) and len(subitem) > 1:
                                    text_parts.append(subitem[1][0])  # Extract the text part
                                    print(f"  Subitem {j}: {subitem[1][0]}")
        
        # Join all text parts
        text = ' '.join(text_parts)
        print(f"Extracted text length: {len(text)} characters")
        print(f"Extracted text preview: {text[:1000]}...")
        
    except Exception as e:
        print(f"Error during PaddleOCR test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_paddleocr()