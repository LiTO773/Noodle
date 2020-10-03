from sqlite3 import Connection

from db.queries import get_config_courses, get_config_files, get_section_modules, get_course_sections, \
    get_config_urls
from model.config import Config
from model.course import Course, Section
from model.file import File
from model.folder import Folder
from model.url import URL


def populate_config(conn: Connection, config: Config):
    """
    This function is responsible for adding the already present courses to the config.
    THIS FUNCTION MUTATES THE config PARAM
    :param conn: DB connection
    :param config: Moodle configuration
    """
    rows = get_config_courses(conn, config.id())

    # Create the courses and populate each one
    # TODO test this code
    for row in rows:
        course = Course.create_from_db(row)

        # Create the sections and populate each one
        rows_sections = get_course_sections(conn, config.id(), course.id())

        for r_section in rows_sections:
            section = Section.create_from_db(r_section)
            section.add_files(__fetch_files_and_urls(conn, config.id(), section.id(), True))

            # Create the modules, populate each one and add them to the section
            rows_folders = get_section_modules(conn, config.id(), section.id())
            for r_folder in rows_folders:
                folder = Folder.create_from_db(r_folder)
                folder.add_files(__fetch_files_and_urls(conn, config.id(), folder.id(), False))
                section.add_file(folder)

            course.add_section(section)

        config.add_course(course)


def __fetch_files_and_urls(conn: Connection, id: int, is_section: bool) -> list:
    """ This function gets all the files and urls stored in the DB of a section or a folder. """
    result = []

    # Create the files and populate each one
    rows = get_config_files(conn, id, is_section)
    for row in rows:
        result.append(File.create_from_db(row))

    # Create the urls, populate each one and add them to the section
    rows = get_config_urls(conn, id, is_section)
    for row in rows:
        result.append(URL.create_from_db(row))

    return result
