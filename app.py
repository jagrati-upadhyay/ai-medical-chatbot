from flask import Flask, render_template, request, jsonify
from groq import Groq

from utils.safety import check_emergency
from utils.nlp import analyze_message
from utils.ml_model import predict_category

from database import (
    init_db,
    save_message,
    clear_history,
    create_session,
    get_sessions,
    get_session_history
)

import os
import traceback


app = Flask(__name__)


# --------------------------------
# Conversation History
# --------------------------------

conversation_history = []


# --------------------------------
# Initialize Database
# --------------------------------

init_db()


# --------------------------------
# Create Current Chat Session
# --------------------------------

current_session_id = create_session()


# --------------------------------
# Groq Client
# --------------------------------

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# --------------------------------
# Home Page
# --------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------
# Chat API
# --------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json() or {}

    user_message = data.get("message", "").strip()


    # --------------------------------
    # Empty Message Check
    # --------------------------------

    if not user_message:

        return jsonify({
            "response": "Please enter a message.",
            "emergency": False,
            "symptoms": [],
            "duration": None,
            "category": None,
            "confidence": None
        })


    # --------------------------------
    # STEP 1: Emergency Check
    # --------------------------------

    message = user_message.lower()

    if check_emergency(message):

        return jsonify({

            "response": (
                "⚠️ This message may describe a potentially serious "
                "medical situation. Please seek urgent medical attention "
                "or contact your local emergency medical service. "
                "Do not rely on this chatbot for emergency care."
            ),

            "emergency": True,

            "symptoms": [],

            "duration": None,

            "category": None,

            "confidence": None
        })


    # --------------------------------
    # STEP 2: NLP Symptom Analysis
    # --------------------------------

    analysis = analyze_message(user_message)

    symptoms = analysis["symptoms"]

    duration = analysis["duration"]


    # --------------------------------
    # STEP 3: ML Prediction
    # --------------------------------

    predicted_category = None

    prediction_confidence = None


    if symptoms:

        predicted_category, prediction_confidence = (
            predict_category(symptoms)
        )


    # --------------------------------
    # Save User Message + Analysis
    # --------------------------------

    save_message(
        current_session_id,
        "user",
        user_message,
        symptoms=", ".join(symptoms) if symptoms else None,
        duration=duration,
        category=predicted_category,
        confidence=prediction_confidence
    )


    # --------------------------------
    # STEP 4: Prepare NLP Information
    # --------------------------------

    if symptoms:

        symptom_context = ", ".join(symptoms)

    else:

        symptom_context = "No specific symptoms detected"


    if duration:

        duration_context = duration

    else:

        duration_context = "Not provided"


    # --------------------------------
    # STEP 5: Prepare ML Information
    # --------------------------------

    if predicted_category:

        category_context = predicted_category

    else:

        category_context = "No category predicted"


    if prediction_confidence is not None:

        confidence_context = (
            f"{prediction_confidence * 100:.1f}%"
        )

    else:

        confidence_context = "Not available"


    # --------------------------------
    # STEP 6: Prepare AI Prompt
    # --------------------------------

    system_prompt = f"""
You are an AI Medical Information Assistant.

Your purpose is to provide general health information
for educational purposes.

You are NOT a doctor and must NOT provide a medical diagnosis.

IMPORTANT SAFETY RULES:

1. Do not diagnose the user.
2. Do not claim that the user definitely has a disease.
3. Do not prescribe medicines.
4. Do not provide medication dosages.
5. Do not tell the user to start or stop prescription medication.
6. Do not replace a qualified doctor or healthcare professional.
7. Use simple and understandable language.
8. Use cautious language such as:
   "may be associated with",
   "can sometimes occur with",
   "one possibility is".
9. Do not claim certainty from the ML prediction.
10. Clearly explain that the ML category is only a
    model-generated symptom pattern and is NOT a diagnosis.
11. If symptoms sound potentially serious, recommend
    seeking appropriate medical care.

Information extracted by our system:

Symptoms:
{symptom_context}

Duration:
{duration_context}

Possible symptom pattern category:
{category_context}

ML prediction confidence:
{confidence_context}

IMPORTANT:

The ML prediction is only a model-generated pattern.
It must never be presented as a medical diagnosis.

Generate the response using this structure:

### What your symptoms may indicate

Briefly explain possible general causes or symptom
patterns based on the provided information.

Do not diagnose the user.

### What you can do

Give general, low-risk self-care and monitoring
suggestions.

Do not prescribe medication or dosage.

### When to seek medical care

Explain what worsening or concerning symptoms would
justify contacting a healthcare professional or seeking
urgent medical care.

### Important note

Clearly state that this information is for educational
purposes and that the ML prediction is not a medical diagnosis.

Keep the response clear, concise and easy to understand.
"""


    # --------------------------------
    # STEP 7: Prepare Messages
    # --------------------------------

    messages = [

        {
            "role": "system",
            "content": system_prompt
        }

    ]


    # --------------------------------
    # Add Previous Conversation
    # --------------------------------

    messages.extend(
        conversation_history
    )


    # --------------------------------
    # Add Current User Message
    # --------------------------------

    messages.append({

        "role": "user",

        "content": user_message

    })


    # --------------------------------
    # STEP 8: Groq API Call
    # --------------------------------

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=messages

        )

        bot_response = response.choices[0].message.content


    except Exception as e:

        print("================================")

        print("Groq API Error:")

        print(repr(e))

        traceback.print_exc()

        print("================================")


        bot_response = (
            "I'm sorry, but I'm currently unable to generate "
            "a response. Please try again in a moment. "
            "If your symptoms are serious or worsening, "
            "please contact a healthcare professional."
        )


    # --------------------------------
    # STEP 9: Save AI Response
    # --------------------------------

    save_message(

        current_session_id,

        "assistant",

        bot_response,

        symptoms=", ".join(symptoms) if symptoms else None,

        duration=duration,

        category=predicted_category,

        confidence=prediction_confidence

    )


    # --------------------------------
    # STEP 10: Save Conversation
    # --------------------------------

    conversation_history.append({

        "role": "user",

        "content": user_message

    })


    conversation_history.append({

        "role": "assistant",

        "content": bot_response

    })


    # --------------------------------
    # STEP 11: Send Response
    # --------------------------------

    return jsonify({

        "response": bot_response,

        "emergency": False,

        "symptoms": symptoms,

        "duration": duration,

        "category": predicted_category,

        "confidence": prediction_confidence

    })


# --------------------------------
# Clear Chat
# --------------------------------

@app.route("/clear-chat", methods=["POST"])
def clear_chat():

    global conversation_history

    conversation_history.clear()

    clear_history(current_session_id)

    return jsonify({

        "success": True,

        "message": "Conversation cleared successfully."

    })


# --------------------------------
# New Chat
# --------------------------------

@app.route("/new-chat", methods=["POST"])
def new_chat():

    global conversation_history

    global current_session_id


    # Clear current memory

    conversation_history.clear()


    # Create completely new session

    current_session_id = create_session()


    return jsonify({

        "success": True,

        "message": "New chat started."

    })


# --------------------------------
# Get Chat History
# --------------------------------

@app.route("/chat-history", methods=["GET"])
def chat_history():

    sessions = get_sessions()

    result = []


    for session_id, created_at in sessions:

        history = get_session_history(session_id)

        title = "New Chat"


        for role, message, symptoms, duration, category, confidence in history:

            if role == "user":

                if symptoms:

                    symptom_list = [

                        symptom.strip()

                        for symptom in symptoms.split(",")

                        if symptom.strip()

                    ]


                    if len(symptom_list) > 0:

                        if len(symptom_list) == 1:

                            title = symptom_list[0].title()


                        elif len(symptom_list) == 2:

                            title = (

                                symptom_list[0].title()

                                + " & "

                                + symptom_list[1].title()

                            )


                        else:

                            title = (

                                symptom_list[0].title()

                                + " & "

                                + symptom_list[1].title()

                                + "..."

                            )


                    else:

                        title = message[:35]


                else:

                    title = message[:35]


                break


        result.append({

            "session_id": session_id,

            "title": title,

            "created_at": created_at

        })


    return jsonify(result)


# --------------------------------
# Load Specific Chat
# --------------------------------

@app.route("/load-chat/<session_id>", methods=["GET"])
def load_chat(session_id):

    global current_session_id

    global conversation_history


    # --------------------------------
    # Make Selected Chat Active
    # --------------------------------

    current_session_id = session_id


    # --------------------------------
    # Clear Current Memory
    # --------------------------------

    conversation_history.clear()


    # --------------------------------
    # Get Selected Chat
    # --------------------------------

    history = get_session_history(session_id)

    result = []


    # --------------------------------
    # Load Conversation Into Memory
    # --------------------------------

    for (
        role,
        message,
        symptoms,
        duration,
        category,
        confidence
    ) in history:

        conversation_history.append({

            "role": role,

            "content": message

        })


        # --------------------------------
        # Send Complete Information
        # To Frontend
        # --------------------------------

        result.append({

            "role": role,

            "message": message,

            "symptoms": symptoms,

            "duration": duration,

            "category": category,

            "confidence": confidence

        })


    return jsonify(result)


# --------------------------------
# Run Flask
# --------------------------------

if __name__ == "__main__":

    app.run(debug=True)