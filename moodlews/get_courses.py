from model.infos import Infos
from .moodle_request import _moodle_request


def get_courses(state: Infos):
    """ This function gets all the courses available to the user and returns their id and shortname """
    body = _moodle_request(state, 'core_enrol_get_users_courses', {'userid': state.userid})

    # Creates a list of (id, shortname) tuples
    return_value = []
    for obj in body:
        return_value.append((obj['id'], obj['shortname']))

    return return_value