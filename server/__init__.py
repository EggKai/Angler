from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable Cross-Origin Resource Sharing globally
    app.register_blueprint(bp)  # Registering the routes blueprint
    return app
