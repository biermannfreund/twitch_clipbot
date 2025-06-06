import os
import requests
from flask import Flask
from twitch_token_refresh import get_valid_token

app = Flask(__name__)

# Twitch-Daten
ACCESS_TOKEN = get_valid_token()
CLIENT_ID = "xlua26e5vwxr73ey0k81b8br2i6of1"
BROADCASTER_ID = "1219147036"  # schildis_azubi

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
        return f"🎬 Clip erstellt: {clip_url}"
    elif response.status_code == 404 and "offline" in data.get("message", "").lower():
        return "❌ Clip fehlgeschlagen: Dein Kanal ist aktuell nicht live."
    else:
        return "⚠️ Leider konnte kein Clip erstellt werden. Bitte versuche es später nochmal."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
