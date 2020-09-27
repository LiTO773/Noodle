import logging
import sys
from sqlite3 import Error, Connection

__schema = [
    """
    CREATE TABLE IF NOT EXISTS configs (
        id integer PRIMARY KEY AUTOINCREMENT,
        host text NOT NULL,
        username text NOT NULL,
        password text NOT NULL,
        max_file_size integer NOT NULL,
        default_action text NOT NULL,
        userid integer DEFAULT -1
    );""",
    """
    CREATE TABLE IF NOT EXISTS courses (
        id integer PRIMARY KEY,
        moodle_id integer NOT NULL,
        shortname text NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (moodle_id) REFERENCES configs (id)
    );""",
    """
    CREATE TABLE IF NOT EXISTS sections (
        id integer PRIMARY KEY,
        course_id integer NOT NULL,
        name text NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses (id)
    );""",
    """
    CREATE TABLE IF NOT EXISTS folders (
        id integer PRIMARY KEY,
        section_id integer NOT NULL,
        name text NOT NULL,
        url text NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (section_id) REFERENCES sections (id)
    );""",
    """
    CREATE TABLE IF NOT EXISTS files (
        section_id integer,
        folder_id integer,
        filename text NOT NULL,
        filesize integer NOT NULL,
        fileurl text NOT NULL,
        timecreated integer NOT NULL,
        timemodified integer NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (section_id) REFERENCES sections (id),
        FOREIGN KEY (folder_id) REFERENCES folders (id),
        PRIMARY KEY (fileurl, timecreated)
    );""",
    """
    CREATE TABLE IF NOT EXISTS urls (
        section_id integer,
        folder_id integer,
        filename text NOT NULL,
        fileurl text NOT NULL,
        timemodified integer NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (section_id) REFERENCES sections (id),
        FOREIGN KEY (folder_id) REFERENCES folders (id),
        PRIMARY KEY (fileurl, timemodified)
    );"""
]


def create_schema(conn: Connection):
    """ Creates the main database schema. It should only be called if it is the first time the DB is created """
    try:
        c = conn.cursor()
        for query in __schema:
            c.execute(query)
        conn.commit()
        c.close()
    except Error as e:
        print(e)
        logging.critical('Could not create the database schema')
        conn.close()
        sys.exit(-1)
