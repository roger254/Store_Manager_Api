import unittest
import os
import sys
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
            'sales_name': 'Sales 1',
            'sales_price': 11.0,
            'sales_quantity': 1
        }

        # connect app with content
        with self.app.app_context():
            # create tables
            db.create_all()

    def test_sale_creation(self):
        """Test API can create a Sale Order --> [POST] req"""

        response = self.client().post('/sales/', data=self.sale)
        # test correct response
        self.assertEqual(response.status_code, 201)
        # test data in response
        self.assertIn('Sales 1', str(response.data))

    def test_api_can_get_all_sales_orders(self):
        """Test the GET request"""

        response = self.client().post('/sales/', data=self.sale)
        # test response status_code
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/sales/')
        # test return status_code\
        self.assertEqual(response.status_code, 200)
        # test data
        self.assertIn('Sales 1', str(response.data))


if __name__ == "__main__":
    unittest.main()
