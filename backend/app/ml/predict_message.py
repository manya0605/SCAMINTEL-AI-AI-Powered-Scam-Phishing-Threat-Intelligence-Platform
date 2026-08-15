import joblib


MODEL_PATH = "models/message_classifier/scamintel_message_model.joblib"
VECTORIZER_PATH = "models/message_classifier/tfidf_vectorizer.joblib"


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_message(text: str):
    features = vectorizer.transform([text])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    class_probabilities = dict(
        zip(model.classes_, probabilities)
    )

    confidence = max(probabilities)

    return {
        "prediction": prediction,
        "confidence": round(float(confidence), 4),
        "probabilities": {
            label: round(float(probability), 4)
            for label, probability
            in class_probabilities.items()
        }
    }


if __name__ == "__main__":

    print("===================================")
    print("       SCAMINTEL AI V1")
    print("       MESSAGE ANALYZER")
    print("===================================")

    message = input("\nEnter a message to analyze:\n> ")

    result = predict_message(message)

    print("\n===== SCAMINTEL RESULT =====")

    print("Prediction:", result["prediction"])
    print("Confidence:", result["confidence"])

    print("\nClass probabilities:")

    for label, probability in result["probabilities"].items():
        print(f"  {label}: {probability}")