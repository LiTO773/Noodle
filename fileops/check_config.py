from .file_constants import CONFIG_FILE_NAME
from .read_config import read_config
from .file_constants import CONFIG_BODY
from errors.error_codes import CONFIG_FILE_DOESNT_EXIST, CONFIG_FILE_BADLY_FORMATTED
import os.path


def check_config():
    """ This function is responsible for checking if a config file already exists and it's valid. It returns '' if
    everything is fine, otherwise it returns an error code """
    if os.path.exists('./' + CONFIG_FILE_NAME):
        # Check if the file contains contains everything
        content = read_config()
        content_keys = content.keys()
        expected_keys = CONFIG_BODY.keys()

        if set(content_keys) == set(expected_keys) and __validate_data(content):
            return ''
        else:
            return CONFIG_FILE_BADLY_FORMATTED
    else:
        return CONFIG_FILE_DOESNT_EXIST


def __validate_data(content: dict) -> bool:
    return len(content['username']) > 0 and len(content['password']) > 0 and len(content['host'])
