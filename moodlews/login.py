import json

import requests

from errors.error_codes import UNABLE_TO_LOGIN
from model.config import Config


def login(config: Config) -> str:
    """ This function is used to login to moodle. It returns the token if it was successful, otherwise returns
    UNABLE_TO_LOGIN """
    url = config.get_host() + ('/' if config.get_host()[-1] != '/' else '') + 'login/token.php'
    params = {'username': config.get_username(), 'password': config.get_password(), 'service': 'moodle_mobile_app'}

    response = requests.post(url, params=params)
    return json.loads(response.content).get('token', UNABLE_TO_LOGIN)
