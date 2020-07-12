import unittest

from tests import TestConfig, TestData
from app import db, create_app
from app.models import User


class ApiUsersCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        with self.app.test_client() as client:
            result = client.post('/api/users', json=TestData.INVALID_USER)
            user = User.query.filter_by(
                username=TestData.INVALID_USER['username']).first()
            self.assertIsNone(user)
            self.assertEqual(400, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_USER, result.get_json())

            result = client.post('/api/users', json=TestData.INVALID_EMAIL)
            user = User.query.filter_by(
                email=TestData.INVALID_EMAIL['email']).first()
            self.assertIsNone(user)
            self.assertEqual(400, result.status_code)
            self.assertEqual(
                TestData.EXPECTED_INVALID_EMAIL, result.get_json())

            result = client.post('/api/users', json=TestData.INVALID_USERNAME)
            user = User.query.filter_by(
                username=TestData.INVALID_USERNAME['username']).first()
            self.assertIsNone(user)
            self.assertEqual(400, result.status_code)
            self.assertEqual(
                TestData.EXPECTED_INVALID_USERNAME, result.get_json())

            result = client.post('/api/users', json=TestData.VALID_USER)
            user = User.query.filter_by(
                username=TestData.VALID_USER['username']).first()
            self.assertIsNotNone(user)
            self.assertEqual(201, result.status_code)
            self.assertEqual(TestData.EXPECTED_VALID_USER, result.get_json())

    def test_get_user(self):
        user = User()
        user.from_dict(TestData.VALID_USER, new_user=True)
        token = user.get_token()
        db.session.add(user)
        db.session.commit()

        with self.app.test_client() as client:
            result = client.get(
                '/api/users',
                headers={'Authorization': 'Bearer {}'.format(token)}
            )
            self.assertEqual(200, result.status_code)
            self.assertEqual(TestData.EXPECTED_VALID_USER, result.get_json())

            result = client.get('/api/users')
            self.assertEqual(401, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_TOKEN,
                             result.get_json())

            result = client.get(
                '/api/users',
                headers={'Authorization': 'Bearer {}'.format('invalid_token')}
            )
            self.assertEqual(401, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_TOKEN,
                             result.get_json())

    def test_edit_user(self):
        user = User()
        user.from_dict(TestData.VALID_USER, new_user=True)
        token = user.get_token()
        db.session.add(user)
        db.session.commit()

        with self.app.test_client() as client:
            result = client.put('/api/users')
            self.assertEqual(401, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_TOKEN,
                             result.get_json())

            result = client.put(
                '/api/users',
                headers={'Authorization': 'Bearer {}'.format('invalid_token')}
            )
            self.assertEqual(401, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_TOKEN,
                             result.get_json())

            result = client.put(
                '/api/users',
                headers={'Authorization': 'Bearer {}'.format(token)}
            )
            self.assertEqual(400, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_USER_PUT,
                             result.get_json())

            result = client.put(
                '/api/users',
                headers={'Authorization': 'Bearer {}'.format(token)},
                json={'email': 'invalidemail'}
            )
            self.assertEqual(400, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_EMAIL,
                             result.get_json())

            result = client.put(
                '/api/users',
                headers={'Authorization': 'Bearer {}'.format(token)},
                json={'username': '!_invalidusername_!'}
            )
            self.assertEqual(400, result.status_code)
            self.assertEqual(TestData.EXPECTED_INVALID_USERNAME,
                             result.get_json())

            result = client.put(
                '/api/users',
                headers={'Authorization': 'Bearer {}'.format(token)},
                json=TestData.VALID_USER_PUT
            )
            self.assertEqual(200, result.status_code)
            self.assertEqual(TestData.EXPECTED_VALID_USER_PUT,
                             result.get_json())

    def test_delete_user(self):
        pass


if __name__ == '__main__':
    unittest.main()
