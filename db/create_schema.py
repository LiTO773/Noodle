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
        userid integer DEFAULT -1,
        location text NOT NULL
    );""",
    """
    CREATE TABLE IF NOT EXISTS courses (
        id integer NOT NULL,
        moodle_id integer NOT NULL,
        shortname text NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (moodle_id) REFERENCES configs (id),
        PRIMARY KEY (id, moodle_id)
    );""",
    """
    CREATE TABLE IF NOT EXISTS sections (
        id integer NOT NULL,
        moodle_id integer NOT NULL,
        course_id integer NOT NULL,
        name text NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses (id),
        PRIMARY KEY (id, moodle_id, course_id)
    );""",
    """
    CREATE TABLE IF NOT EXISTS modules (
        id integer NOT NULL,
        moodle_id integer NOT NULL,
        section_id integer NOT NULL,
        name text NOT NULL,
        url text NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (moodle_id) REFERENCES configs (id),
        FOREIGN KEY (section_id) REFERENCES sections (id),
        PRIMARY KEY (id, moodle_id, section_id)
    );""",
    """
    CREATE TABLE IF NOT EXISTS files (
        moodle_id integer NOT NULL,
        module_id integer,
        filename text NOT NULL,
        filesize integer NOT NULL,
        fileurl text NOT NULL,
        timecreated integer NOT NULL,
        timemodified integer NOT NULL,
        download integer NOT NULL,
        downloaded integer NOT NULL,
        hash integer NOT NULL,
        FOREIGN KEY (moodle_id) REFERENCES configs (id),
        FOREIGN KEY (module_id) REFERENCES modules (id),
        PRIMARY KEY (moodle_id, module_id, fileurl, timemodified)
    );""",
    # linkablecontents doesn't have a primary key, since it is possible for the same link with the same name and modname
    # to exist in the section
    """
    CREATE TABLE IF NOT EXISTS linkablecontents (
        moodle_id integer NOT NULL,
        modname integer NOT NULL,
        section_id integer,
        module_id integer,
        own_id integer,
        name text NOT NULL,
        url text NOT NULL,
        FOREIGN KEY (moodle_id) REFERENCES configs (id),
        FOREIGN KEY (section_id) REFERENCES sections (id),
        FOREIGN KEY (module_id) REFERENCES modules (id)
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
