import logging
import sys
from sqlite3 import Connection

from db.create_connection import create_connection
from db.read_configs import read_configs
from db.updates import update_config_userid
from errors.error_codes import UNABLE_TO_LOGIN
from errors.error_strings import ERROR_STRINGS
from model.Config import Config
from moodlews.get_site_info import get_site_info
from moodlews.login import login
from ops.populate_config import populate_config


def first_run() -> (list, Connection):
    """ This function is launched when the app starts and makes sure that everything is properly setup. If everything
    ran correctly, it returns the token. Otherwise it stops the application. """
    conn = create_connection()

    db_configs = read_configs(conn)

    # Create the state and the config objects and populate them with their data
    state = []
    for db_config in db_configs:
        config = Config.create_from_db(db_config)
        populate_config(conn, config)

        # Get the token
        token = login(config)
        if token != UNABLE_TO_LOGIN:
            config.token = token
        else:
            logging.error(ERROR_STRINGS[token])
            sys.exit(-1)

        # Check if the userid is still the same, if it isn't update in the DB
        userid = get_site_info(config)

        config.userid = userid
        # Check if the userid was correctly set
        if config.userid == userid:
            # Update to the new userid
            update_config_userid(conn, config.id, userid)

        state.append(config)

    return state, conn

