class URL:
    """ This class stores the information of a Moodle URL. This can be anything that isn't a file or a content wrapper
    """
    @staticmethod
    def create_from_db(info: tuple):
        url = URL(info[2], info[3], info[4], info[5])
        url.__set_remaining_params(info[6], info[7])
        return url

    @staticmethod
    def create_from_json(body: dict, download=False):
        return URL(body['filename'], body['fileurl'], body['timemodified'], download)

    def __init__(self, filename: str, fileurl: str, timemodified: int, download: bool = False):
        self.__filename = filename
        self.__fileurl = fileurl
        self.__timemodified = timemodified
        self.__download = download
        self.__downloaded = False

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.__downloaded = downloaded
        self.__db_hash = current_hash

    def __hash__(self):
        return hash((self.__filename, self.__fileurl))

    # GETTERS
    @property
    def name(self):
        return self.__filename

    @property
    def url(self):
        return self.__fileurl

    @property
    def time_modified(self):
        return self.__timemodified

    @property
    def download(self):
        return self.__download
