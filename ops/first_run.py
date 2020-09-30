import sys
from sqlite3 import Connection

from db.create_connection import create_connection
from db.read_configs import read_configs
from db.updates import update_config_userid
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


def first_run() -> (list, Connection):
    """ This function is launched when the app starts and makes sure that everything is properly setup. If everything
    ran correctly, it returns the token. Otherwise it stops the application. """
    conn = create_connection()

    configs = read_configs(conn)

    # Create the state and the config objects and populate them with their data
    state = []
    for db_config in configs:
        config = Config.create_from_db(db_config)
        populate_config(conn, config)

        # Get the token
        token = login(config)
        if token != UNABLE_TO_LOGIN:
            config.set_token(token)
        else:
            logging.error(ERROR_STRINGS[token])
            sys.exit(-1)

        # Check if the userid is still the same, if it isn't update in the DB
        userid = get_site_info(config)

        if config.update_userid(userid):
            # Update to the new userid
            update_config_userid(conn, config.id(), userid)

        state.append(config)

    print(state[0])

    return state, conn

