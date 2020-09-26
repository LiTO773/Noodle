from fileops.check_config import check_config
from fileops.create_config import create_config
from errors.error_codes import CONFIG_FILE_BADLY_FORMATTED, CONFIG_FILE_DOESNT_EXIST
from errors.error_strings import ERROR_STRINGS
import logging


def first_run():
    """ This function is launched when the app starts and makes sure that everything is properly setup. """
    result = check_config()
    if result == '':
        logging.info('config.json is fine. Logging in.')
        # The config file already exists, read it
    else:
        if result == CONFIG_FILE_DOESNT_EXIST:
            logging.warning("config.json doesn't exist, creating it. Please fill it and run again.")
            create_config()
            return
        else:
            logging.error(ERROR_STRINGS[result])
