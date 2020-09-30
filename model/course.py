from model.ConvertToDict import ConvertToDict
from model.Identifiable import Identifiable
from model.section import Section


class Course(Identifiable, ConvertToDict):
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
        self.__current_hash = current_hash

    def __init__(self, id: int, shortname: str, download: bool=False):
        self.__id = id
        self.__shortname = shortname
        self.__download = download
        self.__downloaded = False
        self.__sections = []

    def id(self):
        return self.__id

    def read_json_contents(self, body: dict):
        for section in body:
            new_section = Section(section['id'], section['name'], self.__download)
            new_section.read_json_contents(section['modules'])
            self.__sections.append(new_section)

    def to_dict(self):
        section_dict = []

        for section in self.__sections:
            section_dict.append(section.to_dict())

        return {
            'id': self.__id,
            'shortname': self.__shortname,
            'download': self.__download,
            'downloaded': self.__downloaded,
            'sections': section_dict,
            'hash': hash(self)
        }

    def __hash__(self):
        section_hash_str = 0

        for section in self.__sections:
            section_hash_str += hash(section)

        return hash((self.__id, section_hash_str))

    def add_section(self, section: Section):
        self.__sections.append(section)

    def get_shortname(self):
        return self.__shortname

    def get_download(self):
        return self.__download

    def get_sections(self):
        return self.__sections