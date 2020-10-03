from model.ContentWrapper import ContentWrapper
from model.Identifiable import Identifiable
from model.file import File


class Module(Identifiable, ContentWrapper):
    """ This class stores the information of a Moodle module """
    @staticmethod
    def create_from_db(info: tuple):
        folder = Module(info[0], info[2], info[3], info[4])
        folder.__set_remaining_params(info[5], info[6])
        return folder

    @staticmethod
    def create_from_json(body: dict, download=False):
        folder = Module(body['id'], body['name'], body['url'], download)

        for content in body['contents']:
            new_file = File.create_file_or_url(content, download)
            if new_file is not None:
                folder.add_content(new_file)

    def __init__(self, id, name, url, download=False):
        self.__id = id
        self.__name = name
        self.__url = url
        self.__download = download
        self.__downloaded = False
        self.__contents = []

    def id(self):
        return self.__id

    def add_content(self, file):
        self.__contents.append(file)

    def add_contents(self, files: list):
        self.__contents = files.copy()

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.__downloaded = downloaded
        self.__db_hash = current_hash

    def __hash__(self):
        file_hash_str = 0

        for file in self.__contents:
            file_hash_str += hash(file)

        return hash((self.__id, self.__url, file_hash_str))

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_download(self):
        return self.__download

    def get_downloaded(self):
        return self.__downloaded

    def get_contents(self):
        return self.__contents
