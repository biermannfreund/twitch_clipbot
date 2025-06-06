from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Clipbot ist online!'

@app.route('/create_clip')
def create_clip():
    return '🎬 Beispiel-Clip erstellt! (Platzhalter)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
