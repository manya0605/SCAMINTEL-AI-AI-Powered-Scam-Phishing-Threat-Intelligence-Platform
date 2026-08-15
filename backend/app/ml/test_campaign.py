from backend.app.services.campaign_detector import (
    analyze_campaign
)


print("\n==============================================")
print("       SCAMINTEL AI — CAMPAIGN DETECTOR")
print("==============================================")


# ------------------------------------------------------------
# CURRENT MESSAGE
# ------------------------------------------------------------

current_message = (
    "Your PayPal account requires urgent verification. "
    "Visit https://paypa1.com immediately."
)


# ------------------------------------------------------------
# PREVIOUS MESSAGES
# ------------------------------------------------------------

previous_messages = [

    (
        "Urgent! Your PayPal account requires verification. "
        "Visit https://paypa1.com immediately."
    ),

    (
        "Congratulations! You won a prize. "
        "Claim it at https://example.com"
    ),

    (
        "Your bank account requires verification. "
        "Please login immediately."
    )

]


# ------------------------------------------------------------
# ANALYZE CAMPAIGN
# ------------------------------------------------------------

result = analyze_campaign(
    current_message=current_message,
    previous_messages=previous_messages
)


# ------------------------------------------------------------
# DISPLAY RESULT
# ------------------------------------------------------------

print("\n==============================================")
print("          CAMPAIGN ANALYSIS")
print("==============================================")


print(
    "Campaign Detected:",
    result["campaign_detected"]
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
    "Highest Similarity:",
    result["highest_similarity"],
    "%"
)

print(
    "Messages Analyzed:",
    result["messages_analyzed"]
)


print("\nCurrent Indicators:")

for indicator in result[
    "current_indicators"
]:

    print(
        " •",
        indicator
    )


print("\nMatching Messages:")


if result["matching_messages"]:

    for match in result[
        "matching_messages"
    ]:

        print(
            "\n • Message Index:",
            match["message_index"]
        )

        print(
            "   Similarity:",
            match["similarity"],
            "%"
        )

        print(
            "   Shared Indicators:"
        )

        for indicator in match[
            "shared_indicators"
        ]:

            print(
                "    -",
                indicator
            )

else:

    print(
        " • No matching campaigns detected."
    )


print("\n==============================================")
print("       CAMPAIGN TEST COMPLETE")
print("==============================================")