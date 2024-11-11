from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning("404 error: Resource not found")
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error("500 error: Internal server error")
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
