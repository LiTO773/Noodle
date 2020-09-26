from .file_constants import CONFIG_BODY, CONFIG_FILE_NAME
import json


def create_config():
    """ Creates a blank config file """
    with open(CONFIG_FILE_NAME, 'w') as file:
        json.dump(CONFIG_BODY, file, indent=4)
