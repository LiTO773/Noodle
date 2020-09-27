from model.ConvertToDict import ConvertToDict
from model.file import File


class Folder(ConvertToDict):
    """ This class stores the information of a Moodle folder """
    def __init__(self, body: dict, download=True):
        self.__create(body['id'], body['name'], body['url'], download)

        for content in body['contents']:
            new_file = File.create_file_or_url(content)
            if new_file is not None:
                self.files.append(new_file)

    def __create(self, id, name, url, download=True):
        self.id = id
        self.name = name
        self.url = url
        self.download = download
        self.downloaded = False
        self.files = []

    def to_dict(self):
        files_dict = []

        for file in self.files:
            files_dict.append(file.to_dict())

        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'download': self.download,
            'downloaded': self.downloaded,
            'files': files_dict
        }
