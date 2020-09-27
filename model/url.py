from model.ConvertToDict import ConvertToDict


class URL(ConvertToDict):
    """ This class stores the information of a Moodle folder """
    def __init__(self, body: dict, download=True):
        self.filename = body['filename']
        self.filesize = body['filesize']
        self.fileurl = body['fileurl']
        self.download = download
        self.downloaded = False

    def to_dict(self):
        return {
            'filename': self.filename,
            'filesize': self.filesize,
            'fileurl': self.fileurl,
            'download': self.download,
            'downloaded': self.downloaded
        }
