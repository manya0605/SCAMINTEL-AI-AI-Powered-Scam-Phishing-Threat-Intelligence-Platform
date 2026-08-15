from backend.app.services.impersonation_detector import (
    detect_impersonation
)


TEST_MESSAGES = [

    "Your bank security team detected suspicious activity. Verify your account immediately.",

    "Your account will be blocked. Share your OTP with our bank support team.",

    "Government tax department notice: verify your details immediately.",

    "Your delivery support team needs your payment information to release your package.",

    "Instagram security team: verify your account immediately or it will be suspended.",

    "Hey, are you free for lunch today?",
]


print("\n=================================================================")
print("       SCAMINTEL AI — IMPERSONATION DETECTOR")
print("=================================================================")


for message in TEST_MESSAGES:

    result = detect_impersonation(
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
        "Credential Request:",
        result["credential_request"]
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
        "URL Detected:",
        result["url_detected"]
    )

    print(
        "Indicators:",
        result["indicators"]
    )


print("\n=================================================================")
print("       IMPERSONATION TEST COMPLETE")
print("=================================================================")