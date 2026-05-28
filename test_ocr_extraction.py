import os
import glob
from browser_detector import extract_ticker_data_with_ocr

def test_ocr_extraction():
    """Test the OCR extraction function with the latest screenshot"""
    # Find the most recent PNG file in the .playwright-mcp directory
    png_files = glob.glob(".playwright-mcp/*.png")
    if not png_files:
        print("No PNG files found in .playwright-mcp directory")
        return
        
    # Use the most recent PNG file
    latest_file = max(png_files, key=os.path.getctime)
    print(f"Testing with file: {latest_file}")
    
    # Extract ticker data
    ticker_data = extract_ticker_data_with_ocr(latest_file)
    
    print(f"\nFound {len(ticker_data)} ticker messages:")
    for item in ticker_data:
        print(f"  - {item['type']}: {item['timestamp']} (Mid: {item['mid']}, Lower: {item['lower']}, Upper: {item['upper']})")

if __name__ == "__main__":
    test_ocr_extraction()