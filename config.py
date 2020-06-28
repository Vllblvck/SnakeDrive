import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
            'mysql://snakedrive:snakedrive@localhost/snakedrivedb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
