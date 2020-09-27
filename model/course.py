from model.ConvertToDict import ConvertToDict
from model.file import File
from model.folder import Folder


class Course(ConvertToDict):
    """ This class is responsible for storing all the info in a course """
    downloaded = False
    current_hash = -1

    @staticmethod
    def create_from_db(info: tuple):
        course = Course(info[0], info[2], info[3] == 1)
        course.__set_remaining_params(info[4] == 1, info[5])
        return course

    def __init__(self, id, shortname, download=False):
        self.id = id
        self.shortname = shortname
        self.download = download
        self.downloaded = False
        self.sections = []

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.downloaded = downloaded
        self.current_hash = current_hash

    def read_json(self, body: dict):
        for section in body:
            new_section = Section(section['id'], section['name'], self.download)
            new_section.read_json(section['modules'])
            self.sections.append(new_section)

    def to_dict(self):
        section_dict = []

        for section in self.sections:
            section_dict.append(section.to_dict())

        return {
            'id': self.id,
            'shortname': self.shortname,
            'download': self.download,
            'downloaded': self.downloaded,
            'sections': section_dict,
            'hash': hash(self)
        }

    def __hash__(self):
        section_hash_str = 0

        for section in self.sections:
            section_hash_str += hash(section)

        return hash((self.id, section_hash_str))


class Section(ConvertToDict):
    """ This class is responsible for storing the information about a course's section """
    @staticmethod
    def create_from_db(info: tuple):
        section = Section(info[0], info[2], info[3] == 1)
        section.__set_remaining_params(info[4] == 1, info[5])
        return section

    def __init__(self, id, name, download=False):
        self.id = id
        self.name = name
        self.download = download
        self.downloaded = False
        self.files = []

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.downloaded = downloaded
        self.current_hash = current_hash

    def read_json(self, body: dict):
        for module in body:
            if module['modname'] == 'resource':
                # It's either a file or a URL
                new_file = File.create_file_or_url(module['contents'][0])
                if new_file is not None:
                    self.files.append(new_file)
            elif module['modname'] == 'folder':
                # It's a folder
                new_folder = Folder(module)
                self.files.append(new_folder)

    def add_files(self, files: list):
        self.files = files.copy()

    def add_file(self, file):
        self.files.append(file)

    def to_dict(self):
        files_dict = []

        for file in self.files:
            files_dict.append(file.to_dict())

        return {
            'id': self.id,
            'name': self.name,
            'download': self.download,
            'downloaded': self.downloaded,
            'files': files_dict,
            'hash': hash(self)
        }

    def __hash__(self):
        file_hash_str = 0

        for file in self.files:
            file_hash_str += hash(file)

        return hash((self.id, file_hash_str))
