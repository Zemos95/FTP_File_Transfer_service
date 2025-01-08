# Import
from flask import Flask
import os
def create_app() -> Flask:
    # Create the Flask application
    try:
        #app = Flask(__name__)
        app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'))
    except Exception as e:
        print(f"Error: {e}")
        return None
    try:
        # Import the routes
        from .routes.home import home_blueprint
        from .routes.ftp import ftp_blueprint
        # Register the blueprints
        app.register_blueprint(home_blueprint)
        app.register_blueprint(ftp_blueprint)
        return app
    except Exception as e:
        print(f"Error: {e}")
        return None
