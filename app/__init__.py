from flask import Flask
from pymongo import MongoClient, errors
from .config import Config
from .routes.api import api_blueprint
from .utils.logger import setup_logging
from .errors.handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    setup_logging()


    try:
        # Try to connect to MongoDB
        mongo_client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)
        
        # Ping the server to check if the connection is successful
        mongo_client.admin.command("ping")
        
        # Set the default database for the app
        app.mongo_client = mongo_client
        app.db = mongo_client.get_default_database()
        app.logger.info("MongoDB connected successfully!")
    except errors.ServerSelectionTimeoutError as err:
        # Handle connection errors
        app.logger.error(f"Failed to connect to MongoDB: {err}")
        app.mongo_client = None
        app.db = None


    app.register_blueprint(api_blueprint, url_prefix='/api')
    register_error_handlers(app)

    return app