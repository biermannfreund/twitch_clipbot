import os
import requests
from flask import Flask
from datetime import datetime
from dateutil import parser
import pytz

app = Flask(__name__)

# === KONFIGURATION ===
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("TWITCH_REFRESH_TOKEN")
BROADCASTER_ID = os.getenv("TWITCH_BROADCASTER_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TOKEN_FILE = "token.json"

# === TOKEN HANDLING ===
def get_valid_token():
    # Prüfen, ob ein gültiger Token existiert
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            token_data = f.read().strip()
            if token_data:
                return token_data

    # Falls nicht vorhanden oder leer, neuen holen
    token_url = "https://id.twitch.tv/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    access_token = response.json().get("access_token")

    # speichern
    with open(TOKEN_FILE, 'w') as f:
        f.write(access_token)

    return access_token

ACCESS_TOKEN = get_valid_token()

@app.route('/')
def home():
    return '✅ Clipbot läuft!'

@app.route('/create_clip')
def create_clip():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Client-Id': CLIENT_ID
    }
    params = {
        'broadcaster_id': BROADCASTER_ID,
        'has_delay': False
    }

    response = requests.post("https://api.twitch.tv/helix/clips", headers=headers, params=params)
    data = response.json()

    if response.status_code == 201 and "data" in data and data["data"]:
        clip_id = data["data"][0]["id"]
        clip_url = f"https://clips.twitch.tv/{clip_id}"

        # Clip-Erstellzeitpunkt holen und formatieren
        utc_time = parser.isoparse(data["data"][0]["created_at"])
        local_time = utc_time.astimezone(pytz.timezone("Europe/Berlin"))
        timestamp = local_time.strftime("%d.%m.%Y – %H:%M:%S")
        message = f"📎 Clip vom {timestamp}: {clip_url}"

        # an Discord senden, falls Webhook definiert
        if DISCORD_WEBHOOK_URL:
            try:
                requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
            except:
                pass

        return message
    else:
        return ""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
