import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Clipbot ist online!'

@app.route('/create_clip')
def create_clip():
    return '🎬 Beispiel-Clip erstellt! (Platzhalter)'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
