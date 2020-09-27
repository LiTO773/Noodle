import logging

from fileops.write_config import write_config
from model.course import Course
from model.config import Config
from moodlews.get_course_contents import get_course_contents
from moodlews.get_courses import get_courses


def check_contents(state: Config):
    """ This function is responsible for checking all the contents available in the user's Moodle. Any alterations
    will be writing to the config file and the corresponding files downloaded """
    courses = get_courses(state)

    # Check for new courses or alterations in the old ones
    new_courses = __check_courses_differences(state, courses.keys())

    # Add the new courses to the config
    for c_id in new_courses:
        course = Course(c_id, courses[c_id], state.default_action == "download")
        content = get_course_contents(state, c_id)
        course.read_json(content)
        state.add_course(course)

    # Write to the config.json the new courses
    write_config(state)

    # Check what to do
    if state.default_action == 'notify':
        # TODO Better notification
        logging.warning("New courses were found, please change the config.json to which contents you want to download.")
    elif state.default_action == 'download':
        # TODO Download
        logging.info("Downloading")


def __check_courses_differences(state: Config, courses_id_received: list):
    """ This function is responsible for checking if new courses appeared or if there was any change to the downloaded
    courses"""

    # Find new courses
    new_courses = []

    for c_id in courses_id_received:
        if c_id not in state.courses:
            new_courses.append(c_id)

    # TODO Find courses that might have changed

    return new_courses
