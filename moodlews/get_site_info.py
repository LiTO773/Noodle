from model.config import Config
from .moodle_request import _moodle_request


def get_site_info(state: Config) -> (int, str):
    """ This function is used to get the userid which is necessary to communicate with the Moodle Web Services."""
    body = _moodle_request(state, 'core_webservice_get_site_info')
    return body['userid']
