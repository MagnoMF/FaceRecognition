import toml
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent / "settings.toml"
    with open(config_path, "r") as file_config:
        return toml.load(file_config)

environments = load_config()