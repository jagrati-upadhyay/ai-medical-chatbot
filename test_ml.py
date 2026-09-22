from utils.ml_model import predict_category


symptoms = [
    "fever",
    "headache",
    "cough"
]


category = predict_category(symptoms)


print("Detected symptoms:")
print(symptoms)

print("\nPredicted category:")
print(category)
