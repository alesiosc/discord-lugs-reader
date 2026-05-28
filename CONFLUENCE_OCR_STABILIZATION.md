# Discord OCR Stabilization – Pipelines, Tests, and Results

Summary
- Objective: Reliably extract ticker text from Discord screenshots with minimal operator steps.
- Status: EnhancedOCR integrated as primary with multi-pipeline, multi-scale preprocessing; tolerant parsing; standardized PaddleOCR initialization; offline and batch test harnesses in place.

Pipelines implemented
1) Inverted Otsu
2) Adaptive (non-inverted) + bilateral denoise + dilation
3) CLAHE + Otsu
- Scales per pipeline: 1.0, 1.5, 2.0, 3.0
- Fallback: raw image

Parsing improvements
- Normalized punctuation/spacing, support for numbers with commas.
- Replacement of common OCR confusions (e.g., Timestarnp -> Timestamp).

Test harnesses
- tmp_rovodev_run_once_offline.py: single latest screenshot, raw → bottom-crop, logs to tmp_rovodev_offline_ocr.txt
- tmp_rovodev_batch_enh_ocr_v2.py: batch test latest N screenshots with multiple crop heights, logs to tmp_rovodev_batch_ocr_log.txt
- tmp_rovodev_multi_ocr_local_1.py: quick multi-prep test

Results (to be updated)
- One-off offline run: no parse on RAW and 700px bottom crop (pre-enhancements). Running enhanced batch now.
- Batch run summary: TBA
- Winning pipeline: TBA

Next steps
- Lock winning pipeline order in EnhancedOCR.
- Verify on live flow (main.py) for 1–2 cycles.
- Document examples and edge cases.

Appendix: File references
- enhanced_ocr.py (pipelines, normalization, parsing)
- main.py (integration and fallback)
- tmp_rovodev_* scripts (tests)
