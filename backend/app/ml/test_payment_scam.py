from backend.app.services.payment_scam_detector import detect_payment_scam


TEST_MESSAGES = [

    "Your UPI account will be blocked. Update your KYC immediately.",

    "Congratulations! You are eligible for a ₹5000 refund. Click the link to claim it.",

    "Please send ₹1 through UPI to verify your account.",

    "Share your UPI PIN and OTP to receive your cashback.",

    "Hey, are you free for lunch today?",

]


print("\n" + "=" * 65)
print("       SCAMINTEL AI — PAYMENT SCAM DETECTOR")
print("=" * 65)


for message in TEST_MESSAGES:

    result = detect_payment_scam(message)

    print("\nMessage:")
    print(message)

    print("\nDetected:", result["detected"])

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
        "Indicators:",
        result["indicators"]
    )


print("\n" + "=" * 65)
print("PAYMENT SCAM TEST COMPLETE")
print("=" * 65)