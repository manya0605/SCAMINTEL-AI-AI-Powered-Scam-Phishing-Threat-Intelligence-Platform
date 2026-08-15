from backend.app.services.hybrid_url_risk import (
    calculate_hybrid_url_risk
)


TEST_URLS = [

    "https://example.com",

    "http://192.0.2.10/login",

    "https://paypa1-login.example.com/verify",

    "https://bit.ly/abc123",

]


print("=" * 65)
print("       SCAMINTEL AI — HYBRID URL RISK ENGINE")
print("=" * 65)


for url in TEST_URLS:

    result = calculate_hybrid_url_risk(
        url
    )

    print("\nURL:")
    print(url)

    print(
        "\nML Prediction:",
        result["ml_prediction"]
    )

    print(
        "ML Confidence:",
        f"{result['ml_confidence'] * 100:.2f}%"
    )

    print(
        "Phishing Probability:",
        f"{result['phishing_probability'] * 100:.2f}%"
    )

    print(
        "Rule-Based Score:",
        result["rule_based_score"]
    )

    print(
        "HYBRID RISK SCORE:",
        result["hybrid_risk_score"]
    )

    print(
        "RISK LEVEL:",
        result["risk_level"]
    )

    print(
        "Brand Matches:",
        result["brand_matches"]
    )

    print(
        "Indicators:",
        result["rule_indicators"]
    )


print("\n" + "=" * 65)
print("HYBRID URL TEST COMPLETE")
print("=" * 65)