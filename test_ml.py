from utils.ml_model import predict_category

symptoms = [
    "fever",
    "body pain",
    "fatigue"
]
category, confidence = predict_category(symptoms)


print("Detected symptoms:")
print(symptoms)

print("\nPredicted category:")
print(category)

print("\nModel confidence:")
print(f"{confidence * 100:.2f}%")