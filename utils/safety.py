# --------------------------------
# Emergency / Red-Flag Symptoms
# --------------------------------

EMERGENCY_KEYWORDS = [

    # Breathing
    "difficulty breathing",
    "can't breathe",
    "cannot breathe",
    "shortness of breath",
    "breathing difficulty",
    "not able to breathe",

    # Chest
    "severe chest pain",
    "crushing chest pain",
    "chest pain",

    # Consciousness
    "unconscious",
    "passed out",
    "fainted",
    "loss of consciousness",

    # Stroke
    "stroke",
    "face drooping",
    "slurred speech",
    "sudden weakness",

    # Seizure
    "seizure",
    "convulsion",

    # Bleeding
    "severe bleeding",
    "heavy bleeding",
    "uncontrolled bleeding",

    # Poisoning / Overdose
    "overdose",
    "poisoning",

    # Self-harm emergency
    "suicide",
    "suicidal",
    "kill myself",
    "want to die"
]


def check_emergency(message):

    message = message.lower()

    for keyword in EMERGENCY_KEYWORDS:

        if keyword in message:
            return True

    return False