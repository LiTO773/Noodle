from model.ConvertToDict import ConvertToDict
from model.Identifiable import Identifiable
from model.file import File
from model.folder import Folder


class Section(Identifiable, ConvertToDict):
    """ This class is responsible for storing the information about a course's section """
    @staticmethod
    def create_from_db(info: tuple):
        section = Section(info[0], info[2], info[3] == 1)
        section.__set_remaining_params(info[4] == 1, info[5])
        return section

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.__downloaded = downloaded
        self.__current_hash = current_hash

    def __init__(self, id, name, download=False):
        self.__id = id
        self.__name = name
        self.__download = download
        self.__downloaded = False
        self.__files = []

    def id(self):
        return self.__id

    def read_json_contents(self, body: dict):
        for module in body:
            if module['modname'] == 'resource':
                # It's either a file or a URL
                new_file = File.create_file_or_url(module['contents'][0], self.__download)
                if new_file is not None:
                    self.__files.append(new_file)
            elif module['modname'] == 'folder':
                # It's a folder
                new_folder = Folder.create_from_json(module, self.__download)
                self.__files.append(new_folder)

    def add_files(self, files: list):
        self.__files = files.copy()

    def add_file(self, file):
        self.__files.append(file)

    def to_dict(self):
        files_dict = []

        for file in self.__files:
            files_dict.append(file.to_dict())

        return {
            'id': self.__id,
            'name': self.__name,
            'download': self.__download,
            'downloaded': self.__downloaded,
            'files': files_dict,
            'hash': hash(self)
        }

    def __hash__(self):
        file_hash_str = 0

        for file in self.__files:
            file_hash_str += hash(file)

        return hash((self.__id, file_hash_str))

    def get_name(self):
        return self.__name

    def get_download(self):
        return self.__download

    def get_files(self):
        return self.__files