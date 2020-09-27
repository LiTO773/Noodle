from model.ConvertToDict import ConvertToDict
from model.url import URL


class File(ConvertToDict):
    """ This class stores the information of a Moodle file """
    @staticmethod
    def create_from_db(info: tuple):
        file = File(info[2], info[3], info[4], info[5], info[6], info[7])
        file.__set_remaining_params(info[8], info[9])
        return file

    @staticmethod
    def create_from_json(body: dict, download=True):
        return File(body['filename'], body['filesize'], body['fileurl'], body['timecreated'], body['timemodified'],
                      download)

    @staticmethod
    def create_file_or_url(body: dict):
        """ Returns a file, a URL or None if it is none of those """
        if body['type'] == 'file':
            return File(body)
        elif body['type'] == 'url':
            return URL(body)

        return None

    def __init__(self, filename, filesize, fileurl, timecreated, timemodified, download=False):
        self.filename = filename
        self.filesize = filesize
        self.fileurl = fileurl
        self.timecreated = timecreated
        self.timemodified = timemodified
        self.download = download
        self.downloaded = False

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.downloaded = downloaded
        self.current_hash = current_hash

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