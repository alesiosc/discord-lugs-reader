
import easyocr
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_easyocr_test():
    """
    A minimal script to test EasyOCR in isolation.
    """
    try:
        image_path = str(Path("screenshots") / "test_ocr_image.png")
        logging.info(f"Using test image: {image_path}")

        # 1. Initialize EasyOCR Reader
        # This will download the model on the first run
        logging.info("Initializing EasyOCR Reader for English...")
        reader = easyocr.Reader(['en'])
        logging.info("EasyOCR Reader initialized.")

        # 2. Run OCR
        logging.info(f"Calling reader.readtext() on {image_path}...")
        result = reader.readtext(image_path)
        logging.info("readtext() call completed.")

        # 3. Print result
        logging.info("--- EASYOCR RESULT ---")
        if not result:
            logging.warning("No text found.")
        else:
            for (bbox, text, prob) in result:
                print(f'Text: "{text}", Probability: {prob:.4f}')

    except Exception as e:
        logging.error(f"An error occurred in EasyOCR test: {e}")
        import traceback
        logging.error(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    run_easyocr_test()
