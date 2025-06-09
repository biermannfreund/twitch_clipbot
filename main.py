from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

def send_discord_message(webhook_url, message):
    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        print(f"✅ Discord-Testantwort: {response.status_code} – {response.text[:100]}")
        return response
    except Exception as e:
        print(f"❌ Fehler beim Senden der Nachricht: {e}")
        return None

@app.route('/test_webhook')
def test_webhook():
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    clip_url = request.args.get("clip", "https://example.com/dein-clip")
    silent = request.args.get("silent", "0") == "1"

    timestamp = datetime.now().strftime("%d.%m.%Y um %H:%M Uhr")
    message = f"📎 Clip vom {timestamp}: [Klicke hier, um zum Clip zu gelangen]({clip_url})"

    if not silent and webhook_url:
        send_discord_message(webhook_url, message)
    else:
        print("🟡 Discord-Ausgabe übersprungen (silent mode aktiviert oder kein Webhook konfiguriert).")
        print(f"Vorschau: {message}")

    return "✅ Test abgeschlossen"

if __name__ == '__main__':
    app.run(debug=True)
