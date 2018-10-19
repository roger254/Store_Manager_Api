import unittest
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app import create_app, db


class AuthenticationTest(unittest.TestCase):
    """Test for auth Blueprint"""

    def setUp(self):
        """Init values"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user_data = {
            'user_name': 'roger254',
            'password': 'test123',
            'user_status': 'regular'
        }

        with self.app.app_context():
            # create tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        """Test user registration POST req."""

        response = self.client().post(
            '/auth/register',
            data=self.user_data
        )
        result = json.loads(response.data.decode())
        # test response message
        self.assertEqual(
            result['message'],
            "Registration Successful. Login!"
        )
        # test response status_code
        self.assertEqual(response.status_code, 201)

    def test_user_is_already_registered(self):
        """Test user can't  registered twice."""

        response = self.client().post(
            '/auth/register',
            data=self.user_data
        )
        self.assertEqual(response.status_code, 201)
        second_result = self.client().post(
            '/auth/register',
            data=self.user_data
        )
        self.assertEqual(second_result.status_code, 202)
        result = json.loads(second_result.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Login!")

    def test_user_login(self):
        """Test User Login"""

        response = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        result = self.client().post('/auth/login', data=self.user_data)
        # Response Code
        self.assertEqual(result.status_code, 201)

        # Test response message
        results_in_json = json.loads(result.data.decode())
        self.assertEqual(
            results_in_json['message'], "You've logged in successfully.")
        self.assertTrue(results_in_json['access_token'])

    def test_not_registered_user_login(self):
        """Test non registered user login"""

        fake_user = {
            'user_name': 'anonymous',
            'password': 'hack'
        }
        # Login
        response = self.client().post('/auth/login', data=fake_user)

        # status_code
        self.assertEqual(response.status_code, 401)
        # response message
        response_in_json = json.loads(response.data.decode())
        self.assertEqual(response_in_json['message'],
                         "Invalid User, Please try again"
                         )
