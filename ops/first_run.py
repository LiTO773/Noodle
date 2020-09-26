import sys

from fileops.check_config import check_config
from fileops.create_config import create_config
from fileops.read_config import read_config
from model.infos import Infos
from moodlews.get_site_info import get_site_info
from moodlews.login import login
from errors.error_codes import CONFIG_FILE_BADLY_FORMATTED, CONFIG_FILE_DOESNT_EXIST, UNABLE_TO_LOGIN
from errors.error_strings import ERROR_STRINGS
import logging


def first_run() -> Infos:
    """ This function is launched when the app starts and makes sure that everything is properly setup. If everything
    ran correctly, it returns the token. Otherwise it stops the application. """
    result = check_config()
    if result == '':
        logging.info('config.json is fine. Logging in.')
        # The config file already exists, read it
        content = read_config()
        token = login(content)

        if token == UNABLE_TO_LOGIN:
            logging.error(ERROR_STRINGS[UNABLE_TO_LOGIN])
            sys.exit(-1)

        # Login complete, get the user's info
        state = Infos(content['host'], content['username'], content['password'], content['courses'], token)
        get_site_info(state)

        return state
    else:
        if result == CONFIG_FILE_DOESNT_EXIST:
            logging.error("config.json doesn't exist, creating it. Please fill it and run again.")
            create_config()
            sys.exit(-1)
        else:
            logging.error(ERROR_STRINGS[result])
            sys.exit(-1)
