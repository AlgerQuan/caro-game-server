from flask import Flask
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return "Caro Game Server is Running!"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    print("🚀 Server starting...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
