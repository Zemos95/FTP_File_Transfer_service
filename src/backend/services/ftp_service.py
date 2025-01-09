from pathlib import Path
from flask import jsonify, make_response
import paramiko
from ..configurations.settings import load_settings
from ..monitoring.server_status import start_monitor


class FTPService:
    def __init__(self):
        self.observer = None
        self.transferred_files = 0
        self.sftp = None
        self.ssh = None
        self.server_status = 'offline'
        self.login_status = 'failed'

    def connect_to_server(self, settings):
        try:
            print("Attempting to connect to SFTP server...")
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(settings['ftp_server'], port=settings['port'],
                             username=settings['username'],
                             password=settings['password'])
            self.sftp = self.ssh.open_sftp()
            print("Connected to SFTP server.")
            self.server_status = 'online'
            response = jsonify({'message': 'Connected to SFTP server.'})
            return make_response(response, 200)
        except Exception as e:
            print(f"Error: {e}")
            self.server_status = 'offline'
            response = jsonify({'message': 'Error connecting to SFTP server.'})
            return make_response(response, 500)

    def start_transfer(self):
        try:
            settings = load_settings()
        except Exception as e:
            print(f"Error: {e}")
            response = jsonify(
                {'message': 'Error loading settings.'})
            return make_response(response, 500)
        if self.observer:
            response = jsonify(
                {'message': 'SFTP transfer is already running.'})
            return make_response(response, 400)

        def process_file(file_path: Path):
            try:
                self.send_file(settings['ftp_server'],
                               settings['port'], settings['username'],
                               settings['password'], file_path,
                               settings['ftp_target_directory'])
                self.transferred_files += 1
            except Exception as e:
                print(f"Error: {e}")
                return None

        self.observer = start_monitor(settings, process_file)
        response = jsonify({'message': 'SFTP transfer started.'})
        return make_response(response, 200)

    def stop_transfer(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        self.server_status = 'offline'
        self.login_status = 'failed'
        response = jsonify({'message': 'SFTP transfer stopped.'})
        return make_response(response, 200)

    def send_file(self, ftp_server, port, username, password, file_path, target_directory):
        try:
            self.sftp.put(file_path, f"{target_directory}/{file_path.name}")
        except Exception as e:
            print(f"Error: {e}")