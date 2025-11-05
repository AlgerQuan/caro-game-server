from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Caro Game Server is Running!"

@app.route('/health')
def health():
    return "OK"

@app.route('/test')
def test():
    return "Test endpoint works!"

# THÊM DÒNG NÀY - quan trọng
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # THÊM threaded=True để xử lý multiple requests
    app.run(host='0.0.0.0', port=port, threaded=True)
