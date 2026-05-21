from flask import Flask, request, jsonify, render_template
import os
import random

app = Flask(__name__)

# 🔹 Home page
@app.route('/')
def home():
    return render_template("index.html")

# 🔹 Memory
user_state = {}

# 🔹 Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']
    text = req['queryResult']['queryText'].lower()
    session = req['session']

    # 🔴 STEP 1: Escalation (ticket creation)
    if intent == "Escalation" or "still not working" in text or "not resolved" in text:
        ticket_id = "TCKT" + str(random.randint(10000, 99999))

        reply = f"""
I understand your issue is not resolved.

Your support ticket has been created.
Ticket ID: {ticket_id}

Our team will get back to you soon.
"""
        return jsonify({"fulfillmentText": reply})

    # 🟢 STEP 2: Provide solution FIRST
    if "login" in text:
        reply = "Please try resetting your password using 'Forgot Password'. Let me know if it works."

    elif "vpn" in text or "network" in text:
        reply = "Check your internet connection and try reconnecting VPN. Let me know if it works."

    elif "app" in text or "error" in text:
        reply = "Try restarting the application or reinstalling it. Let me know if it works."

    elif "printer" in text:
        reply = "Check printer connection and restart the printer. Let me know if it works."

    else:
        reply = "Please describe your issue. I can help with login, network, application, or system issues."

    return jsonify({
        "fulfillmentText": reply
    })

# 🔹 Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))