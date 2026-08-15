from backend.app.services.prize_scam_detector import (
    detect_prize_scam
)


TEST_MESSAGES = [

    "Congratulations! You have won Rs 5 lakh in our special lottery. Claim your prize immediately.",

    "You have been selected as a lucky winner. Pay a processing fee to receive your prize.",

    "Claim your reward today only by visiting https://example.com",

    "Share your OTP and bank account details to receive your lottery prize.",

    "Hey, are you free for lunch today?",

]


print("\n=================================================================")
print("       SCAMINTEL AI — PRIZE / LOTTERY SCAM DETECTOR")
print("=================================================================")


for message in TEST_MESSAGES:

    result = detect_prize_scam(
        message
    )

    print("\nMessage:")
    print(message)

    print(
        "\nDetected:",
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
        "Categories:",
        result["categories"]
    )

    print(
        "Urgency:",
        result["urgency_detected"]
    )

    print(
        "Payment Request:",
        result["payment_request"]
    )

    print(
        "Credential Request:",
        result["credential_request"]
    )

    print(
        "URL Detected:",
        result["url_detected"]
    )

    print(
        "Indicators:",
        result["indicators"]
    )


print("\n=================================================================")
print("       PRIZE / LOTTERY TEST COMPLETE")
print("=================================================================")