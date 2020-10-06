from typing import List, Union

from model.ContentWrapper import ContentWrapper
from model.LinkableContents import LinkableContent
from model.file import File
from model.module import Module


class Section(ContentWrapper):
    """ This class is responsible for storing the information about a course's section """
    @staticmethod
    def create_from_db(info: tuple):
        section = Section(info[0], info[2], info[3] == 1)
        section.__set_remaining_params(info[4] == 1, info[5])
        return section

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.__downloaded = downloaded
        self.__db_hash = current_hash

    def __init__(self, id, name, download=False):
        self.__id = id
        self.__name = name
        self.__download = download
        self.__downloaded = False
        self.__modules = []

    def read_json_contents(self, body: dict):
        """
        This function is responsible for populating the section with the data found in the JSON.
        :param body: JSON info
        """
        for module in body:
            if module['modname'] == 'folder' or module['modname'] == 'resource':
                # It's a module
                new_folder = Module.create_from_json(module, self.__download)
                self.__modules.append(new_folder)
            elif module['modname'] != 'label':
                # It's a LinkableContent
                lc = LinkableContent.create_from_json(module)
                self.__modules.append(lc)

    # GETTERS
    @property
    def id(self):
        return self.__id

    @property
    def modules(self):
        return self.__modules

    @property
    def name(self):
        return self.__name

    @property
    def download(self):
        return self.__download

    @property
    def downloaded(self):
        return self.__downloaded

    @property
    def contents(self):
        return self.modules

    # SETTERS
    @modules.setter
    def modules(self, new_modules: List[Union[Module, LinkableContent]]):
        self.__modules = new_modules.copy()

    def add_module(self, file):
        self.__modules.append(file)

    def __hash__(self):
        file_hash_str = 0

        for file in self.__modules:
            file_hash_str += hash(file)

        return hash((self.__id, file_hash_str))