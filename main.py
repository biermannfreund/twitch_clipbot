from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# === ENV ===
CLOUDFLARE_RELAY_URL = os.environ.get("DISCORD_RELAY_URL")
BROADCASTER_ID = os.environ.get("TWITCH_BROADCASTER_ID")
CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("TWITCH_REFRESH_TOKEN")
TOKEN_FILE = os.environ.get("TWITCH_TOKEN_FILE", "token.json")

# === Token holen oder erneuern ===
def get_access_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)
            return token_data.get("access_token")

    url = "https://id.twitch.tv/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    token_data = r.json()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    return token_data["access_token"]

# === Clip erstellen ===
@app.route("/create_clip", methods=["GET"])
def create_clip():
    try:
        token = get_access_token()
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {token}"
        }
        params = {"broadcaster_id": BROADCASTER_ID, "has_delay": False}
        r = requests.post("https://api.twitch.tv/helix/clips", headers=headers, params=params)
        r.raise_for_status()
        clip_data = r.json()
        clip_url = f"https://clips.twitch.tv/{clip_data['data'][0]['id']}"

        # Discord via Relay posten
        discord_resp = requests.post(
            CLOUDFLARE_RELAY_URL,
            json={"message": f"📎 Clip vom Twitch-Stream: {clip_url}"}
        )

        # Fehler im Discord Relay?
        if discord_resp.status_code != 200:
            return jsonify({"error": "Discord Relay Fehler", "details": discord_resp.text}), 500

        # Rückmeldung an Twitch Chat (SE)
        return jsonify({
            "status": "✅ Clip der letzten Minute wurde erstellt und im Discord gepostet! 🎬",
            "clip": clip_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return "✅ Twitch Clipbot läuft!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
