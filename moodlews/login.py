import requests
import json
from errors.error_codes import UNABLE_TO_LOGIN

def login(config: dict) -> str:
    """ This function is used to login to moodle. It returns the token if it was successful, otherwise returns
    UNABLE_TO_LOGIN """
    url = config['host'] + ('/' if config['host'][-1] == '/' else '') + 'login/token.php'
    params = {'username': config['username'], 'password': config['password'], 'service': 'moodle_mobile_app'}

    response = requests.post(url, params=params)
    return json.loads(response.content).get('token', UNABLE_TO_LOGIN)
