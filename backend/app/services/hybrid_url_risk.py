from backend.app.services.url_ml_predictor import predict_url
from backend.app.services.url_analyzer import analyze_url
from urllib.parse import urlparse


TRUSTED_DOMAINS = {
    "example.com",
    "example.org",
    "example.net",
    "localhost",
}


def calculate_hybrid_url_risk(url: str):

    # ---------------------------------------------------------
    # ML ANALYSIS
    # ---------------------------------------------------------

    ml_result = predict_url(url)

    phishing_probability = (
        ml_result["phishing_probability"]
    )

    # ---------------------------------------------------------
    # RULE-BASED ANALYSIS
    # ---------------------------------------------------------

    rule_result = analyze_url(url)

    rule_score = rule_result.get(
        "risk_score",
        0
    )

    # ---------------------------------------------------------
    # TRUSTED / RESERVED DOMAIN CHECK
    # ---------------------------------------------------------

    parsed = urlparse(url)

    hostname = (
        parsed.hostname or ""
    ).lower()

    is_trusted_domain = (
    hostname in TRUSTED_DOMAINS
    )

    # ---------------------------------------------------------
    # ML RISK SCORE
    # ---------------------------------------------------------

    ml_score = phishing_probability * 100

    # ---------------------------------------------------------
    # HYBRID SCORE
    # ---------------------------------------------------------

    if is_trusted_domain and rule_score == 0:

       hybrid_score = 0

    else:

        hybrid_score = (
        (ml_score * 0.60)
        +
        (rule_score * 0.40)
        )

    hybrid_score = round(
        min(hybrid_score, 100),
        2
    )

    # ---------------------------------------------------------
    # FINAL LEVEL
    # ---------------------------------------------------------

    if hybrid_score >= 70:

        risk_level = "HIGH"

    elif hybrid_score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {

        "url": url,

        "ml_prediction":
            ml_result["prediction"],

        "ml_confidence":
            ml_result["confidence"],

        "phishing_probability":
            phishing_probability,

        "rule_based_score":
            rule_score,

        "hybrid_risk_score":
            hybrid_score,

        "risk_level":
            risk_level,

        "rule_indicators":
            rule_result.get(
                "indicators",
                []
            ),

        "brand_matches":
            rule_result.get(
                "brand_matches",
                []
            ),

    }