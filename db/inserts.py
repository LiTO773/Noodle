from sqlite3 import Connection
from typing import Union

from model.LinkableContents import LinkableContent
from model.course import Course
from model.file import File
from model.module import Module
from model.section import Section


def insert_course(conn: Connection, course: Course, moodle_id: int):
    """
    Adds a new course the the DB
    :param conn: DB connection
    :param course: Course information
    :param moodle_id: Moodle identifier in the DB
    """

    c = conn.cursor()
    c.execute("""INSERT INTO courses(id, moodle_id, shortname, download, downloaded, hash)
                 VALUES(?, ?, ?, ?, 0, ?);""",
              (course.id, moodle_id, course.name, course.download, hash(course)))

    conn.commit()
    c.close()

    # Add the sections
    for section in course.sections:
        insert_section(conn, section, course.id, moodle_id)


def insert_section(conn: Connection, section: Section, course_id: int, moodle_id: int):
    """
    Adds a new section to the DB
    :param conn: DB connection
    :param section: Section information
    :param course_id: Course identifier to which the section belongs
    :param moodle_id: Moodle identifier in the DB
    """

    c = conn.cursor()
    c.execute("""INSERT INTO sections(id, moodle_id, course_id, name, download, downloaded, hash)
                 VALUES(?, ?, ?, ?, ?, 0, ?);""",
              (section.id, moodle_id, course_id, section.name, section.download, hash(section)))

    conn.commit()
    c.close()

    # Add the modules
    for module in section.modules:
        if isinstance(module, Module):
            __insert_module(conn, module, section.id, moodle_id)
        elif isinstance(module, LinkableContent):
            insert_linkablecontent(conn, module, moodle_id, section_id=section.id)


def __insert_module(conn: Connection, module: Union[Module, LinkableContent], section_id: int, moodle_id: int):
    """
    This function adds sections modules
    :param conn: DB connection
    :param module: Module/LinkableContent information
    :param section_id: Section identifier to which the module belongs
    :param moodle_id: Moodle identifier in the DB
    """

    c = conn.cursor()
    c.execute("""INSERT INTO modules(id, moodle_id, section_id, name, url, download, downloaded, hash)
                 VALUES(?, ?, ?, ?, ?, ?, 0, ?);""",
              (module.id, moodle_id, section_id, module.name, module.url, module.download, hash(module)))

    conn.commit()
    c.close()

    # Add the files/urls
    for content in module.contents:
        if isinstance(content, File):
            insert_file(conn, content, module.id, moodle_id)
        elif isinstance(content, LinkableContent):
            insert_linkablecontent(conn, content, moodle_id, module_id=module.id)


def insert_file(conn: Connection, file: File, module_id: int, moodle_id: int):
    """
    Adds a new file to the DB
    :param conn: DB connection
    :param file: File information
    :param module_id: Module identifier to which the file belongs
    :param moodle_id: Moodle identifier in the DB
    """

    c = conn.cursor()
    c.execute("""INSERT INTO files(moodle_id, module_id, filename, filesize, fileurl, timecreated, timemodified,
                                   download, downloaded, hash)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, 0, ?);""",
              (moodle_id, module_id, file.name, file.size, file.url, file.time_created,
               file.time_modified, file.download, hash(file)))

    conn.commit()
    c.close()


def insert_linkablecontent(conn: Connection, lc: LinkableContent, moodle_id: int, section_id: int = None,
                           module_id: int = None):
    """
    Adds a new linkable content to the DB
    :param conn: DB connection
    :param lc: LinkableContent information
    :param moodle_id: Moodle identifier in the DB
    :param section_id: Section identifier to which the module belongs (is None if module_id exists)
    :param module_id: Module identifier to which the file belongs (its None if section_id exists)
    """

    c = conn.cursor()
    c.execute("""INSERT INTO linkablecontents(moodle_id, modname, section_id, module_id, own_id, name, url)
                 VALUES(?, ?, ?, ?, ?, ?, ?);""",
              (moodle_id, lc.modname, section_id, module_id, lc.own_id, lc.name, lc.url))

    conn.commit()
    c.close()
