import os
import requests
from flask import Flask

app = Flask(__name__)

# Deine festen Twitch-Daten
ACCESS_TOKEN = "h75r8winxevcnthjc4blxjlyngfppg"
CLIENT_ID = "xlua26e5vwxr73ey0k81b8br2i6of1"
BROADCASTER_ID = "1219147036"  # gleich unten erklärt

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

    if "data" in data and data["data"]:
        clip_id = data["data"][0]["id"]
        clip_url = f"https://clips.twitch.tv/{clip_id}"
        return f"🎬 Clip erstellt: {clip_url}"
    else:
        return f"❌ Fehler beim Erstellen: {data}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
