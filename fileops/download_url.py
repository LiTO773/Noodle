import logging

from fileops.helpers import _create_path
from model.url import URL


def download_url(url: URL, location: str):
    """
    Creates a new URL file for a certain URL.
    :param url: URL to be saved
    :param location: Location to be saved
    """
    print(url.get_name() + ' ' + url.get_download())

    if not url.get_download():
        return

    url_disk_path = _create_path(location, url.get_name() + '.url')
    try:
        with open(url_disk_path, "w") as url_file:
            url_file.write('[InternetShortcut]\nURL={}'.format(url.get_url()))
    except OSError as e:
        logging.error(url.get_name() + ' unable to write')
