from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS  # To enable Cross-Origin Resource Sharing if needed

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (or configure to allow specific domains)

# Set up your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Securely store in environment variables
TELEGRAM_CHAT_ID = "-1002351667124"  # Your Telegram group chat ID
LANA_USER_ID = "7122508724"  # Lana's user ID for direct messages (if necessary)

@app.route("/")
def home():
    return "Webhook is active!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Extract data from the incoming request
        data = request.json
        name = data.get("name")
        date_from = data.get("dateFrom")
        date_till = data.get("dateTill")
        reason = data.get("reason")
        eld = data.get("eld")

        # Check if all fields are provided
        if not all([name, date_from, date_till, reason, eld]):
            return jsonify({"success": False, "error": "Missing fields"}), 400

        # Format and send the message to Telegram
        message = f"📝 TIME-OFF REQUEST\n🔹 Name: {name}\n🔹 Date Off: From {date_from} till {date_till}\n🔹 Reason: {reason}\n🔹 Pause ELD? {eld}"
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        response_group = requests.post(telegram_url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        })

        # If "Pause ELD" is Yes, notify Lana directly
        if eld.lower() == "yes":
            message_lana = "Lana, please pause the ELD!"
            requests.post(telegram_url, json={
                "chat_id": LANA_USER_ID,
                "text": message_lana,
                "parse_mode": "HTML"
            })

        # Check if the message was successfully sent to the group
        if response_group.status_code == 200:
            return jsonify({"success": True, "message": "Request sent successfully!"})
        else:
            return jsonify({"success": False, "error": response_group.json()}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
