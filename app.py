from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1002351667124")  # Replace with actual ID
MESSAGE_THREAD_ID = os.getenv("MESSAGE_THREAD_ID", "59")  # Convert to int if necessary
USER_ID_LANA = os.getenv("USER_ID_LANA", "7122508724")  # Lana's Telegram user ID
USER_ID_RAUAN = os.getenv("USER_ID_RAUAN", "1546986728")  # Rauan's Telegram user ID

# Ensure required environment variables are set
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the environment.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        # Get JSON data from request
        data = request.json

        # Validate required fields
        required_fields = ["name", "dateFrom", "dateTill", "reason", "eld", "truckNumber"]
        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"success": False, "error": "Missing or invalid data"}), 400

        # Extract values
        name = data["name"]
        date_from = data["dateFrom"]
        date_till = data["dateTill"]
        reason = data["reason"]
        eld = data["eld"]
        truck_number = data["truckNumber"]

        # Construct the message for Telegram (group)
        message = (
            f"📝 *TIME-OFF REQUEST* \n\n"
            f"🔹 *Name:* {name}\n"
			f"🔹 *Truck Number:* {truck_number}"
            f"🔹 *Date Off:* From {date_from} till {date_till}\n"
            f"🔹 *Reason:* {reason}\n"
            f"🔹 *Pause ELD?:* {eld}\n"
			f"🔹 *Pause insurance for the truck?:* {truck_number}\n"
            
			⚠️The driver {name} will be back to work on {date_till}
			
        )

        # Prepare payload for group message
        payload_group = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "message_thread_id": int(MESSAGE_THREAD_ID)  # Include thread ID for group message
        }

        # Send message to Telegram group
        response = requests.post(TELEGRAM_API_URL, json=payload_group)
        response.raise_for_status()  # Raise an error for HTTP failures

        # Send a message to Lana in the same thread
        payload_lana = {
            "chat_id": USER_ID_LANA,
            "text": f"Good day Lana (@semitruckZealot)!, please deactivate the ELD for driver {name}. Check on Activate it on {date_till}. 	Thank you!",
            "parse_mode": "Markdown",
            "message_thread_id": int(MESSAGE_THREAD_ID)  # Same thread ID as group message
        }
        requests.post(TELEGRAM_API_URL, json=payload_lana)

        # Send a message to Rauan in the same thread
        payload_rauan = {
            "chat_id": USER_ID_RAUAN,
            "text": f"Good day Rauan (ahura_mazda12)! Please place on hold the insurance for the truck {truck_number}. Thank you!",
            "parse_mode": "Markdown",
            "message_thread_id": int(MESSAGE_THREAD_ID)  # Same thread ID as group message
        }
        requests.post(TELEGRAM_API_URL, json=payload_rauan)

        return jsonify({"success": True, "message": " Your request has been sent successfully!"})

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Telegram API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
