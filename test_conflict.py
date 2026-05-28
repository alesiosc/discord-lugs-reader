
import logging
import sys

# Configure logging to a file and to stdout
log_file = 'conflict_test.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("--- Conflict Test Start ---")

try:
    logging.info("Attempting to import EasyOCR...")
    import easyocr
    logging.info("Successfully imported EasyOCR.")
    
    logging.info("Attempting to initialize EasyOCR Reader...")
    reader = easyocr.Reader(['en'])
    logging.info("Successfully initialized EasyOCR Reader.")

    logging.info("Attempting to import Playwright...")
    from playwright.async_api import async_playwright
    logging.info("Successfully imported Playwright.")
    
    logging.info("--- Conflict Test Finished Successfully! ---")

except Exception as e:
    logging.error(f"An error occurred during the conflict test: {e}")
    import traceback
    logging.error(f"Full traceback: {traceback.format_exc()}")

logging.info("--- Conflict Test End ---")
