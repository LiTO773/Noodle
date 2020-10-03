import logging

import requests

from model.Config import Config


def ws_download_file(file_url: str, infos: Config) -> bytes:
    """
    This function ios responsible for downloading a file and returning it's content.

    For more information on how the download works on Moodle WS, check:
    https://github.com/moodlehq/sample-ws-clients/blob/master/PHP-HTTP-filehandling/client.php
    :param file_url: The file's url
    :param infos: Configuration file with the Moodle's info
    :return: File content
    """
    params = {'token': infos.token}
    print(file_url)

    response = requests.get(file_url, params=params)
    return response.content
