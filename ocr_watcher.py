print("Starting ocr_watcher.py...")
import time
import os
import subprocess
import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ocr_watcher.log', mode='w'),
        logging.StreamHandler()
    ]
)

def watch_for_requests():
    """
    Watches for ocr.request files and triggers the OCR process.
    """
    logging.info("OCR Watcher started. Waiting for requests...")
    request_file_path = Path("ocr.request")
    response_file_path = Path("ocr.response")
    
    while True:
        try:
            # Add debug logging every 30 seconds to show it's alive
            current_time = time.time()
            if not hasattr(watch_for_requests, 'last_debug_time'):
                watch_for_requests.last_debug_time = current_time
            
            if current_time - watch_for_requests.last_debug_time > 30:
                logging.info(f"OCR Watcher alive. Checking for request file: {request_file_path}")
                watch_for_requests.last_debug_time = current_time
            
            if request_file_path.exists():
                logging.info("Request file found. Processing...")
                
                # Read the image path from the request file
                with open(request_file_path, 'r') as f:
                    image_path = f.read().strip()
                
                logging.info(f"Request contains image path: {image_path}")
                
                if not Path(image_path).exists():
                    logging.error(f"Image path from request file does not exist: {image_path}")
                    # Clean up and continue
                    request_file_path.unlink()
                    continue

                # Run the OCR script as a subprocess
                # Use sys.executable to ensure we use the same Python environment that launched this script
                python_executable = sys.executable
                ocr_script_path = "run_ocr.py"
                command = [python_executable, ocr_script_path, image_path]
                
                logging.info(f"Running command: {' '.join(command)}")
                process = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                # Log stdout and stderr from the subprocess
                if process.stdout:
                    logging.info(f"OCR subprocess stdout:\n{process.stdout}")
                if process.stderr:
                    logging.warning(f"OCR subprocess stderr:\n{process.stderr}")

                if process.returncode != 0:
                    logging.error(f"OCR subprocess failed with exit code {process.returncode}")
                    # Write an empty response
                    with open(response_file_path, 'w') as f:
                        f.write("[]")
                else:
                    # Write the successful JSON output to the response file
                    logging.info("OCR subprocess successful. Writing response file.")
                    with open(response_file_path, 'w') as f:
                        f.write(process.stdout)
                
                # Clean up the request file
                request_file_path.unlink()
                logging.info("Request processed. Waiting for next request.")

            # Wait for a short interval before checking again
            time.sleep(1)
            
        except Exception as e:
            logging.error(f"An error occurred in the watcher loop: {e}")
            # Clean up request file if it exists to prevent getting stuck
            if request_file_path.exists():
                try:
                    request_file_path.unlink()
                except Exception as cleanup_e:
                    logging.error(f"Failed to clean up request file after error: {cleanup_e}")
            time.sleep(5) # Wait a bit longer after an error

if __name__ == "__main__":
    watch_for_requests()
