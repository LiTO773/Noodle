class Infos:
    userid = -1

    def __init__(self, host, username, password, token):
        self.host = host
        self.username = username
        self.password = password
        self.token = token

    def __str__(self):
        return "Host: {}, Username: {}, Password: {}, Token: {}, Userid: {}"\
            .format(self.host, self.username, self.password, self.token, self.userid)
