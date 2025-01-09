# Import
from backend import create_app
from backend.configurations.config import SERVER_CONFIG


def main() -> None:
    """
    Main function to run the application.
    This starts the Flask application.
    """
    try:
        app = create_app()
        if app is not None:
            app.run(host=SERVER_CONFIG['host'], port=SERVER_CONFIG['port'])
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    main()
