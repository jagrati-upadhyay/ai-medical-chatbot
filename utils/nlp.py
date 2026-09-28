import re


SYMPTOM_SYNONYMS = {

    "fever": [
        "fever",
        "high temperature",
        "high temp",
        "feeling hot",
        "feel hot",
        "body feels hot"
    ],

    "headache": [
        "headache",
        "head hurts",
        "head hurt",
        "pain in my head",
        "pain in the head",
        "head pain"
    ],

    "cough": [
        "cough",
        "coughing"
    ],

    "cold": [
        "cold",
        "common cold"
    ],

    "sore throat": [
        "sore throat",
        "throat hurts",
        "throat pain",
        "painful throat"
    ],

    "runny nose": [
        "runny nose",
        "nose is running",
        "running nose"
    ],

    "stomach pain": [
        "stomach pain",
        "stomach ache",
        "stomach hurts",
        "pain in my stomach"
    ],

    "abdominal pain": [
        "abdominal pain",
        "abdomen pain",
        "pain in abdomen"
    ],

    "vomiting": [
        "vomiting",
        "throwing up",
        "threw up",
        "vomit"
    ],

    "nausea": [
        "nausea",
        "feeling nauseous",
        "feel nauseous",
        "feel like vomiting"
    ],

    "diarrhea": [
        "diarrhea",
        "loose motion",
        "loose motions",
        "frequent loose stools"
    ],

    "fatigue": [
        "fatigue",
        "very tired",
        "feeling tired",
        "feel tired",
        "extremely tired"
    ],

    "weakness": [
        "weakness",
        "feeling weak",
        "feel weak",
        "very weak"
    ],

    "dizziness": [
        "dizziness",
        "dizzy",
        "feeling dizzy",
        "feel dizzy"
    ],

    "body pain": [
        "body pain",
        "body ache",
        "body aches",
        "pain all over my body"
    ],

    "back pain": [
        "back pain",
        "back hurts",
        "pain in my back"
    ],

    "joint pain": [
        "joint pain",
        "joints hurt",
        "pain in my joints"
    ],

    "chest pain": [
        "chest pain",
        "chest hurts",
        "pain in my chest"
    ],

    "shortness of breath": [
        "shortness of breath",
        "breathlessness",
        "out of breath"
    ],

    "breathing difficulty": [
        "breathing difficulty",
        "difficulty breathing",
        "trouble breathing"
    ],

    "rash": [
        "rash",
        "skin rash"
    ],

    "itching": [
        "itching",
        "itchy",
        "skin is itchy"
    ],

    "sneezing": [
        "sneezing",
        "sneeze",
        "sneezing a lot"
    ]
}


def extract_symptoms(message):

    message = message.lower()

    found_symptoms = []

    # --------------------------------
    # Fever-specific negative cases
    # --------------------------------

    fever_negative_patterns = [
        "low temperature",
        "low temp",
        "temperature is low",
        "temperature is below normal",
        "below normal temperature",
        "no fever",
        "don't have fever",
        "do not have fever",
        "without fever"
    ]

    fever_is_negative = any(
        pattern in message
        for pattern in fever_negative_patterns
    )

    # --------------------------------
    # Extract symptoms
    # --------------------------------

    for symptom, synonyms in SYMPTOM_SYNONYMS.items():

        # Do not detect fever when the user
        # explicitly says low temperature or no fever
        if symptom == "fever" and fever_is_negative:
            continue

        for phrase in synonyms:

            if phrase in message:

                found_symptoms.append(symptom)

                break

    return found_symptoms


def extract_duration(message):

    message = message.lower()

    patterns = [

        # "for 3 days", "for the last 3 days"
        r"\b(?:for\s+)?(?:the\s+last\s+)?\d+\s*(?:day|days)\b",

        # "for 2 weeks", "last 2 weeks"
        r"\b(?:for\s+)?(?:the\s+last\s+)?\d+\s*(?:week|weeks)\b",

        # "for 2 months"
        r"\b(?:for\s+)?(?:the\s+last\s+)?\d+\s*(?:month|months)\b",

        # "for 5 hours"
        r"\b(?:for\s+)?(?:the\s+last\s+)?\d+\s*(?:hour|hours)\b",

        # "since yesterday"
        r"\bsince\s+yesterday\b",

        # "since today"
        r"\bsince\s+today\b",

        # "since last night"
        r"\bsince\s+last\s+night\b",

        # "since this morning"
        r"\bsince\s+this\s+morning\b"
    ]

    for pattern in patterns:

        match = re.search(pattern, message)

        if match:
            return match.group()

    return None


def analyze_message(message):

    symptoms = extract_symptoms(message)

    duration = extract_duration(message)

    return {
        "symptoms": symptoms,
        "duration": duration
    }