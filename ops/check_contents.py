from model.infos import Infos
from moodlews.get_courses import get_courses


def check_contents(state: Infos):
    """ This function is responsible for checking all the contents available in the user's Moodle. Any alterations
    will be writing to the config file and the corresponding files downloaded """
    print(get_courses(state))
