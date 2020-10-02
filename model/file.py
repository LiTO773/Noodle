from model.url import URL


class File:
    """ This class stores the information of a Moodle file """

    @staticmethod
    def create_from_db(info: tuple):
        file = File(info[2], info[3], info[4], info[5], info[6], info[7])
        file.__set_remaining_params(info[8], info[9])
        return file

    @staticmethod
    def create_from_json(body: dict, download=False):
        return File(body['filename'], body['filesize'], body['fileurl'], body['timecreated'], body['timemodified'],
                    download)

    @staticmethod
    def create_file_or_url(body: dict, download=False):
        """ Returns a file, a URL or None if it is none of those """
        if body['type'] == 'file':
            return File.create_from_json(body, download)
        elif body['type'] == 'url':
            return URL.create_from_json(body, download)

        return None

    def __init__(self, filename, filesize, fileurl, timecreated, timemodified, download=False):
        self.__filename = filename
        self.__filesize = filesize
        self.__fileurl = fileurl
        self.__timecreated = timecreated
        self.__timemodified = timemodified
        self.__download = download
        self.__downloaded = False
        self.__current_hash = -1

    def __set_remaining_params(self, downloaded, current_hash):
        """ Used to add parameters already available in the DB """
        self.__downloaded = downloaded
        self.__current_hash = current_hash

    def __hash__(self):
        return hash((self.__filename, self.__filesize, self.__fileurl, self.__timecreated, self.__timemodified))

    def get_name(self):
        return self.__filename

    def get_size(self):
        return self.__filesize

    def get_url(self):
        return self.__fileurl

    def get_time_created(self):
        return self.__timecreated

    def get_time_modified(self):
        return self.__timemodified

    def get_download(self):
        return self.__download
