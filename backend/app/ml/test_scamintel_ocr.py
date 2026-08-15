from backend.app.services.ocr_analyzer import (
    analyze_screenshot
)

from backend.app.ml.scamintel_analyzer import (
    analyze_with_scamintel
)


print("\n==============================================")
print("       SCAMINTEL AI — OCR SCAM ANALYZER")
print("==============================================")


image_path = input(
    "\nEnter screenshot path: "
).strip()


# ============================================================
# 1. OCR SCREENSHOT
# ============================================================

ocr_result = analyze_screenshot(
    image_path
)


if not ocr_result["success"]:

    print("\nOCR ERROR:")

    print(
        ocr_result["error"]
    )

    raise SystemExit


# ============================================================
# 2. DISPLAY OCR TEXT
# ============================================================

print("\n==============================================")
print("              OCR EXTRACTED TEXT")
print("==============================================")

print(
    ocr_result["text"]
)

print(
    "\nText Blocks:",
    ocr_result["text_blocks"]
)


# ============================================================
# 3. SCAMINTEL ANALYSIS
# ============================================================

print("\n==============================================")
print("          SCAMINTEL ANALYSIS")
print("==============================================")


result = analyze_with_scamintel(
    ocr_result["text"]
)


# ============================================================
# 4. DISPLAY FINAL RESULT
# ============================================================

print("\n==============================================")
print("          SCAMINTEL FINAL RESULT")
print("==============================================")


print(result)


print("\n==============================================")
print("       OCR SCAM ANALYSIS COMPLETE")
print("==============================================")