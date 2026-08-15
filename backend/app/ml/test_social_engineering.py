from backend.app.services.social_engineering_detector import (
    detect_social_engineering
)


TEST_MESSAGES = [

    "Your account will be blocked. Act immediately to verify your identity.",

    "This is the bank security officer. Send your OTP immediately.",

    "Congratulations! You have won ₹50,000. Claim your reward today only.",

    "Do not tell anyone. Keep this transaction confidential.",

    "Your family member is in trouble. Please help me immediately.",

    "Hey, are you free for lunch today?",
]


print("\n=================================================================")
print("       SCAMINTEL AI — SOCIAL ENGINEERING DETECTOR")
print("=================================================================")


for message in TEST_MESSAGES:

    result = detect_social_engineering(
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
        "URL Detected:",
        result["url_detected"]
    )

    print(
        "Indicators:",
        result["indicators"]
    )


print("\n=================================================================")
print("       SOCIAL ENGINEERING TEST COMPLETE")
print("=================================================================")