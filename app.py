from flask import Flask, request, jsonify, render_template
import os
import random

app = Flask(__name__)

# 🔹 Store tickets (in memory)
tickets = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/tickets', methods=['GET'])
def get_tickets():
    return jsonify(tickets)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']
    text = req['queryResult']['queryText'].lower()

    # 🔴 Ticket creation
    if intent == "Escalation" or "not working" in text or "not resolved" in text:
        ticket_id = "TCKT" + str(random.randint(10000, 99999))

        ticket = {
            "id": ticket_id,
            "type": text,
            "status": "Open"
        }

        tickets.append(ticket)  # ✅ store ticket

        reply = f"""
Your issue has been escalated.

🎫 Ticket ID: {ticket_id}
Status: Open

Our team will contact you soon.
"""
        return jsonify({"fulfillmentText": reply})

    # 🟢 Solutions
    if "login" in text:
        reply = "Please reset your password using 'Forgot Password'. Let me know if it works."

    elif "vpn" in text or "network" in text:
        reply = "Check your internet connection and reconnect VPN."

    elif "app" in text:
        reply = "Restart or reinstall the application."

    elif "printer" in text:
        reply = "Check printer connection and restart it."

    else:
        reply = "Please describe your issue (login, network, app, printer)."

    return jsonify({"fulfillmentText": reply})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))