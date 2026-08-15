# ============================================================
# SCAMINTEL AI — SCAM CAMPAIGN DETECTOR
# ============================================================

import re
from collections import Counter


# ------------------------------------------------------------
# NORMALIZE TEXT
# ------------------------------------------------------------

def normalize_text(text: str):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ------------------------------------------------------------
# EXTRACT INDICATORS
# ------------------------------------------------------------

def extract_campaign_indicators(text: str):

    text = normalize_text(text)

    indicators = []

    # URLs
    urls = re.findall(
        r"https?://[^\s]+",
        text
    )

    for url in urls:

        indicators.append(
            url
        )

    # Phone numbers
    phones = re.findall(
        r"\+?\d[\d\s\-()]{7,}\d",
        text
    )

    for phone in phones:

        indicators.append(
            phone
        )

    # Important scam keywords
    keywords = [

        "verify your account",
        "urgent",
        "immediately",
        "within 24 hours",
        "account suspended",
        "account blocked",
        "click here",
        "login",
        "verification",
        "payment",
        "refund",
        "prize",
        "winner",
        "otp",
        "upi"

    ]

    for keyword in keywords:

        if keyword in text:

            indicators.append(
                keyword
            )

    return indicators


# ------------------------------------------------------------
# CAMPAIGN SIMILARITY
# ------------------------------------------------------------

def calculate_campaign_similarity(
    indicators_a,
    indicators_b
):

    if not indicators_a or not indicators_b:

        return 0.0

    set_a = set(
        indicators_a
    )

    set_b = set(
        indicators_b
    )

    intersection = (
        set_a & set_b
    )

    union = (
        set_a | set_b
    )

    if not union:

        return 0.0

    similarity = (
        len(intersection)
        /
        len(union)
    )

    return round(
        similarity * 100,
        2
    )


# ------------------------------------------------------------
# CAMPAIGN ANALYSIS
# ------------------------------------------------------------

def analyze_campaign(
    current_message: str,
    previous_messages=None
):

    if previous_messages is None:

        previous_messages = []


    current_indicators = (
        extract_campaign_indicators(
            current_message
        )
    )


    matches = []

    highest_similarity = 0.0


    for index, message in enumerate(
        previous_messages
    ):

        previous_indicators = (
            extract_campaign_indicators(
                message
            )
        )

        similarity = (
            calculate_campaign_similarity(
                current_indicators,
                previous_indicators
            )
        )

        if similarity > 0:

            matches.append({

                "message_index": index,

                "similarity": similarity,

                "shared_indicators": list(
                    set(current_indicators)
                    &
                    set(previous_indicators)
                )

            })


        highest_similarity = max(
            highest_similarity,
            similarity
        )


    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    if highest_similarity >= 70:

        risk_score = 90
        risk_level = "HIGH"

    elif highest_similarity >= 40:

        risk_score = 60
        risk_level = "MEDIUM"

    elif highest_similarity > 0:

        risk_score = 30
        risk_level = "LOW"

    else:

        risk_score = 0
        risk_level = "LOW"


    campaign_detected = (
        highest_similarity >= 40
    )


    return {

        "campaign_detected":
            campaign_detected,

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "highest_similarity":
            highest_similarity,

        "current_indicators":
            current_indicators,

        "matching_messages":
            matches,

        "messages_analyzed":
            len(previous_messages)

    }