from errors.error_codes import UNABLE_TO_LOGIN
from model.infos import Infos
from .moodle_request import _moodle_request


def get_site_info(state: Infos):
    """ This function is used to get the necessary params to communicate with the Moodle Web Services.
    THE PARAM state IS MUTATED IN THIS FUNCTION"""
    body = _moodle_request(state, 'core_webservice_get_site_info')
    state.userid = body['userid']
