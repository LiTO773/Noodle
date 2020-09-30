from sqlite3 import Connection

from db.query_config import get_config_courses, get_config_files, get_config_folders, get_config_sections, \
    get_config_urls
from model.config import Config
from model.course import Course, Section
from model.file import File
from model.folder import Folder
from model.url import URL


def populate_config(conn: Connection, config: Config):
    """ This function is responsible for populating a config with the information present in the DB """
    rows = get_config_courses(conn, config.id())
    courses = []

    # Create the courses and populate each one
    # TODO test this code
    for row in rows:
        course = Course.create_from_db(row)

        # Create the sections and populate each one
        rows_sections = get_config_sections(conn, course.id())
        sections = []

        for r_section in rows_sections:
            section = Section.create_from_db(r_section)
            section.add_files(__fetch_files_and_urls(conn, section.id(), True))

            # Create the folders, populate each one and add them to the section
            rows_folders = get_config_folders(conn, section.id())
            for r_folder in rows_folders:
                folder = Folder.create_from_db(r_folder)
                folder.add_files(__fetch_files_and_urls(conn, folder.id(), False))
                section.add_file(folder)

            sections.append(section)
        courses.append(course)


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
