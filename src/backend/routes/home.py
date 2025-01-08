# src/backend/routes/home.py
from flask import Blueprint, render_template, jsonify
from ..configurations.settings import load_settings
from ..monitoring.server_status import check_server_status
import random

home_blueprint = Blueprint('home', __name__)

# Globale Variablen
observer_running = False
transferred_files = 0
upload_speed = 0.0  # in MB/s
download_speed = 0.0  # in MB/s

@home_blueprint.route('/')
def home():
    """
    Home route for the application.

    Returns:
        render_template: The rendered template for the home page.
    """
    return render_template('home.html')

@home_blueprint.route('/api/status', methods=['GET'])
def get_status():
    """
    API route to return the current status of the application.

    Returns:
        JSON: Current server and application status.
    """
    global observer_running, transferred_files, upload_speed, download_speed

    try:
        settings = load_settings()
        server_status = check_server_status(settings['ftp_server'])
        # Simulierte Geschwindigkeiten
        upload_speed = random.uniform(0.5, 5.0)
        download_speed = random.uniform(1.0, 10.0)

        return jsonify({
            "server_status": server_status,
            "observer_running": observer_running,
            "transferred_files": transferred_files,
            "upload_speed": f"{upload_speed:.2f} MB/s",
            "download_speed": f"{download_speed:.2f} MB/s"
        })
    except Exception as e:
        return jsonify({"error": str(e)})