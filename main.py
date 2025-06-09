import os
import requests
from flask import Flask
from twitch_token_refresh import get_valid_token
from datetime import datetime
from dateutil import parser
import pytz
import time

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Clipbot läuft!'

@app.route('/test_webhook')
def test_webhook():
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        try:
            timestamp = "09.06.2025 – 21:57:09"
            clip_url = "https://clips.twitch.tv/FakeTestClipURL"
            message = f"📎 Clip vom {timestamp}: [Klicke hier, um zum Clip zu gelangen]({clip_url})"
            r = requests.post(webhook_url, json={"content": message})
            print(f"✅ Discord-Testantwort: {r.status_code} – {r.text}")
            return "✅ Testnachricht gesendet."
        except Exception as e:
            return f"❌ Fehler beim Senden: {e}"
    else:
        return "❌ Kein DISCORD_WEBHOOK_URL definiert."

@app.route('/create_clip')
def create_clip():
    access_token = get_valid_token()
    client_id = os.getenv("TWITCH_CLIENT_ID")
    broadcaster_id = os.getenv("TWITCH_BROADCASTER_ID")
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id
    }
    params = {
        'broadcaster_id': broadcaster_id,
        'has_delay': False
    }

    response = requests.post("https://api.twitch.tv/helix/clips", headers=headers, params=params)
    data = response.json()

    if response.status_code == 202 and "data" in data and data["data"]:
        clip_id = data["data"][0]["id"]
        clip_url = f"https://clips.twitch.tv/{clip_id}"

        # Warte kurz, bis Clip fertig ist
        time.sleep(6)

        # Clip-Infos erneut abrufen, um Erstellungszeit zu bekommen
        clip_info_response = requests.get(
            "https://api.twitch.tv/helix/clips",
            headers=headers,
            params={"id": clip_id}
        )
        clip_info = clip_info_response.json()

        try:
            created_at = clip_info["data"][0].get("created_at")
            print(f"📎 Clip created_at: {created_at}")
            if created_at:
                utc_time = parser.isoparse(created_at)
                local_time = utc_time.astimezone(pytz.timezone("Europe/Berlin"))
                timestamp = local_time.strftime("%d.%m.%Y – %H:%M:%S")
            else:
                timestamp = "Unbekannt"
        except Exception as e:
            print(f"❌ Fehler beim Timestamp-Parsen: {e}")
            timestamp = "Unbekannt"

        message = f"📎 Clip vom {timestamp}: [Klicke hier, um zum Clip zu gelangen]({clip_url})"
        print(f"📤 Sende Nachricht an Discord: {message}")

        if webhook_url:
            try:
                r = requests.post(webhook_url, json={"content": message})
                print(f"✅ Discord-Antwort: {r.status_code} – {r.text}")
                if r.status_code >= 200 and r.status_code < 300:
                    return message
                else:
                    return f"❌ Fehler beim Discord-Post: {r.status_code} – {r.text}"
            except Exception as e:
                return f"❌ Fehler beim Discord-Post: {e}"
        else:
            return "⚠️ Kein DISCORD_WEBHOOK_URL definiert."
    else:
        return f"❌ Fehler bei Clip-Erstellung: {response.status_code} – {data}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
