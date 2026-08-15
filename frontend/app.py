import streamlit as st
import requests


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SCAMINTEL AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


BACKEND_URL = "http://127.0.0.1:8000"


# ============================================================
# DARK THEME CSS
# NO HTML COMPONENTS ARE USED IN THE APPLICATION
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b1020;
        color: #ffffff;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background-color: #080d1a;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* --------------------------------------------------------
       TEXT AREA
       -------------------------------------------------------- */

    textarea {
        background-color: #ffffff !important;
        color: #111111 !important;
        border: 2px solid #475569 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        padding: 15px !important;
        caret-color: #111111 !important;
    }

    textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    textarea:focus {
        border: 2px solid #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }

    /* --------------------------------------------------------
       BUTTONS
       -------------------------------------------------------- */

    .stButton > button {
        border-radius: 10px !important;
        min-height: 45px !important;
        font-weight: 700 !important;
    }

    /* --------------------------------------------------------
       METRICS
       -------------------------------------------------------- */

    [data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #263653;
        border-radius: 14px;
        padding: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* --------------------------------------------------------
       EXPANDERS
       -------------------------------------------------------- */

    [data-testid="stExpander"] {
        background-color: #111827;
        border: 1px solid #263653;
        border-radius: 12px;
    }

    /* --------------------------------------------------------
       GENERAL TEXT
       -------------------------------------------------------- */

    p, li, span, label {
        color: #f8fafc;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ SCAMINTEL AI")

    st.caption(
        "AI-Powered Scam & Threat Intelligence Platform"
    )

    st.divider()

    st.subheader("🔎 Scanner")

    st.write("• Message Analysis")
    st.write("• Smishing Detection")
    st.write("• Phishing Detection")
    st.write("• Scam Detection")

    st.subheader("🧠 Threat Intelligence")

    st.write("• Payment / UPI")
    st.write("• Prize / Lottery")
    st.write("• Impersonation")
    st.write("• Social Engineering")

    st.subheader("🌐 URL Security")

    st.write("• Malicious URLs")
    st.write("• Brand Impersonation")
    st.write("• Look-Alike Domains")
    st.write("• Redirect Analysis")

    st.divider()

    st.caption("SCAMINTEL AI v1.0")


# ============================================================
# HERO
# ============================================================

st.title("🛡️ SCAMINTEL AI")

st.subheader(
    "Unified AI-Powered Scam, Phishing & Threat Intelligence Platform"
)

st.success(
    "● AI THREAT ANALYZER"
)


# ============================================================
# BACKEND STATUS
# ============================================================

try:

    health = requests.get(
        f"{BACKEND_URL}/health",
        timeout=3
    )

    backend_online = (
        health.status_code == 200
    )

except Exception:

    backend_online = False


if backend_online:

    st.success(
        "SCAMINTEL backend connected."
    )

else:

    st.error(
        "SCAMINTEL backend is offline. "
        "Please start FastAPI."
    )


# ============================================================
# MESSAGE SCANNER
# ============================================================

st.markdown("## 🔎 Message Scanner")

st.write(
    "Enter a suspicious message for complete AI threat analysis."
)


if "message_text" not in st.session_state:

    st.session_state.message_text = ""


message = st.text_area(
    "Message",
    value=st.session_state.message_text,
    height=180,
    placeholder=(
        "Paste a suspicious SMS, WhatsApp message, "
        "email or URL here..."
    ),
    label_visibility="collapsed"
)


# Keep typed message available
st.session_state.message_text = message


# ============================================================
# SAMPLE MESSAGE
# ============================================================

sample_message = (
    "Congratulations! Your PayPal account has been "
    "suspended due to unusual activity. Verify your "
    "account immediately at "
    "http://paypal-security-verification.com/login "
    "or your account will be permanently blocked. "
    "Enter your username, password, and OTP to restore access."
)


sample_col, empty_col = st.columns(
    [1, 5]
)


with sample_col:

    if st.button(
        "🧪 Load Sample"
    ):

        st.session_state.message_text = sample_message

        st.rerun()


# ============================================================
# SCAN / CLEAR
# ============================================================

scan_col, clear_col = st.columns(
    [4, 1]
)


with scan_col:

    scan_button = st.button(
        "🔍 Scan Message",
        type="primary",
        use_container_width=True
    )


with clear_col:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


if clear_button:

    st.session_state.message_text = ""

    if "analysis" in st.session_state:

        del st.session_state.analysis

    st.rerun()


# ============================================================
# ANALYSIS REQUEST
# ============================================================

if scan_button:

    current_message = (
        st.session_state.message_text
    )

    if not current_message.strip():

        st.warning(
            "Please enter a message before scanning."
        )

        st.stop()


    if not backend_online:

        st.error(
            "Backend is not running."
        )

        st.stop()


    with st.spinner(
        "SCAMINTEL AI is analyzing the message..."
    ):

        try:

            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json={
                    "message": current_message
                },
                timeout=120
            )


            if response.status_code != 200:

                st.error(
                    f"Backend error: HTTP {response.status_code}"
                )

                st.code(
                    response.text
                )

                st.stop()


            st.session_state.analysis = (
                response.json()
            )


        except Exception as e:

            st.error(
                f"Analysis failed: {e}"
            )

            st.stop()


# ============================================================
# RESULTS
# ============================================================

if "analysis" in st.session_state:

    data = st.session_state.analysis


    # ========================================================
    # EXACT BACKEND OBJECTS
    # ========================================================

    final = data.get(
        "final_assessment",
        {}
    )

    language = data.get(
        "language_intelligence",
        {}
    )

    ml = data.get(
        "ml_classification",
        {}
    )

    message_threat = data.get(
        "message_threat",
        {}
    )

    payment = data.get(
        "payment_threat",
        {}
    )

    prize = data.get(
        "prize_threat",
        {}
    )

    impersonation = data.get(
        "impersonation_threat",
        {}
    )

    social = data.get(
        "social_engineering_threat",
        {}
    )

    url = data.get(
        "url_threat",
        {}
    )

    lookalike = data.get(
        "lookalike_threat",
        {}
    )

    redirect = data.get(
        "redirect_threat",
        {}
    )

    campaign = data.get(
        "campaign_intelligence",
        {}
    )

    explainable = data.get(
        "explainable_ai",
        {}
    )


    # ========================================================
    # FINAL ASSESSMENT
    # ========================================================

    final_score = float(
        final.get(
            "risk_score",
            0
        )
    )

    threat_level = str(
        final.get(
            "threat_level",
            "UNKNOWN"
        )
    ).upper()


    st.markdown("## 📊 Threat Assessment")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "FINAL RISK",
            f"{int(final_score)}/100"
        )

        st.caption(
            threat_level
        )


    with c2:

        prediction = str(
            ml.get(
                "prediction",
                "UNKNOWN"
            )
        ).upper()

        confidence = float(
            ml.get(
                "confidence",
                0
            )
        )

        st.metric(
            "ML PREDICTION",
            prediction
        )

        st.caption(
            f"{confidence * 100:.2f}% confidence"
        )


    with c3:

        campaign_score = float(
            campaign.get(
                "risk_score",
                0
            )
        )

        st.metric(
            "CAMPAIGN RISK",
            f"{int(campaign_score)}/100"
        )

        st.caption(
            str(
                campaign.get(
                    "risk_level",
                    "UNKNOWN"
                )
            ).upper()
        )


    with c4:

        url_score = float(
            url.get(
                "highest_risk",
                0
            )
        )

        st.metric(
            "URL RISK",
            f"{int(url_score)}/100"
        )

        st.caption(
            str(
                url.get(
                    "overall_risk",
                    "UNKNOWN"
                )
            ).upper()
        )


    # ========================================================
    # FINAL VERDICT
    # ========================================================

    st.markdown("## 🚨 Final Verdict")


    if threat_level == "HIGH":

        st.error(
            f"🚨 HIGH RISK — {int(final_score)}/100\n\n"
            "This message contains strong indicators "
            "of a scam or phishing attempt. Do not click "
            "suspicious links or provide passwords, "
            "credentials or OTPs."
        )

    elif threat_level == "MEDIUM":

        st.warning(
            f"⚠️ MEDIUM RISK — {int(final_score)}/100"
        )

    else:

        st.success(
            f"✅ LOW RISK — {int(final_score)}/100"
        )


    # ========================================================
    # LANGUAGE
    # ========================================================

    st.markdown("## 🌐 Language Intelligence")


    l1, l2, l3 = st.columns(3)


    with l1:

        st.metric(
            "Language",
            str(
                language.get(
                    "language",
                    "Unknown"
                )
            )
        )


    with l2:

        st.metric(
            "Language Code",
            str(
                language.get(
                    "language_code",
                    "-"
                )
            )
        )


    with l3:

        st.metric(
            "Analysis",
            "Original"
        )


    # ========================================================
    # ML CLASSIFICATION
    # ========================================================

    st.markdown("## 🤖 ML Classification")


    ml1, ml2 = st.columns(2)


    with ml1:

        st.subheader("Prediction")

        st.success(
            prediction
        )

        st.write(
            f"Confidence: {confidence * 100:.2f}%"
        )


    with ml2:

        st.subheader(
            "Class Probabilities"
        )


        probabilities = ml.get(
            "probabilities",
            {}
        )


        for name, probability in probabilities.items():

            probability = float(
                probability
            )

            st.write(
                f"**{name.upper()}** — "
                f"{probability * 100:.2f}%"
            )

            st.progress(
                min(
                    max(
                        probability,
                        0
                    ),
                    1
                )
            )


    # ========================================================
    # THREAT INTELLIGENCE
    # ========================================================

    st.markdown("## 🧠 Threat Intelligence")


    threat_items = [

        (
            "Message Risk",
            message_threat.get(
                "risk_score",
                0
            )
        ),

        (
            "Payment Risk",
            payment.get(
                "risk_score",
                0
            )
        ),

        (
            "Prize Risk",
            prize.get(
                "risk_score",
                0
            )
        ),

        (
            "Impersonation Risk",
            impersonation.get(
                "risk_score",
                0
            )
        ),

        (
            "Social Engineering",
            social.get(
                "risk_score",
                0
            )
        ),

        (
            "URL Risk",
            url.get(
                "highest_risk",
                0
            )
        ),

        (
            "Look-Alike Risk",
            lookalike.get(
                "highest_risk",
                0
            )
        ),

        (
            "Redirect Risk",
            redirect.get(
                "highest_risk",
                0
            )
        )

    ]


    threat_cols = st.columns(4)


    for index, (label, value) in enumerate(
        threat_items
    ):

        with threat_cols[index % 4]:

            st.metric(
                label,
                f"{int(float(value))}/100"
            )


    # ========================================================
    # MESSAGE THREAT
    # ========================================================

    st.markdown("### 🚨 Message Threat")


    mt1, mt2 = st.columns(2)


    with mt1:

        st.metric(
            "Threat Level",
            str(
                message_threat.get(
                    "threat_level",
                    "UNKNOWN"
                )
            )
        )

        st.metric(
            "Risk Score",
            f"{int(float(message_threat.get('risk_score', 0)))}/100"
        )


    with mt2:

        st.markdown("**Scam Categories**")

        for item in message_threat.get(
            "scam_categories",
            []
        ):

            st.markdown(
                f"- {item}"
            )


        st.markdown("**Risk Indicators**")

        for item in message_threat.get(
            "risk_indicators",
            []
        ):

            st.markdown(
                f"- {item}"
            )


    # ========================================================
    # PAYMENT
    # ========================================================

    st.markdown("### 💳 Payment / UPI Threat")


    p1, p2, p3, p4 = st.columns(4)


    with p1:

        st.metric(
            "Detected",
            "YES"
            if payment.get(
                "detected",
                False
            )
            else "NO"
        )


    with p2:

        st.metric(
            "Risk",
            f"{int(float(payment.get('risk_score', 0)))}/100"
        )


    with p3:

        st.metric(
            "Urgency",
            "YES"
            if payment.get(
                "urgency_detected",
                False
            )
            else "NO"
        )


    with p4:

        st.metric(
            "URL Present",
            "YES"
            if payment.get(
                "url_present",
                False
            )
            else "NO"
        )


    # ========================================================
    # URL
    # ========================================================

    st.markdown("### 🌐 URL Threat Intelligence")


    u1, u2, u3 = st.columns(3)


    with u1:

        st.metric(
            "URLs Detected",
            str(
                url.get(
                    "urls_detected",
                    0
                )
            )
        )


    with u2:

        st.metric(
            "Overall Risk",
            str(
                url.get(
                    "overall_risk",
                    "UNKNOWN"
                )
            )
        )


    with u3:

        st.metric(
            "Highest Risk",
            f"{int(float(url.get('highest_risk', 0)))}/100"
        )


    for index, item in enumerate(
        url.get(
            "results",
            []
        )
    ):

        with st.expander(
            f"🔗 URL {index + 1} — "
            f"{item.get('domain', 'Unknown')}"
        ):

            st.write(
                f"URL: {item.get('url', '')}"
            )

            st.write(
                f"Domain: {item.get('domain', '')}"
            )

            st.write(
                f"Risk Score: "
                f"{item.get('risk_score', 0)}/100"
            )

            st.write(
                f"Risk Level: "
                f"{item.get('risk_level', 'UNKNOWN')}"
            )

            st.markdown("**Indicators**")

            for indicator in item.get(
                "indicators",
                []
            ):

                st.markdown(
                    f"- {indicator}"
                )


    # ========================================================
    # LOOKALIKE
    # ========================================================

    st.markdown(
        "### 🕵️ Look-Alike / Brand Impersonation"
    )


    lk1, lk2 = st.columns(2)


    with lk1:

        st.metric(
            "URLs Analyzed",
            str(
                lookalike.get(
                    "urls_analyzed",
                    0
                )
            )
        )


    with lk2:

        st.metric(
            "Highest Risk",
            f"{int(float(lookalike.get('highest_risk', 0)))}/100"
        )


    for item in lookalike.get(
        "results",
        []
    ):

        st.warning(
            "Possible brand impersonation detected: "
            + ", ".join(
                item.get(
                    "brand_matches",
                    []
                )
            )
        )

        st.write(
            f"Similarity: "
            f"{item.get('similarity', 0)}%"
        )


        for indicator in item.get(
            "indicators",
            []
        ):

            st.markdown(
                f"- {indicator}"
            )


    # ========================================================
    # REDIRECT
    # ========================================================

    st.markdown(
        "### ↪️ Redirect Intelligence"
    )


    r1, r2 = st.columns(2)


    with r1:

        st.metric(
            "URLs Analyzed",
            str(
                redirect.get(
                    "urls_analyzed",
                    0
                )
            )
        )


    with r2:

        st.metric(
            "Highest Risk",
            f"{int(float(redirect.get('highest_risk', 0)))}/100"
        )


    for item in redirect.get(
        "results",
        []
    ):

        st.write(
            "Redirect Detected: "
            + (
                "YES"
                if item.get(
                    "redirect_detected",
                    False
                )
                else "NO"
            )
        )

        st.write(
            "Redirect Count: "
            + str(
                item.get(
                    "redirect_count",
                    0
                )
            )
        )


    # ========================================================
    # CAMPAIGN
    # ========================================================

    st.markdown(
        "## 🧬 Scam Campaign Intelligence"
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Campaign Detected",
            "YES"
            if campaign.get(
                "campaign_detected",
                False
            )
            else "NO"
        )


    with c2:

        st.metric(
            "Campaign Risk",
            f"{int(float(campaign.get('risk_score', 0)))}/100"
        )


    with c3:

        st.metric(
            "Highest Similarity",
            f"{campaign.get('highest_similarity', 0)}%"
        )


    with c4:

        st.metric(
            "Messages Analyzed",
            str(
                campaign.get(
                    "messages_analyzed",
                    0
                )
            )
        )


    st.markdown(
        "**Current Campaign Indicators**"
    )


    for indicator in campaign.get(
        "current_indicators",
        []
    ):

        st.markdown(
            f"- {indicator}"
        )


    # ========================================================
    # MATCHING MESSAGES
    # ========================================================

    st.markdown(
        "### 🔗 Matching Campaign Messages"
    )


    for index, item in enumerate(
        campaign.get(
            "matching_messages",
            []
        )
    ):

        similarity = float(
            item.get(
                "similarity",
                0
            )
        )


        with st.expander(
            f"Message {index + 1} "
            f"— {similarity:.2f}% similarity"
        ):

            st.write(
                f"Message Index: "
                f"{item.get('message_index', '-')}"
            )


            st.markdown(
                "**Shared Indicators**"
            )


            for indicator in item.get(
                "shared_indicators",
                []
            ):

                st.markdown(
                    f"- {indicator}"
                )


    # ========================================================
    # EXPLAINABLE AI
    # ========================================================

    st.markdown(
        "## 💡 Explainable AI"
    )


    st.info(
        explainable.get(
            "summary",
            ""
        )
    )


    st.markdown(
        "### Why Was This Message Flagged?"
    )


    for reason in explainable.get(
        "why_flagged",
        []
    ):

        st.markdown(
            f"- {reason}"
        )


    st.markdown(
        "### Evidence"
    )


    for evidence in explainable.get(
        "evidence",
        []
    ):

        st.markdown(
            f"- {evidence}"
        )


    st.markdown(
        "### Recommended Actions"
    )


    for action in explainable.get(
        "recommendations",
        []
    ):

        st.markdown(
            f"- {action}"
        )


    # ========================================================
    # RISK COMPONENTS
    # ========================================================

    st.markdown(
        "### 📈 Risk Components"
    )


    risk_components = explainable.get(
        "risk_components",
        {}
    )


    rc = st.columns(4)


    for index, (name, value) in enumerate(
        risk_components.items()
    ):

        with rc[index % 4]:

            st.metric(
                name.replace(
                    "_",
                    " "
                ).title(),
                f"{int(float(value))}/100"
            )


    # ========================================================
    # COMPLETE JSON
    # ========================================================

    st.markdown(
        "## 📄 Complete Analysis"
    )


    with st.expander(
        "View Complete Analysis JSON"
    ):

        st.json(
            data
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SCAMINTEL AI • Multi-Layer AI Scam & Threat Intelligence"
)