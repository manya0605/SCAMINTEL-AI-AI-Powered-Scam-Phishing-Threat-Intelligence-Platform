
# 🛡️ SCAMINTEL AI

### AI-Powered Scam, Phishing & Threat Intelligence Platform
**SCAMINTEL AI** is a multi-layer intelligent threat detection platform designed to analyze suspicious messages, URLs, and scam patterns using Machine Learning, Natural Language Processing, rule-based intelligence, URL analysis, social-engineering detection, impersonation detection, and campaign intelligence.

## 🚀 Overview

Online scams are becoming increasingly sophisticated. Attackers use phishing messages, fake login pages, impersonation, urgency tactics, malicious URLs, OTP requests, and social-engineering techniques to trick users into revealing sensitive information.

**SCAMINTEL AI** addresses this problem by combining multiple detection layers into a unified threat-analysis platform.

Instead of relying on a single Machine Learning prediction, the system analyzes a message from several perspectives:

- 🤖 Machine Learning Classification
- 🧠 Message Threat Analysis
- 💳 Payment / UPI Scam Detection
- 🎁 Prize & Lottery Scam Detection
- 🎭 Impersonation Detection
- 🧠 Social Engineering Detection
- 🌐 URL Threat Analysis
- 🕵️ Look-Alike / Brand Impersonation Detection
- ↪️ URL Redirect Analysis
- 🧬 Scam Campaign Intelligence
- 🌐 Language Intelligence
- 💡 Explainable AI
- 📊 Unified Risk Scoring

The final result is presented through an interactive **Streamlit dashboard**.

# ✨ Key Features

## 🤖 1. Machine Learning Scam Classification

SCAMINTEL AI uses a trained ML model to classify suspicious messages into categories such as:

- `normal`
- `promo`
- `smish`

The system also provides a confidence score and class probabilities.

Example:

```text
Prediction: SMISH
Confidence: 97.23%

Class Probabilities:

Normal : 1.83%
Promo  : 0.94%
Smish  : 97.23%
This allows the user to understand not only the prediction but also the model's confidence.

🔎 2. Message Threat Analysis
The message is analyzed for common scam indicators including:

Login requests

Password requests

OTP requests

Account verification

Urgency

Fear-based language

Suspicious authentication requests

Credential theft patterns

Suspicious keywords

Example indicators:

login
password
immediately
OTP
verify your account
The system converts these signals into a message-level risk score.

💳 3. Payment / UPI Scam Detection
The platform identifies payment-related scam patterns such as:

OTP scams

Payment requests

Suspicious payment URLs

Urgency related to financial transactions

Credential requests

UPI-related social engineering

The detector produces:

Detection Status
Risk Score
Risk Level
Categories
Indicators
Urgency Detection
URL Presence
Credential Request

🎁 4. Prize & Lottery Scam Detection

SCAMINTEL AI detects fraudulent prize and lottery messages.

It looks for patterns such as:
Fake winnings
Prize claims
Processing-fee requests
Sensitive information requests
Urgency
Suspicious links

Example:
Congratulations! You have won ₹25,00,000.
Pay the processing fee immediately to claim your reward.

The system analyzes the message and produces a dedicated prize-threat assessment.

🎭 5. Impersonation Detection

Scammers frequently impersonate:
Banks
Payment platforms
Government organizations
Technology companies
Popular brands
Security services

SCAMINTEL AI detects potential impersonation attempts by analyzing:
Brand names
Credential requests
Urgency
Suspicious URLs
Brand-related domain patterns

Example:
Possible impersonated brand:
PayPal
Risk Level:
HIGH

🧠 6. Social Engineering Detection

The system identifies psychological manipulation techniques commonly used by scammers

Detection categories include:
Urgency
Fear
Authority
Emotional pressure
Reward-based manipulation
Account suspension threats
Verification pressure

Example:
Social Engineering Category:
urgency_pressure

This helps identify scams that may not contain obvious malicious technical indicators.

🌐 7. URL Threat Analysis

URLs contained inside suspicious messages are analyzed independently.

SCAMINTEL AI evaluates factors such as:
HTTP vs HTTPS
Domain structure
Suspicious keywords
Brand names
URL length
Hostname length
Number of dots
Number of hyphens
Digits
Special characters
URL shorteners
IP-based URLs
Domain characteristics

Example:

URL:
http://paypal-security-verification.com/login

Risk Score:
90 / 100

Risk Level:
HIGH

🕵️ 8. Look-Alike / Brand Impersonation Detection

A major feature of SCAMINTEL AI is detecting suspicious domains that attempt to imitate trusted brands.

For example:
paypal-security-verification.com
may attempt to create the impression that it belongs to PayPal.

The system analyzes:
Brand matches
Normalized domain names
Similarity
Suspicious brand-related terms
Domain structure

Example output:
Brand:
PayPal

Similarity:
90%

Risk:
HIGH

↪️ 9. URL Redirect Analysis

SCAMINTEL AI can analyze URL redirect behavior.

The system examines:
Redirect detection
Redirect count
Redirect chain
Final URL
Domain changes
Redirect risk

Example:
Redirect Detected:
False

Redirect Count:
0

Risk:
20 / 100

If a URL cannot be safely resolved, the system records the reason rather than treating the failure as a successful redirect.

🧬 10. Scam Campaign Intelligence

SCAMINTEL AI does not only analyze a message individually.

It can also determine whether the message resembles previously analyzed scam messages.

Campaign intelligence includes:
Campaign detection
Campaign risk score
Highest similarity
Shared indicators
Number of analyzed messages
Matching historical messages

Example:
Campaign Detected:
YES

Campaign Risk:
90 / 100

Highest Similarity:
100%

Messages Analyzed:
7

This helps identify repeated scam campaigns and similar attack patterns.

🌐 11. Language Intelligence

The platform detects the language of the submitted message.

Example:
Language:
English

Language Code:
en

Analysis:
Original

This component makes the system more adaptable to multilingual scam detection.

💡 12. Explainable AI

SCAMINTEL AI does not simply output:
SCAM
Instead, it explains why the message was flagged.

The Explainable AI layer provides:
Summary
A short explanation of the overall analysis.

Reasons

For example:
The machine-learning model classified the
message as a smishing attempt.

The message contains strong scam-related
language patterns.

A high-risk URL was detected.

A look-alike domain was detected.
Evidence

The system provides supporting evidence such as:
ML prediction: smish
Message indicator: password
Message indicator: OTP
URL indicator: URL does not use HTTPS
Possible brand impersonation: PayPal
Look-alike similarity: 90%
Recommendations

The system provides safety recommendations such as:
Do not click suspicious links.
Do not trust domains that imitate
well-known brands.

📊 13. Unified Risk Assessment

All detection layers contribute to the final threat assessment.

The dashboard displays:
Final Risk
ML Prediction
Campaign Risk
URL Risk
Threat Level

Example:
FINAL RISK:       100 / 100
THREAT LEVEL:     HIGH

ML PREDICTION:    SMISH
CONFIDENCE:       97.23%

CAMPAIGN RISK:    90 / 100
URL RISK:         90 / 100
This provides a consolidated view of the overall threat.

🖥️ Dashboard

The application provides an interactive Streamlit dashboard.

The dashboard includes:

SCAMINTEL AI
│
├── Message Scanner
│
├── Threat Assessment
│
├── Final Verdict
│
├── Language Intelligence
│
├── ML Classification
│
├── Threat Intelligence
│
├── Payment / UPI Intelligence
│
├── Prize / Lottery Intelligence
│
├── Impersonation Intelligence
│
├── Social Engineering Intelligence
│
├── URL Threat Analysis
│
├── Look-Alike Analysis
│
├── Redirect Analysis
│
├── Scam Campaign Intelligence
│
├── Matching Campaign Messages
│
├── Explainable AI
│
└── Complete Analysis JSON
🏗️ System Architecture
                     ┌──────────────────────┐
                     │      User Input      │
                     │ Suspicious Message   │
                     └──────────┬───────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │    SCAMINTEL Backend   │
                    └────────────┬───────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
 ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
 │ ML Classifier  │     │ Message Threat │     │ URL Analyzer   │
 └───────┬────────┘     └───────┬────────┘     └───────┬────────┘
         │                      │                      │
         ▼                      ▼                      ▼
 ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
 │ Social         │     │ Payment / UPI  │     │ Look-Alike     │
 │ Engineering    │     │ Detection      │     │ Detection      │
 └───────┬────────┘     └───────┬────────┘     └───────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ Campaign Intelligence │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Explainable AI Layer  │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   Final Risk Score     │
                    │     & Threat Level     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Streamlit Dashboard   │
                    └────────────────────────┘

🛠️ Technology Stack

Frontend-Streamlit

Python

Custom CSS

Interactive dashboard components
Backend-FastAPI

Python

REST API

Machine Learning
Scikit-learn

Text classification

Probability estimation

Feature-based threat classification

Threat Intelligence
Rule-based detection

URL analysis

Domain analysis

Brand matching

Social engineering detection

Campaign similarity analysis

Data Processing
Python

Regular expressions

JSON

Text processing

📁 Project Structure

SCAMINTEL-AI/
│
├── backend/
│   └── app/
│       ├── main.py
│       │
│       ├── api/
│       │
│       ├── ml/
│       │   ├── predict_message.py
│       │   ├── scamintel_analyzer.py
│       │   ├── train_message_model.py
│       │   └── train_url_model.py
│       │
│       ├── analyzers/
│       │   ├── url_analyzer.py
│       │   ├── lookalike_analyzer.py
│       │   ├── redirect_analyzer.py
│       │   └── campaign_analyzer.py
│       │
│       ├── detectors/
│       │   ├── payment_scam.py
│       │   ├── prize_scam.py
│       │   ├── impersonation.py
│       │   └── social_engineering.py
│       │
│       ├── services/
│       │
│       └── data/
│           └── campaign_history.json
│
├── frontend/
│   └── app.py
│
├── models/
│   ├── message_model/
│   └── url_model/
│
├── tests/
│   ├── test_campaign.py
│   ├── test_hybrid_url.py
│   ├── test_impersonation.py
│   ├── test_intelligence.py
│   ├── test_lookalike.py
│   ├── test_ocr.py
│   ├── test_payment_scam.py
│   ├── test_prize_scam.py
│   ├── test_redirect.py
│   ├── test_social_engineering.py
│   ├── test_url_analyzer.py
│   └── test_url_ml.py
│
├── scripts/
│   ├── train_baseline.py
│   └── local_redirect_server.py
│
├── data/
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE

⚙️ Installation

1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/SCAMINTEL-AI.git
Move into the project:
cd SCAMINTEL-AI

🐍 2. Create a Virtual Environment
Windows
python -m venv venv
Activate it:
venv\Scripts\activate
Linux / macOS
python3 -m venv venv
source venv/bin/activate

📦 3. Install Dependencies
pip install -r requirements.txt
If requirements.txt is not available yet, install the core packages:
pip install fastapi uvicorn streamlit requests scikit-learn pandas numpy

▶️ Running the Application

SCAMINTEL AI uses a FastAPI backend and a Streamlit frontend.

You should run them in two terminals.

Terminal 1 — Start Backend
Activate the virtual environment:

venv\Scripts\activate
Then run:

uvicorn backend.app.main:app --reload
The backend should be available at:

http://127.0.0.1:8000
FastAPI documentation:

http://127.0.0.1:8000/docs
Terminal 2 — Start Frontend
Open another terminal.

Navigate to the project:

cd SCAMINTEL-AI
Activate the environment:

venv\Scripts\activate
Start Streamlit:

streamlit run frontend/app.py
The dashboard will open at:

http://localhost:8501

🧪 Example Analysis

Input
Your PayPal account has been suspended.
Verify your account immediately at
http://paypal-security-verification.com/login
or your account will be permanently blocked.
Enter your username, password, and OTP
to restore access.
Example Result
FINAL RISK
100 / 100

THREAT LEVEL
HIGH

ML PREDICTION
SMISH

CONFIDENCE
97.23%

CAMPAIGN RISK
90 / 100

URL RISK
90 / 100
Detected Indicators
login
password
immediately
OTP
verify your account
URL Intelligence
Possible brand impersonation: PayPal
Suspicious security keywords
URL does not use HTTPS
Look-Alike Intelligence
Brand Match: PayPal
Similarity: 90%
Risk Level: HIGH

🧪 Testing

The project contains multiple testing modules for individual intelligence components.

Examples:
python -m backend.app.ml.test_url_analyzer
python -m backend.app.ml.test_campaign
python -m backend.app.ml.test_payment_scam
python -m backend.app.ml.test_prize_scam
python -m backend.app.ml.test_social_engineering
python -m backend.app.ml.test_lookalike
Testing helps verify each detection layer independently.

🔐 Security Considerations

SCAMINTEL AI is designed as a defensive security-analysis system.

The platform should be used to:

Analyze suspicious messages

Identify phishing attempts

Detect malicious URLs

Study scam patterns

Improve user awareness

Support cybersecurity research

Users should never enter real passwords, OTPs, banking credentials, API keys, or other sensitive information into the scanner.

⚠️ Disclaimer

SCAMINTEL AI is an educational and defensive cybersecurity project.

The system provides risk assessments based on Machine Learning models, heuristics, URL analysis, and threat-detection rules.

A result should not be considered a guaranteed determination that a message or URL is safe or malicious.

Threat actors continuously change their techniques, so detection accuracy may vary depending on the input.

Always verify suspicious communications through official channels.

🎯 Project Objectives

The primary objectives of SCAMINTEL AI are:

Detect scam and phishing messages.

Identify suspicious URLs.

Detect brand impersonation.

Identify social-engineering techniques.

Detect payment and OTP scams.

Identify prize and lottery scams.

Detect suspicious campaign patterns.

Provide explainable threat intelligence.

Combine ML and rule-based security analysis.

Present results through an easy-to-use dashboard.

💡 What Makes SCAMINTEL AI Different?

Traditional spam classifiers often answer only one question:

"Is this message spam?"

SCAMINTEL AI attempts to answer several security questions:

Is this message suspicious?

What type of scam is it?

How confident is the ML model?

Is there a suspicious URL?

Does the URL imitate a known brand?

Is the message using social engineering?

Is it requesting OTP or credentials?

Does it resemble a known scam campaign?

What evidence caused the system to flag it?

What should the user do?
This multi-layer approach makes SCAMINTEL AI more informative than a simple binary spam classifier.

📈 Future Enhancements

Possible future improvements include:

 Multilingual scam detection

 Real-time threat-intelligence APIs

 Advanced transformer-based NLP models

 Deep-learning URL classification

 Browser extension

 Mobile application

 Email security integration

 SMS gateway integration

 QR-code scam detection

 Screenshot/OCR-based scam analysis

 Improved campaign clustering

 Real-time URL reputation checking

 Threat intelligence database

 User authentication and analyst accounts

 Historical threat dashboards

 Automated security reports

🏆 Skills Demonstrated

This project demonstrates practical experience with:
Python
Machine Learning
Natural Language Processing
Cybersecurity
Threat Intelligence
FastAPI
REST APIs
Streamlit
Scikit-learn
URL Analysis
Pattern Recognition
Social Engineering Detection
Data Processing
JSON
Software Architecture
API Integration
Explainable AI
Testing and Debugging

📚 Learning Outcomes

Through this project, the following concepts were implemented and explored:

Machine Learning
Text classification

Feature extraction

Model training

Prediction

Confidence estimation

Cybersecurity
Phishing detection

Smishing detection

URL security

Brand impersonation

Social engineering

Credential theft detection

Campaign analysis

Software Development
Backend API development

Frontend dashboard development

Modular architecture

Testing

Error handling

JSON-based communication

🚀 Demo Workflow

1. Open SCAMINTEL AI Dashboard
              ↓
2. Enter suspicious message
              ↓
3. Click "Scan Message"
              ↓
4. FastAPI receives the message
              ↓
5. ML classifier analyzes the text
              ↓
6. Threat detectors analyze scam patterns
              ↓
7. URLs are extracted and analyzed
              ↓
8. Look-alike detection is performed
              ↓
9. Social engineering is analyzed
              ↓
10. Campaign intelligence compares history
              ↓
11. Explainable AI generates evidence
              ↓
12. Final risk score is calculated
              ↓
13. Results displayed in Streamlit

👨‍💻 Author

Manya M V

I'm a 3rd year engineering student with a strong interest in Artificial Intelligence, Machine Learning, Python, and Cybersecurity. I enjoy developing practical, real-world technology solutions and exploring how AI can be applied to solve modern security challenges.

🛡️ SCAMINTEL AI
Detect. Analyze. Explain. Protect.
A multi-layer AI-powered platform for understanding modern digital scam and phishing threats.
SCAMINTEL AI was developed as a project to combine Machine Learning, threat intelligence, and intelligent security analysis to help users identify and understand digital scams and phishing threats.

⭐ Support
If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

📜 License
This project is intended for educational, research, and defensive cybersecurity purposes.

See the LICENSE file for licensing information.




