import os
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileHandler(FileSystemEventHandler):
    def __init__(self, settings, callback):
        self.settings = settings
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def process(self, file_path):
        if file_path.endswith(self.settings['file_format']):
            self.callback(file_path)


def start_monitor(settings, callback):
    observer = Observer()
    handler = FileHandler(settings, callback)
    observer.schedule(handler, settings['watch_directory'], recursive=True)
    observer.start()
    return observer



def check_server_status(ftp_server: str) -> str:
    """
    Check if the FTP server is online and reachable.

    Args:
        ftp_server (str): The FTP server address (IP or hostname).

    Returns:
        str: 'Online' if the server is reachable, otherwise 'Offline'.
    """
    try:
        host, port = ftp_server.split(":") if ":" in ftp_server else (ftp_server, 21)
        port = int(port)
        with socket.create_connection((host, port), timeout=5):
            return "Online"
    except (socket.timeout, socket.error) as e:
        return "Offline"