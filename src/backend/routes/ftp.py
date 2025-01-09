from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.ftp_service import FTPService
from ..configurations.settings import load_settings, save_settings

ftp_blueprint = Blueprint('ftp', __name__)
ftp_service = FTPService()


@ftp_blueprint.route('/connect', methods=['POST'])
def connect():
    settings = load_settings()
    response = ftp_service.connect_to_server(settings)
    if response.status_code == 200:
        flash('Connected to SFTP server successfully!', 'success')
    else:
        flash('Error connecting to SFTP server.', 'danger')
    return redirect(url_for('ftp.configure'))


@ftp_blueprint.route('/start', methods=['POST'])
def start_transfer():
    response = ftp_service.start_transfer()
    if response.status_code == 200:
        flash('SFTP Service started successfully!', 'success')
    else:
        flash('Error starting SFTP Service.', 'danger')
    return redirect(url_for('home'))


@ftp_blueprint.route('/stop', methods=['POST'])
def stop_transfer():
    response = ftp_service.stop_transfer()
    if response.status_code == 200:
        flash('SFTP Service stopped successfully!', 'info')
    else:
        flash('Error stopping SFTP Service.', 'danger')
    return redirect(url_for('home'))


@ftp_blueprint.route('/logout', methods=['POST'])
def logout():
    response = ftp_service.stop_transfer()
    if response.status_code == 200:
        flash('Logged out successfully!', 'info')
    else:
        flash('Error logging out.', 'danger')
    return redirect(url_for('home'))


@ftp_blueprint.route('/ftp/configuration', methods=['GET', 'POST'])
def configure() -> str:
    try:
        if request.method == 'POST':
            settings = {
                'ftp_server': request.form['ftp_server'],
                'port': request.form['port'],
                'username': request.form['username'],
                'password': request.form['password'],
                'watch_directory': request.form['watch_directory'],
                'ftp_target_directory': request.form['ftp_target_directory'],
                'file_format': request.form['file_format']
            }
            # Überprüfen, ob alle Felder ausgefüllt sind
            if not all(settings.values()):
                flash('Enter all the configuration settings.', 'danger')
                return redirect(url_for('ftp.configure'))
            # Konvertiere Port zu int
            settings['port'] = int(settings['port'])
            save_settings(settings)
            flash('Configuration saved successfully!', 'success')
            return redirect(url_for('ftp.configure'))

        settings = load_settings()
        return render_template('ftp.html', config=settings)
    except Exception as e:
        print(f"Error: {e}")
        flash('Error loading configuration.', 'danger')
        return redirect(url_for('ftp.configure'))
