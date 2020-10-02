import os
import re


def _create_path(base: str, tail: str) -> str:
    """
    Creates a safe path according to which OS the program is running on
    :param base: The current path
    :param tail: The last part of the path that is to be added
    :return: A new OS safe path
    """
    return base + ('\\' if os.name == 'nt' else '/') + __safe_file_name(tail)


def __safe_file_name(name: str) -> str:
    """
    This helper is responsible for removing forbidden OS characters from a certain string.
    :param name: String to be converted
    :return: Safe string
    """
    return re.sub(r'<|>|/|:|\"|\\|\||\?|\*', '', name)