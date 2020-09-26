import requests
import json
from errors.error_codes import UNABLE_TO_LOGIN
from model.infos import Infos


def _moodle_request(infos: Infos, wsfunction: str, extras: dict = {}) -> dict:
    """ This is an helper function that streamlines the requests made to Moodle's Web Services """
    url = infos.host + ('/' if infos.host[-1] != '/' else '') + 'webservice/rest/server.php'
    params = {'wstoken': infos.token, 'wsfunction': wsfunction, 'moodlewsrestformat': 'json'}
    params.update(extras)

    response = requests.post(url, params=params)
    return json.loads(response.content)
