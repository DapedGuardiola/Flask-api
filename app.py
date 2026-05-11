from flask import Flask
from config import Config
app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return {'status': 'ok', 'message': 'Flask is running'}

if __name__ == '__main__':
    app.run(debug=Config.Debug,
            port=Config.PORT)