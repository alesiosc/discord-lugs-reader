from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_test_image(text, filename="test_ocr_image.png"):
    """Creates a simple PNG image with the given text."""
    img_path = Path("screenshots") / filename
    
    # Create a blank image with a white background
    img = Image.new('RGB', (600, 200), color = (255, 255, 255))
    d = ImageDraw.Draw(img)

    # Try to load a default font, or use a generic one
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        print("Using default font as arial.ttf not found.")

    # Draw text in black
    d.text((50,50), text, fill=(0,0,0), font=font)
    
    img.save(img_path)
    print(f"Created test image: {img_path}")
    return str(img_path)

if __name__ == "__main__":
    create_test_image("NQ Timestamp: 11/08/2025 07:00:00 PM Mid: 123.45 Lower: 120.00 Upper: 125.00")
