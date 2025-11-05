from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Caro Game Server is Running!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/api/test')
def test():
    return {"status": "success", "message": "Server is working"}, 200

# QUAN TRỌNG: Dùng biến môi trường PORT
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)

application = app
