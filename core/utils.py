# make lambda function that returns lower case string
from unidecode import unidecode


def create_key(string: str) -> str:
    """ given a string, return a string that only contains lowercase alphanumeric characters without accents """
    return unidecode(''.join(c for c in string if c.isalnum())).lower()
