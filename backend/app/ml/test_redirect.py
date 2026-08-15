from backend.app.services.redirect_analyzer import (
    analyze_redirects
)


print("\n=================================================================")
print("       SCAMINTEL AI — URL REDIRECT ANALYZER")
print("=================================================================")

test_urls = [

    "https://example.com",

    "http://127.0.0.1:8080/redirect/1",

    "http://127.0.0.1:8080/redirect/3",

]


for url in test_urls:

    print("\nURL:")
    print(url)

    result = analyze_redirects(
        url
    )

    print(
        "Redirect Detected:",
        result["redirect_detected"]
    )

    print(
        "Redirect Count:",
        result["redirect_count"]
    )

    print(
        "Original Domain:",
        result["original_domain"]
    )

    print(
        "Final Domain:",
        result["final_domain"]
    )

    print(
        "Domain Changed:",
        result["domain_changed"]
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

    print("\nRedirect Chain:")

    for item in result[
        "redirect_chain"
    ]:

        print(
            " •",
            item["url"],
            "→",
            item["status_code"]
        )

    print("\nIndicators:")

    if result["indicators"]:

        for indicator in result[
            "indicators"
        ]:

            print(
                " •",
                indicator
            )

    else:

        print(
            " • None"
        )


print("\n=================================================================")
print("       REDIRECT ANALYSIS TEST COMPLETE")
print("=================================================================")