import easyocr
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(text, filename="test_image.png"):
    """Creates a simple image with the given text."""
    img_size = (800, 200)
    img = Image.new('RGB', img_size, color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    
    try:
        # Try to use a common font, or default to a generic one
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        print("Could not load arial.ttf, using default font.")

    text_color = (0, 0, 0)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img_size[0] - text_width) / 2
    y = (img_size[1] - text_height) / 2
    d.text((x, y), text, fill=text_color, font=font)
    img.save(filename)
    print(f"Created test image: {filename}")
    return filename

def run_easyocr_on_image(image_path):
    """Runs EasyOCR on the specified image and prints the results."""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    
    print(f"\n--- EasyOCR Results for {image_path} ---")
    if result:
        for (bbox, text, prob) in result:
            print(f"Text: {text}, Confidence: {prob:.2f}")
    else:
        print("No text detected.")
    print("--------------------------------------")

if __name__ == "__main__":
    test_text = "[ES] Published Level: Timestamp: 11/10/2025 2:28:00 PM, Mid: 6850, Lower: 6793.75, Upper: 6906.25"
    image_file = create_test_image(test_text)
    run_easyocr_on_image(image_file)

    print("\nAttempting OCR on a real screenshot (if available)...")
    # Replace with a path to one of your actual screenshots if you want to test it
    # For example: "screenshots/page-2025-11-11T15-12-45-161794Z.png"
    real_screenshot_path = "screenshots/page-2025-11-11T15-12-45-161794Z.png" 
    if os.path.exists(real_screenshot_path):
        run_easyocr_on_image(real_screenshot_path)
    else:
        print(f"Real screenshot not found at {real_screenshot_path}. Skipping test.")
