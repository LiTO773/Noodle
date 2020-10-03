from abc import ABC, abstractmethod

from model.MoodlePossibleContents import MoodlePossibleContents


class LinkableContent(ABC):
    """
    Linkable Contents are contents present in Moodle that the application won't download, just keep their url.

    Right now those contents are:
     - Assignment
     - Book
     - Chat
     - Choice
     - Database
     - External Tool
     - Feedback
     - Forum
     - Glossary
     - H5P
     - IMS content package
     - Label
     - Lesson
     - Page
     - Quiz
     - SCORM package
     - Survey
     - URL
     - Wiki
     - Workshop

    It is possible, in the future, that some of this contents might be stored in their own data structure and persisted
    in the DB. When that's the case, please remove it from here :)
    """

    def __init__(self, representing: MoodlePossibleContents, parent_id: int, name: str, url: str, own_id: int = None):
        """
        Creates a LinkableContent
        :param representing: What the class is representing (could be a Quiz, URL, Assignment, etc.)
        :param parent_id: ID of the parent, likely a section or a module
        :param own_id: It's own ID. This parameter is optional, since materials in the "contents" section of a module
        don't have an ID
        :param name: Name of the content
        :param url: URL of the content
        """
        self.__representing = representing
        self.__parent_id = parent_id
        self.__own_id = own_id
        self.__name = name
        self.__url = url

    # GETTERS
    @property
    def representing(self):
        """ Representing property """
        return self.__representing

    @property
    def parent_id(self):
        """ Parent_id property """
        return self.__parent_id

    @property
    def own_id(self):
        """ Own_id property """
        return self.__own_id

    @property
    def name(self):
        """ Name property """
        return self.__name

    @property
    def url(self):
        """ URL property """
        return self.__url

    @abstractmethod
    @property
    def content_id(self):
        pass