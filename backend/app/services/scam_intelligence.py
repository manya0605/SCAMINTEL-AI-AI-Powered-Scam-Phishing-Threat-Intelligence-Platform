import re


# ============================================================
# SCAMINTEL AI — SCAM CATEGORY INTELLIGENCE ENGINE
# ============================================================

SCAM_PATTERNS = {

    "phishing": [
        r"\bverify your account\b",
        r"\bverify your identity\b",
        r"\bconfirm your account\b",
        r"\blogin\b",
        r"\bsign in\b",
        r"\baccount verification\b",
        r"\bclick here to verify\b",
        r"\bupdate your account\b",
    ],

    "payment_upi": [
        r"\bupi\b",
        r"\bpayment\b",
        r"\bpay\b",
        r"\brefund\b",
        r"\bcashback\b",
        r"\btransaction\b",
        r"\bbank account\b",
        r"\baccount details\b",
        r"\bpayment request\b",
    ],

    "prize_lottery": [
        r"\byou have won\b",
        r"\byou won\b",
        r"\bwon.*lottery\b",
        r"\blottery\b",
        r"\bprize\b",
        r"\breward\b",
        r"\bcongratulations\b",
        r"\bjackpot\b",
    ],

    "impersonation": [
        r"\bsbi\b",
        r"\bhdfc\b",
        r"\bicici\b",
        r"\baxis bank\b",
        r"\bpaytm\b",
        r"\bphonepe\b",
        r"\bgoogle pay\b",
        r"\bgovernment\b",
        r"\bincome tax\b",
        r"\bpolice\b",
        r"\bcustoms\b",
        r"\bcbi\b",
    ],

    "urgency_social_engineering": [
        r"\bimmediately\b",
        r"\burgent\b",
        r"\bwithin \d+ minutes\b",
        r"\bwithin \d+ hours\b",
        r"\baccount will be blocked\b",
        r"\baccount will be suspended\b",
        r"\blast chance\b",
        r"\bact now\b",
        r"\bdo not delay\b",
    ],

    "credential_theft": [
        r"\botp\b",
        r"\bpassword\b",
        r"\bpin\b",
        r"\bcvv\b",
        r"\bcard number\b",
        r"\bdebit card\b",
        r"\bcredit card\b",
        r"\bsend.*otp\b",
        r"\bshare.*password\b",
    ],

    "investment_scam": [
        r"\binvestment\b",
        r"\binvest\b",
        r"\bguaranteed returns\b",
        r"\bguaranteed profit\b",
        r"\bdaily profit\b",
        r"\bdouble your money\b",
        r"\bcrypto investment\b",
        r"\btrading profit\b",
    ],

    "delivery_scam": [
        r"\bparcel\b",
        r"\bpackage\b",
        r"\bcourier\b",
        r"\bdelivery\b",
        r"\bshipment\b",
        r"\bcustoms fee\b",
        r"\bdelivery fee\b",
        r"\bpay.*delivery\b",
    ],
}


# ============================================================
# URL EXTRACTION
# ============================================================

def extract_urls(text: str):

    url_pattern = r"(https?://[^\s]+|www\.[^\s]+)"

    return re.findall(url_pattern, text, flags=re.IGNORECASE)


# ============================================================
# CATEGORY DETECTION
# ============================================================

def detect_scam_categories(text: str):

    text_lower = text.lower()

    detected_categories = []
    indicators = []

    for category, patterns in SCAM_PATTERNS.items():

        category_matches = []

        for pattern in patterns:

            matches = re.findall(
                pattern,
                text_lower,
                flags=re.IGNORECASE
            )

            if matches:
                category_matches.extend(matches)

        if category_matches:

            detected_categories.append(category)

            indicators.extend(
                category_matches
            )

    return {
        "categories": detected_categories,
        "indicators": list(set(indicators))
    }


# ============================================================
# RISK SCORE
# ============================================================

def calculate_risk_score(
    ml_prediction,
    ml_confidence,
    categories,
    urls
):

    score = 0

    # --------------------------------------------------------
    # ML contribution
    # --------------------------------------------------------

    if ml_prediction == "smish":
        score += int(ml_confidence * 50)

    elif ml_prediction == "promo":
        score += int(ml_confidence * 15)

    # --------------------------------------------------------
    # Scam categories
    # --------------------------------------------------------

    category_weights = {

        "phishing": 15,

        "payment_upi": 15,

        "prize_lottery": 20,

        "impersonation": 15,

        "urgency_social_engineering": 15,

        "credential_theft": 20,

        "investment_scam": 20,

        "delivery_scam": 10,
    }

    for category in categories:

        score += category_weights.get(
            category,
            0
        )

    # --------------------------------------------------------
    # URL presence
    # --------------------------------------------------------

    if urls:
        score += 15

    # Maximum = 100
    score = min(score, 100)

    # --------------------------------------------------------
    # Threat level
    # --------------------------------------------------------

    if score >= 70:
        threat_level = "HIGH"

    elif score >= 40:
        threat_level = "MEDIUM"

    else:
        threat_level = "LOW"

    return score, threat_level


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze_message(
    text,
    ml_prediction,
    ml_confidence
):

    category_result = detect_scam_categories(text)

    categories = category_result["categories"]

    indicators = category_result["indicators"]

    urls = extract_urls(text)

    risk_score, threat_level = calculate_risk_score(
        ml_prediction,
        ml_confidence,
        categories,
        urls
    )

    return {
        "threat_level": threat_level,
        "risk_score": risk_score,
        "scam_categories": categories,
        "risk_indicators": indicators,
        "urls_detected": urls
    }