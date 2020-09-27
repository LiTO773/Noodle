from model.ConvertToDict import ConvertToDict
from model.file import File
from model.folder import Folder


class Course(ConvertToDict):
    """ This class is responsible for storing all the info in a course """
    def __init__(self, id, shortname, download=True):
        self.id = id
        self.shortname = shortname
        self.download = download
        self.downloaded = False
        self.sections = []

    def read_json(self, body: dict):
        for section in body:
            new_section = _Section(section['id'], section['name'], self.download)
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
            'sections': section_dict
        }


class _Section(ConvertToDict):
    """ This class is responsible for storing the information about a course's section """
    def __init__(self, id, name, download=True):
        self.id = id
        self.name = name
        self.download = download
        self.downloaded = False
        self.files = []

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

    def to_dict(self):
        files_dict = []

        for file in self.files:
            files_dict.append(file.to_dict())

        return {
            'id': self.id,
            'name': self.name,
            'download': self.download,
            'downloaded': self.downloaded,
            'files': files_dict
        }

