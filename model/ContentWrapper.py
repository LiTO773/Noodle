class ContentWrapper:
    """ This is an interface that identifies classes that contain more than one contents (aka everything but files and
    urls) """
    def contents(self):
        pass

    def name(self):
        pass

    def download(self):
        pass

    def downloaded(self):
        pass