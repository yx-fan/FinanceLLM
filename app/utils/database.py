from pymongo import MongoClient, errors

def initialize_mongo(app):
    """Initialize MongoDB connection."""
    try:
        mongo_uri = app.config.get("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in configuration.")
        
        # Connect to MongoDB
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command("ping")  # Test connection

        # Set MongoDB client and database
        app.mongo_client = mongo_client
        app.db = mongo_client.get_default_database()
        app.logger.info("MongoDB connected successfully!")

    except (errors.ServerSelectionTimeoutError, ValueError) as err:
        app.logger.error(f"Failed to connect to MongoDB: {err}")
        app.mongo_client = None
        app.db = None
