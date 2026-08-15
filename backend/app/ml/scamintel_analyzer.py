from unittest import result

import joblib
from matplotlib import text

from backend.app.services.scam_intelligence import analyze_message
from backend.app.services.url_analyzer import analyze_urls_in_message
from backend.app.services.payment_scam_detector import detect_payment_scam
from backend.app.services.prize_scam_detector import detect_prize_scam
from backend.app.services.impersonation_detector import detect_impersonation
from backend.app.services.social_engineering_detector import (
    detect_social_engineering
)
from backend.app.services.lookalike_detector import detect_lookalike
from backend.app.services.redirect_analyzer import (
    analyze_redirects
)
from backend.app.services.explainable_ai import generate_explanation
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
from deep_translator import GoogleTranslator
from backend.app.services.campaign_detector import (
    analyze_campaign
)
from backend.app.services.campaign_history import (
    get_previous_messages,
    save_campaign_message
)


MODEL_PATH = "models/message_classifier/scamintel_message_model.joblib"
VECTORIZER_PATH = "models/message_classifier/tfidf_vectorizer.joblib"


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# ============================================================
# MULTILINGUAL LANGUAGE DETECTION
# ============================================================

def detect_message_language(text: str):

    try:

        language = detect(text)

        language_names = {

            "en": "English",
            "hi": "Hindi",
            "kn": "Kannada",
            "ta": "Tamil",
            "te": "Telugu",
            "ml": "Malayalam",
            "bn": "Bengali",
            "mr": "Marathi",
            "gu": "Gujarati",
            "pa": "Punjabi",
            "ur": "Urdu",
            "fr": "French",
            "de": "German",
            "es": "Spanish",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh-cn": "Chinese"
        }

        return {
            "language_code": language,
            "language": language_names.get(
                language,
                language
            )
        }

    except Exception:

        return {
            "language_code": "unknown",
            "language": "Unknown"
        }


# ============================================================
# MULTILINGUAL TEXT NORMALIZATION
# ============================================================

def normalize_for_analysis(
    text: str,
    language_code: str
):

    # English does not need translation
    if language_code == "en":
        return text

    try:

        translated_text = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        return translated_text

    except Exception:

        # Fallback to original text if translation fails
        return text
    

# ============================================================
# MESSAGE ML CLASSIFICATION
# ============================================================


def classify_message(text: str):

    features = vectorizer.transform([text])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    class_probabilities = dict(
        zip(model.classes_, probabilities)
    )

    confidence = max(probabilities)

    return (
        prediction,
        float(confidence),
        class_probabilities
    )


# ============================================================
# FINAL RISK CALCULATION
# ============================================================

def calculate_final_risk(
    message_risk,
    payment_risk,
    prize_risk,
    impersonation_risk,
    social_engineering_risk,
    url_risk,
    lookalike_risk,
    redirect_risk,
    prediction,
    campaign_risk=0
):

    # --------------------------------------------------------
    # BASE RISK
    # --------------------------------------------------------

    risks = [
        message_risk,
        payment_risk,
        prize_risk,
        impersonation_risk,
        social_engineering_risk,
        url_risk,
        lookalike_risk,
        redirect_risk,
        campaign_risk
    ]

    highest_risk = max(risks)


    # --------------------------------------------------------
    # WEIGHTED RISK
    # --------------------------------------------------------

    weighted_score = (
        message_risk * 0.30
        + payment_risk * 0.10
        + prize_risk * 0.10
        + impersonation_risk * 0.10
        + social_engineering_risk * 0.10
        + url_risk * 0.10
        + lookalike_risk * 0.05
        + redirect_risk * 0.05
        + campaign_risk * 0.10
    )


    # --------------------------------------------------------
    # CAMPAIGN BOOST
    # --------------------------------------------------------

    if campaign_risk >= 70:

        weighted_score += 15

    elif campaign_risk >= 40:

        weighted_score += 8


    # --------------------------------------------------------
    # ML SCAM BOOST
    # --------------------------------------------------------

    if prediction == "smish":

        weighted_score += 5


    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    final_score = max(
        weighted_score,
        highest_risk
    )

    final_score = min(
        round(final_score),
        100
    )


    # --------------------------------------------------------
    # THREAT LEVEL
    # --------------------------------------------------------

    if final_score >= 70:

        threat_level = "HIGH"

    elif final_score >= 40:

        threat_level = "MEDIUM"

    else:

        threat_level = "LOW"


    return (
        final_score,
        threat_level
    )


# ============================================================
# COMPLETE SCAMINTEL ANALYSIS
# ============================================================

def analyze_with_scamintel(
    text: str,
    previous_messages=None
):

    # --------------------------------------------------------
    # LOAD PREVIOUS CAMPAIGN MESSAGES
    # --------------------------------------------------------

    if previous_messages is None:

        previous_messages = (
            get_previous_messages()
        )


    # --------------------------------------------------------
    # 0. MULTILINGUAL LANGUAGE DETECTION
    # --------------------------------------------------------

    language_intelligence = detect_message_language(
        text
    )

    analysis_text = normalize_for_analysis(
        text,
        language_intelligence["language_code"]
    )

    print("\n==============================================")
    print("          LANGUAGE INTELLIGENCE")
    print("==============================================")

    print(
        "Detected Language:",
        language_intelligence["language"]
    )

    print(
        "Language Code:",
        language_intelligence["language_code"]
    )

    if language_intelligence["language_code"] != "en":

        print(
            "Analysis Language: English (translated)"
        )

    else:

        print(
            "Analysis Language: Original"
        )


    # --------------------------------------------------------
    # 1. ML CLASSIFICATION
    # --------------------------------------------------------

    prediction, confidence, probabilities = (
        classify_message(analysis_text)
    )


    # --------------------------------------------------------
    # 2. MESSAGE THREAT INTELLIGENCE
    # --------------------------------------------------------

    message_intelligence = analyze_message(
        text=analysis_text,
        ml_prediction=prediction,
        ml_confidence=confidence
    )


    # --------------------------------------------------------
    # 3. URL ANALYSIS
    # --------------------------------------------------------

    url_intelligence = analyze_urls_in_message(
        text
    )


    # --------------------------------------------------------
    # 4. LOOK-ALIKE / HOMOGRAPH ANALYSIS
    # --------------------------------------------------------

    lookalike_results = []

    for url_result in url_intelligence.get(
        "results",
        []
    ):

        url = url_result.get(
            "url"
        )

        if not url:
            continue

        lookalike_result = detect_lookalike(
            url
        )

        lookalike_results.append(
            lookalike_result
        )


    highest_lookalike_risk = 0

    for lookalike_result in lookalike_results:

        highest_lookalike_risk = max(
            highest_lookalike_risk,
            lookalike_result.get(
                "risk_score",
                0
            )
        )


    # --------------------------------------------------------
    # 5. URL REDIRECT ANALYSIS
    # --------------------------------------------------------

    redirect_results = []

    for url_result in url_intelligence.get(
        "results",
        []
    ):

        url = url_result.get(
            "url"
        )

        if not url:
            continue

        redirect_result = analyze_redirects(
            url
        )

        redirect_results.append(
            redirect_result
        )


    highest_redirect_risk = 0

    for redirect_result in redirect_results:

        highest_redirect_risk = max(
            highest_redirect_risk,
            redirect_result.get(
                "risk_score",
                0
            )
        )


    # --------------------------------------------------------
    # 6. PAYMENT / UPI SCAM ANALYSIS
    # --------------------------------------------------------

    payment_intelligence = detect_payment_scam(
        analysis_text
    )


    # --------------------------------------------------------
    # 7. PRIZE / LOTTERY SCAM ANALYSIS
    # --------------------------------------------------------

    prize_intelligence = detect_prize_scam(
        analysis_text
    )


    # --------------------------------------------------------
    # 8. IMPERSONATION SCAM ANALYSIS
    # --------------------------------------------------------

    impersonation_intelligence = detect_impersonation(
        analysis_text
    )


    # --------------------------------------------------------
    # 9. SOCIAL ENGINEERING ANALYSIS
    # --------------------------------------------------------

    social_engineering_intelligence = (
        detect_social_engineering(
            analysis_text
        )
    )


    # --------------------------------------------------------
    # 9.5 SCAM CAMPAIGN DETECTION
    # --------------------------------------------------------

    campaign_intelligence = analyze_campaign(
        current_message=text,
        previous_messages=previous_messages
    )

    print("\n==============================================")
    print("          SCAM CAMPAIGN INTELLIGENCE")
    print("==============================================")

    print(
        "Campaign Detected:",
        campaign_intelligence[
            "campaign_detected"
        ]
    )

    print(
        "Campaign Risk:",
        campaign_intelligence[
            "risk_score"
        ],
        "/ 100"
    )

    print(
        "Campaign Risk Level:",
        campaign_intelligence[
            "risk_level"
        ]
    )

    print(
        "Highest Similarity:",
        campaign_intelligence[
            "highest_similarity"
        ],
        "%"
    )

    print(
        "Messages Analyzed:",
        campaign_intelligence[
            "messages_analyzed"
        ]
    )


    # --------------------------------------------------------
    # 10. RISK VALUES
    # --------------------------------------------------------

    message_risk = message_intelligence[
        "risk_score"
    ]

    payment_risk = payment_intelligence[
        "risk_score"
    ]

    prize_risk = prize_intelligence[
        "risk_score"
    ]

    impersonation_risk = impersonation_intelligence[
        "risk_score"
    ]

    social_engineering_risk = (
        social_engineering_intelligence[
            "risk_score"
        ]
    )

    url_risk = url_intelligence[
        "highest_risk"
    ]

    lookalike_risk = (
        highest_lookalike_risk
    )

    redirect_risk = (
        highest_redirect_risk
    )

    campaign_risk = (
        campaign_intelligence[
            "risk_score"
        ]
    )


    # --------------------------------------------------------
    # LOOK-ALIKE CONTRIBUTES TO URL THREAT
    # --------------------------------------------------------

    url_risk = max(
        url_risk,
        lookalike_risk
    )


    # --------------------------------------------------------
    # REDIRECT CONTRIBUTES TO URL THREAT
    # --------------------------------------------------------

    url_risk = max(
        url_risk,
        redirect_risk
    )


    # --------------------------------------------------------
    # 11. FINAL RISK
    # --------------------------------------------------------

    final_score, final_threat = calculate_final_risk(
        message_risk,
        payment_risk,
        prize_risk,
        impersonation_risk,
        social_engineering_risk,
        url_risk,
        lookalike_risk,
        redirect_risk,
        prediction,
        campaign_risk
    )


    # --------------------------------------------------------
    # 12. EXPLAINABLE AI
    # --------------------------------------------------------

    explanation = generate_explanation(
        text=text,

        ml_result={
            "prediction": prediction,
            "confidence": confidence
        },

        message_threat=message_intelligence,

        payment_threat=payment_intelligence,

        prize_threat=prize_intelligence,

        impersonation_threat=impersonation_intelligence,

        social_engineering_threat=(
            social_engineering_intelligence
        ),

        url_threat=url_intelligence,

        lookalike_threat={
            "urls_analyzed": len(
                lookalike_results
            ),
            "highest_risk": highest_lookalike_risk,
            "results": lookalike_results
        },

        redirect_threat={
            "urls_analyzed": len(
                redirect_results
            ),
            "highest_risk": highest_redirect_risk,
            "results": redirect_results
        }

    )


    # --------------------------------------------------------
    # 13. COMBINED RESULT
    # --------------------------------------------------------

    result = {

        "message": text,

        "language_intelligence": language_intelligence,


        # ----------------------------------------------------
        # ML CLASSIFICATION
        # ----------------------------------------------------

        "ml_classification": {

            "prediction": prediction,

            "confidence": round(
                confidence,
                4
            ),

            "probabilities": {

                label: round(
                    float(probability),
                    4
                )

                for label, probability
                in probabilities.items()
            }
        },


        # ----------------------------------------------------
        # MESSAGE THREAT
        # ----------------------------------------------------

        "message_threat": (
            message_intelligence
        ),


        # ----------------------------------------------------
        # PAYMENT THREAT
        # ----------------------------------------------------

        "payment_threat": (
            payment_intelligence
        ),


        # ----------------------------------------------------
        # PRIZE THREAT
        # ----------------------------------------------------

        "prize_threat": (
            prize_intelligence
        ),


        # ----------------------------------------------------
        # IMPERSONATION THREAT
        # ----------------------------------------------------

        "impersonation_threat": (
            impersonation_intelligence
        ),


        # ----------------------------------------------------
        # SOCIAL ENGINEERING THREAT
        # ----------------------------------------------------

        "social_engineering_threat": (
            social_engineering_intelligence
        ),


        # ----------------------------------------------------
        # URL THREAT
        # ----------------------------------------------------

        "url_threat": (
            url_intelligence
        ),


        # ----------------------------------------------------
        # LOOK-ALIKE THREAT
        # ----------------------------------------------------

        "lookalike_threat": {

            "urls_analyzed": (
                len(lookalike_results)
            ),

            "highest_risk": (
                highest_lookalike_risk
            ),

            "results": (
                lookalike_results
            )
        },


        # ----------------------------------------------------
        # REDIRECT THREAT
        # ----------------------------------------------------

        "redirect_threat": {

            "urls_analyzed": (
                len(redirect_results)
            ),

            "highest_risk": (
                highest_redirect_risk
            ),

            "results": (
                redirect_results
            )
        },


        # ----------------------------------------------------
        # CAMPAIGN INTELLIGENCE
        # ----------------------------------------------------

        "campaign_intelligence":
            campaign_intelligence,


        # ----------------------------------------------------
        # EXPLAINABLE AI
        # ----------------------------------------------------

        "explainable_ai":
            explanation,


        # ----------------------------------------------------
        # FINAL ASSESSMENT
        # ----------------------------------------------------

        "final_assessment": {

            "risk_score": (
                final_score
            ),

            "threat_level": (
                final_threat
            )
        }

    }


    # --------------------------------------------------------
    # SAVE CURRENT MESSAGE TO CAMPAIGN HISTORY
    # --------------------------------------------------------

    save_campaign_message(
        text
    )


    # --------------------------------------------------------
    # RETURN FINAL RESULT
    # --------------------------------------------------------

    return result


# ============================================================
# TERMINAL INTERFACE
# ============================================================

if __name__ == "__main__":

    print("\n==============================================")
    print("              SCAMINTEL AI")
    print("       UNIFIED THREAT ANALYZER")
    print("==============================================")

    message = input(
        "\nEnter a message to analyze:\n> "
    )

    result = analyze_with_scamintel(
        message
    )

    ml = result[
        "ml_classification"
    ]

    message_threat = result[
        "message_threat"
    ]

    payment_threat = result[
        "payment_threat"
    ]

    prize_threat = result[
        "prize_threat"
    ]

    impersonation_threat = result[
        "impersonation_threat"
    ]

    social_engineering_threat = result[
        "social_engineering_threat"
    ]

    url_threat = result[
        "url_threat"
    ]

    lookalike_threat = result[
        "lookalike_threat"
    ]

    redirect_threat = result[
        "redirect_threat"
    ]

    final = result[
        "final_assessment"
    ]

    explanation = result[
        "explainable_ai"
    ]

    # --------------------------------------------------------
    # ML RESULT
    # --------------------------------------------------------

    print("\n==============================================")
    print("              ML CLASSIFICATION")
    print("==============================================")

    print(
        "Prediction:",
        ml["prediction"]
    )

    print(
        "Confidence:",
        f"{ml['confidence'] * 100:.2f}%"
    )

    print("\nClass Probabilities:")

    for label, probability in ml[
        "probabilities"
    ].items():

        print(
            f"  {label}: "
            f"{probability * 100:.2f}%"
        )

    # --------------------------------------------------------
    # MESSAGE INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("          MESSAGE THREAT INTELLIGENCE")
    print("==============================================")

    print(
        "Message Risk:",
        message_threat["risk_score"],
        "/ 100"
    )

    print("\nScam Categories:")

    if message_threat["scam_categories"]:

        for category in message_threat[
            "scam_categories"
        ]:

            print(" •", category)

    else:

        print(" • None detected")

    print("\nRisk Indicators:")

    if message_threat["risk_indicators"]:

        for indicator in message_threat[
            "risk_indicators"
        ]:

            print(" •", indicator)

    else:

        print(" • None detected")

    # --------------------------------------------------------
    # PAYMENT / UPI THREAT INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("        PAYMENT / UPI THREAT INTELLIGENCE")
    print("==============================================")

    print(
        "Payment Scam Detected:",
        payment_threat["detected"]
    )

    print(
        "Payment Risk:",
        payment_threat["risk_score"],
        "/ 100"
    )

    print(
        "Risk Level:",
        payment_threat["risk_level"]
    )

    print("\nCategories:")

    if payment_threat["categories"]:

        for category in payment_threat["categories"]:

            print(" •", category)

    else:

        print(" • None detected")

    print("\nIndicators:")

    if payment_threat["indicators"]:

        for indicator in payment_threat["indicators"]:

            print(" •", indicator)

    else:

        print(" • None detected")

    print(
        "\nCredential Request:",
        payment_threat["credential_request"]
    )

    print(
        "Urgency Detected:",
        payment_threat["urgency_detected"]
    )

    # --------------------------------------------------------
    # PRIZE / LOTTERY THREAT INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("        PRIZE / LOTTERY THREAT INTELLIGENCE")
    print("==============================================")

    print(
        "Prize Scam Detected:",
        prize_threat["detected"]
    )

    print(
        "Prize Risk:",
        prize_threat["risk_score"],
        "/ 100"
    )

    print(
        "Risk Level:",
        prize_threat["risk_level"]
    )

    print("\nCategories:")

    if prize_threat["categories"]:

        for category in prize_threat["categories"]:

            print(" •", category)

    else:

        print(" • None detected")

    print("\nIndicators:")

    if prize_threat["indicators"]:

        for indicator in prize_threat["indicators"]:

            print(" •", indicator)

    else:

        print(" • None detected")

    print(
        "\nUrgency Detected:",
        prize_threat["urgency_detected"]
    )

    print(
        "Payment Request:",
        prize_threat["payment_request"]
    )

    print(
        "Credential Request:",
        prize_threat["credential_request"]
    )

    print(
        "URL Detected:",
        prize_threat["url_detected"]
    )

    # --------------------------------------------------------
    # IMPERSONATION THREAT INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("          IMPERSONATION THREAT INTELLIGENCE")
    print("==============================================")

    print(
        "Impersonation Detected:",
        impersonation_threat["detected"]
    )

    print(
        "Impersonation Risk:",
        impersonation_threat["risk_score"],
        "/ 100"
    )

    print(
        "Risk Level:",
        impersonation_threat["risk_level"]
    )

    print("\nCategories:")

    if impersonation_threat["categories"]:

        for category in impersonation_threat[
            "categories"
        ]:

            print(" •", category)

    else:

        print(" • None detected")

    print("\nIndicators:")

    if impersonation_threat["indicators"]:

        for indicator in impersonation_threat[
            "indicators"
        ]:

            print(" •", indicator)

    else:

        print(" • None detected")

    print(
        "\nCredential Request:",
        impersonation_threat["credential_request"]
    )

    print(
        "Urgency Detected:",
        impersonation_threat["urgency_detected"]
    )

    print(
        "Payment Request:",
        impersonation_threat["payment_request"]
    )

    print(
        "URL Detected:",
        impersonation_threat["url_detected"]
    )

    # --------------------------------------------------------
    # SOCIAL ENGINEERING THREAT INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("       SOCIAL ENGINEERING THREAT INTELLIGENCE")
    print("==============================================")

    print(
        "Social Engineering Detected:",
        social_engineering_threat["detected"]
    )

    print(
        "Social Engineering Risk:",
        social_engineering_threat["risk_score"],
        "/ 100"
    )

    print(
        "Risk Level:",
        social_engineering_threat["risk_level"]
    )

    print("\nCategories:")

    if social_engineering_threat["categories"]:

        for category in social_engineering_threat[
            "categories"
        ]:

            print(" •", category)

    else:

        print(" • None detected")

    print("\nIndicators:")

    if social_engineering_threat["indicators"]:

        for indicator in social_engineering_threat[
            "indicators"
        ]:

            print(" •", indicator)

    else:

        print(" • None detected")

    print(
        "\nURL Detected:",
        social_engineering_threat["url_detected"]
    )

    # --------------------------------------------------------
    # URL INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("             URL THREAT ANALYSIS")
    print("==============================================")

    print(
        "URLs Detected:",
        url_threat["urls_detected"]
    )

    print(
        "Overall URL Risk:",
        url_threat["overall_risk"]
    )

    print(
        "Highest URL Score:",
        url_threat["highest_risk"],
        "/ 100"
    )

    for item in url_threat[
        "results"
    ]:

        print("\nURL:", item["url"])

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
            "Domain:",
            item["domain"]
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

        if "ml_prediction" in item:

            print(
                "URL ML Prediction:",
                item["ml_prediction"]
            )

            print(
                "URL ML Confidence:",
                f"{item['ml_confidence'] * 100:.2f}%"
            )

            print(
                "Phishing Probability:",
                f"{item['phishing_probability'] * 100:.2f}%"
            )

            print(
                "HYBRID URL RISK:",
                item["hybrid_risk_score"],
                "/ 100"
            )

            print(
                "Hybrid Risk Level:",
                item["hybrid_risk_level"]
            )

        if item["brand_matches"]:

            print(
                "Brand Matches:",
                ", ".join(
                    item["brand_matches"]
                )
            )

        if item["indicators"]:

            print("Indicators:")

            for indicator in item[
                "indicators"
            ]:

                print(" •", indicator)

    # --------------------------------------------------------
    # LOOK-ALIKE / HOMOGRAPH INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("       LOOK-ALIKE / HOMOGRAPH ANALYSIS")
    print("==============================================")

    print(
        "URLs Analyzed:",
        lookalike_threat["urls_analyzed"]
    )

    print(
        "Highest Look-Alike Risk:",
        lookalike_threat["highest_risk"],
        "/ 100"
    )

    if lookalike_threat["results"]:

        for item in lookalike_threat[
            "results"
        ]:

            print("\nURL:", item.get(
                "url",
                "Unknown"
            ))

            print(
                "Detected:",
                item.get(
                    "detected",
                    False
                )
            )

            print(
                "Risk Score:",
                item.get(
                    "risk_score",
                    0
                ),
                "/ 100"
            )

            print(
                "Risk Level:",
                item.get(
                    "risk_level",
                    "LOW"
                )
            )

            if item.get(
                "normalized_domain"
            ):

                print(
                    "Normalized Domain:",
                    item["normalized_domain"]
                )

            if item.get(
                "brand_matches"
            ):

                print(
                    "Brand Matches:",
                    ", ".join(
                        item["brand_matches"]
                    )
                )

            if "similarity" in item:

                similarity = item["similarity"]

                # Detector may return similarity either
                # as 0-1 or already as 0-100.

                if similarity <= 1:

                    similarity *= 100

                print(
                    "Similarity:",
                    f"{similarity:.1f}%"
                )

            if item.get(
                "indicators"
            ):

                print("Indicators:")

                for indicator in item[
                    "indicators"
                ]:

                    print(
                        " •",
                        indicator
                    )

            else:

                print(
                    "Indicators: None"
                )

    else:

        print(" • No URLs available for look-alike analysis")

    
    # --------------------------------------------------------
    # URL REDIRECT INTELLIGENCE
    # --------------------------------------------------------

    print("\n==============================================")
    print("          URL REDIRECT ANALYSIS")
    print("==============================================")

    redirect_threat = result[
        "redirect_threat"
    ]

    print(
        "URLs Analyzed:",
        redirect_threat["urls_analyzed"]
    )

    print(
        "Highest Redirect Risk:",
        redirect_threat["highest_risk"],
        "/ 100"
    )

    for item in redirect_threat[
        "results"
    ]:

        print("\nURL:", item["url"])

        print(
            "Redirect Detected:",
            item["redirect_detected"]
        )

        print(
            "Redirect Count:",
            item["redirect_count"]
        )

        print(
            "Original Domain:",
            item["original_domain"]
        )

        print(
            "Final Domain:",
            item["final_domain"]
        )

        print(
            "Domain Changed:",
            item["domain_changed"]
        )

        print(
            "Risk Score:",
            item["risk_score"],
            "/ 100"
        )

        print(
            "Risk Level:",
            item["risk_level"]
        )

        if item.get("redirect_chain"):

            print("\nRedirect Chain:")

            for redirect in item[
                "redirect_chain"
            ]:

                print(
                    " •",
                    redirect
                )

        if item.get("indicators"):

            print("\nIndicators:")

            for indicator in item[
                "indicators"
            ]:

                print(
                    " •",
                    indicator
                )

        else:

            print("\nIndicators:")
            print(" • None")


    # --------------------------------------------------------
    # EXPLAINABLE AI OUTPUT
    # --------------------------------------------------------

    print("\n==============================================")
    print("             EXPLAINABLE AI")
    print("==============================================")

    print("\nWhy this message is dangerous:")

    if explanation["why_flagged"]:

        for reason in explanation["why_flagged"]:
            print(" •", reason)

    else:

        print(" • No major threat reasons detected")


    print("\nEvidence:")

    if explanation["evidence"]:

        for item in explanation["evidence"]:
            print(" •", item)

    else:

        print(" • No additional evidence")


    print("\nML Explanation:")

    print(
        " • Prediction:",
        explanation["ml_explanation"]["prediction"]
    )

    print(
        " • Confidence:",
        f"{explanation['ml_explanation']['confidence'] * 100:.2f}%"
    )


    print("\nRisk Components:")

    for name, score in explanation[
        "risk_components"
    ].items():

        print(
            f" • {name}: {score} / 100"
        )


    print("\nRecommended Actions:")

    if explanation["recommendations"]:

        for recommendation in explanation[
            "recommendations"
        ]:

            print(" •", recommendation)

    else:

        print(" • No additional action required")

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n==============================================")
    print("             FINAL SCAMINTEL RESULT")
    print("==============================================")

    print(
        "FINAL RISK SCORE:",
        final["risk_score"],
        "/ 100"
    )

    print(
        "THREAT LEVEL:",
        final["threat_level"]
    )

    if final["threat_level"] == "HIGH":

        print("\n🚨 HIGH RISK")

        print(
            "Recommendation: "
            "DO NOT interact with this message or its links."
        )

    elif final["threat_level"] == "MEDIUM":

        print("\n⚠️ MEDIUM RISK")

        print(
            "Recommendation: "
            "Verify the sender independently before interacting."
        )

    else:

        print("\n✅ LOW RISK")

        print(
            "Recommendation: "
            "No major threat indicators detected."
        )

    print("\n==============================================")