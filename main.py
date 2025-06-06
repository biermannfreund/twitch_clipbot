import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    code = request.args.get('code')
    if code:
        return f'✅ Auth-Code erhalten: {code}'
    return '✅ Clipbot ist online!'

@app.route('/create_clip')
def create_clip():
    return '🎬 Beispiel-Clip erstellt! (Platzhalter)'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
