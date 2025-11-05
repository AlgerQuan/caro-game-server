from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Caro Game Server is Running!"

@app.route('/health', methods=['GET', 'HEAD'])
def health():
    return "OK", 200

@app.route('/api/status')
def status():
    return {"status": "running", "port": os.environ.get('PORT', '5000')}, 200

# Railway đang set PORT=8080
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    print(f"🚀 Starting Caro Game Server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

application = app
