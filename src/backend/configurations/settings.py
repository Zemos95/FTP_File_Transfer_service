# Import
import json
from pathlib import Path
from typing import Dict


SETTING_PATH = Path('settings.json')

def load_settings() -> Dict:
    """
    Load the settings from the settings.json file.

    Args:
        None
    
    Returns:
        Dict: The settings as a dictionary.    
    """
    try:
        with open(SETTING_PATH, 'r') as f:
            settings = json.load(f)
        return settings
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_settings(setting: Dict[str, str]) -> None:
    """
    Save the configuration to a JSON file.

    Args:
        config (dict): Configuration dictionary.
    """
    with open(SETTING_PATH, "w") as f:
        json.dump(setting, f, indent=4)
        print("Configuration saved successfully.")