class Downloadable:
    """ This is an interface that identifies classes that can be downloaded (aka all but Config) """
    def get_download(self):
        pass

    def get_downloaded(self):
        pass