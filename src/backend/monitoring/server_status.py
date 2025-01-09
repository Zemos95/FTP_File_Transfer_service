# Import
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from typing import Dict, Callable
import socket


class FileHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers a callbackl for specific file types
    """
    def __init__(self, settings: Dict[str, str], callback: Callable[[Path],
                                                                    None]):
        """
        Initialize the FileHandler, settings, callback.
        """
        self.settings = settings
        self.callback = callback

    def on_modified(self, event):
        """
        Trigger the callback when a file is modified.
        Args:
            event: The file system event.
        """
        if not event.is_directory and event.src_path.endswith(self.settings['file_format']):
            self.callback(Path(event.src_path))


def start_monitor(settings: Dict[str, str], callback: Callable[[Path], None]) -> ObservedWatch:
    """
    Start monitoring a directory for file changes.

    Args:
        settings (Dict[str, str]): The settings for the monitoring.
        callback (Callable[[Path], None]): The callback to trigger when a file is modified.

    Returns:
        Observer: The observer object.
    """
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
