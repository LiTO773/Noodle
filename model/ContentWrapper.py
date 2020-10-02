from model.Downloadable import Downloadable


class ContentWrapper(Downloadable):
    """ This is an interface that identifies classes that contain more than one contents (aka everything but files and
    urls) """
    def get_contents(self):
        pass