from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Caro Game Server is Running!"

@app.route('/health')
def health():
    return "OK"

@app.route('/api/status')
def status():
    return {"status": "running"}

# REPLIT CẦN CÁI NÀY
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
