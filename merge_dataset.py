import pandas as pd

ORIGINAL_FILE = "data/symptoms.csv"
PUBLIC_FILE = "data/public_categorized.csv"

OUTPUT_FILE = "data/symptoms_expanded.csv"

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

TARGET = "possible_category"


# Load original dataset
original_df = pd.read_csv(ORIGINAL_FILE)

# Load public categorized dataset
public_df = pd.read_csv(PUBLIC_FILE)


# Keep only required columns
original_df = original_df[
    FEATURES + [TARGET]
]

public_df = public_df[
    FEATURES + [TARGET]
]


# Combine both datasets
expanded_df = pd.concat(
    [original_df, public_df],
    ignore_index=True
)


# Remove exact duplicate rows
expanded_df = expanded_df.drop_duplicates()


# Reset index
expanded_df = expanded_df.reset_index(drop=True)


# Save expanded dataset
expanded_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("Original dataset:", original_df.shape)
print("Public dataset:", public_df.shape)
print("Expanded dataset:", expanded_df.shape)

print()
print("Category distribution:")
print(
    expanded_df[TARGET].value_counts()
)

print()
print("Saved file:")
print(OUTPUT_FILE)