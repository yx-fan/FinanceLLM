from app import create_app
import logging
from datetime import datetime

# Create Flask app
app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Starting Flask app at {datetime.now()}")

if __name__ == "__main__":
    # Run Flask app in debug mode
    app.run(host="0.0.0.0", port=5001, debug=True)
