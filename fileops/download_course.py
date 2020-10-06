import logging
import os

from fileops.download_file import download_file
from fileops.download_linkablecontent import download_linkablecontent
from fileops.helpers import _create_path
from model.ContentWrapper import ContentWrapper
from model.Config import Config
from model.LinkableContents import LinkableContent
from model.course import Course
from model.file import File


def download_course(course: Course, state: Config):
    """
    Downloads all the contents where download = True in a course.
    :param course: Course to download
    :param state: Moodle's config
    """
    __download_content_wrappers(course, state.location, state)


def __download_content_wrappers(cw: ContentWrapper, location: str, state: Config):
    print(cw)
    """
    Downloads all the contents present in a content wrapper. This avoids the re-definition of identical functions for
    Courses, Sections and Folder
    :param cw: ContentWrapper to be downloaded
    :param location: Location to where it will be downloaded
    :param state: Moodle's config
    """
    # Check if it is meant to be downloaded
    if not cw.download:
        return

    # Create the folder if it doesn't exist
    new_path = _create_path(location, cw.name)
    try:
        os.makedirs(new_path)
    except OSError as e:
        logging.info(cw.name + ' folder already exists')

    # Download either the files or another ContentWrapper
    for content in cw.contents:
        print(content.name)
        if isinstance(content, ContentWrapper):
            __download_content_wrappers(content, new_path, state)
        elif isinstance(content, File):
            download_file(content, new_path, state)
        elif isinstance(content, LinkableContent):
            download_linkablecontent(content, new_path)
