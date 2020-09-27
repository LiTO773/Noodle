from errors.error_codes import UNABLE_TO_LOGIN
from model.config import Config
from .moodle_request import _moodle_request


def get_course_contents(state: Config, course_id: int):
    """ This function gets the infos about a course """
    body = _moodle_request(state, 'core_course_get_contents', {'courseid': course_id})
    return body
