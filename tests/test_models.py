import time
import unittest

from tests import TestConfig, TestData
from app import create_app, db
from app.models import User


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User()
        user.set_password('password')
        self.assertFalse(user.check_password('pass'))
        self.assertTrue(user.check_password('password'))

    def test_api_tokens(self):
        user = User()
        user.from_dict(TestData.VALID_USER, new_user=True)
        token = user.get_api_token()
        db.session.commit()

        self.assertEqual(user, User.check_api_token(token))
        user.revoke_api_token()
        self.assertEqual(None, User.check_api_token(token))

    def test_jwt_tokens(self):
        user = User()
        user.from_dict(TestData.VALID_USER, new_user=True)
        db.session.add(user)
        db.session.commit()

        token = user.get_jwt_token()
        self.assertEqual(user, User.check_jwt_token(token))

        token = user.get_jwt_token(expires_in=1)
        time.sleep(2)
        self.assertEqual(None, User.check_jwt_token(token))


if __name__ == '__main__':
    unittest.main()
