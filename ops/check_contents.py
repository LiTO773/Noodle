import logging

from model.course import Course
from model.infos import Infos
from moodlews.get_course_contents import get_course_contents
from moodlews.get_courses import get_courses


def check_contents(state: Infos):
    """ This function is responsible for checking all the contents available in the user's Moodle. Any alterations
    will be writing to the config file and the corresponding files downloaded """
    courses = get_courses(state)

    # Check for new courses
    new_courses = __check_courses_differences(state, courses.keys())

    # Add the new courses to the config
    for c_id in new_courses:
        course = Course(c_id, courses[c_id], state.default_action == "download")
        content = get_course_contents(state, c_id)
        course.read_json(content)
        print(course.to_dict())

    # Check what to do
    if state.default_action == 'notify':
        # TODO Better notification
        logging.warning("New courses were found, please change the config.json to which contents you want to download.")


def __check_courses_differences(state: Infos, courses_id_received: list):
    """ This function is responsible for checking if new courses appeared and if so return them. """
    new_courses = []

    for c_id in courses_id_received:
        if c_id not in state.courses:
            new_courses.append(c_id)

    return new_courses
