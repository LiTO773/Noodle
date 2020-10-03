import json

import requests

from model.Config import Config


def _moodle_request(infos: Config, wsfunction: str, extras: dict = {}) -> dict:
    """ This is an helper function that streamlines the requests made to Moodle's Web Services """
    url = __generate_ws_url(infos)
    params = {'wstoken': infos.token, 'wsfunction': wsfunction, 'moodlewsrestformat': 'json'}
    params.update(extras)

    response = requests.post(url, params=params)
    return json.loads(response.content)


def __generate_ws_url(infos: Config):
    return infos.host + ('/' if infos.host[-1] != '/' else '') + 'webservice/rest/server.php'
