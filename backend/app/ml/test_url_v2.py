from backend.app.services.url_analyzer import analyze_urls_in_message


TEST_MESSAGES = [

    (
        "SHORTENER",
        "Claim your reward: https://bit.ly/abc123"
    ),

    (
        "IP ADDRESS",
        "Verify your account: http://192.0.2.10/login"
    ),

    (
        "SUSPICIOUS LOOKALIKE",
        "Secure your account: https://paypa1-login.example.com/verify"
    ),

    (
        "NORMAL EXAMPLE",
        "Visit https://example.com for information."
    ),
]


print("\n==============================================")
print("       SCAMINTEL AI — URL INTELLIGENCE V2")
print("==============================================")


for name, message in TEST_MESSAGES:

    print("\n\n==============================================")
    print(name)
    print("==============================================")

    print("Message:")
    print(message)

    result = analyze_urls_in_message(message)

    for item in result["results"]:

        print("\nURL:", item["url"])
        print("Domain:", item["domain"])

        print(
            "Risk:",
            item["risk_level"]
        )

        print(
            "Score:",
            item["risk_score"],
            "/ 100"
        )

        print(
            "HTTPS:",
            item["https"]
        )

        print(
            "Shortener:",
            item["url_shortener"]
        )

        print(
            "IP Address:",
            item["ip_address"]
        )

        print(
            "Brand Matches:",
            item["brand_matches"]
        )

        print("\nIndicators:")

        if item["indicators"]:

            for indicator in item["indicators"]:
                print(" •", indicator)

        else:

            print(" • None")

        print("\nCharacter Features:")

        for key, value in item[
            "character_features"
        ].items():

            print(
                f" • {key}: {value}"
            )


print("\n==============================================")
print("URL V2 TEST COMPLETE")
print("==============================================")