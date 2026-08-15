import re


# ============================================================
# PAYMENT / UPI SCAM DETECTOR
# ============================================================

PAYMENT_PATTERNS = {

    "upi_scam": [
        r"\bupi\b",
        r"\bupi\s+id\b",
        r"\bupi\s+payment\b",
        r"\bupi\s+pin\b",
        r"\bupi\s+request\b",
        r"\bupi\s+collect\b",
        r"\bgoogle\s*pay\b",
        r"\bgpay\b",
        r"\bphonepe\b",
        r"\bpaytm\b",
        r"\bbhim\b",
    ],

    "otp_scam": [
        r"\botp\b",
        r"\bone\s*time\s*password\b",
        r"\bverification\s*code\b",
        r"\bsecurity\s*code\b",
    ],

    "payment_request": [
        r"\bsend\s+(?:me\s+)?(?:rs\.?|₹|\$)?\s*\d+",
        r"\bpay\s+(?:now|immediately|urgently)\b",
        r"\bmake\s+(?:a\s+)?payment\b",
        r"\btransfer\s+(?:the\s+)?money\b",
        r"\bsend\s+(?:the\s+)?money\b",
        r"\bscan\s+(?:the\s+)?qr\b",
        r"\bscan\s+qr\s+code\b",
    ],

    "fake_refund": [
        r"\brefund\b",
        r"\bcashback\b",
        r"\breimbursement\b",
        r"\brefund\s+pending\b",
        r"\bclaim\s+(?:your\s+)?refund\b",
        r"\brefund\s+verification\b",
    ],

    "bank_scam": [
        r"\bbank\s+account\b",
        r"\baccount\s+will\s+be\s+(?:blocked|closed|suspended)\b",
        r"\baccount\s+suspended\b",
        r"\baccount\s+blocked\b",
        r"\bk?yc\b",
        r"\bkyc\s+update\b",
        r"\bkyc\s+verification\b",
    ],

    "payment_credential_request": [
        r"\bshare\s+(?:your\s+)?upi\s+pin\b",
        r"\bprovide\s+(?:your\s+)?upi\s+pin\b",
        r"\benter\s+(?:your\s+)?upi\s+pin\b",
        r"\bshare\s+(?:your\s+)?otp\b",
        r"\bsend\s+(?:your\s+)?otp\b",
        r"\bshare\s+(?:your\s+)?cvv\b",
        r"\bshare\s+(?:your\s+)?card\s+number\b",
    ],
}


def detect_payment_scam(text: str):

    text_lower = text.lower()

    categories = []
    indicators = []
    score = 0

    # --------------------------------------------------------
    # CHECK PATTERNS
    # --------------------------------------------------------

    for category, patterns in PAYMENT_PATTERNS.items():

        matched = False

        for pattern in patterns:

            if re.search(pattern, text_lower):

                matched = True

                if category not in categories:
                    categories.append(category)

                if pattern not in indicators:
                    indicators.append(pattern)

                break

        if matched:
            score += 15


    # --------------------------------------------------------
    # HIGH-RISK PAYMENT CREDENTIAL REQUEST
    # --------------------------------------------------------

    credential_patterns = PAYMENT_PATTERNS[
        "payment_credential_request"
    ]

    credential_requested = any(
        re.search(pattern, text_lower)
        for pattern in credential_patterns
    )

    if credential_requested:

        score += 25


    # --------------------------------------------------------
    # URGENCY / PRESSURE
    # --------------------------------------------------------

    urgency_patterns = [
        r"\burgent\b",
        r"\bimmediately\b",
        r"\bwithin\s+\d+\s+(?:minutes?|hours?)\b",
        r"\blast\s+warning\b",
        r"\baction\s+required\b",
        r"\bdo\s+not\s+ignore\b",
    ]

    urgency_detected = any(
        re.search(pattern, text_lower)
        for pattern in urgency_patterns
    )

    if urgency_detected:

        score += 15

        indicators.append(
            "Urgency or pressure detected"
        )


    # --------------------------------------------------------
    # PAYMENT + URL
    # --------------------------------------------------------

    url_present = bool(
        re.search(
            r"https?://\S+",
            text_lower
        )
    )

    payment_context = bool(
        categories
    )

    if url_present and payment_context:

        score += 15

        indicators.append(
            "Payment-related message contains a URL"
        )


    # --------------------------------------------------------
    # CAP SCORE
    # --------------------------------------------------------

    score = min(score, 100)


    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    if score >= 70:

        risk_level = "HIGH"

    elif score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    return {

        "detected": bool(categories),

        "risk_score": score,

        "risk_level": risk_level,

        "categories": categories,

        "indicators": indicators,

        "credential_request": credential_requested,

        "urgency_detected": urgency_detected,

        "url_present": url_present,
    }