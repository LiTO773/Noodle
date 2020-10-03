import logging

from fileops.helpers import _create_path
from model.Config import Config
from model.file import File
from moodlews.download_file import ws_download_file


def download_file(file: File, location: str, state: Config):
    """
    Download a new file
    :param file: File to be downloaded
    :param location: Location to be saved
    :param state: Moodle's config
    """
    if not file.get_download():
        return

    file_path = _create_path(location, file.get_name())
    file_content = ws_download_file(file.get_url(), state)

    try:
        with open(file_path, "wb") as downloaded_file:
            downloaded_file.write(file_content)
    except OSError as e:
        logging.error(file.get_name() + ' unable to write')
