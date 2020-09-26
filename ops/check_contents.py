from model.infos import Infos
from moodlews.get_courses import get_courses


def check_contents(state: Infos):
    """ This function is responsible for checking all the contents available in the user's Moodle. Any alterations
    will be writing to the config file and the corresponding files downloaded """
    courses = get_courses(state)

    print(__check_courses_differences(state, courses.keys()))


def __check_courses_differences(state: Infos, courses_id_received: list):
    """ This function is responsible for checking if new courses appeared and if so return them. """
    new_courses = []

    for c_id in courses_id_received:
        if c_id not in state.courses:
            new_courses.append(c_id)

    return new_courses
