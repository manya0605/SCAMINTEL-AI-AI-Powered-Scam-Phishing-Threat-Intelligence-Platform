from backend.app.services.lookalike_detector import (
    detect_lookalike
)


TEST_URLS = [

    "https://paypal.com",

    "https://paypa1.com",

    "https://paypal-login.com",

    "https://micros0ft.com",

    "https://apple-security.com",

    "https://google.com",

    "https://example.com",

    "https://faceb00k-login.com",

]


print("\n=================================================================")
print("       SCAMINTEL AI — LOOK-ALIKE / HOMOGRAPH DETECTOR")
print("=================================================================")


for url in TEST_URLS:

    result = detect_lookalike(url)

    print("\nURL:")
    print(url)

    print(
        "Detected:",
        result["detected"]
    )

    print(
        "Risk Score:",
        result["risk_score"],
        "/ 100"
    )

    print(
        "Risk Level:",
        result["risk_level"]
    )

    print(
        "Normalized Domain:",
        result["normalized_domain"]
    )

    print(
        "Brand Matches:",
        result["brand_matches"]
    )

    print(
        "Similarity:",
        result["similarity"],
        "%"
    )

    print("Indicators:")

    if result["indicators"]:

        for indicator in result["indicators"]:

            print(
                " •",
                indicator
            )

    else:

        print(" • None")


print("\n=================================================================")
print("       LOOK-ALIKE DETECTOR TEST COMPLETE")
print("=================================================================")