"""
This file stores the functions used to get a certain domain concept from the DB. These are mostly used by
populate_config
"""
from sqlite3 import Connection


def get_config_courses(conn: Connection, config_id: int) -> list:
    """
    Gets the courses of a Moodle
    :param conn: DB connection
    :param config_id: Config id
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM courses WHERE moodle_id = ?", (config_id,))

    rows = c.fetchall()
    c.close()

    return rows


def get_course_sections(conn: Connection, config_id: int, course_id: int) -> list:
    """
    Gets the section of a course.
    :param conn: DB connection
    :param config_id: Moodle config id
    :param course_id: Course id
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM sections WHERE moodle_id = ? AND course_id = ?", (config_id, course_id))

    rows = c.fetchall()
    c.close()

    return rows

def __get_section(conn: Connection, config_id: int, section_id: int, is_module: bool) -> list:
    """
    Helper function for querying the section table
    :param conn: DB connection
    :param config_id: Moodle config id
    :param section_id: Section id
    :param is_module: If it is a module. Otherwise look for LinkableContents
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM ? WHERE moodle_id = ? AND section_id = ?",
              ('modules' if is_module else 'linkablecontents', config_id, section_id)
              )

    rows = c.fetchall()
    c.close()

    return rows


def get_section_modules(conn: Connection, config_id: int, section_id: int) -> list:
    """
    Gets the modules of a section
    :param conn: DB connection
    :param config_id: Moodle config id
    :param section_id: Section id
    :return: Rows found
    """
    return __get_section(conn, config_id, section_id, True)


def get_section_linkablecontents(conn: Connection, config_id: int, section_id: int) -> list:
    """
    Gets the LinkableContents of a section
    :param conn: DB connection
    :param config_id: Moodle config id
    :param section_id: Section id
    :return: Rows found
    """
    return __get_section(conn, config_id, section_id, False)


def __get_module(conn: Connection, config_id: int, module_id: int, table: str) -> list:
    """
    Helper function for querying the module table
    :param conn: DB connection
    :param config_id: Moodle config id
    :param module_id: Module id
    :param table: The table to be queried
    :return: Rows found
    """
    c = conn.cursor()
    c.execute("SELECT * FROM ? WHERE moodle_id = ? AND module_id = ?", (table, config_id, module_id))

    rows = c.fetchall()
    c.close()

    return rows


def get_module_files(conn: Connection, config_id: int, module_id: int) -> list:
    """
    Gets the modules of a section
    :param conn: DB connection
    :param config_id: Moodle config id
    :param module_id: Section id
    :return: Rows found
    """
    return __get_module(conn, config_id, module_id, 'files')


def get_module_linkablecontents(conn: Connection, config_id: int, module_id: int) -> list:
    """
    Gets the LinkableContents of a section
    :param conn: DB connection
    :param config_id: Moodle config id
    :param module_id: Section id
    :return: Rows found
    """
    return __get_section(conn, config_id, module_id, 'linkablecontents')
