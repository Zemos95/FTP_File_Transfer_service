from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from ..api.ftp_client import send_file
from ..configurations.settings import load_settings, save_settings
from ..monitoring.server_status import start_monitor
from pathlib import Path

ftp_blueprint = Blueprint('ftp', __name__)
observer = None
transferred_files = 0

@ftp_blueprint.route('/start', methods=['POST'])
def start_transfer():
    """Start monitoring a directory and transferring files via FTP."""
    global observer
    global transferred_files
    # Laden der User-Einstellungen
    try:
        settings = load_settings()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error loading settings.'}), 500
    if observer:
        return jsonify({'message': 'FTP transfer is already running.'})
    
    def process_file(file_path: Path):
        """
        Callback function to process a file.
        Process a file by sending it via FTP.
        """
        global transferred_files
        try:
            send_file(settings['ftp_server'],
                      settings['port'], settings['username'], 
                      settings['password'], file_path, settings['ftp_target_directory'])
            transferred_files += 1
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    # Überwachung starten
    observer = start_monitor(settings, process_file)
    return jsonify({'message': 'FTP transfer started.'})

@ftp_blueprint.route('/stop', methods=['POST'])
def stop_transfer():
    """Stop monitoring a directory and transferring files via FTP."""
    global observer
    if observer:
        observer.stop()
        observer.join()
        observer = None
    return jsonify({'message': 'FTP transfer stopped.'})

@ftp_blueprint.route('/ftp/configuration', methods=['GET', 'POST'])
def configure() -> str:
    """Render the configuration page or save new settings."""
    try:
        if request.method == 'POST':
            settings = {
                'ftp_server': request.form['ftp_server'],
                'port': int(request.form['port']),
                'username': request.form['username'],
                'password': request.form['password'],
                'watch_directory': request.form['watch_directory'],
                'ftp_target_directory': request.form['ftp_target_directory'],
                'file_format': request.form['file_format']
            }
            save_settings(settings)
            return redirect(url_for('ftp.configure'))
        
        settings = load_settings()
        return render_template('ftp.html', config=settings)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error loading configuration.'}), 500