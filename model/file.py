from model.ConvertToDict import ConvertToDict
from model.url import URL


class File(ConvertToDict):
    @staticmethod
    def create_file_or_url(body: dict):
        """ Returns a file, a URL or None if it is none of those """
        if body['type'] == 'file':
            return File(body)
        elif body['type'] == 'url':
            return URL(body)

        return None

    """ This class stores the information of a Moodle folder """
    def __init__(self, body: dict, download=True):
        self.__create(body['filename'], body['filesize'], body['fileurl'], body['timecreated'], body['timemodified'],
                      download)

    def __create(self, filename, filesize, fileurl, timecreated, timemodified, download):
        self.filename = filename
        self.filesize = filesize
        self.fileurl = fileurl
        self.timecreated = timecreated
        self.timemodified = timemodified
        self.download = download
        self.downloaded = False

    def to_dict(self):
        return {
            'filename': self.filename,
            'filesize': self.filesize,
            'fileurl': self.fileurl,
            'timecreated': self.timecreated,
            'timemodified': self.timemodified,
            'download': self.download,
            'downloaded': self.downloaded,
            'hash': hash(self)
        }

    def __hash__(self):
        return hash((self.filename, self.filesize, self.fileurl, self.timecreated, self.timemodified))