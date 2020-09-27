from model.course import Course


class Config:
    token = ''
    courses = []

    @staticmethod
    def create_from_db(info: tuple):
        return Config(info[0], info[1], info[2], info[3], info[4], info[5], info[6])

    def __init__(self, db_id, host, username, password, max_download_size, default_action, userid):
        self.db_id = db_id
        self.host = host
        self.username = username
        self.password = password
        self.max_download_size = max_download_size
        self.default_action = default_action
        self.userid = userid

    def add_token(self, token: str):
        self.token = token

    def add_courses(self, courses):
        self.courses = courses

    def __str__(self):
        return "Host: {}, Username: {}, Password: {}, Token: {}, Userid: {}"\
            .format(self.host, self.username, self.password, self.token, self.userid)

    def add_course(self, course: Course):
        self.courses[course.id] = course

    def to_writable_dict(self):
        dict_courses = {}

        for course in self.courses:
            dict_courses[course] = self.courses[course].to_dict()

        return {
            'host': self.host,
            'username': self.username,
            'password': self.password,
            'courses': dict_courses,
            'default_action': self.default_action
        }

