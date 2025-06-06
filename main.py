import os
import requests
from flask import Flask
from twitch_token_refresh import get_valid_token
from datetime import datetime
from dateutil import parser
import pytz

app = Flask(__name__)

# Twitch-Daten
ACCESS_TOKEN = get_valid_token()
CLIENT_ID = "xlua26e5vwxr73ey0k81b8br2i6of1"
BROADCASTER_ID = "1219147036"  # schildis_azubi
DISCORD_WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1380373468222193674/fYxgiuvMn3xlsaVTXwDk-UlC2ACMqSvNklz6CYnrTfUiT_fCQwPxXp8W29ESzTco1MSRL")  # muss in Render gesetzt werden

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

        # Echten Clip-Erstellzeitpunkt auslesen und formatieren
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
