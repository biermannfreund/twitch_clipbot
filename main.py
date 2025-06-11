from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Cloudflare Worker Relay URL
CLOUDFLARE_RELAY_URL = "https://discord-relay.biermannfreund.workers.dev"

@app.route("/create_clip", methods=["GET"])
def create_clip():
    # 1. Twitch Clip generieren (hier nur Dummy-URL als Platzhalter)
    clip_url = "https://clips.twitch.tv/FancyTestClip123"

    # 2. Sende an Cloudflare Relay
    try:
        resp = requests.post(
            CLOUDFLARE_RELAY_URL,
            json={"message": f"🎬 Neuer Clip: {clip_url}"}
        )
        if resp.status_code != 200:
            return jsonify({"error": "Cloudflare Relay fehlgeschlagen", "details": resp.text}), 500

        return jsonify({
            "status": "✅ Clip wurde erstellt und im Discord gepostet!",
            "clip": clip_url
        })

    except Exception as e:
        return jsonify({"error": "Fehler beim Clip erstellen", "details": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return "✅ Twitch Clipbot läuft!"

