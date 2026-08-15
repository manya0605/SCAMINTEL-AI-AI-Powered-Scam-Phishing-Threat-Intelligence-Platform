import re


# ============================================================
# SOCIAL ENGINEERING DETECTOR
# ============================================================

SOCIAL_ENGINEERING_PATTERNS = {

    "urgency_pressure": [
        r"\bimmediately\b",
        r"\burgent\b",
        r"\bact\s+now\b",
        r"\bact\s+immediately\b",
        r"\bdo\s+this\s+now\b",
        r"\bwithin\s+\d+\s+(?:minutes?|hours?|days?)\b",
        r"\btoday\s+only\b",
        r"\blast\s+(?:chance|warning)\b",
    ],

    "fear_threat": [
        r"\baccount\s+(?:will\s+be\s+)?(?:blocked|closed|suspended)\b",
        r"\baccount\s+will\s+be\s+deleted\b",
        r"\byour\s+account\s+is\s+(?:compromised|at\s+risk)\b",
        r"\blegal\s+action\b",
        r"\bpolice\s+(?:will|may)\b",
        r"\byou\s+will\s+be\s+arrested\b",
        r"\bfine\s+will\s+be\s+charged\b",
    ],

    "authority_pressure": [
        r"\b(?:bank|government|police|tax)\s+(?:official|officer)\b",
        r"\b(?:bank|government|police|tax)\s+(?:department|authority)\b",
        r"\bsecurity\s+(?:team|department|officer)\b",
        r"\bcyber\s+crime\s+(?:department|officer)\b",
    ],

    "reward_manipulation": [
        r"\byou\s+have\s+won\b",
        r"\byou(?:'ve|\s+have)\s+won\b",
        r"\bcongratulations\b",
        r"\blucky\s+winner\b",
        r"\bclaim\s+(?:your\s+)?(?:prize|reward)\b",
        r"\bexclusive\s+reward\b",
        r"\bcash\s+prize\b",
    ],

    "credential_pressure": [
        r"\bshare\s+(?:your\s+)?(?:otp|pin|password)\b",
        r"\bsend\s+(?:your\s+)?(?:otp|pin|password)\b",
        r"\bprovide\s+(?:your\s+)?(?:otp|pin|password)\b",
        r"\bverify\s+(?:your\s+)?(?:otp|pin|password)\b",
        r"\bshare\s+your\s+upi\s+pin\b",
        r"\bshare\s+your\s+bank\s+(?:details|information)\b",
    ],

    "secrecy_manipulation": [
        r"\bdon't\s+tell\s+anyone\b",
        r"\bdo\s+not\s+tell\s+anyone\b",
        r"\bkeep\s+this\s+(?:secret|private)\b",
        r"\bthis\s+is\s+confidential\b",
        r"\bdon't\s+inform\s+(?:your\s+bank|anyone)\b",
    ],

    "emotional_manipulation": [
        r"\byour\s+(?:family|friend|relative)\s+(?:is|was)\s+in\s+trouble\b",
        r"\b(?:help|save)\s+me\s+immediately\b",
        r"\bi\s+need\s+your\s+help\s+urgently\b",
        r"\bemergency\b",
        r"\baccident\b",
        r"\bhospital\b",
    ],
}


def _matches_patterns(text, patterns):

    matches = []

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            matches.append(pattern)

    return matches


def detect_social_engineering(text: str):

    text = text.strip()

    categories = []
    indicators = []


    # --------------------------------------------------------
    # MANIPULATION PATTERNS
    # --------------------------------------------------------

    for category, patterns in SOCIAL_ENGINEERING_PATTERNS.items():

        matches = _matches_patterns(
            text,
            patterns
        )

        if matches:

            categories.append(
                category
            )

            indicators.extend(
                matches
            )


    # --------------------------------------------------------
    # URL DETECTION
    # --------------------------------------------------------

    url_detected = bool(
        re.search(
            r"https?://\S+",
            text,
            re.IGNORECASE
        )
    )

    if url_detected:

        indicators.append(
            "Social-engineering message contains a URL"
        )


    # --------------------------------------------------------
    # RISK SCORING
    # --------------------------------------------------------

    risk_score = 0

    if categories:

        risk_score += 30


    # Multiple manipulation techniques
    if len(categories) >= 2:

        risk_score += 20


    if len(categories) >= 3:

        risk_score += 15


    # URL increases attack potential
    if url_detected:

        risk_score += 10


    # Strong combinations
    if (
        "urgency_pressure" in categories
        and "fear_threat" in categories
    ):

        risk_score += 15


    if (
        "credential_pressure" in categories
        and "authority_pressure" in categories
    ):

        risk_score += 15


    if (
        "reward_manipulation" in categories
        and "urgency_pressure" in categories
    ):

        risk_score += 10


    risk_score = min(
        risk_score,
        100
    )


    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    if risk_score >= 70:

        risk_level = "HIGH"

    elif risk_score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    # --------------------------------------------------------
    # DETECTION
    # --------------------------------------------------------

    detected = bool(
        categories
    )


    return {

        "detected": detected,

        "risk_score": risk_score,

        "risk_level": risk_level,

        "categories": list(
            dict.fromkeys(
                categories
            )
        ),

        "indicators": list(
            dict.fromkeys(
                indicators
            )
        ),

        "url_detected":
            url_detected,
    }