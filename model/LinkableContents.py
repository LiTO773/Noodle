from model.MoodlePossibleContents import MoodlePossibleContents


class LinkableContent:
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
    @staticmethod
    def create_from_db(info: tuple):
        return LinkableContent(info[1], info[5], info[6], info[2], info[3], info[4])

    def __init__(self, modname: MoodlePossibleContents, name: str, url: str, section_id: int = None,
                 module_id: int = None, own_id: int = None):
        """
        Creates a LinkableContent
        :param modname: What the class is representing (could be a Quiz, URL, Assignment, etc.)
        :param name: Name of the content
        :param url: URL of the content
        :param section_id: ID of the section (can be None if module_id is filled)
        :param module_id: ID of the module (can be None if section_id is filled)
        :param own_id: It's own ID. This parameter is optional, since materials in the "contents" section of a module
        don't have an ID
        """
        self.__modname = modname
        self.__section_id = section_id
        self.__module_id = module_id
        self.__own_id = own_id
        self.__name = name
        self.__url = url

    # GETTERS
    @property
    def modname(self):
        """ Modname property """
        return self.__modname

    @property
    def section_id(self):
        """ Section_id property """
        return self.__section_id

    @property
    def module_id(self):
        """ Module_id property """
        return self.__module_id

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

    # Hash
    def __hash__(self):
        return hash((self.__name, self.__url))
