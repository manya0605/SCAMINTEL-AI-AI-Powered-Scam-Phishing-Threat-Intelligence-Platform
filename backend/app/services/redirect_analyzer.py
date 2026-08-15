import requests
from urllib.parse import urlparse


# ============================================================
# SCAMINTEL AI — URL REDIRECT ANALYZER
# ============================================================

MAX_REDIRECTS = 5

REQUEST_TIMEOUT = 5


def analyze_redirects(url: str):

    result = {
        "url": url,
        "redirect_detected": False,
        "redirect_count": 0,
        "redirect_chain": [],
        "final_url": url,
        "original_domain": "",
        "final_domain": "",
        "domain_changed": False,
        "risk_score": 0,
        "risk_level": "LOW",
        "indicators": [],
        "error": None
    }

    # --------------------------------------------------------
    # ORIGINAL DOMAIN
    # --------------------------------------------------------

    parsed_original = urlparse(url)

    original_domain = (
        parsed_original.hostname or ""
    ).lower()

    result["original_domain"] = original_domain

    try:

        response = requests.get(
            url,
            allow_redirects=True,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent":
                "SCAMINTEL-AI-Security-Scanner/1.0"
            }
        )

        # ----------------------------------------------------
        # REDIRECT HISTORY
        # ----------------------------------------------------

        history = response.history

        result["redirect_count"] = len(history)

        result["redirect_detected"] = (
            len(history) > 0
        )

        # ----------------------------------------------------
        # BUILD REDIRECT CHAIN
        # ----------------------------------------------------

        chain = []

        for redirect in history:

            chain.append({
                "url": redirect.url,
                "status_code": redirect.status_code
            })

        # Add final destination

        chain.append({
            "url": response.url,
            "status_code": response.status_code
        })

        result["redirect_chain"] = chain

        result["final_url"] = response.url

        # ----------------------------------------------------
        # FINAL DOMAIN
        # ----------------------------------------------------

        parsed_final = urlparse(
            response.url
        )

        final_domain = (
            parsed_final.hostname or ""
        ).lower()

        result["final_domain"] = final_domain

        # ----------------------------------------------------
        # DOMAIN CHANGE
        # ----------------------------------------------------

        result["domain_changed"] = (
            original_domain != final_domain
        )

        # ----------------------------------------------------
        # RISK CALCULATION
        # ----------------------------------------------------

        risk_score = 0

        # Redirect detected

        if len(history) > 0:

            risk_score += 20

            result["indicators"].append(
                "URL redirects to another destination"
            )

        # Multiple redirects

        if len(history) >= 3:

            risk_score += 25

            result["indicators"].append(
                "Multiple redirects detected"
            )

        # Excessive redirects

        if len(history) >= 5:

            risk_score += 20

            result["indicators"].append(
                "Excessive redirect chain detected"
            )

        # Domain changed

        if (
            original_domain
            and final_domain
            and original_domain != final_domain
        ):

            risk_score += 30

            result["indicators"].append(
                "Redirect destination uses a different domain"
            )

        # HTTP final destination

        if response.url.startswith(
            "http://"
        ):

            risk_score += 10

            result["indicators"].append(
                "Final destination does not use HTTPS"
            )

        # ----------------------------------------------------
        # LIMIT SCORE
        # ----------------------------------------------------

        risk_score = min(
            risk_score,
            100
        )

        result["risk_score"] = risk_score

        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        if risk_score >= 70:

            result["risk_level"] = "HIGH"

        elif risk_score >= 40:

            result["risk_level"] = "MEDIUM"

        else:

            result["risk_level"] = "LOW"

    except requests.RequestException as error:

        result["error"] = str(error)

        result["indicators"].append(
            "Unable to safely resolve URL redirects"
        )

        result["risk_score"] = 20

        result["risk_level"] = "LOW"

    except Exception as error:

        result["error"] = str(error)

        result["indicators"].append(
            "Redirect analysis failed"
        )

    return result