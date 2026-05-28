import easyocr
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('minimal_ocr_test.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

def test_readtext():
    """
    A minimal test to see if easyocr.readtext is the point of failure.
    """
    # Use a real screenshot path from the previous logs
    image_path = "screenshots\\page-2025-11-09T14:07:43-202438Z.png"
    
    logging.info(f"--- MINIMAL OCR TEST STARTING ---")
    logging.info(f"Using image: {image_path}")
    
    try:
        logging.info("Initializing EasyOCR Reader...")
        reader = easyocr.Reader(['en'])
        logging.info("Reader initialized successfully.")
        
        logging.info(f"Calling reader.readtext() on {image_path}...")
        # This is the line that is suspected to be crashing
        text_blocks = reader.readtext(image_path, detail=1)
        logging.info("reader.readtext() call completed successfully!")
        
        if text_blocks:
            logging.info(f"Successfully extracted {len(text_blocks)} text blocks.")
            for i, block in enumerate(text_blocks):
                logging.info(f"  - Block {i}: '{block[1]}'")
        else:
            logging.warning("readtext() returned no blocks, but did not crash.")
            
    except Exception as e:
        logging.error(f"An exception occurred during the test: {e}", exc_info=True)
        
    logging.info("--- MINIMAL OCR TEST FINISHED ---")

if __name__ == "__main__":
    test_readtext()