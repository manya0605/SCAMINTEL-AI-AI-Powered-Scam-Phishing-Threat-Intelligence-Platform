from backend.app.services.ocr_analyzer import (
    extract_text_from_image
)


print("\n==============================================")
print("          SCAMINTEL OCR TEST")
print("==============================================")


image_path = input(
    "\nEnter screenshot path: "
).strip()


result = extract_text_from_image(
    image_path
)


print("\n==============================================")
print("              OCR RESULT")
print("==============================================")


if result["success"]:

    print(
        "Extracted Text:"
    )

    print(
        result["text"]
    )

    print(
        "\nText Blocks:",
        result["text_blocks"]
    )

else:

    print(
        "OCR failed:"
    )

    print(
        result["error"]
    )


print("\n==============================================")
print("              OCR TEST COMPLETE")
print("==============================================")