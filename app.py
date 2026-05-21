from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# 🔹 Home page (loads your Messenger UI)
@app.route('/')
def home():
    return render_template("index.html")

# 🔹 Webhook (Dialogflow → Flask)
user_state = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']
    session = req['session']  # unique user

    if session not in user_state:

        if intent == "Login Issue":
            user_state[session] = "login"
            reply = "Sure, I can help with that. Please describe your issue."

        elif intent == "Network Issue":
            user_state[session] = "network"
            reply = "Network issue detected. Please describe your problem."

        elif intent == "Application Issue":
            user_state[session] = "application"
            reply = "Application issue detected. Please describe your problem."

        else:
            reply = "Please tell me your issue type (login, network, application)."

    else:
        import random
        issue_type = user_state[session]

        ticket_id = "TCKT" + str(random.randint(10000, 99999))

        reply = f"""
Thank you! Your {issue_type} issue has been recorded.
Our team will get back to you soon.
Ticket ID: {ticket_id}
"""

        del user_state[session]

    return jsonify({
        "fulfillmentText": reply
    })

# 🔹 Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))