import os
import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

# Allow importing from project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.url_features import extract_url_features


# ============================================================
# SCAMINTEL AI — URL ML MODEL V1
# ============================================================

DATA_DIR = PROJECT_ROOT / "data" / "processed_url"

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
    / "url_classifier"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


TRAIN_FILE = DATA_DIR / "train.csv"
VALID_FILE = DATA_DIR / "valid.csv"
TEST_FILE = DATA_DIR / "test.csv"


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def create_features(csv_file):

    print(
        f"\nLoading: {csv_file}"
    )

    df = pd.read_csv(
        csv_file
    )

    print(
        "Samples:",
        len(df)
    )

    print(
        "Extracting URL features..."
    )

    feature_rows = []

    for index, url in enumerate(
        df["url"]
    ):

        feature_rows.append(
            extract_url_features(url)
        )

        if (
            index + 1
        ) % 50000 == 0:

            print(
                f"Processed "
                f"{index + 1} URLs..."
            )

    X = pd.DataFrame(
        feature_rows
    )

    y = df["label"].astype(int)

    print(
        "Feature matrix:",
        X.shape
    )

    return X, y


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("        SCAMINTEL AI — URL ML MODEL V1")
print("=" * 70)

print("\nPreparing training data...")

X_train, y_train = create_features(
    TRAIN_FILE
)

print("\nPreparing validation data...")

X_valid, y_valid = create_features(
    VALID_FILE
)

print("\nPreparing test data...")

X_test, y_test = create_features(
    TEST_FILE
)


# ============================================================
# TRAIN RANDOM FOREST
# ============================================================

print("\n" + "=" * 70)
print("TRAINING RANDOM FOREST")
print("=" * 70)

model = RandomForestClassifier(

    n_estimators=150,

    max_depth=18,

    min_samples_leaf=2,

    random_state=42,

    n_jobs=-1,

)


print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training complete.")


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION RESULTS")
print("=" * 70)

valid_predictions = model.predict(
    X_valid
)

valid_accuracy = accuracy_score(
    y_valid,
    valid_predictions
)

valid_precision = precision_score(
    y_valid,
    valid_predictions
)

valid_recall = recall_score(
    y_valid,
    valid_predictions
)

valid_f1 = f1_score(
    y_valid,
    valid_predictions
)


print(
    f"\nValidation Accuracy: "
    f"{valid_accuracy:.4f}"
)

print(
    f"Validation Precision: "
    f"{valid_precision:.4f}"
)

print(
    f"Validation Recall: "
    f"{valid_recall:.4f}"
)

print(
    f"Validation F1: "
    f"{valid_f1:.4f}"
)

print("\nClassification Report:")

print(
    classification_report(
        y_valid,
        valid_predictions,
        target_names=[
            "BENIGN",
            "PHISHING"
        ]
    )
)


# ============================================================
# FINAL TEST
# ============================================================

print("\n" + "=" * 70)
print("FINAL TEST RESULTS")
print("=" * 70)

test_predictions = model.predict(
    X_test
)

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

test_precision = precision_score(
    y_test,
    test_predictions
)

test_recall = recall_score(
    y_test,
    test_predictions
)

test_f1 = f1_score(
    y_test,
    test_predictions
)


print(
    f"\nTest Accuracy: "
    f"{test_accuracy:.4f}"
)

print(
    f"Test Precision: "
    f"{test_precision:.4f}"
)

print(
    f"Test Recall: "
    f"{test_recall:.4f}"
)

print(
    f"Test F1: "
    f"{test_f1:.4f}"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        test_predictions,
        target_names=[
            "BENIGN",
            "PHISHING"
        ]
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")

cm = confusion_matrix(
    y_test,
    test_predictions
)

print(cm)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print("\n" + "=" * 70)
print("TOP URL FEATURES")
print("=" * 70)

importance = pd.DataFrame({

    "feature": X_train.columns,

    "importance":
        model.feature_importances_

})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print(
    importance.head(15).to_string(
        index=False
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

model_path = (
    MODEL_DIR
    / "scamintel_url_model.joblib"
)

feature_path = (
    MODEL_DIR
    / "url_feature_columns.joblib"
)


joblib.dump(
    model,
    model_path
)

joblib.dump(
    list(X_train.columns),
    feature_path
)


print("\n" + "=" * 70)
print("MODEL SAVED")
print("=" * 70)

print(
    "\nModel:"
)

print(
    model_path
)

print(
    "\nFeature columns:"
)

print(
    feature_path
)

print("\n")
print(
    "SCAMINTEL AI URL MODEL V1 READY!"
)

print("=" * 70)