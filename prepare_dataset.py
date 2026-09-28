import pandas as pd
import re

# Kaggle dataset
INPUT_FILE = "data/public_dataset.csv"

# Cleaned dataset
OUTPUT_FILE = "data/public_symptoms_clean.csv"

# Features used by our ML model
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


def normalize_symptom(value):
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()
    value = value.replace(" ", "_")
    value = re.sub(r"_+", "_", value)

    return value


# Load public dataset
df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:", df.shape)

# Find symptom columns
symptom_columns = [
    column for column in df.columns
    if column.startswith("Symptom_")
]

# Clean symptom names
for column in symptom_columns:
    df[column] = df[column].apply(normalize_symptom)


# Public dataset symptom → our feature
SYMPTOM_MAPPING = {
    "high_fever": "fever",
    "mild_fever": "fever",
    "fever": "fever",

    "headache": "headache",

    "cough": "cough",

    "runny_nose": "runny_nose",

    "fatigue": "fatigue",

    "nausea": "nausea",

    "vomiting": "vomiting",

    "diarrhea": "diarrhea",
    "diarrhoea": "diarrhea",

    "muscle_pain": "body_pain"
}


# Create new dataframe
clean_data = pd.DataFrame()

# Keep disease name for now
clean_data["Disease"] = (
    df["Disease"]
    .astype(str)
    .str.strip()
)

# Create all features with 0
for feature in FEATURES:
    clean_data[feature] = 0


# Convert symptoms into 0/1 features
for index, row in df.iterrows():

    detected_features = set()

    for column in symptom_columns:

        symptom = row[column]

        if symptom in SYMPTOM_MAPPING:
            detected_features.add(
                SYMPTOM_MAPPING[symptom]
            )

    for feature in detected_features:
        clean_data.loc[index, feature] = 1


# Remove duplicate rows
clean_data = clean_data.drop_duplicates()

# Remove rows where none of our selected symptoms were found
clean_data = clean_data[
    clean_data[FEATURES].sum(axis=1) > 0
]

# Reset numbering
clean_data = clean_data.reset_index(drop=True)

# Save cleaned dataset
clean_data.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("Cleaning completed!")
print("Cleaned dataset shape:", clean_data.shape)

print()
print("Output file:")
print(OUTPUT_FILE)