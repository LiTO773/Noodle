import logging
from sqlite3 import Connection
from typing import Dict

from db.inserts import insert_course
from fileops.download_course import download_course
from model.config import Config
from model.course import Course
from moodlews.get_course_contents import get_course_contents
from moodlews.get_courses import get_courses


def check_contents(conn: Connection, state: Config):
    """
    This function is responsible for checking all the contents available in the user's Moodle. Any alterations
    will be written to the db and the corresponding files downloaded (if the user wants)
    :param conn: DB connection
    :param state: A single moodle config
    """
    courses = get_courses(state)

    # Check for new courses
    new_courses = __add_new_courses(conn, state, courses)

    # Check for alterations in the downloaded courses


def __add_new_courses(conn: Connection, state: Config, courses: Dict[int, str]) -> list:
    """
    This function is responsible for finding new courses and adding them to the DB
    :param state: The current moodle state
    :param courses: List of all the courses. The id is the key, and the shortname the value
    :return: A list of the new courses ids
    """
    # Check for new courses and store them
    new_courses = __check_courses_differences(state, courses.keys())

    # Add the new courses to the state and stored them in the DB
    for c_id in new_courses:
        # Create the course and populate ir
        course = Course(c_id, courses[c_id], state.get_default_action() == "download")
        content = get_course_contents(state, c_id)
        course.read_json_contents(content)
        state.add_course(course)

        # DB
        insert_course(conn, course, state.id())

    # Download the courses or notify
    if state.get_default_action() == 'notify':
        # Notify
        logging.warning("New courses were found, please change the config.json to which contents you want to download.")
    elif state.get_default_action() == 'download':
        # Download
        logging.info("Downloading")
        for course_key in state.get_courses():
            course = state.get_courses()[course_key]
            download_course(course, state)
    return new_courses


def __check_courses_differences(state: Config, courses_id_received: list):
    """
    This function is responsible for checking if new courses appeared.
    :param state: The current moodle state
    :param courses_id_received: List of the ids of the courses available to the user
    :return: Ids of the new courses
    """

    # Find new courses
    new_courses = []

    for c_id in courses_id_received:
        if c_id not in state.get_courses():
            new_courses.append(c_id)

    return new_courses
