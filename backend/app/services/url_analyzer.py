import re
import ipaddress
import math
from collections import Counter
from urllib.parse import urlparse, parse_qs

import tldextract


# ============================================================
# SCAMINTEL AI — URL INTELLIGENCE V2
# Static URL analysis only.
# NEVER opens or visits URLs.
# ============================================================


SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "cutt.ly",
    "shorturl.at",
    "ow.ly",
    "buff.ly",
    "rebrand.ly",
}


SUSPICIOUS_TLDS = {
    "xyz",
    "top",
    "click",
    "link",
    "work",
    "zip",
    "review",
    "country",
    "gq",
    "tk",
    "ml",
    "ga",
    "cf",
}


BRANDS = {
    "google",
    "microsoft",
    "apple",
    "amazon",
    "paypal",
    "facebook",
    "instagram",
    "whatsapp",
    "netflix",
    "sbi",
    "hdfc",
    "icici",
    "axis",
    "paytm",
    "phonepe",
}


SUSPICIOUS_KEYWORDS = {
    "login",
    "signin",
    "verify",
    "verification",
    "account",
    "secure",
    "security",
    "update",
    "password",
    "reset",
    "confirm",
    "bank",
    "payment",
    "refund",
    "wallet",
    "otp",
    "claim",
    "prize",
    "winner",
}


# ============================================================
# URL EXTRACTION
# ============================================================

def extract_urls(text: str):

    pattern = r"(?:https?://|www\.)[^\s<>'\"]+"

    urls = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    cleaned = []

    for url in urls:
        url = url.rstrip(".,!?;:)]}")
        cleaned.append(url)

    return cleaned


# ============================================================
# NORMALIZE URL
# ============================================================

def normalize_url(url: str):

    url = url.strip()

    if url.lower().startswith("www."):
        return "http://" + url

    if not re.match(
        r"^[a-zA-Z][a-zA-Z0-9+.-]*://",
        url
    ):
        return "http://" + url

    return url


# ============================================================
# IP ADDRESS
# ============================================================

def is_ip_address(hostname: str):

    if not hostname:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True

    except ValueError:
        return False


# ============================================================
# ENTROPY
# ============================================================

def calculate_entropy(value: str):

    if not value:
        return 0.0

    counts = Counter(value)

    length = len(value)

    entropy = 0.0

    for count in counts.values():

        probability = count / length

        entropy -= probability * math.log2(
            probability
        )

    return entropy


# ============================================================
# BRAND LOOK-ALIKE DETECTION
# ============================================================

def detect_brand_impersonation(hostname: str):

    hostname_lower = hostname.lower()

    matches = []

    # Common character substitutions used in
    # look-alike domains.
    substitutions = str.maketrans({
        "0": "o",
        "1": "l",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "@": "a",
    })

    normalized_hostname = hostname_lower.translate(
        substitutions
    )

    for brand in BRANDS:

        # ----------------------------------------------------
        # Exact brand + suspicious surrounding text
        # ----------------------------------------------------

        if brand in hostname_lower:

            suspicious_patterns = [
                brand + r"\d+",
                brand + r"[-_]",
                r"[-_]" + brand,
                brand + r"(login|verify|secure|support)",
                r"(login|verify|secure|support)" + brand,
            ]

            for pattern in suspicious_patterns:

                if re.search(
                    pattern,
                    hostname_lower
                ):

                    matches.append(brand)

                    break

        # ----------------------------------------------------
        # Look-alike normalization
        # ----------------------------------------------------

        if brand in normalized_hostname:

            # Don't flag the legitimate exact domain.
            if brand not in hostname_lower:

                matches.append(brand)

    return list(set(matches))


# ============================================================
# CHARACTER FEATURES
# ============================================================

def extract_character_features(url: str):

    hostname = urlparse(
        normalize_url(url)
    ).hostname or ""

    return {

        "url_length": len(url),

        "hostname_length": len(hostname),

        "dot_count": url.count("."),

        "hyphen_count": url.count("-"),

        "underscore_count": url.count("_"),

        "digit_count": sum(
            char.isdigit()
            for char in hostname
        ),

        "special_character_count": len(
            re.findall(
                r"[^a-zA-Z0-9.\-_]",
                hostname
            )
        ),

        "subdomain_count": max(
            hostname.count(".") - 1,
            0
        ),

        "hostname_entropy": round(
            calculate_entropy(hostname),
            4
        ),

        "digit_ratio": round(
            (
                sum(char.isdigit() for char in hostname)
                / len(hostname)
            )
            if hostname
            else 0,
            4
        ),
    }


# ============================================================
# ANALYZE ONE URL
# ============================================================

def analyze_url(url: str):

    original_url = url

    normalized = normalize_url(url)

    parsed = urlparse(normalized)

    hostname = parsed.hostname or ""

    hostname = hostname.lower()

    extracted = tldextract.extract(hostname)

    registered_domain = extracted.registered_domain

    suffix = extracted.suffix.lower()

    subdomain = extracted.subdomain

    score = 0

    indicators = []

    # --------------------------------------------------------
    # HTTPS
    # --------------------------------------------------------

    if parsed.scheme.lower() != "https":

        score += 8

        indicators.append(
            "URL does not use HTTPS"
        )

    # --------------------------------------------------------
    # URL SHORTENER
    # --------------------------------------------------------

    if hostname in SHORTENERS:

        score += 35

        indicators.append(
            "Known URL shortening service"
        )

    # --------------------------------------------------------
    # IP ADDRESS
    # --------------------------------------------------------

    if is_ip_address(hostname):

        score += 30

        indicators.append(
            "IP address used instead of a domain name"
        )

    # --------------------------------------------------------
    # @ SYMBOL
    # --------------------------------------------------------

    if "@" in url:

        score += 25

        indicators.append(
            "URL contains @ symbol"
        )

    # --------------------------------------------------------
    # PUNYCODE
    # --------------------------------------------------------

    if "xn--" in hostname:

        score += 25

        indicators.append(
            "Punycode/IDN domain detected"
        )

    # --------------------------------------------------------
    # VERY LONG URL
    # --------------------------------------------------------

    if len(original_url) > 150:

        score += 10

        indicators.append(
            "Unusually long URL"
        )

    # --------------------------------------------------------
    # MANY SUBDOMAINS
    # --------------------------------------------------------

    if subdomain:

        subdomain_parts = subdomain.split(".")

        if len(subdomain_parts) >= 3:

            score += 15

            indicators.append(
                "Excessive subdomain depth"
            )

    # --------------------------------------------------------
    # SUSPICIOUS TLD
    # --------------------------------------------------------

    if suffix in SUSPICIOUS_TLDS:

        score += 15

        indicators.append(
            f"Suspicious top-level domain: .{suffix}"
        )

    # --------------------------------------------------------
    # BRAND IMPERSONATION
    # --------------------------------------------------------

    brand_matches = detect_brand_impersonation(
        hostname
    )

    if brand_matches:

        score += 70

        indicators.append(
            "Possible brand impersonation: "
            + ", ".join(brand_matches)
        )

    # --------------------------------------------------------
    # SUSPICIOUS KEYWORDS
    # --------------------------------------------------------

    keyword_matches = []

    url_lower = original_url.lower()

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in url_lower:

            keyword_matches.append(keyword)

    if keyword_matches:

        score += min(
            len(keyword_matches) * 4,
            20
        )

        indicators.append(
            "Suspicious security/payment keywords in URL"
        )

    # --------------------------------------------------------
    # CREDENTIALS IN URL
    # --------------------------------------------------------

    if parsed.username or parsed.password:

        score += 25

        indicators.append(
            "Credentials embedded in URL"
        )

    # --------------------------------------------------------
    # MANY QUERY PARAMETERS
    # --------------------------------------------------------

    query_parameters = parse_qs(
        parsed.query,
        keep_blank_values=True
    )

    if len(query_parameters) >= 6:

        score += 10

        indicators.append(
            "Large number of URL parameters"
        )

    # --------------------------------------------------------
    # HEAVY ENCODING
    # --------------------------------------------------------

    encoded_count = len(
        re.findall(
            r"%[0-9a-fA-F]{2}",
            original_url
        )
    )

    if encoded_count >= 5:

        score += 10

        indicators.append(
            "Heavy URL encoding detected"
        )

    # --------------------------------------------------------
    # CHARACTER FEATURES
    # --------------------------------------------------------

    character_features = extract_character_features(
        original_url
    )

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    score = min(score, 100)

    if score >= 70:

        risk_level = "HIGH"

    elif score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {

        "url": original_url,

        "domain": hostname,

        "registered_domain": registered_domain,

        "risk_score": score,

        "risk_level": risk_level,

        "indicators": list(
            dict.fromkeys(indicators)
        ),

        "brand_matches": brand_matches,

        "url_shortener": (
            hostname in SHORTENERS
        ),

        "ip_address": is_ip_address(
            hostname
        ),

        "https": (
            parsed.scheme.lower() == "https"
        ),

        "character_features": character_features,
    }


# ============================================================
# ANALYZE ALL URLS IN MESSAGE
# ============================================================

def analyze_urls_in_message(text: str):

    urls = extract_urls(text)

    results = []

    for url in urls:

        results.append(
            analyze_url(url)
        )

    if not results:

        return {

            "urls_detected": 0,

            "results": [],

            "highest_risk": 0,

            "overall_risk": "LOW",

        }

    highest_risk = max(
        result["risk_score"]
        for result in results
    )

    if highest_risk >= 70:

        overall_risk = "HIGH"

    elif highest_risk >= 40:

        overall_risk = "MEDIUM"

    else:

        overall_risk = "LOW"

    return {

        "urls_detected": len(results),

        "results": results,

        "highest_risk": highest_risk,

        "overall_risk": overall_risk,

    }