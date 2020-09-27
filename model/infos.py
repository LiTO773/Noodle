from model.course import Course


class Infos():
    userid = -1

    def __init__(self, host, username, password, courses, default_action, token):
        self.host = host
        self.username = username
        self.password = password
        self.courses = courses # Dict of id: Course
        self.default_action = default_action
        self.token = token

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

