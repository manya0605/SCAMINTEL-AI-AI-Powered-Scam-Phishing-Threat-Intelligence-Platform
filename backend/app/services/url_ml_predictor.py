from pathlib import Path
import sys
import joblib
import pandas as pd


# ============================================================
# SCAMINTEL AI — URL ML PREDICTOR
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.url_features import extract_url_features


MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "url_classifier"
    / "scamintel_url_model.joblib"
)

FEATURE_PATH = (
    PROJECT_ROOT
    / "models"
    / "url_classifier"
    / "url_feature_columns.joblib"
)


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(
    MODEL_PATH
)

feature_columns = joblib.load(
    FEATURE_PATH
)


# ============================================================
# PREDICT URL
# ============================================================

def predict_url(url: str):

    features = extract_url_features(
        url
    )

    feature_df = pd.DataFrame(
        [features]
    )

    # Ensure exactly the same feature
    # order used during training.
    feature_df = feature_df[
        feature_columns
    ]

    prediction = model.predict(
        feature_df
    )[0]

    probabilities = model.predict_proba(
        feature_df
    )[0]

    benign_probability = float(
        probabilities[0]
    )

    phishing_probability = float(
        probabilities[1]
    )

    if prediction == 1:

        label = "PHISHING"

        confidence = phishing_probability

    else:

        label = "BENIGN"

        confidence = benign_probability

    return {

        "prediction": label,

        "confidence": round(
            confidence,
            4
        ),

        "benign_probability": round(
            benign_probability,
            4
        ),

        "phishing_probability": round(
            phishing_probability,
            4
        ),

    }