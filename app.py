from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot token
TELEGRAM_CHAT_ID = "-1002351667124"  # Replace with your Telegram group chat ID
MESSAGE_THREAD_ID = 59  # Replace with your specific thread ID (if required)
USER_ID = "7122508724"  # Lana's Telegram user ID

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        # Get JSON data from request
        data = request.json

        # Validate required fields
        required_fields = ["name", "dateFrom", "dateTill", "reason", "eld"]
        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"success": False, "error": "Missing or invalid data"}), 400

        # Extract values
        name = data["name"]
        date_from = data["dateFrom"]
        date_till = data["dateTill"]
        reason = data["reason"]
        eld = data["eld"]

        # Construct the message for Telegram
        message = (
            f"📝 *TIME-OFF REQUEST* \n\n"
            f"🔹 *Name:* {name}\n"
            f"🔹 *Date Off:* From {date_from} till {date_till}\n"
            f"🔹 *Reason:* {reason}\n"
            f"🔹 *Pause ELD?* {eld}"
        )

        # Telegram API URL for group message
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "message_thread_id": MESSAGE_THREAD_ID  # Send to a specific thread if needed
        }

        # Send message to Telegram group
        response = requests.post(telegram_url, json=payload)
        response_data = response.json()

        # If Telegram request failed
        if not response_data.get("ok"):
            return jsonify({"success": False, "error": "Failed to se
