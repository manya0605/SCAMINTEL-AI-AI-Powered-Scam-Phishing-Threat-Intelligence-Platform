import re


# ============================================================
# IMPERSONATION DETECTOR
# ============================================================

IMPERSONATION_PATTERNS = {

    "bank_impersonation": [
    r"\byour\s+(?:bank|banking)\b",
    r"\b(?:bank|banking)\s+(?:account|security|department|support)\b",
    r"\b(?:bank|account)\s+(?:security|verification|support)\s+team\b",
    r"\b(?:our|your)\s+bank\s+(?:support|security)\s+team\b",
    ],

    "government_impersonation": [
        r"\b(?:government|govt)\s+(?:department|official|agency)\b",
        r"\b(?:tax|income\s+tax)\s+(?:department|authority|office)\b",
        r"\b(?:police|cyber\s+crime)\s+(?:department|official)\b",
    ],

    "payment_service_impersonation": [
        r"\b(?:upi|payment)\s+(?:support|team|department)\b",
        r"\b(?:payment|transaction)\s+(?:support|security)\s+team\b",
        r"\b(?:wallet|payment)\s+security\s+team\b",
    ],

    "delivery_impersonation": [
        r"\b(?:delivery|courier|shipping)\s+(?:company|team|department)\b",
        r"\b(?:delivery|courier)\s+(?:support|service)\b",
        r"\bpackage\s+(?:delivery|verification)\s+team\b",
    ],

    "social_media_impersonation": [
        r"\b(?:facebook|instagram|whatsapp|telegram)\s+(?:security|support)\s+team\b",
        r"\bsocial\s+media\s+(?:security|support)\s+team\b",
        r"\baccount\s+security\s+team\b",
    ],

    "customer_support_impersonation": [
        r"\bcustomer\s+(?:support|service)\s+team\b",
        r"\btechnical\s+support\s+team\b",
        r"\bsecurity\s+support\s+team\b",
    ],
}


CREDENTIAL_PATTERNS = [
    r"\botp\b",
    r"\bpin\b",
    r"\bpassword\b",
    r"\bupi\s+pin\b",
    r"\bcard\s+(?:number|details)\b",
    r"\bbank\s+(?:details|account\s+details)\b",
]


URGENCY_PATTERNS = [
    r"\bimmediately\b",
    r"\burgent\b",
    r"\bact\s+now\b",
    r"\bverify\s+(?:now|immediately)\b",
    r"\bwithin\s+\d+\s+(?:hours?|minutes?|days?)\b",
    r"\baccount\s+(?:will\s+be\s+)?(?:blocked|closed|suspended)\b",
]


PAYMENT_PATTERNS = [
    r"\bpay\b",
    r"\bpayment\b",
    r"\bfee\b",
    r"\bprocessing\s+fee\b",
    r"\bsend\s+(?:money|payment)\b",
    r"\bupi\b",
]


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


def detect_impersonation(text: str):

    text = text.strip()

    categories = []
    indicators = []


    # --------------------------------------------------------
    # ORGANIZATION IMPERSONATION
    # --------------------------------------------------------

    for category, patterns in IMPERSONATION_PATTERNS.items():

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
    # CREDENTIAL REQUEST
    # --------------------------------------------------------

    credential_matches = _matches_patterns(
        text,
        CREDENTIAL_PATTERNS
    )

    credential_request = bool(
        credential_matches
    )

    if credential_request:

        indicators.append(
            "Sensitive credential request detected"
        )


    # --------------------------------------------------------
    # URGENCY
    # --------------------------------------------------------

    urgency_matches = _matches_patterns(
        text,
        URGENCY_PATTERNS
    )

    urgency_detected = bool(
        urgency_matches
    )

    if urgency_detected:

        indicators.append(
            "Urgency or pressure detected"
        )


    # --------------------------------------------------------
    # PAYMENT REQUEST
    # --------------------------------------------------------

    payment_matches = _matches_patterns(
        text,
        PAYMENT_PATTERNS
    )

    payment_request = bool(
        payment_matches
    )

    if payment_request:

        indicators.append(
            "Payment-related request detected"
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
            "Impersonation message contains a URL"
        )


    # --------------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------------

    risk_score = 0

    if categories:

        risk_score += 35

    if credential_request:

        risk_score += 25

    if urgency_detected:

        risk_score += 15

    if payment_request:

        risk_score += 15

    if url_detected:

        risk_score += 10


    # Strong combination
    if categories and credential_request:

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

        "credential_request":
            credential_request,

        "urgency_detected":
            urgency_detected,

        "payment_request":
            payment_request,

        "url_detected":
            url_detected,
    }