from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Verwende Umgebungsvariable für Discord Relay URL (anstatt direkten Webhook)
DISCORD_RELAY_URL = os.getenv("DISCORD_RELAY_URL") 


def send_discord_message(message):
    if not DISCORD_RELAY_URL:
        print("❌ Kein DISCORD_RELAY_URL gesetzt!")
        return None
    try:
        data = {"message": message}
        response = requests.post(DISCORD_RELAY_URL, json=data)
        print(f"✅ Discord-Antwort: {response.status_code} – {response.text[:100]}")
        return response
    except Exception as e:
        print(f"❌ Fehler beim Senden der Nachricht: {e}")
        return None


@app.route('/test_webhook')
def test_webhook():
    clip_url = request.args.get("clip", "https://example.com/dein-clip")
    silent = request.args.get("silent", "0") == "1"

    timestamp = datetime.now().strftime("%d.%m.%Y um %H:%M:%S")
    message = f"📎 Clip vom {timestamp}: [Klicke hier, um zum Clip zu gelangen]({clip_url})"

    if not silent:
        send_discord_message(message)
    else:
        print("🟡 Discord-Ausgabe übersprungen (silent mode aktiviert).")
        print(f"Vorschau: {message}")

    return jsonify({"status": "success", "preview": message})


@app.route("/")
def index():
    return "Twitch Clipbot Service läuft. Benutze /test_webhook für Tests."


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
