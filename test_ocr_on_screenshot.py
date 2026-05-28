
import os
from pathlib import Path
import logging
from enhanced_ocr import EnhancedOCR
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_ocr_on_latest_screenshot():
    """
    Finds the most recent screenshot in the 'screenshots' directory
    and runs the EnhancedOCR extraction on it.
    """
    load_dotenv()
    
    try:
        # Find the latest screenshot
        screenshot_dir = Path('screenshots')
        if not screenshot_dir.exists():
            logging.error("The 'screenshots' directory does not exist.")
            return

        # Use the specific test image
        latest_screenshot = Path("screenshots") / "test_ocr_image.png"
        if not latest_screenshot.exists():
            logging.error(f"Test image {latest_screenshot} not found. Please run create_test_image.py first.")
            return
        logging.info(f"Using test image: {latest_screenshot}")

        # Initialize OCR
        logging.info("Initializing EnhancedOCR...")
        try:
            ocr_engine = EnhancedOCR(timeout_seconds=60)
            logging.info("EnhancedOCR initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize EnhancedOCR: {e}")
            return

        # Run OCR extraction
        logging.info(f"Running OCR extraction on {latest_screenshot}...")
        extracted_data = []
        try:
            extracted_data = ocr_engine.extract_ticker_data(str(latest_screenshot))
        except Exception as e:
            logging.error(f"Error during OCR extraction: {e}")
            import traceback
            logging.error(f"Full traceback: {traceback.format_exc()}")

        # Print results
        if not extracted_data:
            logging.warning("--- OCR RESULT: NO VALID STRINGS EXTRACTED ---")
        else:
            logging.info("--- OCR RESULT: SUCCESSFULLY EXTRACTED STRINGS ---")
            for item in extracted_data:
                print(item)

    except Exception as e:
        logging.error(f"An error occurred during the OCR test: {e}")

if __name__ == "__main__":
    test_ocr_on_latest_screenshot()
