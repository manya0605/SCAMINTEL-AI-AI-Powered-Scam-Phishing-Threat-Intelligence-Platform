import re
import unicodedata

from urllib.parse import urlparse


# ============================================================
# PROTECTED / WELL-KNOWN BRANDS
# ============================================================

PROTECTED_BRANDS = {

    "paypal": [
        "paypal.com"
    ],

    "google": [
        "google.com"
    ],

    "microsoft": [
        "microsoft.com"
    ],

    "apple": [
        "apple.com"
    ],

    "amazon": [
        "amazon.com"
    ],

    "facebook": [
        "facebook.com"
    ],

    "instagram": [
        "instagram.com"
    ],

    "whatsapp": [
        "whatsapp.com"
    ],

    "netflix": [
        "netflix.com"
    ],

    "linkedin": [
        "linkedin.com"
    ],
}


# ============================================================
# HOMOGRAPH / LOOK-ALIKE CHARACTER MAP
# ============================================================

HOMOGRAPH_MAP = {

    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
    "6": "g",
    "7": "t",
    "8": "b",

    "@": "a",
    "$": "s",
}


# ============================================================
# SUSPICIOUS BRAND DOMAIN TERMS
# ============================================================

SUSPICIOUS_BRAND_TERMS = {

    "login",
    "log-in",

    "signin",
    "sign-in",

    "verify",
    "verification",

    "security",
    "secure",

    "account",

    "support",

    "update",

    "auth",
    "authentication",

    "wallet",

    "payment",
    "payments",

    "billing",

    "confirm",
    "confirmation",

    "unlock",

    "recovery",

    "password",

    "alert",

    "notice",

    "helpdesk",
}


# ============================================================
# NORMALIZE DOMAIN
# ============================================================

def normalize_domain(domain: str):

    domain = (
        domain
        .lower()
        .strip(".")
    )

    try:

        domain = (
            domain
            .encode("idna")
            .decode("ascii")
        )

    except UnicodeError:

        pass

    return domain


# ============================================================
# NORMALIZE LOOK-ALIKE CHARACTERS
# ============================================================

def normalize_lookalike(text: str):

    text = text.lower()

    for fake_char, real_char in HOMOGRAPH_MAP.items():

        text = text.replace(
            fake_char,
            real_char
        )

    return text


# ============================================================
# LEVENSHTEIN DISTANCE
# ============================================================

def levenshtein_distance(
    a: str,
    b: str
):

    if len(a) < len(b):

        a, b = b, a

    previous = list(
        range(
            len(b) + 1
        )
    )

    for i, char_a in enumerate(
        a,
        start=1
    ):

        current = [i]

        for j, char_b in enumerate(
            b,
            start=1
        ):

            insert_cost = (
                current[j - 1] + 1
            )

            delete_cost = (
                previous[j] + 1
            )

            replace_cost = (
                previous[j - 1]
                + (char_a != char_b)
            )

            current.append(
                min(
                    insert_cost,
                    delete_cost,
                    replace_cost
                )
            )

        previous = current

    return previous[-1]


# ============================================================
# SIMILARITY SCORE
# ============================================================

def similarity_score(
    a: str,
    b: str
):

    if not a or not b:

        return 0.0

    distance = levenshtein_distance(
        a,
        b
    )

    maximum = max(
        len(a),
        len(b)
    )

    if maximum == 0:

        return 100.0

    return round(
        (
            1
            - distance / maximum
        )
        * 100,
        2
    )


# ============================================================
# EXTRACT REGISTERED DOMAIN
# ============================================================

def extract_domain_label(
    hostname: str
):

    parts = hostname.split(".")

    if len(parts) >= 2:

        return parts[-2]

    return hostname


# ============================================================
# MAIN LOOK-ALIKE DETECTOR
# ============================================================

def detect_lookalike(url: str):

    parsed = urlparse(url)

    raw_hostname = parsed.hostname or ""

    hostname = (
        raw_hostname
        .lower()
        .strip(".")
    )

    hostname = normalize_domain(hostname)

    registered_domain = extract_domain_label(hostname)

    normalized_domain = normalize_lookalike(
        registered_domain
    )

    matches = []
    indicators = []

    highest_similarity = 0.0
    detected = False

    # ========================================================
    # BRAND ANALYSIS
    # ========================================================

    for brand, legitimate_domains in PROTECTED_BRANDS.items():

        # ----------------------------------------------------
        # LEGITIMATE OFFICIAL DOMAIN
        # ----------------------------------------------------

        legitimate = any(
            hostname == domain
            or hostname.endswith("." + domain)
            for domain in legitimate_domains
        )

        if legitimate:
            continue

        # ----------------------------------------------------
        # EXACT BRAND DOMAIN
        # ----------------------------------------------------

        if normalized_domain == brand:

            detected = True

            if brand not in matches:
                matches.append(brand)

            highest_similarity = max(
                highest_similarity,
                100.0
            )

            indicators.append(
                f"Possible {brand} domain impersonation"
            )

            continue

        # ----------------------------------------------------
        # BRAND + SUSPICIOUS TERM
        # ----------------------------------------------------

        domain_parts = normalized_domain.split("-")

        if (
            brand in domain_parts
            and any(
                part in SUSPICIOUS_BRAND_TERMS
                for part in domain_parts
            )
        ):

            detected = True

            if brand not in matches:
                matches.append(brand)

            highest_similarity = max(
                highest_similarity,
                90.0
            )

            indicators.append(
                f"Possible {brand} impersonation "
                f"using suspicious domain term"
            )

            continue

        # ----------------------------------------------------
        # BRAND AS DOMAIN PREFIX
        # ----------------------------------------------------

        if normalized_domain.startswith(brand + "-"):

            suffix = normalized_domain[
                len(brand) + 1:
            ]

            if suffix in SUSPICIOUS_BRAND_TERMS:

                detected = True

                if brand not in matches:
                    matches.append(brand)

                highest_similarity = max(
                    highest_similarity,
                    90.0
                )

                indicators.append(
                    f"Possible {brand} impersonation "
                    f"using suspicious domain term"
                )

                continue

        # ----------------------------------------------------
        # LOOK-ALIKE CHARACTER SUBSTITUTION
        # ----------------------------------------------------

        original_similarity = similarity_score(
            registered_domain,
            brand
        )

        normalized_similarity = similarity_score(
            normalized_domain,
            brand
        )

        # Strong similarity after normalization
        if normalized_similarity >= 80:

            detected = True

            if brand not in matches:
                matches.append(brand)

            highest_similarity = max(
                highest_similarity,
                normalized_similarity
            )

            indicators.append(
                f"Possible look-alike "
                f"domain for {brand}"
            )

        # Moderate similarity is accepted only when the
        # original domain is reasonably close to the brand.
        elif (
            original_similarity >= 70
            and abs(
                len(registered_domain) - len(brand)
            ) <= 3
        ):

            detected = True

            if brand not in matches:
                matches.append(brand)

            highest_similarity = max(
                highest_similarity,
                original_similarity
            )

            indicators.append(
                f"Possible look-alike "
                f"domain for {brand}"
            )

    # ========================================================
    # HOMOGRAPH / CHARACTER SUBSTITUTION CHECK
    # ========================================================

    original_domain = registered_domain

    normalized_homograph = normalize_lookalike(
        original_domain
    )

    contains_substitution = (
        normalized_homograph != original_domain
    )

    # Only report character substitution when the
    # normalized domain actually resembles a protected brand.
    if contains_substitution:

        for brand in PROTECTED_BRANDS:

            homograph_similarity = similarity_score(
                normalized_homograph,
                brand
            )

            if homograph_similarity >= 80:

                detected = True

                if brand not in matches:
                    matches.append(brand)

                highest_similarity = max(
                    highest_similarity,
                    homograph_similarity
                )

                indicator = (
                    "Possible homograph or "
                    "character substitution detected"
                )

                if indicator not in indicators:
                    indicators.append(indicator)

                break

    # ========================================================
    # UNICODE CHARACTER CHECK
    # ========================================================

    try:

        has_unicode = any(
            ord(char) > 127
            for char in raw_hostname
        )

        if has_unicode:

            detected = True

            indicator = (
                "Unicode characters detected "
                "in domain"
            )

            if indicator not in indicators:
                indicators.append(indicator)

    except Exception:

        pass

    # ========================================================
    # RISK SCORE
    # ========================================================

    if detected:

        if highest_similarity >= 90:
            risk_score = 90

        elif highest_similarity >= 80:
            risk_score = 80

        elif highest_similarity >= 70:
            risk_score = 70

        else:
            risk_score = 65

        # Character substitution
        if contains_substitution:
            risk_score = max(
                risk_score,
                75
            )

        # Unicode domain
        if (
            "Unicode characters detected "
            "in domain"
            in indicators
        ):

            risk_score = max(
                risk_score,
                80
            )

        # Suspicious brand impersonation
        if any(
            "impersonation using suspicious"
            in indicator
            for indicator in indicators
        ):

            risk_score = max(
                risk_score,
                85
            )

    else:

        risk_score = 0

    # ========================================================
    # RISK LEVEL
    # ========================================================

    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "url": url,

        "domain": hostname,

        "normalized_domain":
            normalized_domain,

        "detected":
            detected,

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "brand_matches":
            matches,

        "similarity":
            highest_similarity,

        "indicators":
            indicators,

    }