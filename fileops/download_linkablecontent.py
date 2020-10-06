import logging

from fileops.helpers import _create_path
from model.LinkableContents import LinkableContent


def download_linkablecontent(url: LinkableContent, location: str):
    """
    Creates a new URL file for a certain URL.
    :param url: URL to be saved
    :param location: Location to be saved
    """
    url_disk_path = _create_path(location, url.name + '.url')
    try:
        with open(url_disk_path, "w") as url_file:
            url_file.write('[InternetShortcut]\nURL={}'.format(url.url))
    except OSError as e:
        logging.error(url.name + ' unable to write')
