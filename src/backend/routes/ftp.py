from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from ..services.ftp_service import FTPService
from ..configurations.settings import load_settings, save_settings

ftp_blueprint = Blueprint('ftp', __name__)
ftp_service = FTPService()

@ftp_blueprint.route('/start', methods=['POST'])
def start_transfer():
    return ftp_service.start_transfer()

@ftp_blueprint.route('/stop', methods=['POST'])
def stop_transfer():
    return ftp_service.stop_transfer()

@ftp_blueprint.route('/ftp/configuration', methods=['GET', 'POST'])
def configure() -> str:
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