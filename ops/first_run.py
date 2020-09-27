import sys

from db.create_connection import create_connection
from db.read_configs import read_configs
from fileops.check_config import check_config
from fileops.create_config import create_config
from fileops.read_config import read_config
from model.config import Config
from moodlews.get_site_info import get_site_info
from moodlews.login import login
from errors.error_codes import CONFIG_FILE_BADLY_FORMATTED, CONFIG_FILE_DOESNT_EXIST, UNABLE_TO_LOGIN
from errors.error_strings import ERROR_STRINGS
import logging

from ops.populate_config import populate_config


def first_run() -> Config:
    """ This function is launched when the app starts and makes sure that everything is properly setup. If everything
    ran correctly, it returns the token. Otherwise it stops the application. """
    conn = create_connection()

    configs = read_configs(conn)

    # Create the state and the config objects
    # and populate them with their data
    state = []
    for config in configs:
        obj = Config.create_from_db(config)
        populate_config(conn, obj)
        state.append(obj)



    conn.close()

    # result = check_config()
    # if isinstance(result, dict):
    #     logging.info('config.json is fine. Logging in.')
    #     # The config file already exists, read it
    #     token = login(result)
    #
    #     if token == UNABLE_TO_LOGIN:
    #         logging.error(ERROR_STRINGS[UNABLE_TO_LOGIN])
    #         sys.exit(-1)
    #
    #     # Login complete, get the user's info
    #     state = Infos(result['host'], result['username'], result['password'], result['courses'],
    #                   result['default_action'], token)
    #     get_site_info(state)
    #
    #     return state
    # else:
    #     if result == CONFIG_FILE_DOESNT_EXIST:
    #         logging.error("config.json doesn't exist, creating it. Please fill it and run again.")
    #         create_config()
    #         sys.exit(-1)
    #     else:
    #         logging.error(ERROR_STRINGS[result])
    #         sys.exit(-1)
