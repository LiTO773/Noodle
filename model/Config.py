import logging

from model.course import Course


class Config:
    @staticmethod
    def create_from_db(info: tuple):
        return Config(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7])

    def __init__(self, id, host, username, password, max_download_size, default_action, userid, location):
        self.__id = id
        self.__host = host
        self.__username = username
        self.__password = password
        self.__max_download_size = max_download_size
        self.__default_action = default_action
        self.__userid = userid
        self.__location = location
        self.__token = ''
        self.__courses = {}

    # GETTERS
    @property
    def id(self):
        """ ID property """
        return self.__id

    @property
    def host(self):
        return self.__host

    @property
    def token(self):
        return self.__token

    @property
    def userid(self):
        return self.__userid

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def courses(self):
        return self.__courses

    @property
    def default_action(self):
        return self.__default_action

    @property
    def location(self):
        return self.__location

    # SETTERS
    @token.setter
    def token(self, token: str):
        if not isinstance(token, str):
            logging.error("The given token isn't valid")
            return
        self.__token = token

    @userid.setter
    def userid(self, userid: int):
        """ Returns False if the userid has changed or is invalid. If it is different, it will update the object with
        the new one and return True """
        if not isinstance(userid, int):
            logging.error("The given userid isn't valid")
            return

        if userid == self.__userid:
            logging.info("The userid hasn't changed")
            return

        self.__userid = userid

    # Python methods

    def __str__(self):
        return "Host: {}, Username: {}, Password: {}, Token: {}, Userid: {}"\
            .format(self.__host, self.__username, self.__password, self.__token, self.__userid)

    # Other methods
    def add_course(self, course: Course):
        self.__courses[course.id] = course
