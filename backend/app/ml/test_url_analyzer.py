from backend.app.services.url_analyzer import (
    analyze_urls_in_message
)


print("\n===================================")
print("       SCAMINTEL AI")
print("        URL ANALYZER")
print("===================================")


# SAFE SYNTHETIC TEST URL
message = """
Your account needs verification.
Visit https://paypa1.com
to continue.
"""


result = analyze_urls_in_message(message)


print("\nURLs detected:", result["urls_detected"])

print(
    "Overall URL Risk:",
    result["overall_risk"]
)

print(
    "Highest Risk Score:",
    result["highest_risk"],
    "/ 100"
)


for item in result["results"]:

    print("\n-----------------------------------")

    print("URL:", item["url"])

    print(
        "Domain:",
        item["domain"]
    )

    print(
        "Risk Level:",
        item["risk_level"]
    )

    print(
        "Risk Score:",
        item["risk_score"],
        "/ 100"
    )

    print(
        "HTTPS:",
        item["https"]
    )

    print(
        "URL Shortener:",
        item["url_shortener"]
    )

    print(
        "IP Address:",
        item["ip_address"]
    )

    print("\nIndicators:")

    if item["indicators"]:

        for indicator in item["indicators"]:
            print(" •", indicator)

    else:

        print(" • None")


print("\n===================================")