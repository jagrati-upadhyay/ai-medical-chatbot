import pandas as pd

INPUT_FILE = "data/public_symptoms_clean.csv"
OUTPUT_FILE = "data/public_categorized.csv"

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

def assign_category(row):

    fever = row["fever"]
    headache = row["headache"]
    cough = row["cough"]
    sore_throat = row["sore_throat"]
    runny_nose = row["runny_nose"]
    body_pain = row["body_pain"]
    fatigue = row["fatigue"]
    nausea = row["nausea"]
    vomiting = row["vomiting"]
    diarrhea = row["diarrhea"]

    # Count gastrointestinal symptoms
    gi_count = nausea + vomiting + diarrhea

    # Count respiratory symptoms
    respiratory_count = cough + sore_throat + runny_nose

    # 1. Strong gastrointestinal pattern
    if gi_count >= 2:
        return "gastrointestinal"

    # 2. Flu-like pattern
    if fever and (
        headache
        or cough
        or sore_throat
        or runny_nose
    ):
        return "flu_like"

    # 3. Viral-like pattern
    if fever and body_pain and fatigue:
        return "viral_like"

    # 4. Respiratory pattern
    if respiratory_count >= 2:
        return "respiratory"

    # 5. Headache-like pattern
    if headache and not fever and not cough:
        return "headache_like"

    # 6. Fatigue-like pattern
    if fatigue and not fever and not headache and not cough:
        return "fatigue_like"

    return None


# Load cleaned public dataset
df = pd.read_csv(INPUT_FILE)

print("Input dataset:", df.shape)


# Assign category
df["possible_category"] = df.apply(
    assign_category,
    axis=1
)


# Remove rows that could not be categorized
df = df.dropna(
    subset=["possible_category"]
).reset_index(drop=True)


# Keep only the features required by our ML model
df = df[
    FEATURES + ["possible_category"]
]


# Remove duplicate rows
df = df.drop_duplicates().reset_index(drop=True)


# Save categorized dataset
df.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("Categorization completed!")
print("Final dataset shape:", df.shape)

print()
print("Category distribution:")
print(
    df["possible_category"].value_counts()
)

print()
print("Saved file:")
print(OUTPUT_FILE)