from flask import Flask
import os
from flask_login import LoginManager
from .models.user import User


def create_app() -> Flask:
    # Create the Flask application
    try:
        app = Flask(__name__,
                    template_folder=os.path.join(os.path.dirname(__file__),
                                                 '..', 'frontend', 'templates'))
        app.secret_key = os.urandom(24)
    except Exception as e:
        print(f"Error: {e}")
        return None

    try:
        # Flask-Login konfigurieren
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'login.login'  # Blueprint.name.route_name

        # Dummy-Benutzer für Demo-Zwecke (ersetzen Sie dies durch eine echte Benutzerverwaltung)
        users = {
            'admin': User(id=1, username='admin', password='password')  # Passwort sollte gehasht werden
        }

        @login_manager.user_loader
        def load_user(user_id):
            for user in users.values():
                if user.id == int(user_id):
                    return user
            return None

        # Import der Routen
        from .routes.home import home_blueprint
        from .routes.ftp import ftp_blueprint
        from .routes.status import status_blueprint
        from .routes.modbus import modbus_blueprint
        from .routes.login import login_blueprint  # Neuer Blueprint für Login

        # Register der Blueprints
        app.register_blueprint(home_blueprint)
        app.register_blueprint(ftp_blueprint)
        app.register_blueprint(status_blueprint)
        app.register_blueprint(modbus_blueprint)
        app.register_blueprint(login_blueprint)  # Registrierung des Login-Blueprints

        return app
    except Exception as e:
        print(f"Error: {e}")
        return None