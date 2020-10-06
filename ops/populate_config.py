from sqlite3 import Connection
from typing import List, Union

from db.queries import get_config_courses, get_section_modules, get_course_sections, get_section_linkablecontents, \
    get_module_linkablecontents, get_module_files
from model.LinkableContents import LinkableContent
from model.Config import Config
from model.course import Course, Section
from model.file import File
from model.module import Module
from model.url import URL


def populate_config(conn: Connection, config: Config):
    """
    This function is responsible for adding the already present courses to the config.
    THIS FUNCTION MUTATES THE config PARAM
    :param conn: DB connection
    :param config: Moodle configuration
    """
    rows = get_config_courses(conn, config.id)

    # Create the courses and populate each one
    # TODO test this code
    for row in rows:
        course = Course.create_from_db(row)

        # Create the sections and populate each one
        rows_sections = get_course_sections(conn, config.id, course.id())

        for r_section in rows_sections:
            section = Section.create_from_db(r_section)

            # Add the LinkableContents
            section.modules = __get_linkablecontents(conn, config.id, section.id(), True)

            # Create the modules, populate each one and add them to the section
            rows_modules = get_section_modules(conn, config.id, section.id())
            for r_module in rows_modules:
                module = Module.create_from_db(r_module)

                # Add the LinkableContents
                module.add_contents(__get_linkablecontents(conn, config.id, module.id(), False))

                # Add the Files
                rows_files = get_module_files(conn, config.id, module.id())

                for r_file in rows_files:
                    module.add_content(File.create_file_or_url(r_file))

                # Add the module to the section
                section.add_module(module)

            # Add the section to the course
            course.add_section(section)

        # Add the course to the config
        config.add_course(course)


def __get_linkablecontents(conn: Connection, config_id: int, target_id: int, is_section: bool) -> List[Union[Module, LinkableContent]]:
    """
    This function gets all the files and urls stored in the DB of a section or a folder.
    :param conn: DB connection
    :param config_id: Moodle's configuration id
    :param target_id: Either the Section's id or the Module's id
    :param is_section: True if it is a Section, otherwise it's a module
    :return: A list with LinkableContents
    """
    # Chose the right query
    rows = []
    if is_section:
        rows = get_section_linkablecontents(conn, config_id, target_id)
    else:
        rows = get_module_linkablecontents(conn, config_id, target_id)

    # Create the array with the Linkables
    result = []
    for row in rows:
        result.append(LinkableContent.create_from_db(row))

    return result
