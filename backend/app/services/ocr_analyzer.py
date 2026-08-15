import easyocr
from PIL import Image


# ============================================================
# SCAMINTEL OCR ANALYZER
# ============================================================

reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def extract_text_from_image(image_path: str):

    try:

        image = Image.open(image_path)

        results = reader.readtext(
            image_path,
            detail=1
        )

        extracted_text = []

        for result in results:

            text = result[1]

            if text.strip():

                extracted_text.append(
                    text.strip()
                )

        final_text = " ".join(
            extracted_text
        )

        return {
            "success": True,
            "text": final_text,
            "text_blocks": len(
                extracted_text
            )
        }

    except Exception as e:

        return {
            "success": False,
            "text": "",
            "text_blocks": 0,
            "error": str(e)
        }

# ============================================================
# OCR + SCAMINTEL INTEGRATION
# ============================================================

def analyze_screenshot(image_path: str):

    ocr_result = extract_text_from_image(
        image_path
    )

    if not ocr_result["success"]:
        return ocr_result

    extracted_text = ocr_result["text"]

    if not extracted_text.strip():

        return {
            "success": False,
            "text": "",
            "text_blocks": 0,
            "error": "No readable text detected in screenshot."
        }

    return {
        "success": True,
        "text": extracted_text,
        "text_blocks": ocr_result["text_blocks"]
    }