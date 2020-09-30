from sqlite3 import Connection
from typing import Union

from model.course import Course
from model.file import File
from model.folder import Folder
from model.section import Section
from model.url import URL


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
              (course.id(), moodle_id, course.get_shortname(), course.get_download(), hash(course)))

    conn.commit()
    c.close()

    # Add the sections
    for section in course.get_sections():
        insert_section(conn, section, course.id())


def insert_section(conn: Connection, section: Section, course_id: int):
    """
    Adds a new section to the DB
    :param conn: DB connection
    :param section: Section information
    :param course_id: Course identifier to which the section belongs
    """

    c = conn.cursor()
    c.execute("""INSERT INTO sections(id, course_id, name, download, downloaded, hash)
                 VALUES(?, ?, ?, ?, 0, ?);""",
              (section.id(), course_id, section.get_name(), section.get_download(), hash(section)))

    conn.commit()
    c.close()

    # Add the modules
    for module in section.get_files():
        __insert_module(conn, module, section.id())


def __insert_module(conn: Connection, module: Union[File, Folder, URL], section_id: int):
    """
    This function adds sections modules, automatically assigning the correct INSET for function for Files, Folders or
    URLs
    :param conn: DB connection
    :param module: File/Folder/URL information
    :param section_id: Section identifier to which the module belongs
    """

    if isinstance(module, File):
        insert_file(conn, module, section_id)
    elif isinstance(module, Folder):
        insert_folder(conn, module, section_id)
    elif isinstance(module, URL):
        insert_url(conn, module, section_id)


def insert_file(conn: Connection, file: File, section_id: int = None, folder_id: int = None):
    """
    Adds a new file to the DB
    :param conn: DB connection
    :param file: File information
    :param section_id: Section identifier to which the file belongs (if folder_id exists, this is None)
    :param folder_id: Folder identifier to which the file belongs (if section_id exists, this is None)
    """

    c = conn.cursor()
    c.execute("""INSERT INTO files(section_id, folder_id, filename, filesize, fileurl, timecreated, timemodified,
                                   download, downloaded, hash)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, 0, ?);""",
              (section_id, folder_id, file.get_name(), file.get_size(), file.get_url(), file.get_time_created(),
               file.get_time_modified(), file.get_download(), hash(file)))

    conn.commit()
    c.close()


def insert_url(conn: Connection, url: URL, section_id: int = None, folder_id: int = None):
    """
    Adds a new url to the DB
    :param conn: DB connection
    :param url: URL information
    :param section_id: Section identifier to which the url belongs (if folder_id exists, this is None)
    :param folder_id: Folder identifier to which the url belongs (if section_id exists, this is None)
    """

    c = conn.cursor()
    c.execute("""INSERT INTO urls(section_id, folder_id, filename, fileurl, timemodified, download, downloaded, hash)
                 VALUES(?, ?, ?, ?, ?, ?, 0, ?);""",
              (section_id, folder_id, url.get_name(), url.get_url(), url.get_time_modified(), url.get_download(),
               hash(url))
              )

    conn.commit()
    c.close()


def insert_folder(conn: Connection, folder: Folder, section_id: int):
    """
    Adds a new folder to the DB
    :param conn: DB connection
    :param folder: Folder information
    :param section_id: Section identifier to which the folder belongs
    """

    c = conn.cursor()
    c.execute("""INSERT INTO folders(id, section_id, name, url, download, downloaded, hash)
                 VALUES(?, ?, ?, ?, ?, 0, ?);""",
              (folder.id(), section_id, folder.get_name(), folder.get_url(), folder.get_download(), hash(folder)))

    conn.commit()
    c.close()

    # Add the files/urls
    for file in folder.get_files():
        if isinstance(file, File):
            insert_file(conn, file, folder_id=folder.id())
        elif isinstance(file, URL):
            insert_url(conn, file, folder_id=folder.id())
