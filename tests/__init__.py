import os


basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    SECRET_KEY = os.urandom(20)
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_FILES_DEST = os.path.join(basedir, 'test_uploads')
    MAIL_SERVER = 'localhost'
    APP_MAIL = 'snakedrive@snakedrive.com'
    TESTING = True


class TestData:
    VALID_USER = {
        'email': 'test@test.com',
        'username': 'test',
        'password': 'password',
        'verified': False
    }
    VALID_USER_PUT = {
        'email': 'tset@tset.moc',
        'username': 'tset',
        'password': 'drowssap',
        'verified': False
    }
    INVALID_USER = {
        'email': 'test@test.com',
        'username': 'test'
    }
    INVALID_EMAIL = {
        'email': 'invalidemail',
        'username': 'test',
        'password': 'password',
        'verified': False
    }
    INVALID_USERNAME = {
        'email': 'test@test.com',
        'username': '!_test_!',
        'password': 'password',
        'verified': False
    }

    EXPECTED_VALID_USER = {
        'id': 1,
        'email': 'test@test.com',
        'username': 'test',
        'verified': False
    }
    EXPECTED_VALID_USER_PUT = {
        'id': 1,
        'email': 'tset@tset.moc',
        'username': 'tset',
        'verified': False
    }
    EXPECTED_INVALID_USER = {
        'error': 'Bad Request',
        'message': 'Must include username, email and password fields'
    }
    EXPECTED_INVALID_EMAIL = {
        'error': 'Bad Request',
        'message': 'Data must contain valid email'
    }
    EXPECTED_INVALID_USERNAME = {
        'error': 'Bad Request',
        'message': 'Data must contain valid username'
    }
    EXPECTED_INVALID_TOKEN = {
        'error': 'Unauthorized'
    }
    EXPECTED_INVALID_USER_PUT = {
        'error': 'Bad Request',
        'message': 'Must include at least one of: username, email, password'
    }
