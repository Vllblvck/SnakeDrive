import string
import re


#Used by api and web app
def valid_username(username):
    if len(username) >= 1 and len(username) <= 32:
        forbidden_chars = string.punctuation
        return not any(char in forbidden_chars for char in username)
    return False


#Used by api
def valid_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email) and len(email) <= 120:
        return True
    return False
