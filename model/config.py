from model.Identifiable import Identifiable
from model.course import Course


class Config(Identifiable):
    token = ''
    courses = []

    @staticmethod
    def create_from_db(info: tuple):
        return Config(info[0], info[1], info[2], info[3], info[4], info[5], info[6])

    def __init__(self, id, host, username, password, max_download_size, default_action, userid):
        self.__id = id
        self.__host = host
        self.__username = username
        self.__password = password
        self.__max_download_size = max_download_size
        self.__default_action = default_action
        self.__userid = userid
        self.__token = ''
        self.__courses = []

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

