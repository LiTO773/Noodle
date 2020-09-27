import json

from fileops.file_constants import CONFIG_FILE_NAME
from model.config import Config


def write_config(state: Config):
    """ Writes the config.json with the current state """
    with open(CONFIG_FILE_NAME, 'w') as file:
        json.dump(state.to_writable_dict(), file, indent=4)