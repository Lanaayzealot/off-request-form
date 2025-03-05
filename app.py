from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Time-Off Request API is Running!"

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.json
        name = data.get("name")
        date_from = data.get("dateFrom")
        date_till = data.get("dateTill")
        reason = data.get("reason")
        eld = data.get("eld")

        if not all([name, date_from, date_till, reason, eld]):
            return jsonify({"success": False, "error": "Missing fields"}), 400

        message = f"""📝 TIME-OFF REQUEST
🔹 Name: {name}
🔹 Date Off: From {date_from} till {date_till}
🔹 Reason: {reason}
🔹 Pause ELD? {eld}"""

        TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Secure Token
        TELEGRAM_CHAT_ID = "-1002351667124"  # Telegram group ID
        MESSAGE_THREAD_ID = 59
        LANA_USER_ID = "7122508724"  # Lana's Telegram user ID

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        # Send message to group
        response_group = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "message_thread_id": MESSAGE_THREAD_ID
        })

        # If "Pause ELD" is Yes, send message to Lana
        if eld.lower() == "yes":
            message_lana = "Lana, please pause the ELD!"
            response_lana = requests.post(url, json={
                "chat_id": LANA_USER_ID,
                "text": message_lana,
                "parse_mode": "HTML"
            })

        if response_group.status_code == 200:
            return jsonify({"success": True, "message": "Request sent successfully!"})
        else:
            return jsonify({"success": False, "error": response_group.json()}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
