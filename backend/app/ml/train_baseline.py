from datasets import load_from_disk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os


print("Loading cleaned SCAMINTEL dataset...")

train_data = load_from_disk("data/processed/train")
validation_data = load_from_disk("data/processed/validation")
test_data = load_from_disk("data/processed/test")


X_train = train_data["text"]
y_train = train_data["label"]

X_validation = validation_data["text"]
y_validation = validation_data["label"]

X_test = test_data["text"]
y_test = test_data["label"]


print("\nTraining samples:", len(X_train))
print("Validation samples:", len(X_validation))
print("Test samples:", len(X_test))


# --------------------------------------------------
# TF-IDF
# --------------------------------------------------

print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    max_features=30000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_validation_tfidf = vectorizer.transform(X_validation)
X_test_tfidf = vectorizer.transform(X_test)


print("TF-IDF training shape:", X_train_tfidf.shape)


# --------------------------------------------------
# Logistic Regression
# --------------------------------------------------

print("\nTraining Logistic Regression...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_tfidf, y_train)


# --------------------------------------------------
# Validation
# --------------------------------------------------

print("\n===== VALIDATION RESULTS =====")

validation_predictions = model.predict(X_validation_tfidf)

print(
    "Validation Accuracy:",
    accuracy_score(y_validation, validation_predictions)
)

print(
    classification_report(
        y_validation,
        validation_predictions,
        digits=4
    )
)


# --------------------------------------------------
# Test
# --------------------------------------------------

print("\n===== FINAL TEST RESULTS =====")

test_predictions = model.predict(X_test_tfidf)

print(
    "Test Accuracy:",
    accuracy_score(y_test, test_predictions)
)

print(
    classification_report(
        y_test,
        test_predictions,
        digits=4
    )
)


# --------------------------------------------------
# Save model
# --------------------------------------------------

os.makedirs("models/message_classifier", exist_ok=True)

joblib.dump(
    vectorizer,
    "models/message_classifier/tfidf_vectorizer.joblib"
)

joblib.dump(
    model,
    "models/message_classifier/scamintel_message_model.joblib"
)

print("\n===== MODEL SAVED =====")
print("Vectorizer:")
print("models/message_classifier/tfidf_vectorizer.joblib")

print("\nModel:")
print("models/message_classifier/scamintel_message_model.joblib")

print("\nSCAMINTEL AI MESSAGE MODEL V1 READY!")