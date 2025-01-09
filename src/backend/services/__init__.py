from pathlib import Path
from flask import jsonify
from ..api.ftp_client import send_file
from ..configurations.settings import load_settings
from ..monitoring.server_status import start_monitor

class FTPService:
    def __init__(self):
        self.observer = None
        self.transferred_files = 0

    def start_transfer(self):
        try:
            settings = load_settings()
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Error loading settings.'}), 500
        if self.observer:
            return jsonify({'message': 'FTP transfer is already running.'})
        
        def process_file(file_path: Path):
            try:
                send_file(settings['ftp_server'],
                          settings['port'], settings['username'], 
                          settings['password'], file_path, settings['ftp_target_directory'])
                self.transferred_files += 1
            except Exception as e:
                print(f"Error: {e}")
                return None
        
        self.observer = start_monitor(settings, process_file)
        return jsonify({'message': 'FTP transfer started.'})

    def stop_transfer(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        return jsonify({'message': 'FTP transfer stopped.'})