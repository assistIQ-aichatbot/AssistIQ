from flask import Flask, request, jsonify
import os

# 🔹 Create Flask app
app = Flask(__name__)

# 🔹 UI Route
@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AssistIQ</title>

<style>
body {
    margin: 0;
    font-family: Arial;
    display: flex;
}

/* Sidebar */
.sidebar {
    width: 220px;
    background: #0d6efd;
    color: white;
    height: 100vh;
    padding: 20px;
}

.sidebar h2 {
    margin-bottom: 30px;
}

.sidebar div {
    margin: 15px 0;
    cursor: pointer;
}

/* Main Chat Area */
.main {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.header {
    padding: 15px;
    border-bottom: 1px solid #ddd;
    font-size: 20px;
}

.chat-container {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: #f5f5f5;
}

/* Messages */
.message {
    margin: 10px 0;
    max-width: 60%;
    padding: 10px;
    border-radius: 10px;
}

.user {
    background: #0d6efd;
    color: white;
    margin-left: auto;
}

.bot {
    background: white;
    border: 1px solid #ddd;
}

/* Input */
.input-box {
    display: flex;
    padding: 10px;
    border-top: 1px solid #ddd;
}

input {
    flex: 1;
    padding: 10px;
}

button {
    padding: 10px 15px;
    background: #0d6efd;
    color: white;
    border: none;
}
</style>

</head>

<body>

<!-- Sidebar -->
<div class="sidebar">
    <h2>AssistIQ</h2>
    <div>Chat</div>
    <div>New Conversation</div>
    <div>My Tickets</div>
    <div>Help</div>
</div>

<!-- Main -->
<div class="main">

    <div class="header">
        AssistIQ – AI Chatbot
    </div>

    <div id="chat" class="chat-container">
        <div class="message bot">Hi! I'm AssistIQ. How can I help you?</div>
    </div>

    <div class="input-box">
        <input id="userInput" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>
    </div>

</div>

<script>
async function sendMessage() {
    let input = document.getElementById("userInput").value;
    let chat = document.getElementById("chat");

    if (!input) return;

    chat.innerHTML += `<div class="message user">${input}</div>`;

    let response = await fetch("/webhook", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            queryResult: {
                intent: { displayName: input }
            }
        })
    });

    let data = await response.json();

    chat.innerHTML += `<div class="message bot">${data.fulfillmentText}</div>`;

    document.getElementById("userInput").value = "";
    chat.scrollTop = chat.scrollHeight;
}
</script>

</body>
</html>
"""

# 🔹 Webhook Route
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']

    if intent == "Login Issue":
        reply = "Your login issue has been recorded. Please reset your password."

    elif intent == "Network Issue":
        reply = "Your network issue has been noted. Please check your connection."

    elif intent == "Application Issue":
        reply = "Your application issue has been recorded. Please restart the app."

    else:
        reply = "Please type: Login Issue, Network Issue, or Application Issue"

    return jsonify({
        "fulfillmentText": reply
    })

# 🔹 Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))