import requests
import json
import time
import os

# === KONFIGURATION ===
CLIENT_ID = "xlua26e5vwxr73ey0k81b8br2i6of1"
CLIENT_SECRET = "riuq74p6hqnhv2duek2lds6gri4hlb"
REFRESH_TOKEN = "bd463ohkghsubc9ggs8xyvmg7rhy8ni0knmh7nkt4j6x4h0rwu"
TOKEN_FILE = "token.json"


def refresh_access_token():
    print("🔄 Aktualisiere Access-Token mit Refresh-Token...")
    url = "https://id.twitch.tv/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        new_token = response.json()
        print("✅ Neuer Token erhalten!")
        # Ablaufzeit berechnen
        expires_at = int(time.time()) + new_token["expires_in"]
        new_token["expires_at"] = expires_at
        with open(TOKEN_FILE, "w") as f:
            json.dump(new_token, f, indent=2)
        return new_token
    else:
        print("❌ Fehler beim Aktualisieren des Tokens:", response.text)
        return None


def get_valid_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)
        if int(time.time()) < token_data.get("expires_at", 0):
            print("🟢 Token ist noch gültig.")
            return token_data["access_token"]
        else:
            print("⚠️ Token ist abgelaufen.")
            return refresh_access_token()["access_token"]
    else:
        print("🚫 Keine gespeicherte Token-Datei gefunden. Aktualisiere...")
        return refresh_access_token()["access_token"]


if __name__ == "__main__":
    access_token = get_valid_token()
    print("💡 Aktueller gültiger Token:", access_token)
