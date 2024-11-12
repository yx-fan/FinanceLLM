from flask import Flask
from pymongo import MongoClient, errors
from .config import Config
from .routes.api import api_blueprint
from .utils.logger import setup_logging
from .errors.handlers import register_error_handlers
from .utils.database import initialize_mongo 

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup logging
    setup_logging()

    # Initialize MongoDB
    initialize_mongo(app)

    # Register API routes
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Register error handlers
    register_error_handlers(app)

    return app
