# ============================================================
# SCAMINTEL AI — EXPLAINABLE AI ENGINE
# ============================================================

def generate_explanation(
    text,
    ml_result,
    message_threat,
    payment_threat,
    prize_threat,
    impersonation_threat,
    social_engineering_threat,
    url_threat,
    lookalike_threat,
    redirect_threat=None
):
    """
    Generates a human-readable explanation of why
    SCAMINTEL classified a message as suspicious.
    """

    reasons = []
    evidence = []
    recommendations = []

    # ========================================================
    # ML EXPLANATION
    # ========================================================

    prediction = ml_result.get(
        "prediction",
        "unknown"
    )

    confidence = ml_result.get(
        "confidence",
        0
    )

    if prediction == "smish":
        reasons.append(
            "The machine-learning model classified the "
            "message as a smishing attempt."
        )

        evidence.append(
            f"ML prediction: smish "
            f"({confidence * 100:.2f}% confidence)"
        )

    elif prediction == "promo":
        reasons.append(
            "The machine-learning model classified "
            "the message as promotional content."
        )

    else:
        evidence.append(
            f"ML prediction: {prediction} "
            f"({confidence * 100:.2f}% confidence)"
        )

    # ========================================================
    # MESSAGE THREAT EXPLANATION
    # ========================================================

    message_risk = message_threat.get(
        "risk_score",
        0
    )

    message_indicators = message_threat.get(
        "risk_indicators",
        []
    )

    if message_risk >= 70:

        reasons.append(
            "The message contains strong scam-related "
            "language patterns."
        )

    elif message_risk >= 40:

        reasons.append(
            "The message contains suspicious language "
            "patterns."
        )

    for indicator in message_indicators:

        if indicator not in evidence:

            evidence.append(
                f"Message indicator: {indicator}"
            )

    # ========================================================
    # PAYMENT / UPI EXPLANATION
    # ========================================================

    payment_risk = payment_threat.get(
        "risk_score",
        0
    )

    payment_categories = payment_threat.get(
        "categories",
        []
    )

    if payment_threat.get("detected", False):

        reasons.append(
            "Payment or UPI scam indicators were detected."
        )

        for category in payment_categories:

            evidence.append(
                f"Payment threat category: {category}"
            )

    if payment_threat.get(
        "credential_request",
        False
    ):

        reasons.append(
            "The message requests sensitive payment "
            "credentials or authentication information."
        )

        recommendations.append(
            "Never share your UPI PIN, OTP, password, "
            "or banking credentials."
        )

    # ========================================================
    # PRIZE / LOTTERY EXPLANATION
    # ========================================================

    prize_risk = prize_threat.get(
        "risk_score",
        0
    )

    if prize_threat.get("detected", False):

        reasons.append(
            "Prize, lottery, reward, or cash-windfall "
            "scam patterns were detected."
        )

        for category in prize_threat.get(
            "categories",
            []
        ):

            evidence.append(
                f"Prize threat category: {category}"
            )

    # ========================================================
    # IMPERSONATION EXPLANATION
    # ========================================================

    impersonation_risk = impersonation_threat.get(
        "risk_score",
        0
    )

    if impersonation_threat.get(
        "detected",
        False
    ):

        reasons.append(
            "The message appears to impersonate a "
            "trusted organization or service."
        )

        for category in impersonation_threat.get(
            "categories",
            []
        ):

            evidence.append(
                f"Impersonation category: {category}"
            )

        recommendations.append(
            "Verify the sender through the organization's "
            "official website or application."
        )

    # ========================================================
    # SOCIAL ENGINEERING EXPLANATION
    # ========================================================

    social_risk = social_engineering_threat.get(
        "risk_score",
        0
    )

    if social_engineering_threat.get(
        "detected",
        False
    ):

        reasons.append(
            "Social-engineering techniques such as "
            "urgency, authority, fear, reward, or "
            "emotional manipulation were detected."
        )

        for category in social_engineering_threat.get(
            "categories",
            []
        ):

            evidence.append(
                f"Social-engineering category: {category}"
            )

    # ========================================================
    # URL EXPLANATION
    # ========================================================

    url_risk = url_threat.get(
        "highest_risk",
        0
    )

    if url_risk >= 70:

        reasons.append(
            "A high-risk URL was detected in the message."
        )

        recommendations.append(
            "Do not click suspicious links."
        )

    for result in url_threat.get(
        "results",
        []
    ):

        url = result.get(
            "url",
            ""
        )

        if not url:
            continue

        for indicator in result.get(
            "indicators",
            []
        ):

            evidence.append(
                f"URL indicator: {indicator}"
            )

        if result.get(
            "brand_matches"
        ):

            brands = ", ".join(
                result["brand_matches"]
            )

            evidence.append(
                f"Potential impersonated brand: {brands}"
            )

    # ========================================================
    # LOOK-ALIKE / HOMOGRAPH EXPLANATION
    # ========================================================

    lookalike_risk = lookalike_threat.get(
        "highest_risk",
        0
    )

    if lookalike_risk >= 80:

        reasons.append(
            "A look-alike or homograph domain was detected."
        )

        recommendations.append(
            "Do not trust domains that imitate well-known "
            "brands using character substitutions."
        )

    for result in lookalike_threat.get(
        "results",
        []
    ):

        if not result.get(
            "detected",
            False
        ):
            continue

        normalized_domain = result.get(
            "normalized_domain",
            ""
        )

        similarity = result.get(
            "similarity",
            0
        )

        if normalized_domain:

            evidence.append(
                f"Look-alike normalized domain: "
                f"{normalized_domain}"
            )

        evidence.append(
            f"Look-alike similarity: "
            f"{similarity:.1f}%"
        )

        for indicator in result.get(
            "indicators",
            []
        ):

            evidence.append(
                f"Look-alike indicator: {indicator}"
            )

    # ========================================================
    # REDIRECT EXPLANATION
    # ========================================================

    if redirect_threat:

        redirect_risk = redirect_threat.get(
            "highest_risk",
            0
        )

        if redirect_risk >= 40:

            reasons.append(
                "The URL uses multiple redirects or "
                "shows suspicious redirect behavior."
            )

            recommendations.append(
                "Avoid links that pass through multiple "
                "unknown destinations."
            )

        for result in redirect_threat.get(
            "results",
            []
        ):

            if result.get(
                "redirect_detected",
                False
            ):

                evidence.append(
                    "URL redirect chain detected."
                )

                evidence.append(
                    f"Redirect count: "
                    f"{result.get('redirect_count', 0)}"
                )

                if result.get(
                    "domain_changed",
                    False
                ):

                    evidence.append(
                        "Redirect destination changed domains."
                    )

    # ========================================================
    # GENERAL RECOMMENDATIONS
    # ========================================================

    if not recommendations:

        if message_risk >= 70:

            recommendations.append(
                "Do not interact with the message "
                "until its source is independently verified."
            )

        elif message_risk >= 40:

            recommendations.append(
                "Verify the sender independently before "
                "taking any action."
            )

        else:

            recommendations.append(
                "No major threat indicators were detected."
            )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    reasons = list(
        dict.fromkeys(reasons)
    )

    evidence = list(
        dict.fromkeys(evidence)
    )

    recommendations = list(
        dict.fromkeys(recommendations)
    )

    # ========================================================
    # FINAL EXPLANATION
    # ========================================================

    return {

        "summary": (
            "SCAMINTEL analyzed the message using "
            "machine learning and multiple threat "
            "intelligence detectors."
        ),

        "why_flagged": reasons,

        "evidence": evidence,

        "ml_explanation": {

            "prediction": prediction,

            "confidence": round(
                confidence,
                4
            )
        },

        "risk_components": {

            "message_risk": message_risk,

            "payment_risk": payment_risk,

            "prize_risk": prize_risk,

            "impersonation_risk": impersonation_risk,

            "social_engineering_risk": social_risk,

            "url_risk": url_risk,

            "lookalike_risk": lookalike_risk,

            "redirect_risk": (
                redirect_threat.get(
                    "highest_risk",
                    0
                )
                if redirect_threat
                else 0
            )
        },

        "recommendations": recommendations
    }