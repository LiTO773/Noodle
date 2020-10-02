import logging

from model.Identifiable import Identifiable
from model.course import Course


class Config(Identifiable):
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

    def id(self):
        return self.__id

    def add_token(self, token: str):
        self.__token = token

    def add_courses(self, courses):
        self.__courses = courses

    def __str__(self):
        return "Host: {}, Username: {}, Password: {}, Token: {}, Userid: {}"\
            .format(self.__host, self.__username, self.__password, self.__token, self.__userid)

    def add_course(self, course: Course):
        self.__courses[course.id()] = course

    def to_writable_dict(self):
        dict_courses = {}

        for course in self.__courses:
            dict_courses[course] = self.__courses[course].to_dict()

        return {
            'host': self.__host,
            'username': self.__username,
            'password': self.__password,
            'courses': dict_courses,
            'default_action': self.__default_action
        }

    def get_host(self):
        return self.__host

    def get_token(self):
        return self.__token

    def get_userid(self):
        return self.__userid

    def update_userid(self, userid: int):
        """ Returns False if the userid has changed or is invalid. If it is different, it will update the object with
        the new one and return True """
        if not isinstance(userid, int):
            logging.error("The given userid isn't valid")
            return False

        if userid == self.__userid:
            logging.info("The userid hasn't changed")
            return False

        self.__userid = userid
        return True

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def set_token(self, token: str):
        if not isinstance(token, str):
            logging.error("The given token isn't valid")
            return
        self.__token = token

    def get_courses(self):
        return self.__courses

    def get_default_action(self):
        return self.__default_action

    def get_location(self):
        return self.__location
