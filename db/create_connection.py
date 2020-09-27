import logging
import os
import sqlite3
import sys
from sqlite3 import Error

from db import DB_NAME
from db.create_schema import create_schema


def create_connection():
    """ Connects to the DB """
    conn = None
    try:
        first_time = not os.path.isfile(DB_NAME)
        conn = sqlite3.connect(DB_NAME)

        # The DB didn't exist, generate the schema
        if first_time:
            create_schema(conn)
    except Error as e:
        print(e)
        logging.critical("Unable to connect to the DB!")
        sys.exit(-1)

    return conn
