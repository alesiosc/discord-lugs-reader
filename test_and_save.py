import os
import glob
from browser_detector import DiscordBrowserDetector

def test_and_save():
    """Test the OCR extraction and save results to snapshot.txt"""
    # Prefer a known good debug full-page screenshot for smoke testing
    debug_candidates = glob.glob("debug_screenshots/full_page_*.png")
    if debug_candidates:
        latest_file = max(debug_candidates, key=os.path.getctime)
        print(f"Testing with debug full-page file: {latest_file}")
    else:
        # Fallback to the most recent PNG file in the .playwright-mcp directory
        png_files = glob.glob(".playwright-mcp/*.png")
        if not png_files:
            print("No PNG files found in debug_screenshots or .playwright-mcp directory")
            return
        latest_file = max(png_files, key=os.path.getctime)
        print(f"Testing with file: {latest_file}")
    
    # Extract ticker data using the detector class
    detector = DiscordBrowserDetector()
    ticker_data = detector.extract_ticker_data_with_ocr(latest_file)
    
    print(f"\nFound {len(ticker_data)} ticker messages:")
    for item in ticker_data:
        print(f"  - {item['type']}: {item['timestamp']} (Mid: {item['mid']}, Lower: {item['lower']}, Upper: {item['upper']})")
    
    # Save to snapshot.txt
    detector.save_to_snapshot(ticker_data)
    print("\nSnapshot saved to snapshot.txt")

if __name__ == "__main__":
    test_and_save()