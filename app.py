from flask import Flask
from config import Config
from app.routes.saw_routes import saw_bp
from app.routes.edas_routes import edas_bp
from app.routes.cbf_routes import cbf_bp
from app.routes.compute_routes import compute_bp

app = Flask(__name__)
app.register_blueprint(saw_bp)
app.register_blueprint(edas_bp)
app.register_blueprint(cbf_bp)
app.register_blueprint(compute_bp)

@app.route('/ping', methods=['GET'])
def ping():
    return {'status': 'ok', 'message': 'Flask is running'}

if __name__ == '__main__':
    app.run(debug=Config.Debug,
            port=Config.PORT)