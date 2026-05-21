from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# 🔹 Home page (loads your Messenger UI)
@app.route('/')
def home():
    return render_template("index.html")

# 🔹 Webhook (Dialogflow → Flask)
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']

    if intent == "Login Issue":
        reply = "Your login issue has been recorded. Please reset your password or contact support."

    elif intent == "Network Issue":
        reply = "Your network issue has been noted. Please check your connection or VPN."

    elif intent == "Application Issue":
        reply = "Your application issue has been recorded. Please restart the application."

    else:
        reply = "I'm here to help. Please describe your issue."

    return jsonify({
        "fulfillmentText": reply
    })

# 🔹 Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))