from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Load Telegram Bot Token securely from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Store token securely in Render environment variables
TELEGRAM_CHAT_ID = "-1002351667124"  # Your Telegram group chat ID
MESSAGE_THREAD_ID = 59  # Your thread ID for the specific group thread
LANA_USER_ID = "7122508724"  # Lana's Telegram user ID (direct message)

@app.route("/")
def home():
    return "🚀 Webhook is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Get the data sent in the form submission
        data = request.json
        name = data.get("name")
        date_from = data.get("dateFrom")
        date_till = data.get("dateTill")
        reason = data.get("reason")
        eld = data.get("eld")

        # Check if all required fields are present
        if not all([name, date_from, date_till, reason, eld]):
            return jsonify({"success": False, "error": "Missing fields"}), 400

        # Format the message to send to Telegram group
        message = f"""📝 TIME-OFF REQUEST
🔹 Name: {name}
🔹 Date Off: From {date_from} till {date_till}
🔹 Reason: {reason}
🔹 Pause ELD? {eld}"""

        # Send the message to the Telegram group
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        response_group = requests.post(telegram_url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "message_thread_id": MESSAGE_THREAD_ID
        })

        # If "Pause ELD" is Yes, send a message to Lana
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

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
