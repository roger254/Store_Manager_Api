import unittest
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app import create_app, db


class SalesTestCase(unittest.TestCase):
    """Represents Sales TestCase"""

    def setUp(self):
        """Initialize test client"""
        self.app = create_app(config_name='testing')
        self.app.testing = True
        self.client = self.app.test_client
        self.sale = {
            'sales_name': 'Sale 1',
            'sales_price': 11.0,
            'sales_quantity': 1
        }

        # connect app with content
        with self.app.app_context():
            # create tables
            db.create_all()

    def create_user(
        self,
        user_name='user1',
        password='test@123',
        user_status='regular'
    ):
        """Create a test user"""
        user_data = {
            'user_name': user_name,
            'password': password,
            'user_status': user_status
        }
        return self.client().post('/auth/register', data=user_data)

    def login_test_user(
        self,
        user_name='user1',
        password='test@123',
        user_status='regular'
    ):
        """Log in The test user Created"""
        user_data = {
            'user_name': user_name,
            'password': password,
            'user_status': user_status
        }
        return self.client().post('/auth/login', data=user_data)

    def test_sale_creation(self):
        """Test API can create a Sale Order --> [POST] req"""

        # register and login user
        self.create_user()
        login_response = self.login_test_user()
        # access_token
        access_token = json.loads(login_response.data.decode())['access_token']

        response = self.client().post(
            '/sales/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.sale
        )
        # test correct response
        self.assertEqual(response.status_code, 201)
        # test data in response
        self.assertIn('Sale 1', str(response.data))

    def test_api_can_get_all_sales_orders(self):
        """Test the GET request"""

        # register and login user
        self.create_user()
        login_response = self.login_test_user()
        # access_token
        return_data_in_json = json.loads(login_response.data.decode())
        access_token = return_data_in_json['access_token']

        response = self.client().post(
            '/sales/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.sale
        )
        # test response status_code
        self.assertEqual(response.status_code, 201)
        response = self.client().get(
            '/sales/',
            headers=dict(Authorization="Bearer " + access_token)
        )
        # test return status_code\
        self.assertEqual(response.status_code, 200)
        # test data
        self.assertIn('Sale 1', str(response.data))

    def test_api_can_get_specific_sale(self):
        """Test API can GET specific sale"""

        # register and login user
        self.create_user()
        login_response = self.login_test_user()
        # access_token
        return_data_in_json = json.loads(login_response.data.decode())
        access_token = return_data_in_json['access_token']

        response = self.client().post(
            '/sales/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.sale
        )
        # test the return status_code
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(
            response.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/sales/{}'.format(response_data['id']),
            headers=dict(Authorization="Bearer " + access_token)
        )
        # status_code
        self.assertEqual(result.status_code, 200)
        self.assertIn('Sale 1', str(result.data))


if __name__ == "__main__":
    unittest.main()
