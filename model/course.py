from model.ContentWrapper import ContentWrapper
from model.section import Section


class Course(ContentWrapper):
    """ This class is responsible for storing all the info about a course """

    @staticmethod
    def create_from_db(info: tuple):
        """ Allows the creation of a Course object from DB information """
        course = Course(info[0], info[2], info[3] == 1)
        course.__set_remaining_params(info[4] == 1, info[5])
        return course

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.__downloaded = downloaded
        self.__db_hash = current_hash

    def __init__(self, id: int, shortname: str, download: bool=False):
        self.__id = id
        self.__shortname = shortname
        self.__download = download
        self.__downloaded = False
        self.__sections = []

    # GETTER
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__shortname

    @property
    def download(self):
        return self.__download

    @property
    def downloaded(self):
        return self.__downloaded

    @property
    def sections(self):
        return self.__sections

    @property
    def contents(self):
        return self.__sections

    def read_json_contents(self, body: dict):
        """
        This function is responsible for populating the course with the data found in the JSON.
        :param body: JSON info
        """
        for section in body:
            new_section = Section(section['id'], section['name'], self.__download)
            new_section.read_json_contents(section['modules'])
            self.__sections.append(new_section)

    def __hash__(self):
        section_hash_str = 0

        for section in self.__sections:
            section_hash_str += hash(section)

        return hash((self.__id, section_hash_str))