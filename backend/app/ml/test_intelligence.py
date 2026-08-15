from backend.app.services.scam_intelligence import analyze_message


message = """
Congratulations! You have won Rs 5 lakh in our special lottery.
Send your bank account details immediately to claim your prize.
"""


result = analyze_message(
    text=message,
    ml_prediction="smish",
    ml_confidence=0.9432
)


print("\n===================================")
print("       SCAMINTEL AI")
print("   THREAT INTELLIGENCE ENGINE")
print("===================================")

print("\nThreat Level:", result["threat_level"])

print("Risk Score:", result["risk_score"], "/ 100")

print("\nScam Categories:")

for category in result["scam_categories"]:
    print(" •", category)

print("\nRisk Indicators:")

for indicator in result["risk_indicators"]:
    print(" •", indicator)

print("\nURLs Detected:")

if result["urls_detected"]:
    for url in result["urls_detected"]:
        print(" •", url)
else:
    print(" • None")