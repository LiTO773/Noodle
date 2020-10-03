from enum import Enum


class MoodlePossibleContents(Enum):
    """
    This enum stores all the types of resources a Moodle can contain. Each name corresponds to the value of the modname
    property
    """
    assignment = 1
    book = 2
    chat = 3
    choice = 4
    database = 5
    lti = 6  # External tool
    feedback = 7
    file = 8
    folder = 9
    forum = 10
    glossary = 11
    h5p = 12
    imscp = 13  # IMS Content Package
    label = 14
    lesson = 15
    page = 16
    quiz = 17
    scorm = 18
    survey = 19
    url = 20
    wiki = 21
    workshop = 22
