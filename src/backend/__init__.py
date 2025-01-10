from flask import Flask, redirect, url_for  # Added redirect and url_for imports
import os
from flask_login import LoginManager, current_user  # Added current_user import
from .models.user import users


def create_app() -> Flask:
    try:
        app = Flask(
            __name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..',
                                         'frontend', 'templates')
        )
        app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))
    except Exception as e:
        print(f"Error initializing Flask app: {e}")
        return None

    try:
        # Flask-Login konfigurieren
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'login.login'  # Blueprint.name.route_name
        login_manager.login_message_category = 'info'  # Kategorie für Flash-Nachrichten

        @login_manager.user_loader
        def load_user(user_id):
            print(f"Loading user with ID: {user_id}")  # Debugging-Statement
            for user in users.values():
                if str(user.id) == str(user_id):
                    # Debugging-Statement
                    print(f"User found: {user.username}")
                    return user
            print("User not found.")  # Debugging-Statement
            return None

        # Import der Routen
        from .routes.home import home_blueprint
        from .routes.ftp import ftp_blueprint
        from .routes.status import status_blueprint
        from .routes.modbus import modbus_blueprint
        from .routes.login import login_blueprint  # Neuer Blueprint für Login

        # Register der Blueprints
        app.register_blueprint(login_blueprint)
        app.register_blueprint(home_blueprint)
        app.register_blueprint(ftp_blueprint, url_prefix='/ftp')
        app.register_blueprint(status_blueprint)
        app.register_blueprint(modbus_blueprint)

        # Root-Route definieren
        @app.route('/')
        def index():
            if current_user.is_authenticated:
                return redirect(url_for('home.home'))
            return redirect(url_for('login.login'))

        return app
    except Exception as e:
        print(f"Error setting up Flask-Login and Blueprints: {e}")
        return None