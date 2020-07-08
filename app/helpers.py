import pathlib
import string
import re


def delete_folder(path):
    for child in path.iterdir():
        if child.is_dir():
            delete_folder(child)
        else:
            path.unlink()
    path.rmdir()


def valid_username(username):
    if len(username) >= 1:
        forbidden_chars = string.punctuation
        return not any(char in forbidden_chars for char in username)
    return False


def valid_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    return False
