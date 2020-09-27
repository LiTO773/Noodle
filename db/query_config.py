"""
This file stores the functions used to get a certain domain concept from the DB. These are mostly used by
populate_config
"""
from sqlite3 import Connection


def get_config_courses(conn: Connection, id: int) -> list:
    """
    Gets the courses
    :param conn: DB connection
    :param id: Config id
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM courses WHERE moodle_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows


def get_config_folders(conn: Connection, id: int) -> list:
    """
    Gets the folders of a section
    :param conn: DB connection
    :param id: Section id
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM folders WHERE section_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows


def get_config_sections(conn: Connection, id: int) -> list:
    """
    Gets the section of a course.
    :param conn: DB connection
    :param id: Course id
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM sections WHERE course_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows


def get_config_files(conn: Connection, id: int, is_section: bool) -> list:
    """
    Gets the files of either a folder or a section
    :param conn: DB connection
    :param id: Folder/section id
    :param is_section: If the id corresponds to a section
    :return: Rows found
    """
    c = conn.cursor()

    if is_section:
        c.execute("SELECT * FROM files WHERE section_id = ?", (id,))
    else:
        c.execute("SELECT * FROM files WHERE folder_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows


def get_config_urls(conn: Connection, id: int, is_section: bool) -> list:
    """
    Gets the urls of either a folder or a section
    :param conn: DB connection
    :param id: Folder/section id
    :param is_section: If the id corresponds to a section
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM urls WHERE section_id = ?", (id,))

    if is_section:
        c.execute("SELECT * FROM urls WHERE section_id = ?", (id,))
    else:
        c.execute("SELECT * FROM urls WHERE folder_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows
