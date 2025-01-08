# Import
import os
from ftplib import FTP
from pathlib import Path


def send_file(ftp_server: str, port: int, username: str, password: str, file_path: Path, target_directory: str) -> None:
    """
    Send a file via FTP to a server.

    Args:
        ftp_server (str): The FTP server to connect to.
        port (int): The port to connect to.
        username (str): The username for the FTP server.
        password (str): The password for the FTP server.
        file_path (Path): The path to the file to send.
        target_directory (str): The target directory on the FTP server.

    Returns:
        None
    """
    # Create an FTP object
    try:
        ftp = FTP()
    except Exception as e:
        print(f"Error: {e}")
        return None
    # Connect to the FTP server
    try:
        ftp.connect(ftp_server, port)
    except Exception as e:
        print(f"Error: {e}")
        return None
    # Login to the FTP server
    try:  
        ftp.login(username, password) # Login to the FTP server
    except Exception as e:
        print(f"Error: {e}")
        return None
    # Change to the target_ directory
    try:
        ftp.cwd(target_directory)
    except Exception as e:
        print(f"Error: {e}")

    try:    
        with open(file_path, 'rb') as f:
            ftp.storbinary(f'STOR {os.path.basename(file_path)}', f)
        ftp.quit()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    