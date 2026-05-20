@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AssistIQ Chatbot</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                background-color: #f5f5f5;
            }
            h1 {
                margin-top: 20px;
            }
            .chat-box {
                width: 350px;
                height: 500px;
                border: 1px solid #ccc;
                margin: auto;
                padding: 10px;
                background: white;
                overflow-y: auto;
            }
            .input-box {
                margin-top: 10px;
            }
            input {
                width: 250px;
                padding: 8px;
            }
            button {
                padding: 8px 12px;
            }
        </style>
    </head>
    <body>

        <h1>AssistIQ – AI Chatbot</h1>
        <p>Your intelligent service desk assistant</p>

        <div class="chat-box" id="chat"></div>

        <div class="input-box">
            <input type="text" id="userInput" placeholder="Type your message..." />
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            async function sendMessage() {
                let input = document.getElementById("userInput").value;
                let chat = document.getElementById("chat");

                chat.innerHTML += "<p><b>You:</b> " + input + "</p>";

                let response = await fetch("/webhook", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        queryResult: {
                            intent: {
                                displayName: input
                            }
                        }
                    })
                });

                let data = await response.json();

                chat.innerHTML += "<p><b>Bot:</b> " + data.fulfillmentText + "</p>";

                document.getElementById("userInput").value = "";
                chat.scrollTop = chat.scrollHeight;
            }
        </script>

    </body>
    </html>
    """