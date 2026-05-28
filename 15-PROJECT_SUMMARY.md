# Project Summary: Discord Lugs Reader

This document provides a comprehensive overview of the work done on the Discord Lugs Reader project, including what has been accomplished, what issues have been encountered, and the plan for moving forward.

## Project Goal

The primary goal of this project is to create an automated system that can:

1.  Monitor a specific Discord channel for new messages containing stock ticker information.
2.  Take screenshots of these messages.
3.  Use Optical Character Recognition (OCR) to extract the ticker data from the screenshots.
4.  Parse the extracted data to identify the ticker symbol, timestamp, and associated values (Mid, Lower, Upper).
5.  Send the parsed data to a Discord webhook.

## High-Level Architecture

The system is designed to run as two separate, concurrent processes:

1.  **`main.py` (The "Reader"):**
    *   Uses the Playwright library to launch a browser and navigate to the specified Discord channel.
    *   Periodically takes screenshots of the message area.
    *   Communicates with the OCR process by creating an `ocr.request` file containing the path to the screenshot.
    *   Waits for an `ocr.response` file to be created by the OCR process.
    *   Reads the extracted data from the `ocr.response` file, parses it, and sends it to the configured Discord webhook.

2.  **`ocr_watcher.py` (The "Watcher"):**
    *   Continuously monitors the file system for the creation of an `ocr.request` file.
    *   When a request is found, it launches a subprocess (`run_ocr.py`) to perform OCR on the specified screenshot.
    *   Captures the output of the OCR process and writes it to an `ocr.response` file.

This two-process architecture was chosen to prevent the OCR process from blocking the main browser automation thread, which could lead to timeouts and other issues.

## What Has Worked

*   **Browser Automation:** The `main.py` script is successfully launching a browser, navigating to the correct Discord channel, and taking screenshots of the message area.
*   **Inter-Process Communication:** The file-based communication system between `main.py` and `ocr_watcher.py` is functioning correctly. `main.py` creates `ocr.request` files, and `ocr_watcher.py` detects them and creates `ocr.response` files.
*   **OCR Library Change:** We successfully switched from PaddleOCR to EasyOCR in the `enhanced_ocr.py` script. This was done because PaddleOCR was not extracting any text, and EasyOCR is generally considered easier to set up and use.
*   **JSON Parsing Fix:** We identified and fixed an issue where the `ocr.response` file contained non-JSON text, which was causing the `main.py` script to fail when parsing the response. This was caused by a debug `print` statement in `enhanced_ocr.py`, which has now been removed.

## What Hasn't Worked (and Why)

The core issue that we are currently facing is that **EasyOCR is not extracting any text from the screenshots.**

Here's a detailed breakdown of the problem and the debugging steps taken:

1.  `main.py` takes a screenshot and creates an `ocr.request` file.
2.  `ocr_watcher.py` detects the request and runs `run_ocr.py` as a subprocess.
3.  `run_ocr.py` calls `enhanced_ocr.py` to perform OCR on the screenshot.
4.  `enhanced_ocr.py` uses the EasyOCR library to extract text from the image.

**The Problem:** Despite switching to EasyOCR, the `ocr_watcher.log` consistently shows `OCR subprocess stdout: []`. This indicates that the `run_ocr.py` script, and by extension `enhanced_ocr.py`, is not outputting any recognized text to standard output.

**Debugging Steps and Observations:**

*   **Initial JSON Parsing Errors:** Previously, `main.py` was failing to decode JSON from the `ocr.response` file. This was traced back to:
    *   `print()` statements in `enhanced_ocr.py` that were polluting the `stdout` of `run_ocr.py`.
    *   Extraneous log messages from `run_ocr.py` itself being directed to `stdout`.
    *   **Fixes:** These were addressed by:
        *   Replacing `print()` with `logger.info()` in `enhanced_ocr.py`.
        *   Modifying `run_ocr.py` to direct all logging to `ocr_subprocess.log` and *only* print the final JSON output to `stdout`.
        *   Adjusting `main.py` to search for the start of the JSON array (`[`) in the `ocr.response` content, ignoring any preceding non-JSON text.
    *   **Result:** These fixes successfully resolved the JSON decoding errors in `main.py`. However, `main.py` now reports "OCR response contained no data" because the JSON it receives is an empty array (`[]`).

*   **EasyOCR Not Extracting Text:** The current problem is that EasyOCR itself is not detecting any text in the images. The `ocr_watcher.log` confirms this by showing `OCR subprocess stdout: []` for every OCR request. The `stderr` from EasyOCR shows warnings about "Neither CUDA nor MPS are available - defaulting to CPU," but these are not critical errors and simply indicate that EasyOCR is running on the CPU, which is expected if a GPU is not configured.

**Current Hypothesis:** My hypothesis is that there is an issue with how EasyOCR is being initialized or used, or that there is a problem with the quality or characteristics of the images being fed to it. The fact that it is not throwing any errors, but simply returning no text, is unusual.

## Tools Used

*   **Python:** The primary programming language for the project.
*   **Playwright:** A Python library for browser automation.
*   **EasyOCR:** A Python library for Optical Character Recognition.
*   **Pillow:** A Python library for image manipulation.
*   **OpenCV:** A Python library for computer vision (used for image preprocessing).
*   **`logging`:** The standard Python library for logging.
*   **`dotenv`:** A Python library for managing environment variables.

## Next Steps

To diagnose and fix the current issue, I propose the following plan:

1.  **Isolate and Verify EasyOCR:** I will create a simple, standalone Python script (`test_easyocr_direct.py`) that does nothing but:
    *   Create a clean, simple test image with known text.
    *   Run EasyOCR on that test image.
    *   Run EasyOCR on one of the actual screenshots taken by `main.py`.
    This will allow us to determine if EasyOCR is working at all in your environment, and if it is capable of reading the text in the screenshots.

2.  **Analyze Screenshots:** I will ask you to provide one of the screenshots that `main.py` has taken, so that I can examine it and see if there are any visual issues that might be preventing EasyOCR from working.

3.  **Improve Image Preprocessing:** If the screenshots are of low quality, or if EasyOCR is struggling with the colors or fonts, I will add image preprocessing steps to `enhanced_ocr.py` to improve the image quality before it is sent to EasyOCR. This could include:
    *   Converting the image to grayscale.
    *   Increasing the contrast.
    *   Resizing the image.

By following this plan, I am confident that we can identify the root cause of the OCR failure and get the project working as intended.
