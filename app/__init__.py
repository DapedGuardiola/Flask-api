from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.routes.saw_routes import saw_bp
    from app.routes.cbf_routes import cbf_bp
    
    app.register_blueprint(saw_bp)
    app.register_blueprint(cbf_bp)
    
    return app