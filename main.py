from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Caro Game Server is Running!"

@app.route('/health')
def health():
    return "OK", 200

# LẤY PORT TỪ BIẾN MÔI TRƯỜNG - SỬA CHỖ NÀY
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    print(f"Starting server on port {port}")  # Debug
    app.run(host='0.0.0.0', port=port, debug=False)

application = app
