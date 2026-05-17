import joblib


model = joblib.load("models/injection_model.pkl")


def detect_semantic_injection(text):

    prediction = model.predict([text])[0]

    probability = model.predict_proba([text])[0][1]

    return {

        "semantic_prediction": int(prediction),

        "semantic_score": round(float(probability), 2),

        "is_attack": bool(prediction)

    }