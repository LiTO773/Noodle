from model.ConvertToDict import ConvertToDict


class URL(ConvertToDict):
    """ This class stores the information of a Moodle folder """
    def __init__(self, body: dict, download=True):
        self.__filename = body['filename']
        self.__filesize = body['filesize']
        self.__fileurl = body['fileurl']
        self.__download = download
        self.__downloaded = False

    def to_dict(self):
        return {
            'filename': self.__filename,
            'filesize': self.__filesize,
            'fileurl': self.__fileurl,
            'download': self.__download,
            'downloaded': self.__downloaded,
            'hash': hash(self)
        }

    def __hash__(self):
        return hash((self.__filename, self.__filesize, self.__fileurl))
