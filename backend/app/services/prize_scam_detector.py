import re


# ============================================================
# PRIZE / LOTTERY SCAM DETECTOR
# ============================================================

PRIZE_PATTERNS = {

    "lottery_scam": [
        r"\blottery\b",
        r"\blottery\s+(?:winner|prize|claim)\b",
        r"\byou\s+have\s+won\b",
        r"\byou(?:'ve|\s+have)\s+won\b",
    ],

    "prize_scam": [
        r"\bprize\b",
        r"\bprize\s+(?:winner|claim|money)\b",
        r"\bcongratulations\b",
        r"\byou\s+(?:are|have\s+been)\s+(?:selected|chosen)\b",
    ],

    "reward_scam": [
        r"\breward\b",
        r"\bclaim\s+(?:your\s+)?reward\b",
        r"\bspecial\s+reward\b",
        r"\bexclusive\s+reward\b",
    ],

    "cash_windfall": [
        r"\bcash\s+prize\b",
        r"\bcashback\s+reward\b",
        r"\bwon\s+(?:rs\.?|₹|\$)\s*\d+",
        r"\b(?:rs\.?|₹|\$)\s*\d+\s*(?:lakh|crore|thousand)?\b",
    ],

    "winner_impersonation": [
        r"\bselected\s+as\s+(?:a\s+)?winner\b",
        r"\blucky\s+winner\b",
        r"\bprize\s+winner\b",
        r"\blottery\s+winner\b",
    ],
}


URGENCY_PATTERNS = [
    r"\bimmediately\b",
    r"\burgent\b",
    r"\bact\s+now\b",
    r"\bclaim\s+now\b",
    r"\btoday\s+only\b",
    r"\bwithin\s+\d+\s+(?:hours?|minutes?|days?)\b",
    r"\bexpires?\b",
]


PAYMENT_PATTERNS = [
    r"\bpay\b",
    r"\bpayment\b",
    r"\bfee\b",
    r"\bprocessing\s+fee\b",
    r"\btransfer\b",
    r"\bsend\s+(?:money|payment)\b",
    r"\bupi\b",
    r"\bbank\s+account\b",
]


CREDENTIAL_PATTERNS = [
    r"\botp\b",
    r"\bpin\b",
    r"\bupi\s+pin\b",
    r"\bpassword\b",
    r"\bcard\s+(?:number|details)\b",
    r"\bbank\s+(?:details|account\s+details)\b",
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


def detect_prize_scam(text: str):

    text = text.strip()

    all_categories = []
    indicators = []

    # --------------------------------------------------------
    # PRIZE / LOTTERY PATTERNS
    # --------------------------------------------------------

    for category, patterns in PRIZE_PATTERNS.items():

        matches = _matches_patterns(
            text,
            patterns
        )

        if matches:

            all_categories.append(
                category
            )

            indicators.extend(
                matches
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
            "Prize message contains a payment-related request"
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
            "Prize message requests sensitive credentials"
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
            "Prize message contains a URL"
        )


    # --------------------------------------------------------
    # RISK SCORING
    # --------------------------------------------------------

    risk_score = 0

    # Base prize/lottery detection
    if all_categories:

        risk_score += 30


    # Urgency
    if urgency_detected:

        risk_score += 15


    # Payment request
    if payment_request:

        risk_score += 20


    # Credential theft
    if credential_request:

        risk_score += 25


    # URL
    if url_detected:

        risk_score += 10


    # Strong combination:
    # prize + urgency
    if all_categories and urgency_detected:

        risk_score += 10


    # Strong combination:
    # prize + payment
    if all_categories and payment_request:

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
        all_categories
    )


    return {

        "detected": detected,

        "risk_score": risk_score,

        "risk_level": risk_level,

        "categories": list(
            dict.fromkeys(
                all_categories
            )
        ),

        "indicators": list(
            dict.fromkeys(
                indicators
            )
        ),

        "urgency_detected":
            urgency_detected,

        "payment_request":
            payment_request,

        "credential_request":
            credential_request,

        "url_detected":
            url_detected,
    }