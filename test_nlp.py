from utils.nlp import extract_symptoms


test_messages = [
    "I have high temperature",
    "I have low temperature",
    "My temperature is low",
    "I have fever",
    "I don't have fever",
    "I have cough and fever"
]


for message in test_messages:

    symptoms = extract_symptoms(message)

    print("Message:", message)
    print("Detected symptoms:", symptoms)
    print("-" * 50)