function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();

    if (message === "") {
        return;
    }

const sendButton = document.querySelector(".input-area button");
sendButton.disabled = true;
    // -----------------------------
    // Display User Message
    // -----------------------------

    const userMessage = document.createElement("div");

    userMessage.className = "user-message";

    userMessage.textContent = message;

    chatBox.appendChild(userMessage);

    input.value = "";

    // -----------------------------
// Show Typing Indicator
// -----------------------------
// -----------------------------
// Show Processing Indicator
// -----------------------------

const typingMessage =
    document.createElement("div");

typingMessage.className =
    "bot-message typing-message";

typingMessage.id =
    "typing-indicator";

typingMessage.innerHTML = `
    <div class="processing-title">
        🤖 AI Medical Assistant
    </div>

    <div class="processing-status">
        <span class="loading-dot"></span>
        Analyzing your message...
    </div>
`;

chatBox.appendChild(typingMessage);

chatBox.scrollTop =
    chatBox.scrollHeight;


    // -----------------------------
    // Send Message to Flask
    // -----------------------------

    fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    })

    .then(response => response.json())

    .then(data => {
        sendButton.disabled = false;

        // Remove typing indicator

        const typingIndicator =
            document.getElementById("typing-indicator");

        if (typingIndicator) {

            typingIndicator.remove();

        }


        // -----------------------------
        // Create Bot Message
        // -----------------------------

        const botMessage = document.createElement("div");


        if (data.emergency) {

            botMessage.className =
                "bot-message emergency-message";

        } else {

            botMessage.className =
                "bot-message";

        }


        // -----------------------------
        // NLP Information
        // -----------------------------

        let nlpHTML = "";

if (data.symptoms && data.symptoms.length > 0) {

    nlpHTML += `
        <div class="analysis-card">

            <div class="analysis-header">
                🧠 Analysis Summary
            </div>

            <div class="analysis-item">
                <span class="analysis-label">
                    Symptoms detected
                </span>

                <div class="symptom-tags">
                    ${data.symptoms.map(symptom =>
                        `<span class="symptom-tag">${symptom}</span>`
                    ).join("")}
                </div>
            </div>
    `;

    if (data.duration) {
        nlpHTML += `
            <div class="analysis-item">
                <span class="analysis-label">
                    ⏱️ Duration
                </span>

                <span class="analysis-value">
                    ${data.duration}
                </span>
            </div>
        `;
    }

    if (data.category) {
        nlpHTML += `
            <div class="analysis-item">
                <span class="analysis-label">
                    🤖 Possible symptom pattern
                </span>

                <span class="analysis-value">
                    ${data.category}
                </span>
            </div>
        `;
    }

    if (data.confidence !== null && data.confidence !== undefined) {

        const confidence =
            (Number(data.confidence) * 100).toFixed(1);

        nlpHTML += `
            <div class="analysis-item">
                <span class="analysis-label">
                    📊 ML prediction confidence
                </span>

                <span class="analysis-value">
                    ${confidence}%
                </span>
            </div>

            <small class="confidence-note">
                This is a model prediction score,
                not medical certainty.
            </small>
        `;
    }

    nlpHTML += `</div>`;
}

        // -----------------------------
        // AI Response
        // -----------------------------

        if (data.emergency) {

            botMessage.innerHTML = `

                <div class="emergency-alert">

                    <strong>⚠️ URGENT MEDICAL ALERT</strong>

                    <p>${formatAIResponse(data.response)}</p>

                </div>

            `;

        } else {

            botMessage.innerHTML = `

                ${nlpHTML}

                <div class="ai-response">

                    <strong>🤖 AI Medical Assistant:</strong>

                    <p>${formatAIResponse(data.response)}</p>

                </div>

            `;

        }


        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;

    })


    // -----------------------------
    // Error Handling
    // -----------------------------

.catch(error => {
sendButton.disabled = false;
    console.error("Chat error:", error);

    const typingIndicator =
        document.getElementById("typing-indicator");

    if (typingIndicator) {
        typingIndicator.remove();
    }

    const errorMessage =
        document.createElement("div");

    errorMessage.className = "bot-message";

    errorMessage.innerHTML = `
        <div class="emergency-message">
            <strong>⚠️ Something went wrong</strong>

            <p>
                I couldn't process your request right now.
                Please try again in a moment.
            </p>
        </div>
    `;

    chatBox.appendChild(errorMessage);

    chatBox.scrollTop = chatBox.scrollHeight;
});
}

// --------------------------------
// Format AI Markdown
// --------------------------------
function formatAIResponse(text) {

    // Escape HTML to prevent unwanted HTML injection
    let formatted = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Bold text: **text**
    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    // Headings: ### Heading
    formatted = formatted.replace(
        /^### (.*)$/gm,
        "<h4>$1</h4>"
    );

    formatted = formatted.replace(
        /^## (.*)$/gm,
        "<h3>$1</h3>"
    );

    formatted = formatted.replace(
        /^# (.*)$/gm,
        "<h2>$1</h2>"
    );

    // Bullet points
    formatted = formatted.replace(
        /^[-•] (.*)$/gm,
        "<li>$1</li>"
    );

    // Numbered points
    formatted = formatted.replace(
        /^\d+\.\s(.*)$/gm,
        "<li>$1</li>"
    );

    // Convert consecutive <li> elements into <ul>
    formatted = formatted.replace(
        /(<li>.*?<\/li>\s*)+/gs,
        function(match) {
            return "<ul>" + match + "</ul>";
        }
    );

    // Convert remaining line breaks
    formatted = formatted.replace(/\n/g, "<br>");

    return formatted;
}

// --------------------------------
// Clear Chat
// --------------------------------

function clearChat() {

    fetch("/clear-chat", {

        method: "POST"

    })

    .then(response => response.json())

    .then(data => {

        if (data.success) {

            const chatBox =
                document.getElementById("chat-box");

            chatBox.innerHTML = "";

        }

    })

    .catch(error => {

        console.error("Clear chat error:", error);

    });
}

// --------------------------------
// Enter Key Support
// --------------------------------

document.getElementById("user-input").addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();

    }

});

// --------------------------------
// New Chat
// --------------------------------

function newChat() {

    fetch("/new-chat", {

        method: "POST"

    })

    .then(response => response.json())

    .then(data => {

        if (data.success) {

            const chatBox =
                document.getElementById("chat-box");

            chatBox.innerHTML = `
                <div class="bot-message">

                    <strong>
                        Hello! 👋 I am your AI Medical Assistant.
                    </strong>

                    <p>
                        I can provide general health information,
                        analyze symptoms, and identify possible
                        symptom patterns.
                    </p>

                    <p>
                        I cannot diagnose diseases or prescribe
                        medicines.
                    </p>

                </div>
            `;

        }
            loadChatHistory();
    })

    .catch(error => {

        console.error("New chat error:", error);

    });
}

// --------------------------------
// Load Chat History
// --------------------------------

function loadChatHistory() {

    fetch("/chat-history")
        .then(response => response.json())
        .then(data => {

            const historyList =
                document.getElementById("chat-history-list");

            historyList.innerHTML = "";

            if (!data || data.length === 0) {

                historyList.innerHTML = `
                    <div class="no-history">
                        No previous chats
                    </div>
                `;

                return;
            }

            data.forEach(chat => {

                const chatItem =
                    document.createElement("div");

                chatItem.className = "chat-history-item";

                const title =
                    chat.title || "New Conversation";

                const date =
                    chat.created_at
                        ? new Date(chat.created_at + " UTC")
                            .toLocaleDateString()
                        : "";

                chatItem.innerHTML = `
                    <div class="chat-history-title">
                        💬 ${title}
                    </div>

                    <div class="chat-history-date">
                        ${date}
                    </div>
                `;

                chatItem.onclick = function() {

                    // Remove active state
                    document
                        .querySelectorAll(".chat-history-item")
                        .forEach(item => {
                            item.classList.remove("active");
                        });

                    // Highlight selected chat
                    chatItem.classList.add("active");

                    // Load conversation
                    loadOldChat(chat.session_id);
                };

                historyList.appendChild(chatItem);
            });
        })
        .catch(error => {
            console.error(
                "Chat history error:",
                error
            );
        });
}

// --------------------------------
// Load Old Chat
// --------------------------------

// --------------------------------
// Load Old Chat
// --------------------------------

function loadOldChat(sessionId) {

    fetch(`/load-chat/${sessionId}`)

        .then(response => response.json())

        .then(data => {

            const chatBox =
                document.getElementById("chat-box");

            // Clear current chat
            chatBox.innerHTML = "";


            // --------------------------------
            // Recreate Old Messages
            // --------------------------------

            data.forEach(item => {


                // =================================
                // USER MESSAGE
                // =================================

                if (item.role === "user") {

                    const userMessage =
                        document.createElement("div");

                    userMessage.className =
                        "user-message";

                    userMessage.textContent =
                        item.message;

                    chatBox.appendChild(
                        userMessage
                    );

                }


                // =================================
                // AI RESPONSE
                // =================================

                else if (item.role === "assistant") {

                    const botMessage =
                        document.createElement("div");

                    botMessage.className =
                        "bot-message";


                    // --------------------------------
                    // NLP + ML Information
                    // --------------------------------

                    let nlpHTML = "";


                    // Symptoms

                    if (item.symptoms) {

                        const symptoms =
                            item.symptoms.split(",");

                        nlpHTML += `
                            <div class="nlp-section">

                                <strong>
                                    🧠 Symptoms detected:
                                </strong>

                                <ul>
                        `;

                        symptoms.forEach(symptom => {

                            nlpHTML += `
                                <li>
                                    ${symptom.trim()}
                                </li>
                            `;

                        });

                        nlpHTML += `
                                </ul>

                            </div>
                        `;
                    }


                    // Duration

                    if (item.duration) {

                        nlpHTML += `
                            <div class="nlp-section">

                                <strong>
                                    ⏱️ Duration:
                                </strong>

                                <span>
                                    ${item.duration}
                                </span>

                            </div>
                        `;
                    }


                    // ML Category

                    if (item.category) {

                        nlpHTML += `
                            <div class="nlp-section">

                                <strong>
                                    🤖 ML symptom pattern:
                                </strong>

                                <span>
                                    ${item.category}
                                </span>

                            </div>
                        `;
                    }


                    // Confidence

                  if (
                     item.confidence !== null &&
                     item.confidence !== undefined
                 ) {

                     const confidence =
                         (
                             Number(item.confidence) * 100
                         ).toFixed(1);

                     nlpHTML += `
                         <div class="nlp-section">

                             <strong>
                                 📊 ML prediction confidence:
                             </strong>

                             <span>
                                 ${confidence}%
                             </span>

                             <small class="confidence-note">
                                 This is a model prediction score,
                                 not medical certainty.
                             </small>

                         </div>
                     `;
                 }

                    // --------------------------------
                    // AI Response
                    // --------------------------------

                    botMessage.innerHTML = `

                        ${nlpHTML}

                        <div class="ai-response">

                            <strong>
                                🤖 AI Medical Assistant:
                            </strong>

                            <p>
                                ${formatAIResponse(item.message)}
                            </p>

                        </div>

                    `;


                    chatBox.appendChild(
                        botMessage
                    );

                }

            });


            // Scroll to bottom

            chatBox.scrollTop =
                chatBox.scrollHeight;

        })

        .catch(error => {

            console.error(
                "Load chat error:",
                error
            );

        });
    }