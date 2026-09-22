import joblib
import pandas as pd


# Load trained model
model = joblib.load("models/symptom_model.pkl")


FEATURES = [
    "fever",
    "headache",
    "cough",
    "sore_throat",
    "runny_nose",
    "body_pain",
    "fatigue",
    "nausea",
    "vomiting",
    "diarrhea"
]


SYMPTOM_MAPPING = {

    "fever": "fever",

    "headache": "headache",

    "cough": "cough",

    "sore throat": "sore_throat",

    "runny nose": "runny_nose",

    "body pain": "body_pain",

    "fatigue": "fatigue",

    "nausea": "nausea",

    "vomiting": "vomiting",

    "diarrhea": "diarrhea",

    # Symptoms currently not represented
    # as features in the trained model

    "cold": None,

    "stomach pain": None,

    "abdominal pain": None,

    "weakness": None,

    "dizziness": None,

    "back pain": None,

    "joint pain": None,

    "chest pain": None,

    "shortness of breath": None,

    "breathing difficulty": None,

    "rash": None,

    "itching": None,

    "sneezing": None
}


def predict_category(symptoms):

    input_data = {
        feature: 0
        for feature in FEATURES
    }

    for symptom in symptoms:

        mapped_symptom = SYMPTOM_MAPPING.get(
            symptom,
            symptom
        )

        if mapped_symptom in input_data:

            input_data[mapped_symptom] = 1

    input_df = pd.DataFrame(
        [input_data],
        columns=FEATURES
    )

    # Prediction
    prediction = model.predict(input_df)

    predicted_category = prediction[0]

    # Prediction probabilities
    probabilities = model.predict_proba(input_df)[0]

    # Highest probability
    confidence = max(probabilities)

    return predicted_category, confidence