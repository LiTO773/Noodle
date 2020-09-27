import requests
import json
from model.config import Config


def _moodle_request(infos: Config, wsfunction: str, extras: dict = {}) -> dict:
    """ This is an helper function that streamlines the requests made to Moodle's Web Services """
    url = __generate_ws_url(infos)
    params = {'wstoken': infos.get_token(), 'wsfunction': wsfunction, 'moodlewsrestformat': 'json'}
    params.update(extras)

    response = requests.post(url, params=params)
    return json.loads(response.content)


def __generate_ws_url(infos: Config):
    return infos.get_host() + ('/' if infos.get_host()[-1] != '/' else '') + 'webservice/rest/server.php'
