# MCP Multi-Engine OCR Test Plan

Date: 2025-11-07

Purpose
- Systematically evaluate multiple OCR engines (DeepSeek, Tesseract, TensorFlow, PaddleOCR) against the same Discord screenshots to identify which engine reliably extracts ticker text from Discord’s white-on-dark styling.

Prereqs
- rovodev.yml configured (done).
- MCP client/runner installed (e.g., Rovo Dev Studio or compatible MCP runner) and restarted so servers in rovodev.yml are active.
- This repository available locally.

Test Inputs
- We will prepare a curated set of recent screenshots from:
  - screenshots/
  - .playwright-mcp/
  - debug_screenshots/
- A helper script will copy the latest N images into mcp_test_inputs/ and produce a manifest mcp_test_manifest.json

Steps
1) Prepare test images and manifest:
   - Activate venv (optional but recommended)
   - Run:
     python mcp_ocr_prepare_inputs.py --max 12
   - Output:
     - mcp_test_inputs/ (copied images)
     - mcp_test_manifest.json (list of files with timestamps)

2) Run OCR engines via MCP on each input image:
   - In your MCP client/runner, select each engine:
     - DeepSeek-OCR Docs
     - tesseract Docs
     - tensorflow-ocr Docs
     - PaddleOCR Docs
   - For each engine and each image in mcp_test_inputs/:
     - Perform OCR (use the engine’s default OCR method; for Tesseract, ensure psm/osd suitable for scene text)
     - Save the raw extracted text to mcp_test_results.json under the schema defined in mcp_test_results.json.example
     - If the engine provides word boxes instead of a single string, join lines into a best-effort text block per image.

3) Evaluate and compare results:
   - Run:
     python mcp_ocr_eval_results.py --results mcp_test_results.json
   - The evaluator will parse each engine’s raw text using the project’s ticker parsers and output metrics:
     - Count of parsed tickers, by type (NQ/ES/YM/RTY/CL)
     - Latest timestamp per type successfully parsed
     - Sample of matched entries
   - A summary table and per-engine diagnostics will be printed.

4) Decide next integration step:
   - If a non-Paddle engine succeeds consistently, integrate it as a fallback in main.py’s OCR chain.
   - If multiple engines succeed, choose the most stable/accurate by the metrics and manual spot checks.

Artifacts
- mcp_test_inputs/               # curated input images
- mcp_test_manifest.json         # list of images with metadata
- mcp_test_results.json          # raw OCR outputs (to be filled by you via MCP)
- mcp_test_results.json.example  # schema + example

Notes
- This test isolates OCR correctness from browser automation. If needed, re-run main.py or check_latest_messages.py to refresh screenshots, then re-run the input preparation step.
- You can increase --max to broaden coverage.
- If an engine crashes or returns nothing, leave its text empty for that image in the results JSON; the evaluator will report zeros for parsed entries.

Next Actions after evaluation
- Update 2-WHERE AM I UPTO.md and 11-CHANGE LOG.md with the winning engine choice and observed accuracy.
- Integrate the engine as a fallback (or primary) in main.py and/or EnhancedOCR.
