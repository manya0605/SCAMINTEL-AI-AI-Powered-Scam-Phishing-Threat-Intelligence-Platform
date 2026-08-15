from backend.app.services.url_ml_predictor import predict_url


TEST_URLS = [

    "https://example.com",

    "http://192.0.2.10/login",

    "https://paypa1-login.example.com/verify",

    "https://bit.ly/abc123",

]


print("=" * 60)
print("       SCAMINTEL AI — URL ML MODEL TEST")
print("=" * 60)


for url in TEST_URLS:

    result = predict_url(
        url
    )

    print("\nURL:")
    print(url)

    print(
        "\nPrediction:",
        result["prediction"]
    )

    print(
        "Confidence:",
        f"{result['confidence'] * 100:.2f}%"
    )

    print(
        "Benign Probability:",
        f"{result['benign_probability'] * 100:.2f}%"
    )

    print(
        "Phishing Probability:",
        f"{result['phishing_probability'] * 100:.2f}%"
    )


print("\n" + "=" * 60)
print("URL ML TEST COMPLETE")
print("=" * 60)